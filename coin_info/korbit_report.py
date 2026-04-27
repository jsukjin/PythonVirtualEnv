#!/usr/bin/env python3
"""
코빗 보유코인 EMA 이격도 리포트 API
- GET /report : 전체 보유코인 EMA + 이격도 + 수익률
- GET /health : 서버 상태 확인
"""

import os
import hmac
import hashlib
import time
import urllib.parse
from datetime import datetime, timezone, timedelta

import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# ─── 환경변수 로드 (.env) ─────────────────────────────────────
load_dotenv()

API_KEY         = os.getenv("KORBIT_API_KEY", "")
API_SECRET      = os.getenv("KORBIT_API_SECRET", "")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "10"))
PORT            = int(os.getenv("FLASK_PORT", "5001"))
BASE_URL        = "https://api.korbit.co.kr/v2"

app = Flask(__name__)
API_AUTH_KEY = os.getenv("API_AUTH_KEY", "")

# ════════════════════════════════════════════════════════════
# 코빗 API 헬퍼
# ════════════════════════════════════════════════════════════

def sign(query_string: str) -> str:
    """HMAC-SHA256 서명 생성 (공식 문서 방식)"""
    return hmac.new(
        API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def signed_get(path: str, extra: dict = {}) -> dict:
    """인증이 필요한 GET 요청 (잔고 등)"""
    ts     = str(int(time.time() * 1000))
    params = {**extra, "timestamp": ts}
    qs     = urllib.parse.urlencode(params)
    sig    = sign(qs)
    url    = f"{BASE_URL}{path}?{qs}&signature={sig}"
    r      = requests.get(url, headers={"X-KAPI-KEY": API_KEY}, timeout=10)
    r.raise_for_status()
    return r.json()


def public_get(path: str, params: dict = {}) -> dict:
    """인증 불필요 GET 요청 (시세, 캔들 등)"""
    qs  = urllib.parse.urlencode(params)
    url = f"{BASE_URL}{path}?{qs}" if qs else f"{BASE_URL}{path}"
    r   = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


# ════════════════════════════════════════════════════════════
# EMA 계산
# ════════════════════════════════════════════════════════════

def calc_ema(prices: list, period: int):
    """지수이동평균 계산"""
    if len(prices) < period:
        return None
    k   = 2 / (period + 1)
    ema = sum(prices[:period]) / period  # SMA로 초기값
    for p in prices[period:]:
        ema = p * k + ema * (1 - k)
    return ema


# ════════════════════════════════════════════════════════════
# 포맷 헬퍼
# ════════════════════════════════════════════════════════════

def fmt_krw(n) -> str:
    return f"{round(n):,}원" if n is not None else "N/A"

def fmt_pct(d) -> str:
    if d is None:
        return "N/A"
    return f"{'+' if d >= 0 else ''}{d:.2f}%"

def dev_emoji(d) -> str:
    if d is None:  return "⚪"
    if d >  20:    return "🔴🔴"
    if d >  10:    return "🔴"
    if d >   5:    return "🟠"
    if d >  -5:    return "🟢"
    if d > -10:    return "🔵"
    if d > -20:    return "🔷"
    return "🔷🔷"


# ════════════════════════════════════════════════════════════
# 라우트
# ════════════════════════════════════════════════════════════

@app.route("/health")
def health():
    """서버 상태 확인"""
    return jsonify({
        "status": "ok",
        "time": datetime.now(timezone(timedelta(hours=9))).strftime("%Y.%m.%d %H:%M"),
        "api_key_set": bool(API_KEY),
    })


@app.route("/report")
def report():
    """전체 보유코인 EMA + 이격도 리포트"""
    if API_AUTH_KEY:
        key = request.headers.get("X-API-KEY", "")
        if key != API_AUTH_KEY:
            return jsonify({"error": "Unauthorized"}), 401
    try:
        if not API_KEY or not API_SECRET:
            return jsonify({"error": ".env에 API_KEY, API_SECRET을 입력하세요."}), 500

        # ── 1. 잔고 조회 ─────────────────────────────────────
        bal = signed_get("/balance")
        if not bal.get("success"):
            return jsonify({"error": "잔고 조회 실패", "detail": bal}), 500

        held = [
            {
                "currency":  b["currency"],
                "symbol":    f"{b['currency']}_krw",
                "balance":   float(b["balance"]),
                "avg_price": float(b.get("avgPrice") or 0),
            }
            for b in bal["data"]
            if b["currency"] != "krw" and float(b["balance"]) > 0
        ]

        if not held:
            return jsonify({"message": "⚠️ 보유 코인이 없습니다.", "data": []})

        # ── 2. 코인별 가격 + EMA 계산 ─────────────────────────
        results = []
        for coin in held:
            try:
                # 현재가
                ticker = public_get("/tickers", {"symbol": coin["symbol"]})
                price  = float(ticker["data"][0]["close"])

                # 일봉 캔들 최대 200개
                candles = public_get("/candles", {
                    "symbol":   coin["symbol"],
                    "interval": "1D",
                    "limit":    200,
                })
                closes = [float(c["close"]) for c in candles["data"]]
                closes.append(price)  # 현재가 포함

                # EMA 20 / 50 / 150 / 200
                e20  = calc_ema(closes, 20)
                e50  = calc_ema(closes, 50)
                e150 = calc_ema(closes, 150)
                e200 = calc_ema(closes, 200)

                # 이격도 (%)
                d20  = (price / e20  - 1) * 100 if e20  else None
                d50  = (price / e50  - 1) * 100 if e50  else None
                d150 = (price / e150 - 1) * 100 if e150 else None
                d200 = (price / e200 - 1) * 100 if e200 else None

                # 수익/손실
                avg      = coin["avg_price"]
                eval_krw = round(price * coin["balance"])
                cost_krw = round(avg * coin["balance"]) if avg > 0 else None
                pnl_krw  = eval_krw - cost_krw if cost_krw else None
                pnl_pct  = (price / avg - 1) * 100 if avg > 0 else None

                # 이격도 알림 (임계값 초과)
                alerts = [
                    f"EMA{p}({fmt_pct(d)})"
                    for p, d in [("20", d20), ("50", d50), ("150", d150), ("200", d200)]
                    if d is not None and abs(d) >= ALERT_THRESHOLD
                ]

                results.append({
                    "currency":     coin["currency"].upper(),
                    "balance":      coin["balance"],
                    "avg_price":    avg,
                    "price":        price,
                    "eval_krw":     eval_krw,
                    "cost_krw":     cost_krw,
                    "pnl_krw":      pnl_krw,
                    "pnl_pct":      pnl_pct,
                    "e20": e20, "e50": e50, "e150": e150, "e200": e200,
                    "d20": d20, "d50": d50, "d150": d150, "d200": d200,
                    "alerts":       alerts,
                    "candle_count": len(closes) - 1,
                })

            except Exception as e:
                results.append({"currency": coin["currency"].upper(), "error": str(e)})

        # ── 3. 텔레그램 메시지 포맷 ───────────────────────────
        kst = timezone(timedelta(hours=9))
        now = datetime.now(kst).strftime("%Y.%m.%d %H:%M")
        today = datetime.now(kst).strftime("%Y-%m-%d")

        total_eval = sum(r.get("eval_krw", 0) for r in results)
        total_cost = sum(r["cost_krw"] for r in results if r.get("cost_krw"))
        total_pct  = (total_eval / total_cost - 1) * 100 if total_cost > 0 else None
        total_pnl  = total_eval - total_cost if total_cost > 0 else None

        msg  = f"==== 📊 코인 ({today}) ====\n\n"
        msg += "📊 *코빗 보유코인 EMA 현황*\n"
        msg += f"🕘 {now} (KST)\n"
        if total_pnl is not None:
            c_emoji = "🔴" if total_pnl >= 0 else "🔵"
            s = "▲" if total_pnl >= 0 else "▼"
            msg += f"💼 투자한 금액 : `{total_cost:,}`원\n"
            msg += f"   평가금액   : `{total_eval:,}`원 {c_emoji} {s}{abs(total_pct):.2f}%  {'+' if total_pnl >= 0 else ''}{total_pnl:,}원\n"
        msg += "─" * 15 + "\n\n"

        for r in results:
            if "error" in r:
                msg += f"❌ *{r['currency']}* 오류: {r['error']}\n\n"
                continue

            s       = "▲" if (r.get("pnl_pct") or 0) >= 0 else "▼"
            pnl_str = ""
            if r.get("pnl_krw") is not None:
                c_emoji = "🔴" if r["pnl_krw"] >= 0 else "🔵"
                sign_c  = "+" if r["pnl_krw"] >= 0 else ""
                pnl_str = f" {c_emoji} {s}{abs(r['pnl_pct']):.2f}%  {sign_c}{r['pnl_krw']:,}원"

            msg += f"💰 *{r['currency']}/KRW*\n"
            msg += f"현재가: `{round(r['price']):,}`원{pnl_str}\n"
            msg += f"보유량: `{r['balance']}` | 평가: `{r['eval_krw']:,}`원\n"
            if r["avg_price"] > 0:
                msg += f"평균단가: `{round(r['avg_price']):,}`원\n"
            msg += f"\n📈 *이평선 & 이격도* (일봉 {r['candle_count']}개)\n"
            msg += f"┌ EMA\\_20 : `{fmt_krw(r['e20'])}`  {dev_emoji(r['d20'])} `{fmt_pct(r['d20'])}`\n"
            msg += f"├ EMA\\_50 : `{fmt_krw(r['e50'])}`  {dev_emoji(r['d50'])} `{fmt_pct(r['d50'])}`\n"
            msg += f"├ EMA150 : `{fmt_krw(r['e150'])}`  {dev_emoji(r['d150'])} `{fmt_pct(r['d150'])}`\n"
            msg += f"└ EMA200 : `{fmt_krw(r['e200'])}`  {dev_emoji(r['d200'])} `{fmt_pct(r['d200'])}`\n"
            if r["alerts"]:
                msg += f"\n⚠️ *이격도 ±{ALERT_THRESHOLD:.0f}% 초과* → {' | '.join(r['alerts'])}\n"
            msg += "\n"

        msg += "─" * 30 + "\n"
        msg += "🟢근접  🟠과매수주의  🔴과매수  🔵이평아래  🔷과매도"

        return jsonify({"message": msg, "data": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ════════════════════════════════════════════════════════════
# 실행
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 45)
    print("  코빗 EMA 리포트 API 서버 시작")
    print(f"  http://0.0.0.0:{PORT}/report")
    print(f"  http://0.0.0.0:{PORT}/health")
    print("=" * 45)
    app.run(host="0.0.0.0", port=PORT, debug=False)

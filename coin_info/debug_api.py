#!/usr/bin/env python3
"""
코빗 API + Flask 인증 진단 스크립트
Dev Container 안에서 실행: python debug_api.py
"""
import hmac, hashlib, time, urllib.parse, requests, os
from dotenv import load_dotenv

load_dotenv()

API_KEY      = os.getenv("KORBIT_API_KEY", "")
API_SECRET   = os.getenv("KORBIT_API_SECRET", "")
API_AUTH_KEY = os.getenv("API_AUTH_KEY", "")
FLASK_PORT   = os.getenv("FLASK_PORT", "5001")

print("=" * 50)
print("[ 1. 환경변수 확인 ]")
print(f"  API_KEY      : {repr(API_KEY[:6])}...  (길이: {len(API_KEY)})")
print(f"  API_SECRET   : {repr(API_SECRET[:6])}...  (길이: {len(API_SECRET)})")
print(f"  API_AUTH_KEY : {repr(API_AUTH_KEY[:6]) if API_AUTH_KEY else '(미설정)'}  (길이: {len(API_AUTH_KEY)})")

# 따옴표/공백 오염 체크
if API_KEY.startswith('"') or API_KEY.startswith("'"):
    print("  ⚠️  API_KEY에 따옴표 포함됨 → .env 파일 따옴표 제거 필요")
if " " in API_KEY:
    print("  ⚠️  API_KEY에 공백 포함됨")

print()
print("[ 2. 서명 생성 ]")
ts     = str(int(time.time() * 1000))
params = {"timestamp": ts}
qs     = urllib.parse.urlencode(params)
sig    = hmac.new(API_SECRET.encode("utf-8"), qs.encode("utf-8"), hashlib.sha256).hexdigest()
url    = f"https://api.korbit.co.kr/v2/balance?{qs}&signature={sig}"

print(f"  timestamp  : {ts}")
print(f"  signed str : {qs}")
print(f"  signature  : {sig}")
print(f"  URL        : {url}")

print()
print("[ 3. 코빗 API 호출 결과 ]")
try:
    r = requests.get(url, headers={"X-KAPI-KEY": API_KEY}, timeout=10)
    print(f"  HTTP 상태  : {r.status_code}")
    print(f"  응답 본문  : {r.text}")
except Exception as e:
    print(f"  연결 오류  : {e}")

print()
print("[ 4. Flask /report 인증 테스트 ]")
flask_url = f"http://localhost:{FLASK_PORT}/report"
try:
    # 인증키 없이 호출
    r_no_auth = requests.get(flask_url, timeout=10)
    print(f"  인증키 없음 → HTTP {r_no_auth.status_code} {'✅ 정상(인증없음)' if r_no_auth.status_code == 200 else '🔒 인증 필요'}")

    # 인증키 포함 호출
    if API_AUTH_KEY:
        r_auth = requests.get(flask_url, headers={"X-API-KEY": API_AUTH_KEY}, timeout=30)
        print(f"  인증키 포함 → HTTP {r_auth.status_code} {'✅ 성공' if r_auth.status_code == 200 else '❌ 실패'}")
    else:
        print("  API_AUTH_KEY 미설정 → 인증 테스트 생략")
except Exception as e:
    print(f"  Flask 연결 오류: {e}")

print()
print("[ 5. 서버 시각 비교 ]")
try:
    t = requests.get("https://api.korbit.co.kr/v2/time", timeout=5).json()
    server_ts = t["data"]["serverTime"]
    my_ts     = int(time.time() * 1000)
    diff      = abs(server_ts - my_ts)
    print(f"  서버 시각  : {server_ts}")
    print(f"  내 시각    : {my_ts}")
    print(f"  차이       : {diff}ms  {'✅ 정상' if diff < 5000 else '⚠️ 5초 초과 → 시각 동기화 필요'}")
except Exception as e:
    print(f"  시각 조회 실패: {e}")

print("=" * 50)

# 통합 검색 API 테스트 가이드

## 서버 실행

### 방법 1: 배치 파일 사용 (Windows)
```bash
run_server.bat
```

### 방법 2: 명령어로 직접 실행
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload
```

## 테스트 실행

서버가 실행된 상태에서 **새 터미널**을 열어 다음 명령어 실행:

```bash
python test_search_all_simple.py
```

## 예상 결과

```
============================================================
통합 검색 API 테스트 (/search/all)
============================================================

요청 URL: http://localhost:8002/search/all

활성화된 엔진:
  - Tavily: False
  - Serper (Google): True
  - Naver Blog: True
  - Naver News: True
  - DuckDuckGo: False

검색어: 파이썬
엔진별 최대 결과 수: 1

============================================================

✓ 검색 성공!

검색어: 파이썬
요청 결과 수 (desired_count): 3
실제 결과 수 (success_count): 3
성공 여부: True

============================================================
검색 결과 상세 (3개)
============================================================

[1] 출처: SERPER
제목: 파이썬 - 위키백과, 우리 모두의 백과사전
URL: https://ko.wikipedia.org/wiki/%ED%8C%8C%EC%9D%B4%EC%8D%AC
내용: 파이썬은 1991년 프로그래머인 귀도 반 로섬이 발표한 고급 프로그래밍 언어로...
검색 순위: 1

[2] 출처: NAVER_BLOG
제목: 클로드 AI 활용한 파이썬 기초 및 실무 과정
URL: https://blog.naver.com/songin06/224212880770
내용: 기초부터 심화까지 단계별로 구성된 로드맵과...
블로거: 소소한 일상?, 날짜: 20260311

[3] 출처: NAVER_NEWS
제목: 파이썬 활용 AI 프로그래밍 교육
URL: https://news.naver.com/...
내용: 파이썬을 활용한 인공지능 프로그래밍 교육이...
발행일: Mon, 15 Mar 2024 10:00:00 +0900

============================================================
테스트 완료!
============================================================
```

## 파라미터 변경

`test_search_all_simple.py` 파일에서 다음 값들을 수정하여 테스트:

```python
data = {
    "query": "검색어",              # 원하는 검색어로 변경
    "max_results": 3,               # 엔진별 결과 수 (1~10)
    "enable_tavily": True,          # True/False
    "enable_serper": True,
    "enable_naver_blog": True,
    "enable_naver_news": True,
    "enable_ddg": True
}
```

## Swagger UI로 테스트

브라우저에서 아래 URL 접속:
```
http://localhost:8002/docs
```

1. `/search/all` 엔드포인트 클릭
2. "Try it out" 버튼 클릭
3. Parameters 섹션에서 `KURT_HEADERAUTH_API_KEY` 입력: `KurtJang123456`
4. Request body 수정
5. "Execute" 버튼 클릭

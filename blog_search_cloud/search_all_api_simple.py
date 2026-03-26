#pip install requests

import requests
import json
import sys

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# API 설정
url = "http://localhost:8002/search/all"
headers = {
    "KURT_HEADERAUTH_API_KEY": "KurtJang123456",
    "Content-Type": "application/json"
}

# 테스트 요청 데이터 (1개씩만 검색)
data = {
    "query": "파이썬 강의 추천",  # 더 한국어 중심 결과를 위한 검색어
    "max_results": 1,
    "enable_tavily": True,
    "enable_serper": True,
    "enable_naver_blog": True,
    "enable_naver_news": True,
    "enable_ddg": True
}

print("="*60)
print("통합 검색 API 테스트 (/search/all)")
print("="*60)
print(f"\n요청 URL: {url}")
print(f"\n활성화된 엔진:")
print(f"  - Tavily: {data['enable_tavily']}")
print(f"  - Serper (Google): {data['enable_serper']}")
print(f"  - Naver Blog: {data['enable_naver_blog']}")
print(f"  - Naver News: {data['enable_naver_news']}")
print(f"  - DuckDuckGo: {data['enable_ddg']}")
print(f"\n검색어: {data['query']}")
print(f"엔진별 최대 결과 수: {data['max_results']}")
print("\n" + "="*60)

try:
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()

        print(f"\n✓ 검색 성공!")
        print(f"\n검색어: {result['query']}")
        print(f"요청 결과 수 (desired_count): {result['desired_count']}")
        print(f"실제 결과 수 (success_count): {result['success_count']}")
        print(f"성공 여부: {result['success']}")

        if result.get('errors'):
            print(f"\n⚠ 에러가 발생한 엔진:")
            for engine, error in result['errors'].items():
                print(f"  - {engine}: {error}")

        print(f"\n" + "="*60)
        print(f"검색 결과 상세 ({len(result['results'])}개)")
        print("="*60)

        for i, item in enumerate(result['results'], 1):
            print(f"\n[{i}] 출처: {item['source'].upper()}")
            print(f"제목: {item['title']}")
            print(f"URL: {item['url']}")
            snippet = item['snippet'][:150].replace('\n', ' ')
            print(f"내용: {snippet}...")

            # 추가 메타데이터
            if 'bloggername' in item:
                print(f"블로거: {item['bloggername']}, 날짜: {item['postdate']}")
            elif 'pubDate' in item:
                print(f"발행일: {item['pubDate']}")
            elif 'position' in item:
                print(f"검색 순위: {item['position']}")
            elif 'score' in item:
                print(f"관련도 점수: {item['score']}")

        print("\n" + "="*60)
        print("테스트 완료!")
        print("="*60)

    else:
        print(f"\n✗ 에러 발생!")
        print(f"응답 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")

except requests.exceptions.ConnectionError:
    print("\n✗ 서버 연결 실패!")
    print("먼저 run_server.bat를 실행하여 서버를 시작하세요.")
    print("또는 다른 터미널에서: python -m uvicorn main:app --host 127.0.0.1 --port 8002")
except Exception as e:
    print(f"\n✗ 예외 발생: {str(e)}")

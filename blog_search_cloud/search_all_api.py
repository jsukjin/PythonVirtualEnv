import requests
import json
import sys

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# API 설정
url = "http://localhost:8000/search/all"
headers = {
    "KURT_HEADERAUTH_API_KEY": "KurtJang123456",
    "Content-Type": "application/json"
}

# 테스트 요청 데이터 (1개씩만 검색)
data = {
    "query": "파이썬",
    "max_results": 1,
    "enable_tavily": True,
    "enable_serper": True,
    "enable_naver_blog": True,
    "enable_naver_news": True,
    "enable_ddg": True
}

print(f"요청 URL: {url}")
print(f"요청 데이터: {json.dumps(data, ensure_ascii=False, indent=2)}\n")

try:
    response = requests.post(url, headers=headers, json=data)

    print(f"응답 코드: {response.status_code}")
    print(f"응답 내용:\n")

    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))

        print(f"\n=== 검색 결과 요약 ===")
        print(f"검색어: {result['query']}")
        print(f"요청 결과 수 (desired_count): {result['desired_count']}")
        print(f"실제 결과 수 (success_count): {result['success_count']}")
        print(f"성공: {result['success']}")

        if result.get('errors'):
            print(f"\n에러:")
            print(json.dumps(result['errors'], ensure_ascii=False, indent=2))

        print(f"\n=== 검색 결과 상세 ===")
        for i, item in enumerate(result['results'], 1):
            print(f"\n{i}. [{item['source']}] {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   내용: {item['snippet'][:100]}...")
    else:
        print(f"에러 발생: {response.text}")

except Exception as e:
    print(f"예외 발생: {str(e)}")

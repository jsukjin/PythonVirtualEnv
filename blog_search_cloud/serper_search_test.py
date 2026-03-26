#pip install requests python-dotenv

import os
import sys
from dotenv import load_dotenv
import requests
import json

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# .env 파일에서 환경변수 로드
load_dotenv()

# Serper.dev API 키
API_KEY = os.getenv("SERP_API_KEY")
if not API_KEY:
    raise ValueError("SERP_API_KEY가 .env 파일에 설정되지 않았습니다.")

# 검색 실행
query = "파이썬 기초"
url = "https://google.serper.dev/search"

payload = json.dumps({
    "q": query,
    "gl": "kr",  # 국가: 한국
    "hl": "ko",  # 언어: 한국어
    "num": 5     # 결과 수
})

headers = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)

# 결과 출력
if response.status_code == 200:
    data = response.json()
    print(f"검색어: {query}\n")

    # 검색 결과
    for idx, item in enumerate(data.get('organic', []), 1):
        print(f"{idx}. {item['title']}")
        print(f"   URL: {item['link']}")
        print(f"   내용: {item.get('snippet', 'N/A')[:100]}...")
        print()

    # 관련 검색어
    if 'relatedSearches' in data:
        print("관련 검색어:")
        for related in data['relatedSearches'][:3]:
            print(f"  - {related['query']}")
else:
    print(f"에러 발생! 코드: {response.status_code}")
    print(f"상세 메시지: {response.text}")

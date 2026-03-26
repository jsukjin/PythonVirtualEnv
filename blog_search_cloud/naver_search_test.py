#pip install requests python-dotenv

import os
import sys
from dotenv import load_dotenv
import requests

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# .env 파일에서 환경변수 로드
load_dotenv()

# Naver API 키 설정
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
    raise ValueError("NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET이 .env 파일에 설정되지 않았습니다.")

# 검색 실행
query = "파이썬 기초"
search_type = "blog"  # blog, news, webkr, image 등
display = 5  # 검색 결과 출력 건수 (기본값: 10, 최대: 100)
sort = "sim"  # sim (정확도순), date (날짜순)

url = f"https://openapi.naver.com/v1/search/{search_type}.json"

headers = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

params = {
    "query": query,
    "display": display,
    "sort": sort
}

response = requests.get(url, headers=headers, params=params)

# 결과 출력
if response.status_code == 200:
    data = response.json()
    print(f"검색어: {query}")
    print(f"검색 타입: {search_type}")
    print(f"총 결과 수: {data.get('total', 0)}\n")

    for idx, item in enumerate(data.get('items', []), 1):
        print(f"{idx}. {item.get('title', '').replace('<b>', '').replace('</b>', '')}")
        print(f"   URL: {item.get('link', 'N/A')}")

        # 블로그인 경우
        if search_type == "blog":
            print(f"   블로거: {item.get('bloggername', 'N/A')}")
            print(f"   날짜: {item.get('postdate', 'N/A')}")

        # 뉴스인 경우
        elif search_type == "news":
            print(f"   언론사: {item.get('originallink', 'N/A')}")
            print(f"   날짜: {item.get('pubDate', 'N/A')}")

        description = item.get('description', 'N/A').replace('<b>', '').replace('</b>', '')
        print(f"   내용: {description[:100]}...")
        print()
else:
    print(f"에러 발생! 코드: {response.status_code}")
    print(f"상세 메시지: {response.text}")

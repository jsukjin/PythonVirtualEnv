#pip install tavily-python python-dotenv

import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# .env 파일에서 환경변수 로드
load_dotenv()

# Tavily API 키 설정
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY가 .env 파일에 설정되지 않았습니다.")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# 검색 실행
query = "파이썬 기초"
response = tavily_client.search(query, max_results=3)

# 결과 출력
print(f"검색어: {query}\n")
for idx, result in enumerate(response['results'], 1):
    print(f"{idx}. {result['title']}")
    print(f"   URL: {result['url']}")
    print(f"   내용: {result['content'][:100]}...")
    print()

#pip install duckduckgo-search

import sys

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# DuckDuckGo는 API 키가 필요 없습니다
from duckduckgo_search import DDGS

# 검색 실행
query = "파이썬 기초"

with DDGS() as ddgs:
    results = list(ddgs.text(query, max_results=3))

# 결과 출력
print(f"검색어: {query}\n")
for idx, result in enumerate(results, 1):
    print(f"{idx}. {result['title']}")
    print(f"   URL: {result['href']}")
    print(f"   내용: {result['body'][:100]}...")
    print()

#pip install requests python-dotenv

import os
from dotenv import load_dotenv
import requests
import json
import argparse
import sys

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# .env 파일에서 환경변수 로드
load_dotenv()

def search_serper(api_key, query, num_results=10, country="kr", language="ko",
                  search_type="search", include_answer_box=True):
    """
    Serper.dev Google Search API 실행

    Args:
        api_key: Serper.dev API 키
        query: 검색어
        num_results: 최대 결과 수 (기본값: 10)
        country: 국가 코드 (기본값: kr)
        language: 언어 코드 (기본값: ko)
        search_type: 검색 타입 "search", "images", "news", "places" (기본값: search)
        include_answer_box: Answer Box 포함 여부 (기본값: True)
    """
    try:
        url = f"https://google.serper.dev/{search_type}"

        payload = {
            "q": query,
            "gl": country,
            "hl": language,
            "num": num_results
        }

        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()

            result = {
                "success": True,
                "data": {
                    "searchParameters": data.get('searchParameters', {}),
                    "organic": data.get('organic', []),
                }
            }

            # Answer Box가 있으면 포함
            if include_answer_box and 'answerBox' in data:
                result["data"]["answerBox"] = data['answerBox']

            # 관련 검색어
            if 'relatedSearches' in data:
                result["data"]["relatedSearches"] = data['relatedSearches']

            # Knowledge Graph
            if 'knowledgeGraph' in data:
                result["data"]["knowledgeGraph"] = data['knowledgeGraph']

            return result
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serper.dev Google Search API")
    parser.add_argument("--api-key", default=os.getenv("SERP_API_KEY"),
                       help="Serper.dev API 키 (.env 파일에서 자동 로드)")
    parser.add_argument("--query", required=True, help="검색어")
    parser.add_argument("--num-results", type=int, default=10, help="최대 결과 수 (기본값: 10)")
    parser.add_argument("--country", default="kr", help="국가 코드 (기본값: kr)")
    parser.add_argument("--language", default="ko", help="언어 코드 (기본값: ko)")
    parser.add_argument("--search-type", choices=["search", "images", "news", "places"],
                       default="search", help="검색 타입 (기본값: search)")
    parser.add_argument("--no-answer-box", dest="include_answer_box", action="store_false",
                       help="Answer Box 제외")

    args = parser.parse_args()

    if not args.api_key:
        print("Error: SERP_API_KEY가 .env 파일에 없거나 --api-key 인자가 제공되지 않았습니다.")
        sys.exit(1)

    result = search_serper(
        api_key=args.api_key,
        query=args.query,
        num_results=args.num_results,
        country=args.country,
        language=args.language,
        search_type=args.search_type,
        include_answer_box=args.include_answer_box
    )

    # JSON 출력 (n8n이 파싱하기 쉽게)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 에러 시 종료 코드 1
    if not result["success"]:
        sys.exit(1)

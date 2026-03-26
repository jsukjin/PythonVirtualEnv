#pip install tavily-python python-dotenv

import os
from dotenv import load_dotenv
import json
import argparse
import sys
from tavily import TavilyClient

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# .env 파일에서 환경변수 로드
load_dotenv()

def search_tavily(api_key, query, max_results=5, search_depth="advanced",
                  include_answer=True, include_images=False, include_raw_content=False):
    """
    Tavily 검색 실행

    Args:
        api_key: Tavily API 키
        query: 검색어
        max_results: 최대 결과 수 (기본값: 5)
        search_depth: 검색 깊이 "basic" or "advanced" (기본값: advanced)
        include_answer: AI 생성 답변 포함 여부 (기본값: True)
        include_images: 이미지 포함 여부 (기본값: False)
        include_raw_content: 원본 콘텐츠 포함 여부 (기본값: False)
    """
    try:
        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_answer=include_answer,
            include_images=include_images,
            include_raw_content=include_raw_content
        )

        return {
            "success": True,
            "data": response
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tavily Search API")
    parser.add_argument("--api-key", default=os.getenv("TAVILY_API_KEY"),
                       help="Tavily API 키 (.env 파일에서 자동 로드)")
    parser.add_argument("--query", required=True, help="검색어")
    parser.add_argument("--max-results", type=int, default=5, help="최대 결과 수 (기본값: 5)")
    parser.add_argument("--search-depth", choices=["basic", "advanced"], default="advanced",
                       help="검색 깊이 (기본값: advanced)")
    parser.add_argument("--include-answer", action="store_true", default=True,
                       help="AI 답변 포함")
    parser.add_argument("--no-answer", dest="include_answer", action="store_false",
                       help="AI 답변 제외")
    parser.add_argument("--include-images", action="store_true",
                       help="이미지 포함")
    parser.add_argument("--include-raw-content", action="store_true",
                       help="원본 콘텐츠 포함")

    args = parser.parse_args()

    if not args.api_key:
        print("Error: TAVILY_API_KEY가 .env 파일에 없거나 --api-key 인자가 제공되지 않았습니다.")
        sys.exit(1)

    result = search_tavily(
        api_key=args.api_key,
        query=args.query,
        max_results=args.max_results,
        search_depth=args.search_depth,
        include_answer=args.include_answer,
        include_images=args.include_images,
        include_raw_content=args.include_raw_content
    )

    # JSON 출력 (n8n이 파싱하기 쉽게)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 에러 시 종료 코드 1
    if not result["success"]:
        sys.exit(1)

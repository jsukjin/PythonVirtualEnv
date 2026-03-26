#pip install duckduckgo-search

import json
import argparse
import sys

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def search_duckduckgo(query, max_results=10, region="kr-kr", safesearch="moderate",
                      timelimit=None, backend="api"):
    """
    DuckDuckGo 검색 실행

    Args:
        query: 검색어
        max_results: 최대 결과 수 (기본값: 10)
        region: 지역 설정 (기본값: kr-kr)
        safesearch: 안전 검색 "on", "moderate", "off" (기본값: moderate)
        timelimit: 시간 제한 "d"(day), "w"(week), "m"(month), "y"(year) (기본값: None)
        backend: 백엔드 "api", "html", "lite" (기본값: api)

    Returns:
        dict: 검색 결과
    """
    try:
        # Import inside function to avoid circular import issues
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(
                keywords=query,
                region=region,
                safesearch=safesearch,
                timelimit=timelimit,
                backend=backend,
                max_results=max_results
            ))

        return {
            "success": True,
            "provider": "duckduckgo",
            "data": {
                "query": query,
                "count": len(results),
                "results": results
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def search_duckduckgo_news(query, max_results=10, region="kr-kr", safesearch="moderate", timelimit=None):
    """
    DuckDuckGo 뉴스 검색

    Args:
        query: 검색어
        max_results: 최대 결과 수 (기본값: 10)
        region: 지역 설정 (기본값: "kr-kr")
        safesearch: 안전 검색 ("on", "moderate", "off")
        timelimit: 시간 제한 ("d", "w", "m", "y", None)

    Returns:
        dict: {"success": bool, "provider": "duckduckgo", "search_type": "news", "data": {...}}
    """
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.news(
                keywords=query,
                region=region,
                safesearch=safesearch,
                timelimit=timelimit,
                max_results=max_results
            ))

        return {
            "success": True,
            "provider": "duckduckgo",
            "search_type": "news",
            "data": {
                "query": query,
                "count": len(results),
                "results": results
            }
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "duckduckgo",
            "search_type": "news",
            "error": str(e)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DuckDuckGo Search")
    parser.add_argument("--query", required=True, help="검색어")
    parser.add_argument("--max-results", type=int, default=10, help="최대 결과 수 (기본값: 10)")
    parser.add_argument("--region", default="kr-kr", help="지역 설정 (기본값: kr-kr)")
    parser.add_argument("--safesearch", choices=["on", "moderate", "off"],
                       default="moderate", help="안전 검색 (기본값: moderate)")
    parser.add_argument("--timelimit", choices=["d", "w", "m", "y"],
                       help="시간 제한: d(day), w(week), m(month), y(year)")
    parser.add_argument("--backend", choices=["api", "html", "lite"],
                       default="api", help="백엔드 (기본값: api)")

    args = parser.parse_args()

    result = search_duckduckgo(
        query=args.query,
        max_results=args.max_results,
        region=args.region,
        safesearch=args.safesearch,
        timelimit=args.timelimit,
        backend=args.backend
    )

    # JSON 출력 (n8n이 파싱하기 쉽게)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 에러 시 종료 코드 1
    if not result["success"]:
        sys.exit(1)

import os
import requests

SEARXNG_URL = os.getenv("SEARXNG_URL", "http://searxng:8080")


def search_searxng(
    query,                  # 검색어 (필수)
    base_url=None,          # SearXNG 인스턴스 URL. None이면 .env의 SEARXNG_URL 사용 (기본: http://searxng:8080)
    categories="general",   # 검색 카테고리: "general"(웹) | "news"(뉴스) | "images"(이미지) | "videos" | "social_media" | "science" | "it"
    language="ko",          # 검색 언어: "ko"(한국어) | "en"(영어) | "ja"(일본어) | "all"(전체)
    max_results=10,         # 최대 결과 수. 페이지당 결과가 부족하면 자동으로 다음 페이지를 요청해 채움
    pageno=1,               # 시작 페이지 번호 (기본: 1)
    time_range=None,        # 검색 기간 필터: "day"(하루) | "week"(일주일) | "month"(한달) | "year"(1년) | None(전체)
    safesearch=1,           # 성인 콘텐츠 필터: 0(off) | 1(moderate, 기본) | 2(strict)
    engines=None,           # 사용할 검색엔진 지정. None이면 SearXNG settings.yml 기본 설정 사용
                            # 예: "google" | "bing" | "google,bing,duckduckgo"
):
    url = f"{base_url or SEARXNG_URL}/search"

    base_params = {
        "q": query,
        "format": "json",
        "language": language,
        "categories": categories,
        "safesearch": safesearch
    }
    if time_range:
        base_params["time_range"] = time_range
    if engines:
        base_params["engines"] = ",".join(engines) if isinstance(engines, list) else engines

    headers = {
        "X-Forwarded-For": "127.0.0.1",
        "X-Real-IP": "127.0.0.1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

    try:
        all_results = []
        last_data = {}
        current_page = pageno

        while len(all_results) < max_results:
            params = {**base_params, "pageno": current_page}
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            last_data = response.json()

            page_results = last_data.get("results", [])
            if not page_results:
                break

            all_results.extend(page_results)
            current_page += 1

        final_results = all_results[:max_results]

        return {
            "success": True,
            "provider": "searxng",
            "data": {
                "query": query,
                "count": len(final_results),
                "results": final_results,
                "unresponsive_engines": last_data.get("unresponsive_engines", [])
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

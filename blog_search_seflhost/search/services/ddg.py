import time
import random
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException, RatelimitException


def search_duckduckgo(
    query,                  # 검색어 (필수)
    max_results=10,         # 최대 결과 수 (기본: 10)
    region="kr-kr",         # 검색 지역/언어: "kr-kr"(한국) | "us-en"(미국) | "wt-wt"(전체) 등
    safesearch="moderate",  # 성인 콘텐츠 필터: "on"(차단) | "moderate"(적당) | "off"(해제)
    timelimit=None,         # 검색 기간 필터: "d"(하루) | "w"(일주일) | "m"(한달) | "y"(1년) | None(전체)
    backend="api",          # 요청 백엔드: "api" | "html" | "lite". api는 서버 환경에서 차단될 수 있어 html→lite 순으로 자동 폴백
):
    # Docker/서버 환경에서 api 백엔드는 차단 가능성 높음 → html → lite 순으로 폴백
    backends = ["html", "lite"] if backend == "api" else [backend]
    last_error = None

    for b in backends:
        try:
            time.sleep(random.uniform(1.0, 2.5))
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    keywords=query,
                    region=region,
                    safesearch=safesearch,
                    timelimit=timelimit,
                    backend=b,
                    max_results=max_results
                ))
            return {
                "success": True,
                "provider": "duckduckgo",
                "backend_used": b,
                "data": {"query": query, "count": len(results), "results": results}
            }
        except RatelimitException as e:
            last_error = f"Ratelimit [{b}]: {str(e)}"
            time.sleep(random.uniform(3.0, 6.0))
            continue
        except DuckDuckGoSearchException as e:
            last_error = f"DDG Error [{b}]: {str(e)}"
            continue
        except Exception as e:
            last_error = f"Unexpected [{b}]: {str(e)}"
            continue

    return {"success": False, "error": last_error}

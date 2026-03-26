import os
from tavily import TavilyClient


def search_tavily(
    query,                      # 검색어 (필수)
    api_key=None,               # Tavily API 키. None이면 .env의 TAVILY_API_KEY 사용
    max_results=5,              # 최대 결과 수 (기본: 5)
    search_depth="advanced",    # 검색 깊이: "basic"(빠름, 크레딧 1) | "advanced"(정확, 크레딧 2)
    include_answer=True,        # AI가 생성한 요약 답변 포함 여부
    include_images=False,       # 관련 이미지 URL 목록 포함 여부
    include_raw_content=False,  # 각 결과 페이지의 원본 HTML/텍스트 전체 포함 여부 (응답 크기 주의)
):
    api_key = api_key or os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"success": False, "error": "TAVILY_API_KEY가 필요합니다."}

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
        return {"success": True, "provider": "tavily", "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

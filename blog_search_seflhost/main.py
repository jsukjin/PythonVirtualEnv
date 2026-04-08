#pip install fastapi uvicorn tavily-python duckduckgo-search requests python-dotenv

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from search.router import router as search_router
# 새 프로젝트 추가 시: from another_project.router import router as another_router

load_dotenv()

app = FastAPI(
    title="Search API Server",
    description="Tavily, DuckDuckGo, Serper, Naver 통합 검색 API",
    version="1.0.0"
)

app.include_router(search_router, prefix="/search", tags=["Search"])
# 새 프로젝트 추가 시: app.include_router(another_router, prefix="/another", tags=["Another"])


@app.get("/")
async def root():
    return {
        "message": "Search API Server",
        "endpoints": {
            "individual_engines": {
                "tavily": "/search/tavily",
                "duckduckgo": "/search/duckduckgo",
                "serper": "/search/serper",
                "naver": "/search/naver",
                "searxng": "/search/searxng"
            },
            "integrated_search": {
                "blog": "/search/blog",
                "news": "/search/news",
                "all": "/search/all"
            }
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

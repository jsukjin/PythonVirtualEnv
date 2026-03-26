import os
import json
import requests as http_requests
from fastapi import APIRouter, HTTPException, Depends

from common.auth import verify_header_auth
from search.models import (
    TavilySearchRequest, DuckDuckGoSearchRequest, SerperSearchRequest,
    NaverSearchRequest, SearXNGSearchRequest,
    BlogSearchRequest, NewsSearchRequest, SearchAllRequest
)
from search.services.tavily import search_tavily
from search.services.serper import search_serper
from search.services.naver import search_naver
from search.services.ddg import search_duckduckgo
from search.services.searxng import search_searxng

router = APIRouter()


@router.post("/tavily")
async def tavily_endpoint(request: TavilySearchRequest, auth: str = Depends(verify_header_auth)):
    """Tavily 검색 API (Header Auth 필요)"""
    result = search_tavily(
        query=request.query,
        api_key=request.api_key,
        max_results=request.max_results,
        search_depth=request.search_depth,
        include_answer=request.include_answer,
        include_images=request.include_images,
        include_raw_content=request.include_raw_content
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/duckduckgo")
async def duckduckgo_endpoint(request: DuckDuckGoSearchRequest, auth: str = Depends(verify_header_auth)):
    """DuckDuckGo 검색 API (Header Auth 필요)"""
    result = search_duckduckgo(
        query=request.query,
        max_results=request.max_results,
        region=request.region,
        safesearch=request.safesearch,
        timelimit=request.timelimit,
        backend=request.backend
    )
    if not result["success"]:
        error_detail = result.get("error", "Unknown DDG Error")
        status_code = 429 if "202" in str(error_detail) else 500
        raise HTTPException(status_code=status_code, detail=error_detail)
    return result


@router.post("/serper")
async def serper_endpoint(request: SerperSearchRequest, auth: str = Depends(verify_header_auth)):
    """Serper.dev Google Search API (Header Auth 필요)"""
    result = search_serper(
        query=request.query,
        api_key=request.api_key,
        num_results=request.num_results,
        country=request.country,
        language=request.language,
        search_type=request.search_type,
        include_answer_box=request.include_answer_box
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/naver")
async def naver_endpoint(request: NaverSearchRequest, auth: str = Depends(verify_header_auth)):
    """Naver Search API (Header Auth 필요)"""
    result = search_naver(
        query=request.query,
        client_id=request.client_id,
        client_secret=request.client_secret,
        search_type=request.search_type,
        display=request.display,
        sort=request.sort,
        start=request.start
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
    return result


@router.post("/searxng")
async def searxng_endpoint(request: SearXNGSearchRequest, auth: str = Depends(verify_header_auth)):
    """SearXNG 검색 API (Header Auth 필요)"""
    base_url = request.base_url or os.getenv("SEARXNG_URL")
    if not base_url:
        raise HTTPException(
            status_code=400,
            detail="SEARXNG_URL이 필요합니다. .env에 설정하거나 요청에 base_url을 포함하세요."
        )
    result = search_searxng(
        query=request.query,
        base_url=base_url,
        categories=request.categories,
        language=request.language,
        max_results=request.max_results,
        pageno=request.pageno,
        time_range=request.time_range,
        safesearch=request.safesearch,
        engines=request.engines
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Unknown SearXNG error"))
    return result


@router.post("/blog")
async def blog_endpoint(request: BlogSearchRequest, auth: str = Depends(verify_header_auth)):
    """통합 블로그 검색 API (Header Auth 필요)"""
    results = {}
    errors = {}

    if "naver" in request.engines:
        r = search_naver(query=request.query, search_type="blog", display=request.max_results)
        if r["success"]:
            results["naver"] = r["data"]
        else:
            errors["naver"] = r.get("error")

    if "serper" in request.engines:
        r = search_serper(query=f"{request.query} blog", num_results=request.max_results)
        if r["success"]:
            results["serper"] = {"searchParameters": r["data"]["searchParameters"], "organic": r["data"]["organic"]}
        else:
            errors["serper"] = r.get("error")

    if "searxng" in request.engines:
        searxng_url = os.getenv("SEARXNG_URL")
        if searxng_url:
            r = search_searxng(query=f"{request.query} blog", base_url=searxng_url,
                               categories="general", language="ko", max_results=request.max_results)
            if r["success"]:
                results["searxng"] = r["data"]
            else:
                errors["searxng"] = r.get("error")
        else:
            errors["searxng"] = "SEARXNG_URL not configured"

    return {
        "success": len(results) > 0,
        "search_type": "blog",
        "query": request.query,
        "results": results,
        "errors": errors if errors else None
    }


@router.post("/news")
async def news_endpoint(request: NewsSearchRequest, auth: str = Depends(verify_header_auth)):
    """통합 뉴스 검색 API (Header Auth 필요)"""
    results = {}
    errors = {}

    if "naver" in request.engines:
        r = search_naver(query=request.query, search_type="news", display=request.max_results)
        if r["success"]:
            results["naver"] = r["data"]
        else:
            errors["naver"] = r.get("error")

    if "serper" in request.engines:
        r = search_serper(query=request.query, num_results=request.max_results, search_type="news")
        if r["success"]:
            results["serper"] = {"searchParameters": r["data"]["searchParameters"], "news": r["data"].get("organic", [])}
        else:
            errors["serper"] = r.get("error")

    if "duckduckgo" in request.engines:
        r = search_duckduckgo(query=request.query, max_results=request.max_results, region="kr-kr")
        if r["success"]:
            results["duckduckgo"] = r["data"]
        else:
            errors["duckduckgo"] = r.get("error")

    if "searxng" in request.engines:
        searxng_url = os.getenv("SEARXNG_URL")
        if searxng_url:
            r = search_searxng(query=request.query, base_url=searxng_url,
                               categories="news", language="ko", max_results=request.max_results)
            if r["success"]:
                results["searxng"] = r["data"]
            else:
                errors["searxng"] = r.get("error")
        else:
            errors["searxng"] = "SEARXNG_URL not configured"

    return {
        "success": len(results) > 0,
        "search_type": "news",
        "query": request.query,
        "results": results,
        "errors": errors if errors else None
    }


@router.post("/all")
async def all_endpoint(request: SearchAllRequest, auth: str = Depends(verify_header_auth)):
    """통합 전체 검색 API (Header Auth 필요)"""
    all_results = []
    errors = {}

    n_tavily     = request.tavily_max_results     or request.max_results
    n_serper     = request.serper_max_results     or request.max_results
    n_naver_blog = request.naver_blog_max_results or request.max_results
    n_naver_news = request.naver_news_max_results or request.max_results
    n_ddg        = request.ddg_max_results        or request.max_results
    n_searxng    = request.searxng_max_results    or request.max_results

    desired_count = sum([
        n_tavily     if request.enable_tavily     else 0,
        n_serper     if request.enable_serper     else 0,
        n_naver_blog if request.enable_naver_blog else 0,
        n_naver_news if request.enable_naver_news else 0,
        n_ddg        if request.enable_ddg        else 0,
        n_searxng    if request.enable_searxng    else 0,
    ])

    if request.enable_tavily:
        r = search_tavily(query=request.query, max_results=n_tavily,
                          search_depth="advanced", include_answer=False)
        if r["success"]:
            for item in r["data"].get("results", []):
                all_results.append({
                    "source": "tavily",
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("content", ""),
                    "score": item.get("score", 0)
                })
        else:
            errors["tavily"] = r.get("error")

    if request.enable_serper:
        r = search_serper(query=request.query, num_results=n_serper)
        if r["success"]:
            for item in r["data"].get("organic", [])[:n_serper]:
                all_results.append({
                    "source": "serper",
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "position": item.get("position", 0)
                })
        else:
            errors["serper"] = r.get("error")

    if request.enable_naver_blog:
        r = search_naver(query=request.query, search_type="blog", display=n_naver_blog)
        if r["success"]:
            for item in r["data"].get("items", []):
                all_results.append({
                    "source": "naver_blog",
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("description", ""),
                    "bloggername": item.get("bloggername", ""),
                    "postdate": item.get("postdate", "")
                })
        else:
            errors["naver_blog"] = r.get("error")

    if request.enable_naver_news:
        r = search_naver(query=request.query, search_type="news", display=n_naver_news)
        if r["success"]:
            for item in r["data"].get("items", []):
                all_results.append({
                    "source": "naver_news",
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("description", ""),
                    "originallink": item.get("originallink", ""),
                    "pubDate": item.get("pubDate", "")
                })
        else:
            errors["naver_news"] = r.get("error")

    if request.enable_ddg:
        r = search_duckduckgo(query=request.query, max_results=n_ddg, region="kr-kr")
        if r["success"]:
            for item in r["data"].get("results", []):
                all_results.append({
                    "source": "duckduckgo",
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", "")
                })
        else:
            errors["duckduckgo"] = r.get("error")

    if request.enable_searxng:
        searxng_url = os.getenv("SEARXNG_URL")
        if searxng_url:
            r = search_searxng(query=request.query, base_url=searxng_url,
                               max_results=n_searxng, engines=request.searxng_engines)
            if r["success"]:
                for item in r["data"].get("results", []):
                    all_results.append({
                        "source": "searxng",
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("content", ""),
                        "engine": item.get("engine", "")
                    })
            else:
                errors["searxng"] = r.get("error")
        else:
            errors["searxng"] = "SEARXNG_URL not configured"

    return {
        "success": len(all_results) > 0,
        "query": request.query,
        "desired_count": desired_count,
        "success_count": len(all_results),
        "results": all_results,
        "errors": errors if errors else None
    }

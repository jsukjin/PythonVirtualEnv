from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from test import test_post_handler, calculate_handler, user_info_handler
from search import search_all, search_naver_blog, search_naver_news, search_google

# 환경 변수 로드
load_dotenv()

app = FastAPI()

# API 키 검증 함수
def verify_api_key(kurt_api_key: str = Header(..., alias="KURT-API-KEY")):
    """
    API 키 검증
    Header에 KURT-API-KEY를 포함해야 함
    """
    expected_api_key = os.getenv("KURT_API_KEY")

    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: API key not set"
        )

    if kurt_api_key != expected_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return True

# n8n에서 데이터를 보낼 때 받을 데이터 구조 정의
class Item(BaseModel):
    name: str
    message: str

class CalculateItem(BaseModel):
    num1: float
    num2: float
    operation: str  # "add", "subtract", "multiply", "divide"

class UserItem(BaseModel):
    name: str
    email: str
    age: int

class SearchRequest(BaseModel):
    query: str
    enable_blog: Optional[bool] = True
    enable_news: Optional[bool] = True
    enable_google: Optional[bool] = True
    blog_count: Optional[int] = 10
    news_count: Optional[int] = 10
    google_count: Optional[int] = 10

@app.get("/") #http reuqest get
def read_root():
    return {"status": "ok", "info": "Python API is running inside Docker"}

@app.post("/n8n-test") #http request post
def test_post(item: Item):
    return test_post_handler(item)

@app.post("/calculate") #계산 API
def calculate(item: CalculateItem):
    return calculate_handler(item)

@app.post("/user-register") #사용자 등록 API
def register_user(item: UserItem):
    return user_info_handler(item)

@app.post("/blogauto-search/all") #통합 검색 API
def search_all_api(request: SearchRequest, authorized: bool = Depends(verify_api_key)):
    """
    블로그, 뉴스, 구글 통합 검색 API

    Parameters:
    - query: 검색 키워드 (필수)
    - enable_blog: 블로그 검색 활성화 (기본값: True)
    - enable_news: 뉴스 검색 활성화 (기본값: True)
    - enable_google: 구글 검색 활성화 (기본값: True)
    - blog_count: 블로그 검색 결과 개수 (기본값: 10)
    - news_count: 뉴스 검색 결과 개수 (기본값: 10)
    - google_count: 구글 검색 결과 개수 (기본값: 10)

    Returns:
    - status: 성공 여부 (success / partial_success / fail)
    - query: 검색 키워드
    - results: 검색 결과 (blog, news, google)
    - details: 각 검색의 성공/실패 정보
    """
    try:
        results = search_all(
            query=request.query,
            enable_blog=request.enable_blog,
            enable_news=request.enable_news,
            enable_google=request.enable_google,
            blog_count=request.blog_count,
            news_count=request.news_count,
            google_count=request.google_count
        )

        # 활성화된 검색의 성공/실패 확인
        details = {}
        enabled_count = 0
        success_count = 0

        if request.enable_blog:
            enabled_count += 1
            blog_success = len(results.get("blog", [])) > 0
            details["blog"] = "success" if blog_success else "fail"
            if blog_success:
                success_count += 1

        if request.enable_news:
            enabled_count += 1
            news_success = len(results.get("news", [])) > 0
            details["news"] = "success" if news_success else "fail"
            if news_success:
                success_count += 1

        if request.enable_google:
            enabled_count += 1
            google_success = len(results.get("google", [])) > 0
            details["google"] = "success" if google_success else "fail"
            if google_success:
                success_count += 1

        # 전체 상태 결정
        if success_count == 0:
            overall_status = "fail"
        elif success_count == enabled_count:
            overall_status = "success"
        else:
            overall_status = "partial_success"

        return {
            "status": overall_status,
            "query": request.query,
            "results": results,
            "details": details
        }
    except Exception as e:
        return {
            "status": "error",
            "query": request.query,
            "error": str(e)
        }

@app.post("/blogauto-search/blog") #블로그 검색 API
def search_blog_api(query: str, display: int = 10, authorized: bool = Depends(verify_api_key)):
    """
    네이버 블로그 검색 API

    Parameters:
    - query: 검색 키워드
    - display: 검색 결과 개수 (기본값: 10, 최대: 100)

    Returns:
    - status: 성공 여부
    - query: 검색 키워드
    - count: 결과 개수
    - results: 검색 결과 리스트
    """
    try:
        results = search_naver_blog(query, display)
        return {
            "status": "success",
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "error": str(e)
        }

@app.post("/blogauto-search/blog/news") #뉴스 검색 API
def search_news_api(query: str, display: int = 10, authorized: bool = Depends(verify_api_key)):
    """
    네이버 뉴스 검색 API

    Parameters:
    - query: 검색 키워드
    - display: 검색 결과 개수 (기본값: 10, 최대: 100)

    Returns:
    - status: 성공 여부
    - query: 검색 키워드
    - count: 결과 개수
    - results: 검색 결과 리스트
    """
    try:
        results = search_naver_news(query, display)
        return {
            "status": "success",
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "error": str(e)
        }

@app.post("/blogauto-search/google") #구글 검색 API
def search_google_api(query: str, num: int = 10, authorized: bool = Depends(verify_api_key)):
    """
    구글 검색 API

    Parameters:
    - query: 검색 키워드
    - num: 검색 결과 개수 (기본값: 10, 최대: 10)

    Returns:
    - status: 성공 여부
    - query: 검색 키워드
    - count: 결과 개수
    - results: 검색 결과 리스트
    """
    try:
        results = search_google(query, num)
        return {
            "status": "success",
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "error": str(e)
        }

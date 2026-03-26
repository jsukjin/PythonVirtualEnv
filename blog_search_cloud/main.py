#pip install fastapi uvicorn tavily-python duckduckgo-search requests python-dotenv

"""
통합 검색 API 서버 (Tavily, DuckDuckGo, Serper, Naver)

서버 실행:
  python main.py
  또는
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

API 문서:
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc

================================================================================
n8n에서 사용 방법 (HTTP Request 노드)
================================================================================

[공통 설정]
  - Request Method: POST
  - JSON/RAW Parameters: ON
  - Body Content Type: JSON

  [필수] Header Auth 설정:
    - Header Name: KURT_HEADERAUTH_API_KEY
    - Header Value: [.env의 KURT_HEADERAUTH_API_KEY 값]

  또는 Headers 탭에서 직접 추가:
    - Name: KURT_HEADERAUTH_API_KEY
    - Value: [.env의 KURT_HEADERAUTH_API_KEY 값]

Docker 환경:
  - localhost 대신 컨테이너 이름 또는 Docker 호스트 IP 사용
  - 예: http://search-api:8000 또는 http://host.docker.internal:8000

================================================================================
1. Tavily 검색 (AI 답변 포함)
================================================================================
  URL: http://localhost:8000/search/tavily

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬 기초",
    "max_results": 5,
    "search_depth": "advanced",
    "include_answer": true,
    "include_images": false,
    "include_raw_content": false
  }

  참고: api_key 필드는 생략 가능 (.env에서 자동 로드)

  Response 예시:
  {
    "success": true,
    "provider": "tavily",
    "data": {
      "query": "파이썬 기초",
      "answer": "AI가 생성한 답변...",
      "results": [
        {
          "title": "검색 결과 제목",
          "url": "https://example.com",
          "content": "검색 결과 내용...",
          "score": 0.95
        }
      ]
    }
  }

================================================================================
2. DuckDuckGo 검색 (무료, API 키 불필요)
================================================================================
  URL: http://localhost:8000/search/duckduckgo

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬 기초",
    "max_results": 10,
    "region": "kr-kr",
    "safesearch": "moderate",
    "timelimit": null,
    "backend": "api"
  }

  파라미터 설명:
    - query: 검색어 (필수)
    - max_results: 최대 결과 수 (기본값: 10)
    - region: 지역 설정 (기본값: "kr-kr")
    - safesearch: "on", "moderate", "off" (기본값: "moderate")
    - timelimit: "d"(day), "w"(week), "m"(month), "y"(year), null (기본값: null)
    - backend: "api", "html", "lite" (기본값: "api")

  Response 예시:
  {
    "success": true,
    "provider": "duckduckgo",
    "data": {
      "query": "파이썬 기초",
      "count": 10,
      "results": [
        {
          "title": "검색 결과 제목",
          "href": "https://example.com",
          "body": "검색 결과 내용..."
        }
      ]
    }
  }

================================================================================
3. Serper (Google Search) 검색
================================================================================
  URL: http://localhost:8000/search/serper

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬 기초",
    "num_results": 10,
    "country": "kr",
    "language": "ko",
    "search_type": "search",
    "include_answer_box": true
  }

  참고: api_key 필드는 생략 가능 (.env에서 자동 로드)

  파라미터 설명:
    - query: 검색어 (필수)
    - num_results: 최대 결과 수 (기본값: 10)
    - country: "kr", "us", "jp" 등 국가 코드 (기본값: "kr")
    - language: "ko", "en", "ja" 등 언어 코드 (기본값: "ko")
    - search_type: "search", "images", "news", "places" (기본값: "search")
    - include_answer_box: Answer Box 포함 여부 (기본값: true)

  Response 예시:
  {
    "success": true,
    "provider": "serper",
    "data": {
      "searchParameters": {
        "q": "파이썬 기초",
        "gl": "kr",
        "hl": "ko",
        "num": 10
      },
      "answerBox": {
        "snippet": "답변 박스 내용...",
        "title": "답변 제목"
      },
      "organic": [
        {
          "title": "검색 결과 제목",
          "link": "https://example.com",
          "snippet": "검색 결과 내용...",
          "position": 1
        }
      ],
      "relatedSearches": [
        {"query": "관련 검색어 1"},
        {"query": "관련 검색어 2"}
      ],
      "knowledgeGraph": {
        "title": "지식 그래프 제목",
        "description": "설명..."
      }
    }
  }

================================================================================
4. 통합 블로그 검색 (여러 엔진 동시 호출)
================================================================================
  URL: http://localhost:8000/search/blog

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬 기초",
    "engines": ["naver", "serper"],
    "max_results": 10
  }

  파라미터 설명:
    - query: 검색어 (필수)
    - engines: 사용할 검색 엔진 목록 (기본값: ["naver", "serper"])
    - max_results: 엔진별 최대 결과 수 (기본값: 10)

  Response 예시:
  {
    "success": true,
    "search_type": "blog",
    "query": "파이썬 기초",
    "results": {
      "naver": {
        "query": "파이썬 기초",
        "search_type": "blog",
        "total": 1234,
        "items": [...]
      },
      "serper": {
        "searchParameters": {...},
        "organic": [...]
      }
    },
    "errors": null
  }

================================================================================
5. 통합 뉴스 검색 (여러 엔진 동시 호출)
================================================================================
  URL: http://localhost:8000/search/news

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬",
    "engines": ["naver", "serper", "duckduckgo"],
    "max_results": 10
  }

  파라미터 설명:
    - query: 검색어 (필수)
    - engines: 사용할 검색 엔진 목록 (기본값: ["naver", "serper", "duckduckgo"])
    - max_results: 엔진별 최대 결과 수 (기본값: 10)

  Response 예시:
  {
    "success": true,
    "search_type": "news",
    "query": "파이썬",
    "results": {
      "naver": {
        "query": "파이썬",
        "search_type": "news",
        "items": [...]
      },
      "serper": {
        "searchParameters": {...},
        "news": [...]
      },
      "duckduckgo": {
        "query": "파이썬",
        "results": [...]
      }
    },
    "errors": null
  }

================================================================================
6. 통합 전체 검색 (모든 엔진 통합 제어)
================================================================================
  URL: http://localhost:8000/search/all

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬",
    "max_results": 3,
    "enable_tavily": false,
    "enable_serper": true,
    "enable_naver_blog": true,
    "enable_naver_news": true,
    "enable_ddg": false
  }

  파라미터 설명:
    - query: 검색어 (필수)
    - max_results: 엔진별 최대 검색 수 (기본값: 3)
    - enable_tavily: Tavily 검색 사용 여부 (기본값: false)
    - enable_serper: Serper 검색 사용 여부 (기본값: true)
    - enable_naver_blog: Naver 블로그 검색 사용 여부 (기본값: true)
    - enable_naver_news: Naver 뉴스 검색 사용 여부 (기본값: true)
    - enable_ddg: DuckDuckGo 검색 사용 여부 (기본값: false)

  Response 예시:
  {
    "success": true,
    "query": "파이썬",
    "desired_count": 9,
    "success_count": 9,
    "results": [
      {
        "source": "serper",
        "title": "검색 결과 제목",
        "url": "https://example.com",
        "snippet": "검색 결과 내용...",
        "position": 1
      },
      {
        "source": "naver_blog",
        "title": "블로그 제목",
        "url": "https://blog.naver.com/...",
        "snippet": "블로그 내용...",
        "bloggername": "블로거명",
        "postdate": "20240315"
      },
      {
        "source": "naver_news",
        "title": "뉴스 제목",
        "url": "https://news.naver.com/...",
        "snippet": "뉴스 내용...",
        "originallink": "https://...",
        "pubDate": "Mon, 15 Mar 2024 10:00:00 +0900"
      }
    ],
    "errors": null
  }

  참고:
    - desired_count: 활성화된 엔진 수 × max_results
    - success_count: 실제로 받은 결과 수
    - 모든 검색 결과가 하나의 배열로 통합됨
    - 각 결과는 source 필드로 출처를 구분

================================================================================
7. Naver 검색 (블로그, 뉴스, 웹문서)
================================================================================
  URL: http://localhost:8000/search/naver

  Headers (필수):
    KURT_HEADERAUTH_API_KEY: [.env의 KURT_HEADERAUTH_API_KEY 값]

  Request Body (JSON):
  {
    "query": "파이썬 기초",
    "search_type": "blog",
    "display": 10,
    "sort": "sim",
    "start": 1
  }

  참고: client_id, client_secret 필드는 생략 가능 (.env에서 자동 로드)

  파라미터 설명:
    - query: 검색어 (필수)
    - search_type: "blog", "news", "webkr", "image" 등 (기본값: "blog")
    - display: 검색 결과 출력 건수 (기본값: 10, 최대: 100)
    - sort: "sim"(정확도순), "date"(날짜순) (기본값: "sim")
    - start: 검색 시작 위치 (기본값: 1, 최대: 1000)

  Response 예시:
  {
    "success": true,
    "provider": "naver",
    "data": {
      "query": "파이썬 기초",
      "search_type": "blog",
      "total": 1234,
      "start": 1,
      "display": 10,
      "items": [
        {
          "title": "검색 결과 제목",
          "link": "https://blog.naver.com/...",
          "description": "검색 결과 내용...",
          "bloggername": "블로거명",
          "bloggerlink": "https://blog.naver.com/...",
          "postdate": "20240315"
        }
      ]
    }
  }

================================================================================
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Literal, Optional
import uvicorn
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# Header Auth 인증 함수
async def verify_header_auth(kurt_headerauth_api_key: str = Header(..., alias="KURT_HEADERAUTH_API_KEY", description="API 인증 키")):
    """
    Header Auth 인증 검증
    n8n에서 Header에 KURT_HEADERAUTH_API_KEY를 포함해서 요청
    """
    expected_key = os.getenv("KURT_HEADERAUTH_API_KEY")

    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="서버 인증 설정이 완료되지 않았습니다. KURT_HEADERAUTH_API_KEY를 .env에 설정하세요."
        )

    if kurt_headerauth_api_key != expected_key:
        raise HTTPException(
            status_code=403,
            detail="유효하지 않은 API 키입니다."
        )

    return kurt_headerauth_api_key

# Search modules
from tavily import TavilyClient
import requests
import json

# Local search modules
from ddg_search import search_duckduckgo, search_duckduckgo_news
from naver_search import search_naver

app = FastAPI(
    title="Search API Server",
    description="Tavily, DuckDuckGo, Serper, Naver 통합 검색 API",
    version="1.0.0"
)

# Request Models
class TavilySearchRequest(BaseModel):
    api_key: Optional[str] = Field(None, description="Tavily API 키 (생략시 .env에서 로드)")
    query: str = Field(..., description="검색어")
    max_results: int = Field(5, description="최대 결과 수")
    search_depth: Literal["basic", "advanced"] = Field("advanced", description="검색 깊이")
    include_answer: bool = Field(True, description="AI 답변 포함 여부")
    include_images: bool = Field(False, description="이미지 포함 여부")
    include_raw_content: bool = Field(False, description="원본 콘텐츠 포함 여부")

class DuckDuckGoSearchRequest(BaseModel):
    query: str = Field(..., description="검색어")
    max_results: int = Field(10, description="최대 결과 수")
    region: str = Field("kr-kr", description="지역 설정")
    safesearch: Literal["on", "moderate", "off"] = Field("moderate", description="안전 검색")
    timelimit: Optional[Literal["d", "w", "m", "y"]] = Field(None, description="시간 제한")
    backend: Literal["api", "html", "lite"] = Field("api", description="백엔드")

class SerperSearchRequest(BaseModel):
    api_key: Optional[str] = Field(None, description="Serper.dev API 키 (생략시 .env에서 로드)")
    query: str = Field(..., description="검색어")
    num_results: int = Field(10, description="최대 결과 수")
    country: str = Field("kr", description="국가 코드")
    language: str = Field("ko", description="언어 코드")
    search_type: Literal["search", "images", "news", "places"] = Field("search", description="검색 타입")
    include_answer_box: bool = Field(True, description="Answer Box 포함 여부")

class NaverSearchRequest(BaseModel):
    client_id: Optional[str] = Field(None, description="Naver Client ID (생략시 .env에서 로드)")
    client_secret: Optional[str] = Field(None, description="Naver Client Secret (생략시 .env에서 로드)")
    query: str = Field(..., description="검색어")
    search_type: Literal["blog", "news", "webkr", "image", "encyc", "cafearticle", "kin", "book", "doc"] = Field("blog", description="검색 타입")
    display: int = Field(10, description="검색 결과 출력 건수 (최대: 100)")
    sort: Literal["sim", "date"] = Field("sim", description="정렬 방법 (sim: 정확도순, date: 날짜순)")
    start: int = Field(1, description="검색 시작 위치 (최대: 1000)")

class BlogSearchRequest(BaseModel):
    query: str = Field(..., description="검색어")
    engines: list[Literal["naver", "serper"]] = Field(["naver", "serper"], description="사용할 검색 엔진 목록")
    max_results: int = Field(10, description="엔진별 최대 결과 수")

class NewsSearchRequest(BaseModel):
    query: str = Field(..., description="검색어")
    engines: list[Literal["naver", "serper", "duckduckgo"]] = Field(["naver", "serper", "duckduckgo"], description="사용할 검색 엔진 목록")
    max_results: int = Field(10, description="엔진별 최대 결과 수")

class SearchAllRequest(BaseModel):
    query: str = Field(..., description="검색어")
    max_results: int = Field(3, description="엔진별 최대 검색 수")
    enable_tavily: bool = Field(False, description="Tavily 검색 사용 여부")
    enable_serper: bool = Field(True, description="Serper 검색 사용 여부")
    enable_naver_blog: bool = Field(True, description="Naver 블로그 검색 사용 여부")
    enable_naver_news: bool = Field(True, description="Naver 뉴스 검색 사용 여부")
    enable_ddg: bool = Field(False, description="DuckDuckGo 검색 사용 여부")

# Endpoints
@app.post("/search/tavily")
async def search_tavily(
    request: TavilySearchRequest,
    auth: str = Depends(verify_header_auth)
):
    """Tavily 검색 API (Header Auth 필요)"""
    try:
        # API 키: 요청에서 제공되지 않으면 .env에서 로드
        api_key = request.api_key or os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise HTTPException(status_code=400, detail="TAVILY_API_KEY가 필요합니다.")

        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=request.query,
            max_results=request.max_results,
            search_depth=request.search_depth,
            include_answer=request.include_answer,
            include_images=request.include_images,
            include_raw_content=request.include_raw_content
        )

        return {
            "success": True,
            "provider": "tavily",
            "data": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/duckduckgo")
async def duckduckgo_endpoint(
    request: DuckDuckGoSearchRequest,
    auth: str = Depends(verify_header_auth)
):
    """DuckDuckGo 검색 API (Header Auth 필요)"""
    try:
        result = search_duckduckgo(
            query=request.query,
            max_results=request.max_results,
            region=request.region,
            safesearch=request.safesearch,
            timelimit=request.timelimit,
            backend=request.backend
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/serper")
async def search_serper(
    request: SerperSearchRequest,
    auth: str = Depends(verify_header_auth)
):
    """Serper.dev Google Search API (Header Auth 필요)"""
    try:
        # API 키: 요청에서 제공되지 않으면 .env에서 로드
        api_key = request.api_key or os.getenv("SERP_API_KEY")
        if not api_key:
            raise HTTPException(status_code=400, detail="SERP_API_KEY가 필요합니다.")

        url = f"https://google.serper.dev/{request.search_type}"

        payload = {
            "q": request.query,
            "gl": request.country,
            "hl": request.language,
            "num": request.num_results
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
                "provider": "serper",
                "data": {
                    "searchParameters": data.get('searchParameters', {}),
                    "organic": data.get('organic', []),
                }
            }

            if request.include_answer_box and 'answerBox' in data:
                result["data"]["answerBox"] = data['answerBox']

            if 'relatedSearches' in data:
                result["data"]["relatedSearches"] = data['relatedSearches']

            if 'knowledgeGraph' in data:
                result["data"]["knowledgeGraph"] = data['knowledgeGraph']

            return result
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Serper API Error: {response.text}"
            )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/naver")
async def search_naver_endpoint(
    request: NaverSearchRequest,
    auth: str = Depends(verify_header_auth)
):
    """Naver Search API (Header Auth 필요)"""
    try:
        # API 키: 요청에서 제공되지 않으면 .env에서 로드
        client_id = request.client_id or os.getenv("NAVER_CLIENT_ID")
        client_secret = request.client_secret or os.getenv("NAVER_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise HTTPException(status_code=400, detail="NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET이 필요합니다.")

        result = search_naver(
            client_id=client_id,
            client_secret=client_secret,
            query=request.query,
            search_type=request.search_type,
            display=request.display,
            sort=request.sort,
            start=request.start
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/blog")
async def search_blog(
    request: BlogSearchRequest,
    auth: str = Depends(verify_header_auth)
):
    """
    통합 블로그 검색 API (Header Auth 필요)
    여러 검색 엔진을 동시에 호출하여 블로그 검색 결과를 반환
    """
    results = {}
    errors = {}

    # Naver 블로그 검색
    if "naver" in request.engines:
        try:
            client_id = os.getenv("NAVER_CLIENT_ID")
            client_secret = os.getenv("NAVER_CLIENT_SECRET")

            if client_id and client_secret:
                naver_result = search_naver(
                    client_id=client_id,
                    client_secret=client_secret,
                    query=request.query,
                    search_type="blog",
                    display=request.max_results,
                    sort="sim",
                    start=1
                )
                if naver_result["success"]:
                    results["naver"] = naver_result["data"]
                else:
                    errors["naver"] = naver_result.get("error", "Unknown error")
            else:
                errors["naver"] = "NAVER_CLIENT_ID or NAVER_CLIENT_SECRET not configured"
        except Exception as e:
            errors["naver"] = str(e)

    # Serper 검색 (일반 검색, 블로그 필터링은 쿼리에 "blog" 추가)
    if "serper" in request.engines:
        try:
            api_key = os.getenv("SERP_API_KEY")

            if api_key:
                url = "https://google.serper.dev/search"
                payload = {
                    "q": f"{request.query} blog",
                    "gl": "kr",
                    "hl": "ko",
                    "num": request.max_results
                }
                headers = {
                    'X-API-KEY': api_key,
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, headers=headers, data=json.dumps(payload))

                if response.status_code == 200:
                    data = response.json()
                    results["serper"] = {
                        "searchParameters": data.get('searchParameters', {}),
                        "organic": data.get('organic', [])
                    }
                else:
                    errors["serper"] = f"API Error {response.status_code}: {response.text}"
            else:
                errors["serper"] = "SERP_API_KEY not configured"
        except Exception as e:
            errors["serper"] = str(e)

    return {
        "success": len(results) > 0,
        "search_type": "blog",
        "query": request.query,
        "results": results,
        "errors": errors if errors else None
    }

@app.post("/search/news")
async def search_news(
    request: NewsSearchRequest,
    auth: str = Depends(verify_header_auth)
):
    """
    통합 뉴스 검색 API (Header Auth 필요)
    여러 검색 엔진을 동시에 호출하여 뉴스 검색 결과를 반환
    """
    results = {}
    errors = {}

    # Naver 뉴스 검색
    if "naver" in request.engines:
        try:
            client_id = os.getenv("NAVER_CLIENT_ID")
            client_secret = os.getenv("NAVER_CLIENT_SECRET")

            if client_id and client_secret:
                naver_result = search_naver(
                    client_id=client_id,
                    client_secret=client_secret,
                    query=request.query,
                    search_type="news",
                    display=request.max_results,
                    sort="sim",
                    start=1
                )
                if naver_result["success"]:
                    results["naver"] = naver_result["data"]
                else:
                    errors["naver"] = naver_result.get("error", "Unknown error")
            else:
                errors["naver"] = "NAVER_CLIENT_ID or NAVER_CLIENT_SECRET not configured"
        except Exception as e:
            errors["naver"] = str(e)

    # Serper 뉴스 검색
    if "serper" in request.engines:
        try:
            api_key = os.getenv("SERP_API_KEY")

            if api_key:
                url = "https://google.serper.dev/news"
                payload = {
                    "q": request.query,
                    "gl": "kr",
                    "hl": "ko",
                    "num": request.max_results
                }
                headers = {
                    'X-API-KEY': api_key,
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, headers=headers, data=json.dumps(payload))

                if response.status_code == 200:
                    data = response.json()
                    results["serper"] = {
                        "searchParameters": data.get('searchParameters', {}),
                        "news": data.get('news', [])
                    }
                else:
                    errors["serper"] = f"API Error {response.status_code}: {response.text}"
            else:
                errors["serper"] = "SERP_API_KEY not configured"
        except Exception as e:
            errors["serper"] = str(e)

    # DuckDuckGo 뉴스 검색
    if "duckduckgo" in request.engines:
        try:
            ddg_result = search_duckduckgo_news(
                query=request.query,
                max_results=request.max_results,
                region="kr-kr"
            )
            if ddg_result["success"]:
                results["duckduckgo"] = ddg_result["data"]
            else:
                errors["duckduckgo"] = ddg_result.get("error", "Unknown error")
        except Exception as e:
            errors["duckduckgo"] = str(e)

    return {
        "success": len(results) > 0,
        "search_type": "news",
        "query": request.query,
        "results": results,
        "errors": errors if errors else None
    }

@app.post("/search/all")
async def search_all_api(
    request: SearchAllRequest,
    auth: str = Depends(verify_header_auth)
):
    """
    통합 전체 검색 API (Header Auth 필요)
    모든 검색 엔진을 제어하여 결과를 하나로 통합
    """
    all_results = []
    errors = {}
    desired_count = 0

    # 활성화된 엔진 수 계산
    enabled_engines = sum([
        request.enable_tavily,
        request.enable_serper,
        request.enable_naver_blog,
        request.enable_naver_news,
        request.enable_ddg
    ])
    desired_count = enabled_engines * request.max_results

    # Tavily 검색
    if request.enable_tavily:
        try:
            api_key = os.getenv("TAVILY_API_KEY")
            if api_key:
                client = TavilyClient(api_key=api_key)
                response = client.search(
                    query=request.query,
                    max_results=request.max_results,
                    search_depth="advanced",
                    include_answer=False
                )

                for item in response.get('results', []):
                    all_results.append({
                        "source": "tavily",
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "snippet": item.get('content', ''),
                        "score": item.get('score', 0)
                    })
            else:
                errors["tavily"] = "TAVILY_API_KEY not configured"
        except Exception as e:
            errors["tavily"] = str(e)

    # Serper 검색
    if request.enable_serper:
        try:
            api_key = os.getenv("SERP_API_KEY")
            if api_key:
                url = "https://google.serper.dev/search"
                payload = {
                    "q": request.query,
                    "gl": "kr",
                    "hl": "ko",
                    "num": request.max_results
                }
                headers = {
                    'X-API-KEY': api_key,
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, headers=headers, data=json.dumps(payload))

                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('organic', [])[:request.max_results]:
                        all_results.append({
                            "source": "serper",
                            "title": item.get('title', ''),
                            "url": item.get('link', ''),
                            "snippet": item.get('snippet', ''),
                            "position": item.get('position', 0)
                        })
                else:
                    errors["serper"] = f"API Error {response.status_code}"
            else:
                errors["serper"] = "SERP_API_KEY not configured"
        except Exception as e:
            errors["serper"] = str(e)

    # Naver 블로그 검색
    if request.enable_naver_blog:
        try:
            client_id = os.getenv("NAVER_CLIENT_ID")
            client_secret = os.getenv("NAVER_CLIENT_SECRET")

            if client_id and client_secret:
                naver_result = search_naver(
                    client_id=client_id,
                    client_secret=client_secret,
                    query=request.query,
                    search_type="blog",
                    display=request.max_results,
                    sort="sim",
                    start=1
                )

                if naver_result["success"]:
                    for item in naver_result["data"].get("items", []):
                        all_results.append({
                            "source": "naver_blog",
                            "title": item.get('title', ''),
                            "url": item.get('link', ''),
                            "snippet": item.get('description', ''),
                            "bloggername": item.get('bloggername', ''),
                            "postdate": item.get('postdate', '')
                        })
                else:
                    errors["naver_blog"] = naver_result.get("error", "Unknown error")
            else:
                errors["naver_blog"] = "NAVER_CLIENT_ID or NAVER_CLIENT_SECRET not configured"
        except Exception as e:
            errors["naver_blog"] = str(e)

    # Naver 뉴스 검색
    if request.enable_naver_news:
        try:
            client_id = os.getenv("NAVER_CLIENT_ID")
            client_secret = os.getenv("NAVER_CLIENT_SECRET")

            if client_id and client_secret:
                naver_result = search_naver(
                    client_id=client_id,
                    client_secret=client_secret,
                    query=request.query,
                    search_type="news",
                    display=request.max_results,
                    sort="sim",
                    start=1
                )

                if naver_result["success"]:
                    for item in naver_result["data"].get("items", []):
                        all_results.append({
                            "source": "naver_news",
                            "title": item.get('title', ''),
                            "url": item.get('link', ''),
                            "snippet": item.get('description', ''),
                            "originallink": item.get('originallink', ''),
                            "pubDate": item.get('pubDate', '')
                        })
                else:
                    errors["naver_news"] = naver_result.get("error", "Unknown error")
            else:
                errors["naver_news"] = "NAVER_CLIENT_ID or NAVER_CLIENT_SECRET not configured"
        except Exception as e:
            errors["naver_news"] = str(e)

    # DuckDuckGo 검색
    if request.enable_ddg:
        try:
            ddg_result = search_duckduckgo(
                query=request.query,
                max_results=request.max_results,
                region="kr-kr"
            )

            if ddg_result["success"]:
                for item in ddg_result["data"].get("results", []):
                    all_results.append({
                        "source": "duckduckgo",
                        "title": item.get('title', ''),
                        "url": item.get('href', ''),
                        "snippet": item.get('body', '')
                    })
            else:
                errors["duckduckgo"] = ddg_result.get("error", "Unknown error")
        except Exception as e:
            errors["duckduckgo"] = str(e)

    success_count = len(all_results)

    return {
        "success": success_count > 0,
        "query": request.query,
        "desired_count": desired_count,
        "success_count": success_count,
        "results": all_results,
        "errors": errors if errors else None
    }

@app.get("/")
async def root():
    """API 정보"""
    return {
        "message": "Search API Server",
        "endpoints": {
            "individual_engines": {
                "tavily": "/search/tavily",
                "duckduckgo": "/search/duckduckgo",
                "serper": "/search/serper",
                "naver": "/search/naver"
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
    # 서버 실행: python main.py
    # 또는: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)

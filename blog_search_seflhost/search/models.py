from pydantic import BaseModel, Field
from typing import Literal, Optional


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


class SearXNGSearchRequest(BaseModel):
    base_url: Optional[str] = Field(None, description="SearXNG 인스턴스 URL (생략시 .env에서 로드)")
    query: str = Field(..., description="검색어")
    categories: str = Field("general", description="검색 카테고리 (general, news, images, social_media 등)")
    language: str = Field("ko", description="검색 언어 (ko, en, ja 등)")
    max_results: int = Field(10, description="최대 결과 수")
    pageno: int = Field(1, description="페이지 번호")
    time_range: Optional[Literal["day", "week", "month", "year"]] = Field(None, description="시간 범위")
    safesearch: Literal[0, 1, 2] = Field(1, description="안전 검색 (0: off, 1: moderate, 2: strict)")
    engines: Optional[str] = Field(None, description="사용할 엔진 (쉼표 구분, 예: google,bing)")


class BlogSearchRequest(BaseModel):
    query: str = Field(..., description="검색어")
    engines: list[Literal["naver", "serper", "searxng"]] = Field(["naver", "serper"], description="사용할 검색 엔진 목록")
    max_results: int = Field(10, description="엔진별 최대 결과 수")


class NewsSearchRequest(BaseModel):
    query: str = Field(..., description="검색어")
    engines: list[Literal["naver", "serper", "duckduckgo", "searxng"]] = Field(["naver", "serper", "duckduckgo"], description="사용할 검색 엔진 목록")
    max_results: int = Field(10, description="엔진별 최대 결과 수")


class SearchAllRequest(BaseModel):
    query: str = Field(..., description="검색어")
    max_results: int = Field(3, description="엔진별 기본 최대 검색 수")
    enable_tavily: bool = Field(False, description="Tavily 검색 사용 여부")
    enable_serper: bool = Field(True, description="Serper 검색 사용 여부")
    enable_naver_blog: bool = Field(True, description="Naver 블로그 검색 사용 여부")
    enable_naver_news: bool = Field(True, description="Naver 뉴스 검색 사용 여부")
    enable_ddg: bool = Field(False, description="DuckDuckGo 검색 사용 여부")
    enable_searxng: bool = Field(False, description="SearXNG 검색 사용 여부")
    tavily_max_results: Optional[int] = Field(None, description="Tavily 개별 최대 결과 수")
    serper_max_results: Optional[int] = Field(None, description="Serper 개별 최대 결과 수")
    naver_blog_max_results: Optional[int] = Field(None, description="Naver 블로그 개별 최대 결과 수")
    naver_news_max_results: Optional[int] = Field(None, description="Naver 뉴스 개별 최대 결과 수")
    ddg_max_results: Optional[int] = Field(None, description="DuckDuckGo 개별 최대 결과 수")
    searxng_max_results: Optional[int] = Field(None, description="SearXNG 개별 최대 결과 수")
    searxng_engines: Optional[str] = Field(None, description="SearXNG에서 사용할 검색엔진 (쉼표 구분)")

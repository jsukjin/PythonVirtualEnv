import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')


def search_naver_blog(query: str, display: int = 10) -> List[Dict[str, str]]:
    """
    네이버 블로그 검색

    Args:
        query: 검색 키워드
        display: 검색 결과 개수 (기본값: 10, 최대 100)

    Returns:
        검색 결과 리스트 [{"url": "", "title": "", "content": ""}]
    """
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": min(display, 100),  # 최대 100개까지
        "sort": "sim"  # sim (유사도순), date (날짜순)
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get('items', []):
            results.append({
                "url": item.get('link', ''),
                "title": _remove_html_tags(item.get('title', '')),
                "content": _remove_html_tags(item.get('description', ''))
            })

        return results

    except requests.exceptions.RequestException as e:
        print(f"네이버 블로그 검색 오류: {e}")
        return []


def search_naver_news(query: str, display: int = 10) -> List[Dict[str, str]]:
    """
    네이버 뉴스 검색

    Args:
        query: 검색 키워드
        display: 검색 결과 개수 (기본값: 10, 최대 100)

    Returns:
        검색 결과 리스트 [{"url": "", "title": "", "content": ""}]
    """
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": min(display, 100),
        "sort": "sim"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get('items', []):
            results.append({
                "url": item.get('originallink', item.get('link', '')),
                "title": _remove_html_tags(item.get('title', '')),
                "content": _remove_html_tags(item.get('description', ''))
            })

        return results

    except requests.exceptions.RequestException as e:
        print(f"네이버 뉴스 검색 오류: {e}")
        return []


def search_google(query: str, num: int = 10) -> List[Dict[str, str]]:
    """
    구글 검색 (Custom Search JSON API)

    Args:
        query: 검색 키워드
        num: 검색 결과 개수 (기본값: 10, 최대 10)

    Returns:
        검색 결과 리스트 [{"url": "", "title": "", "content": ""}]
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": query,
        "num": min(num, 10)  # 한 번에 최대 10개
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get('items', []):
            results.append({
                "url": item.get('link', ''),
                "title": item.get('title', ''),
                "content": item.get('snippet', '')
            })

        return results

    except requests.exceptions.RequestException as e:
        print(f"구글 검색 오류: {e}")
        return []


def search_all(
    query: str,
    enable_blog: bool = True,
    enable_news: bool = True,
    enable_google: bool = True,
    blog_count: int = 10,
    news_count: int = 10,
    google_count: int = 10
) -> Dict[str, List[Dict[str, str]]]:
    """
    통합 검색 함수 - 블로그, 뉴스, 구글 검색을 선택적으로 수행

    Args:
        query: 검색 키워드
        enable_blog: 블로그 검색 활성화 여부 (기본값: True)
        enable_news: 뉴스 검색 활성화 여부 (기본값: True)
        enable_google: 구글 검색 활성화 여부 (기본값: True)
        blog_count: 블로그 검색 결과 개수 (기본값: 10)
        news_count: 뉴스 검색 결과 개수 (기본값: 10)
        google_count: 구글 검색 결과 개수 (기본값: 10)

    Returns:
        {
            "blog": [...],
            "news": [...],
            "google": [...]
        }
    """
    results = {
        "blog": [],
        "news": [],
        "google": []
    }

    if enable_blog:
        print(f"블로그 검색 중: {query}")
        results["blog"] = search_naver_blog(query, blog_count)
        print(f"블로그 검색 완료: {len(results['blog'])}개 결과")

    if enable_news:
        print(f"뉴스 검색 중: {query}")
        results["news"] = search_naver_news(query, news_count)
        print(f"뉴스 검색 완료: {len(results['news'])}개 결과")

    if enable_google:
        print(f"구글 검색 중: {query}")
        results["google"] = search_google(query, google_count)
        print(f"구글 검색 완료: {len(results['google'])}개 결과")

    return results


def _remove_html_tags(text: str) -> str:
    """
    HTML 태그 제거 (<b>, </b> 등)

    Args:
        text: HTML 태그가 포함된 텍스트

    Returns:
        HTML 태그가 제거된 텍스트
    """
    import re
    return re.sub(r'<[^>]+>', '', text)


if __name__ == "__main__":
    import sys
    import io

    # Windows 인코딩 문제 해결
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # 테스트 코드
    query = "파이썬 프로그래밍"

    # 모든 검색 수행
    print("=" * 50)
    print("모든 검색 수행")
    print("=" * 50)
    results = search_all(query, enable_blog=True, enable_news=True, enable_google=True)

    # 결과를 JSON 형식으로 출력
    print("\n" + "=" * 50)
    print("검색 결과 (JSON)")
    print("=" * 50)
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # 블로그만 검색
    print("\n" + "=" * 50)
    print("블로그만 검색")
    print("=" * 50)
    blog_only = search_all(query, enable_blog=True, enable_news=False, enable_google=False)
    print(json.dumps(blog_only, ensure_ascii=False, indent=2))

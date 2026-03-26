#pip install requests python-dotenv

"""
Naver Search API 검색 (n8n 연동용)

사용법:
  python naver_search.py --query "검색어" --client_id "YOUR_ID" --client_secret "YOUR_SECRET"
  python naver_search.py --query "검색어" --search_type "news" --display 10

.env 파일에 API 키가 있으면 --client_id, --client_secret 생략 가능
"""

import os
import sys
from dotenv import load_dotenv
import requests
import json
import argparse

# Windows 환경에서 UTF-8 인코딩 설정
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# .env 파일에서 환경변수 로드
load_dotenv()

def search_naver(client_id, client_secret, query, search_type="blog", display=10, sort="sim", start=1):
    """
    Naver Search API 검색

    Args:
        client_id: Naver Client ID
        client_secret: Naver Client Secret
        query: 검색어
        search_type: 검색 타입 (blog, news, webkr, image, etc.)
        display: 검색 결과 출력 건수 (기본값: 10, 최대: 100)
        sort: 정렬 방법 (sim: 정확도순, date: 날짜순)
        start: 검색 시작 위치 (기본값: 1, 최대: 1000)

    Returns:
        dict: {"success": bool, "provider": "naver", "data": {...}}
    """
    try:
        url = f"https://openapi.naver.com/v1/search/{search_type}.json"

        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        params = {
            "query": query,
            "display": display,
            "sort": sort,
            "start": start
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            # HTML 태그 제거
            for item in data.get('items', []):
                if 'title' in item:
                    item['title'] = item['title'].replace('<b>', '').replace('</b>', '')
                if 'description' in item:
                    item['description'] = item['description'].replace('<b>', '').replace('</b>', '')

            return {
                "success": True,
                "provider": "naver",
                "data": {
                    "query": query,
                    "search_type": search_type,
                    "total": data.get('total', 0),
                    "start": data.get('start', 1),
                    "display": data.get('display', display),
                    "items": data.get('items', [])
                }
            }
        else:
            return {
                "success": False,
                "provider": "naver",
                "error": f"API Error {response.status_code}: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "provider": "naver",
            "error": str(e)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naver Search API")
    parser.add_argument("--query", type=str, required=True, help="검색어")
    parser.add_argument("--client_id", type=str, default=None, help="Naver Client ID (생략시 .env에서 로드)")
    parser.add_argument("--client_secret", type=str, default=None, help="Naver Client Secret (생략시 .env에서 로드)")
    parser.add_argument("--search_type", type=str, default="blog",
                        help="검색 타입 (blog, news, webkr, image 등, 기본값: blog)")
    parser.add_argument("--display", type=int, default=10, help="검색 결과 출력 건수 (기본값: 10, 최대: 100)")
    parser.add_argument("--sort", type=str, default="sim", help="정렬 방법 (sim: 정확도순, date: 날짜순)")
    parser.add_argument("--start", type=int, default=1, help="검색 시작 위치 (기본값: 1)")

    args = parser.parse_args()

    # API 키: 인자로 제공되지 않으면 .env에서 로드
    client_id = args.client_id or os.getenv("NAVER_CLIENT_ID")
    client_secret = args.client_secret or os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        print(json.dumps({
            "success": False,
            "error": "NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET이 필요합니다."
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 검색 실행
    result = search_naver(
        client_id=client_id,
        client_secret=client_secret,
        query=args.query,
        search_type=args.search_type,
        display=args.display,
        sort=args.sort,
        start=args.start
    )

    # JSON 출력
    print(json.dumps(result, ensure_ascii=False, indent=2))

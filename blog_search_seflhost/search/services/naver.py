import os
import requests


def search_naver(
    query,                  # 검색어 (필수)
    client_id=None,         # Naver API Client ID. None이면 .env의 NAVER_CLIENT_ID 사용
    client_secret=None,     # Naver API Client Secret. None이면 .env의 NAVER_CLIENT_SECRET 사용
    search_type="blog",     # 검색 타입: "blog" | "news" | "webkr" | "image" | "encyc" | "cafearticle" | "kin" | "book" | "doc"
    display=10,             # 한 번에 가져올 결과 수 (기본: 10, 최대: 100)
    sort="sim",             # 정렬 기준: "sim"(정확도순) | "date"(최신순)
    start=1,                # 검색 시작 위치, 페이지네이션에 사용 (기본: 1, 최대: 1000)
):
    client_id = client_id or os.getenv("NAVER_CLIENT_ID")
    client_secret = client_secret or os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        return {"success": False, "error": "NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET이 필요합니다."}

    try:
        url = f"https://openapi.naver.com/v1/search/{search_type}.json"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        params = {"query": query, "display": display, "sort": sort, "start": start}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                if "title" in item:
                    item["title"] = item["title"].replace("<b>", "").replace("</b>", "")
                if "description" in item:
                    item["description"] = item["description"].replace("<b>", "").replace("</b>", "")

            return {
                "success": True,
                "provider": "naver",
                "data": {
                    "query": query,
                    "search_type": search_type,
                    "total": data.get("total", 0),
                    "start": data.get("start", 1),
                    "display": data.get("display", display),
                    "items": data.get("items", [])
                }
            }
        else:
            return {"success": False, "error": f"API Error {response.status_code}: {response.text}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

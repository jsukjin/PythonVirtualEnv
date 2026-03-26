import os
import json
import requests


def search_serper(
    query,                  # 검색어 (필수)
    api_key=None,           # Serper.dev API 키. None이면 .env의 SERP_API_KEY 사용
    num_results=10,         # 최대 결과 수 (기본: 10)
    country="kr",           # 검색 국가 코드: "kr"(한국) | "us"(미국) | "jp"(일본) 등 ISO 3166-1 alpha-2
    language="ko",          # 검색 언어 코드: "ko"(한국어) | "en"(영어) | "ja"(일본어) 등 ISO 639-1
    search_type="search",   # 검색 타입: "search"(웹) | "news"(뉴스) | "images"(이미지) | "places"(장소)
    include_answer_box=True, # Google Answer Box(바로 답변 박스) 결과 포함 여부
):
    api_key = api_key or os.getenv("SERP_API_KEY")
    if not api_key:
        return {"success": False, "error": "SERP_API_KEY가 필요합니다."}

    try:
        url = f"https://google.serper.dev/{search_type}"
        payload = {"q": query, "gl": country, "hl": language, "num": num_results}
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "provider": "serper",
                "data": {
                    "searchParameters": data.get("searchParameters", {}),
                    "organic": data.get("organic", []),
                }
            }
            if include_answer_box and "answerBox" in data:
                result["data"]["answerBox"] = data["answerBox"]
            if "relatedSearches" in data:
                result["data"]["relatedSearches"] = data["relatedSearches"]
            if "knowledgeGraph" in data:
                result["data"]["knowledgeGraph"] = data["knowledgeGraph"]
            return result
        else:
            return {"success": False, "error": f"Serper API Error {response.status_code}: {response.text}"}

    except Exception as e:
        return {"success": False, "error": str(e)}

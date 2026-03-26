"""
네이버 뉴스 검색 테스트 파일
실행 방법: python search_test_news.py
"""
import sys
import io
import json
from search import search_naver_news

# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_news_search():
    """네이버 뉴스 검색 테스트"""
    query = input("검색할 키워드를 입력하세요 (기본값: 파이썬 프로그래밍): ").strip()
    if not query:
        query = "파이썬 프로그래밍"

    display = input("검색 결과 개수 (기본값: 10): ").strip()
    display = int(display) if display.isdigit() else 10

    print("\n" + "=" * 50)
    print(f"네이버 뉴스 검색: {query}")
    print("=" * 50)

    results = search_naver_news(query, display)

    print(f"\n검색 결과: {len(results)}개")
    print("\n" + "=" * 50)
    print("결과 (JSON)")
    print("=" * 50)
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # 결과를 파일로 저장
    with open("news_search_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 결과가 news_search_results.json 파일로 저장되었습니다.")


if __name__ == "__main__":
    test_news_search()

"""
구글 검색 테스트 파일
실행 방법: python search_test_google.py
"""
import sys
import io
import json
from search import search_google

# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_google_search():
    """구글 검색 테스트"""
    query = input("검색할 키워드를 입력하세요 (기본값: python programming): ").strip()
    if not query:
        query = "python programming"

    num = input("검색 결과 개수 (기본값: 10, 최대: 10): ").strip()
    num = int(num) if num.isdigit() else 10
    num = min(num, 10)  # 최대 10개

    print("\n" + "=" * 50)
    print(f"구글 검색: {query}")
    print("=" * 50)

    results = search_google(query, num)

    print(f"\n검색 결과: {len(results)}개")
    print("\n" + "=" * 50)
    print("결과 (JSON)")
    print("=" * 50)
    print(json.dumps(results, ensure_ascii=False, indent=2))

    if len(results) == 0:
        print("\n⚠️  결과가 없습니다. API 키를 확인해주세요.")
        print("Google Cloud Console에서 Custom Search API를 활성화하고")
        print("API 키 권한을 확인하세요.")
    else:
        # 결과를 파일로 저장
        with open("google_search_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 결과가 google_search_results.json 파일로 저장되었습니다.")


if __name__ == "__main__":
    test_google_search()

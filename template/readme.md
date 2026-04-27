## how to debug

1. 서버 실행
python korbit_report.py

2. 다른 터미널에서 아래 코드 실행 (API_KEY는 수정)
python3 -c "import requests; r = requests.get('http://localhost:5001/report', headers={'X-API-KEY': 'MY_API_KEY'}); print(r.status_code, r.text[:200])"
 
# 1. 파이썬 경량 버전 사용
FROM python:3.9-slim

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. 라이브러리 목록 복사 및 설치
COPY requirements.txt .

# 이미지 빌드 시점에 설치하므로 속도가 매우 빠릅니다.
RUN pip install --no-cache-dir -r requirements.txt


# 4. 소스 코드 복사
COPY . .

# 5. 실행 환경 설정 (PATH 명시)
ENV PATH="/usr/local/bin:$PATH"

# 6. 기본 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim

WORKDIR /workspace

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 프로젝트 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 개발 도구 설치
RUN pip install --no-cache-dir \
    debugpy \
    pytest \
    pytest-asyncio \
    httpx \
    black \
    isort \
    pylint \
    python-dotenv

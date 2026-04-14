# Blog File Server


## Cloudflare
CNAME, files, kurtnote.com , DNS only

## NPM (Nginx Proxy Manager)
### proxy hots
source - files.kurttnoe.com
destination - http://kurtnote.com:9997

### certificates
files.kurtntoe.com (create로)
(enable - force SSL, HSTS enabled, HTTP2 surrport)

### diagram

외부 요청
https://files.kurtnote.com
        ↓
   NPM (80/443)
        ↓
http://kurtnote.com:9997   ← VPS 호스트의 9997 포트
        ↓
  Docker 포트 매핑
  "9997:8001"
  (호스트:컨테이너)
        ↓
  컨테이너 내부 8001
  uvicorn 실행 중



FastAPI 기반 파일 업로드/다운로드 서버.

## 구성

```
https://files.kurtnote.com
    → Nginx Proxy Manager
    → http://kurtnote.com:9997
    → Docker 컨테이너 (내부 포트 8001)
    → FastAPI (main.py)
```

## 실행

```bash
docker compose up -d --build
```

## API

### 파일 업로드 - `POST /upload`

**로컬 파일 업로드:**
```bash
curl -X POST https://files.kurtnote.com/upload \
  -F "file=@/path/to/image.jpg"
```

**URL로 이미지 저장:**
```bash
curl -X POST https://files.kurtnote.com/upload \
  -F "url=https://example.com/image.jpg"
```

**응답:**
```json
{
  "filename": "fb51ab44b9d84357b6384927916dc1e3.jpg",
  "url": "/files/fb51ab44b9d84357b6384927916dc1e3.jpg"
}
```

---

### 파일 접근 - `GET /files/{filename}`

```bash
curl https://files.kurtnote.com/files/fb51ab44b9d84357b6384927916dc1e3.jpg

# 파일로 저장
curl -O https://files.kurtnote.com/files/fb51ab44b9d84357b6384927916dc1e3.jpg
```

브라우저에서 바로 열기:
```
https://files.kurtnote.com/files/{파일명}
```

---

### Swagger UI

```
https://files.kurtnote.com/docs
```

## 로컬 개발

```bash
# Dev Container (VSCode)
# Ctrl+Shift+P → Dev Containers: Reopen in Container
# F5 → FastAPI 디버그 (uvicorn)

# 로컬 직접 실행
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

로컬 Swagger UI: `http://localhost:8001/docs`



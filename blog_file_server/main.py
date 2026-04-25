"""
FastAPI 파일 서버
- 파일 업로드 (직접 업로드 또는 URL로부터 다운로드 후 저장)
- 파일 다운로드 (/files/{파일명} 또는 /view/{파일명})
"""

import os
import uuid
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse

load_dotenv()

API_KEY = os.getenv("API_KEY", "")

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# -------------------------------------------------------
# 파일 저장 경로 설정
# 현재 실행 위치 기준으로 /files 폴더를 저장 경로로 사용
# -------------------------------------------------------
FILES_DIR = Path("./files")
FILES_DIR.mkdir(exist_ok=True)  # 폴더가 없으면 자동 생성


def make_unique_filename(original_name: str) -> str:
    """
    중복되지 않는 랜덤 파일명을 생성합니다.
    원본 파일의 확장자(예: .jpg, .pdf)는 유지됩니다.
    예) 원본: photo.jpg  →  결과: a3f2c1d4e5...jpg
    """
    # 원본 파일에서 확장자만 추출 (없으면 빈 문자열)
    ext = Path(original_name).suffix
    # UUID를 16진수 문자열로 변환하여 파일명으로 사용
    return f"{uuid.uuid4().hex}{ext}"


# -------------------------------------------------------
# 업로드 엔드포인트
# POST /upload
# -------------------------------------------------------
@app.post("/upload")
async def upload(
    file: UploadFile = File(None),
    url: str = Form(None),
    x_api_key: str = Header(None),
):
    """
    파일을 업로드합니다.

    두 가지 방식 지원:
    1. file: 로컬 파일을 직접 업로드 (multipart/form-data)
    2. url: 외부 URL을 전달하면 해당 파일을 다운로드하여 저장

    저장 시 중복을 방지하기 위해 UUID 기반 랜덤 파일명으로 저장됩니다.
    """

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="인증 실패: API Key가 올바르지 않습니다.")

    # file도 url도 전달되지 않은 경우 에러 반환
    if not file and not url:
        raise HTTPException(
            status_code=400,
            detail="'file' 또는 'url' 중 하나를 반드시 전달해야 합니다.",
        )

    if url:
        # ── URL 방식: 외부 URL에서 파일을 가져와 저장 ──────────────────────
        async with httpx.AsyncClient() as client:
            try:
                # URL에 GET 요청을 보내 파일 내용을 가져옴 (리다이렉트 자동 따라감)
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()  # HTTP 오류가 있으면 예외 발생
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"URL에서 파일을 가져오는 데 실패했습니다: {e}",
                )

        # URL 경로에서 파일명 추출 (쿼리 파라미터 제거)
        # 예) https://example.com/images/photo.jpg?token=abc → photo.jpg
        url_path = url.split("?")[0]
        original_name = url_path.split("/")[-1] or "downloaded_file"

        # 랜덤 파일명 생성 후 저장
        new_filename = make_unique_filename(original_name)
        file_path = FILES_DIR / new_filename
        file_path.write_bytes(response.content)

    else:
        # ── 파일 방식: 업로드된 파일을 직접 저장 ────────────────────────────
        new_filename = make_unique_filename(file.filename or "upload")
        file_path = FILES_DIR / new_filename

        # 파일 내용을 읽어서 디스크에 저장
        content = await file.read()
        file_path.write_bytes(content)

    # 저장된 파일명과 접근 URL을 반환
    return {
        "filename": new_filename,
        "url": f"/files/{new_filename}",
    }


# -------------------------------------------------------
# 다운로드 엔드포인트 1: /files/{파일명}
# GET /files/{filename}
# -------------------------------------------------------
@app.get("/files/{filename}")
async def download_by_files(filename: str):
    """
    /files/{파일명} 경로로 파일을 다운로드합니다.
    예) GET /files/a3f2c1d4e5.jpg
    """
    # 경로 조작 공격 방지: 파일명에 상위 폴더 이동 문자열이 있으면 차단
    file_path = (FILES_DIR / filename).resolve()
    if not str(file_path).startswith(str(FILES_DIR.resolve())):
        raise HTTPException(status_code=400, detail="잘못된 파일명입니다.")

    # 파일이 존재하지 않으면 404 오류 반환
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return FileResponse(path=file_path, filename=filename)


# -------------------------------------------------------
# 다운로드 엔드포인트 2: /view/{파일명}
# GET /view/{filename}
# -------------------------------------------------------
@app.get("/view/{filename}")
async def download_by_view(filename: str):
    """
    /view/{파일명} 경로로 브라우저에서 파일을 직접 표시합니다.
    예) GET /view/a3f2c1d4e5.jpg
    """
    # 경로 조작 공격 방지
    file_path = (FILES_DIR / filename).resolve()
    if not str(file_path).startswith(str(FILES_DIR.resolve())):
        raise HTTPException(status_code=400, detail="잘못된 파일명입니다.")

    # 파일이 존재하지 않으면 404 오류 반환
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return FileResponse(path=file_path)

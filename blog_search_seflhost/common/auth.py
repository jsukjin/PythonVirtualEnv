import os
from fastapi import HTTPException, Header


async def verify_header_auth(
    kurt_headerauth_api_key: str = Header(
        ..., alias="KURT_HEADERAUTH_API_KEY", description="API 인증 키"
    )
):
    expected_key = os.getenv("KURT_HEADERAUTH_API_KEY")

    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="서버 인증 설정이 완료되지 않았습니다. KURT_HEADERAUTH_API_KEY를 .env에 설정하세요."
        )

    if kurt_headerauth_api_key != expected_key:
        raise HTTPException(status_code=403, detail="유효하지 않은 API 키입니다.")

    return kurt_headerauth_api_key

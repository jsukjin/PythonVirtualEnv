import base64

USERNAME = "kurt"
APP_PASSWORD = "lQx4 1oTy 9lMN VDY6 7KMs ke96"

token = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
print(f"Base64:              {token}")
print(f"Authorization Header: Basic {token}")

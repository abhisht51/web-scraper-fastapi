from fastapi import HTTPException, Header
from typing import Optional

STATIC_TOKEN = "super-secret-token"

def verify_token(authorization: Optional[str] = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split("Bearer ")[-1]
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
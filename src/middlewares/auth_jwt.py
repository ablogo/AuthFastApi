from typing import Dict
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from src.services.jwt_service import verify_token

class JWTCustom(OAuth2PasswordBearer):

    def __init__(self, tokenUrl: str, scheme_name: str | None = None, scopes: Dict[str, str] | None = None, description: str | None = None, auto_error: bool = True):
        super().__init__(tokenUrl, scheme_name, scopes, description, auto_error)
    
    async def __call__(self, request: Request):
        try:
            token = await super().__call__(request)
            if token is not None:
                email = await verify_token(token)
                return email
        except Exception as e:
            raise e
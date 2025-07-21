from starlette.middleware.base import BaseHTTPMiddleware
from app.config.env import PRIVATE_ROUTES
from fastapi import Request, HTTPException
from fnmatch import fnmatch
from starlette.status import HTTP_401_UNAUTHORIZED
from app.config.utils import decode_token

class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == 'OPTIONS':
            return await call_next(request)
        if not any (fnmatch(request.url.path, route) for route in PRIVATE_ROUTES):
            return await call_next(request)
        
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="User not authorized"
            )
        token = auth_header.split(" ")[1]
        
        try:
            payload = decode_token(token=token)
            request.state.user_id = payload.get(
                '_id'
            )
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return await call_next(request)
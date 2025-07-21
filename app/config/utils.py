
from app.config.env import JWT_SECRET
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
import jwt
from fastapi.responses import JSONResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def success_response(status_code , data= None, message: str = "") -> JSONResponse :
    
    response_body = {
        "message": message,
        "data":data,
        "status": "success"
    }
    
    return JSONResponse(
        status_code=status_code,
        content=response_body,
    )

def create_token(data:dict, expires_delta:timedelta=timedelta(days=1)):
    encode_data = data.copy()
    expire_time = datetime.now(timezone.utc) + expires_delta
    encode_data.update({'exp': expire_time})
    encoded_data = jwt.encode(encode_data, JWT_SECRET, algorithm="HS256")
    return encoded_data


def decode_token(token:str):
    payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")
    return payload


def hash_password(password:str) -> str:
    return pwd_context.hash(password)


def verify_password(hash_password:str, plain_password) -> bool:
    return pwd_context.verify(plain_password, hash_password)

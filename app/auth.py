from datetime import datetime, timedelta
from typing import Optional
import os
from passlib.context import CryptContext
import jwt

PWD_CTX = CryptContext(schemes=["argon2"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret-dev-key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day by default


def verify_password(plain_password, hashed_password):
    return PWD_CTX.verify(plain_password, hashed_password)

def get_password_hash(password):
    return PWD_CTX.hash(password)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # pyjwt returns str in v2+
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload

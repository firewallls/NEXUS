from jose import JWTError, jwt
from datetime import datetime, timedelta
import os


def create_access_token(data: dict, expiry_time: int = 30) -> str:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now() + timedelta(minutes=expiry_time)})
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not set in environment variables")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
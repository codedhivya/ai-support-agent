from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import (
    SECRET_KEY,
    ALGORITHM
)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password :str):
    print("password:", password)
    print("length:", len(password))
    return pwd_context.hash(password)

def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
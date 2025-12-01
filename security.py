from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
from typing import Optional
from datetime import timedelta
import datetime
import jwt

load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")
hasher = PasswordHash.recommended()
ALGORITHM = 'HS256' 



def get_hased_password(password : str) -> str:
    return hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hasher.verify(plain_password, hashed_password)

def create_access_token(data : dict , expires_delta : Optional[timedelta] = None):
    to_encode = data.copy()
    expires = datetime.datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp' : expires})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt
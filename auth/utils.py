import time, os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.models import Student
from database.connector import get_db


load_dotenv(".env")

SECRETKEY = "whostolethemeatfromthecookingpot"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context=CryptContext(schemes=["bcrypt"])

class HashPass:
    pass

def create_hash(password:str):  
    return pwd_context.hash(password)
    
def verify_hash(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)



def create_access_token(data: dict):
    payload=data.copy()
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    payload.update({"exp":expire})
    token = jwt.encode(payload, SECRETKEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM])
        if time.time() > payload.get("exp"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(Student).filter(Student.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


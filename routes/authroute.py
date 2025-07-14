# Example usage in a router file
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, crede
from sqlalchemy.orm import Session
from database.connector import get_db
from database.models import Student
from fastapi import APIRouter, Depends
from auth.basic_auth import basic_auth_user

router = APIRouter()
security = HTTPBasic()

def basic_auth_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user = db.query(Student).filter(Student.username == credentials.username).first()
    if user:
        if credentials.password != user.password:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
            return user


@router.put("/update_a_student/{id}")
def update_student(id: int, user=Depends(basic_auth_user)):
    # Only authenticated users can update
    ...

@router.delete("/delete_a_student/{id}")
def delete_student(id: int, user=Depends(basic_auth_user)):
    return "Only authenticated users can delete"
    ...
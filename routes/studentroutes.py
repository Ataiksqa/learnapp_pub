from fastapi import APIRouter, status, HTTPException, Depends 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.studentmodel import CreateStudentModel as crt, UpdateStudentModel as upd, StudentModel as std
from database.crud import create_student, get_students, get_student_by_id, get_student_by_username, delete_student, update_student_email, update_student_details
from database.connector import get_db
from database.models import Student
from auth.utils import HashPass, pwd_context
from auth.models import User


student_router = APIRouter()


@student_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_new_student(student :crt, db: Session = Depends(get_db)): #,  email: str, grade: str, password: str,
    check_student = get_student_by_username(db=db, username=student.username)
    if check_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    hashed_pass = pwd_context.hash(student.password)
    student.password=hashed_pass
    return create_student(db=db, username=student.username, email=student.email, grade=student.grade, password=student.password)


@student_router.get("/students")
async def get_all_students(db: Session = Depends(get_db)):
    students = get_students(db=db)
    return students

@student_router.get("/{username}")
async def get_student_by_name(username: str, db: Session = Depends(get_db)):
    student = get_student_by_username(db=db, username=username)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student   
 
@student_router.get("/{id}")
async def get_student_by_ID(id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db=db, id=id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student   

@student_router.post("/basicauth", status_code=status.HTTP_200_OK)
async def sign_in(username:str, password:str, db:Session = Depends(get_db)):
    student= db.query(Student).filter(Student.username==username).first()
    if student:
        return student.password == password

@student_router.post("/hardauth", status_code=status.HTTP_200_OK)
async def sign_in_hard(username:str, password:str, db:Session = Depends(get_db)):
    student= db.query(Student).filter(Student.username==username).first()
    if student:
        if pwd_context.verify(password,str(student.password)):
            return "welcome to LearnApp, You're authorized"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@student_router.post("/sign_in", status_code=status.HTTP_200_OK) 
async def sign_in_student(user:User, db: Session = Depends(get_db)):# username: str, password, db: Session = Depends(get_db), hash_password: HashPass = Depends()):
    student = get_student_by_username(db=db, username=user.username)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    if not pwd_context.verify(user.password,str(student.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful", "student": student.username}

@student_router.delete("/{name}")#status_code=status.HTTP_204_NO_CONTENT,)
async def delete_a_student (name, db: Session = Depends(get_db)):
    return delete_student(db=db, username=name)


@student_router.put("/update_details/{id}", status_code=status.HTTP_201_CREATED)
async def update_details( id:int, details:upd, db:Session= Depends(get_db)):#, grade:None, email:None):
    student= update_student_details(db=db, id=id, updates=details)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


# new_details= update_student(db=db, id=id, username=upd.username, grade=upd.grade, email=upd.email)
    
#     # for key in dict(student.__dict__).keys():
#     #     print(key)
#         #     exists = item in updates
#         #     if exists:
#         #         student.key = update
#             # if key:
#             #     new_student.__dict__[id] = 
#     #     student.__dict__.items
#     #     print(f"{key} :=: ")

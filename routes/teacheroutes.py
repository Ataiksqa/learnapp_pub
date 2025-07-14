from fastapi import APIRouter, status, HTTPException, Depends 
from sqlalchemy.orm import Session
# from models.studentmodel import CreateStudentModel as crt
from models.teachermodel import CreateTeacherModel as tcm
from database.crud import create_teacher, get_teachers, get_teacher_by_id, get_teacher_by_username, delete_teacher, update_teacher_email
from database.connector import get_db

teacher_router = APIRouter(
    # prefix="/teacher",
    # tags=["teachers"],
)


@teacher_router.get("/teachers")
async def get_all_teachers(db: Session = Depends(get_db)):
    teachers = get_teachers(db=db)
    return teachers

@teacher_router.get("/{username}")
async def get_teacher_by_name(username: str, db: Session = Depends(get_db)):
    teacher = get_teacher_by_username(db=db, username=username)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teacher not found")
    return teacher   
 
@teacher_router.get("/{id}")
async def get_teacher_by_ID(id: int, db: Session = Depends(get_db)):
    teacher = get_teacher_by_id(db=db, id=id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teacher not found")
    return teacher   

@teacher_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_new_teacher(teacher :tcm, db: Session = Depends(get_db)): #,  email: str, grade: str, password: str,
    check_teacher = get_teacher_by_username(db=db, username=teacher.username)
    if check_teacher:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    return create_teacher(db=db, username=teacher.username, email=teacher.email, grades=teacher.grades, password=teacher.password)
   

@teacher_router.delete("/{name}")#status_code=status.HTTP_204_NO_CONTENT,)g
async def delete_a_teacher (name, db: Session = Depends(get_db)):
    return delete_teacher(db=db, username=name)

@teacher_router.put("/update_email/{username}", status_code=status.HTTP_201_CREATED)
async def update_teacher_email_route(username: str, new_email: str, db: Session = Depends(get_db)):
    teacher = update_teacher_email(username=username, new_email=new_email, db=db)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teacher not found")
    return teacher


from sqlalchemy.orm import Session
from fastapi import Depends
from .models import Student, Teacher, File
from fastapi import UploadFile


MAX_FILE_SIZE = 1024 * 1024 * 5  

# 5 MB
# #Dependenc
# def get_db():
#      db= SessionLocal()
#      try:
#          yield db
#      finally:
#          db.close()

def get_students(db: Session):
    return db.query(Student).all()


def create_student (db: Session,username: str, email :str, grade :str, password : str):
    db_user = Student (username=username, email=email, grade = grade, password = password )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    return db_user

def get_student_by_username (db: Session, username:str):
    return db.query(Student).filter(Student.username==username).first()

def get_student_by_id (db: Session, id:int):
    return db.query(Student).filter(Student.id==id).first()

def update_student_email(db:Session, username:str, new_email):
    student = db.query(Student).filter(Student.username==username).first()
    if student:
        student.email = new_email
        # student.grade = grade
        db.commit()
        db.refresh(student)
        return student

def update_student_grade(db:Session, username:str, new_grade):
    student = db.query(Student).filter(Student.username==username).first()
    if student:
        student.grade = new_grade
        db.commit()
        db.refresh(student)
        return student

def delete_student(db: Session, username: str):
    student = db.query(Student).filter(Student.username==username).first()
    if student:
        db.delete(student)
        db.commit()
        return {"message": f"Student {username} deleted successfully"}
    return {"message": f"Student {username} not found"} 

def update_student_details(db:Session, id:int, updates):
    student = db.query(Student).filter(Student.id==id).first()
    if not student:
        return None
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


#  new_student = {"username":username,
#                    "grade":grade,
#                  "email":email}

#     # for item in new_student.keys():
#     #     if new_student[item]:
#     #         print(new_student[item])
#     #         student.username=new_student["username"]    
    
#     try:
#         db._update_impl
#         db.commit()
#         db.refresh(student)
#     except Exception as e:
#         db.rollback()
#         raise e
#     finally:
#         db.close()
#     return student


###TEACHER CRUD OPERATIONS
###TEACHER CRUD OPERATIONS
###TEACHER CRUD OPERATIONS
###TEACHER CRUD OPERATIONS

def get_teachers(db: Session):
    return db.query(Teacher).all()

def create_teacher (db: Session,username: str, email :str, grades :str, password : str):
    db_user = Teacher (username=username, email=email, grades = grades, password = password )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    return db_user

def get_teacher_by_username (db: Session, username:str):
    return db.query(Teacher).filter(Teacher.username==username).first()

def get_teacher_by_id (db: Session, id:int):
    return db.query(Teacher).filter(Teacher.id==id).first()

def update_teacher_email(db:Session, username:str, new_email):
    teacher = db.query(Teacher).filter(Teacher.username==username).first()
    if teacher:
        teacher.email = new_email
        # teacher.grade = grade
        db.commit()
        db.refresh(teacher)
        return teacher

def update_teacher_grade(db:Session, username:str, new_grade):
    teacher = db.query(Teacher).filter(Teacher.username==username).first()
    if teacher:
        teacher.grades = new_grade
        db.commit()
        db.refresh(teacher)
        return teacher

def delete_teacher(db: Session, username: str):
    teacher = db.query(Teacher).filter(Teacher.username==username).first()
    if teacher:
        db.delete(teacher)
        db.commit()
        return {"message": f"Teacher {username} deleted successfully"}
    return {"message": f"Teacher {username} not found"} 


# def upload_image(db:Session, file:UploadFile = File()):
#     db_file=File(filename=file.filename,
#                   size=file.size, 
#                   type=file.content_type, 
#                   data=file.file.read())
#     try:
#         db.add(db_file)
#         db.commit()
#         db.refresh(db_file)
#     except Exception as e:
#         db.rollback()
        # raise e
  # 5 MB

def check_file_size(file_bytes: bytes, max_size: int = MAX_FILE_SIZE):
    if len(file_bytes) > max_size:
        raise ValueError(f"File size exceeds {max_size // (1024*1024)} MB limit.")
    
def save_file(db: Session, filename: str, path: str, content_type: str|None=None, user_id: int|None=None, size: int|None=None, data: bytes|None=None):
    db_file = File(filename=filename, 
                   content_type=content_type, 
                   path=path,
                   user_id=user_id, 
                   size=size, 
                   data=data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
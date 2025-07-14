import time, os
from fastapi import FastAPI, HTTPException, status, Depends, Form, middleware, Request, Response, UploadFile, File
from routes.studentroutes import student_router
from routes.filerouter import filerouter
# from routes.teacheroutes import teacher_router
from database.models import  Student
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.models import Token
from database.connector import get_db
from database.crud import get_student_by_id, save_file
from auth.utils import create_access_token, create_hash, verify_hash, get_current_user
from middleware import RateLimitMiddleware


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI(
    title="LearnApp API",
    description="API for the LearnApp application, managing students and teachers.",
    version="1.0.0",
    openapi_tags=[{"name":"Auth"}]
)
# import auth.cors
# app.add_middleware(RateLimitMiddleware)
#
@app.middleware("http")
async def add_process_time_header(request: Request, call_next ):
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

def auth_user(db, username, password):
    user = db.query(Student).filter(Student.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_hash(plain_password=password,hashed_password=user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user



@app.post("/token",response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=auth_user(db=db, username=form_data.username, password=form_data.password)
    if user:
        access_token = create_access_token(data={"sub":user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

@app.get("/myprofile")
async def who_are_me(user:Student = Depends(get_current_user)):
    return user

@app.post("/upload_image")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    
    file_location = os.path.join(UPLOAD_DIR, str(file.filename))
    print(f"Saving file to {file_location}")
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    try:
        file_to_db = save_file(db=db, filename=str(file.filename), content_type=file.content_type, path=file_location, size=file.size)  
        return {"filename": file_to_db.filename,
        "content_type": file_to_db.content_type,
        "path": file_to_db.path,
        "message": f"File{file.filename} uploaded and saved to database"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/upload_basic_file")
async def upload_basic_file(file: UploadFile =File(...)): #, db: Session = Depends(get_db)):
    contents= await file.read()
    print(f"File {file.filename} of type {file.content_type} received with size {len(contents)} bytes")

app.include_router(student_router, prefix="/student", tags=["students"])
#app.include_router(teacher_router, prefix="/teacher", tags=["teachers"])
app.include_router(filerouter, prefix="/File", tags=["files"])
# def on_startup():
#     Base.metadata.create_all(bind=Base.metadata.bind)
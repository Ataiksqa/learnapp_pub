from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class StudentModel(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the student")
    username: str= Field(..., description="Username of the student")
    email: str = Field(..., description="Email address of the student")
    grade: str = Field(..., description="class of the student")

class CreateStudentModel(StudentModel):
    password: str = Field(default="pass1234", description="Password for the student account")

class UpdateStudentModel(BaseModel):
    username :Optional[str]
    grade: Optional[str]
    email: Optional[str]
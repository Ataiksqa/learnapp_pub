from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class TeacherModel(BaseModel):
    username: str = Field(..., description="Username of the Teacher")
    email: EmailStr = Field(..., description="Email address of the Teacher")
    grades: str = Field(..., description="class of the Teacher")

class CreateTeacherModel(TeacherModel):
    password: str = Field(default="pass1234", description="Password for the Teacher account")


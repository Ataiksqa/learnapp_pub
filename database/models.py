from sqlalchemy import Column,Integer,String, LargeBinary, DateTime
from sqlalchemy.ext.declarative import  declarative_base
from .connector import engine

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    password = Column(String, unique=False, index=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    grade = Column(String, unique=False, index=False, nullable=True, default=0)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    password = Column(String, unique=False, index=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    subject = Column(String, unique=False, index=False)
    grades= Column(String, unique=False, index=False)

class File(Base):
    __tablename__="files"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String)
    user_id = Column(Integer, nullable=True)
    size = Column(Integer, unique=False, index=False)
    content_type = Column(String, unique=False, index=False)
    path = Column(String, unique=False, index=False)
    data=Column(LargeBinary, unique=False, index=False, nullable=True)
    uploaded_at=Column(DateTime, nullable=False,server_default="now()" )

# Base.metadata.drop_all(bind=engine)  # Drop all tables if they exist
Base.metadata.create_all(bind=engine)

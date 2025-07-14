from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv( override=True)

# from sqlalchemy.ext.declarative import 
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
print(SQLALCHEMY_DATABASE_URI)
engine= create_engine(SQLALCHEMY_DATABASE_URI, echo=True, connect_args= {"check_same_thread" : True})




SessionLocal= sessionmaker(autoflush=False, autocommit = False, bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

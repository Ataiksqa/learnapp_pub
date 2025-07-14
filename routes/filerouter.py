from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.connector import get_db
from database.crud import save_file, check_file_size, MAX_FILE_SIZE as MX
# from database.models import File

filerouter = APIRouter()

@filerouter.post("/upload_basic_file")
async def upload_basic_file(file: UploadFile = File(...)):
                            content=await file.read()
                            return file.filename, file.content_type, len(content)
                            # return JSONResponse(
                            #     content={"filename": file.filename, "content_type": file.content_type, "size": len(content)},
                            #     status_code=status.HTTP_200_OK
                            # )

@filerouter.post("/upload_file")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file:
        content = await file.read()
        try:
            check_file_size(content, max_size=MX)  # Check if file size exceeds 5 MB
            print(f"File {file.filename} of type {file.content_type} received with size {len(content)} bytes")  
            file_to_db = save_file(db=db, filename=str(file.filename), content_type=file.content_type, path="", size=file.size, data=content)
            return {
                "filename": file_to_db.filename,
                "content_type": file_to_db.content_type,
                "path": file_to_db.path,
                "size": file_to_db.size,
                "message": f"File  {file.filename} uploaded and saved to database"
            }
        except ValueError as ve:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
@filerouter.post("/upload_multiple_files")
async def upload_multiple_files(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided")
    
    uploaded_files = []
    for file in files:
        try:
            content = await file.read()
            check_file_size(content, max_size=MX)  # Check if file size exceeds
            file_to_db = save_file(db=db, filename=str(file.filename), content_type=file.content_type, path="", size=file.size)
            uploaded_files.append({
                "filename": file_to_db.filename,
                "content_type": file_to_db.content_type,
                "path": file_to_db.path,
                "message": f"File {file.filename} uploaded and saved to database"
            })
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return {"uploaded_files": uploaded_files}
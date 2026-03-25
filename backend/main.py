from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil
import uuid

from services.excel_service import parse_excel
from services.template_service import generate_docx
from fastapi import Form


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"
TEMPLATE_PATH = "template.docx"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

DATA_STORE = {}

# Upload Excel

@app.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    salary_file: UploadFile = File(...),
    doc_no: str = Form(...)
):
    if not file.filename.endswith(".xlsx") or not salary_file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx allowed")

    file_id = str(uuid.uuid4())

    main_path = os.path.join(UPLOAD_DIR, f"{file_id}_main.xlsx")
    salary_path = os.path.join(UPLOAD_DIR, f"{file_id}_salary.xlsx")


    with open(main_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(salary_path, "wb") as buffer:
        shutil.copyfileobj(salary_file.file, buffer)

    data = parse_excel(main_path)

    if not data:
        raise HTTPException(status_code=400, detail="Empty Excel")

  
    DATA_STORE[file_id] = {
        "data": data,
        "salary_path": salary_path,
        "doc_no": doc_no
    }

    return {
        "file_id": file_id,
        "total_candidates": len(data)
    }
    
@app.post("/generate/{file_id}")
def generate(file_id: str):
    if file_id not in DATA_STORE:
        raise HTTPException(status_code=404, detail="Invalid file_id")
 
    stored = DATA_STORE[file_id]
 
    data = stored["data"]
    salary_path = stored["salary_path"]
    doc_no = stored["doc_no"]   
 
   
    docx_records = generate_docx(data, TEMPLATE_PATH, salary_path, doc_no)
 
 
    return {
        "message": "Generated successfully",
        "results": docx_records
    }
 
 

@app.get("/download/{filename}")
def download(filename: str):
    file_path = os.path.join(TEMP_DIR, filename)  

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import Base, engine, SessionLocal
from schemas import ConversionResponse
from crud import save_conversion , get_latest_conversion
from utils import save_uploaded_file, convert_word_to_pdf,convert_html_to_pdf, convert_pdf_to_image_pdf ,convert_excel_to_pdf
import os
from fastapi.responses import FileResponse


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)

# Ensure dirs exist
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/converted", exist_ok=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/convert/word-to-pdf", response_model=ConversionResponse)
async def convert_word_to_pdf_api(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are allowed.")
    
    try:
        original_path = save_uploaded_file(file)
        converted_path = convert_word_to_pdf(original_path)
        
        conversion = save_conversion(
            db,
            original_filename=file.filename,
            original_path=original_path,
            converted_path=converted_path,
            conversion_type="word-to-pdf"
        )
        # ✅ Automatically download the converted file
        return FileResponse(
            path=converted_path,
            media_type="application/pdf",
            filename=os.path.basename(converted_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from crud import get_conversion_by_id



@app.post("/convert/html-to-pdf", response_model=ConversionResponse)
async def convert_html_to_pdf_api(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".html"):
        raise HTTPException(status_code=400, detail="Only .html files are allowed.")
    
    try:
        original_path = save_uploaded_file(file)
        converted_path = convert_html_to_pdf(original_path)

        conversion = save_conversion(
            db,
            original_filename=file.filename,
            original_path=original_path,
            converted_path=converted_path,
            conversion_type="html-to-pdf"
        )
        # ✅ Automatically download the converted file
        return FileResponse(
            path=converted_path,
            media_type="application/pdf",
            filename=os.path.basename(converted_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/pdf-to-image-pdf", response_model=ConversionResponse)
async def convert_pdf_to_image_pdf_api(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are allowed.")
    
    try:
        original_path = save_uploaded_file(file)
        converted_path = convert_pdf_to_image_pdf(original_path)

        conversion = save_conversion(
            db,
            original_filename=file.filename,
            original_path=original_path,
            converted_path=converted_path,
            conversion_type="pdf-to-image-pdf"
        )
       # ✅ Automatically download the converted file
        return FileResponse(
            path=converted_path,
            media_type="application/pdf",
            filename=os.path.basename(converted_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/convert/excel-to-pdf", response_model=ConversionResponse)
async def convert_excel_to_pdf_api(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx or .xls files are allowed.")
    
    try:
        original_path = save_uploaded_file(file)
        converted_path = convert_excel_to_pdf(original_path)

        conversion = save_conversion(
            db,
            original_filename=file.filename,
            original_path=original_path,
            converted_path=converted_path,
            conversion_type="excel-to-pdf"
        )
       # ✅ Automatically download the converted file
        return FileResponse(
            path=converted_path,
            media_type="application/pdf",
            filename=os.path.basename(converted_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/conversion/latest", response_model=ConversionResponse)
def get_latest_conversion_api(db: Session = Depends(get_db)):
    from crud import get_latest_conversion

    conversion = get_latest_conversion(db)
    if not conversion:
        raise HTTPException(status_code=404, detail="No recent conversion found.")
    return conversion

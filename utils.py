import os
import uuid
import subprocess
from pdf2image import convert_from_path
from PIL import Image
import os

UPLOAD_DIR = "static/uploads"
OUTPUT_DIR = "static/converted"
def save_uploaded_file(upload_file):
    filename = f"{uuid.uuid4()}_{upload_file.filename}"
    file_path = os.path.join("static/uploads", filename)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path.replace("\\", "/")

def convert_word_to_pdf(word_path):
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    os.makedirs("static/converted", exist_ok=True)

    result = subprocess.run([
        soffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", "static/converted",
        word_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception(f"LibreOffice conversion failed: {result.stderr.decode()}")

    # Extract filename from original
    filename_base = os.path.splitext(os.path.basename(word_path))[0]
    pdf_path = os.path.join("static/converted", f"{filename_base}.pdf")
    return pdf_path.replace("\\", "/")



def convert_html_to_pdf(html_path):
    import subprocess
    import os

    OUTPUT_DIR = "static/converted"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename_base = os.path.splitext(os.path.basename(html_path))[0]
    output_pdf_path = os.path.join(OUTPUT_DIR, f"{filename_base}.pdf")

    result = subprocess.run([
        "wkhtmltopdf",
        "--enable-local-file-access",
        "--load-error-handling", "ignore",          # ✅ suppress errors
        "--load-media-error-handling", "ignore",    # ✅ ignore CSS/JS/image load failures
        html_path,
        output_pdf_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode not in [0, 1]:  # 1 = handled warnings
        raise Exception(f"wkhtmltopdf failed: {result.stderr.decode()}")

    return output_pdf_path.replace("\\", "/")



def convert_pdf_to_image_pdf(pdf_path: str) -> str:
    OUTPUT_DIR = "static/converted"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Convert PDF to list of PIL images
    images = convert_from_path(pdf_path)

    # Output PDF path
    filename_base = os.path.splitext(os.path.basename(pdf_path))[0]
    output_pdf_path = os.path.join(OUTPUT_DIR, f"{filename_base}_image_converted.pdf")

    # Save all images into a single PDF
    images[0].save(
        output_pdf_path,
        "PDF",
        save_all=True,
        append_images=images[1:]
    )

    return output_pdf_path.replace("\\", "/")


def convert_excel_to_pdf(excel_path: str) -> str:
    OUTPUT_DIR = "static/converted"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build PDF output path
    filename_base = os.path.splitext(os.path.basename(excel_path))[0]
    output_pdf_path = os.path.join(OUTPUT_DIR, f"{filename_base}.pdf")

    # Convert using LibreOffice
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"  # Change if different
    result = subprocess.run([
        soffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", OUTPUT_DIR,
        excel_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise Exception(f"LibreOffice conversion failed: {result.stderr.decode()}")

    return output_pdf_path.replace("\\", "/")
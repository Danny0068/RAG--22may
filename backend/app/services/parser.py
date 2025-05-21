# The parser code has been moved to backend/app/services/parser.py as per the new project structure.
# Please use the new location for all imports and modifications.

import os
import pdfplumber
import pytesseract
from PIL import Image
from docx import Document

def parse_pdf(file_path):
    text_chunks = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                text = page.extract_text()
                if not text:
                    # Fallback to OCR
                    pil_img = page.to_image(resolution=300).original
                    text = pytesseract.image_to_string(pil_img)
                if text and text.strip():
                    text_chunks.append((f"{os.path.basename(file_path)} page {i+1}", text))
            except Exception as e:
                print(f"Error processing {file_path} page {i+1}: {e}")
    return text_chunks

def parse_docx(file_path):
    doc = Document(file_path)
    paragraphs = [(f"{os.path.basename(file_path)} para {i+1}", para.text)
                  for i, para in enumerate(doc.paragraphs) if para.text.strip()]
    return paragraphs

def parse_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return [(f"{os.path.basename(file_path)} image",text)]
import pytesseract
from paddleocr import PaddleOCR
from PIL import Image
import PyPDF2
import io
import os
from typing import List, Tuple, Dict
import json

class DocumentProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
    def process_document(self, file_content: bytes, filename: str) -> Dict:
        """Process a document and return its content and metadata"""
        file_type = filename.split('.')[-1].lower()
        
        if file_type in ['jpg', 'jpeg', 'png']:
            return self._process_image(file_content, filename)
        elif file_type == 'pdf':
            return self._process_pdf(file_content, filename)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _process_image(self, content: bytes, filename: str) -> Dict:
        """Process an image file using OCR"""
        image = Image.open(io.BytesIO(content))
        
        # Try PaddleOCR first (better for complex documents)
        result = self.ocr.ocr(numpy.array(image))
        if result and result[0]:
            text = '\n'.join([line[1][0] for line in result[0]])
        else:
            # Fallback to Tesseract
            text = pytesseract.image_to_string(image)
        
        return {
            'content': text,
            'metadata': {
                'filename': filename,
                'type': 'image',
                'is_scanned': 1,
                'ocr_text': text
            }
        }
    
    def _process_pdf(self, content: bytes, filename: str) -> Dict:
        """Process a PDF file"""
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        metadata = {
            'filename': filename,
            'type': 'pdf',
            'pages': len(pdf_reader.pages),
            'is_scanned': 0
        }
        
        # Extract text from each page
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            # If no text extracted, try OCR
            if not page_text.strip():
                # Convert PDF page to image and OCR
                # This requires additional PDF to image conversion
                # Implementation depends on your PDF processing library
                pass
            
            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        
        return {
            'content': text,
            'metadata': metadata
        } 
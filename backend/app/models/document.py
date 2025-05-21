from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
    metadata = Column(Text)  # JSON string of metadata
    vector_store_id = Column(String)  # Reference to FAISS index
    is_scanned = Column(Integer, default=0)  # 0 for text, 1 for scanned
    ocr_text = Column(Text, nullable=True)  # OCR processed text for scanned documents 
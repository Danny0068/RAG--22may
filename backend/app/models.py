from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class DocumentMetadata(BaseModel):
    filename: str
    upload_date: datetime
    type: str
    size: int

class Document(BaseModel):
    id: str
    filename: str
    content: str
    metadata: DocumentMetadata

class ThemeCitation(BaseModel):
    document_id: str
    page: Optional[int]
    paragraph: Optional[int]
    text: str

class Theme(BaseModel):
    name: str
    description: str
    citations: List[ThemeCitation]

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    selected_docs: List[str] = Field(default_factory=list)

class QueryResponse(BaseModel):
    themes: List[Theme]
    document_count: int

class ErrorResponse(BaseModel):
    detail: str 
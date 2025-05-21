# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.document_processor import DocumentProcessor
from app.services.theme_analyzer import ThemeAnalyzer
from app.services.supabase_service import SupabaseService
from app.models import QueryRequest, QueryResponse, Document, ErrorResponse
import os
from typing import List
from datetime import datetime

app = FastAPI(
    title="RAG API",
    description="API for Document Research and Theme Identification",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_processor = DocumentProcessor()
theme_analyzer = ThemeAnalyzer(api_key=os.getenv("GROQ_API_KEY"))
supabase_service = SupabaseService()

@app.post("/upload/", response_model=dict)
async def upload(files: List[UploadFile] = File(...)):
    """Upload and process documents."""
    try:
        for file in files:
            content = await file.read()
            
            # Process document
            processed = document_processor.process_document(content, file.filename)
            
            # Store in Supabase
            await supabase_service.store_document(
                file_content=content,
                filename=file.filename,
                metadata=processed['metadata']
            )
        
        return {"status": "Documents uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/", response_model=List[Document])
async def list_documents():
    """List all uploaded documents."""
    try:
        documents = await supabase_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query documents and analyze themes."""
    try:
        # Get selected documents
        documents = []
        if request.selected_docs:
            for doc_id in request.selected_docs:
                doc = await supabase_service.get_document(doc_id)
                if doc:
                    documents.append({
                        "id": doc_id,
                        "content": doc["content"],
                        "metadata": doc["metadata"]
                    })
        else:
            # Get all documents
            all_docs = await supabase_service.list_documents()
            for doc in all_docs:
                full_doc = await supabase_service.get_document(doc["id"])
                if full_doc:
                    documents.append({
                        "id": doc["id"],
                        "content": full_doc["content"],
                        "metadata": full_doc["metadata"]
                    })
        
        # Analyze themes
        themes = theme_analyzer.analyze_themes(documents, request.question)
        
        return QueryResponse(
            themes=themes.get("themes", []),
            document_count=len(documents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
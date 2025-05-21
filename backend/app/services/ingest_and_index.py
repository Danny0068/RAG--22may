# ingest_and_index.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.services.parser import parse_pdf, parse_docx, parse_image

def ingest_files(file_paths):
    all_chunks = []
    for path in file_paths:
        if path.endswith(".pdf"):
            chunks = parse_pdf(path)
        elif path.endswith(".docx"):
            chunks = parse_docx(path)
        elif path.endswith((".png", ".jpg", ".jpeg")):
            chunks = parse_image(path)
        else:
            continue
        for metadata, content in chunks:
            all_chunks.append(Document(page_content=content, metadata={"source": metadata}))
    return all_chunks

def build_vectorstore(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(split_docs, embeddings)
# main.py
from fastapi import FastAPI, UploadFile, File
from app.services.ingest_and_index import ingest_files, build_vectorstore
from app.services.qa_engine import setup_qa, ask_question
import os
from fastapi import Request

app = FastAPI()
vectorstore = None
qa_chain = None

@app.post("/upload/")
async def upload(files: list[UploadFile]):
    os.makedirs("temp", exist_ok=True)
    paths = []
    for f in files:
        path = f"temp/{f.filename}"
        with open(path, "wb") as out_file:
            content = await f.read()
            out_file.write(content)
        paths.append(path)

    docs = ingest_files(paths)
    global vectorstore, qa_chain
    vectorstore = build_vectorstore(docs)
    qa_chain = setup_qa(vectorstore)
    return {"status": "Documents uploaded and indexed."}

@app.post("/query/")
async def query(request: Request):
    data = await request.json()
    question = data.get("question")
    if qa_chain is None:
        return {"answer": "No documents indexed yet."}
    answer = ask_question(qa_chain, question)
    return {"answer": answer}
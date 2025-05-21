# qa_engine.py
import os
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def setup_qa(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa

def ask_question(qa, query):
    result = qa(query)
    answer = result['result']
    sources = "\n".join([f"- {doc.metadata['source']}" for doc in result['source_documents']])
    return f"{answer}\n\n*Citations:*\n{sources}"
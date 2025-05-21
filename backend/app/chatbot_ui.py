import streamlit as st
import requests
import os
import json
from datetime import datetime

# Get backend URL from environment variable or use default
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

st.title("Document Research & Theme Identification Chatbot")

# Sidebar for document management
with st.sidebar:
    st.header("Document Management")
    
    # Upload documents
    uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)
    if st.button("Process Documents") and uploaded_files:
        files = [("files", (f.name, f, "application/pdf" if f.name.endswith(".pdf") else "image/jpeg")) for f in uploaded_files]
        with st.spinner("Processing documents..."):
            res = requests.post(f"{BACKEND_URL}/upload/", files=files)
            st.write(res.json())
    
    # List uploaded documents
    st.subheader("Uploaded Documents")
    try:
        docs = requests.get(f"{BACKEND_URL}/documents/").json()
        selected_docs = []
        for doc in docs:
            if st.checkbox(f"{doc['filename']} ({datetime.fromisoformat(doc['upload_date']).strftime('%Y-%m-%d')})", key=doc['id']):
                selected_docs.append(doc['id'])
    except:
        st.warning("No documents uploaded yet")

# Main chat interface
st.header("Research Query")
user_input = st.text_input("Enter your research question:")

if st.button("Analyze") and user_input:
    with st.spinner("Analyzing documents..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/query/",
                json={
                    "question": user_input,
                    "selected_docs": selected_docs if 'selected_docs' in locals() else []
                }
            ).json()
            
            # Display themes
            for theme in response.get("themes", []):
                with st.expander(f"Theme: {theme['name']}"):
                    st.write(theme['description'])
                    
                    # Display citations
                    st.subheader("Citations")
                    for citation in theme['citations']:
                        st.markdown(f"""
                        **Document {citation['document_id']}**
                        - Page: {citation['page']}
                        - Paragraph: {citation['paragraph']}
                        - Text: {citation['text']}
                        """)
            
            st.info(f"Analyzed {response.get('document_count', 0)} documents")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.header("Chat History")
for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}")

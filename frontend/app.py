import streamlit as st
from api_client import APIClient
import os
from datetime import datetime

# Initialize API client
api_client = APIClient()

st.title("Document Research & Theme Identification Chatbot")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_docs" not in st.session_state:
    st.session_state.selected_docs = []

# Sidebar for document management
with st.sidebar:
    st.header("Document Management")
    
    # Upload documents
    uploaded_files = st.file_uploader(
        "Upload Documents", 
        type=["pdf", "jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    if st.button("Process Documents") and uploaded_files:
        try:
            with st.spinner("Processing documents..."):
                result = api_client.upload_documents(uploaded_files)
                st.success("Documents processed successfully!")
                st.session_state.selected_docs = []  # Reset selection
        except Exception as e:
            st.error(f"Error processing documents: {str(e)}")
    
    # List uploaded documents
    st.subheader("Uploaded Documents")
    try:
        docs = api_client.list_documents()
        if not docs:
            st.info("No documents uploaded yet")
        else:
            for doc in docs:
                if st.checkbox(
                    f"{doc['filename']} ({datetime.fromisoformat(doc['upload_date']).strftime('%Y-%m-%d')})",
                    key=doc['id'],
                    value=doc['id'] in st.session_state.selected_docs
                ):
                    if doc['id'] not in st.session_state.selected_docs:
                        st.session_state.selected_docs.append(doc['id'])
                else:
                    if doc['id'] in st.session_state.selected_docs:
                        st.session_state.selected_docs.remove(doc['id'])
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")

# Main chat interface
st.header("Research Query")
user_input = st.text_input("Enter your research question:")

if st.button("Analyze") and user_input:
    try:
        with st.spinner("Analyzing documents..."):
            response = api_client.query_documents(
                question=user_input,
                selected_docs=st.session_state.selected_docs
            )
            
            # Add to chat history
            st.session_state.history.append(("User", user_input))
            
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
            st.session_state.history.append(("Assistant", f"Found {len(response.get('themes', []))} themes"))
            
    except Exception as e:
        st.error(f"Error analyzing documents: {str(e)}")
        st.session_state.history.append(("Assistant", f"Error: {str(e)}"))

# Display chat history
st.header("Chat History")
for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}") 
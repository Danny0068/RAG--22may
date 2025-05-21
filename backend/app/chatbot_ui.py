import streamlit as st
import requests

st.title("RAG Chatbot")

# Upload PDFs
st.header("Upload Documents")
uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
if st.button("Upload") and uploaded_files:
    files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
    res = requests.post("http://localhost:8000/upload/", files=files)
    st.write(res.json())

# Chat interface
st.header("Ask a Question")
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Your question:")
if st.button("Send") and user_input:
    # You need to implement a /query endpoint in your FastAPI backend!
    res = requests.post("http://localhost:8000/query/", json={"question": user_input})
    answer = res.json().get("answer", "No answer")
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", answer))

for speaker, msg in st.session_state.history:
    st.markdown(f"**{speaker}:** {msg}")

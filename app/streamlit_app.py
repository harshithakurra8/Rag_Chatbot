import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.document_handler import upload_document
from app.rag_pipeline import answer_question

st.title("RAG Chatbot")

# Document upload
st.header("Upload a Document")
uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])
if uploaded_file is not None:
    class DummyFile:
        def __init__(self, file):
            self.file = file
    # Wrap the uploaded file to match your upload_document interface
    result = upload_document(DummyFile(uploaded_file))
    st.success(result.get("message", "Upload failed."))

# Chat interface
st.header("Ask a Question")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Your question:")
if st.button("Ask") and question:
    answer = answer_question(question)
    st.session_state.chat_history.append((question, answer))

# Display chat history
for q, a in st.session_state.chat_history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")


    #streamlit run app/streamlit_app.py

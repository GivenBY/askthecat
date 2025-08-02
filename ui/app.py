import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.query_engine import QueryEngine
from src.ingest import ingest_file
from src.chunker import chunk_text
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.groq_llm import GroqLLM, list_groq_models

st.set_page_config(page_title="RAG Study Assistant", layout="wide")
st.title("📚 RAG Study Assistant")
st.markdown("Ask questions from your own files using Retrieval-Augmented Generation (RAG).")

with st.sidebar:
    st.header("⚙️ Controls")
    
    available_models = list_groq_models()
    if not available_models:
        st.warning("⚠️ Could not fetch models from Groq. Check API key or internet.")
    model_choice = st.selectbox("Select a Groq LLM Model", available_models)

    st.header("📁 File Upload")
    uploaded_files = st.file_uploader(
        "Upload one or more files (PDF, DOCX, PPTX, or Images)",
        type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

if "messages" not in st.session_state:
    st.session_state.messages = []
if "engine" not in st.session_state:
    st.session_state.engine = None

if uploaded_files and st.session_state.engine is None:
    with st.spinner("Processing documents... This may take a moment."):
        all_chunks = []
        for uploaded_file in uploaded_files:
            text = ingest_file(uploaded_file)
            if text:
                chunks = chunk_text(text)
                all_chunks.extend(chunks)

        embedder = Embedder()
        vectors = embedder.embed(all_chunks)
        
        if vectors.size > 0:
            dim = vectors.shape[1]
            vector_store = VectorStore(dim=dim)
            vector_store.add(vectors, all_chunks)
            llm = GroqLLM(model=model_choice)

            st.session_state.engine = QueryEngine(
                llm=llm, 
                vector_store=vector_store, 
                embedder=embedder
            )
            st.success("Files processed successfully. You can now ask questions!")
        else:
            st.error("Could not extract any text from the uploaded files. Please check the files and try again.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your uploaded documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.engine:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.engine.ask(prompt)
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.warning("Please upload your documents first before asking a question.")
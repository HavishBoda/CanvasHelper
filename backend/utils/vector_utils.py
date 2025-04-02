from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# === Constants ===
CHROMA_DB_DIR = "chroma_db"

# === Utility Functions ===

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def create_vector_store(chunks, directory=None):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # For persistent vector store (course-wide)
    if directory:
        vectorstore = Chroma.from_texts(
            chunks,
            embedding=embedding,
            persist_directory=directory
        )
        vectorstore.persist()
    else:
        # For session-based (in-memory)
        vectorstore = Chroma.from_texts(
            chunks,
            embedding=embedding
        )
    return vectorstore

def load_vector_store(directory):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=directory, embedding_function=embedding)
    return vectorstore
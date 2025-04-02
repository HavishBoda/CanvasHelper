from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils.canvas_utils import get_courses, get_course_files, download_file
from utils.vector_utils import create_vector_store, load_vector_store, get_text_chunks
from rag_pipeline import ask_question, ask_session_question
from utils.pdf_utils import extract_text_from_pdf
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Models ===
class RegisterData(BaseModel):
    user_id: str
    courses: List[str]

class FileURLs(BaseModel):
    file_urls: List[str]

# === Global Session Vectorstore ===
session_vectorstore = None

# === Endpoints ===

@app.post("/register")
def register(data: RegisterData):
    for course_id in data.courses:
        combined_text = ""
        files = get_course_files(course_id)
        for f in files:
            file_path = download_file(f["url"], f["name"])
            text = extract_text_from_pdf(file_path)
            combined_text += text
        chunks = get_text_chunks(combined_text)
        directory = f"chroma_db/{data.user_id}/{course_id}"
        os.makedirs(directory, exist_ok=True)
        create_vector_store(chunks, directory)
    return {"message": "Vectorstores created."}

@app.get("/ask")
def ask(user_id: str, course_id: str, question: str):
    directory = f"chroma_db/{user_id}/{course_id}"
    vectorstore = load_vector_store(directory)
    answer = ask_question(vectorstore, question)
    return {"answer": answer}

@app.post("/session/process")
def process_selected_files(data: FileURLs):
    combined_text = ""
    for url in data.file_urls:
        file_name = url.split("/")[-1]
        file_path = download_file(url, file_name)
        text = extract_text_from_pdf(file_path)
        combined_text += text

    chunks = get_text_chunks(combined_text)

    global session_vectorstore
    session_vectorstore = create_vector_store(chunks)  # in-memory

    return {"message": "Session vectorstore created."}

@app.get("/session/ask")
def session_ask(question: str):
    global session_vectorstore
    if not session_vectorstore:
        return {"error": "No session vectorstore yet."}

    answer = ask_session_question(session_vectorstore, question)
    return {"answer": answer}

@app.get("/canvas/courses")
def fetch_courses():
    return get_courses()

@app.get("/canvas/courses/{course_id}/files")
def fetch_files(course_id: int):
    return get_course_files(course_id)

@app.get("/chat")
def chat(user_id: str, course_id: str, question: str):
    global session_vectorstore
    if session_vectorstore:
        answer = ask_session_question(session_vectorstore, question)
    else:
        directory = f"chroma_db/{user_id}/{course_id}"
        vectorstore = load_vector_store(directory)
        answer = ask_question(vectorstore, question)
    return {"answer": answer}

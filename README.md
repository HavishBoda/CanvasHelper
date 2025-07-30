# Canvas RAG Assistant

A Retrieval-Augmented Generation (RAG) application that helps students and educators interact with Canvas LMS course materials using natural language. Built with FastAPI, Next.js, and modern AI technologies.

## Features

- Course Material Access: Connect to Canvas LMS account
- AI-Powered Q&A: Get instant answers to course-related questions
- Document Processing: Upload and query various course materials
- Context-Aware Responses: AI understands course context for relevant answers
- Modern Interface: Clean UI built with Next.js

## Tech Stack

### Backend
- FastAPI - Web framework
- LangChain - LLM application framework
- ChromaDB - Vector database for document retrieval
- Sentence Transformers - Document embeddings
- PyPDF2 - PDF text extraction

### Frontend
- Next.js - React framework
- Tailwind CSS - CSS framework
- Axios - HTTP client

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16.8+ and npm
- Canvas LMS API access token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/canvas-rag.git
   cd canvas-rag
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Canvas API token
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## Configuration

Create a `.env` file in the backend directory with:

```
CANVAS_ACCESS_TOKEN=your_canvas_api_token
CANVAS_BASE_URL=https://your-institution.instructure.com
```

## How It Works

1. Authentication: Connect to Canvas LMS
2. Course Selection: Choose from enrolled courses
3. Document Processing: System indexes course materials
4. Natural Language Queries: Ask questions in plain English
5. Intelligent Responses: Get relevant answers from course materials

## Project Structure

```
canvas-rag/
├── backend/               # FastAPI backend
│   ├── app.py            # Main application
│   ├── rag_pipeline.py   # RAG implementation
│   └── utils/            # Utility functions
├── frontend/             # Next.js frontend
│   ├── src/              # Source code
│   └── public/           # Static assets
└── README.md             # Documentation
```
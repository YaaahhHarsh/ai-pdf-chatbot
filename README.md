# AI PDF Chatbot

A full-stack AI PDF chatbot built with Next.js, FastAPI, LangChain, and FAISS.

Features:
- Upload PDF documents
- Extract text using PyMuPDF
- Split into chunks and store in a vector database
- Ask questions about the document using an LLM
- Get cited source snippets from the uploaded PDF
- Modern chat UI

## Tech stack
- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- AI: LangChain + OpenAI
- Vector store: FAISS
- PDF parsing: PyMuPDF

## Quick start

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### 3) OpenAI setup

Create a `.env` file in the backend with your key:

```env
OPENAI_API_KEY=your_openai_key_here
```

### 4) Access the app

Frontend: http://localhost:3000
Backend docs: http://localhost:8000/docs

## Project structure

```text
.
├── backend/
│   ├── app/
│   ├── data/
│   ├── uploads/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── README.md
├── .gitignore
└── .env.example
```

## Notes

This is a production-friendly starter project. For local testing, an OpenAI API key is required. If you want to use a local model or a different embedding provider, you can swap the backend integrations without changing the API shape.

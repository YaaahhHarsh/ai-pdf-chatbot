# AI PDF Chatbot

A full-stack AI PDF chatbot built with Next.js, FastAPI, LangChain, and FAISS.

## Features
- Upload PDF files
- Extract text from the document
- Split text into chunks and index them with embeddings
- Ask questions based on uploaded PDF content
- See page-aware source references
- Multi-file chat workflow

## Tech stack
- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- AI: LangChain + OpenAI
- Vector store: FAISS
- PDF parsing: PyMuPDF

## Local development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Production deployment

See `DEPLOYMENT.md` for Vercel + Render instructions.

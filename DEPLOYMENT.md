# AI PDF Chatbot Deployment Guide

This project is ready for deployment in two parts:

- Frontend: Vercel
- Backend: Render

## 1) Backend on Render

### Prerequisites
- GitHub repo connected to Render
- OpenAI API key

### Render setup
- Create a new Web Service on Render
- Connect this repository
- Set the root directory to `backend` if using the backend folder as the service root
- Use the included `Dockerfile`
- Set environment variables:
  - `OPENAI_API_KEY=your_key_here`
  - `MODEL_NAME=gpt-4o-mini`
  - `UPLOAD_DIR=./uploads`
  - `VECTOR_STORE_DIR=./data/vectorstore`

### Runtime command
Render will use the Dockerfile automatically.

## 2) Frontend on Vercel

### Prerequisites
- Vercel account
- GitHub repo connected to Vercel

### Vercel setup
- Import the `frontend` folder as the project root, or configure the project root to `frontend`
- Set environment variables:
  - `NEXT_PUBLIC_API_URL=https://your-render-backend-url.onrender.com`

### Build settings
- Framework: Next.js
- Root directory: `frontend`

## 3) Production workflow

1. Upload a PDF via the frontend.
2. Backend extracts text and creates embeddings.
3. The frontend sends questions to the backend API.
4. The backend queries relevant chunks and returns grounded answers.

## 4) Notes

- The backend stores uploaded vector indexes locally inside the container. For production, you may eventually want a persistent volume or cloud object storage.
- For better production scaling, consider replacing FAISS with pgvector or Pinecone.

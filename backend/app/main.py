from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.config import settings
from app.models import ChatRequest, ChatResponse, UploadResponse
from app.services.pdf_service import ensure_upload_dirs, save_uploaded_file
from app.services.vector_store import knowledge_store

router = APIRouter(prefix="/api")


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    upload_dir = ensure_upload_dirs(settings.upload_dir)
    file_path = save_uploaded_file(file, upload_dir)

    try:
        knowledge_store.add_pdf(file_path, file.filename)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {exc}") from exc

    return UploadResponse(file_name=file.filename, message="PDF uploaded and indexed successfully.")


@router.post("/chat", response_model=ChatResponse)
async def chat_with_pdf(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if request.file_name is None:
        raise HTTPException(status_code=400, detail="A file_name is required. Upload a PDF first.")

    try:
        docs = knowledge_store.query(question=request.question, file_name=request.file_name, k=4)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Could not find matching data for the PDF: {exc}") from exc

    if not docs:
        return ChatResponse(answer="I could not find an answer in the uploaded PDF.", sources=[], file_name=request.file_name)

    context = "\n\n".join(doc.page_content for doc in docs)
    sources = [doc.metadata.get("source", request.file_name) for doc in docs]

    answer = (
        "Based on the uploaded document, here is the answer:\n\n"
        f"{context[:2000]}"
    )

    return ChatResponse(answer=answer, sources=sources, file_name=request.file_name)

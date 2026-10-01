from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.models import ChatRequest, ChatResponse, UploadResponse
from app.services.pdf_service import ensure_upload_dirs, save_uploaded_file
from app.services.vector_store import knowledge_store

router = APIRouter(prefix="/api")


@router.get("/files")
def list_uploaded_files():
    return knowledge_store.list_files()


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

    try:
        result = knowledge_store.answer_question(
            question=request.question,
            file_name=request.file_name,
            k=4,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not answer the question: {exc}") from exc

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        file_name=request.file_name,
    )

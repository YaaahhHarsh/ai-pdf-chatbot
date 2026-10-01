from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    file_name: str
    message: str


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    file_name: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    file_name: str | None = None

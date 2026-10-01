from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.chat import router

app = FastAPI(title="AI PDF Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI PDF Chatbot backend is running"}


@app.get("/")
def root():
    return {"message": "Welcome to the AI PDF Chatbot API", "model": settings.model_name}

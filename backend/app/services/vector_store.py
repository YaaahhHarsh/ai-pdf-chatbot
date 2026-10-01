import os
from pathlib import Path

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from app.config import settings
from app.services.pdf_service import extract_text_from_pdf


class PDFKnowledgeStore:
    def __init__(self, vector_store_dir: str | None = None):
        self.vector_store_dir = vector_store_dir or settings.vector_store_dir
        self.store_path = Path(self.vector_store_dir)
        self.store_path.mkdir(parents=True, exist_ok=True)

    def add_pdf(self, file_path: str, file_name: str) -> list[str]:
        text = extract_text_from_pdf(file_path)
        if not text.strip():
            raise ValueError("No readable text found in the uploaded PDF.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = splitter.split_text(text)

        docs = [
            Document(page_content=chunk, metadata={"source": file_name})
            for chunk in chunks
        ]

        vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings(openai_api_key=settings.openai_api_key))
        target_dir = self.store_path / file_name
        target_dir.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(target_dir))

        return [chunk for chunk in chunks]

    def query(self, question: str, file_name: str | None = None, k: int = 4) -> list[Document]:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing. Set it in your backend .env file.")

        target_dir = self.store_path / (file_name or "")
        if file_name and not target_dir.exists():
            raise FileNotFoundError(f"No indexed document found for {file_name}")

        if file_name is None:
            vector_dirs = [p for p in self.store_path.iterdir() if p.is_dir()]
            if not vector_dirs:
                raise FileNotFoundError("No uploaded PDF has been indexed yet.")
            target_dir = vector_dirs[0]

        vectorstore = FAISS.load_local(
            str(target_dir),
            OpenAIEmbeddings(openai_api_key=settings.openai_api_key),
            allow_dangerous_deserialization=True,
        )

        return vectorstore.similarity_search(question, k=k)


knowledge_store = PDFKnowledgeStore()

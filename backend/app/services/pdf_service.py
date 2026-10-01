import os
from pathlib import Path

import fitz


def extract_pages_from_pdf(file_path: str) -> list[tuple[int, str]]:
    doc = fitz.open(file_path)
    pages: list[tuple[int, str]] = []

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text and text.strip():
            pages.append((page_number, text))

    doc.close()
    return pages


def extract_text_from_pdf(file_path: str) -> str:
    pages = extract_pages_from_pdf(file_path)
    return "\n\n".join(page_text for _, page_text in pages)


def ensure_upload_dirs(base_dir: str) -> str:
    upload_dir = Path(base_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return str(upload_dir)


def save_uploaded_file(file, upload_dir: str) -> str:
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)

    file_path = upload_path / file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return str(file_path)

import os
from pathlib import Path

import fitz


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text_chunks = []

    for page in doc:
        text = page.get_text("text")
        if text:
            text_chunks.append(text)

    doc.close()
    return "\n\n".join(text_chunks)


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

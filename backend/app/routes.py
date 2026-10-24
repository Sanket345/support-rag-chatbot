"""STAGE 2: the HTTP endpoints the React app will call."""
import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from . import config
from .document_processing import load_and_split
from .retrieval import ask
from .vector_store import clear_store, list_documents, replace_document

router = APIRouter(prefix="/api")
log = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    role: str      # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    question: str
    history: list[ChatMessage] = []


@router.get("/documents")
def get_documents():
    return list_documents()


@router.post("/upload")
def upload(files: list[UploadFile] = File(...)):
    config.UPLOAD_DIR.mkdir(exist_ok=True)
    indexed, errors = [], []

    for f in files:
        name = Path(f.filename).name  # strips any folder parts for safety
        if not name.lower().endswith(".pdf"):
            errors.append(f"{name}: only PDF files are allowed")
            continue

        path = config.UPLOAD_DIR / name
        with open(path, "wb") as out:
            shutil.copyfileobj(f.file, out)

        try:
            chunks = load_and_split(str(path), name)
        except Exception:
            log.exception("Failed to read %s", name)
            errors.append(f"{name}: could not read this PDF")
            continue

        if not chunks:
            errors.append(f"{name}: no text found (is it a scanned image?)")
            continue

        replace_document(name, chunks)
        indexed.append({"name": name, "chunks": len(chunks)})

    if not indexed:
        raise HTTPException(status_code=400, detail="; ".join(errors) or "No files received")
    return {"indexed": indexed, "errors": errors, "documents": list_documents()}


@router.delete("/documents")
def delete_all():
    clear_store()
    shutil.rmtree(config.UPLOAD_DIR, ignore_errors=True)
    return {"documents": []}


@router.post("/chat")
def chat(req: ChatRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")
    try:
        return ask(req.question, [m.model_dump() for m in req.history])
    except RuntimeError as e:  # e.g. missing API key
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        log.exception("Chat failed")
        raise HTTPException(status_code=500, detail="Something went wrong while answering. Please try again.")

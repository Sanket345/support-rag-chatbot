"""All settings in one place. Secrets come from the .env file, never from code."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "models/gemini-embedding-001"

CHROMA_DIR = BASE_DIR / "chroma_db"
UPLOAD_DIR = BASE_DIR / "uploads"
COLLECTION_NAME = "company_docs"

CHUNK_SIZE = 1000          # characters per chunk
CHUNK_OVERLAP = 200        # characters shared between neighbouring chunks
TOP_K = 4                  # how many chunks to retrieve
MAX_DISTANCE = 0.75        # cosine distance cutoff: lower = stricter. Tune this!
MAX_HISTORY_MESSAGES = 6   # how many past messages the LLM sees
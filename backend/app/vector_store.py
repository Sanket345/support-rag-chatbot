"""Step 2: embeddings (text -> numbers) and the Chroma database that stores them."""
from collections import Counter

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from . import config

_embeddings = None


def get_embeddings():
    """Embeddings computed online by Google Gemini (free tier)."""
    global _embeddings
    if _embeddings is None:
        _embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
        )
    return _embeddings
def get_vector_store():
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(config.CHROMA_DIR),
        collection_metadata={"hnsw:space": "cosine"},
    )


def replace_document(name: str, chunks):
    """Add a document's chunks. Re-uploading the same file replaces the old version."""
    store = get_vector_store()
    old_ids = store.get(where={"source": name})["ids"]
    if old_ids:
        store.delete(ids=old_ids)
    store.add_documents(chunks)


def list_documents():
    metadatas = get_vector_store().get(include=["metadatas"])["metadatas"]
    counts = Counter(m["source"] for m in metadatas)
    return [{"name": n, "chunks": c} for n, c in sorted(counts.items())]


def clear_store():
    get_vector_store().delete_collection()

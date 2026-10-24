from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .vector_store import get_embeddings


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_embeddings()  # load the model at startup so the first request is fast
    yield


app = FastAPI(title="Support RAG Chatbot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .vector_store import get_embeddings


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_embeddings()
    yield


app = FastAPI(title="Support RAG Chatbot", lifespan=lifespan)

# Comma-separated list of allowed websites, set as an environment variable on Render.
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
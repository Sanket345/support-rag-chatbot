# Customer Support RAG Chatbot

React + Vite + Tailwind frontend, FastAPI + LangChain backend, Groq LLM (`openai/gpt-oss-120b`),
local HuggingFace embeddings (`all-MiniLM-L6-v2`) and a Chroma vector store.

## 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then put your Groq key inside .env
```

**Stage 1 - test the RAG pipeline in the terminal:**
```bash
python test_rag.py path/to/some.pdf
```

**Stage 2 - start the API:**
```bash
uvicorn app.main:app --reload --port 8000
```
Try it at http://localhost:8000/docs

## 2. Frontend (Stage 3)

```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## Tuning
- `MAX_DISTANCE` in `backend/app/config.py`: lower = stricter ("not found" more often), higher = more lenient.
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K` in the same file.

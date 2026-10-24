"""STAGE 1 TEST: run the RAG pipeline in the terminal, no API or UI needed.

Usage (from the backend folder):
    python test_rag.py path/to/some.pdf
"""
import sys
from pathlib import Path

from app.document_processing import load_and_split
from app.retrieval import ask
from app.vector_store import replace_document

if len(sys.argv) < 2:
    sys.exit("Usage: python test_rag.py path/to/file.pdf")

pdf = Path(sys.argv[1])
chunks = load_and_split(str(pdf), pdf.name)
replace_document(pdf.name, chunks)
print(f"Indexed {len(chunks)} chunks from {pdf.name}\n")

history = []
while True:
    question = input("You: ").strip()
    if question.lower() in {"", "quit", "exit"}:
        break
    result = ask(question, history)
    print(f"\nBot: {result['answer']}")
    for s in result["sources"]:
        print(f"   source: {s['source']} (page {s['page']})")
    print()
    history += [{"role": "user", "content": question},
                {"role": "assistant", "content": result["answer"]}]

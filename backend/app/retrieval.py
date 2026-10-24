"""Step 3: find relevant chunks, then ask the LLM to answer from them."""
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from . import config
from .prompts import ANSWER_PROMPT, CONDENSE_PROMPT, NOT_FOUND_MESSAGE
from .vector_store import get_vector_store


def get_llm():
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to backend/.env")
    return ChatGroq(model=config.LLM_MODEL, api_key=config.GROQ_API_KEY, temperature=0)


def to_messages(history):
    """Turn [{'role': 'user', 'content': '...'}] into LangChain message objects."""
    recent = history[-config.MAX_HISTORY_MESSAGES:]
    return [
        HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
        for m in recent
    ]


def retrieve(query: str):
    """Return only chunks that are close enough to the question (distance filter)."""
    results = get_vector_store().similarity_search_with_score(query, k=config.TOP_K)
    return [doc for doc, distance in results if distance <= config.MAX_DISTANCE]


def unique_sources(docs):
    seen, sources = set(), []
    for d in docs:
        key = (d.metadata["source"], d.metadata["page"])
        if key not in seen:
            seen.add(key)
            sources.append({"source": key[0], "page": key[1]})
    return sources


def ask(question: str, history: list[dict]) -> dict:
    llm = get_llm()
    messages = to_messages(history)

    # Follow-ups like "and how long does it take?" need the history to be searchable.
    search_query = question
    if messages:
        search_query = (CONDENSE_PROMPT | llm | StrOutputParser()).invoke(
            {"history": messages, "question": question}
        )

    docs = retrieve(search_query)
    if not docs:  # nothing relevant -> do not even call the LLM
        return {"answer": NOT_FOUND_MESSAGE, "sources": []}

    context = "\n\n".join(
        f"[{d.metadata['source']}, page {d.metadata['page']}]\n{d.page_content}" for d in docs
    )
    answer = (ANSWER_PROMPT | llm | StrOutputParser()).invoke(
        {"context": context, "history": messages, "question": question}
    ).strip()

    sources = [] if NOT_FOUND_MESSAGE in answer else unique_sources(docs)
    return {"answer": answer, "sources": sources}

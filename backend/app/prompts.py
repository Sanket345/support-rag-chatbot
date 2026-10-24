"""All prompt text lives here so it is easy to find and tweak."""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

NOT_FOUND_MESSAGE = "I couldn't find that information in the uploaded documents."

CONDENSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Given the chat history and the latest user question, rewrite the question as a "
     "standalone question that makes sense without the history. Do NOT answer it. "
     "If it is already standalone, return it unchanged. Return only the question."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a customer support assistant. Answer the customer's question using ONLY "
     "the context below, which comes from the company's documents.\n\n"
     "Rules:\n"
     f'- If the context does not contain enough information, reply with exactly: "{NOT_FOUND_MESSAGE}" and nothing else.\n'
     "- Never guess and never use outside knowledge.\n"
     "- Be clear and concise. Use bullet points for steps.\n"
     "- Do not write file names or page numbers; they are shown to the user separately.\n\n"
     "Context:\n{context}"),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

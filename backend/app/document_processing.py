"""Step 1 of the pipeline: PDF -> pages -> chunks."""
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from . import config


def load_and_split(pdf_path: str, original_name: str):
    """Read a PDF and cut it into overlapping chunks that remember their file and page."""
    pages = PyPDFLoader(pdf_path).load()

    for page in pages:
        page.metadata["source"] = original_name              # show the real file name
        page.metadata["page"] = page.metadata.get("page", 0) + 1  # PyPDF counts from 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(pages)
    return [c for c in chunks if c.page_content.strip()]

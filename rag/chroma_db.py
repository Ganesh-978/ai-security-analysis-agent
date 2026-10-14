import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
FAISS_DIR = os.getenv("FAISS_INDEX_DIR", "./data/faiss_index")
COLLECTION_NAME = "secure_coding_kb"


def get_chroma_vectorstore() -> Chroma:
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )


def save_faiss_vectorstore(chunks: List[Document]) -> FAISS:
    Path(FAISS_DIR).mkdir(parents=True, exist_ok=True)
    vectorstore = FAISS.from_documents(chunks, get_embeddings())
    vectorstore.save_local(FAISS_DIR)
    return vectorstore


def load_faiss_vectorstore() -> Optional[FAISS]:
    index_file = Path(FAISS_DIR) / "index.faiss"
    if not index_file.exists():
        return None
    return FAISS.load_local(
        FAISS_DIR, get_embeddings(), allow_dangerous_deserialization=True
    )
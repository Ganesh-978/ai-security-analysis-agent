from typing import List
from langchain_core.documents import Document
from rag.chroma_db import get_chroma_vectorstore, load_faiss_vectorstore


def search_knowledge_base(
    query: str, k: int = 3, backend: str = "chroma") -> List[Document]:
    if backend == "faiss":
        faiss_db = load_faiss_vectorstore()
        if faiss_db is not None:
            return faiss_db.similarity_search(query, k=k)

    chroma_db = get_chroma_vectorstore()
    return chroma_db.similarity_search(query, k=k)
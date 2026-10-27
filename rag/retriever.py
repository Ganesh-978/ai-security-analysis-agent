from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from rag.chroma_db import get_chroma_vectorstore
from rag.embeddings import get_embeddings

_FAISS_CACHE: Optional[FAISS] = None
_CACHED_DOC_COUNT: int = 0


def _get_or_build_faiss_index() -> Optional[FAISS]:
    global _FAISS_CACHE, _CACHED_DOC_COUNT

    chroma_db = get_chroma_vectorstore()
    stored_data = chroma_db.get(include=["embeddings", "documents", "metadatas"])

    texts = stored_data.get("documents")
    embeddings = stored_data.get("embeddings")
    metadatas = stored_data.get("metadatas")

    if texts is None or len(texts) == 0:
        return None

    if _FAISS_CACHE is None or _CACHED_DOC_COUNT != len(texts):
        if embeddings is not None and len(embeddings) == len(texts):
            # Instantaneous: reuse pre-computed vectors from ChromaDB
            text_embedding_pairs = list(zip(texts, embeddings))
            _FAISS_CACHE = FAISS.from_embeddings(
                text_embeddings=text_embedding_pairs,
                embedding=get_embeddings(),
                metadatas=metadatas,
            )
        else:
            docs = [
                Document(page_content=t, metadata=m or {})
                for t, m in zip(texts, metadatas)
            ]
            _FAISS_CACHE = FAISS.from_documents(docs, get_embeddings())

        _CACHED_DOC_COUNT = len(texts)

    return _FAISS_CACHE


def search_knowledge_base(
    query: str,
    k: int = 4,
    allowed_categories: Optional[List[str]] = None,
    backend: str = "faiss",
) -> List[Document]:
    faiss_index = _get_or_build_faiss_index()
    if faiss_index is None:
        return []

    if not allowed_categories:
        return faiss_index.similarity_search(query, k=k)

    candidates = faiss_index.similarity_search(query, k=max(k * 4, 12))
    filtered = [
        doc
        for doc in candidates
        if doc.metadata.get("category") in allowed_categories
        or doc.metadata.get("folder") in allowed_categories
    ]
    return filtered[:k] if filtered else candidates[:k]

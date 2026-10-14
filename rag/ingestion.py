import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from rag.loader import load_documents
from rag.chunking import split_documents
from rag.chroma_db import get_chroma_vectorstore, save_faiss_vectorstore


def ingest_knowledge_base(kb_dir: str = "knowledge_base") -> dict:
    docs = load_documents(kb_dir)
    if not docs:
        return {"status": "empty", "docs_loaded": 0, "chunks_created": 0, "files": []}

    chunks = split_documents(docs)

    chroma_db = get_chroma_vectorstore()
    existing = chroma_db.get()
    if existing and existing.get("ids"):
        chroma_db.delete(ids=existing["ids"])
    chroma_db.add_documents(chunks)

    save_faiss_vectorstore(chunks)

    files = sorted(list({d.metadata.get("source", "") for d in docs}))
    return {
        "status": "success",
        "docs_loaded": len(docs),
        "chunks_created": len(chunks),
        "files": files,
    }


if __name__ == "__main__":
    result = ingest_knowledge_base()
    print("Knowledge Base Ingestion Result:", result)
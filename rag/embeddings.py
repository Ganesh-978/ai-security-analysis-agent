import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

_EMBEDDING_INSTANCE = None


def get_embeddings() -> HuggingFaceEmbeddings:
    global _EMBEDDING_INSTANCE
    if _EMBEDDING_INSTANCE is None:
        model_name = os.getenv(
            "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
        )
        _EMBEDDING_INSTANCE = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _EMBEDDING_INSTANCE

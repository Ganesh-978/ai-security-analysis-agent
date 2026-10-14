from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader, TextLoader



def load_documents(kb_dir: str = "knowledge_base") -> List[Document]:
    base_path = Path(kb_dir)
    if not base_path.exists():
        return []

    documents: List[Document] = []

    # Loading Markdown (.md) files using Unstructured
    for md_file in base_path.rglob("*.md"):
        try:
            loader = UnstructuredMarkdownLoader(str(md_file))
            docs = loader.load()
        except Exception:
            loader = TextLoader(str(md_file), encoding="utf-8")
            docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = str(md_file.relative_to(base_path))
            doc.metadata["category"] = md_file.parent.name
            documents.append(doc)

    # Loading PDF (.pdf) files using PyPDF
    for pdf_file in base_path.rglob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        for doc in loader.load():
            doc.metadata["source"] = str(pdf_file.relative_to(base_path))
            doc.metadata["category"] = pdf_file.parent.name
            documents.append(doc)

    return documents
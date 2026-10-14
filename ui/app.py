import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from parsers.code_validator import validate_submission
from rag.ingestion import ingest_knowledge_base
from rag.retriever import search_knowledge_base

st.set_page_config(
    page_title="AI Code Review & Security Analysis - Milestone 1",
    layout="wide",
)

st.title("🛡️ AI Code Review & Security Analysis Agent ")
st.caption("Modules: Code Submission, Auto Language Detection, Syntax Validation & OWASP RAG Pipeline")

# Sidebar: Knowledge Base Indexing
with st.sidebar:
    st.header("📚 RAG Knowledge Base")
    vector_backend = st.selectbox("Vector Search Backend:", ["chroma", "faiss"])

    if st.button("🔄 Index Knowledge Base", use_container_width=True):
        with st.spinner("Chunking & embedding knowledge_base files..."):
            res = ingest_knowledge_base()
            if res["status"] == "success":
                st.success(f"Indexed {res['chunks_created']} chunks from {res['docs_loaded']} files!")
                st.write("**Indexed Files:**", res["files"])
            else:
                st.warning("No .md or .pdf files found in knowledge_base/ folder.")

# Split Screen: Left (Editor) | Right (Validation & RAG Output)
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("1. Code Submission Module")
    uploaded_file = st.file_uploader("Upload Python (.py) or Java (.java) file", type=["py", "java"])

    default_code = ""
    filename = None
    if uploaded_file is not None:
        filename = uploaded_file.name
        default_code = uploaded_file.getvalue().decode("utf-8", errors="replace")

    code_input = st.text_area(
        "Or Paste Source Code Here (Python / Java auto-detected):",
        value=default_code,
        height=380,
        placeholder="Paste your Python or Java code here...",
    )

    submit_btn = st.button("✅ Validate Code & Retrieve OWASP Guidelines", type="primary", use_container_width=True)

with right_col:
    st.subheader("2. Validation & RAG Knowledge Base Output")

    if code_input.strip() or submit_btn:
        validation = validate_submission(code_input, filename=filename)

        # Display Auto-Detected Language
        if validation.detected_language == "python":
            st.info("🐍 **Auto-Detected Language:** Python")
        elif validation.detected_language == "java":
            st.info("☕ **Auto-Detected Language:** Java")
        else:
            st.warning("❓ **Auto-Detected Language:** Unknown / Unsupported")

        # Gatekeeper: Stop if syntax error exists
        if not validation.is_valid:
            st.error("🚫 **Syntax Error Detected — Blocked from Review Pipeline**")
            st.markdown(
                f"- **Line Number:** `{validation.line_number}`\n"
                f"- **Error:** `{validation.error_message}`"
            )
            if validation.offending_line:
                st.code(validation.offending_line, language="text")
        else:
            st.success("✅ **Syntax Validation Passed!** Code is valid and ready for review.")

            # Demonstrate Milestone 1 RAG Retrieval against indexed OWASP docs
            st.markdown("---")
            st.markdown("#### 🔍 Relevant Security Guidelines Retrieved from RAG (`knowledge_base/`)")
            docs = search_knowledge_base(
                query=f"{validation.detected_language} security OWASP:\n{code_input[:600]}",
                k=3,
                backend=vector_backend,
            )
            if not docs:
                st.warning("Knowledge base is not indexed yet. Click 'Index Knowledge Base' in the sidebar.")
            else:
                for i, doc in enumerate(docs, start=1):
                    source = doc.metadata.get("source", "knowledge_base")
                    with st.expander(f"Chunk #{i} — Source: {source}", expanded=(i == 1)):
                        st.write(doc.page_content)
    else:
        st.info("Paste code or upload a `.py` / `.java` file on the left to auto-detect language and validate syntax.")
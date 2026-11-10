<div align="center">

# 🛡️ AI Code Review & Security Analysis Agent

**Multi-Agent SAST, Automated Code Quality Inspection, AI Remediation & RAG Developer Assistant for Python and Java**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![RAG](https://img.shields.io/badge/RAG-ChromaDB%20%2B%20FAISS-FF6F00?style=for-the-badge)](https://www.trychroma.com/)
[![SAST](https://img.shields.io/badge/SAST-AST%20%7C%20Tree--sitter%20%7C%20Bandit-D32F2F?style=for-the-badge)](https://github.com/PyCQA/bandit)

[Overview](#-1-overview--problem-statement) •
[Architecture](#-2-6-layer-system-architecture) •
[Multi-Agent Workflow](#-3-end-to-end-multi-agent-workflow) •
[Core Agents](#-4-core-agents--capabilities) •
[Quickstart](#-7-installation--quickstart) •
[API Reference](#-10-rest-api-specification)

</div>

---

## 🎯 1. Overview & Problem Statement

Engineering teams frequently face inconsistent code quality, undetected security vulnerabilities, and slow, subjective manual code reviews. Developers often lack immediate access to contextual secure coding standards and actionable remediation guidance during active development—leaving critical vulnerabilities and design flaws undetected until late in the software development lifecycle (SDLC).

**AI Code Review & Security Analysis Agent** is a multi-agent platform that automates static code inspection, OWASP vulnerability detection, root-cause remediation, pull-request summarization, and interactive developer Q&A in **under 15 seconds**.

### ✨ Key Highlights
* **Syntax Gatekeeper (`AST` + `Tree-sitter`)**: Automatically detects **Python** or **Java** from pasted code or uploaded files and validates syntax trees before invoking downstream AI agents.
* **Hybrid SAST + Parallel LangGraph Agents**: Combines deterministic static scanners (`Bandit`, `Semgrep`, `Pylint`, `Radon`, `SpotBugs`, `PMD`, `Checkstyle`) with parallel LLM reasoning so findings include exact line numbers, severity scores, and exploit explanations.
* **AI Remediation & Human-in-the-Loop Controls**: Explains root causes, classifies fixes across 4 recommendation categories (*Security, Code Quality, Performance, Maintainability*), provides side-by-side corrected code, and tracks developer approval status.
* **PR Summary & Exportable Reports**: Generates pull-request review verdicts, an overall **Code Health Score (`0–100`)**, interactive severity charts, and downloadable **Markdown (`.md`)** and **JSON (`.json`)** reports.
* **RAG Conversational Code Assistant**: Multi-turn chat assistant grounded in an indexed **OWASP Top 10 (A01–A10)**, **CWE**, **SEI CERT**, and **Clean Code** knowledge base powered by **Sentence Transformers (`all-MiniLM-L6-v2`)**, **ChromaDB**, and in-memory **FAISS**.

---

## 🏗️ 2. 6-Layer System Architecture

| Layer | Architectural Layer | Core Responsibilities & Technologies |
| :--- | :--- | :--- |
| **Layer 1** | **Code Input & Syntax Gatekeeper** | Accepts pasted code or `.py` / `.java` uploads. Auto-detects language and validates grammar via Python `ast` and `Tree-sitter` (`tree-sitter-python`, `tree-sitter-java`). |
| **Layer 2** | **Static Analysis Engine (SAST)** | Executes non-execution static analysis across Python (`Bandit`, `Semgrep`, `Pylint`, `Radon`), Java (`SpotBugs`, `PMD`, `Checkstyle`), and Enterprise (`SonarQube`, `Snyk`) rule patterns. |
| **Layer 3** | **Multi-Agent AI Orchestration** | Coordinates parallel agent fan-out/fan-in and sequential remediation/reporting pipelines using `LangGraph` and `LangChain`. |
| **Layer 4** | **LLM Processing & Vector RAG** | Grounds `Google Gemini` (`gemini-2.5-flash`) in curated security standards stored in `ChromaDB` and searched in-memory via `FAISS` using `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`). |
| **Layer 5** | **Remediation, Scoring & Reporting** | Computes **Code Health Score (`0–100`)**, 4 complexity metrics, 5-tier severity breakdown, root-cause remediation plans, PR summaries, and exportable `.md` / `.json` reports. |
| **Layer 6** | **Developer Portal & Persistence** | Split-screen `Streamlit` developer portal decoupled via a `FastAPI` REST backend with automated audit history stored in `SQLite` (`data/reviews.db`). |

---

## 🔄 3. End-to-End Multi-Agent Workflow

```text
+-----------------------------------------------------------------------------+
| 1. Developer Submits Code (Paste in Editor or Upload .py / .java File)      |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| 2. Auto-Language Detection & AST / Tree-sitter Syntax Gatekeeper            |
|    -> If Syntax Invalid: Block Pipeline Immediately & Show Exact Line Error |
+-----------------------------------------------------------------------------+
                                      | (Valid Syntax)
                                      v
+-----------------------------------------------------------------------------+
| 3. SAST Pattern Scan + In-Memory FAISS Retrieval from ChromaDB Vectors      |
+-----------------------------------------------------------------------------+
                                      |
               +----------------------+----------------------+
               |  (Parallel Fan-Out via LangGraph StateGraph) |
               v                                             v
+-------------------------------------+   +-----------------------------------+
| 4A. Code Analysis Agent             |   | 4B. Security Vulnerability Agent  |
| - Code Smells & Linting Rules       |   | - Full OWASP Top 10 (A01-A10)     |
| - 4 Complexity Metrics              |   | - CWE / CERT / Bandit / SpotBugs  |
| - 6 Design Anti-Patterns            |   | - 8 Secure Coding Guidelines      |
+-------------------------------------+   +-----------------------------------+
               |                                             |
               +----------------------+----------------------+
                                      | (Parallel Fan-In)
                                      v
+-----------------------------------------------------------------------------+
| 5. OWASP Rule Matcher & Severity Scoring Engine                             |
|    (Critical | High | Medium | Low | Informational + Code Health Score)     |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| 6. AI Remediation Agent                                                     |
|    - Root Cause Analysis & "Why It Occurs" Explanation                      |
|    - 4 Categories: Security | Code Quality | Performance | Maintainability  |
|    - Side-by-Side Flagged vs. Corrected Code + Human-in-the-Loop Approval   |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| 7. PR Summary Agent & Report Generator (.md / .json)                        |
|    + Interactive Severity Dashboard + Multi-Turn RAG Code Assistant         |
+-----------------------------------------------------------------------------+
```

---

## 🧠 4. Core Agents & Capabilities

### 1️⃣ Code Analysis Agent
Evaluates structural quality, maintainability, and design patterns without executing the program:
* **Four Dimensions of Code Complexity**:
  * **Cyclomatic Complexity**: Measures decision paths (`if`, `for`, `while`, `case`, `catch`) and assigns a risk rank (`A` to `F`).
  * **Cognitive Complexity**: Evaluates human understandability and penalizes deep control-flow nesting.
  * **Time Complexity**: Estimates Big-O execution time growth ($\mathcal{O}(1)$, $\mathcal{O}(n)$, $\mathcal{O}(n^2)$, $\mathcal{O}(n^k)$).
  * **Space Complexity**: Estimates auxiliary memory allocation growth ($\mathcal{O}(1)$ vs. $\mathcal{O}(n)$).
* **Six Common Design Anti-Patterns**: *God Object*, *Spaghetti Code*, *Blob Class*, *Lava Flow*, *Golden Hammer*, and *Copy-Paste Programming*.
* **Quality Telemetry**: *Overall Code Health Score ($0\text{--}100$)*, *Maintainability Score ($0\text{--}100$)*, *Complexity Score ($0\text{--}100$)*, *Duplication %*, *Documentation Coverage %*, and *Estimated Technical Debt (mins)*.

### 2️⃣ Security Vulnerability Agent
Combines SAST pattern matching with RAG-grounded LLM analysis across **all OWASP Top 10 (A01–A10)** categories and **8 Core Secure Coding Guidelines**:
* **OWASP Top 10 & CWE Coverage**:
  * **A01: Broken Access Control** (CSRF `CWE-352`, Path Traversal `CWE-22`, Overly Permissive Permissions `CWE-732`)
  * **A02: Cryptographic Failures** (Hardcoded Secrets `CWE-798`, Weak Hashing `MD5`/`SHA-1` `CWE-328`, Weak Ciphers `DES`/`ECB` `CWE-327`, Insecure PRNG `CWE-338`)
  * **A03: Injection** (SQL Injection `CWE-89`, Cross-Site Scripting / XSS `CWE-79`, OS Command Injection `CWE-78`, Code Injection `eval`/`exec` `CWE-95`)
  * **A04: Insecure Design** (Missing validation & workflow flaws)
  * **A05: Security Misconfiguration** (Debug mode enabled `CWE-489`, SSL/TLS verification disabled `CWE-295`, XML External Entity / XXE `CWE-611`)
  * **A06: Vulnerable & Outdated Components** (Deprecated/unsafe APIs)
  * **A07: Identification & Authentication Failures** (Unverified JWT signatures `CWE-347`, hardcoded passwords)
  * **A08: Software & Data Integrity Failures** (Insecure deserialization via `pickle`, `yaml.load`, `ObjectInputStream` `CWE-502`)
  * **A09: Security Logging & Monitoring Failures** (Swallowed security exceptions `CWE-390`, improper error handling)
  * **A10: Server-Side Request Forgery (SSRF)** (Unvalidated outbound HTTP requests `CWE-918`)
* **6 Structured Report Fields per Finding**: *(1) Vulnerability Name*, *(2) Severity Level*, *(3) Affected Line Number*, *(4) Risk Description*, *(5) Recommendation*, and *(6) Secure Coding Suggestion*.

### 3️⃣ AI Remediation Agent & Human-in-the-Loop Collaboration
Bridges the gap between issue detection and resolution:
* **Root Cause & Impact Analysis**: Explains *why* the issue exists in the code and how attackers or runtime edge cases can trigger it.
* **4 Recommendation Categories**: Classifies every fix into **Security**, **Code Quality**, **Performance**, or **Maintainability** recommendations.
* **Side-by-Side Code Diffs**: Displays the flagged lines alongside copy-ready, standards-compliant replacement code in Python or Java.
* **Human-in-the-Loop Controls**: Allows developers and team leads to mark each fix as *Pending Review*, *Approved & Applied*, *Team Lead Approved*, or *Rejected (Intentional Business Logic)*, dynamically updating the **Fix Progress %** KPI.

### 4️⃣ PR Summary Agent & Report Generator
Compiles all multi-agent outputs into a structured Pull Request review summary containing:
1. **Project Information & Release Verdict** (*Approved*, *Approved with Minor Recommendations*, or *Changes Requested*)
2. **Code Quality & Complexity Summary**
3. **Security Vulnerability Summary**
4. **Code Smell & Anti-Pattern Summary**
5. **Severity Breakdown & Prioritized Fix Roadmap** (Exportable as `.md` and `.json`)

### 5️⃣ RAG-Powered Conversational Code Assistant
An interactive multi-turn chat assistant grounded in the indexed `knowledge_base/`:
* **Intent Recognition**: Automatically classifies developer queries (*Vulnerability Explanation*, *Remediation & Secure Code Generation*, *Code Smell Guidance*, *Static Warning Diagnosis*).
* **Context-Aware Multi-Turn Memory**: Retains conversation history alongside the active source file and flagged findings.
* **Grounded Citations**: Cites the exact knowledge base source files (`owasp`, `cwe`, `cert`, `python`, `java`, `clean_code`) used to generate each answer.

---

## 🛠️ 5. Technology Stack & Tooling Matrix

| Category | Tools & Libraries | Purpose |
| :--- | :--- | :--- |
| **Agent Orchestration** | `LangGraph`, `LangChain`, `Google Gemini` | Parallel multi-agent workflow, remediation synthesis, and conversational Q&A. |
| **Vector DB & Search** | `ChromaDB`, `FAISS` (`faiss-cpu`) | `ChromaDB` persists embeddings on disk; cached `FAISS` executes sub-millisecond similarity search. |
| **Embeddings** | `Sentence Transformers`, `HuggingFaceEmbeddings` | Local CPU embedding generation using `sentence-transformers/all-MiniLM-L6-v2`. |
| **Document Loaders** | `Unstructured`, `PyPDF`, `Markdown` | Parses `.md` and `.pdf` security guidelines during RAG ingestion. |
| **Syntax & AST Parsing** | Python `ast`, `Tree-sitter` | Builds syntax trees for Python and Java to validate syntax and count AST nodes. |
| **Python SAST & Quality** | `Bandit`, `Semgrep`, `Pylint`, `Radon`, `Ruff` | Detects Python security vulnerabilities, cyclomatic complexity, and code smells. |
| **Java SAST & Quality** | `SpotBugs`, `PMD`, `Checkstyle`, `SEI CERT` | Detects Java resource leaks, SQLi, weak crypto, empty catch blocks, and naming issues. |
| **Backend & Database** | `FastAPI`, `Uvicorn`, `SQLite3`, `Pydantic` | Asynchronous REST API endpoints, strict schema validation, and review audit storage. |
| **Developer Portal** | `Streamlit`, `Pandas` | Split-screen UI with severity bar charts, KPI cards, remediation diff viewer, and chat interface. |

---

## 📂 6. Repository Directory Structure

```text
ai-security-analysis-agent/
├── data/
│   ├── chroma_db/                   # Persistent ChromaDB vector store
│   └── reviews.db                   # SQLite database for historical review records
├── knowledge_base/                  # Curated Secure Coding & Quality Knowledge Base
│   ├── cert/                        # SEI CERT Oracle Secure Coding Standard for Java
│   ├── clean_code/                  # Clean Code, Refactoring & Design Anti-Pattern rules
│   ├── cwe/                         # CWE Top Software Weaknesses specifications
│   ├── java/                        # PMD & SpotBugs Java static analysis rules
│   ├── owasp/                       # OWASP Top 10 (A01-A10) security guidelines
│   └── python/                      # Bandit & Python secure coding guidelines
├── llm/
│   ├── gemini_client.py             # Google Gemini ChatModel initialization & timeout config
│   └── prompt_manager.py            # System prompts for Code, Security, Remediation, PR & Chat Agents
├── models/
│   └── schemas.py                   # Pydantic schemas for findings, remediation, chat & reports
├── parsers/
│   ├── code_validator.py            # Auto Python/Java detector + AST & Tree-sitter gatekeeper
│   └── output_parser.py             # Resilient JSON array parser for LLM outputs
├── rag/
│   ├── chroma_db.py                 # ChromaDB persistent client & FAISS index helpers
│   ├── chunking.py                  # RecursiveCharacterTextSplitter semantic chunker
│   ├── embeddings.py                # Singleton HuggingFaceEmbeddings (all-MiniLM-L6-v2)
│   ├── ingestion.py                 # Offline ETL script to index knowledge_base/ into ChromaDB
│   ├── loader.py                    # UnstructuredMarkdownLoader (.md) & PyPDFLoader (.pdf)
│   └── retriever.py                 # In-memory cached FAISS similarity search over ChromaDB vectors
├── reports/
│   └── report_generator.py          # Structured Markdown & JSON report generator
├── sample_codes/
│   ├── vulnerable_python_sample.py  # Python sample containing known OWASP flaws & code smells
│   └── VulnerableJavaSample.java    # Java sample containing known SpotBugs/PMD/CERT flaws
├── services/
│   ├── api.py                       # FastAPI service (/health, /api/v1/analyze, /api/v1/chat, /api/v1/history)
│   └── database.py                  # SQLite persistence layer for review history
├── src/
│   ├── agents.py                    # Implementation of all 5 AI agents + OWASP rule matcher
│   ├── state.py                     # LangGraph ReviewWorkflowState TypedDict definition
│   └── workflow.py                  # LangGraph StateGraph orchestration pipeline
├── tests/
│   └── test_agents.py               # Automated test suite for syntax validation & agent detection
├── tools/
│   └── static_analyzer.py           # In-memory SAST scanner, 4-complexity & quality metric engine
├── ui/
│   └── app.py                       # Split-screen Streamlit developer portal & chat interface
├── .env                             # Environment variables (gitignored)
├── .gitignore                       # Ignores .venv, .env, __pycache__, and *.db files
├── pyproject.toml                   # Project metadata and uv lock configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## ⚙️ 7. Installation & Quickstart

### 1. Clone the Repository
```powershell
git clone [https://github.com/Ganesh-978/ai-security-analysis-agent.git](https://github.com/Ganesh-978/ai-security-analysis-agent.git)
cd ai-security-analysis-agent
```

### 2. Create & Activate Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
uv add tree-sitter tree-sitter-python tree-sitter-java bandit radon fastapi uvicorn
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./data/chroma_db
FAISS_INDEX_DIR=./data/faiss_index
```

### 5. Index the Secure Coding Knowledge Base
Run the ingestion script once to chunk, embed, and index all `.md` and `.pdf` guidelines from `knowledge_base/` into ChromaDB:
```powershell
.\.venv\Scripts\python.exe rag/ingestion.py
```

---

## 🚀 8. Running the Platform

Open two terminals in VS Code inside the project root:

### Terminal 1 — Start the FastAPI Backend Server
```powershell
.\.venv\Scripts\python.exe -m uvicorn services.api:app --reload --host 127.0.0.1 --port 8000
```
* **API Base URL**: `http://127.0.0.1:8000`
* **Swagger Docs**: `http://127.0.0.1:8000/docs`

### Terminal 2 — Launch the Streamlit Developer Portal
```powershell
.\.venv\Scripts\python.exe -m streamlit run ui/app.py --server.fileWatcherType none
```
* **Developer Portal URL**: `http://localhost:8501`

---

## 🖥️ 9. Live Demo Walkthrough

1. **Auto Language Detection & Syntax Gatekeeper**:
   * Paste Python or Java code in the left editor or upload `sample_codes/vulnerable_python_sample.py` / `sample_codes/VulnerableJavaSample.java`.
   * Observe the live badge displaying the detected language (`Python` or `Java`), active parser (`AST / Tree-sitter`), and syntax tree node count.
   * Introduce a syntax error (e.g., remove a `:` in Python or `;` in Java) to verify that the **Syntax Gatekeeper** blocks execution and highlights the exact line number.
2. **Full Multi-Agent Analysis & Severity Dashboard**:
   * Click **"🚀 Run Full Multi-Agent Code Review"**.
   * Review the top KPI banner (**Code Health Score**, **Total Issues**, **Security vs. Quality Split**, **Fix Progress %**, and execution timer).
   * In the **`📊 Severity Dashboard`** tab, inspect the **Severity Distribution** and **Security vs. Code Quality** bar charts alongside the 4 complexity cards (*Cyclomatic, Cognitive, Time, Space*).
3. **AI Remediation & Human-in-the-Loop Approval**:
   * Open the **`🛠️ AI Remediation`** tab to view the **Root Cause Analysis**, **Why This Issue Occurs**, **4-Category Classification**, and side-by-side **Flagged vs. Corrected Code**.
   * Change the **Human-in-the-Loop Review Decision** dropdown to *Approved & Applied* and watch the **Fix Progress %** KPI update automatically.
4. **PR Summary & Report Export**:
   * Open **`📝 PR Summary`** to view the formatted pull-request verdict and prioritized fix roadmap.
   * Open **`📥 Export Report`** to download the full review as a `.md` or `.json` file.
5. **RAG Conversational Code Assistant**:
   * Open **`💬 Conversational Assistant`**, click any preset prompt (e.g., *"How do I fix SQL Injection?"*) or ask a custom follow-up question about your code, and inspect the grounded response with cited OWASP/CERT sources.

---

## 🔌 10. REST API Specification

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns backend service health status (`{"status": "ok"}`). |
| `POST` | `/api/v1/analyze` | Validates syntax, runs SAST + Parallel Code & Security Agents + Remediation Agent + PR Summary Agent, saves to SQLite, and returns `CodeReviewReport`. |
| `POST` | `/api/v1/chat` | Processes multi-turn developer questions via RAG similarity search over ChromaDB/FAISS and returns `AssistantQueryResponse` with detected intent and sources. |
| `GET` | `/api/v1/history` | Returns the most recent code review audit records from `data/reviews.db`. |

---

## 📈 11. Agile Project Roadmap

* ✅ **Sprint 1 (Milestone 1 — Weeks 1–2): Foundation, Syntax Gatekeeper & OWASP RAG Pipeline**
  * Designed modular 6-layer architecture and Pydantic schemas (`models/schemas.py`).
  * Built Code Submission Module with automatic Python/Java detection and syntax validation (`parsers/code_validator.py`).
  * Built Secure Coding Knowledge Base & RAG pipeline using `Unstructured`, `PyPDF`, `Sentence Transformers`, `ChromaDB`, and `FAISS` (`rag/`).
* ✅ **Sprint 2 (Milestone 2 — Weeks 3–4): SAST Engine & Parallel Detection Agents**
  * Integrated `Tree-sitter` and built the SAST & 4-Complexity Engine (`tools/static_analyzer.py`).
  * Implemented `Code Analysis Agent` and `Security Vulnerability Agent` running in parallel via `LangGraph` (`src/agents.py`, `src/workflow.py`).
  * Added OWASP Top 10 (A01–A10) rule matching, 5-tier severity scoring, `FastAPI` backend (`services/api.py`), and `SQLite` persistence (`services/database.py`).
* ✅ **Sprint 3 (Milestone 3 — Weeks 5–6): AI Remediation, PR Summary, Dashboard & RAG Assistant**
  * Built `AI Remediation Agent` with root-cause analysis, 4 recommendation categories, side-by-side corrected code, and Human-in-the-Loop approval controls.
  * Built `PR Summary Agent` and `Report Generator` (`reports/report_generator.py`) with `.md` and `.json` export.
  * Added the interactive `Severity Dashboard` with **Code Health Score (`0–100`)** and visual charts.
  * Built the multi-turn `RAG Conversational Code Assistant` (`/api/v1/chat`) and optimized end-to-end pipeline speed to complete in under 15 seconds.
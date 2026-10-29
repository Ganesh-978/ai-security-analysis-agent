# 🛡️ AI Code Review & Security Analysis Agent

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph%20%7C%20LangChain-1C3C3C)
![RAG](https://img.shields.io/badge/Vector%20RAG-ChromaDB%20%2B%20FAISS-orange)
![SAST](https://img.shields.io/badge/SAST-AST%20%7C%20Tree--sitter%20%7C%20Bandit-critical)

An enterprise-grade, multi-agent **Static Application Security Testing (SAST)** and **Automated Code Quality Review** platform for **Python** and **Java**. Built using a **6-Layer AI Security Architecture** and orchestrated with **LangGraph**, the system combines deterministic static code analysis (**AST**, **Tree-sitter**, **Bandit**, **Semgrep**, **Pylint**, **SpotBugs**, **PMD**, **Checkstyle**, **Radon**) with **Retrieval-Augmented Generation (RAG)** over an indexed **OWASP Top 10, CWE, SEI CERT, and Clean Code Knowledge Base** (**ChromaDB**, **FAISS**, and **Sentence Transformers**).

---

## 📖 Table of Contents

1. [Problem Statement & Project Objective](#-1-problem-statement--project-objective)
2. [6-Layer System Architecture](#-2-6-layer-system-architecture)
3. [7-Stage Multi-Agent Execution Workflow](#-3-7-stage-multi-agent-execution-workflow)
4. [Core Agents & Technical Capabilities](#-4-core-agents--technical-capabilities)
5. [Technology Stack & Tooling Matrix](#-5-technology-stack--tooling-matrix)
6. [Repository Directory Structure](#-6-repository-directory-structure)
7. [Installation & Environment Setup](#-7-installation--environment-setup)
8. [Running the Platform](#-8-running-the-platform)
9. [Live Demonstration Walkthrough (Evaluation Guide)](#-9-live-demonstration-walkthrough-evaluation-guide)
10. [REST API Specification](#-10-rest-api-specification)
11. [Agile Milestone Roadmap](#-11-agile-milestone-roadmap)

---

## 🎯 1. Problem Statement & Project Objective

Software engineering teams frequently face inconsistent code quality, undetected security vulnerabilities, and slow, subjective manual code reviews. Developers often lack immediate access to contextual secure coding standards and actionable remediation guidance during active development—leaving critical vulnerabilities undetected until late in the software development lifecycle (SDLC).

### Key Objectives
* **Deterministic Syntax Gatekeeping**: Automatically detect whether submitted code is **Python** or **Java** and validate syntax structure using **AST** and **Tree-sitter** before invoking downstream AI agents.
* **Hybrid SAST + LLM Reasoning**: Combine static rule scanners with parallel LLM agents so findings are both deterministic (exact line numbers) and context-aware (exploit impact and refactored code).
* **Grounded RAG Knowledge Base**: Index **OWASP Top 10 (A01–A10)**, **CWE**, **SEI CERT**, **Bandit**, **PMD**, **SpotBugs**, and **Clean Code** guidelines locally using **Sentence Transformers (`all-MiniLM-L6-v2`)**, **ChromaDB**, and **FAISS**.
* **Actionable Developer Portal**: Deliver a split-screen **Streamlit** interface backed by **FastAPI** and **SQLite** with 5-tier severity scoring, 4-dimensional complexity metrics, and best-practice code suggestions.

---

## 🏗️ 2. 6-Layer System Architecture

The platform is engineered around a modular 6-layer architecture:

| Layer | Architectural Layer | Core Responsibilities & Technologies |
| :--- | :--- | :--- |
| **Layer 1** | **Code Input & Syntax Gatekeeper** | Accepts pasted code or `.py` / `.java` file uploads. Automatically detects language and validates grammar via Python `ast` and `Tree-sitter` (`tree-sitter-python`, `tree-sitter-java`). |
| **Layer 2** | **Static Analysis Engine (SAST)** | Executes non-execution static analysis across Python (`Bandit`, `Semgrep`, `Pylint`, `Radon`), Java (`SpotBugs`, `PMD`, `Checkstyle`), and Enterprise (`SonarQube`, `Snyk`) rule patterns. |
| **Layer 3** | **Multi-Agent AI Orchestration** | Coordinates parallel agent execution (`StateGraph` fan-out / fan-in) using `LangGraph` and `LangChain`. |
| **Layer 4** | **LLM Processing & Vector RAG** | Grounds `Google Gemini` (`gemini-2.5-flash`) in curated security standards stored in `ChromaDB` and searched in-memory via `FAISS` using `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`). |
| **Layer 5** | **Severity Scoring & Report Engine** | Computes Code Quality Assessment scores, 4 complexity metrics, and classifies findings across the 5-tier Severity Pyramid (`Critical`, `High`, `Medium`, `Low`, `Informational`). |
| **Layer 6** | **User Interface & Persistence** | Split-screen `Streamlit` developer portal decoupled via a `FastAPI` REST backend with automated audit persistence in `SQLite` (`data/reviews.db`). |

---

## 🔄 3. 7-Stage Multi-Agent Execution Workflow

~~~text
+-------------------------------------------------------------------------+
| Stage 1: Developer Submits Source Code (Paste or .py / .java Upload)    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Stage 2: Auto-Language Detection & AST / Tree-sitter Syntax Gatekeeper  |
|          -> If Syntax Invalid: Block Pipeline & Highlight Exact Line    |
+-------------------------------------------------------------------------+
                                    | (Valid Syntax)
                                    v
+-------------------------------------------------------------------------+
| Stage 3: Layer 2 SAST Scan + Layer 4 RAG Retrieval (ChromaDB -> FAISS)  |
+-------------------------------------------------------------------------+
                                    |
             +----------------------+----------------------+
             | (Parallel Fan-Out via LangGraph StateGraph) |
             v                                             v
+-----------------------------------+   +---------------------------------+
| Stage 3A: Code Analysis Agent     |   | Stage 4: Security Vulnerability |
| - Code Smells & Linting           |   |          Agent (SAST + LLM)     |
| - 4 Complexity Metrics            |   | - Full OWASP Top 10 (A01-A10)   |
| - 6 Design Anti-Patterns          |   | - CWE / CERT / Bandit / SpotBugs|
| - Best Practice Validation        |   | - 8 Secure Coding Guidelines    |
+-----------------------------------+   +---------------------------------+
             |                                             |
             +----------------------+----------------------+
                                    | (Parallel Fan-In)
                                    v
+-------------------------------------------------------------------------+
| Stage 5: OWASP Top 10 (A01-A10) & CWE Standard Rule Matching            |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Stage 6: Severity Scoring Engine & Technical Debt Calculation           |
|          (Critical | High | Medium | Low | Informational)               |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Stage 7: Unified Findings Report Generation (SQLite + Streamlit Portal) |
+-------------------------------------------------------------------------+
~~~

---

## 🧠 4. Core Agents & Technical Capabilities

### A. Code Analysis Agent
Evaluates structural quality, maintainability, and software design without executing the code:
1. **Four Dimensions of Code Complexity**:
   * **Cyclomatic Complexity**: Quantifies independent decision paths (`if`, `for`, `while`, `case`, `catch`) and assigns a maintainability risk rank (`A` through `F`).
   * **Cognitive Complexity**: Measures human readability and penalizes deeply nested control flow structures.
   * **Time Complexity**: Estimates asymptotic execution time growth ($\mathcal{O}(1)$, $\mathcal{O}(n)$, $\mathcal{O}(n^2)$, $\mathcal{O}(n^k)$) from loop nesting depth.
   * **Space Complexity**: Estimates auxiliary memory allocation growth ($\mathcal{O}(1)$ vs. $\mathcal{O}(n)$).
2. **Six Common Design Anti-Patterns**:
   * **God Object**: Single class centralizing excessive methods and responsibilities.
   * **Spaghetti Code**: Deeply nested, unstructured control logic.
   * **Blob Class**: Data-heavy class dominating application state and behavior.
   * **Lava Flow**: Dead, commented-out, or experimental legacy code left in production.
   * **Golden Hammer**: Overuse of awkward or inappropriate constructs.
   * **Copy-Paste Programming**: Duplicated code blocks violating DRY principles.
3. **Code Quality Assessment Metrics**:
   * **Maintainability Score** ($0\text{--}100$)
   * **Complexity Health Score** ($0\text{--}100$)
   * **Code Duplication Percentage** ($\%$)
   * **Documentation & Comment Coverage** ($\%$)
   * **Estimated Technical Debt** (in minutes)

### B. Security Vulnerability Agent
Combines SAST pattern matching with RAG-grounded LLM analysis across **all OWASP Top 10 (A01–A10)** categories and **8 Core Secure Coding Guidelines**:
* **OWASP Top 10 & CWE Coverage**:
  * **A01: Broken Access Control** (CSRF `CWE-352`, Path Traversal `CWE-22`, Overly Permissive Permissions `CWE-732`, IDOR)
  * **A02: Cryptographic Failures** (Hardcoded Secrets `CWE-798`, Weak Hashing `MD5`/`SHA-1` `CWE-328`, Weak Ciphers `DES`/`ECB` `CWE-327`, Insecure PRNG `CWE-338`)
  * **A03: Injection** (SQL Injection `CWE-89`, Cross-Site Scripting / XSS `CWE-79`, OS Command Injection `CWE-78`, Code Injection `eval`/`exec` `CWE-95`)
  * **A04: Insecure Design** (Missing validation & business logic flaws)
  * **A05: Security Misconfiguration** (Debug mode enabled `CWE-489`, SSL/TLS verification disabled `CWE-295`, XML External Entity / XXE `CWE-611`)
  * **A06: Vulnerable & Outdated Components** (Deprecated/unsafe APIs)
  * **A07: Identification & Authentication Failures** (Unverified JWT signatures `CWE-347`, hardcoded passwords)
  * **A08: Software & Data Integrity Failures** (Insecure deserialization via `pickle`, `yaml.load`, `ObjectInputStream` `CWE-502`)
  * **A09: Security Logging & Monitoring Failures** (Swallowed security exceptions `CWE-390`, improper error handling)
  * **A10: Server-Side Request Forgery (SSRF)** (Unvalidated outbound HTTP requests `CWE-918`)
* **6 Mandatory Structured Security Report Fields per Finding**:
  1. **Vulnerability Name** (Standardized classification)
  2. **Severity Level** (`Critical`, `High`, `Medium`, `Low`, `Informational`)
  3. **Affected Line Number** (Exact line reference in source file)
  4. **Risk Description** (Plain-language explanation of exploit mechanics and impact)
  5. **Recommendation** (Actionable remediation steps grounded in OWASP/CERT standards)
  6. **Secure Coding Suggestion** (Refactored, copy-ready secure code snippet)

---

## 🛠️ 5. Technology Stack & Tooling Matrix

| Category | Tools & Libraries Used | Role in Project |
| :--- | :--- | :--- |
| **Multi-Agent & LLM** | `LangGraph`, `LangChain`, `Google Gemini` | Parallel agent state machine orchestration and contextual vulnerability reasoning. |
| **Vector Store & Search** | `ChromaDB`, `FAISS` (`faiss-cpu`) | `ChromaDB` persists document embeddings on disk; `FAISS` performs fast in-memory similarity search. |
| **Embeddings** | `Sentence Transformers`, `HuggingFaceEmbeddings` | Local embedding generation via `sentence-transformers/all-MiniLM-L6-v2`. |
| **Document Ingestion** | `Unstructured`, `PyPDF`, `Markdown` | Loads `.md` and `.pdf` security standards from `knowledge_base/`. |
| **Syntax & AST Parsing** | Python `ast`, `Tree-sitter` | Builds syntax trees for Python and Java to validate grammar and count AST nodes. |
| **Python SAST & Quality** | `Bandit`, `Semgrep`, `Pylint`, `Radon`, `Ruff` | Scans Python code for security flaws, complexity, and PEP8/maintainability issues. |
| **Java SAST & Quality** | `SpotBugs`, `PMD`, `Checkstyle`, `SEI CERT` | Detects Java resource leaks, SQLi, weak crypto, empty catch blocks, and naming violations. |
| **Enterprise Standards** | `SonarQube`, `Snyk`, `OWASP Top 10`, `CWE` | Maps findings to enterprise continuous-inspection and vulnerability classifications. |
| **Backend & Storage** | `FastAPI`, `Uvicorn`, `SQLite3`, `Pydantic` | RESTful API service layer, strict schema validation, and persistent review history. |
| **Frontend Portal** | `Streamlit` | Interactive split-screen developer portal with live validation and tabbed reports. |

---

## 📂 6. Repository Directory Structure

~~~text
ai-security-analysis-agent/
├── .streamlit/
│   └── config.toml                  # Streamlit server & file-watcher configuration
├── data/
│   ├── chroma_db/                   # Persistent ChromaDB vector database storage
│   └── reviews.db                   # SQLite database storing historical review reports
├── knowledge_base/                  # Curated Secure Coding & Quality Knowledge Base
│   ├── cert/                        # SEI CERT Oracle Secure Coding Standard for Java
│   ├── clean_code/                  # Clean Code, Refactoring & Design Anti-Pattern rules
│   ├── cwe/                         # CWE Top Software Weaknesses specifications
│   ├── java/                        # PMD & SpotBugs Java static analysis rules
│   ├── owasp/                       # OWASP Top 10 (A01-A10) security guidelines
│   └── python/                      # Bandit & Python secure coding rules
├── llm/
│   ├── gemini_client.py             # Google Gemini ChatModel initialization & retry config
│   └── prompt_manager.py            # Structured system prompts for Code & Security Agents
├── models/
│   └── schemas.py                   # Pydantic data models for validation, metrics & reports
├── parsers/
│   ├── code_validator.py            # Auto Python/Java language detector + AST/Tree-sitter gatekeeper
│   └── output_parser.py             # Resilient JSON array extractor for agent responses
├── rag/
│   ├── chroma_db.py                 # ChromaDB persistent client & FAISS index helpers
│   ├── chunking.py                  # RecursiveCharacterTextSplitter semantic chunking
│   ├── embeddings.py                # Singleton HuggingFaceEmbeddings (all-MiniLM-L6-v2)
│   ├── ingestion.py                 # Offline ETL pipeline to index knowledge_base/ into ChromaDB
│   ├── loader.py                    # UnstructuredMarkdownLoader (.md) & PyPDFLoader (.pdf)
│   └── retriever.py                 # High-speed cached FAISS retrieval over ChromaDB embeddings
├── sample_codes/
│   ├── vulnerable_python_sample.py  # Python test sample with known OWASP flaws & code smells
│   └── VulnerableJavaSample.java    # Java test sample with known SpotBugs/PMD/CERT flaws
├── services/
│   ├── api.py                       # FastAPI REST endpoints (/health, /api/v1/analyze, /api/v1/history)
│   └── database.py                  # SQLite database initialization & CRUD operations
├── src/
│   ├── agents.py                    # SAST/RAG node, Code Agent, Security Agent & Scoring Engine
│   ├── state.py                     # LangGraph ReviewWorkflowState TypedDict schema
│   └── workflow.py                  # Parallel LangGraph StateGraph compilation & runner
├── tests/
│   └── test_milestone2_agents.py    # Automated accuracy validation script for Python & Java
├── tools/
│   └── static_analyzer.py           # Layer 2 SAST scanner, 4-complexity & quality metric engine
├── ui/
│   └── app.py                       # Split-screen Streamlit developer dashboard
├── .env                             # Environment variables (API keys & paths - gitignored)
├── .gitignore                       # Excludes .venv, .env, __pycache__, and local .db files
├── pyproject.toml                   # Project metadata and uv dependency lock configuration
├── requirements.txt                 # Required Python libraries
└── README.md                        # Project documentation
~~~

---

## ⚙️ 7. Installation & Environment Setup

### Step 1: Clone the Repository
~~~powershell
git clone https://github.com/Ganesh-978/ai-security-analysis-agent.git
cd ai-security-analysis-agent
~~~

### Step 2: Create & Activate Virtual Environment
~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

### Step 3: Install Required Dependencies
Using `pip` or `uv`:
~~~powershell
pip install -r requirements.txt
uv add tree-sitter tree-sitter-python tree-sitter-java bandit radon
~~~

### Step 4: Configure Environment Variables (`.env`)
Create a `.env` file in the root directory of the project:
~~~env
GOOGLE_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./data/chroma_db
FAISS_INDEX_DIR=./data/faiss_index
~~~

### Step 5: Index the Knowledge Base into ChromaDB
Run the RAG ingestion pipeline once to load, chunk, embed, and store all `.md` and `.pdf` documents from `knowledge_base/` into `./data/chroma_db`:
~~~powershell
python rag/ingestion.py
~~~

---

## 🚀 8. Running the Platform

Open two terminals in VS Code with your `.venv` activated:

### Terminal 1: Start the FastAPI Backend Server
~~~powershell
uvicorn services.api:app --reload --host 127.0.0.1 --port 8000
~~~
* **Backend API URL**: `http://127.0.0.1:8000`
* **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`

### Terminal 2: Launch the Streamlit Developer Portal
~~~powershell
streamlit run ui/app.py
~~~
* **Streamlit Web App**: `http://localhost:8501`

### Run Automated Detection Accuracy Tests (Optional)
~~~powershell
python tests/test_milestone2_agents.py
~~~

---

## 🖥️ 9. Live Demonstration Walkthrough (Evaluation Guide)

Follow these steps during project evaluation to demonstrate all system capabilities:

1. **Automatic Language Detection & AST / Tree-sitter Gatekeeper**:
   * Paste any Python or Java snippet into the left-hand editor (or upload `sample_codes/vulnerable_python_sample.py` or `sample_codes/VulnerableJavaSample.java`).
   * Point out the live status bar showing **Auto-Detected Language (`Python` or `Java`)**, **Parser Used (`AST / Tree-sitter`)**, and **Syntax Tree Node Count**.
2. **Syntax Error Blocking**:
   * Intentionally remove a colon `:` in Python or a semicolon `;` in Java.
   * Show that the **Syntax Gatekeeper** immediately flags the exact line number and offending statement and blocks the multi-agent pipeline from executing.
3. **Parallel Multi-Agent Execution & Severity Scoring**:
   * Fix the syntax error and click **"🚀 Run SAST + Parallel Multi-Agent Analysis"**.
   * On the right panel, highlight:
     * **Stage 6 Severity Scoring Breakdown** (`Critical`, `High`, `Medium`, `Low`, `Informational`).
     * **Code Quality Assessment Metrics** (`Maintainability Score`, `Complexity Score`, `Duplication %`, `Documentation %`, and `Technical Debt`).
     * **Four Complexity Metrics** (`Cyclomatic`, `Cognitive`, `Time Complexity`, `Space Complexity`).
4. **Structured 6-Field Security & Quality Reports**:
   * Open the **Unified Findings Report**, **Security Vulnerability Report**, **Code Analysis Report**, and **SAST & Linter Alerts** tabs.
   * Expand any finding card to show the 6 mandatory report fields, including the matched **OWASP Top 10 / CWE / Bandit / SpotBugs rule** and the refactored **Secure Coding Suggestion**.
5. **SQLite Audit Persistence**:
   * Open the **SQLite History** tab to show all completed reviews persisted inside `data/reviews.db`.

---

## 🔌 10. REST API Specification

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns service health status and architecture version. |
| `POST` | `/api/v1/analyze` | Validates code syntax, runs Layer 2 SAST + Layer 3 Parallel LangGraph Agents, saves to SQLite, and returns the structured `AnalysisReport`. |
| `GET` | `/api/v1/history` | Fetches the 10 most recent code review summaries from the SQLite database. |

---

## 📈 11. Agile Milestone Roadmap

* ✅ **Milestone 1 (Sprint 1 — Weeks 1–2)**:
  * Studied OWASP Top 10, CWE, SEI CERT, and Clean Code standards.
  * Designed modular repository structure and Pydantic schemas (`models/schemas.py`).
  * Built Code Submission Module with automatic Python/Java detection and syntax validation (`parsers/code_validator.py`).
  * Built Secure Coding Knowledge Base & RAG pipeline using `Unstructured`, `PyPDF`, `Sentence Transformers`, `ChromaDB`, and `FAISS` (`rag/`).
* ✅ **Milestone 2 (Sprint 2 — Weeks 3–4)**:
  * Implemented Layer 2 SAST & Complexity Engine (`Tree-sitter`, `AST`, `Bandit`, `Radon`, `SpotBugs`/`PMD`/`Checkstyle` rules in `tools/static_analyzer.py`).
  * Built `Code Analysis Agent` and `Security Vulnerability Agent` with 6-field structured reporting (`src/agents.py`).
  * Implemented parallel multi-agent orchestration in `LangGraph` (`src/workflow.py`) with OWASP Rule Matching and Severity Scoring Engine.
  * Integrated decoupled `FastAPI` backend (`services/api.py`), `SQLite` persistence (`services/database.py`), and enhanced `Streamlit` portal (`ui/app.py`).
* ⏳ **Milestone 3 (Upcoming — Weeks 5–6)**:
  * Dedicated `Remediation Agent` for automated full-file patch generation.
  * `PR Summary Agent` for pull-request ready markdown summaries.
  * RAG-powered `Conversational Code Assistant` for interactive Q&A on flagged findings.
  * Exportable PDF, Markdown, and JSON compliance reports.
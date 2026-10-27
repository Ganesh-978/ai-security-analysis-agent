# ui/app.py
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
import streamlit as st
from parsers.code_validator import validate_submission
from src.workflow import run_milestone2_pipeline
from services.database import save_review_to_db, get_recent_reviews

API_URL = "http://127.0.0.1:8000/api/v1/analyze"

st.set_page_config(
    page_title="AI Code Review & Security Analysis Agent",
    layout="wide",
)

st.title("🛡️ AI Code Review & Security Analysis Agent")
st.caption(
    "6-Layer Architecture: Code Input → Static Analysis (Bandit/SpotBugs/PMD/Pylint/Radon) "
    "→ LangGraph Parallel Agents → Gemini + OWASP RAG → Severity Scoring → Streamlit/FastAPI/SQLite"
)

if "m2_report" not in st.session_state:
    st.session_state.m2_report = None

SEVERITY_ICON = {
    "Critical": "🔴 **CRITICAL**",
    "High": "🟠 **HIGH**",
    "Medium": "🟡 **MEDIUM**",
    "Low": "🔵 **LOW**",
    "Informational": "⚪ **INFORMATIONAL**",
}

left_col, right_col = st.columns([1, 1.25], gap="large")

with left_col:
    st.subheader("Layer 1: Code Submission & Syntax Gatekeeper")

    uploaded_file = st.file_uploader(
        "Upload Python (.py) or Java (.java) file", type=["py", "java"]
    )

    default_code = ""
    filename = None
    if uploaded_file is not None:
        filename = uploaded_file.name
        default_code = uploaded_file.getvalue().decode("utf-8", errors="replace")

    code_input = st.text_area(
        "Paste Source Code (Auto-detects Python or Java):",
        value=default_code,
        height=390,
        placeholder="Paste Python or Java source code here...",
    )

    validation = validate_submission(code_input, filename=filename)

    if code_input.strip():
        if validation.detected_language == "python":
            st.info("🐍 **Auto-Detected Language:** Python")
        elif validation.detected_language == "java":
            st.info("☕ **Auto-Detected Language:** Java")
        else:
            st.warning("❓ **Auto-Detected Language:** Unknown / Unsupported")

        if validation.is_valid:
            st.success("✅ **Syntax Validation Passed** — Ready for Static + Multi-Agent Analysis")
        else:
            st.error(
                f"🚫 **Syntax Error on Line {validation.line_number}:** {validation.error_message}"
            )
            if validation.offending_line:
                st.code(validation.offending_line, language="text")

    run_btn = st.button(
        "🚀 Run Static Analysis + Parallel Multi-Agent Review",
        type="primary",
        use_container_width=True,
    )

with right_col:
    st.subheader("Layers 2–6: Quality Metrics, Complexity & Findings")

    if run_btn:
        if not code_input.strip():
            st.warning("Please paste or upload source code on the left first.")
        elif not validation.is_valid:
            st.session_state.m2_report = None
            st.error(
                "🚫 **Blocked by Syntax Gatekeeper:** Fix syntax errors before running the agents."
            )
        else:
            fname = filename or (
                "snippet.py" if validation.detected_language == "python" else "Snippet.java"
            )
            with st.spinner(
                "Running Layer 2 Static Scanners, Layer 3 LangGraph Agents & Layer 4 OWASP RAG..."
            ):
                try:
                    resp = requests.post(
                        API_URL,
                        json={
                            "filename": fname,
                            "code": code_input,
                            "language": validation.detected_language,
                        },
                        timeout=120,
                    )
                    if resp.status_code == 200:
                        st.session_state.m2_report = resp.json()
                    else:
                        raise RuntimeError(resp.text)
                except Exception:
                    raw_res = run_milestone2_pipeline(
                        code=code_input,
                        language=validation.detected_language,
                        filename=fname,
                    )
                    raw_res["filename"] = fname
                    raw_res["language"] = validation.detected_language
                    save_review_to_db(raw_res)
                    st.session_state.m2_report = raw_res

    if st.session_state.m2_report:
        rep = st.session_state.m2_report
        sev = rep.get("severity_breakdown", {})
        cm = rep.get("complexity_metrics", {})
        qa = rep.get("quality_assessment", {})

        # 1. Severity Scoring Pyramid Breakdown
        st.markdown("##### 🔺 Severity Scoring Breakdown")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("🔴 Critical", sev.get("Critical", 0))
        s2.metric("🟠 High", sev.get("High", 0))
        s3.metric("🟡 Medium", sev.get("Medium", 0))
        s4.metric("🔵 Low", sev.get("Low", 0))
        s5.metric("⚪ Informational", sev.get("Informational", 0))

        # 2. Code Quality Assessment (Slide 10)
        st.markdown("##### 📊 Code Quality Assessment & Four Complexity Metrics")
        q1, q2, q3, q4, q5 = st.columns(5)
        q1.metric("Maintainability", f"{qa.get('maintainability_score', 0)}/100")
        q2.metric("Complexity Score", f"{qa.get('complexity_score', 0)}/100")
        q3.metric("Duplication", f"{qa.get('duplication_percentage', 0)}%")
        q4.metric("Documentation", f"{qa.get('documentation_score', 0)}%")
        q5.metric("Tech Debt", f"{qa.get('technical_debt_minutes', 0)} mins")

        # 3. Four Types of Code Complexity (Slide 15)
        c1, c2, c3, c4 = st.columns(4)
        c1.info(f"**Cyclomatic:** {cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})")
        c2.info(f"**Cognitive:** {cm.get('cognitive_complexity', 0)}")
        c3.info(f"**Time:** {cm.get('time_complexity', 'O(1)')}")
        c4.info(f"**Space:** {cm.get('space_complexity', 'O(1)')}")

        unified = rep.get("unified_findings", [])
        sec_list = rep.get("security_findings", [])
        qual_list = rep.get("quality_findings", [])
        static_flags = rep.get("static_tool_flags", [])

        t_uni, t_sec, t_qual, t_stat, t_db = st.tabs([
            f"📋 Unified Findings ({len(unified)})",
            f"🔒 Security Agent ({len(sec_list)})",
            f"🧹 Code Analysis Agent ({len(qual_list)})",
            f"🛠️ Static Analysis Tools ({len(static_flags)})",
            "🗄️ SQLite History",
        ])

        def render_finding_cards(items, lang):
            if not items:
                st.success("No issues flagged in this section.")
                return
            for item in items:
                icon = SEVERITY_ICON.get(item["severity"], item["severity"])
                title = (
                    f"{icon} | [{item['id']}] {item['title']} "
                    f"— {item['line_reference']} ({item['issue_type']})"
                )
                with st.expander(title):
                    st.markdown(
                        f"- **Agent:** `{item['agent_source']}` (`{item.get('sub_category', '')}`)\n"
                        f"- **Classification / Anti-Pattern:** `{item['issue_type']}`\n"
                        f"- **Tool / Standard Reference:** `{item.get('tool_or_standard', '')}`\n"
                        f"- **Location:** `{item['line_reference']}`"
                    )
                    if item.get("code_snippet"):
                        st.code(item["code_snippet"], language=lang)
                    st.markdown(f"**Analysis:** {item['description']}")
                    if item.get("recommendation"):
                        st.markdown(f"💡 **Recommendation:** {item['recommendation']}")

        with t_uni:
            render_finding_cards(unified, validation.detected_language)

        with t_sec:
            render_finding_cards(sec_list, validation.detected_language)

        with t_qual:
            render_finding_cards(qual_list, validation.detected_language)

        with t_stat:
            st.caption("Layer 2 Deterministic Static Scanner Alerts (Bandit, SpotBugs, Semgrep, Pylint, PMD, Radon)")
            if not static_flags:
                st.success("No static pattern violations triggered.")
            for sf in static_flags:
                st.markdown(
                    f"- **[{sf['severity']}] {sf['tool']}** ({sf['line']}): {sf['message']}"
                )
                if sf.get("snippet"):
                    st.code(sf["snippet"], language=validation.detected_language)

        with t_db:
            st.caption("Layer 6 SQLite Database (`data/reviews.db`) — Recent Stored Reviews")
            history_rows = get_recent_reviews(limit=10)
            if history_rows:
                st.dataframe(history_rows, use_container_width=True)
            else:
                st.info("No reviews stored in SQLite yet.")
    else:
        st.info(
            "Paste valid Python or Java code on the left and click **Run Static Analysis + Parallel Multi-Agent Review**."
        )
        
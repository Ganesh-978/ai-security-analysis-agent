import os
import sys
from pathlib import Path

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
import streamlit as st
from parsers.code_validator import validate_submission
from services.database import save_review_to_db, get_recent_reviews

API_URL = "http://127.0.0.1:8000/api/v1/analyze"

st.set_page_config(
    page_title="AI Code Review & Security Analysis Agent",
    layout="wide",
)

st.title("🛡️ AI Code Review & Security Analysis Agent")
st.caption(
    "Pipeline: Code Input → AST/Tree-sitter Validation → SAST (Bandit/Semgrep/Pylint/SpotBugs/PMD/Checkstyle) "
    "→ Parallel Code & Security Agents → OWASP Rule Matching → Severity Scoring → Unified Report"
)

if "review_report" not in st.session_state:
    st.session_state.review_report = None

SEVERITY_ICON = {
    "Critical": "🔴 **CRITICAL**",
    "High": "🟠 **HIGH**",
    "Medium": "🟡 **MEDIUM**",
    "Low": "🔵 **LOW**",
    "Informational": "⚪ **INFORMATIONAL**",
}

left_col, right_col = st.columns([1, 1.25], gap="large")

with left_col:
    st.subheader("Code Submission & Syntax Validation")

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
        lang_label = (
            "🐍 **Python**"
            if validation.detected_language == "python"
            else "☕ **Java**"
            if validation.detected_language == "java"
            else "❓ **Unknown**"
        )
        st.info(
            f"**Auto-Detected Language:** {lang_label} | "
            f"**Parser:** `{validation.parser_used}` | "
            f"**Syntax Tree Nodes:** `{validation.ast_node_count}`"
        )

        if validation.is_valid:
            st.success("✅ **Syntax Validation Passed** — Ready for SAST + Multi-Agent Analysis")
        else:
            st.error(
                f"🚫 **Syntax Error on Line {validation.line_number}:** {validation.error_message}"
            )
            if validation.offending_line:
                st.code(validation.offending_line, language="text")

    run_btn = st.button(
        "🚀 Analyze Code",
        type="primary",
        width="stretch",
    )

with right_col:
    st.subheader("Security & Code Quality Analysis Report")

    if run_btn:
        if not code_input.strip():
            st.warning("Please paste or upload source code on the left first.")
        elif not validation.is_valid:
            st.session_state.review_report = None
            st.error(
                "🚫 **Blocked by Syntax Gatekeeper:** Fix syntax errors before running analysis."
            )
        else:
            fname = filename or (
                "snippet.py" if validation.detected_language == "python" else "Snippet.java"
            )
            with st.spinner("Running SAST Scanners, Parallel Agents & OWASP Rule Matching..."):
                try:
                    resp = requests.post(
                        API_URL,
                        json={
                            "filename": fname,
                            "code": code_input,
                            "language": validation.detected_language,
                        },
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        st.session_state.review_report = resp.json()
                    else:
                        raise RuntimeError(resp.text)
                except Exception:
                    from src.workflow import run_review_pipeline

                    raw_res = run_review_pipeline(
                        code=code_input,
                        language=validation.detected_language,
                        filename=fname,
                    )
                    raw_res["filename"] = fname
                    raw_res["language"] = validation.detected_language
                    save_review_to_db(raw_res)
                    st.session_state.review_report = raw_res

    if st.session_state.review_report:
        rep = st.session_state.review_report
        sev = rep.get("severity_breakdown", {})
        cm = rep.get("complexity_metrics", {})
        qa = rep.get("quality_assessment", {})

        st.markdown("##### 🔺 Severity Scoring Breakdown")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("🔴 Critical", sev.get("Critical", 0))
        s2.metric("🟠 High", sev.get("High", 0))
        s3.metric("🟡 Medium", sev.get("Medium", 0))
        s4.metric("🔵 Low", sev.get("Low", 0))
        s5.metric("⚪ Informational", sev.get("Informational", 0))

        st.markdown("##### 📊 Code Quality Assessment & Complexity Metrics")
        q1, q2, q3, q4, q5 = st.columns(5)
        q1.metric("Maintainability", f"{qa.get('maintainability_score', 0)}/100")
        q2.metric("Complexity Score", f"{qa.get('complexity_score', 0)}/100")
        q3.metric("Duplication", f"{qa.get('duplication_percentage', 0)}%")
        q4.metric("Documentation", f"{qa.get('documentation_score', 0)}%")
        q5.metric("Tech Debt", f"{qa.get('technical_debt_minutes', 0)} mins")

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
            f"🔒 Security Vulnerabilities ({len(sec_list)})",
            f"🧹 Code Quality ({len(qual_list)})",
            f"🛠️ SAST & Linter Alerts ({len(static_flags)})",
            "🗄️ Review History",
        ])

        def render_structured_report_cards(items, lang):
            if not items:
                st.success("No issues detected in this category.")
                return
            for item in items:
                icon = SEVERITY_ICON.get(item["severity"], item["severity"])
                vuln_name = item.get("vulnerability_name") or item.get("issue_type", "Issue")
                header = (
                    f"{icon} | [{item['id']}] {vuln_name}: {item['title']} "
                    f"— {item['line_reference']}"
                )
                with st.expander(header):
                    st.markdown(
                        f"1. **Vulnerability / Issue Name:** `{vuln_name}`\n"
                        f"2. **Severity Level:** {icon}\n"
                        f"3. **Affected Line Number:** `{item['line_reference']}`\n"
                        f"- **Matched OWASP / Standard Rule:** `{item.get('owasp_category') or item.get('tool_or_standard', '')}`\n"
                        f"- **Detection Tool / Agent:** `{item['agent_source']}` (`{item.get('tool_or_standard', '')}`)"
                    )
                    if item.get("code_snippet"):
                        st.markdown("**Flagged Source Line(s):**")
                        st.code(item["code_snippet"], language=lang)
                    st.markdown(f"4. **Risk Description:**\n{item['description']}")
                    st.markdown(f"5. **Recommendation:**\n{item.get('recommendation', '')}")
                    if item.get("secure_code_suggestion"):
                        st.markdown("6. **Secure Coding Suggestion (Best-Practice Example):**")
                        st.code(item["secure_code_suggestion"], language=lang)

        with t_uni:
            render_structured_report_cards(unified, validation.detected_language)

        with t_sec:
            render_structured_report_cards(sec_list, validation.detected_language)

        with t_qual:
            render_structured_report_cards(qual_list, validation.detected_language)

        with t_stat:
            st.caption(
                "SAST & Static Linter Alerts (Python: Bandit, Semgrep, Pylint | Java: SpotBugs, PMD, Checkstyle | Enterprise: SonarQube, Snyk)"
            )
            if not static_flags:
                st.success("No static pattern violations triggered.")
            for sf in static_flags:
                st.markdown(
                    f"- **[{sf['severity']}] {sf.get('vulnerability_name', sf['type'])}** "
                    f"— `{sf['tool']}` ({sf['line']}): {sf['message']}"
                )
                if sf.get("snippet"):
                    st.code(sf["snippet"], language=validation.detected_language)

        with t_db:
            st.caption("SQLite Database (`data/reviews.db`) — Stored Analysis History")
            history_rows = get_recent_reviews(limit=10)
            if history_rows:
                st.dataframe(history_rows, width="stretch")
            else:
                st.info("No reviews stored in SQLite yet.")
    else:
        st.info("Paste valid Python or Java code on the left and click **Analyze Code**.")
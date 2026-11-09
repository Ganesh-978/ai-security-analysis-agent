import json
import os
import sys
from pathlib import Path

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import requests
import streamlit as st
from parsers.code_validator import validate_submission
from reports.report_generator import generate_full_markdown_report
from services.database import save_review_to_db, get_recent_reviews

API_BASE = "http://127.0.0.1:8000"
ANALYZE_URL = f"{API_BASE}/api/v1/analyze"
CHAT_URL = f"{API_BASE}/api/v1/chat"

st.set_page_config(
    page_title="AI Code Review & Security Analysis Agent",
    layout="wide",
)

st.title("🛡️ AI Code Review & Security Analysis Agent")
st.caption(
    "Multi-Agent Platform: Code Analysis Agent • Security Vulnerability Agent • "
    "AI Remediation Agent • PR Summary Agent • RAG Conversational Code Assistant"
)

if "review_report" not in st.session_state:
    st.session_state.review_report = None
if "submitted_code" not in st.session_state:
    st.session_state.submitted_code = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "remediation_status" not in st.session_state:
    st.session_state.remediation_status = {}

SEVERITY_ICON = {
    "Critical": "🔴 **CRITICAL**",
    "High": "🟠 **HIGH**",
    "Medium": "🟡 **MEDIUM**",
    "Low": "🔵 **LOW**",
    "Informational": "⚪ **INFORMATIONAL**",
}

CATEGORY_BADGE = {
    "Security Recommendation": "🔒 Security Recommendation",
    "Code Quality Recommendation": "🧹 Code Quality Recommendation",
    "Performance Recommendation": "⚡ Performance Recommendation",
    "Maintainability Recommendation": "🏗️ Maintainability Recommendation",
}

left_col, right_col = st.columns([1, 1.35], gap="large")

with left_col:
    st.subheader("1. Code Submission & Syntax Gatekeeper")

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
        height=400,
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
            f"**Language:** {lang_label} | "
            f"**Parser:** `{validation.parser_used}` | "
            f"**AST Nodes:** `{validation.ast_node_count}`"
        )

        if validation.is_valid:
            st.success("✅ **Syntax Validation Passed** — Ready for Multi-Agent Pipeline")
        else:
            st.error(
                f"🚫 **Syntax Error on Line {validation.line_number}:** {validation.error_message}"
            )
            if validation.offending_line:
                st.code(validation.offending_line, language="text")

    run_btn = st.button(
        "🚀 Run Full Multi-Agent Code Review",
        type="primary",
        width="stretch",
    )

with right_col:
    st.subheader("2. Developer Review Portal & Conversational Assistant")

    if run_btn:
        if not code_input.strip():
            st.warning("Please paste or upload source code on the left first.")
        elif not validation.is_valid:
            st.session_state.review_report = None
            st.error(
                "🚫 **Blocked by Syntax Gatekeeper:** Fix syntax errors before triggering the multi-agent pipeline."
            )
        else:
            fname = filename or (
                "snippet.py" if validation.detected_language == "python" else "Snippet.java"
            )
            with st.spinner(
                "Running Code Analysis, Security Vulnerability, Remediation, and PR Summary Agents..."
            ):
                try:
                    resp = requests.post(
                        ANALYZE_URL,
                        json={
                            "filename": fname,
                            "code": code_input,
                            "language": validation.detected_language,
                        },
                        timeout=75,
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

                st.session_state.submitted_code = code_input
                st.session_state.remediation_status = {}

    if st.session_state.review_report:
        rep = st.session_state.review_report
        sev = rep.get("severity_breakdown", {})
        cm = rep.get("complexity_metrics", {})
        qa = rep.get("quality_assessment", {})
        unified = rep.get("unified_findings", [])
        sec_list = rep.get("security_findings", [])
        qual_list = rep.get("quality_findings", [])
        rem_list = rep.get("remediation_plan", [])
        lang = rep.get("language", validation.detected_language)

        # Calculate Human-in-the-Loop Fix Progress
        total_issues = len(unified)
        resolved_count = sum(
            1
            for fid, status in st.session_state.remediation_status.items()
            if status in ("Approved & Applied", "Team Lead Approved")
        )
        progress_pct = int((resolved_count / total_issues) * 100) if total_issues > 0 else 100

        # Top KPI Summary Row
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("🏥 Code Health Score", f"{qa.get('code_health_score', 80.0)}/100")
        k2.metric("🔎 Total Issues", total_issues)
        k3.metric("🔒 Security Issues", len(sec_list))
        k4.metric("🧹 Quality / Smells", len(qual_list))
        k5.metric("✅ Fix Progress", f"{progress_pct}% ({resolved_count}/{total_issues})")

        t_dash, t_find, t_rem, t_pr, t_chat, t_exp, t_hist = st.tabs([
            "📊 Severity Dashboard",
            f"📋 Findings ({total_issues})",
            f"🛠️ AI Remediation ({len(rem_list)})",
            "📝 PR Summary",
            "💬 Conversational Assistant",
            "📥 Export Report",
            "🗄️ History",
        ])

        # TAB 1: Enterprise Severity Dashboard (Charts + KPIs)
        with t_dash:
            st.markdown("##### 🔺 Issues by Severity Level")
            s1, s2, s3, s4, s5 = st.columns(5)
            s1.metric("🔴 Critical", sev.get("Critical", 0))
            s2.metric("🟠 High", sev.get("High", 0))
            s3.metric("🟡 Medium", sev.get("Medium", 0))
            s4.metric("🔵 Low", sev.get("Low", 0))
            s5.metric("⚪ Informational", sev.get("Informational", 0))

            ch_col1, ch_col2 = st.columns(2)
            with ch_col1:
                st.markdown("**Severity Distribution Chart**")
                sev_df = pd.DataFrame({
                    "Severity": ["Critical", "High", "Medium", "Low", "Informational"],
                    "Count": [
                        sev.get("Critical", 0),
                        sev.get("High", 0),
                        sev.get("Medium", 0),
                        sev.get("Low", 0),
                        sev.get("Informational", 0),
                    ],
                }).set_index("Severity")
                st.bar_chart(sev_df)

            with ch_col2:
                st.markdown("**Security vs. Code Quality Breakdown**")
                cat_df = pd.DataFrame({
                    "Category": ["Security Vulnerabilities", "Code Quality & Smells"],
                    "Issues": [len(sec_list), len(qual_list)],
                }).set_index("Category")
                st.bar_chart(cat_df)

            st.markdown("##### 📐 Code Quality & Complexity Telemetry")
            m1, m2, m3, m4 = st.columns(4)
            m1.info(f"**Maintainability:** {qa.get('maintainability_score', 0)}/100")
            m2.info(f"**Cyclomatic:** {cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})")
            m3.info(f"**Time Complexity:** {cm.get('time_complexity', 'O(1)')}")
            m4.info(f"**Tech Debt:** {qa.get('technical_debt_minutes', 0)} mins")

        # TAB 2: Unified Findings Display Module
        with t_find:
            filter_type = st.radio(
                "Filter Findings:",
                ["All Unified Findings", "Security Vulnerabilities Only", "Code Quality & Smells Only"],
                horizontal=True,
            )
            display_items = (
                unified
                if filter_type == "All Unified Findings"
                else sec_list
                if filter_type == "Security Vulnerabilities Only"
                else qual_list
            )

            if not display_items:
                st.success("No issues detected in this view.")
            for item in display_items:
                icon = SEVERITY_ICON.get(item["severity"], item["severity"])
                v_name = item.get("vulnerability_name") or item.get("issue_type", "Issue")
                with st.expander(
                    f"{icon} | [{item['id']}] {v_name}: {item['title']} — {item['line_reference']}"
                ):
                    st.markdown(
                        f"- **Agent Source:** `{item['agent_source']}` (`{item.get('sub_category', '')}`)\n"
                        f"- **Standard / Tool Rule:** `{item.get('owasp_category') or item.get('tool_or_standard', '')}`\n"
                        f"- **Affected Line:** `{item['line_reference']}`"
                    )
                    if item.get("code_snippet"):
                        st.code(item["code_snippet"], language=lang)
                    st.markdown(f"**Risk & Impact Description:**\n{item['description']}")
                    st.markdown(f"**Quick Recommendation:**\n{item.get('recommendation', '')}")

        # TAB 3: AI Remediation Agent & Human-in-the-Loop Validation
        with t_rem:
            st.caption(
                "AI Remediation Agent: Explains root causes, retrieves OWASP/CERT standards, "
                "and generates corrected code examples with Human-in-the-Loop review controls."
            )
            if not rem_list:
                st.success("No remediations needed — code is clean!")
            for r in rem_list:
                fid = r["finding_id"]
                current_status = st.session_state.remediation_status.get(fid, "Pending Review")
                cat_label = CATEGORY_BADGE.get(
                    r.get("recommendation_category", ""), "🛠️ Remediation"
                )
                sev_badge = SEVERITY_ICON.get(r.get("severity", "Medium"), "🟡 MEDIUM")

                with st.expander(
                    f"{sev_badge} | Fix for [{fid}] {r['issue_title']} ({r['line_reference']}) — Status: {current_status}",
                    expanded=(r.get("severity") == "Critical"),
                ):
                    st.markdown(f"**Category:** `{cat_label}` | **Standard:** `{r['best_practice_guideline']}`")
                    st.markdown(f"**1. Root Cause Analysis:**\n{r['root_cause']}")
                    st.markdown(f"**2. Why This Issue Occurs:**\n{r['why_it_occurs']}")
                    st.markdown(f"**3. Recommended Fix Steps:**\n{r['fix_steps']}")

                    c_orig, c_fix = st.columns(2)
                    with c_orig:
                        st.markdown("❌ **Flagged Code:**")
                        st.code(r.get("original_code") or "// See affected line in source", language=lang)
                    with c_fix:
                        st.markdown("✅ **Corrected Secure Code:**")
                        st.code(r.get("corrected_code", ""), language=lang)

                    # Human-in-the-Loop Collaboration Control
                    new_status = st.selectbox(
                        f"Human-in-the-Loop Review Decision ({fid}):",
                        [
                            "Pending Review",
                            "Approved & Applied",
                            "Team Lead Approved",
                            "Rejected (Intentional Business Logic)",
                        ],
                        index=[
                            "Pending Review",
                            "Approved & Applied",
                            "Team Lead Approved",
                            "Rejected (Intentional Business Logic)",
                        ].index(current_status),
                        key=f"hitl_{fid}",
                    )
                    st.session_state.remediation_status[fid] = new_status

        # TAB 4: Pull Request Review Summary
        with t_pr:
            st.markdown(rep.get("pr_summary_markdown", ""))

        # TAB 5: RAG-Powered Conversational Code Assistant
        with t_chat:
            st.markdown("##### 💬 RAG-Powered Conversational Code Assistant")
            st.caption(
                "Ask follow-up questions about flagged vulnerabilities, code smells, or OWASP best practices."
            )

            # Quick-Ask Preset Buttons from Presentation Slide 4
            q_cols = st.columns(3)
            preset_questions = [
                "Explain this vulnerability.",
                "How do I fix SQL Injection?",
                "Why is duplicate code bad?",
                "Show secure coding practices.",
                "Explain this warning.",
                "Suggest better code.",
            ]
            selected_preset = None
            for idx, pq in enumerate(preset_questions):
                if q_cols[idx % 3].button(pq, key=f"preset_q_{idx}", width="stretch"):
                    selected_preset = pq

            custom_q = st.chat_input("Ask a question about your code, errors, or OWASP security rules...")
            active_question = selected_preset or custom_q

            if active_question:
                st.session_state.chat_history.append({"role": "user", "content": active_question})
                with st.spinner("Searching OWASP Knowledge Base & generating response..."):
                    findings_summary = json.dumps(unified[:6])
                    try:
                        c_resp = requests.post(
                            CHAT_URL,
                            json={
                                "question": active_question,
                                "language": lang,
                                "code_context": st.session_state.submitted_code or code_input,
                                "findings_context": findings_summary,
                                "chat_history": st.session_state.chat_history[:-1],
                            },
                            timeout=45,
                        )
                        if c_resp.status_code == 200:
                            ans_payload = c_resp.json()
                        else:
                            raise RuntimeError(c_resp.text)
                    except Exception:
                        from src.agents import run_conversational_assistant

                        ans_payload = run_conversational_assistant(
                            question=active_question,
                            language=lang,
                            code_context=st.session_state.submitted_code or code_input,
                            findings_context=findings_summary,
                            chat_history=st.session_state.chat_history[:-1],
                        )

                    formatted_reply = (
                        f"{ans_payload['answer']}\n\n"
                        f"---\n*🎯 Intent: `{ans_payload.get('intent', 'General')}` | "
                        f"📚 Grounded RAG Sources: `{', '.join(ans_payload.get('sources', ['OWASP KB']))}`*"
                    )
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": formatted_reply}
                    )

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # TAB 6: Exportable Code Review Report (.md & .json)
        with t_exp:
            st.markdown("##### 📥 Export Structured Code Review Report")
            md_report = generate_full_markdown_report(rep)
            st.download_button(
                "📄 Download Full Markdown Report (.md)",
                data=md_report,
                file_name=f"{rep.get('filename', 'code')}_review_report.md",
                mime="text/markdown",
                width="stretch",
            )
            st.download_button(
                "📦 Download Structured JSON Report (.json)",
                data=json.dumps(rep, indent=2),
                file_name=f"{rep.get('filename', 'code')}_review_report.json",
                mime="application/json",
                width="stretch",
            )
            with st.expander("Preview Markdown Report"):
                st.markdown(md_report)

        # TAB 7: SQLite Historical Reviews
        with t_hist:
            st.caption("SQLite Database (`data/reviews.db`) — Historical Code Quality & Security Trends")
            history_rows = get_recent_reviews(limit=15)
            if history_rows:
                st.dataframe(history_rows, width="stretch")
            else:
                st.info("No historical reviews stored yet.")
    else:
        st.info(
            "Paste valid Python or Java code on the left and click **Run Full Multi-Agent Code Review**."
        )
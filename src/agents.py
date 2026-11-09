import json
from typing import Dict, Any, List
from src.state import ReviewWorkflowState
from tools.static_analyzer import (
    compute_complexity_and_quality_metrics,
    run_static_pattern_scanners,
)
from rag.retriever import search_knowledge_base
from llm.gemini_client import get_llm
from llm.prompt_manager import (
    CODE_ANALYSIS_AGENT_PROMPT,
    SECURITY_VULNERABILITY_AGENT_PROMPT,
    REMEDIATION_AGENT_PROMPT,
    PR_SUMMARY_AGENT_PROMPT,
    CONVERSATIONAL_ASSISTANT_PROMPT,
)
from parsers.output_parser import parse_json_array

VALID_SEVERITIES = {"Critical", "High", "Medium", "Low", "Informational"}
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}
VALID_REC_CATEGORIES = {
    "Security Recommendation",
    "Code Quality Recommendation",
    "Performance Recommendation",
    "Maintainability Recommendation",
}

OWASP_TOP_10_MAP = {
    "access control": "OWASP A01 - Broken Access Control / CWE-284",
    "path traversal": "OWASP A01 - Broken Access Control (Path Traversal) / CWE-22",
    "csrf": "OWASP A01 - Broken Access Control (CSRF) / CWE-352",
    "crypto": "OWASP A02 - Cryptographic Failures / CWE-327",
    "md5": "OWASP A02 - Cryptographic Failures (Weak Hashing) / CWE-328",
    "sha1": "OWASP A02 - Cryptographic Failures (Weak Hashing) / CWE-328",
    "hardcoded": "OWASP A02 & A07 - Hardcoded Credentials / CWE-798",
    "secret": "OWASP A02 & A07 - Hardcoded Secrets / CWE-798",
    "sql injection": "OWASP A03 - Injection (SQL Injection) / CWE-89",
    "xss": "OWASP A03 - Injection (Cross-Site Scripting) / CWE-79",
    "command injection": "OWASP A03 - Injection (OS Command Injection) / CWE-78",
    "eval": "OWASP A03 - Injection (Code Injection) / CWE-95",
    "misconfiguration": "OWASP A05 - Security Misconfiguration / CWE-16",
    "debug": "OWASP A05 - Security Misconfiguration (Debug Enabled) / CWE-489",
    "authentication": "OWASP A07 - Identification and Authentication Failures / CWE-287",
    "deserializ": "OWASP A08 - Software and Data Integrity Failures / CWE-502",
    "pickle": "OWASP A08 - Software and Data Integrity Failures / CWE-502",
    "exception": "OWASP A09 - Security Logging & Error Handling Failures / CWE-390",
    "ssrf": "OWASP A10 - Server-Side Request Forgery (SSRF) / CWE-918",
}


def _normalize_severity(raw_sev: str, default: str = "Medium") -> str:
    s = str(raw_sev).strip().capitalize()
    if s == "Info":
        return "Informational"
    return s if s in VALID_SEVERITIES else default


def _match_owasp_rule(vuln_name: str, existing_ref: str) -> str:
    if existing_ref and any(
        tag in existing_ref.upper()
        for tag in ["A0", "A10", "CWE-", "CERT", "BANDIT", "SPOTBUGS"]
    ):
        return existing_ref
    lower_search = f"{vuln_name} {existing_ref}".lower()
    for keyword, owasp_std in OWASP_TOP_10_MAP.items():
        if keyword in lower_search:
            return owasp_std
    return existing_ref or "OWASP Secure Coding & CWE Standard"


def _default_secure_fix_snippet(vuln_name: str, language: str, original_snippet: str) -> str:
    v_lower = vuln_name.lower()
    if language == "python":
        if "sql" in v_lower:
            return (
                '# Use parameterized queries (DB-API "?" placeholder)\n'
                'cursor.execute("SELECT * FROM users WHERE username = ?", (username,))'
            )
        if "hardcoded" in v_lower or "secret" in v_lower or "password" in v_lower:
            return (
                "import os\n"
                '# Load sensitive credentials from environment variables or secret manager\n'
                'SECRET_KEY = os.environ.get("APP_SECRET_KEY")'
            )
        if "command" in v_lower or "subprocess" in v_lower:
            return (
                "import subprocess\n"
                "# Pass arguments as a list with shell=False\n"
                'subprocess.run(["ping", "-c", "1", host_input], shell=False, check=True)'
            )
        if "eval" in v_lower or "code injection" in v_lower:
            return (
                "import ast\n"
                "# Safely evaluate literal structures without executing arbitrary code\n"
                "safe_value = ast.literal_eval(user_expression)"
            )
        if "xss" in v_lower or "scripting" in v_lower:
            return (
                "import html\n"
                "safe_output = html.escape(user_input)"
            )
        if "exception" in v_lower or "error" in v_lower:
            return (
                "import logging\n"
                "try:\n"
                "    conn.commit()\n"
                "except sqlite3.Error as exc:\n"
                '    logging.error("Database commit failed: %s", exc)'
            )
    else:
        if "sql" in v_lower:
            return (
                "String sql = \"SELECT * FROM accounts WHERE username = ?\";\n"
                "try (PreparedStatement pstmt = conn.prepareStatement(sql)) {\n"
                "    pstmt.setString(1, userInput);\n"
                "    ResultSet rs = pstmt.executeQuery();\n"
                "}"
            )
        if "hardcoded" in v_lower or "secret" in v_lower or "password" in v_lower:
            return 'String dbPassword = System.getenv("DB_PASSWORD");'
        if "crypto" in v_lower or "md5" in v_lower or "sha" in v_lower:
            return 'MessageDigest md = MessageDigest.getInstance("SHA-256");'
        if "resource" in v_lower or "connection" in v_lower:
            return (
                "try (Connection conn = DriverManager.getConnection(url, user, System.getenv(\"DB_PASS\"));\n"
                "     PreparedStatement stmt = conn.prepareStatement(sql)) {\n"
                "    // Execute query safely with automatic resource closure\n"
                "}"
            )
    return original_snippet or "// Refactor according to OWASP and Clean Code guidelines"


def static_analysis_and_rag_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    code = state["code"]
    lang = state["language"].lower()

    numbered = "\n".join(
        f"{i:4d} | {line}" for i, line in enumerate(code.splitlines(), start=1)
    )

    metrics = compute_complexity_and_quality_metrics(code, lang)
    static_flags = run_static_pattern_scanners(code, lang)

    qual_cats = ["clean_code", "python"] if lang == "python" else ["clean_code", "java"]
    sec_cats = (
        ["owasp", "cwe", "python"]
        if lang == "python"
        else ["owasp", "cwe", "cert", "java"]
    )

    detected_alert_names = " ".join(
        {f.get("vulnerability_name", "") for f in static_flags}
    )

    try:
        qual_docs = search_knowledge_base(
            query=f"{lang} clean code smells complexity PMD Pylint {detected_alert_names}:\n{code[:500]}",
            k=3,
            allowed_categories=qual_cats,
        )
        sec_docs = search_knowledge_base(
            query=f"{lang} OWASP Top 10 CWE Bandit SpotBugs CERT security {detected_alert_names}:\n{code[:500]}",
            k=4,
            allowed_categories=sec_cats,
        )
    except Exception:
        qual_docs, sec_docs = [], []

    return {
        "numbered_code": numbered,
        "complexity_metrics": metrics["complexity_metrics"],
        "quality_assessment": metrics["quality_assessment"],
        "static_tool_flags": static_flags,
        "quality_guidelines": [
            f"[{d.metadata.get('source', 'KB')}]\n{d.page_content}" for d in qual_docs
        ],
        "security_guidelines": [
            f"[{d.metadata.get('source', 'KB')}]\n{d.page_content}" for d in sec_docs
        ],
    }


def code_analysis_agent_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    lang = state["language"].lower()
    try:
        llm = get_llm(temperature=0.1)
        chain = CODE_ANALYSIS_AGENT_PROMPT | llm

        static_summary = json.dumps(
            {
                "complexity_metrics": state.get("complexity_metrics", {}),
                "quality_assessment": state.get("quality_assessment", {}),
                "static_flags": [
                    f
                    for f in state.get("static_tool_flags", [])
                    if "Security" not in f.get("type", "")
                ],
            },
            indent=2,
        )

        res = chain.invoke({
            "filename": state["filename"],
            "language": state["language"],
            "numbered_code": state["numbered_code"],
            "static_context": static_summary,
            "quality_guidelines": "\n\n".join(state.get("quality_guidelines", [])),
        })

        parsed = parse_json_array(res.content)
        for idx, item in enumerate(parsed, start=1):
            v_name = str(
                item.get("vulnerability_name") or item.get("issue_type") or "Code Smell"
            )
            orig_snip = str(item.get("code_snippet", ""))
            sug = str(item.get("secure_code_suggestion", "")) or _default_secure_fix_snippet(
                v_name, lang, orig_snip
            )
            findings.append({
                "id": str(item.get("id", f"QUAL-{idx:02d}")),
                "agent_source": "Code Analysis Agent",
                "sub_category": str(item.get("sub_category", "Code Smell")),
                "vulnerability_name": v_name,
                "issue_type": v_name,
                "title": str(item.get("title", v_name)),
                "severity": _normalize_severity(item.get("severity", "Medium"), "Medium"),
                "tool_or_standard": str(
                    item.get("tool_or_standard", "Pylint / PMD / SonarQube")
                ),
                "owasp_category": "Clean Code & Maintainability Standard",
                "line_reference": str(item.get("line_reference", "N/A")),
                "code_snippet": orig_snip,
                "description": str(item.get("description", "")),
                "recommendation": str(
                    item.get("recommendation", "Refactor to improve maintainability.")
                ),
                "secure_code_suggestion": sug,
            })
    except Exception:
        pass

    if not findings:
        qual_flags = [
            f
            for f in state.get("static_tool_flags", [])
            if "Security" not in f.get("type", "")
        ]
        for idx, qf in enumerate(qual_flags, start=1):
            v_name = qf.get("vulnerability_name", "Code Smell")
            orig_snip = qf.get("snippet", "")
            findings.append({
                "id": f"QUAL-{idx:02d}",
                "agent_source": "Code Analysis Agent",
                "sub_category": qf.get("type", "Code Smell"),
                "vulnerability_name": v_name,
                "issue_type": v_name,
                "title": v_name,
                "severity": _normalize_severity(qf.get("severity", "Medium"), "Medium"),
                "tool_or_standard": qf.get("tool", "Pylint / PMD"),
                "owasp_category": "Clean Code Standard",
                "line_reference": qf.get("line", "N/A"),
                "code_snippet": orig_snip,
                "description": qf.get("message", ""),
                "recommendation": qf.get(
                    "recommendation", "Refactor code according to Clean Code principles."
                ),
                "secure_code_suggestion": _default_secure_fix_snippet(v_name, lang, orig_snip),
            })

    return {"quality_findings": findings}


def security_vulnerability_agent_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    lang = state["language"].lower()
    sec_flags = [
        f
        for f in state.get("static_tool_flags", [])
        if "Security" in f.get("type", "") or "Resource" in f.get("type", "")
    ]

    try:
        llm = get_llm(temperature=0.1)
        chain = SECURITY_VULNERABILITY_AGENT_PROMPT | llm

        res = chain.invoke({
            "filename": state["filename"],
            "language": state["language"],
            "numbered_code": state["numbered_code"],
            "static_context": json.dumps(sec_flags, indent=2),
            "security_guidelines": "\n\n".join(state.get("security_guidelines", [])),
        })

        parsed = parse_json_array(res.content)
        for idx, item in enumerate(parsed, start=1):
            v_name = str(
                item.get("vulnerability_name")
                or item.get("issue_type")
                or "OWASP Vulnerability"
            )
            tool_std = str(
                item.get("tool_or_standard", "Bandit / Semgrep / SpotBugs / OWASP")
            )
            owasp_cat = _match_owasp_rule(v_name, str(item.get("owasp_category", "")))
            orig_snip = str(item.get("code_snippet", ""))
            sug = str(item.get("secure_code_suggestion", "")) or _default_secure_fix_snippet(
                v_name, lang, orig_snip
            )

            findings.append({
                "id": str(item.get("id", f"SEC-{idx:02d}")),
                "agent_source": "Security Vulnerability Agent",
                "sub_category": str(
                    item.get("sub_category", "OWASP Security Vulnerability")
                ),
                "vulnerability_name": v_name,
                "issue_type": v_name,
                "title": str(item.get("title", v_name)),
                "severity": _normalize_severity(item.get("severity", "High"), "High"),
                "tool_or_standard": tool_std,
                "owasp_category": owasp_cat,
                "line_reference": str(item.get("line_reference", "N/A")),
                "code_snippet": orig_snip,
                "description": str(item.get("description", "")),
                "recommendation": str(
                    item.get("recommendation", "Follow OWASP remediation guidelines.")
                ),
                "secure_code_suggestion": sug,
            })
    except Exception:
        pass

    if not findings and sec_flags:
        for idx, sf in enumerate(sec_flags, start=1):
            v_name = sf.get("vulnerability_name", "Security Vulnerability")
            orig_snip = sf.get("snippet", "")
            findings.append({
                "id": f"SEC-{idx:02d}",
                "agent_source": "Security Vulnerability Agent",
                "sub_category": "OWASP Security Vulnerability",
                "vulnerability_name": v_name,
                "issue_type": v_name,
                "title": v_name,
                "severity": _normalize_severity(sf.get("severity", "High"), "High"),
                "tool_or_standard": sf.get("tool", "SAST Scanner"),
                "owasp_category": _match_owasp_rule(v_name, ""),
                "line_reference": sf.get("line", "N/A"),
                "code_snippet": orig_snip,
                "description": sf.get("message", ""),
                "recommendation": sf.get(
                    "recommendation", "Apply OWASP secure coding practices."
                ),
                "secure_code_suggestion": _default_secure_fix_snippet(v_name, lang, orig_snip),
            })

    return {"security_findings": findings}


def owasp_rule_matching_and_scoring_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    qual = state.get("quality_findings", [])
    sec = state.get("security_findings", [])

    for s_item in sec:
        s_item["owasp_category"] = _match_owasp_rule(
            s_item.get("vulnerability_name", ""),
            s_item.get("owasp_category", ""),
        )

    unified = sorted(
        sec + qual,
        key=lambda x: SEVERITY_ORDER.get(x.get("severity", "Informational"), 99),
    )

    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0}
    for f in unified:
        sev = f.get("severity", "Informational")
        if sev in counts:
            counts[sev] += 1

    qa = dict(state.get("quality_assessment", {}))
    debt_mins = (
        counts["Critical"] * 30
        + counts["High"] * 20
        + counts["Medium"] * 10
        + counts["Low"] * 5
        + counts["Informational"] * 2
    )
    if debt_mins > 0:
        qa["technical_debt_minutes"] = debt_mins

    # Compute Overall Code Health Score (0-100) combining maintainability & security penalties
    maint = float(qa.get("maintainability_score", 85.0))
    sec_penalty = (
        counts["Critical"] * 18.0
        + counts["High"] * 10.0
        + counts["Medium"] * 4.0
        + counts["Low"] * 1.5
    )
    health_score = round(max(5.0, min(100.0, (maint * 0.55) + max(0.0, 45.0 - sec_penalty))), 1)
    qa["code_health_score"] = health_score

    return {
        "security_findings": sec,
        "unified_findings": unified,
        "severity_breakdown": counts,
        "quality_assessment": qa,
    }


def remediation_agent_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """
    AI Remediation Agent:
    Generates root cause analysis, 4-category classification, best-practice explanation,
    and corrected code examples for every flagged finding.
    """
    unified = state.get("unified_findings", [])
    if not unified:
        return {"remediation_plan": []}

    lang = state["language"].lower()
    remediation_list: List[Dict[str, Any]] = []

    try:
        llm = get_llm(temperature=0.1)
        chain = REMEDIATION_AGENT_PROMPT | llm
        all_guidelines = state.get("security_guidelines", []) + state.get(
            "quality_guidelines", []
        )

        res = chain.invoke({
            "language": state["language"],
            "code": state["code"],
            "findings_json": json.dumps(unified, indent=2),
            "rag_guidelines": "\n\n".join(all_guidelines[:5]),
        })
        parsed = parse_json_array(res.content)
        for item in parsed:
            cat = str(item.get("recommendation_category", "Security Recommendation"))
            if cat not in VALID_REC_CATEGORIES:
                cat = (
                    "Security Recommendation"
                    if str(item.get("finding_id", "")).startswith("SEC")
                    else "Code Quality Recommendation"
                )
            remediation_list.append({
                "finding_id": str(item.get("finding_id", "ISSUE-01")),
                "issue_title": str(item.get("issue_title", "Flagged Issue")),
                "severity": _normalize_severity(item.get("severity", "High"), "High"),
                "line_reference": str(item.get("line_reference", "N/A")),
                "recommendation_category": cat,
                "root_cause": str(
                    item.get(
                        "root_cause",
                        "Missing input validation or adherence to secure design patterns.",
                    )
                ),
                "why_it_occurs": str(item.get("why_it_occurs", "")),
                "best_practice_guideline": str(
                    item.get("best_practice_guideline", "OWASP Top 10 / Clean Code")
                ),
                "fix_steps": str(item.get("fix_steps", "")),
                "original_code": str(item.get("original_code", "")),
                "corrected_code": str(item.get("corrected_code", "")),
            })
    except Exception:
        pass

    # Ensure every single finding has a complete remediation entry (instant fallback/completion)
    covered_ids = {r["finding_id"] for r in remediation_list}
    for f in unified:
        fid = f.get("id", "ISSUE")
        if fid not in covered_ids:
            is_sec = f.get("agent_source") == "Security Vulnerability Agent"
            sub_cat = f.get("sub_category", "").lower()
            if is_sec:
                rec_cat = "Security Recommendation"
            elif "complexity" in sub_cat:
                rec_cat = "Performance Recommendation"
            elif "anti-pattern" in sub_cat:
                rec_cat = "Maintainability Recommendation"
            else:
                rec_cat = "Code Quality Recommendation"

            v_name = f.get("vulnerability_name", "Issue")
            orig_code = f.get("code_snippet", "")
            corr_code = f.get("secure_code_suggestion") or _default_secure_fix_snippet(
                v_name, lang, orig_code
            )

            remediation_list.append({
                "finding_id": fid,
                "issue_title": f.get("title", v_name),
                "severity": f.get("severity", "Medium"),
                "line_reference": f.get("line_reference", "N/A"),
                "recommendation_category": rec_cat,
                "root_cause": (
                    f"Direct use of unvalidated/unsafe pattern ({v_name}) at {f.get('line_reference', 'code block')} "
                    f"violating {f.get('owasp_category') or f.get('tool_or_standard', 'coding standards')}."
                ),
                "why_it_occurs": f.get("description", ""),
                "best_practice_guideline": f.get("owasp_category")
                or f.get("tool_or_standard", "OWASP & SEI CERT Standard"),
                "fix_steps": f.get(
                    "recommendation", "Apply the corrected code pattern shown below."
                ),
                "original_code": orig_code,
                "corrected_code": corr_code,
            })

    return {"remediation_plan": remediation_list}


def pr_summary_agent_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """
    PR Summary Agent & AI Report Generator:
    Compiles all findings, metrics, and remediations into a Pull Request style summary.
    """
    unified = state.get("unified_findings", [])
    sev = state.get("severity_breakdown", {})
    qa = state.get("quality_assessment", {})
    rem = state.get("remediation_plan", [])
    health_score = qa.get("code_health_score", 80.0)
    filename = state.get("filename", "snippet")
    language = state.get("language", "python").upper()

    verdict = (
        "❌ **CHANGES REQUESTED (Blocking Security/Quality Risks Detected)**"
        if (sev.get("Critical", 0) > 0 or sev.get("High", 0) > 0)
        else "⚠️ **APPROVED WITH MINOR RECOMMENDATIONS**"
        if len(unified) > 0
        else "✅ **APPROVED (Clean & Secure Code)**"
    )

    sec_findings = state.get("security_findings", [])
    qual_findings = state.get("quality_findings", [])

    # Build a deterministic, instantaneous, executive-grade PR summary
    # (and optionally enrich via LLM if needed, avoiding slow double timeouts)
    lines = [
        f"## 🔍 Pull Request Review Summary — `{filename}` ({language})",
        f"**Review Verdict:** {verdict}  ",
        f"**Overall Code Health Score:** `{health_score}/100` | **Maintainability:** `{qa.get('maintainability_score', 0)}/100` | **Estimated Tech Debt:** `{qa.get('technical_debt_minutes', 0)} mins`",
        "",
        "### 1. Severity Breakdown",
        f"- 🔴 **Critical:** {sev.get('Critical', 0)} | 🟠 **High:** {sev.get('High', 0)} | 🟡 **Medium:** {sev.get('Medium', 0)} | 🔵 **Low:** {sev.get('Low', 0)} | ⚪ **Informational:** {sev.get('Informational', 0)}",
        "",
        "### 2. Security Vulnerability Summary (OWASP & SAST)",
    ]

    if sec_findings:
        for s in sec_findings:
            lines.append(
                f"- **[{s['severity']}] `{s['id']}` {s['vulnerability_name']}** ({s['line_reference']}): "
                f"{s['description']} *(Rule: `{s.get('owasp_category', '')}`)*"
            )
    else:
        lines.append("- No OWASP security vulnerabilities detected.")

    lines.append("")
    lines.append("### 3. Code Quality & Smell Summary")
    if qual_findings:
        for q in qual_findings:
            lines.append(
                f"- **[{q['severity']}] `{q['id']}` {q['vulnerability_name']}** ({q['line_reference']}): "
                f"{q['description']} *(Tool: `{q.get('tool_or_standard', '')}`)*"
            )
    else:
        lines.append("- No code smells or design anti-patterns detected.")

    lines.append("")
    lines.append("### 4. Prioritized Remediation Roadmap")
    if rem:
        for idx, r in enumerate(rem, start=1):
            lines.append(
                f"{idx}. **`{r['finding_id']}` ({r['recommendation_category']} - {r['severity']})** at `{r['line_reference']}`: {r['fix_steps']}"
            )
    else:
        lines.append("1. Code meets security and quality standards. Ready to merge.")

    return {"pr_summary_markdown": "\n".join(lines)}


def classify_question_intent(question: str) -> str:
    q = question.lower()
    if any(w in q for w in ["sql", "xss", "csrf", "vulnerability", "owasp", "attack", "exploit", "secret"]):
        return "Vulnerability Explanation & OWASP Guidance"
    if any(w in q for w in ["fix", "remediate", "solve", "patch", "better code", "refactor", "secure"]):
        return "Remediation & Secure Code Generation"
    if any(w in q for w in ["duplicate", "smell", "complexity", "spaghetti", "god object", "clean code"]):
        return "Code Smell & Maintainability Guidance"
    if any(w in q for w in ["error", "warning", "syntax", "exception", "bandit", "pmd", "spotbugs"]):
        return "Static Warning & Error Diagnosis"
    return "General Secure Coding & Best Practice Inquiry"


def run_conversational_assistant(
    question: str,
    language: str = "python",
    code_context: str = "",
    findings_context: str = "",
    chat_history: List[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    6-Step RAG Conversational Code Assistant:
    1. Receive Question -> 2. Classify Intent -> 3. Retrieve RAG Docs ->
    4. Generate Grounded Response -> 5. Return Answer + Sources -> 6. Preserve Multi-Turn Context
    """
    intent = classify_question_intent(question)
    docs = search_knowledge_base(
        query=f"{language} {intent}: {question}",
        k=4,
    )
    kb_context = "\n\n".join(
        [f"Source [{d.metadata.get('source', 'Knowledge Base')}]:\n{d.page_content}" for d in docs]
    )
    sources = sorted(list({d.metadata.get("source", "OWASP Knowledge Base") for d in docs}))

    history_str = ""
    if chat_history:
        recent = chat_history[-6:]
        history_str = "\n".join(
            [f"{msg.get('role', 'user').upper()}: {msg.get('content', '')}" for msg in recent]
        )

    try:
        llm = get_llm(temperature=0.2)
        chain = CONVERSATIONAL_ASSISTANT_PROMPT | llm
        res = chain.invoke({
            "language": language,
            "kb_context": kb_context or "Standard OWASP Top 10 and Clean Code guidelines apply.",
            "code_context": code_context[:2500] if code_context else "No code submitted yet.",
            "findings_context": findings_context[:2500] if findings_context else "No findings flagged yet.",
            "history_context": history_str or "Start of conversation.",
            "intent": intent,
            "question": question,
        })
        answer_text = res.content
    except Exception:
        # Reliable RAG fallback if LLM quota is reached during demo
        answer_text = (
            f"### Grounded Guidance ({intent})\n\n"
            f"Based on the indexed **Secure Coding Knowledge Base**, here are the relevant standards for your query:\n\n"
            f"{kb_context if kb_context else 'Always validate inputs, use parameterized queries, avoid hardcoded credentials, and keep cyclomatic complexity low.'}"
        )

    return {
        "intent": intent,
        "answer": answer_text,
        "sources": sources,
    }
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
)
from parsers.output_parser import parse_json_array

VALID_SEVERITIES = {"Critical", "High", "Medium", "Low", "Informational"}
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}

# Comprehensive fallback mapping across all OWASP Top 10 (A01-A10) categories
OWASP_TOP_10_MAP = {
    "access control": "OWASP A01 - Broken Access Control / CWE-284",
    "authorization": "OWASP A01 - Broken Access Control / CWE-862",
    "idor": "OWASP A01 - Broken Access Control (IDOR) / CWE-639",
    "path traversal": "OWASP A01 - Broken Access Control (Path Traversal) / CWE-22",
    "csrf": "OWASP A01 - Broken Access Control (CSRF) / CWE-352",
    "cross-site request forgery": "OWASP A01 - Broken Access Control (CSRF) / CWE-352",
    "permission": "OWASP A01 - Broken Access Control (Least Privilege) / CWE-732",
    "crypto": "OWASP A02 - Cryptographic Failures / CWE-327",
    "md5": "OWASP A02 - Cryptographic Failures (Weak Hashing) / CWE-328",
    "sha1": "OWASP A02 - Cryptographic Failures (Weak Hashing) / CWE-328",
    "sha-1": "OWASP A02 - Cryptographic Failures (Weak Hashing) / CWE-328",
    "des": "OWASP A02 - Cryptographic Failures (Broken Cipher) / CWE-327",
    "random": "OWASP A02 - Cryptographic Failures (Insecure PRNG) / CWE-338",
    "hardcoded": "OWASP A02 & A07 - Hardcoded Credentials & Cryptographic Failures / CWE-798",
    "secret": "OWASP A02 & A07 - Hardcoded Secrets / CWE-798",
    "api key": "OWASP A02 & A07 - Hardcoded API Key / CWE-798",
    "sql injection": "OWASP A03 - Injection (SQL Injection) / CWE-89",
    "sqli": "OWASP A03 - Injection (SQL Injection) / CWE-89",
    "xss": "OWASP A03 - Injection (Cross-Site Scripting) / CWE-79",
    "cross-site scripting": "OWASP A03 - Injection (Cross-Site Scripting) / CWE-79",
    "command injection": "OWASP A03 - Injection (OS Command Injection) / CWE-78",
    "code injection": "OWASP A03 - Injection (Code Injection) / CWE-94",
    "eval": "OWASP A03 - Injection (Unsafe Dynamic Evaluation) / CWE-95",
    "insecure design": "OWASP A04 - Insecure Design / CWE-209",
    "misconfiguration": "OWASP A05 - Security Misconfiguration / CWE-16",
    "debug": "OWASP A05 - Security Misconfiguration (Debug Enabled) / CWE-489",
    "xxe": "OWASP A05 - Security Misconfiguration (XML External Entity) / CWE-611",
    "xml": "OWASP A05 - Security Misconfiguration (XXE) / CWE-611",
    "tls": "OWASP A05 - Security Misconfiguration (Improper Certificate Validation) / CWE-295",
    "ssl": "OWASP A05 - Security Misconfiguration (Improper Certificate Validation) / CWE-295",
    "outdated": "OWASP A06 - Vulnerable and Outdated Components / CWE-1104",
    "deprecated": "OWASP A06 - Vulnerable and Outdated Components / CWE-477",
    "authentication": "OWASP A07 - Identification and Authentication Failures / CWE-287",
    "password": "OWASP A07 - Identification and Authentication Failures / CWE-798",
    "jwt": "OWASP A07 - Identification and Authentication Failures (JWT) / CWE-347",
    "session": "OWASP A07 - Identification and Authentication Failures (Session) / CWE-384",
    "deserializ": "OWASP A08 - Software and Data Integrity Failures / CWE-502",
    "pickle": "OWASP A08 - Software and Data Integrity Failures (Pickle) / CWE-502",
    "yaml": "OWASP A08 - Software and Data Integrity Failures (Unsafe YAML) / CWE-502",
    "logging": "OWASP A09 - Security Logging and Monitoring Failures / CWE-778",
    "exception": "OWASP A09 - Security Logging & Error Handling Failures / CWE-390",
    "ssrf": "OWASP A10 - Server-Side Request Forgery (SSRF) / CWE-918",
}


def _normalize_severity(raw_sev: str, default: str = "Medium") -> str:
    s = str(raw_sev).strip().capitalize()
    if s == "Info":
        return "Informational"
    return s if s in VALID_SEVERITIES else default


def _match_owasp_rule(vuln_name: str, existing_ref: str) -> str:
    """
    Preserves specific OWASP/CWE/CERT/Bandit categories identified by the LLM from
    the RAG Knowledge Base, or enriches via the full A01-A10 map if missing.
    """
    if existing_ref and any(
        tag in existing_ref.upper() for tag in ["A0", "A10", "CWE-", "CERT", "BANDIT", "SPOTBUGS"]
    ):
        return existing_ref

    lower_search = f"{vuln_name} {existing_ref}".lower()
    for keyword, owasp_std in OWASP_TOP_10_MAP.items():
        if keyword in lower_search:
            return owasp_std
    return existing_ref or "OWASP Secure Coding & CWE Standard"


def static_analysis_and_rag_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """
    Stage 3 & 4 Preparation:
    Runs SAST (Bandit, Semgrep, Pylint, SpotBugs, PMD, Checkstyle) and dynamically
    queries the RAG Knowledge Base (ChromaDB + FAISS) using detected patterns + code.
    """
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

    # Build dynamic RAG query from any detected static alert names + code context
    detected_alert_names = " ".join(
        {f.get("vulnerability_name", "") for f in static_flags}
    )

    qual_docs = search_knowledge_base(
        query=f"{lang} clean code smells complexity anti-patterns PMD Pylint Checkstyle {detected_alert_names}:\n{code[:700]}",
        k=4,
        allowed_categories=qual_cats,
    )
    sec_docs = search_knowledge_base(
        query=f"{lang} OWASP Top 10 CWE Bandit SpotBugs CERT security vulnerabilities {detected_alert_names}:\n{code[:700]}",
        k=5,
        allowed_categories=sec_cats,
    )

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
    """Stage 3 (Parallel Branch A): Code Analysis Agent."""
    llm = get_llm(temperature=0.1)
    chain = CODE_ANALYSIS_AGENT_PROMPT | llm

    static_summary = json.dumps(
        {
            "complexity_metrics": state.get("complexity_metrics", {}),
            "quality_assessment": state.get("quality_assessment", {}),
            "static_flags": state.get("static_tool_flags", []),
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
    findings: List[Dict[str, Any]] = []
    for idx, item in enumerate(parsed, start=1):
        v_name = str(item.get("vulnerability_name") or item.get("issue_type") or "Code Smell")
        findings.append({
            "id": str(item.get("id", f"QUAL-{idx:02d}")),
            "agent_source": "Code Analysis Agent",
            "sub_category": str(item.get("sub_category", "Code Smell")),
            "vulnerability_name": v_name,
            "issue_type": v_name,
            "title": str(item.get("title", v_name)),
            "severity": _normalize_severity(item.get("severity", "Medium"), "Medium"),
            "tool_or_standard": str(item.get("tool_or_standard", "Pylint / PMD / SonarQube")),
            "owasp_category": "Clean Code & Maintainability Standard",
            "line_reference": str(item.get("line_reference", "N/A")),
            "code_snippet": str(item.get("code_snippet", "")),
            "description": str(item.get("description", "")),
            "recommendation": str(item.get("recommendation", "Refactor to improve maintainability.")),
            "secure_code_suggestion": str(item.get("secure_code_suggestion", "")),
        })

    return {"quality_findings": findings}


def security_vulnerability_agent_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """Stage 4 & 5 (Parallel Branch B): Security Vulnerability Agent (SAST + AI Vulnerability Detection)."""
    llm = get_llm(temperature=0.1)
    chain = SECURITY_VULNERABILITY_AGENT_PROMPT | llm

    sec_flags = [
        f
        for f in state.get("static_tool_flags", [])
        if "Security" in f.get("type", "") or "Resource" in f.get("type", "") or "Error" in f.get("type", "")
    ]

    res = chain.invoke({
        "filename": state["filename"],
        "language": state["language"],
        "numbered_code": state["numbered_code"],
        "static_context": json.dumps(sec_flags, indent=2),
        "security_guidelines": "\n\n".join(state.get("security_guidelines", [])),
    })

    parsed = parse_json_array(res.content)
    findings: List[Dict[str, Any]] = []
    for idx, item in enumerate(parsed, start=1):
        v_name = str(item.get("vulnerability_name") or item.get("issue_type") or "OWASP Vulnerability")
        tool_std = str(item.get("tool_or_standard", "Bandit / Semgrep / SpotBugs / OWASP"))
        owasp_cat = _match_owasp_rule(v_name, str(item.get("owasp_category", "")))

        findings.append({
            "id": str(item.get("id", f"SEC-{idx:02d}")),
            "agent_source": "Security Vulnerability Agent",
            "sub_category": str(item.get("sub_category", "OWASP Security Vulnerability")),
            "vulnerability_name": v_name,
            "issue_type": v_name,
            "title": str(item.get("title", v_name)),
            "severity": _normalize_severity(item.get("severity", "High"), "High"),
            "tool_or_standard": tool_std,
            "owasp_category": owasp_cat,
            "line_reference": str(item.get("line_reference", "N/A")),
            "code_snippet": str(item.get("code_snippet", "")),
            "description": str(item.get("description", "")),
            "recommendation": str(item.get("recommendation", "Follow OWASP remediation guidelines.")),
            "secure_code_suggestion": str(item.get("secure_code_suggestion", "")),
        })

    return {"security_findings": findings}


def owasp_rule_matching_and_scoring_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """
    Stages 5, 6 & 7:
    - Matches all security findings against OWASP Top 10 (A01-A10) & CWE rules
    - Assigns and counts Severity Levels (Critical, High, Medium, Low, Informational)
    - Produces the Unified Findings Report combining Code Analysis & Security findings
    """
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

    return {
        "security_findings": sec,
        "unified_findings": unified,
        "severity_breakdown": counts,
        "quality_assessment": qa,
    }
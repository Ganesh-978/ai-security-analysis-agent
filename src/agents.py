# src/agents.py
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


def _normalize_severity(raw_sev: str, default: str = "Medium") -> str:
    s = str(raw_sev).strip().capitalize()
    if s == "Info":
        return "Informational"
    return s if s in VALID_SEVERITIES else default


def static_analysis_and_rag_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """
    Executes Layer 2 (Static Analysis, AST, Complexity & Anti-Pattern Scan)
    and Layer 4 (OWASP Knowledge Base Retrieval via ChromaDB + FAISS).
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

    qual_docs = search_knowledge_base(
        query=f"{lang} code smells complexity anti-patterns PMD Pylint:\n{code[:700]}",
        k=3,
        allowed_categories=qual_cats,
    )
    sec_docs = search_knowledge_base(
        query=f"{lang} OWASP CWE Bandit SpotBugs CERT secure coding guidelines:\n{code[:700]}",
        k=3,
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
        findings.append({
            "id": str(item.get("id", f"QUAL-{idx:02d}")),
            "agent_source": "Code Analysis Agent",
            "sub_category": str(item.get("sub_category", "Code Smell")),
            "issue_type": str(item.get("issue_type", "Code Quality Issue")),
            "title": str(item.get("title", "Code Quality Finding")),
            "severity": _normalize_severity(item.get("severity", "Medium"), "Medium"),
            "tool_or_standard": str(item.get("tool_or_standard", "Pylint / PMD / Clean Code")),
            "line_reference": str(item.get("line_reference", "N/A")),
            "code_snippet": str(item.get("code_snippet", "")),
            "description": str(item.get("description", "")),
            "recommendation": str(item.get("recommendation", "Refactor according to Clean Code standards.")),
        })

    return {"quality_findings": findings}


def security_vulnerability_agent_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    llm = get_llm(temperature=0.1)
    chain = SECURITY_VULNERABILITY_AGENT_PROMPT | llm

    sec_flags = [
        f for f in state.get("static_tool_flags", []) if "Security" in f.get("type", "")
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
        findings.append({
            "id": str(item.get("id", f"SEC-{idx:02d}")),
            "agent_source": "Security Vulnerability Agent",
            "sub_category": str(item.get("sub_category", "OWASP Security Vulnerability")),
            "issue_type": str(item.get("issue_type", "OWASP Vulnerability")),
            "title": str(item.get("title", "Security Vulnerability")),
            "severity": _normalize_severity(item.get("severity", "High"), "High"),
            "tool_or_standard": str(item.get("tool_or_standard", "Bandit / SpotBugs / OWASP")),
            "line_reference": str(item.get("line_reference", "N/A")),
            "code_snippet": str(item.get("code_snippet", "")),
            "description": str(item.get("description", "")),
            "recommendation": str(item.get("recommendation", "Apply OWASP secure coding guidelines.")),
        })

    return {"security_findings": findings}


def severity_scoring_engine_node(state: ReviewWorkflowState) -> Dict[str, Any]:
    """
    Severity Scoring Engine (Slides 10, 12, 19-21):
    Merges parallel agent outputs, classifies across the 5-tier Severity Pyramid
    (Critical, High, Medium, Low, Informational), and adjusts technical debt.
    """
    qual = state.get("quality_findings", [])
    sec = state.get("security_findings", [])

    unified = sorted(
        sec + qual,
        key=lambda x: SEVERITY_ORDER.get(x.get("severity", "Informational"), 99),
    )

    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0}
    for f in unified:
        sev = f.get("severity", "Informational")
        if sev in counts:
            counts[sev] += 1

    # Refine technical debt estimate based on actual flagged severities
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
        "unified_findings": unified,
        "severity_breakdown": counts,
        "quality_assessment": qa,
    }
# src/state.py
from typing import TypedDict, List, Dict, Any


class ReviewWorkflowState(TypedDict):
    filename: str
    language: str
    code: str
    numbered_code: str
    complexity_metrics: Dict[str, Any]
    quality_assessment: Dict[str, Any]
    static_tool_flags: List[Dict[str, str]]
    quality_guidelines: List[str]
    security_guidelines: List[str]
    quality_findings: List[Dict[str, Any]]
    security_findings: List[Dict[str, Any]]
    unified_findings: List[Dict[str, Any]]
    severity_breakdown: Dict[str, int]
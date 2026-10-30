from langgraph.graph import StateGraph, START, END
from src.state import ReviewWorkflowState
from src.agents import (
    static_analysis_and_rag_node,
    code_analysis_agent_node,
    security_vulnerability_agent_node,
    owasp_rule_matching_and_scoring_node,
)


def build_review_graph():
    workflow = StateGraph(ReviewWorkflowState)

    workflow.add_node("static_analysis_and_rag", static_analysis_and_rag_node)
    workflow.add_node("code_analysis_agent", code_analysis_agent_node)
    workflow.add_node("security_vulnerability_agent", security_vulnerability_agent_node)
    workflow.add_node(
        "owasp_rule_matching_and_scoring", owasp_rule_matching_and_scoring_node
    )

    workflow.add_edge(START, "static_analysis_and_rag")
    workflow.add_edge("static_analysis_and_rag", "code_analysis_agent")
    workflow.add_edge("static_analysis_and_rag", "security_vulnerability_agent")
    workflow.add_edge("code_analysis_agent", "owasp_rule_matching_and_scoring")
    workflow.add_edge("security_vulnerability_agent", "owasp_rule_matching_and_scoring")
    workflow.add_edge("owasp_rule_matching_and_scoring", END)

    return workflow.compile()


review_graph = build_review_graph()


def run_review_pipeline(code: str, language: str, filename: str = "snippet") -> dict:
    initial_state: ReviewWorkflowState = {
        "filename": filename,
        "language": language,
        "code": code,
        "numbered_code": "",
        "complexity_metrics": {},
        "quality_assessment": {},
        "static_tool_flags": [],
        "quality_guidelines": [],
        "security_guidelines": [],
        "quality_findings": [],
        "security_findings": [],
        "unified_findings": [],
        "severity_breakdown": {
            "Critical": 0,
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Informational": 0,
        },
    }
    return review_graph.invoke(initial_state)
# src/workflow.py
from langgraph.graph import StateGraph, START, END
from src.state import ReviewWorkflowState
from src.agents import (
    static_analysis_and_rag_node,
    code_analysis_agent_node,
    security_vulnerability_agent_node,
    severity_scoring_engine_node,
)


def build_milestone2_graph():
    workflow = StateGraph(ReviewWorkflowState)

    workflow.add_node("static_analysis_and_rag", static_analysis_and_rag_node)
    workflow.add_node("code_analysis_agent", code_analysis_agent_node)
    workflow.add_node("security_vulnerability_agent", security_vulnerability_agent_node)
    workflow.add_node("severity_scoring_engine", severity_scoring_engine_node)

    workflow.add_edge(START, "static_analysis_and_rag")

    # Parallel Multi-Agent Execution
    workflow.add_edge("static_analysis_and_rag", "code_analysis_agent")
    workflow.add_edge("static_analysis_and_rag", "security_vulnerability_agent")

    # Fan-In to Severity Scoring Engine
    workflow.add_edge("code_analysis_agent", "severity_scoring_engine")
    workflow.add_edge("security_vulnerability_agent", "severity_scoring_engine")

    workflow.add_edge("severity_scoring_engine", END)

    return workflow.compile()


milestone2_graph = build_milestone2_graph()


def run_milestone2_pipeline(code: str, language: str, filename: str = "snippet") -> dict:
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
    return milestone2_graph.invoke(initial_state)
# models/schemas.py
from typing import Optional, Literal, List, Dict
from pydantic import BaseModel, Field

SeverityType = Literal["Critical", "High", "Medium", "Low", "Informational"]


class CodeSubmission(BaseModel):
    filename: Optional[str] = "snippet"
    code: str = Field(..., description="Submitted Python or Java source code")
    language: Literal["python", "java", "unknown"] = "unknown"


class SyntaxValidationResult(BaseModel):
    is_valid: bool
    detected_language: Literal["python", "java", "unknown"]
    error_message: Optional[str] = None
    line_number: Optional[int] = None
    offending_line: Optional[str] = None


class ComplexityMetrics(BaseModel):
    cyclomatic_complexity: int = Field(..., description="Decision paths & branching logic")
    cyclomatic_rank: str = Field(..., description="A (Low risk) to F (Very high risk)")
    cognitive_complexity: int = Field(..., description="Human understandability & nesting score")
    time_complexity: str = Field(..., description="Estimated Big-O execution time growth")
    space_complexity: str = Field(..., description="Estimated Big-O memory usage growth")


class QualityAssessmentMetrics(BaseModel):
    maintainability_score: float = Field(..., description="0-100 maintainability index")
    complexity_score: float = Field(..., description="0-100 complexity health score")
    duplication_percentage: float = Field(..., description="Estimated duplicate line %")
    documentation_score: float = Field(..., description="0-100 comment/docstring coverage %")
    technical_debt_minutes: int = Field(..., description="Estimated minutes to resolve issues")


class FindingItem(BaseModel):
    id: str
    agent_source: Literal["Code Analysis Agent", "Security Vulnerability Agent"]
    sub_category: str = Field(
        ...,
        description="e.g., Code Smell, Design Anti-Pattern, Complexity, Best Practice, OWASP Vulnerability",
    )
    issue_type: str = Field(
        ...,
        description="e.g., God Object, Spaghetti Code, SQL Injection, Hardcoded Credentials",
    )
    title: str
    severity: SeverityType
    tool_or_standard: str = Field(
        ...,
        description="e.g., Bandit B608 / OWASP A03 / PMD / Pylint / SpotBugs / Clean Code",
    )
    line_reference: str
    code_snippet: Optional[str] = ""
    description: str
    recommendation: str = Field(..., description="Actionable fix recommendation")


class SeverityBreakdown(BaseModel):
    Critical: int = 0
    High: int = 0
    Medium: int = 0
    Low: int = 0
    Informational: int = 0


class Milestone2AnalysisReport(BaseModel):
    filename: str
    language: str
    syntax_validation: SyntaxValidationResult
    complexity_metrics: Optional[ComplexityMetrics] = None
    quality_assessment: Optional[QualityAssessmentMetrics] = None
    static_tool_flags: List[Dict[str, str]] = []
    severity_breakdown: SeverityBreakdown = Field(default_factory=SeverityBreakdown)
    quality_findings: List[FindingItem] = []
    security_findings: List[FindingItem] = []
    unified_findings: List[FindingItem] = []
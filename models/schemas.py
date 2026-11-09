from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field

SeverityType = Literal["Critical", "High", "Medium", "Low", "Informational"]
RecommendationCategory = Literal[
    "Security Recommendation",
    "Code Quality Recommendation",
    "Performance Recommendation",
    "Maintainability Recommendation",
]


class CodeSubmission(BaseModel):
    filename: Optional[str] = "snippet"
    code: str = Field(..., description="Submitted Python or Java source code")
    language: Literal["python", "java", "unknown"] = "unknown"


class SyntaxValidationResult(BaseModel):
    is_valid: bool
    detected_language: Literal["python", "java", "unknown"]
    parser_used: str = Field(default="AST / Lexical Parser")
    ast_node_count: int = Field(default=0)
    error_message: Optional[str] = None
    line_number: Optional[int] = None
    offending_line: Optional[str] = None


class ComplexityMetrics(BaseModel):
    cyclomatic_complexity: int
    cyclomatic_rank: str
    cognitive_complexity: int
    time_complexity: str
    space_complexity: str


class QualityAssessmentMetrics(BaseModel):
    code_health_score: float = Field(default=100.0, description="Overall 0-100 Code Health Score")
    maintainability_score: float
    complexity_score: float
    duplication_percentage: float
    documentation_score: float
    technical_debt_minutes: int


class FindingItem(BaseModel):
    id: str
    agent_source: Literal["Code Analysis Agent", "Security Vulnerability Agent"]
    sub_category: str = "OWASP Security Vulnerability"
    vulnerability_name: str
    issue_type: str
    title: str
    severity: SeverityType
    line_reference: str
    code_snippet: Optional[str] = ""
    description: str
    recommendation: str
    secure_code_suggestion: Optional[str] = ""
    tool_or_standard: str = "OWASP Top 10"
    owasp_category: Optional[str] = ""


class RemediationPlanItem(BaseModel):
    finding_id: str
    issue_title: str
    severity: SeverityType
    line_reference: str
    recommendation_category: RecommendationCategory = "Security Recommendation"
    root_cause: str = Field(..., description="Underlying reason why the issue exists in the code")
    why_it_occurs: str = Field(..., description="Developer-friendly explanation of risk and impact")
    best_practice_guideline: str = Field(..., description="OWASP, CERT, or Clean Code standard reference")
    fix_steps: str = Field(..., description="Concrete actionable steps to resolve the issue")
    original_code: Optional[str] = ""
    corrected_code: str = Field(..., description="Refactored or patched code snippet")


class SeverityBreakdown(BaseModel):
    Critical: int = 0
    High: int = 0
    Medium: int = 0
    Low: int = 0
    Informational: int = 0


class CodeReviewReport(BaseModel):
    filename: str
    language: str
    syntax_validation: SyntaxValidationResult
    complexity_metrics: Optional[ComplexityMetrics] = None
    quality_assessment: Optional[QualityAssessmentMetrics] = None
    static_tool_flags: List[Dict[str, Any]] = []
    severity_breakdown: SeverityBreakdown = Field(default_factory=SeverityBreakdown)
    quality_findings: List[FindingItem] = []
    security_findings: List[FindingItem] = []
    unified_findings: List[FindingItem] = []
    remediation_plan: List[RemediationPlanItem] = []
    pr_summary_markdown: str = ""


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AssistantQueryRequest(BaseModel):
    question: str
    language: Optional[str] = "python"
    code_context: Optional[str] = ""
    findings_context: Optional[str] = ""
    chat_history: List[ChatMessage] = []


class AssistantQueryResponse(BaseModel):
    intent: str
    answer: str
    sources: List[str] = []
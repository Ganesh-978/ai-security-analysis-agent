from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field

SeverityType = Literal["Critical", "High", "Medium", "Low", "Informational"]


class CodeSubmission(BaseModel):
    filename: Optional[str] = "snippet"
    code: str = Field(..., description="Submitted Python or Java source code")
    language: Literal["python", "java", "unknown"] = "unknown"


class SyntaxValidationResult(BaseModel):
    is_valid: bool
    detected_language: Literal["python", "java", "unknown"]
    parser_used: str = Field(default="AST / Lexical Parser", description="AST or Tree-sitter parser")
    ast_node_count: int = Field(default=0, description="Number of syntax tree nodes parsed")
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
    maintainability_score: float
    complexity_score: float
    duplication_percentage: float
    documentation_score: float
    technical_debt_minutes: int


class FindingItem(BaseModel):
    id: str = Field(..., description="Unique finding ID, e.g., SEC-01 or QUAL-01")
    agent_source: Literal["Code Analysis Agent", "Security Vulnerability Agent"]
    sub_category: str = Field(
        default="OWASP Security Vulnerability",
        description="Code Smell, Design Anti-Pattern, Complexity, or OWASP Security Vulnerability",
    )
    # 1. Vulnerability Name / Issue Type (Slide 6)
    vulnerability_name: str = Field(
        ...,
        description="Standardized name, e.g., SQL Injection, Cross-Site Scripting (XSS), CSRF, Hardcoded Secret",
    )
    issue_type: str = Field(..., description="Alias for vulnerability_name / smell category")
    title: str = Field(..., description="Concise title of the issue")
    # 2. Severity Level (Slide 6)
    severity: SeverityType
    # 3. Affected Line Number (Slide 6)
    line_reference: str = Field(..., description="Exact affected line number(s)")
    code_snippet: Optional[str] = Field(default="", description="Flagged source code line(s)")
    # 4. Risk Description (Slide 6)
    description: str = Field(
        ...,
        description="Plain-language explanation of what the issue is, how it is exploited, and impact",
    )
    # 5. Recommendation (Slide 6)
    recommendation: str = Field(
        ...,
        description="Specific remediation guidance (e.g., parameterized queries, environment variables)",
    )
    # 6. Secure Coding Suggestion (Slide 6)
    secure_code_suggestion: Optional[str] = Field(
        default="",
        description="Best-practice secure/refactored code example demonstrating the fix",
    )
    tool_or_standard: str = Field(
        default="OWASP Top 10",
        description="Matched tool/rule (Bandit, Semgrep, Pylint, SpotBugs, PMD, Checkstyle, SonarQube, Snyk, OWASP)",
    )
    owasp_category: Optional[str] = Field(
        default="",
        description="Matched OWASP Top 10 / CWE rule from Stage 4 OWASP Rule Matching",
    )


class SeverityBreakdown(BaseModel):
    Critical: int = 0
    High: int = 0
    Medium: int = 0
    Low: int = 0
    Informational: int = 0


class AnalysisReport(BaseModel):
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
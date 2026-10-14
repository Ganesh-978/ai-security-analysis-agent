from typing import Optional, Literal, List
from pydantic import BaseModel, Field


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


class RetrievedGuideline(BaseModel):
    source: str
    category: str
    content: str
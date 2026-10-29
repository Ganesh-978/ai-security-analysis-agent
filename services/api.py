import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import (
    CodeSubmission,
    AnalysisReport,
    ComplexityMetrics,
    QualityAssessmentMetrics,
    SeverityBreakdown,
    FindingItem,
)
from parsers.code_validator import validate_submission
from src.workflow import run_pipeline
from services.database import init_db, save_review_to_db, get_recent_reviews

app = FastAPI(
    title="AI Code Review & Security Analysis Agent - 6-Layer API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/health")
def health():
    return {"status": "ok", "architecture": "6-Layer AI Security Agent"}


@app.get("/api/v1/history")
def fetch_review_history():
    return {"history": get_recent_reviews(limit=10)}


@app.post("/api/v1/analyze", response_model=AnalysisReport)
def analyze_code_endpoint(submission: CodeSubmission):
    validation = validate_submission(submission.code, filename=submission.filename)
    fname = submission.filename or (
        "snippet.py" if validation.detected_language == "python" else "Snippet.java"
    )

    if not validation.is_valid:
        return AnalysisReport(
            filename=fname,
            language=validation.detected_language,
            syntax_validation=validation,
        )

    try:
        res = run_pipeline(
            code=submission.code,
            language=validation.detected_language,
            filename=fname,
        )
        report = AnalysisReport(
            filename=fname,
            language=validation.detected_language,
            syntax_validation=validation,
            complexity_metrics=ComplexityMetrics(**res["complexity_metrics"]),
            quality_assessment=QualityAssessmentMetrics(**res["quality_assessment"]),
            static_tool_flags=res.get("static_tool_flags", []),
            severity_breakdown=SeverityBreakdown(**res["severity_breakdown"]),
            quality_findings=[FindingItem(**f) for f in res["quality_findings"]],
            security_findings=[FindingItem(**f) for f in res["security_findings"]],
            unified_findings=[FindingItem(**f) for f in res["unified_findings"]],
        )
        save_review_to_db(report.model_dump())
        return report
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
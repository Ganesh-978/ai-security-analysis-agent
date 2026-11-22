import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from parsers.code_validator import validate_submission
from rag.retriever import search_knowledge_base
from src.workflow import run_review_pipeline
from reports.report_generator import generate_pdf_report, generate_full_markdown_report


SAMPLES = [
    (
        "token_utility.py",
        "python",
        '''import hashlib\nAPI_KEY = "sk_live_123456789"\ndef hash_pw(pw):\n    return hashlib.md5(pw.encode()).hexdigest()\n''',
    ),
    (
        "order_service.py",
        "python",
        '''import sqlite3\nimport subprocess\ndef run_query(user, host):\n    conn = sqlite3.connect("db.sqlite")\n    c = conn.cursor()\n    c.execute(f"SELECT * FROM orders WHERE user = '{user}'")\n    subprocess.Popen("ping " + host, shell=True)\n''',
    ),
    (
        "AccountDao.java",
        "java",
        '''import java.sql.*;\npublic class AccountDao {\n    private static final String PASS = "Secret12345";\n    public void query(String input) {\n        try {\n            Connection c = DriverManager.getConnection("jdbc:mysql://localhost/db", "root", PASS);\n            Statement s = c.createStatement();\n            s.executeQuery("SELECT * FROM users WHERE name = '" + input + "'");\n        } catch (Exception e) {}\n    }\n}\n''',
    ),
]


def run_end_to_end_validation():
    print("=" * 75)
    print("RUNNING END-TO-END VALIDATION SUITE (3 SAMPLES OF VARYING COMPLEXITY)")
    print("=" * 75)

    # 1. Validate RAG Retrieval Relevance
    rag_docs = search_knowledge_base("OWASP SQL Injection parameterized queries", k=2)
    assert isinstance(rag_docs, list), "RAG retrieval must return a document list"
    print(f"[PASS] RAG Knowledge Base Retrieval Verified ({len(rag_docs)} chunks returned)")

    # 2. Validate Detection, Remediation & PDF Report Generation Across All 3 Samples
    for fname, expected_lang, code in SAMPLES:
        val = validate_submission(code, filename=fname)
        assert val.is_valid, f"Syntax validation failed on valid sample: {fname}"
        assert val.detected_language == expected_lang, f"Language mismatch on {fname}"

        report = run_review_pipeline(code=code, language=val.detected_language, filename=fname)
        unified = report.get("unified_findings", [])
        remediations = report.get("remediation_plan", [])

        assert len(unified) > 0, f"Expected findings in {fname}"
        assert len(remediations) == len(unified), f"Every finding in {fname} must have a remediation item"

        pdf_bytes = generate_pdf_report(report)
        md_text = generate_full_markdown_report(report)

        assert pdf_bytes.startswith(b"%PDF-"), f"Generated PDF for {fname} must have valid %PDF header"
        assert len(md_text) > 200, f"Markdown report for {fname} is incomplete"

        print(
            f"[PASS] {fname} ({expected_lang.upper()}): "
            f"Findings={len(unified)} | Remediations={len(remediations)} | "
            f"Health={report['quality_assessment']['code_health_score']}/100 | "
            f"PDF Size={len(pdf_bytes)} bytes"
        )

    print("=" * 75)
    print("ALL END-TO-END TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_end_to_end_validation()
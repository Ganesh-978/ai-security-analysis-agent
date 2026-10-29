import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Anchor database path to the absolute project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "reviews.db"


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # If reviews.db was accidentally created as a folder in VS Code, remove the folder
    if DB_PATH.exists() and DB_PATH.is_dir():
        shutil.rmtree(DB_PATH)

    with sqlite3.connect(str(DB_PATH), check_same_thread=False) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                filename TEXT NOT NULL,
                language TEXT NOT NULL,
                maintainability_score REAL,
                cyclomatic_complexity INTEGER,
                critical_count INTEGER,
                high_count INTEGER,
                total_findings INTEGER,
                report_json TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_review_to_db(report: Dict[str, Any]) -> None:
    init_db()
    qa = report.get("quality_assessment") or {}
    cm = report.get("complexity_metrics") or {}
    sev = report.get("severity_breakdown") or {}
    unified = report.get("unified_findings") or []

    with sqlite3.connect(str(DB_PATH), check_same_thread=False) as conn:
        conn.execute(
            """
            INSERT INTO review_history (
                timestamp, filename, language, maintainability_score,
                cyclomatic_complexity, critical_count, high_count,
                total_findings, report_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                report.get("filename", "snippet"),
                report.get("language", "unknown"),
                qa.get("maintainability_score", 0.0),
                cm.get("cyclomatic_complexity", 0),
                sev.get("Critical", 0),
                sev.get("High", 0),
                len(unified),
                json.dumps(report),
            ),
        )
        conn.commit()


def get_recent_reviews(limit: int = 10) -> List[Dict[str, Any]]:
    init_db()
    with sqlite3.connect(str(DB_PATH), check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, timestamp, filename, language, maintainability_score,
                   cyclomatic_complexity, critical_count, high_count, total_findings
            FROM review_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
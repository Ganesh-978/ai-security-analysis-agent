import html
import inspect
import json
import os
import sys
import time
from pathlib import Path

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import requests
import streamlit as st
from parsers.code_validator import detect_language, validate_submission
from reports.report_generator import (
    compute_grade_and_verdict,
    generate_executive_html_report,
    generate_full_markdown_report,
    generate_pdf_report,
)
from services.database import save_review_to_db, get_recent_reviews
from ui.charts import (
    build_git_diff_html,
    build_pentagon_radar_figure,
    build_severity_bar_figure,
)

try:
    from streamlit_ace import st_ace

    HAS_ACE_EDITOR = True
except Exception:
    HAS_ACE_EDITOR = False

APP_TITLE = "AI Code Review & Security Analysis Agent"
APP_SUBTITLE = "Multi-Agent Static Analysis, OWASP Top 10 Security Review & RAG Remediation Platform"

API_BASE = "http://127.0.0.1:8000"
HEALTH_URL = f"{API_BASE}/health"
ANALYZE_URL = f"{API_BASE}/api/v1/analyze"
CHAT_URL = f"{API_BASE}/api/v1/chat"
FIX_ALL_URL = f"{API_BASE}/api/v1/fix-all"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _render_html(markup: str) -> None:
    """
    Renders HTML/CSS safely in Streamlit by stripping leading indentation per line
    so CommonMark never turns indented tags into raw code blocks.
    """
    compact = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(compact, unsafe_allow_html=True)


def _render_ace_editor(
    value: str,
    language: str,
    height: int,
    key: str,
    annotations: list = None,
) -> str:
    """
    Renders a full IDE-grade code editor (line numbers, syntax highlighting, zero
    English spellcheck squiggles, and live syntax-error gutter markers).
    """
    if not HAS_ACE_EDITOR:
        return st.text_area(
            "Source Code Editor",
            value=value,
            height=height,
            key=f"fallback_{key}",
            label_visibility="collapsed",
        )

    ace_lang = "java" if language == "java" else "python"
    kwargs = {
        "value": value,
        "language": ace_lang,
        "theme": "chrome",
        "keybinding": "vscode",
        "font_size": 14,
        "tab_size": 4,
        "show_gutter": True,
        "show_print_margin": False,
        "wrap": False,
        "auto_update": True,
        "height": height,
        "key": key,
    }

    try:
        sig = inspect.signature(st_ace)
        if annotations and "annotations" in sig.parameters:
            kwargs["annotations"] = annotations
    except Exception:
        pass

    content = st_ace(**kwargs)
    return value if content is None else content


# ---------------------------------------------------------------------------
# Complete Unified Enterprise Blue & White Design System (Single Stylesheet)
# ---------------------------------------------------------------------------
_render_html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
[data-testid="stAppViewContainer"], .stApp {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
.block-container {
    padding-top: 1.15rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
}
#MainMenu, footer, [data-testid="stDeployButton"] {
    visibility: hidden !important;
    display: none !important;
}

/* Primary Buttons -> Royal Enterprise Blue */
button[kind="primary"],
div.stButton > button[kind="primary"],
div.stDownloadButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #1D4ED8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
    transition: all 0.15s ease !important;
}
button[kind="primary"]:hover,
div.stButton > button[kind="primary"]:hover,
div.stDownloadButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    color: #FFFFFF !important;
    border-color: #1E40AF !important;
}
button[kind="primary"] p, button[kind="primary"] span {
    color: #FFFFFF !important;
}

/* Secondary Buttons -> Crisp White with Dark Slate Text */
button[kind="secondary"],
div.stButton > button[kind="secondary"],
div.stDownloadButton > button[kind="secondary"],
div.stDownloadButton > button {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
}
button[kind="secondary"]:hover,
div.stButton > button[kind="secondary"]:hover,
div.stDownloadButton > button:hover {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
    border-color: #2563EB !important;
}
button[kind="secondary"] p, button[kind="secondary"] span {
    color: #0F172A !important;
}
button[kind="secondary"]:hover p, button[kind="secondary"]:hover span {
    color: #1D4ED8 !important;
}
button:disabled {
    background-color: #E2E8F0 !important;
    color: #64748B !important;
    border-color: #CBD5E1 !important;
    opacity: 0.75 !important;
}

/* Expanders */
[data-testid="stExpander"],
[data-testid="stExpander"] details {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    margin-bottom: 10px !important;
}
[data-testid="stExpander"] summary {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}
[data-testid="stExpander"] summary:hover {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary svg {
    color: #0F172A !important;
    fill: #0F172A !important;
}
[data-testid="stExpanderDetails"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-top: 1px solid #E2E8F0 !important;
}

/* File Uploader Dropzone */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background-color: #F8FAFC !important;
    border: 1.5px dashed #93C5FD !important;
    border-radius: 12px !important;
    color: #0F172A !important;
}
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] div {
    color: #334155 !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background-color: #FFFFFF !important;
    color: #1D4ED8 !important;
    border: 1px solid #2563EB !important;
    border-radius: 8px !important;
}

/* Segmented Control & Filter Pills */
[data-testid="stSegmentedControl"] button,
[data-baseweb="button-group"] button {
    background-color: #FFFFFF !important;
    color: #334155 !important;
    border: 1px solid #CBD5E1 !important;
    font-weight: 600 !important;
}
[data-testid="stSegmentedControl"] button[aria-pressed="true"],
[data-baseweb="button-group"] button[aria-pressed="true"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border-color: #2563EB !important;
}
[data-testid="stSegmentedControl"] button[aria-pressed="true"] p,
[data-baseweb="button-group"] button[aria-pressed="true"] p {
    color: #FFFFFF !important;
}

/* Selectbox, Inputs & Bordered Containers */
[data-baseweb="select"] > div,
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-color: #CBD5E1 !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] input,
label, .stMarkdown p, .stMarkdown li, .stCaption {
    color: #0F172A !important;
}
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
}

/* Code Blocks */
[data-testid="stCodeBlock"], pre {
    background-color: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}
[data-testid="stCodeBlock"] code, pre code {
    color: #0F172A !important;
}

/* IDE Editor Frame Header */
.cg-editor-header {
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-bottom: none;
    border-radius: 12px 12px 0 0;
    padding: 9px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.82rem;
    font-weight: 600;
    color: #1E293B;
    margin-top: 8px;
}
.cg-editor-dots {
    display: flex;
    align-items: center;
    gap: 6px;
}
.cg-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

/* Top Brand Bar */
.cg-topbar {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 16px;
    padding: 15px 24px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
}
.cg-brand { display: flex; align-items: center; gap: 14px; }
.cg-logo {
    width: 44px; height: 44px; border-radius: 12px;
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: #FFFFFF; display: flex; align-items: center; justify-content: center;
    font-size: 1.35rem; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28);
}
.cg-title { font-size: 1.22rem; font-weight: 800; color: #0F172A; letter-spacing: -0.025em; line-height: 1.2; }
.cg-sub { font-size: 0.81rem; color: #475569; margin-top: 2px; }
.cg-status-group { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.cg-pill {
    background: #EFF6FF; border: 1px solid #BFDBFE; color: #1E40AF;
    padding: 5px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 600;
}
.cg-pill-live {
    background: #ECFDF5; border: 1px solid #A7F3D0; color: #047857;
    padding: 5px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 600;
}

/* Section Headers */
.cg-section-head { margin: 6px 0 16px 0; }
.cg-section-head h2 { margin: 0; font-size: 1.42rem; font-weight: 700; color: #0F172A; letter-spacing: -0.02em; }
.cg-section-head p { margin: 4px 0 0 0; font-size: 0.89rem; color: #475569; }

/* Cards & Status Strips */
.cg-card {
    background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 14px;
    padding: 18px 22px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}
.cg-syntax-bar {
    background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px;
    padding: 12px 16px; margin: 10px 0 14px 0;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
}
.cg-syntax-left { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.cg-tag {
    display: inline-block; padding: 4px 10px; border-radius: 6px;
    font-size: 0.76rem; font-weight: 600; background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE;
}
.cg-tag-neutral {
    display: inline-block; padding: 4px 10px; border-radius: 6px;
    font-size: 0.76rem; font-weight: 600; background: #F1F5F9; color: #334155; border: 1px solid #CBD5E1;
}
.cg-badge-ok {
    background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0;
    padding: 4px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 600;
}
.cg-badge-err {
    background: #FEF2F2; color: #B91C1C; border: 1px solid #FECACA;
    padding: 4px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 600;
}

/* KPI Grid */
.cg-kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 16px; }
.cg-kpi {
    background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 14px;
    padding: 18px 20px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}
.cg-kpi-label { font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: #475569; }
.cg-kpi-val { font-size: 1.82rem; font-weight: 800; color: #0F172A; margin: 4px 0 2px 0; letter-spacing: -0.03em; }
.cg-kpi-foot { font-size: 0.78rem; color: #64748B; }

/* 5-Column Severity Strip */
.cg-sev-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 18px; }
.cg-sev-card { border-radius: 12px; padding: 13px 12px; text-align: center; border: 1px solid #CBD5E1; background: #FFFFFF; }
.cg-sev-crit { border-top: 4px solid #DC2626; }
.cg-sev-high { border-top: 4px solid #EA580C; }
.cg-sev-med  { border-top: 4px solid #CA8A04; }
.cg-sev-low  { border-top: 4px solid #2563EB; }
.cg-sev-info { border-top: 4px solid #64748B; }
.cg-sev-count { font-size: 1.48rem; font-weight: 800; color: #0F172A; }
.cg-sev-name  { font-size: 0.73rem; font-weight: 700; text-transform: uppercase; color: #475569; margin-top: 2px; }

.cg-tele-footer { display: flex; flex-wrap: wrap; gap: 8px; padding-top: 10px; margin-top: 4px; border-top: 1px solid #E2E8F0; }
.cg-gauge-head { display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; color: #1E293B; margin-bottom: 6px; }
.cg-track { width: 100%; height: 9px; background: #E2E8F0; border-radius: 999px; overflow: hidden; }
.cg-fill { height: 100%; border-radius: 999px; }

/* Git-Style Diff Viewer */
.gd-wrap { border: 1px solid #CBD5E1; border-radius: 12px; overflow: hidden; background: #FFFFFF; margin: 12px 0 18px 0; }
.gd-header {
    background: #EFF6FF; border-bottom: 1px solid #BFDBFE; padding: 10px 16px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    font-size: 0.82rem; font-weight: 600; color: #1E3A8A;
}
.gd-stat-add { background: #DCFCE7; color: #166534; padding: 3px 9px; border-radius: 999px; font-size: 0.75rem; margin-right: 6px; }
.gd-stat-del { background: #FEE2E2; color: #991B1B; padding: 3px 9px; border-radius: 999px; font-size: 0.75rem; }
.gd-scroll { max-height: 480px; overflow: auto; }
.gd-table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.8rem; line-height: 1.5; }
.gd-ln { width: 44px; min-width: 40px; text-align: right; padding: 1px 8px; color: #94A3B8; user-select: none; border-right: 1px solid #E2E8F0; }
.gd-sign { width: 24px; text-align: center; font-weight: 700; user-select: none; }
.gd-code { padding: 1px 12px; white-space: pre; }
.gd-eq td { background: #FFFFFF; color: #334155; }
.gd-del td { background: #FEF2F2; color: #991B1B; }
.gd-del .gd-ln { background: #FEE2E2; color: #B91C1C; }
.gd-add td { background: #ECFDF5; color: #166534; }
.gd-add .gd-ln { background: #DCFCE7; color: #15803D; }

/* Centered Modern Chatbot Styling */
[data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(248, 250, 252, 0) 0%, #F8FAFC 30%) !important;
    padding-bottom: 14px !important;
}
[data-testid="stBottom"] > div {
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 0 12px !important;
}
[data-testid="stChatInput"] {
    max-width: 820px !important;
    margin: 0 auto !important;
}
[data-testid="stChatInput"] > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 16px !important;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.08) !important;
    padding: 4px 6px !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14), 0 6px 20px rgba(15, 23, 42, 0.08) !important;
}
[data-testid="stChatInput"] textarea {
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
    color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    width: 38px !important;
    height: 38px !important;
    margin: 2px !important;
}
[data-testid="stChatInputSubmitButton"]:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
}
[data-testid="stChatInputSubmitButton"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}
[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
}

/* Empty State */
.cg-empty { background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 16px; padding: 48px 24px; text-align: center; margin: 18px 0; }
.cg-empty h3 { color: #0F172A; margin: 10px 0 8px 0; font-weight: 700; }
.cg-empty p  { color: #475569; max-width: 520px; margin: 0 auto; font-size: 0.92rem; }

/* Monospace Fallback Textarea */
textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.87rem !important;
    line-height: 1.55 !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
}

@media (max-width: 960px) {
    .cg-kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .cg-sev-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 600px) {
    .cg-kpi-grid { grid-template-columns: 1fr; }
    .cg-sev-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""
)

# ---------------------------------------------------------------------------
# 3 Benchmark Samples of Varying Complexity
# ---------------------------------------------------------------------------
BENCHMARK_SAMPLES = {
    "Low Complexity — Python Token Utility": {
        "filename": "token_utility.py",
        "code": (
            "import hashlib\n"
            "import random\n\n"
            "# Hardcoded API Secret (OWASP A02 / CWE-798 / Bandit B105)\n"
            'DEFAULT_API_SECRET = "sk_live_998877665544332211_secret"\n\n\n'
            "def generate_reset_token(user_email):\n"
            "    # Weak PRNG + Weak MD5 Hashing (OWASP A02 / CWE-328 & CWE-338)\n"
            '    seed = f"{user_email}-{random.randint(1000, 9999)}"\n'
            '    return hashlib.md5(seed.encode("utf-8")).hexdigest()\n'
        ),
    },
    "Medium Complexity — Python Auth & Order API": {
        "filename": "auth_order_controller.py",
        "code": (
            "import sqlite3\n"
            "import subprocess\n\n"
            'JWT_SIGNING_SECRET = "prod-jwt-secret-key-2026-hardcoded"\n\n\n'
            "def authenticate_and_audit(username, raw_filter_expr, audit_host, cart_items):\n"
            '    conn = sqlite3.connect("enterprise_store.db")\n'
            "    cursor = conn.cursor()\n\n"
            "    # SQL Injection via f-string (OWASP A03 / CWE-89 / Bandit B608)\n"
            "    query = f\"SELECT id, role FROM users WHERE username = '{username}'\"\n"
            "    cursor.execute(query)\n"
            "    user_row = cursor.fetchone()\n\n"
            "    # OS Command Injection via shell=True (OWASP A03 / CWE-78 / Bandit B602)\n"
            '    subprocess.Popen("ping -c 1 " + audit_host, shell=True)\n\n'
            "    # Arbitrary Code Execution via eval (OWASP A03 / CWE-95 / Bandit B307)\n"
            "    discount_factor = eval(raw_filter_expr)\n\n"
            "    # Spaghetti Code / Deep Nesting + Magic Numbers\n"
            "    net_total = 0.0\n"
            "    if user_row is not None:\n"
            "        if cart_items is not None:\n"
            "            for item in cart_items:\n"
            '                if item.get("price", 0) > 0:\n'
            '                    if item.get("qty", 0) > 25:\n'
            '                        net_total += item["price"] * item["qty"] * 0.845\n'
            "                    else:\n"
            '                        net_total += item["price"] * item["qty"] * 1.125\n\n'
            "    try:\n"
            "        conn.commit()\n"
            "    except:\n"
            "        pass\n\n"
            "    return net_total - discount_factor\n"
        ),
    },
    "High Complexity — Java Banking Service": {
        "filename": "EnterprisePaymentService.java",
        "code": (
            "import java.security.MessageDigest;\n"
            "import java.sql.Connection;\n"
            "import java.sql.DriverManager;\n"
            "import java.sql.ResultSet;\n"
            "import java.sql.Statement;\n\n"
            "public class EnterprisePaymentService {\n\n"
            "    // Hardcoded Database Credential (OWASP A07 / CWE-798 / SpotBugs)\n"
            '    private static final String DB_PASSWORD = "ProdRootPassword!9988";\n\n'
            "    public ResultSet processAccountSettlement(String accountId, String rawPin, int tierLevel, double amount) {\n"
            "        ResultSet rs = null;\n"
            "        try {\n"
            "            // Weak MD5 Cryptographic Hash (OWASP A02 / CERT MSC61-J / CWE-328)\n"
            '            MessageDigest md = MessageDigest.getInstance("MD5");\n'
            "            byte[] pinHash = md.digest(rawPin.getBytes());\n\n"
            "            // Unclosed JDBC Connection Resource Leak (SpotBugs / PMD CloseResource)\n"
            "            Connection conn = DriverManager.getConnection(\n"
            '                "jdbc:mysql://10.20.30.40:3306/core_banking", "admin", DB_PASSWORD\n'
            "            );\n"
            "            Statement stmt = conn.createStatement();\n\n"
            "            // SQL Injection via String Concatenation (OWASP A03 / CERT IDS00-J / CWE-89)\n"
            '            String sql = "SELECT balance, status FROM ledgers WHERE account_id = \'" + accountId + "\'";\n'
            "            rs = stmt.executeQuery(sql);\n\n"
            "            // Deeply Nested Control Flow (Spaghetti Code) & Magic Numbers\n"
            "            if (tierLevel > 0) {\n"
            "                if (tierLevel != 99) {\n"
            "                    if (amount > 10000.0) {\n"
            "                        if (tierLevel == 42) {\n"
            '                            System.out.println("High value settlement authorized");\n'
            "                        }\n"
            "                    }\n"
            "                }\n"
            "            }\n"
            "        } catch (Exception e) {\n"
            "            // Empty Catch Block Swallowing Exceptions (PMD EmptyCatchBlock)\n"
            "        }\n"
            "        return rs;\n"
            "    }\n"
            "}\n"
        ),
    },
}

# ---------------------------------------------------------------------------
# Zero Re-Scan Session State Initialization
# ---------------------------------------------------------------------------
defaults = {
    "active_page": "Code Scanner",
    "editor_code": BENCHMARK_SAMPLES["Medium Complexity — Python Auth & Order API"]["code"],
    "editor_filename": BENCHMARK_SAMPLES["Medium Complexity — Python Auth & Order API"]["filename"],
    "editor_version": 0,
    "last_uploaded_id": None,
    "review_report": None,
    "scan_id": 0,
    "submitted_code": "",
    "chat_history": [],
    "elapsed_seconds": None,
    "fixed_full_code": "",
    "fixed_filename": "",
    "fixed_issues_count": 0,
    "cached_radar_fig": None,
    "cached_sev_fig": None,
    "cached_report_scan_id": -1,
    "cached_html_report": "",
    "cached_pdf_report": b"",
    "cached_md_report": "",
    "cached_json_report": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def _set_editor_content(code_text: str, fname: str) -> None:
    """Programmatically updates the IDE code editor by bumping its mount version."""
    st.session_state.editor_code = code_text
    st.session_state.editor_filename = fname
    st.session_state.editor_version += 1


def _is_fastapi_online() -> bool:
    try:
        r = requests.get(HEALTH_URL, timeout=0.35)
        return r.status_code == 200
    except Exception:
        return False


def _pill_selector(label: str, options: list, default: str):
    if hasattr(st, "segmented_control"):
        val = st.segmented_control(label, options, default=default, label_visibility="collapsed")
        return val if val else default
    return st.radio(
        label,
        options,
        index=options.index(default),
        horizontal=True,
        label_visibility="collapsed",
    )


def _clear_hitl_states() -> None:
    for k in list(st.session_state.keys()):
        if k.startswith("hitl_studio_"):
            del st.session_state[k]


def _execute_scan(code_text: str, language: str, fname: str, backend_online: bool) -> None:
    start_t = time.perf_counter()
    report_data = None
    if backend_online:
        try:
            resp = requests.post(
                ANALYZE_URL,
                json={"filename": fname, "code": code_text, "language": language},
                timeout=40,
            )
            if resp.status_code == 200:
                report_data = resp.json()
        except Exception:
            report_data = None

    if report_data is None:
        from src.workflow import run_review_pipeline

        raw_res = run_review_pipeline(code=code_text, language=language, filename=fname)
        raw_res["filename"] = fname
        raw_res["language"] = language
        save_review_to_db(raw_res)
        report_data = raw_res

    st.session_state.scan_id += 1
    st.session_state.review_report = report_data
    st.session_state.elapsed_seconds = round(time.perf_counter() - start_t, 2)
    st.session_state.submitted_code = code_text
    st.session_state.fixed_full_code = ""
    st.session_state.fixed_filename = ""
    st.session_state.fixed_issues_count = 0
    st.session_state.cached_radar_fig = build_pentagon_radar_figure(report_data)
    st.session_state.cached_sev_fig = build_severity_bar_figure(report_data)
    st.session_state.cached_report_scan_id = -1
    _clear_hitl_states()


def _execute_fix_all(report_data: dict, orig_code: str, backend_online: bool) -> None:
    fname = str(report_data.get("filename", "snippet.py"))
    lang = str(report_data.get("language", "python")).lower()
    findings = report_data.get("unified_findings") or []
    rem_plan = report_data.get("remediation_plan") or []

    fix_payload = None
    if backend_online:
        try:
            resp = requests.post(
                FIX_ALL_URL,
                json={
                    "filename": fname,
                    "language": lang,
                    "code": orig_code,
                    "findings": findings,
                    "remediation_plan": rem_plan,
                },
                timeout=45,
            )
            if resp.status_code == 200:
                fix_payload = resp.json()
        except Exception:
            fix_payload = None

    if fix_payload is None:
        from src.agents import generate_full_file_fix

        fix_payload = generate_full_file_fix(
            filename=fname,
            language=lang,
            code=orig_code,
            findings=findings,
            remediation_plan=rem_plan,
        )

    st.session_state.fixed_full_code = fix_payload.get("fixed_code", "")
    ext = "py" if lang == "python" else "java"
    st.session_state.fixed_filename = fix_payload.get("fixed_filename", f"{Path(fname).stem}_fixed.{ext}")
    st.session_state.fixed_issues_count = int(fix_payload.get("issues_addressed", len(findings)))
    for r in rem_plan:
        fid = r.get("finding_id", "ID")
        st.session_state[f"hitl_studio_{fid}"] = "Approved & Applied"


def _ensure_cached_exports(report_data: dict) -> None:
    if st.session_state.cached_report_scan_id == st.session_state.scan_id:
        return
    st.session_state.cached_html_report = generate_executive_html_report(report_data)
    st.session_state.cached_pdf_report = generate_pdf_report(report_data)
    st.session_state.cached_md_report = generate_full_markdown_report(report_data)
    st.session_state.cached_json_report = json.dumps(report_data, indent=2)
    st.session_state.cached_report_scan_id = st.session_state.scan_id


SEVERITY_ICON = {
    "Critical": "🔴 CRITICAL",
    "High": "🟠 HIGH",
    "Medium": "🟡 MEDIUM",
    "Low": "🔵 LOW",
    "Informational": "⚪ INFO",
}

CATEGORY_BADGE = {
    "Security Recommendation": "🔒 Security Remediation",
    "Code Quality Recommendation": "🧹 Code Quality Refactoring",
    "Performance Recommendation": "⚡ Performance Optimization",
    "Maintainability Recommendation": "🏗️ Maintainability Enhancement",
}

backend_online = _is_fastapi_online()

# ---------------------------------------------------------------------------
# Top Enterprise Navigation Bar
# ---------------------------------------------------------------------------
status_pills = []
if st.session_state.review_report:
    fname_esc = html.escape(str(st.session_state.review_report.get("filename", "")))
    status_pills.append(f'<span class="cg-pill">📄 {fname_esc}</span>')
else:
    status_pills.append('<span class="cg-pill">📄 Ready to Scan</span>')

if st.session_state.elapsed_seconds is not None:
    status_pills.append(f'<span class="cg-pill">⚡ {st.session_state.elapsed_seconds}s</span>')

if backend_online:
    status_pills.append('<span class="cg-pill-live">● FastAPI Backend Online</span>')
else:
    status_pills.append('<span class="cg-pill-live">● Direct Agent Engine Ready</span>')

_render_html(
    f"""
<div class="cg-topbar">
<div class="cg-brand">
<div class="cg-logo">🛡️</div>
<div>
<div class="cg-title">{APP_TITLE}</div>
<div class="cg-sub">{APP_SUBTITLE}</div>
</div>
</div>
<div class="cg-status-group">{''.join(status_pills)}</div>
</div>
"""
)

# ---------------------------------------------------------------------------
# Full-Width 5-Page Navigation Bar
# ---------------------------------------------------------------------------
rep = st.session_state.review_report
total_findings_count = len(rep.get("unified_findings", [])) if rep else 0
rem_count = len(rep.get("remediation_plan", [])) if rep else 0

nav_items = [
    ("Code Scanner", "🔍 Code Scanner"),
    ("Review Dashboard", f"📊 Dashboard ({total_findings_count})" if rep else "📊 Dashboard"),
    ("Remediation Studio", f"🛠️ Remediations ({rem_count})" if rep else "🛠️ Remediations"),
    ("AI Code Assistant", "💬 AI Assistant"),
    ("Reports & History", "📄 Reports & History"),
]

nav_cols = st.columns(len(nav_items))
for idx, (page_key, label) in enumerate(nav_items):
    btn_type = "primary" if st.session_state.active_page == page_key else "secondary"
    if nav_cols[idx].button(label, key=f"nav_{page_key}", type=btn_type, width="stretch"):
        st.session_state.active_page = page_key
        st.rerun()

_render_html('<div style="height: 10px;"></div>')

# ===========================================================================
# PAGE 1: CODE SCANNER (IDE-GRADE CODE EDITOR WITH LINE NUMBERS & SYNTAX CHECK)
# ===========================================================================
if st.session_state.active_page == "Code Scanner":
    _render_html(
        """
<div class="cg-section-head">
<h2>Source Code Scanner</h2>
<p>Paste Python or Java source code, upload a file, or select a benchmark sample to trigger the parallel multi-agent review pipeline.</p>
</div>
"""
    )

    b1, b2, b3, b4 = st.columns([1.2, 1.2, 1.2, 0.7])
    sample_keys = list(BENCHMARK_SAMPLES.keys())
    if b1.button("⚡ Low Complexity (Python)", width="stretch"):
        _set_editor_content(
            BENCHMARK_SAMPLES[sample_keys[0]]["code"],
            BENCHMARK_SAMPLES[sample_keys[0]]["filename"],
        )
        st.rerun()
    if b2.button("⚡ Medium Complexity (Python)", width="stretch"):
        _set_editor_content(
            BENCHMARK_SAMPLES[sample_keys[1]]["code"],
            BENCHMARK_SAMPLES[sample_keys[1]]["filename"],
        )
        st.rerun()
    if b3.button("⚡ High Complexity (Java)", width="stretch"):
        _set_editor_content(
            BENCHMARK_SAMPLES[sample_keys[2]]["code"],
            BENCHMARK_SAMPLES[sample_keys[2]]["filename"],
        )
        st.rerun()
    if b4.button("🗑️ Clear", width="stretch"):
        _set_editor_content("", "snippet.py")
        st.rerun()

    with st.expander("📁 Upload a Python (.py) or Java (.java) source file from your computer", expanded=False):
        uploaded_file = st.file_uploader(
            "Choose a .py or .java file",
            type=["py", "java"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None and uploaded_file.file_id != st.session_state.last_uploaded_id:
            st.session_state.last_uploaded_id = uploaded_file.file_id
            _set_editor_content(
                uploaded_file.getvalue().decode("utf-8", errors="replace"),
                uploaded_file.name,
            )
            st.rerun()

    # Pre-detect language & syntax for IDE syntax highlighting and gutter error marker
    pre_lang = detect_language(
        st.session_state.editor_code, filename=st.session_state.editor_filename
    )
    pre_val = validate_submission(
        st.session_state.editor_code, filename=st.session_state.editor_filename
    )
    ace_annotations = None
    if st.session_state.editor_code.strip() and not pre_val.is_valid and pre_val.line_number:
        ace_annotations = [
            {
                "row": max(0, int(pre_val.line_number) - 1),
                "column": 0,
                "text": str(pre_val.error_message or "Syntax Error"),
                "type": "error",
            }
        ]

    lang_mode_label = (
        "Python" if pre_lang == "python" else "Java" if pre_lang == "java" else "Auto-Detect"
    )
    _render_html(
        f"""
<div class="cg-editor-header">
<div class="cg-editor-dots">
<span class="cg-dot" style="background:#EF4444;"></span>
<span class="cg-dot" style="background:#F59E0B;"></span>
<span class="cg-dot" style="background:#10B981;"></span>
<span style="margin-left:8px;">{html.escape(str(st.session_state.editor_filename))}</span>
</div>
<div><span class="cg-tag">{lang_mode_label} IDE · Line Numbers &amp; Syntax Highlighting</span></div>
</div>
"""
    )

    code_input = _render_ace_editor(
        value=st.session_state.editor_code,
        language=pre_lang,
        height=400,
        key=f"scanner_ace_v{st.session_state.editor_version}",
        annotations=ace_annotations,
    )
    st.session_state.editor_code = code_input

    validation = validate_submission(code_input, filename=st.session_state.editor_filename)

    if code_input.strip():
        lang_disp = (
            "🐍 Python"
            if validation.detected_language == "python"
            else "☕ Java"
            if validation.detected_language == "java"
            else "❓ Unknown"
        )
        status_badge = (
            '<span class="cg-badge-ok">✓ Syntax Valid — Ready to Scan</span>'
            if validation.is_valid
            else f'<span class="cg-badge-err">✕ Syntax Error (Line {validation.line_number})</span>'
        )
        _render_html(
            f"""
<div class="cg-syntax-bar">
<div class="cg-syntax-left">
<span class="cg-tag">Auto-Detected: {lang_disp}</span>
<span class="cg-tag-neutral">Parser: {html.escape(validation.parser_used)}</span>
<span class="cg-tag-neutral">AST Nodes: {validation.ast_node_count}</span>
</div>
<div>{status_badge}</div>
</div>
"""
        )

        if not validation.is_valid:
            st.error(
                f"Syntax Gatekeeper Blocked Execution — Line {validation.line_number}: {validation.error_message}"
            )
            if validation.offending_line:
                st.code(validation.offending_line, language="text")

    cta_left, cta_right = st.columns([2.2, 1])
    with cta_left:
        scan_clicked = st.button(
            "🚀 Run Multi-Agent Security & Code Quality Scan",
            type="primary",
            disabled=(not code_input.strip() or not validation.is_valid),
            width="stretch",
        )
    with cta_right:
        if rep is not None:
            if st.button("📊 Open Full Dashboard →", width="stretch"):
                st.session_state.active_page = "Review Dashboard"
                st.rerun()

    if scan_clicked:
        fname = st.session_state.editor_filename or (
            "snippet.py" if validation.detected_language == "python" else "Snippet.java"
        )
        with st.spinner("Running SAST scanners, parallel Code & Security agents, OWASP rule matching, and remediation synthesis..."):
            _execute_scan(code_input, validation.detected_language, fname, backend_online)
        st.session_state.active_page = "Review Dashboard"
        st.rerun()

    if rep is not None:
        qa = rep.get("quality_assessment") or {}
        sev = rep.get("severity_breakdown") or {}
        health = qa.get("code_health_score", 80.0)
        h_color = "#059669" if health >= 75 else "#D97706" if health >= 50 else "#DC2626"

        st.markdown("---")
        st.markdown("#### Latest Scan Overview")
        _render_html(
            f"""
<div class="cg-kpi-grid">
<div class="cg-kpi" style="border-top: 4px solid {h_color};">
<div class="cg-kpi-label">Code Health Score</div>
<div class="cg-kpi-val" style="color: {h_color};">{health}/100</div>
<div class="cg-kpi-foot">{html.escape(str(rep.get('filename', '')))}</div>
</div>
<div class="cg-kpi" style="border-top: 4px solid #EF4444;">
<div class="cg-kpi-label">Critical &amp; High Risks</div>
<div class="cg-kpi-val">{sev.get('Critical', 0) + sev.get('High', 0)}</div>
<div class="cg-kpi-foot">{sev.get('Critical', 0)} Critical · {sev.get('High', 0)} High</div>
</div>
<div class="cg-kpi" style="border-top: 4px solid #2563EB;">
<div class="cg-kpi-label">Total Findings</div>
<div class="cg-kpi-val">{len(rep.get('unified_findings', []))}</div>
<div class="cg-kpi-foot">{len(rep.get('security_findings', []))} Security · {len(rep.get('quality_findings', []))} Quality</div>
</div>
<div class="cg-kpi" style="border-top: 4px solid #4F46E5;">
<div class="cg-kpi-label">Estimated Tech Debt</div>
<div class="cg-kpi-val">{qa.get('technical_debt_minutes', 0)}m</div>
<div class="cg-kpi-foot">Scanned in {st.session_state.elapsed_seconds or 0}s</div>
</div>
</div>
"""
        )

# ===========================================================================
# PAGE 2: REVIEW DASHBOARD
# ===========================================================================
elif st.session_state.active_page == "Review Dashboard":
    if rep is None:
        _render_html(
            """
<div class="cg-empty">
<div style="font-size: 2.5rem;">📊</div>
<h3>No Analysis Report Available Yet</h3>
<p>Go to the Code Scanner, select a benchmark sample or paste your Python/Java code, and run a scan to view the executive dashboard.</p>
</div>
"""
        )
        c_mid = st.columns([1, 1, 1])[1]
        if c_mid.button("← Go to Code Scanner", type="primary", width="stretch"):
            st.session_state.active_page = "Code Scanner"
            st.rerun()
    else:
        qa = rep.get("quality_assessment") or {}
        cm = rep.get("complexity_metrics") or {}
        sev = rep.get("severity_breakdown") or {}
        unified = rep.get("unified_findings") or []
        sec_list = rep.get("security_findings") or []
        qual_list = rep.get("quality_findings") or []
        lang = rep.get("language", "python")

        health = float(qa.get("code_health_score", 80.0))
        grade_info = compute_grade_and_verdict(health, sev)
        h_color = grade_info["color"]

        _render_html(
            f"""
<div class="cg-section-head">
<h2>Security &amp; Code Quality Dashboard — {html.escape(str(rep.get('filename', 'snippet')))}</h2>
<p>Interactive telemetry from the Code Analysis Agent, Security Vulnerability Agent, SAST scanners, and OWASP Top 10 knowledge base.</p>
</div>
"""
        )

        _render_html(
            f"""
<div class="cg-kpi-grid">
<div class="cg-kpi" style="border-top: 4px solid {h_color};">
<div class="cg-kpi-label">Overall Code Health (Grade {grade_info['grade']})</div>
<div class="cg-kpi-val" style="color: {h_color};">{health}/100</div>
<div class="cg-kpi-foot">Maintainability: {qa.get('maintainability_score', 0)}/100</div>
</div>
<div class="cg-kpi" style="border-top: 4px solid #EF4444;">
<div class="cg-kpi-label">Security Vulnerabilities</div>
<div class="cg-kpi-val">{len(sec_list)}</div>
<div class="cg-kpi-foot">OWASP Top 10 &amp; CWE Rules</div>
</div>
<div class="cg-kpi" style="border-top: 4px solid #F97316;">
<div class="cg-kpi-label">Code Quality &amp; Smells</div>
<div class="cg-kpi-val">{len(qual_list)}</div>
<div class="cg-kpi-foot">Anti-Patterns &amp; Complexity</div>
</div>
<div class="cg-kpi" style="border-top: 4px solid #2563EB;">
<div class="cg-kpi-label">Estimated Tech Debt</div>
<div class="cg-kpi-val">{qa.get('technical_debt_minutes', 0)} mins</div>
<div class="cg-kpi-foot">Cyclomatic: {cm.get('cyclomatic_complexity', 1)} ({html.escape(str(cm.get('cyclomatic_rank', 'A')))})</div>
</div>
</div>
"""
        )

        _render_html(
            f"""
<div class="cg-sev-grid">
<div class="cg-sev-card cg-sev-crit"><div class="cg-sev-count">{sev.get('Critical', 0)}</div><div class="cg-sev-name">Critical</div></div>
<div class="cg-sev-card cg-sev-high"><div class="cg-sev-count">{sev.get('High', 0)}</div><div class="cg-sev-name">High</div></div>
<div class="cg-sev-card cg-sev-med"><div class="cg-sev-count">{sev.get('Medium', 0)}</div><div class="cg-sev-name">Medium</div></div>
<div class="cg-sev-card cg-sev-low"><div class="cg-sev-count">{sev.get('Low', 0)}</div><div class="cg-sev-name">Low</div></div>
<div class="cg-sev-card cg-sev-info"><div class="cg-sev-count">{sev.get('Informational', 0)}</div><div class="cg-sev-name">Informational</div></div>
</div>
"""
        )

        if st.session_state.cached_radar_fig is None:
            st.session_state.cached_radar_fig = build_pentagon_radar_figure(rep)
        if st.session_state.cached_sev_fig is None:
            st.session_state.cached_sev_fig = build_severity_bar_figure(rep)

        ch_left, ch_right = st.columns([1.05, 1], gap="large")
        with ch_left:
            with st.container(border=True):
                st.markdown("#### ⬟ Quality & Security Posture Radar")
                st.plotly_chart(
                    st.session_state.cached_radar_fig,
                    width="stretch",
                    config={"displayModeBar": False, "responsive": True},
                )
                _render_html(
                    f"""
<div class="cg-tele-footer">
<span class="cg-tag-neutral">Cyclomatic: {cm.get('cyclomatic_complexity', 1)}</span>
<span class="cg-tag-neutral">Cognitive: {cm.get('cognitive_complexity', 0)}</span>
<span class="cg-tag-neutral">Time: {html.escape(str(cm.get('time_complexity', 'O(1)')))}</span>
<span class="cg-tag-neutral">Space: {html.escape(str(cm.get('space_complexity', 'O(1)')))}</span>
</div>
"""
                )

        with ch_right:
            with st.container(border=True):
                st.markdown("#### 🎯 Severity Distribution")
                st.plotly_chart(
                    st.session_state.cached_sev_fig,
                    width="stretch",
                    config={"displayModeBar": False, "responsive": True},
                )
                _render_html(
                    f"""
<div class="cg-tele-footer">
<span class="cg-tag-neutral">Verdict: {html.escape(grade_info['verdict'])}</span>
</div>
"""
                )

        sub_view = _pill_selector(
            "Dashboard Section",
            ["All Unified Findings", "Security Only", "Code Quality Only", "PR Review Summary"],
            default="All Unified Findings",
        )

        if sub_view == "PR Review Summary":
            with st.container(border=True):
                st.markdown(rep.get("pr_summary_markdown", "No PR summary generated."))
        else:
            shown = (
                unified
                if sub_view == "All Unified Findings"
                else sec_list
                if sub_view == "Security Only"
                else qual_list
            )
            if not shown:
                st.success("No issues flagged in this category.")
            for item in shown:
                sev_label = SEVERITY_ICON.get(item.get("severity", "Medium"), "🟡 MEDIUM")
                v_name = item.get("vulnerability_name") or item.get("issue_type", "Issue")
                with st.expander(
                    f"{sev_label}  |  [{item.get('id', '')}] {v_name} — {item.get('line_reference', '')}",
                    expanded=(item.get("severity") == "Critical"),
                ):
                    _render_html(
                        f'<span class="cg-tag">{html.escape(str(item.get("agent_source", "")))}</span> '
                        f'<span class="cg-tag-neutral">{html.escape(str(item.get("owasp_category") or item.get("tool_or_standard", "")))}</span> '
                        f'<span class="cg-tag-neutral">Location: {html.escape(str(item.get("line_reference", "")))}</span>'
                    )
                    if item.get("code_snippet"):
                        st.code(item["code_snippet"], language=lang)
                    st.markdown(f"**Risk & Impact Analysis:** {item.get('description', '')}")
                    st.markdown(f"**Actionable Recommendation:** {item.get('recommendation', '')}")

        _render_html('<div style="height: 8px;"></div>')
        nav_b1, nav_b2 = st.columns(2)
        if nav_b1.button("🛠️ Open Remediation Studio & Fix Everything →", type="primary", width="stretch"):
            st.session_state.active_page = "Remediation Studio"
            st.rerun()
        if nav_b2.button("💬 Ask AI Assistant About These Findings →", width="stretch"):
            st.session_state.active_page = "AI Code Assistant"
            st.rerun()

# ===========================================================================
# PAGE 3: REMEDIATION STUDIO
# ===========================================================================
elif st.session_state.active_page == "Remediation Studio":
    if rep is None:
        _render_html(
            """
<div class="cg-empty">
<div style="font-size: 2.5rem;">🛠️</div>
<h3>No Remediation Plan Generated Yet</h3>
<p>Scan a Python or Java file first to unlock one-click Full-File Automated Remediation, Git-style diffs, and per-finding fix cards.</p>
</div>
"""
        )
        c_mid = st.columns([1, 1, 1])[1]
        if c_mid.button("← Go to Code Scanner", type="primary", width="stretch"):
            st.session_state.active_page = "Code Scanner"
            st.rerun()
    else:
        rem_list = rep.get("remediation_plan") or []
        lang = str(rep.get("language", "python")).lower()
        fname = str(rep.get("filename", "snippet.py"))
        orig_code = st.session_state.submitted_code or st.session_state.editor_code or ""
        total_r = len(rem_list)

        approved_r = sum(
            1
            for r in rem_list
            if st.session_state.get(f"hitl_studio_{r.get('finding_id', 'ID')}", "Pending Review")
            in ("Approved & Applied", "Team Lead Approved")
        )
        pct_r = int((approved_r / total_r) * 100) if total_r > 0 else 100

        _render_html(
            f"""
<div class="cg-section-head">
<h2>AI Remediation Studio — {html.escape(fname)}</h2>
<p>Apply all fixes automatically with a Git-style diff &amp; interactive IDE editor, or review individual vulnerability cards with Human-in-the-Loop approval.</p>
</div>
"""
        )

        with st.container(border=True):
            fh1, fh2 = st.columns([2.2, 1.1])
            with fh1:
                st.markdown("#### ✨ Automated Full-File Fix Studio")
                st.caption(
                    "Generate a complete, optimized, runnable patched file resolving all security & code quality issues in one click."
                )
            with fh2:
                if st.button(
                    "✨ Fix Everything (Accept All Changes)",
                    type="primary",
                    width="stretch",
                    disabled=(total_r == 0),
                ):
                    with st.spinner("Generating complete optimized & hardened source file..."):
                        _execute_fix_all(rep, orig_code, backend_online)
                    st.rerun()

            if st.session_state.fixed_full_code:
                fixed_code = st.session_state.fixed_full_code
                diff_html, add_cnt, del_cnt = build_git_diff_html(orig_code, fixed_code, fname)

                s_col1, s_col2 = st.columns([1.8, 1])
                with s_col1:
                    _render_html(
                        f'<span class="gd-stat-add">+{add_cnt} additions</span>'
                        f'<span class="gd-stat-del">-{del_cnt} deletions</span>'
                        f'<span class="cg-tag">✓ {st.session_state.fixed_issues_count} issues addressed</span>'
                    )
                with s_col2:
                    view_mode = _pill_selector(
                        "Fix Studio Mode",
                        ["Git Diff View", "Editable Fixed Code"],
                        default="Git Diff View",
                    )

                if view_mode == "Git Diff View":
                    _render_html(diff_html)
                else:
                    edited = _render_ace_editor(
                        value=fixed_code,
                        language=lang,
                        height=430,
                        key=f"fixed_ace_s{st.session_state.scan_id}",
                    )
                    if edited != st.session_state.fixed_full_code:
                        st.session_state.fixed_full_code = edited

                dl_col1, dl_col2 = st.columns([1.5, 1])
                with dl_col1:
                    st.download_button(
                        f"⬇️ Download Clean Fixed Code ({st.session_state.fixed_filename})",
                        data=st.session_state.fixed_full_code,
                        file_name=st.session_state.fixed_filename,
                        mime="text/plain",
                        type="primary",
                        width="stretch",
                    )
                with dl_col2:
                    if st.button("🔄 Load Fixed Code into Scanner", width="stretch"):
                        _set_editor_content(
                            st.session_state.fixed_full_code,
                            st.session_state.fixed_filename,
                        )
                        st.session_state.active_page = "Code Scanner"
                        st.rerun()

        _render_html(
            f"""
<div class="cg-card">
<div class="cg-gauge-head">
<span>Human-in-the-Loop Remediation Approval Progress</span>
<span>{approved_r} / {total_r} Approved ({pct_r}%)</span>
</div>
<div class="cg-track"><div class="cg-fill" style="width:{pct_r}%; background:#10B981;"></div></div>
</div>
"""
        )

        cat_filter = _pill_selector(
            "Filter Remediation Category",
            [
                "All Categories",
                "Security Recommendation",
                "Code Quality Recommendation",
                "Performance Recommendation",
                "Maintainability Recommendation",
            ],
            default="All Categories",
        )

        filtered_rem = (
            rem_list
            if cat_filter == "All Categories"
            else [r for r in rem_list if r.get("recommendation_category") == cat_filter]
        )

        if not filtered_rem:
            st.success("No remediation items in this category.")
        for r in filtered_rem:
            fid = r.get("finding_id", "ID")
            cat_tag = CATEGORY_BADGE.get(r.get("recommendation_category", ""), "🛠️ Remediation")
            sev_tag = SEVERITY_ICON.get(r.get("severity", "Medium"), "🟡 MEDIUM")

            with st.container(border=True):
                h_col1, h_col2 = st.columns([2.5, 1])
                with h_col1:
                    st.markdown(f"#### {sev_tag} · `[{fid}]` {r.get('issue_title', '')}")
                    _render_html(
                        f'<span class="cg-tag">{html.escape(cat_tag)}</span> '
                        f'<span class="cg-tag-neutral">Standard: {html.escape(str(r.get("best_practice_guideline", "")))}</span> '
                        f'<span class="cg-tag-neutral">Line: {html.escape(str(r.get("line_reference", "")))}</span>'
                    )
                with h_col2:
                    options = [
                        "Pending Review",
                        "Approved & Applied",
                        "Team Lead Approved",
                        "Rejected (Intentional Business Logic)",
                    ]
                    key_name = f"hitl_studio_{fid}"
                    if key_name not in st.session_state:
                        st.session_state[key_name] = "Pending Review"
                    st.selectbox("Approval Status", options, key=key_name)

                st.markdown(f"**Root Cause:** {r.get('root_cause', '')}")
                if r.get("why_it_occurs"):
                    st.markdown(f"**Why It Occurs:** {r.get('why_it_occurs', '')}")
                st.markdown(f"**Actionable Fix Steps:** {r.get('fix_steps', '')}")

                diff_l, diff_r = st.columns(2, gap="medium")
                with diff_l:
                    st.markdown("❌ **Flagged Code**")
                    st.code(r.get("original_code") or "// See affected line in source file", language=lang)
                with diff_r:
                    st.markdown("✅ **Patched Secure Code**")
                    st.code(r.get("corrected_code", ""), language=lang)

# ===========================================================================
# PAGE 4: AI CODE ASSISTANT (CENTERED MODERN CHATBOT WORKSPACE)
# ===========================================================================
elif st.session_state.active_page == "AI Code Assistant":
    _, chat_col, _ = st.columns([0.14, 0.72, 0.14])

    with chat_col:
        _render_html(
            """
<div class="cg-section-head" style="text-align:center;">
<h2>RAG-Powered Conversational Code Assistant</h2>
<p>Ask follow-up questions about flagged vulnerabilities, refactoring, or OWASP Top 10 &amp; SEI CERT standards.</p>
</div>
"""
        )

        ctx_left, ctx_right = st.columns([3.8, 1.1])
        with ctx_left:
            if rep is not None:
                st.info(
                    f"🔗 Active Context: **{rep.get('filename', 'snippet')}** ({str(rep.get('language', 'python')).upper()}) — "
                    f"**{len(rep.get('unified_findings', []))} findings** loaded."
                )
            else:
                st.info("📚 General Secure Coding Mode — OWASP Top 10, CWE, Bandit, PMD & SEI CERT KB.")
        with ctx_right:
            if st.button("🧹 Clear Chat", width="stretch", disabled=(len(st.session_state.chat_history) == 0)):
                st.session_state.chat_history = []
                st.rerun()

        user_input = st.chat_input("Ask about your code, vulnerabilities, or how to fix an issue...")
        chosen_preset = None

        if not st.session_state.chat_history and not user_input:
            _render_html(
                """
<div class="cg-empty" style="padding: 34px 24px; margin: 12px 0 18px 0;">
<div style="font-size: 2.1rem;">💬</div>
<h3>How can I help harden your code?</h3>
<p>Type any question in the box below or choose a quick prompt to get RAG-grounded explanations and patched code examples.</p>
</div>
"""
            )
            preset_prompts = [
                "Explain this vulnerability.",
                "How do I fix SQL Injection?",
                "Why is duplicate code bad?",
                "Show secure coding practices.",
                "Explain this warning.",
                "Suggest better code.",
            ]
            q_cols = st.columns(3)
            for idx, pq in enumerate(preset_prompts):
                if q_cols[idx % 3].button(pq, key=f"chat_preset_{idx}", width="stretch"):
                    chosen_preset = pq

        for msg in st.session_state.chat_history:
            avatar = "👤" if msg["role"] == "user" else "🛡️"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        active_query = chosen_preset or user_input

        if active_query:
            st.session_state.chat_history.append({"role": "user", "content": active_query})
            with st.chat_message("user", avatar="👤"):
                st.markdown(active_query)

            with st.chat_message("assistant", avatar="🛡️"):
                with st.spinner("Searching OWASP Knowledge Base & generating response..."):
                    lang = rep.get("language", "python") if rep else "python"
                    findings_ctx = json.dumps((rep.get("unified_findings") or [])[:6]) if rep else ""
                    code_ctx = st.session_state.submitted_code or st.session_state.editor_code or ""
                    ans_data = None

                    if backend_online:
                        try:
                            c_resp = requests.post(
                                CHAT_URL,
                                json={
                                    "question": active_query,
                                    "language": lang,
                                    "code_context": code_ctx,
                                    "findings_context": findings_ctx,
                                    "chat_history": st.session_state.chat_history[:-1],
                                },
                                timeout=25,
                            )
                            if c_resp.status_code == 200:
                                ans_data = c_resp.json()
                        except Exception:
                            ans_data = None

                    if ans_data is None:
                        from src.agents import run_conversational_assistant

                        ans_data = run_conversational_assistant(
                            question=active_query,
                            language=lang,
                            code_context=code_ctx,
                            findings_context=findings_ctx,
                            chat_history=st.session_state.chat_history[:-1],
                        )

                    sources_str = ", ".join(ans_data.get("sources") or ["OWASP Knowledge Base"])
                    reply_md = (
                        f"{ans_data.get('answer', '')}\n\n"
                        f"---\n*🎯 Intent: `{ans_data.get('intent', 'General')}` · "
                        f"📚 Grounded RAG Sources: `{sources_str}`*"
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": reply_md})
            st.rerun()

# ===========================================================================
# PAGE 5: REPORTS & AUDIT HISTORY
# ===========================================================================
elif st.session_state.active_page == "Reports & History":
    _render_html(
        """
<div class="cg-section-head">
<h2>Executive Security Reports &amp; Review History</h2>
<p>Download publication-grade PDF monographs, self-contained HTML reports with embedded charts, Markdown PR summaries, or JSON payloads.</p>
</div>
"""
    )

    if rep is not None:
        with st.spinner("Preparing visual executive reports..."):
            _ensure_cached_exports(rep)

        base_fname = Path(rep.get("filename", "code_review")).stem

        e1, e2, e3, e4 = st.columns(4, gap="medium")
        with e1:
            with st.container(border=True):
                st.markdown("#### 📕 Executive PDF Report")
                st.caption("Research-grade multi-page PDF with embedded charts, compliance matrix & patched code.")
                st.download_button(
                    "Download PDF (.pdf)",
                    data=st.session_state.cached_pdf_report,
                    file_name=f"{base_fname}_security_report.pdf",
                    mime="application/pdf",
                    type="primary",
                    width="stretch",
                )
        with e2:
            with st.container(border=True):
                st.markdown("#### 🌐 Interactive HTML Report")
                st.caption("Self-contained technical monograph with high-DPI charts & 1-click Print-to-PDF.")
                st.download_button(
                    "Download HTML (.html)",
                    data=st.session_state.cached_html_report,
                    file_name=f"{base_fname}_executive_report.html",
                    mime="text/html",
                    width="stretch",
                )
        with e3:
            with st.container(border=True):
                st.markdown("#### 📄 Markdown PR Report")
                st.caption("Clean Pull Request summary ready for GitHub, GitLab, or documentation wikis.")
                st.download_button(
                    "Download Markdown (.md)",
                    data=st.session_state.cached_md_report,
                    file_name=f"{base_fname}_security_report.md",
                    mime="text/markdown",
                    width="stretch",
                )
        with e4:
            with st.container(border=True):
                st.markdown("#### 📦 Structured JSON")
                st.caption("Complete machine-readable scan payload for CI/CD security gates & archiving.")
                st.download_button(
                    "Download JSON (.json)",
                    data=st.session_state.cached_json_report,
                    file_name=f"{base_fname}_security_report.json",
                    mime="application/json",
                    width="stretch",
                )

        with st.expander("👁️ Live Preview — Executive HTML Audit Report", expanded=False):
            st.components.v1.html(
                st.session_state.cached_html_report, height=680, scrolling=True
            )
    else:
        st.info("Run a code scan in the **Code Scanner** tab first to generate executive PDF, HTML, Markdown, and JSON reports.")

    st.markdown("---")
    st.markdown("#### 🗄️ SQLite Historical Audit Log (`data/reviews.db`)")
    history_rows = get_recent_reviews(limit=20)
    if history_rows:
        st.dataframe(history_rows, width="stretch", hide_index=True)
    else:
        st.info("No historical reviews recorded in SQLite yet.")
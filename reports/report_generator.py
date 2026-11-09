from datetime import datetime
from typing import Dict, Any


def generate_full_markdown_report(report: Dict[str, Any]) -> str:
    qa = report.get("quality_assessment", {})
    cm = report.get("complexity_metrics", {})
    sev = report.get("severity_breakdown", {})
    sec_list = report.get("security_findings", [])
    qual_list = report.get("quality_findings", [])
    rem_list = report.get("remediation_plan", [])
    lang = report.get("language", "python")

    md = [
        "# 🛡️ AI Code Review & Security Analysis Report",
        "",
        "## 1. Project Information",
        f"- **Source File:** `{report.get('filename', 'snippet')}`",
        f"- **Detected Language:** `{lang.upper()}`",
        f"- **Generated Timestamp:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- **Overall Code Health Score:** `{qa.get('code_health_score', 0)}/100`",
        "",
        "## 2. Code Quality Summary",
        f"- **Maintainability Score:** `{qa.get('maintainability_score', 0)}/100`",
        f"- **Complexity Health Score:** `{qa.get('complexity_score', 0)}/100`",
        f"- **Cyclomatic Complexity:** `{cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})`",
        f"- **Cognitive Complexity:** `{cm.get('cognitive_complexity', 0)}`",
        f"- **Estimated Time / Space Complexity:** `{cm.get('time_complexity', 'O(1)')}` / `{cm.get('space_complexity', 'O(1)')}`",
        f"- **Code Duplication:** `{qa.get('duplication_percentage', 0)}%`",
        f"- **Documentation Coverage:** `{qa.get('documentation_score', 0)}%`",
        f"- **Estimated Technical Debt:** `{qa.get('technical_debt_minutes', 0)} mins`",
        "",
        "## 3. Security Vulnerability Summary (OWASP & SAST)",
    ]

    if not sec_list:
        md.append("- No OWASP security vulnerabilities detected.")
    else:
        for s in sec_list:
            md.append(
                f"### [{s['severity']}] {s['id']}: {s['vulnerability_name']} ({s['line_reference']})\n"
                f"- **Standard / Rule:** `{s.get('owasp_category') or s.get('tool_or_standard', '')}`\n"
                f"- **Risk Description:** {s['description']}\n"
                f"- **Recommendation:** {s['recommendation']}\n"
            )

    md.append("## 4. Code Smell & Design Anti-Pattern Summary")
    if not qual_list:
        md.append("- No code smells or design anti-patterns detected.")
    else:
        for q in qual_list:
            md.append(
                f"### [{q['severity']}] {q['id']}: {q['vulnerability_name']} ({q['line_reference']})\n"
                f"- **Category:** `{q.get('sub_category', 'Code Smell')}` (`{q.get('tool_or_standard', '')}`)\n"
                f"- **Description:** {q['description']}\n"
                f"- **Recommendation:** {q['recommendation']}\n"
            )

    md.extend([
        "## 5. Severity Levels Breakdown",
        f"- **Critical (Immediate action required):** {sev.get('Critical', 0)}",
        f"- **High (Fix before release):** {sev.get('High', 0)}",
        f"- **Medium (Address in next sprint):** {sev.get('Medium', 0)}",
        f"- **Low (Minor impact):** {sev.get('Low', 0)}",
        f"- **Informational (Best practice suggestion):** {sev.get('Informational', 0)}",
        "",
        "## 6. AI Remediation Plan & Corrected Code Examples",
    ])

    if not rem_list:
        md.append("- No remediations required.")
    else:
        for r in rem_list:
            md.append(
                f"### Fix for `{r['finding_id']}`: {r['issue_title']} ({r['recommendation_category']})\n"
                f"- **Root Cause:** {r['root_cause']}\n"
                f"- **Standard Reference:** `{r['best_practice_guideline']}`\n"
                f"- **Actionable Fix Steps:** {r['fix_steps']}\n"
                f"```{lang}\n{r['corrected_code']}\n```\n"
            )

    md.extend([
        "## 7. Pull Request Review Summary",
        report.get("pr_summary_markdown", ""),
    ])

    return "\n".join(md)
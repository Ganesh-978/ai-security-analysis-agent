import base64
import html
import io
import math
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Informational"]
SEVERITY_COLORS = {
    "Critical": "#DC2626",
    "High": "#EA580C",
    "Medium": "#CA8A04",
    "Low": "#2563EB",
    "Informational": "#64748B",
}
SEVERITY_RGB = {
    "Critical": (220, 38, 38),
    "High": (234, 88, 12),
    "Medium": (202, 138, 4),
    "Low": (37, 99, 235),
    "Informational": (100, 116, 139),
}
SEVERITY_EFFORT = {
    "Critical": "30 min (P0)",
    "High": "20 min (P1)",
    "Medium": "10 min (P2)",
    "Low": "5 min (P3)",
    "Informational": "2 min (Info)",
}


def compute_grade_and_verdict(health_score: float, sev: Dict[str, int]) -> Dict[str, Any]:
    crit = int(sev.get("Critical", 0))
    high = int(sev.get("High", 0))
    if crit > 0 or health_score < 45:
        return {
            "grade": "F",
            "color": "#DC2626",
            "rgb": (220, 38, 38),
            "verdict": "BLOCK RELEASE - Critical Security or Architectural Defects Detected",
        }
    if high > 0 or health_score < 60:
        return {
            "grade": "D",
            "color": "#EA580C",
            "rgb": (234, 88, 12),
            "verdict": "CHANGES REQUESTED - High-Severity Findings Require Remediation",
        }
    if health_score < 75:
        return {
            "grade": "C",
            "color": "#CA8A04",
            "rgb": (202, 138, 4),
            "verdict": "CONDITIONAL APPROVAL - Remediate Medium Findings Prior to Release",
        }
    if health_score < 88:
        return {
            "grade": "B",
            "color": "#2563EB",
            "rgb": (37, 99, 235),
            "verdict": "APPROVED WITH MINOR RECOMMENDATIONS",
        }
    return {
        "grade": "A",
        "color": "#059669",
        "rgb": (5, 150, 105),
        "verdict": "APPROVED - Compliant with OWASP Top 10 & Clean Code Benchmarks",
    }


def _compute_radar_scores_local(report: Dict[str, Any]) -> Dict[str, float]:
    qa = report.get("quality_assessment") or {}
    sev = report.get("severity_breakdown") or {}

    maint = round(max(0.0, min(100.0, float(qa.get("maintainability_score", 0.0)))), 1)
    comp = round(max(0.0, min(100.0, float(qa.get("complexity_score", 0.0)))), 1)
    doc = round(max(0.0, min(100.0, float(qa.get("documentation_score", 0.0)))), 1)
    dup_hygiene = round(
        max(0.0, min(100.0, 100.0 - float(qa.get("duplication_percentage", 0.0)))), 1
    )
    sec_penalty = (
        int(sev.get("Critical", 0)) * 18.0
        + int(sev.get("High", 0)) * 10.0
        + int(sev.get("Medium", 0)) * 4.0
        + int(sev.get("Low", 0)) * 1.5
    )
    sec_posture = round(max(5.0, min(100.0, 100.0 - sec_penalty)), 1)

    return {
        "Maintainability\nIndex": maint,
        "Complexity\nHealth": comp,
        "Documentation\nCoverage": doc,
        "Duplication\nHygiene": dup_hygiene,
        "Security\nPosture": sec_posture,
    }


def _evaluate_secure_coding_checklist(report: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    findings = report.get("unified_findings") or []
    blob = " ".join(
        f"{f.get('vulnerability_name', '')} {f.get('owasp_category', '')} {f.get('description', '')}"
        for f in findings
    ).lower()

    checks = [
        ("Parameterized SQL Queries", "sql" in blob or "cwe-89" in blob, "OWASP A03 / CWE-89"),
        ("Input Validation & Sanitization", any(k in blob for k in ("command", "eval", "xss", "path traversal", "cwe-78", "cwe-79")), "OWASP A03 / CWE-20"),
        ("Secrets & Credential Hygiene", any(k in blob for k in ("hardcoded", "secret", "password", "cwe-798")), "OWASP A02 & A07 / CWE-798"),
        ("Strong Cryptography & Hashing", any(k in blob for k in ("md5", "sha1", "crypto", "prng", "random", "cwe-327", "cwe-328")), "OWASP A02 / CWE-327"),
        ("Secure Error Handling & Logging", any(k in blob for k in ("swallowed", "empty catch", "bare except", "error handling", "cwe-390")), "OWASP A09 / CWE-390"),
        ("Clean Architecture & Modularity", any(k in blob for k in ("spaghetti", "nesting", "god object", "complexity", "resource")), "ISO/IEC 25010 / Clean Code"),
    ]

    return [(name, "NON-COMPLIANT" if failed else "PASS", std) for name, failed, std in checks]


def _render_radar_png_bytes(report: Dict[str, Any]) -> Tuple[Optional[bytes], float]:
    """Renders a crisp, unclipped 5-axis Pentagon Radar Chart with generous top/side margins."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        scores = _compute_radar_scores_local(report)
        labels = list(scores.keys())
        values = list(scores.values())
        n = len(labels)
        angles = [math.pi / 2 - (2 * math.pi * i / n) for i in range(n)]

        fig, ax = plt.subplots(figsize=(5.6, 4.35), dpi=220)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        ax.set_aspect("equal")
        ax.axis("off")

        for level in [20, 40, 60, 80, 100]:
            xs = [level * math.cos(a) for a in angles] + [level * math.cos(angles[0])]
            ys = [level * math.sin(a) for a in angles] + [level * math.sin(angles[0])]
            ax.plot(xs, ys, color="#CBD5E1", linewidth=0.9, zorder=1)
            ax.text(4, level - 2, str(level), fontsize=7.5, color="#64748B", ha="left", va="top")

        for idx, (a, lbl, val) in enumerate(zip(angles, labels, values)):
            ax.plot([0, 100 * math.cos(a)], [0, 100 * math.sin(a)], color="#CBD5E1", linewidth=0.9, zorder=1)
            if idx == 0:
                lx, ly = 0, 134
            elif idx in (1, 4):
                lx, ly = 142 * math.cos(a), 124 * math.sin(a)
            else:
                lx, ly = 132 * math.cos(a), 128 * math.sin(a)
            ax.text(
                lx,
                ly,
                f"{lbl}\n({val:.0f}/100)",
                fontsize=8.2,
                fontweight="bold",
                color="#0F172A",
                ha="center",
                va="center",
            )

        px = [v * math.cos(a) for v, a in zip(values, angles)]
        py = [v * math.sin(a) for v, a in zip(values, angles)]
        ax.fill(px + [px[0]], py + [py[0]], color="#2563EB", alpha=0.20, zorder=2)
        ax.plot(px + [px[0]], py + [py[0]], color="#1D4ED8", linewidth=2.2, zorder=3)
        ax.scatter(px, py, color="#1E40AF", s=36, edgecolors="#FFFFFF", linewidths=1.3, zorder=4)

        ax.set_xlim(-195, 195)
        ax.set_ylim(-168, 186)
        ax.set_title("Figure 1: 5-Axis Quality & Security Posture", fontsize=10, fontweight="bold", color="#0F172A", pad=10)
        plt.tight_layout(pad=0.45)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=220, facecolor="#FFFFFF")
        plt.close(fig)
        return buf.getvalue(), (4.35 / 5.6)
    except Exception:
        return None, 0.78


def _render_severity_png_bytes(report: Dict[str, Any]) -> Tuple[Optional[bytes], float]:
    """Renders a crisp, color-coded Horizontal Severity Chart matching Figure 1 aspect ratio."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        sev = report.get("severity_breakdown") or {}
        labels = list(reversed(SEVERITY_ORDER))
        counts = [int(sev.get(lvl, 0)) for lvl in labels]
        colors = [SEVERITY_COLORS[lvl] for lvl in labels]
        max_val = max(counts) if counts else 0

        fig, ax = plt.subplots(figsize=(5.6, 4.35), dpi=220)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        bars = ax.barh(labels, counts, color=colors, height=0.52, edgecolor="none")
        for bar, cnt in zip(bars, counts):
            ax.text(
                bar.get_width() + max(0.16, max_val * 0.03),
                bar.get_y() + bar.get_height() / 2,
                str(cnt),
                va="center",
                ha="left",
                fontsize=10.5,
                fontweight="bold",
                color="#0F172A",
            )

        ax.set_xlim(0, max(max_val + 1.8, 5))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#CBD5E1")
        ax.spines["bottom"].set_color("#CBD5E1")
        ax.xaxis.grid(True, linestyle="--", alpha=0.55, color="#CBD5E1")
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", labelsize=9.5, colors="#0F172A")
        ax.tick_params(axis="x", labelsize=8.5, colors="#64748B")
        ax.set_xlabel("Detected Findings Count", fontsize=9, fontweight="bold", color="#334155")
        ax.set_title("Figure 2: Severity Distribution Profile", fontsize=10, fontweight="bold", color="#0F172A", pad=12)
        plt.tight_layout(pad=0.65)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=220, facecolor="#FFFFFF")
        plt.close(fig)
        return buf.getvalue(), (4.35 / 5.6)
    except Exception:
        return None, 0.78


def _b64_img_tag(png_bytes: Optional[bytes], alt: str) -> str:
    if not png_bytes:
        return f'<div style="padding:24px;text-align:center;color:#64748B;">{html.escape(alt)} unavailable</div>'
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f'<img src="data:image/png;base64,{b64}" alt="{html.escape(alt)}" class="chart-img" />'


def generate_executive_html_report(report: Dict[str, Any]) -> str:
    """Produces a publication-grade Technical Security & Quality Audit Report in HTML."""
    qa = report.get("quality_assessment") or {}
    cm = report.get("complexity_metrics") or {}
    sev = report.get("severity_breakdown") or {}
    sv = report.get("syntax_validation") or {}
    unified = report.get("unified_findings") or []
    sec_list = report.get("security_findings") or []
    qual_list = report.get("quality_findings") or []
    rem_list = report.get("remediation_plan") or []
    rem_map = {r.get("finding_id"): r for r in rem_list}
    compliance_rows = _evaluate_secure_coding_checklist(report)

    filename = str(report.get("filename", "snippet"))
    lang = str(report.get("language", "python")).upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_id = f"CG-AUD-{datetime.now().strftime('%Y%m%d-%H%M')}"
    health_score = float(qa.get("code_health_score", 0.0))
    tech_debt = int(qa.get("technical_debt_minutes", 0))
    grade_info = compute_grade_and_verdict(health_score, sev)

    radar_bytes, _ = _render_radar_png_bytes(report)
    sev_bytes, _ = _render_severity_png_bytes(report)
    radar_img = _b64_img_tag(radar_bytes, "5-Axis Pentagon Quality & Security Radar")
    sev_img = _b64_img_tag(sev_bytes, "Color-Coded Severity Distribution Chart")

    comp_html_rows = []
    for ctrl, status, std in compliance_rows:
        pill_bg = "#059669" if status == "PASS" else "#DC2626"
        comp_html_rows.append(
            f'<tr><td><strong>{html.escape(ctrl)}</strong></td>'
            f'<td><span class="sev-pill" style="background:{pill_bg};">{status}</span></td>'
            f'<td><code>{html.escape(std)}</code></td></tr>'
        )

    matrix_rows: List[str] = []
    for item in unified:
        s_lvl = str(item.get("severity", "Medium"))
        s_col = SEVERITY_COLORS.get(s_lvl, "#64748B")
        rule = str(item.get("owasp_category") or item.get("tool_or_standard", "Standard"))
        effort = SEVERITY_EFFORT.get(s_lvl, "10 min")
        matrix_rows.append(
            "<tr>"
            f'<td><span class="sev-pill" style="background:{s_col};">{html.escape(s_lvl)}</span></td>'
            f'<td><strong>{html.escape(str(item.get("id", "")))}</strong></td>'
            f'<td>{html.escape(str(item.get("vulnerability_name") or item.get("title", "")))}</td>'
            f'<td><code>{html.escape(rule)}</code></td>'
            f'<td>{html.escape(str(item.get("sub_category", item.get("agent_source", ""))))}</td>'
            f'<td>{html.escape(str(item.get("line_reference", "N/A")))}</td>'
            f'<td>{html.escape(effort)}</td>'
            "</tr>"
        )
    if not matrix_rows:
        matrix_rows.append(
            '<tr><td colspan="7" style="text-align:center;color:#059669;font-weight:700;padding:16px;">Zero security vulnerabilities or code quality defects detected. Artifact meets production release criteria.</td></tr>'
        )

    deep_cards: List[str] = []
    for idx, item in enumerate(unified, start=1):
        fid = str(item.get("id", f"F-{idx:02d}"))
        rem = rem_map.get(fid, {})
        s_lvl = str(item.get("severity", "Medium"))
        s_col = SEVERITY_COLORS.get(s_lvl, "#64748B")
        v_name = str(item.get("vulnerability_name") or item.get("title", "Issue"))
        root_cause = str(rem.get("root_cause") or item.get("description", ""))
        impact = str(item.get("description", ""))
        fix_steps = str(rem.get("fix_steps") or item.get("recommendation", ""))
        orig_code = str(rem.get("original_code") or item.get("code_snippet") or "// See affected line in source file")
        fixed_code = str(rem.get("corrected_code") or item.get("secure_code_suggestion") or "// Apply secure coding guideline")
        std_ref = str(rem.get("best_practice_guideline") or item.get("owasp_category") or item.get("tool_or_standard", ""))
        rec_cat = str(rem.get("recommendation_category") or "Security Recommendation")
        verification = (
            f"Re-execute AST/SAST verification and regression unit tests on {item.get('line_reference', 'modified lines')} "
            f"to confirm elimination of {v_name} and compliance with {std_ref}."
        )

        deep_cards.append(
            f'<div class="finding-card" style="border-left:5px solid {s_col};">'
            '<div class="finding-head">'
            f'<div><span class="sev-pill" style="background:{s_col};">{html.escape(s_lvl)}</span> '
            f'<span class="fid-title">5.{idx} [{html.escape(fid)}] {html.escape(v_name)}</span></div>'
            f'<div class="finding-meta">{html.escape(rec_cat)} · {html.escape(str(item.get("line_reference", "")))}</div>'
            "</div>"
            '<ul class="detail-bullets">'
            f'<li><strong>Mapped Standard &amp; Detection Source:</strong> <code>{html.escape(std_ref)}</code> ({html.escape(str(item.get("agent_source", "Agent")))})</li>'
            f'<li><strong>Root Cause Analysis:</strong> {html.escape(root_cause)}</li>'
            f'<li><strong>Security / Maintainability Impact:</strong> {html.escape(impact)}</li>'
            f'<li><strong>Remediation Protocol:</strong> {html.escape(fix_steps)}</li>'
            "</ul>"
            '<div class="code-compare">'
            f'<div><div class="code-lbl bad">Flagged Source Pattern</div><pre><code>{html.escape(orig_code)}</code></pre></div>'
            f'<div><div class="code-lbl good">Verified Secure Implementation</div><pre><code>{html.escape(fixed_code)}</code></pre></div>'
            "</div>"
            f'<div class="verify-box"><strong>Verification Criterion:</strong> {html.escape(verification)}</div>'
            "</div>"
        )

    p0_items = [f"[{i.get('id')}] {i.get('vulnerability_name')} ({i.get('line_reference')})" for i in unified if i.get("severity") == "Critical"]
    p1_items = [f"[{i.get('id')}] {i.get('vulnerability_name')} ({i.get('line_reference')})" for i in unified if i.get("severity") == "High"]
    p2_items = [f"[{i.get('id')}] {i.get('vulnerability_name')} ({i.get('line_reference')})" for i in unified if i.get("severity") in ("Medium", "Low", "Informational")]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Code Review & Security Analysis Agent Technical Audit Report - {html.escape(filename)}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Merriweather:wght@700;900&family=JetBrains+Mono:wght@400;500&display=swap');
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 32px; background: #F1F5F9; color: #0F172A; line-height: 1.62; }}
  .paper {{ max-width: 1080px; margin: 0 auto; background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 14px; padding: 40px 46px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06); }}
  .doc-header {{ border-bottom: 3px solid #1D4ED8; padding-bottom: 20px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px; }}
  .doc-kicker {{ font-size: 0.74rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: #1D4ED8; margin-bottom: 6px; }}
  .doc-title {{ font-family: 'Merriweather', Georgia, serif; font-size: 1.68rem; font-weight: 900; color: #0F172A; margin: 0 0 8px 0; line-height: 1.25; }}
  .doc-meta {{ font-size: 0.84rem; color: #475569; }}
  .grade-panel {{ display: flex; align-items: center; gap: 16px; background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 12px; padding: 12px 18px; }}
  .grade-badge {{ font-size: 2.1rem; font-weight: 800; color: #FFFFFF; background: {grade_info['color']}; width: 56px; height: 56px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }}
  .abstract-box {{ background: #EFF6FF; border: 1px solid #BFDBFE; border-left: 5px solid #1D4ED8; border-radius: 10px; padding: 16px 20px; margin-bottom: 24px; }}
  .abstract-title {{ font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: #1E40AF; margin-bottom: 6px; }}
  .verdict-strip {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 5px solid {grade_info['color']}; border-radius: 10px; padding: 12px 18px; margin-bottom: 24px; font-weight: 700; color: #0F172A; }}
  .print-btn {{ background: #2563EB; color: #FFFFFF; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.84rem; }}
  .sec-heading {{ font-family: 'Merriweather', Georgia, serif; font-size: 1.18rem; font-weight: 700; color: #0F172A; margin: 28px 0 12px 0; padding-bottom: 6px; border-bottom: 1.5px solid #E2E8F0; }}
  .sec-num {{ color: #1D4ED8; margin-right: 6px; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }}
  .kpi-box {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-top: 3px solid #2563EB; border-radius: 10px; padding: 14px 16px; }}
  .kpi-lbl {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; font-weight: 700; }}
  .kpi-val {{ font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-top: 4px; }}
  .kpi-sub {{ font-size: 0.76rem; color: #64748B; margin-top: 2px; }}
  .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 18px; }}
  .chart-card {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; text-align: center; }}
  .chart-img {{ width: 100%; height: auto; display: block; border-radius: 6px; }}
  .chart-caption {{ font-size: 0.78rem; color: #64748B; margin-top: 8px; font-style: italic; }}
  table {{ width: 100%; border-collapse: collapse; margin: 12px 0 22px 0; font-size: 0.84rem; border: 1px solid #CBD5E1; }}
  th {{ background: #0F172A; color: #F8FAFC; text-align: left; padding: 10px 12px; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; }}
  td {{ padding: 10px 12px; border-top: 1px solid #E2E8F0; vertical-align: top; }}
  tbody tr:nth-child(even) {{ background: #F8FAFC; }}
  .sev-pill {{ display: inline-block; padding: 2px 10px; border-radius: 999px; color: #FFFFFF; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }}
  .finding-card {{ background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 18px 20px; margin-bottom: 18px; page-break-inside: avoid; }}
  .finding-head {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid #F1F5F9; }}
  .fid-title {{ font-size: 1.0rem; font-weight: 700; color: #0F172A; margin-left: 6px; }}
  .finding-meta {{ font-size: 0.78rem; font-weight: 600; color: #475569; }}
  .detail-bullets {{ margin: 8px 0 12px 0; padding-left: 20px; font-size: 0.88rem; color: #1E293B; }}
  .detail-bullets li {{ margin-bottom: 6px; }}
  .code-compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 12px 0; }}
  .code-lbl {{ font-size: 0.74rem; font-weight: 700; text-transform: uppercase; padding: 6px 12px; border-radius: 6px 6px 0 0; }}
  .code-lbl.bad {{ background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; border-bottom: none; }}
  .code-lbl.good {{ background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; border-bottom: none; }}
  pre {{ margin: 0; padding: 12px 14px; background: #0F172A; color: #F1F5F9; border-radius: 0 0 6px 6px; overflow-x: auto; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.78rem; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }}
  .verify-box {{ background: #EFF6FF; border: 1px solid #BFDBFE; color: #1E3A8A; border-radius: 8px; padding: 9px 14px; font-size: 0.82rem; margin-top: 8px; }}
  .method-list {{ margin: 8px 0 16px 0; padding-left: 20px; font-size: 0.88rem; color: #1E293B; }}
  .method-list li {{ margin-bottom: 6px; }}
  .ref-list {{ font-size: 0.82rem; color: #475569; padding-left: 20px; }}
  .ref-list li {{ margin-bottom: 5px; }}
  .doc-footer {{ margin-top: 32px; padding-top: 14px; border-top: 1px solid #CBD5E1; font-size: 0.76rem; color: #64748B; display: flex; justify-content: space-between; flex-wrap: wrap; }}
  @media print {{
    body {{ background: #FFFFFF; padding: 0; }}
    .paper {{ border: none; box-shadow: none; padding: 0; max-width: 100%; }}
    .no-print {{ display: none !important; }}
    th, .sev-pill, .grade-badge, .abstract-box {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
</style>
</head>
<body>
<div class="paper">
  <div class="doc-header">
    <div>
      <div class="doc-kicker">AI Code Review & Security Analysis Agent · Automated Security &amp; Software Quality Technical Monograph</div>
      <h1 class="doc-title">Static Security &amp; Code Quality Audit Report</h1>
      <div class="doc-meta">
        <strong>Document ID:</strong> {report_id} &nbsp;|&nbsp;
        <strong>Target Artifact:</strong> <code>{html.escape(filename)}</code> ({html.escape(lang)}) &nbsp;|&nbsp;
        <strong>Timestamp:</strong> {html.escape(timestamp)}
      </div>
    </div>
    <div class="grade-panel">
      <div class="grade-badge">{grade_info['grade']}</div>
      <div>
        <div style="font-size:0.72rem;text-transform:uppercase;color:#64748B;font-weight:700;">Composite Health</div>
        <div style="font-size:1.45rem;font-weight:800;color:#0F172A;">{health_score}/100</div>
      </div>
    </div>
  </div>

  <div class="abstract-box">
    <div class="abstract-title">Executive Abstract</div>
    This automated audit evaluates <code>{html.escape(filename)}</code> using AI Code Review & Security Analysis Agent's 6-layer multi-agent architecture combining Abstract Syntax Tree (AST/Tree-sitter) parsing, deterministic Static Application Security Testing (SAST), Retrieval-Augmented Generation (RAG) over OWASP Top 10, CWE, Bandit, PMD, SpotBugs, and SEI CERT knowledge bases, and parallel LLM reasoning. Across the evaluated artifact, <strong>{len(unified)} total findings</strong> were identified (<strong>{len(sec_list)} security vulnerabilities</strong> and <strong>{len(qual_list)} code quality/design smells</strong>), yielding a composite Code Health Score of <strong>{health_score}/100 (Grade {grade_info['grade']})</strong> and an estimated remediation effort of <strong>{tech_debt} minutes</strong>.
  </div>

  <div class="verdict-strip">
    <span>Release Gate Verdict: {html.escape(grade_info['verdict'])}</span>
    <button class="print-btn no-print" onclick="window.print()">🖨️ Print / Export Clean PDF</button>
  </div>

  <h2 class="sec-heading"><span class="sec-num">1.</span>Visual Analytics Snapshot</h2>
  <div class="charts-grid">
    <div class="chart-card">{radar_img}<div class="chart-caption">5-axis linear pentagon radar mapping Maintainability, Complexity Health, Documentation, Duplication Hygiene, and Security Posture.</div></div>
    <div class="chart-card">{sev_img}<div class="chart-caption">Distribution of unified findings across the 5-tier enterprise severity pyramid (Critical to Informational).</div></div>
  </div>

  <h2 class="sec-heading"><span class="sec-num">2.</span>Complexity Telemetry &amp; Secure Coding Compliance</h2>
  <div class="kpi-grid">
    <div class="kpi-box"><div class="kpi-lbl">Code Health Score</div><div class="kpi-val" style="color:{grade_info['color']};">{health_score}/100</div><div class="kpi-sub">Security Grade: {grade_info['grade']}</div></div>
    <div class="kpi-box"><div class="kpi-lbl">Security Findings</div><div class="kpi-val">{len(sec_list)}</div><div class="kpi-sub">{int(sev.get('Critical', 0))} Critical · {int(sev.get('High', 0))} High</div></div>
    <div class="kpi-box"><div class="kpi-lbl">Code Quality Smells</div><div class="kpi-val">{len(qual_list)}</div><div class="kpi-sub">Maintainability: {qa.get('maintainability_score', 0)}/100</div></div>
    <div class="kpi-box"><div class="kpi-lbl">Estimated Tech Debt</div><div class="kpi-val">{tech_debt} min</div><div class="kpi-sub">Documentation: {qa.get('documentation_score', 0)}%</div></div>
  </div>

  <table>
    <thead>
      <tr><th>Metric Dimension</th><th>Measured Value</th><th>Engineering Benchmark / Standard</th><th>Interpretation</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>McCabe Cyclomatic Complexity</strong></td><td>{cm.get('cyclomatic_complexity', 1)} ({html.escape(str(cm.get('cyclomatic_rank', 'A')))})</td><td>&le; 5 (Rank A - Low Risk)</td><td>Measures independent control-flow decision paths per function/method.</td></tr>
      <tr><td><strong>Cognitive Complexity</strong></td><td>{cm.get('cognitive_complexity', 0)}</td><td>&le; 8 (High Readability)</td><td>Quantifies human comprehension overhead with nesting depth penalties.</td></tr>
      <tr><td><strong>Asymptotic Time / Space</strong></td><td>{html.escape(str(cm.get('time_complexity', 'O(1)')))} / {html.escape(str(cm.get('space_complexity', 'O(1)')))}</td><td>O(1) to O(n) preferred</td><td>Estimated execution and memory scaling relative to input size.</td></tr>
      <tr><td><strong>Maintainability Index</strong></td><td>{qa.get('maintainability_score', 0)} / 100</td><td>&ge; 80 / 100 (ISO/IEC 25010)</td><td>Composite health factoring complexity, duplication, size, and documentation.</td></tr>
      <tr><td><strong>Duplication &amp; Documentation</strong></td><td>{qa.get('duplication_percentage', 0)}% dup · {qa.get('documentation_score', 0)}% doc</td><td>&lt; 5% dup · &ge; 60% docs</td><td>Indicates Copy-Paste Programming risk and inline maintainability clarity.</td></tr>
      <tr><td><strong>Syntax Verification Engine</strong></td><td>{html.escape(str(sv.get('parser_used', 'AST / Tree-sitter')))} ({sv.get('ast_node_count', 0)} nodes)</td><td>Zero syntax errors</td><td>Deterministic pre-agent AST gatekeeper verified source grammar.</td></tr>
    </tbody>
  </table>

  <table>
    <thead>
      <tr><th>Secure Coding Control</th><th>Compliance Status</th><th>Reference Standard</th></tr>
    </thead>
    <tbody>
      {''.join(comp_html_rows)}
    </tbody>
  </table>

  <h2 class="sec-heading"><span class="sec-num">3.</span>Multi-Agent Architecture &amp; Audit Methodology</h2>
  <ul class="method-list">
    <li><strong>Stage 1 — Syntax Gatekeeper &amp; Parsing:</strong> Automatic language detection followed by deterministic Python <code>ast</code> / <code>Tree-sitter</code> grammar verification prevents malformed code from consuming LLM inference cycles.</li>
    <li><strong>Stage 2 — Static Application Security Testing (SAST):</strong> In-memory pattern scanners evaluate OWASP Top 10 (A01–A10), CWE rules, Bandit/Pylint (Python), SpotBugs/PMD/Checkstyle/SEI CERT (Java), and design anti-patterns.</li>
    <li><strong>Stage 3 — Grounded RAG Retrieval:</strong> Security standards stored persistently in <strong>ChromaDB</strong> (embedded via local <code>sentence-transformers/all-MiniLM-L6-v2</code>) are queried via an in-memory <strong>FAISS</strong> index to ground agent reasoning.</li>
    <li><strong>Stage 4 — Parallel Multi-Agent Orchestration (LangGraph):</strong> The <em>Code Analysis Agent</em> and <em>Security Vulnerability Agent</em> execute concurrently, deduplicate overlapping alerts, and pass unified findings to the <em>AI Remediation Agent</em> and <em>PR Summary Generator</em>.</li>
  </ul>

  <h2 class="sec-heading"><span class="sec-num">4.</span>Prioritized Findings Inventory</h2>
  <table>
    <thead>
      <tr><th>Severity</th><th>ID</th><th>Issue / Vulnerability</th><th>Mapped OWASP / CWE / Tool Rule</th><th>Category</th><th>Line</th><th>Effort</th></tr>
    </thead>
    <tbody>
      {''.join(matrix_rows)}
    </tbody>
  </table>

  <h2 class="sec-heading"><span class="sec-num">5.</span>Detailed Technical Findings &amp; Remediation Analysis</h2>
  {''.join(deep_cards) if deep_cards else '<div class="abstract-box" style="background:#ECFDF5;border-color:#A7F3D0;border-left-color:#059669;"><strong>Clean Verification Result:</strong> No security vulnerabilities or code quality smells require remediation.</div>'}

  <h2 class="sec-heading"><span class="sec-num">6.</span>Phased Remediation Roadmap &amp; References</h2>
  <ul class="method-list">
    <li><strong>Phase P0 — Immediate Release Blockers (Critical):</strong> {html.escape(', '.join(p0_items)) if p0_items else 'None detected.'}</li>
    <li><strong>Phase P1 — Pre-Release Hardening (High):</strong> {html.escape(', '.join(p1_items)) if p1_items else 'None detected.'}</li>
    <li><strong>Phase P2 — Sprint Refactoring &amp; Hygiene (Medium / Low / Info):</strong> {html.escape(', '.join(p2_items)) if p2_items else 'None detected.'}</li>
  </ul>
  <ol class="ref-list">
    <li>OWASP Foundation, <em>OWASP Top 10 Web Application Security Risks (A01–A10)</em>, 2025 Standard.</li>
    <li>MITRE Corporation, <em>Common Weakness Enumeration (CWE Top 25 Software Weaknesses)</em>, 2025.</li>
    <li>Carnegie Mellon SEI, <em>SEI CERT Oracle Coding Standard for Java &amp; Secure Coding Guidelines</em>.</li>
    <li>McCabe, T. J., <em>A Complexity Measure</em>, IEEE Transactions on Software Engineering, and ISO/IEC 25010 Software Quality Model.</li>
    <li>Static Analysis Rulebooks: Python <em>Bandit</em> &amp; <em>Pylint/Radon</em>; Java <em>SpotBugs</em>, <em>PMD</em>, and <em>Checkstyle</em>.</li>
  </ol>

  <div class="doc-footer">
    <span>Generated by AI Code Review & Security Analysis Agent · Multi-Agent Security Analysis Platform</span>
    <span>Document ID: {report_id} · {html.escape(timestamp)}</span>
  </div>
</div>
</body>
</html>
"""


def _sanitize_pdf_text(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "—": "-",
        "–": "-",
        "•": "*",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "→": "->",
        "²": "^2",
        "≤": "<=",
        "≥": ">=",
        "·": "|",
        "\t": "    ",
    }
    out = str(text)
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out.encode("latin-1", errors="ignore").decode("latin-1")


def _wrap_text_to_width(pdf, text: str, max_w: float) -> List[str]:
    """Word-wraps text accurately to a given PDF column width (in mm) with zero truncation."""
    clean = _sanitize_pdf_text(text)
    if not clean:
        return [""]
    result: List[str] = []
    for raw_para in clean.splitlines():
        if not raw_para.strip():
            result.append("")
            continue
        words = raw_para.split(" ")
        curr = ""
        for word in words:
            while pdf.get_string_width(word) > max_w and len(word) > 1:
                cut = len(word) - 1
                while cut > 1 and pdf.get_string_width(word[:cut]) > max_w:
                    cut -= 1
                if curr:
                    result.append(curr)
                    curr = ""
                result.append(word[:cut])
                word = word[cut:]
            candidate = f"{curr} {word}".strip() if curr else word
            if pdf.get_string_width(candidate) <= max_w:
                curr = candidate
            else:
                if curr:
                    result.append(curr)
                curr = word
        if curr:
            result.append(curr)
    return result or [""]


def generate_full_markdown_report(report: Dict[str, Any]) -> str:
    qa = report.get("quality_assessment") or {}
    cm = report.get("complexity_metrics") or {}
    sev = report.get("severity_breakdown") or {}
    sec_list = report.get("security_findings") or []
    qual_list = report.get("quality_findings") or []
    rem_list = report.get("remediation_plan") or []
    lang = report.get("language", "python")
    grade_info = compute_grade_and_verdict(float(qa.get("code_health_score", 0.0)), sev)

    md = [
        "# AI Code Review & Security Analysis Agent — Technical Security & Code Quality Audit Report",
        "",
        "## 1. Executive Summary",
        f"- **Source File:** `{report.get('filename', 'snippet')}` ({lang.upper()})",
        f"- **Generated:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- **Composite Code Health Score:** `{qa.get('code_health_score', 0)}/100` (Security Grade: **{grade_info['grade']}**)",
        f"- **Release Gate Verdict:** {grade_info['verdict']}",
        "",
        "## 2. Complexity & ISO/IEC 25010 Quality Telemetry",
        f"- **Maintainability Index:** `{qa.get('maintainability_score', 0)}/100` | **Complexity Health:** `{qa.get('complexity_score', 0)}/100`",
        f"- **Documentation Coverage:** `{qa.get('documentation_score', 0)}%` | **Code Duplication:** `{qa.get('duplication_percentage', 0)}%`",
        f"- **McCabe Cyclomatic Complexity:** `{cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})` | **Cognitive Complexity:** `{cm.get('cognitive_complexity', 0)}`",
        f"- **Asymptotic Time / Space:** `{cm.get('time_complexity', 'O(1)')}` / `{cm.get('space_complexity', 'O(1)')}`",
        f"- **Estimated Technical Debt:** `{qa.get('technical_debt_minutes', 0)} minutes`",
        "",
        "## 3. Severity Distribution",
        f"- **Critical:** {sev.get('Critical', 0)} | **High:** {sev.get('High', 0)} | **Medium:** {sev.get('Medium', 0)} | **Low:** {sev.get('Low', 0)} | **Informational:** {sev.get('Informational', 0)}",
        "",
        "## 4. Security Vulnerabilities (OWASP & SAST)",
    ]

    if not sec_list:
        md.append("- No OWASP security vulnerabilities detected.")
    else:
        for s in sec_list:
            md.append(
                f"### [{s.get('severity', 'High')}] {s.get('id', 'SEC')}: {s.get('vulnerability_name', 'Vulnerability')} ({s.get('line_reference', 'N/A')})\n"
                f"- **Mapped Standard:** `{s.get('owasp_category') or s.get('tool_or_standard', '')}`\n"
                f"- **Impact Analysis:** {s.get('description', '')}\n"
                f"- **Recommendation:** {s.get('recommendation', '')}\n"
            )

    md.append("## 5. Code Quality & Design Smells")
    if not qual_list:
        md.append("- No code smells or design anti-patterns detected.")
    else:
        for q in qual_list:
            md.append(
                f"### [{q.get('severity', 'Medium')}] {q.get('id', 'QUAL')}: {q.get('vulnerability_name', 'Code Smell')} ({q.get('line_reference', 'N/A')})\n"
                f"- **Category:** `{q.get('sub_category', 'Code Smell')}` (`{q.get('tool_or_standard', '')}`)\n"
                f"- **Description:** {q.get('description', '')}\n"
                f"- **Recommendation:** {q.get('recommendation', '')}\n"
            )

    md.append("## 6. Prioritized Remediation Roadmap")
    if not rem_list:
        md.append("- No remediations required.")
    else:
        for r in rem_list:
            md.append(
                f"### Fix for `{r.get('finding_id', 'ID')}`: {r.get('issue_title', 'Issue')} ({r.get('recommendation_category', 'Remediation')})\n"
                f"- **Root Cause:** {r.get('root_cause', '')}\n"
                f"- **Standard:** `{r.get('best_practice_guideline', '')}`\n"
                f"- **Action Steps:** {r.get('fix_steps', '')}\n"
                f"```{lang}\n{r.get('corrected_code', '')}\n```\n"
            )

    return "\n".join(md)


def generate_pdf_report(report: Dict[str, Any]) -> bytes:
    """
    Generates a publication-grade PDF Technical Audit Report with auto-wrapping
    multi-line tables (zero truncation), unclipped high-DPI charts, aligned hanging-indent
    bullets, OWASP compliance matrix, and clean page breaks.
    """
    qa = report.get("quality_assessment") or {}
    cm = report.get("complexity_metrics") or {}
    sev = report.get("severity_breakdown") or {}
    sv = report.get("syntax_validation") or {}
    unified = report.get("unified_findings") or []
    sec_list = report.get("security_findings") or []
    qual_list = report.get("quality_findings") or []
    rem_list = report.get("remediation_plan") or []
    rem_map = {r.get("finding_id"): r for r in rem_list}
    compliance_rows = _evaluate_secure_coding_checklist(report)

    filename = str(report.get("filename", "snippet"))
    language = str(report.get("language", "python")).upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_id = f"CG-AUD-{datetime.now().strftime('%Y%m%d-%H%M')}"
    health_score = float(qa.get("code_health_score", 0.0))
    grade_info = compute_grade_and_verdict(health_score, sev)

    temp_files: List[Path] = []
    try:
        import fpdf as fpdf_mod
        from fpdf import FPDF

        class ResearchAuditPDF(FPDF):
            def header(self):
                if self.page_no() == 1:
                    return
                self.set_font("Helvetica", "B", 8)
                self.set_text_color(71, 85, 105)
                self.cell(
                    0,
                    5.5,
                    _sanitize_pdf_text(
                        f"AI Code Review & Security Analysis Agent Technical Security & Quality Audit  |  {filename} ({language})"
                    ),
                    align="L",
                )
                self.ln(5.5)
                self.set_draw_color(203, 213, 225)
                self.set_line_width(0.3)
                self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
                self.ln(4.5)

            def footer(self):
                self.set_y(-13)
                self.set_draw_color(203, 213, 225)
                self.set_line_width(0.3)
                self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
                self.ln(2)
                self.set_font("Helvetica", "", 8)
                self.set_text_color(100, 116, 139)
                self.cell(
                    0,
                    5.5,
                    _sanitize_pdf_text(
                        f"Document ID: {report_id}  |  Generated: {timestamp}  |  Page {self.page_no()} of {{nb}}"
                    ),
                    align="C",
                )

            def section_header(self, number: str, title: str):
                if self.get_y() > 246:
                    self.add_page()
                self.ln(3.5)
                y = self.get_y()
                usable = self.w - self.l_margin - self.r_margin
                self.set_fill_color(241, 245, 249)
                self.rect(self.l_margin, y, usable, 8.0, "F")
                self.set_fill_color(29, 78, 216)
                self.rect(self.l_margin, y, 2.8, 8.0, "F")
                self.set_xy(self.l_margin + 5.5, y + 0.5)
                self.set_font("Helvetica", "B", 11)
                self.set_text_color(15, 23, 42)
                self.cell(usable - 6, 7.0, _sanitize_pdf_text(f"{number}.  {title}"))
                self.ln(10.0)

            def draw_table(
                self,
                headers: List[str],
                rows: List[List[str]],
                widths: List[float],
                bold_cols: Optional[set] = None,
                color_col_fn=None,
            ):
                """Renders an auto-wrapping multi-line table with ZERO text truncation."""
                bold_cols = bold_cols or set()
                line_h = 4.6
                pad_x = 2.0
                pad_y = 1.6

                def _draw_header():
                    self.set_fill_color(15, 23, 42)
                    self.set_draw_color(15, 23, 42)
                    self.set_text_color(255, 255, 255)
                    self.set_font("Helvetica", "B", 8)
                    x = self.l_margin
                    y = self.get_y()
                    for h_txt, w in zip(headers, widths):
                        self.rect(x, y, w, 7.0, "FD")
                        self.set_xy(x + pad_x, y + 1.2)
                        self.cell(w - 2 * pad_x, 4.6, _sanitize_pdf_text(h_txt))
                        x += w
                    self.set_y(y + 7.0)

                if self.get_y() > 250:
                    self.add_page()
                _draw_header()

                for r_idx, row in enumerate(rows):
                    wrapped_cells: List[List[str]] = []
                    max_lines = 1
                    for c_idx, (val, w) in enumerate(zip(row, widths)):
                        style = "B" if c_idx in bold_cols else ""
                        self.set_font("Helvetica", style, 7.8)
                        lines = _wrap_text_to_width(self, str(val), w - 2 * pad_x)
                        wrapped_cells.append(lines)
                        max_lines = max(max_lines, len(lines))

                    row_h = max_lines * line_h + 2 * pad_y
                    if self.get_y() + row_h > 274:
                        self.add_page()
                        _draw_header()

                    y = self.get_y()
                    x = self.l_margin
                    fill_rgb = (248, 250, 252) if r_idx % 2 == 1 else (255, 255, 255)
                    self.set_draw_color(203, 213, 225)
                    self.set_line_width(0.25)

                    for c_idx, (lines, w) in enumerate(zip(wrapped_cells, widths)):
                        self.set_fill_color(*fill_rgb)
                        self.rect(x, y, w, row_h, "FD")
                        style = "B" if c_idx in bold_cols else ""
                        self.set_font("Helvetica", style, 7.8)
                        if color_col_fn:
                            rgb = color_col_fn(c_idx, row[c_idx])
                            self.set_text_color(*rgb)
                        else:
                            self.set_text_color(15, 23, 42) if c_idx in bold_cols else self.set_text_color(51, 65, 85)

                        for l_idx, ln in enumerate(lines):
                            self.set_xy(x + pad_x, y + pad_y + l_idx * line_h)
                            self.cell(w - 2 * pad_x, line_h, ln)
                        x += w

                    self.set_y(y + row_h)
                self.ln(3)

            def hanging_bullet(self, label: str, text: str):
                """Clean hanging-indent bullet with Royal Blue square marker."""
                usable = self.w - self.l_margin - self.r_margin
                indent_x = self.l_margin + 4.5
                content_w = usable - 4.5
                self.set_font("Helvetica", "", 8.6)
                wrapped = _wrap_text_to_width(self, f"{label}: {text}", content_w)
                needed_h = len(wrapped) * 4.8 + 1.5
                if self.get_y() + needed_h > 274:
                    self.add_page()

                y0 = self.get_y()
                self.set_fill_color(37, 99, 235)
                self.rect(self.l_margin + 1.2, y0 + 1.6, 1.6, 1.6, "F")

                self.set_xy(indent_x, y0)
                self.set_font("Helvetica", "B", 8.6)
                self.set_text_color(15, 23, 42)
                lbl_str = _sanitize_pdf_text(f"{label}: ")
                lbl_w = self.get_string_width(lbl_str)
                if lbl_w < content_w * 0.55:
                    self.cell(lbl_w, 4.8, lbl_str)
                    self.set_font("Helvetica", "", 8.6)
                    self.set_text_color(51, 65, 85)
                    first_rem = content_w - lbl_w
                    rem_lines = _wrap_text_to_width(self, text, first_rem)
                    self.cell(first_rem, 4.8, rem_lines[0])
                    self.ln(4.8)
                    if len(rem_lines) > 1:
                        rest_text = " ".join(rem_lines[1:])
                        for ln in _wrap_text_to_width(self, rest_text, content_w):
                            self.set_x(indent_x)
                            self.cell(content_w, 4.8, ln)
                            self.ln(4.8)
                else:
                    self.multi_cell(content_w, 4.8, lbl_str)
                    self.set_font("Helvetica", "", 8.6)
                    self.set_text_color(51, 65, 85)
                    for ln in _wrap_text_to_width(self, text, content_w):
                        self.set_x(indent_x)
                        self.cell(content_w, 4.8, ln)
                        self.ln(4.8)
                self.ln(1.0)

            def code_box(self, title: str, code_text: str, is_fix: bool = False):
                usable = self.w - self.l_margin - self.r_margin
                self.set_font("Courier", "", 7.8)
                wrapped_lines = _wrap_text_to_width(self, code_text or "// N/A", usable - 6)
                box_h = 6.0 + len(wrapped_lines) * 4.2 + 3.0
                if self.get_y() + box_h > 274:
                    self.add_page()

                y = self.get_y()
                if is_fix:
                    self.set_fill_color(236, 253, 245)
                    self.set_draw_color(167, 243, 208)
                    self.set_text_color(6, 95, 70)
                else:
                    self.set_fill_color(254, 242, 242)
                    self.set_draw_color(254, 202, 202)
                    self.set_text_color(153, 27, 27)
                self.set_font("Helvetica", "B", 7.8)
                self.set_xy(self.l_margin, y)
                self.cell(usable, 5.8, _sanitize_pdf_text(f"  {title}"), border=1, fill=True)
                self.ln(5.8)

                body_y = self.get_y()
                body_h = len(wrapped_lines) * 4.2 + 3.0
                self.set_fill_color(248, 250, 252)
                self.set_draw_color(203, 213, 225)
                self.rect(self.l_margin, body_y, usable, body_h, "FD")
                self.set_font("Courier", "", 7.8)
                self.set_text_color(15, 23, 42)
                for idx_l, ln in enumerate(wrapped_lines):
                    self.set_xy(self.l_margin + 3.0, body_y + 1.5 + idx_l * 4.2)
                    self.cell(usable - 6.0, 4.2, ln)
                self.set_y(body_y + body_h + 2.5)

        pdf = ResearchAuditPDF()
        pdf.alias_nb_pages()
        pdf.set_margins(15, 14, 15)
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.add_page()
        usable_w = pdf.w - pdf.l_margin - pdf.r_margin

        # Cover Header Banner
        y0 = pdf.get_y()
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(pdf.l_margin, y0, usable_w, 31, "F")
        pdf.set_fill_color(37, 99, 235)
        pdf.rect(pdf.l_margin, y0, usable_w, 2.5, "F")

        pdf.set_xy(pdf.l_margin + 5, y0 + 4.5)
        pdf.set_font("Helvetica", "B", 7.8)
        pdf.set_text_color(147, 197, 253)
        pdf.cell(usable_w - 34, 4.5, "AI CODE REVIEW & SECURITY ANALYSIS AGENT  |  TECHNICAL SECURITY & SOFTWARE QUALITY AUDIT MONOGRAPH")

        pdf.set_xy(pdf.l_margin + 5, y0 + 10.0)
        pdf.set_font("Helvetica", "B", 14.5)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(usable_w - 34, 7.0, "Static Security & Code Quality Analysis Report")

        pdf.set_xy(pdf.l_margin + 5, y0 + 18.2)
        pdf.set_font("Helvetica", "", 8.3)
        pdf.set_text_color(226, 232, 240)
        pdf.cell(usable_w - 34, 4.5, _sanitize_pdf_text(f"Target Artifact: {filename} ({language})"))

        pdf.set_xy(pdf.l_margin + 5, y0 + 23.0)
        pdf.set_font("Helvetica", "", 8.0)
        pdf.set_text_color(148, 163, 184)
        pdf.cell(usable_w - 34, 4.5, _sanitize_pdf_text(f"Document ID: {report_id}   |   Generated: {timestamp}"))

        gr_r, gr_g, gr_b = grade_info["rgb"]
        pdf.set_fill_color(gr_r, gr_g, gr_b)
        pdf.rect(pdf.l_margin + usable_w - 26, y0 + 6.0, 21, 19.5, "F")
        pdf.set_xy(pdf.l_margin + usable_w - 26, y0 + 7.5)
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(21, 9.5, grade_info["grade"], align="C")
        pdf.set_xy(pdf.l_margin + usable_w - 26, y0 + 18.0)
        pdf.set_font("Helvetica", "B", 7.8)
        pdf.cell(21, 5.0, f"{health_score:.1f}/100", align="C")
        pdf.set_y(y0 + 35)

        # Executive Abstract Callout
        pdf.set_fill_color(239, 246, 255)
        pdf.set_draw_color(191, 219, 254)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(30, 64, 175)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable_w, 6.2, "  EXECUTIVE ABSTRACT & RELEASE GATE VERDICT", border="LTR", fill=True)
        pdf.ln(6.2)
        pdf.set_font("Helvetica", "", 8.6)
        pdf.set_text_color(30, 41, 59)
        abstract_text = (
            f"This technical audit evaluates {filename} ({language}) using AI Code Review & Security Analysis Agent's 6-layer multi-agent architecture: "
            f"{sv.get('parser_used', 'AST / Tree-sitter')} grammar verification, deterministic SAST scanning, ChromaDB+FAISS RAG retrieval "
            f"over OWASP Top 10, CWE, Bandit, PMD, SpotBugs, and SEI CERT guidelines, and parallel LangGraph agent reasoning. "
            f"Summary: {len(unified)} total findings ({len(sec_list)} security vulnerabilities, {len(qual_list)} quality smells), "
            f"Composite Health Score {health_score}/100 (Grade {grade_info['grade']}), Release Verdict: {grade_info['verdict']}."
        )
        abs_lines = _wrap_text_to_width(pdf, abstract_text, usable_w - 6)
        abs_y = pdf.get_y()
        abs_h = len(abs_lines) * 4.7 + 3.5
        pdf.rect(pdf.l_margin, abs_y, usable_w, abs_h, "FD")
        for idx_a, ln in enumerate(abs_lines):
            pdf.set_xy(pdf.l_margin + 3, abs_y + 1.8 + idx_a * 4.7)
            pdf.cell(usable_w - 6, 4.7, ln)
        pdf.set_y(abs_y + abs_h + 4.0)

        # 4 KPI Cards Row
        kpi_w = (usable_w - 9) / 4.0
        kpi_y = pdf.get_y()
        kpis = [
            ("CODE HEALTH", f"{health_score}/100", f"Security Grade {grade_info['grade']}", grade_info["rgb"]),
            ("SECURITY ISSUES", str(len(sec_list)), f"{sev.get('Critical', 0)} Critical / {sev.get('High', 0)} High", (220, 38, 38)),
            ("QUALITY SMELLS", str(len(qual_list)), f"Maintainability {qa.get('maintainability_score', 0)}/100", (37, 99, 235)),
            ("EST. TECH DEBT", f"{qa.get('technical_debt_minutes', 0)} min", f"CC: {cm.get('cyclomatic_complexity', 1)} | Cog: {cm.get('cognitive_complexity', 0)}", (79, 70, 229)),
        ]
        for idx, (klbl, kval, ksub, krgb) in enumerate(kpis):
            kx = pdf.l_margin + idx * (kpi_w + 3)
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(203, 213, 225)
            pdf.rect(kx, kpi_y, kpi_w, 20.5, "FD")
            pdf.set_fill_color(*krgb)
            pdf.rect(kx, kpi_y, kpi_w, 2.0, "F")
            pdf.set_xy(kx + 2.5, kpi_y + 3.2)
            pdf.set_font("Helvetica", "B", 7)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(kpi_w - 5, 4, klbl)
            pdf.set_xy(kx + 2.5, kpi_y + 7.8)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(kpi_w - 5, 6, _sanitize_pdf_text(kval))
            pdf.set_xy(kx + 2.5, kpi_y + 14.5)
            pdf.set_font("Helvetica", "", 7)
            pdf.set_text_color(71, 85, 105)
            pdf.cell(kpi_w - 5, 4, _sanitize_pdf_text(ksub))
        pdf.set_y(kpi_y + 24.5)

        # Section 1: Visual Analytics Snapshot
        radar_png, radar_ratio = _render_radar_png_bytes(report)
        sev_png, sev_ratio = _render_severity_png_bytes(report)
        if radar_png and sev_png:
            pdf.section_header("1", "Visual Analytics Snapshot")
            p1 = Path(tempfile.mkstemp(suffix=".png")[1])
            p2 = Path(tempfile.mkstemp(suffix=".png")[1])
            p1.write_bytes(radar_png)
            p2.write_bytes(sev_png)
            temp_files.extend([p1, p2])

            half_w = (usable_w - 6) / 2.0
            chart_h = max(half_w * radar_ratio, half_w * sev_ratio)
            if pdf.get_y() + chart_h + 10 > 274:
                pdf.add_page()
            y_ch = pdf.get_y()
            pdf.set_draw_color(203, 213, 225)
            pdf.rect(pdf.l_margin, y_ch, half_w, chart_h + 2)
            pdf.rect(pdf.l_margin + half_w + 6, y_ch, half_w, chart_h + 2)
            pdf.image(str(p1), x=pdf.l_margin + 1, y=y_ch + 1, w=half_w - 2)
            pdf.image(str(p2), x=pdf.l_margin + half_w + 7, y=y_ch + 1, w=half_w - 2)
            pdf.set_y(y_ch + chart_h + 6)

        # Section 2: Complexity & Quality Telemetry (Auto-Wrapping Table)
        pdf.section_header("2", "Complexity & ISO/IEC 25010 Quality Telemetry")
        telemetry_rows = [
            ["McCabe Cyclomatic Complexity", f"{cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})", "Target <= 5 (Rank A). Independent control-flow decision paths per function."],
            ["Sonar Cognitive Complexity", str(cm.get("cognitive_complexity", 0)), "Target <= 8. Human comprehension penalty for deeply nested control blocks."],
            ["Asymptotic Time / Space", f"{cm.get('time_complexity', 'O(1)')} / {cm.get('space_complexity', 'O(1)')}", "Estimated execution time and auxiliary memory scaling relative to input size."],
            ["Maintainability Index", f"{qa.get('maintainability_score', 0)} / 100", "Target >= 80/100 (ISO/IEC 25010 composite maintainability benchmark)."],
            ["Documentation / Duplication", f"{qa.get('documentation_score', 0)}% docs | {qa.get('duplication_percentage', 0)}% dup", "Target >= 60% inline documentation and < 5% code duplication."],
            ["Syntax & AST Parser", f"{sv.get('parser_used', 'AST')} ({sv.get('ast_node_count', 0)} AST nodes)", "Deterministic pre-agent grammar verification passed with zero errors."],
        ]
        pdf.draw_table(
            headers=["Metric Dimension", "Measured Value", "Engineering Benchmark & Interpretation"],
            rows=telemetry_rows,
            widths=[48, 52, 80],
            bold_cols={0},
        )

        # Section 3: Secure Coding Compliance Matrix & Methodology
        pdf.section_header("3", "Secure Coding Compliance Matrix & Audit Methodology")
        pdf.draw_table(
            headers=["Secure Coding Control", "Audit Status", "Reference Standard"],
            rows=[[c, s, std] for c, s, std in compliance_rows],
            widths=[75, 40, 65],
            bold_cols={0, 1},
            color_col_fn=lambda c_idx, val: (
                (5, 150, 105) if (c_idx == 1 and val == "PASS")
                else (220, 38, 38) if (c_idx == 1 and val != "PASS")
                else (15, 23, 42) if c_idx == 0
                else (51, 65, 85)
            ),
        )
        pdf.hanging_bullet("Syntax Gatekeeper", "Automatically detects Python/Java and validates grammar via AST and Tree-sitter before invoking AI agents.")
        pdf.hanging_bullet("Hybrid SAST + RAG Engine", "Combines deterministic OWASP/Bandit/PMD/SpotBugs rules with ChromaDB+FAISS vector retrieval (all-MiniLM-L6-v2).")
        pdf.hanging_bullet("Parallel Multi-Agent Graph", "Executes Code Analysis and Security Vulnerability Agents concurrently in LangGraph, deduplicates overlaps, and synthesizes fixes.")

        # Section 4: Prioritized Findings Inventory (Auto-Wrapping Table)
        pdf.section_header("4", f"Prioritized Findings Inventory ({len(unified)} Findings)")
        if not unified:
            pdf.set_fill_color(236, 253, 245)
            pdf.set_draw_color(167, 243, 208)
            pdf.set_text_color(6, 95, 70)
            pdf.set_font("Helvetica", "B", 8.8)
            pdf.cell(usable_w, 8.5, "  Zero security vulnerabilities or code quality defects detected. Artifact meets release criteria.", border=1, fill=True)
            pdf.ln(11)
        else:
            inv_rows = []
            for item in unified:
                s_lvl = str(item.get("severity", "Medium"))
                inv_rows.append([
                    s_lvl,
                    str(item.get("id", "")),
                    str(item.get("vulnerability_name") or item.get("title", "")),
                    str(item.get("owasp_category") or item.get("tool_or_standard", "")),
                    str(item.get("line_reference", "N/A")),
                    SEVERITY_EFFORT.get(s_lvl, "10 min"),
                ])
            pdf.draw_table(
                headers=["Severity", "ID", "Issue / Vulnerability", "Mapped Standard / CWE", "Line", "Effort"],
                rows=inv_rows,
                widths=[21, 16, 49, 52, 18, 24],
                bold_cols={0, 1},
                color_col_fn=lambda c_idx, val: (
                    SEVERITY_RGB.get(val, (100, 116, 139)) if c_idx == 0
                    else (15, 23, 42) if c_idx in (1, 2)
                    else (51, 65, 85)
                ),
            )

        # Section 5: Detailed Technical Findings & Remediation Deep Dives
        pdf.section_header("5", "Detailed Technical Findings & Remediation Analysis")
        if not unified:
            pdf.hanging_bullet("Audit Conclusion", "All deterministic SAST checks, complexity benchmarks, and OWASP Top 10 AI reviews passed cleanly.")
        else:
            for idx, item in enumerate(unified, start=1):
                if pdf.get_y() > 210:
                    pdf.add_page()
                fid = str(item.get("id", f"F-{idx:02d}"))
                rem = rem_map.get(fid, {})
                s_lvl = str(item.get("severity", "Medium"))
                s_rgb = SEVERITY_RGB.get(s_lvl, (37, 99, 235))
                v_name = str(item.get("vulnerability_name") or item.get("title", "Issue"))
                std_ref = str(rem.get("best_practice_guideline") or item.get("owasp_category") or item.get("tool_or_standard", ""))

                pdf.set_fill_color(241, 245, 249)
                pdf.set_draw_color(203, 213, 225)
                y_band = pdf.get_y()
                pdf.rect(pdf.l_margin, y_band, usable_w, 8.0, "FD")
                pdf.set_fill_color(*s_rgb)
                pdf.rect(pdf.l_margin, y_band, 3.2, 8.0, "F")
                pdf.set_xy(pdf.l_margin + 5.5, y_band + 1.2)
                pdf.set_font("Helvetica", "B", 9.5)
                pdf.set_text_color(15, 23, 42)
                pdf.cell(usable_w - 8, 5.5, _sanitize_pdf_text(f"5.{idx}  [{s_lvl.upper()}]  {fid}: {v_name}  ({item.get('line_reference', 'N/A')})"))
                pdf.ln(10.0)

                pdf.hanging_bullet("Mapped Standard & Source", f"{std_ref}  |  {item.get('agent_source', 'Agent')}  |  {rem.get('recommendation_category', 'Remediation')}")
                pdf.hanging_bullet("Root Cause Analysis", str(rem.get("root_cause") or item.get("description", "")))
                pdf.hanging_bullet("Risk & Technical Impact", str(item.get("description", "")))
                pdf.hanging_bullet("Actionable Fix Protocol", str(rem.get("fix_steps") or item.get("recommendation", "")))

                orig_snip = str(rem.get("original_code") or item.get("code_snippet") or "")
                fix_snip = str(rem.get("corrected_code") or item.get("secure_code_suggestion") or "")
                if orig_snip:
                    pdf.code_box("Flagged Source Pattern", orig_snip, is_fix=False)
                if fix_snip:
                    pdf.code_box("Verified Secure Implementation", fix_snip, is_fix=True)
                pdf.ln(2.5)

        # Section 6: Phased Remediation Roadmap & Standards References
        pdf.section_header("6", "Phased Remediation Roadmap & Standards References")
        p0 = [f"{i.get('id')} ({i.get('vulnerability_name')})" for i in unified if i.get("severity") == "Critical"]
        p1 = [f"{i.get('id')} ({i.get('vulnerability_name')})" for i in unified if i.get("severity") == "High"]
        p2 = [f"{i.get('id')} ({i.get('vulnerability_name')})" for i in unified if i.get("severity") in ("Medium", "Low", "Informational")]

        pdf.hanging_bullet("Phase P0 (Immediate - Critical)", ", ".join(p0) if p0 else "None detected.")
        pdf.hanging_bullet("Phase P1 (Pre-Release - High)", ", ".join(p1) if p1 else "None detected.")
        pdf.hanging_bullet("Phase P2 (Next Sprint - Medium/Low)", ", ".join(p2) if p2 else "None detected.")
        pdf.ln(2)

        refs = [
            "[1] OWASP Foundation, OWASP Top 10 Web Application Security Risks (A01-A10), 2025 Standard.",
            "[2] MITRE Corporation, Common Weakness Enumeration (CWE Top 25 Software Weaknesses), 2025.",
            "[3] Carnegie Mellon SEI, SEI CERT Coding Standards for Java & Python Secure Coding Guidelines.",
            "[4] McCabe, T. J., A Complexity Measure, IEEE Trans. Softw. Eng., & ISO/IEC 25010 Quality Model.",
        ]
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(71, 85, 105)
        for ref in refs:
            pdf.set_x(pdf.l_margin + 2)
            pdf.multi_cell(0, 4.5, _sanitize_pdf_text(ref))

        ver = str(getattr(fpdf_mod, "__version__", "1.0"))
        major = int(ver.split(".")[0]) if ver and ver[0].isdigit() else 1
        raw_out = pdf.output() if major >= 2 else pdf.output(dest="S")
        return raw_out.encode("latin-1") if isinstance(raw_out, str) else bytes(raw_out)
    finally:
        for tf in temp_files:
            try:
                tf.unlink(missing_ok=True)
            except Exception:
                pass
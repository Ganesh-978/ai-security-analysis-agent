import base64
import html
import io
import math
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Informational"]
SEVERITY_COLORS = {
    "Critical": "#EF4444",
    "High": "#F97316",
    "Medium": "#EAB308",
    "Low": "#3B82F6",
    "Informational": "#64748B",
}
SEVERITY_EFFORT = {
    "Critical": "30 mins (Immediate)",
    "High": "20 mins (Before Release)",
    "Medium": "10 mins (Next Sprint)",
    "Low": "5 mins (Backlog)",
    "Informational": "2 mins (Optional)",
}


def compute_grade_and_verdict(health_score: float, sev: Dict[str, int]) -> Dict[str, str]:
    crit = int(sev.get("Critical", 0))
    high = int(sev.get("High", 0))
    if crit > 0 or health_score < 45:
        grade, g_color = "F", "#DC2626"
        verdict = "BLOCK RELEASE - Critical Security & Quality Risks Detected"
    elif high > 0 or health_score < 60:
        grade, g_color = "D", "#EA580C"
        verdict = "CHANGES REQUESTED - High-Severity Findings Require Remediation"
    elif health_score < 75:
        grade, g_color = "C", "#CA8A04"
        verdict = "CONDITIONAL APPROVAL - Address Medium Findings Before Next Release"
    elif health_score < 88:
        grade, g_color = "B", "#2563EB"
        verdict = "APPROVED WITH MINOR RECOMMENDATIONS"
    else:
        grade, g_color = "A", "#059669"
        verdict = "APPROVED - Meets Enterprise Security & Quality Standards"
    return {"grade": grade, "color": g_color, "verdict": verdict}


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


def _render_radar_png_bytes(report: Dict[str, Any]) -> Optional[bytes]:
    """High-DPI PNG of the 5-Axis Pentagon Radar Chart (Plotly+Kaleido -> Matplotlib fallback)."""
    try:
        from ui.charts import build_pentagon_radar_figure

        fig = build_pentagon_radar_figure(report)
        return fig.to_image(format="png", width=620, height=420, scale=2)
    except Exception:
        pass

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        scores = _compute_radar_scores_local(report)
        labels = list(scores.keys())
        values = list(scores.values())
        n = len(labels)
        angles = [math.pi / 2 - (2 * math.pi * i / n) for i in range(n)]

        fig, ax = plt.subplots(figsize=(5.6, 4.0), dpi=180)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        ax.set_aspect("equal")
        ax.axis("off")

        for level in [20, 40, 60, 80, 100]:
            xs = [level * math.cos(a) for a in angles] + [level * math.cos(angles[0])]
            ys = [level * math.sin(a) for a in angles] + [level * math.sin(angles[0])]
            ax.plot(xs, ys, color="#CBD5E1", linewidth=0.9, zorder=1)
            ax.text(2, level - 3, str(level), fontsize=7.5, color="#64748B", ha="left", va="top")

        for a, lbl, val in zip(angles, labels, values):
            ax.plot([0, 100 * math.cos(a)], [0, 100 * math.sin(a)], color="#CBD5E1", linewidth=0.9, zorder=1)
            lx, ly = 124 * math.cos(a), 118 * math.sin(a)
            ax.text(
                lx,
                ly,
                f"{lbl}\n({val:.0f})",
                fontsize=8.5,
                fontweight="bold",
                color="#0F172A",
                ha="center",
                va="center",
            )

        px = [v * math.cos(a) for v, a in zip(values, angles)]
        py = [v * math.sin(a) for v, a in zip(values, angles)]
        ax.fill(px + [px[0]], py + [py[0]], color="#2563EB", alpha=0.20, zorder=2)
        ax.plot(px + [px[0]], py + [py[0]], color="#2563EB", linewidth=2.2, zorder=3)
        ax.scatter(px, py, color="#1D4ED8", s=34, edgecolors="#FFFFFF", linewidths=1.2, zorder=4)

        ax.set_xlim(-150, 150)
        ax.set_ylim(-142, 145)
        plt.tight_layout(pad=0.3)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight", facecolor="#FFFFFF")
        plt.close(fig)
        return buf.getvalue()
    except Exception:
        return None


def _render_severity_png_bytes(report: Dict[str, Any]) -> Optional[bytes]:
    """High-DPI PNG of the Color-Coded Severity Chart (Plotly+Kaleido -> Matplotlib fallback)."""
    try:
        from ui.charts import build_severity_bar_figure

        fig = build_severity_bar_figure(report)
        return fig.to_image(format="png", width=620, height=420, scale=2)
    except Exception:
        pass

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        sev = report.get("severity_breakdown") or {}
        labels = list(reversed(SEVERITY_ORDER))
        counts = [int(sev.get(lvl, 0)) for lvl in labels]
        colors = [SEVERITY_COLORS[lvl] for lvl in labels]
        max_val = max(counts) if counts else 0

        fig, ax = plt.subplots(figsize=(5.6, 3.8), dpi=180)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        bars = ax.barh(labels, counts, color=colors, height=0.55, edgecolor="none")
        for bar, cnt in zip(bars, counts):
            ax.text(
                bar.get_width() + 0.15,
                bar.get_y() + bar.get_height() / 2,
                str(cnt),
                va="center",
                ha="left",
                fontsize=10,
                fontweight="bold",
                color="#0F172A",
            )

        ax.set_xlim(0, max(max_val + 1.5, 5))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#CBD5E1")
        ax.spines["bottom"].set_color("#CBD5E1")
        ax.xaxis.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1")
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", labelsize=9.5, colors="#0F172A")
        ax.tick_params(axis="x", labelsize=8.5, colors="#64748B")
        ax.set_xlabel("Number of Findings", fontsize=9, color="#64748B")
        plt.tight_layout(pad=0.6)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight", facecolor="#FFFFFF")
        plt.close(fig)
        return buf.getvalue()
    except Exception:
        return None


def _b64_img_tag(png_bytes: Optional[bytes], alt: str) -> str:
    if not png_bytes:
        return f'<div style="padding:24px;text-align:center;color:#64748B;">{html.escape(alt)} unavailable</div>'
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f'<img src="data:image/png;base64,{b64}" alt="{html.escape(alt)}" class="chart-img" />'


def generate_executive_html_report(report: Dict[str, Any]) -> str:
    """
    Generates a self-contained Executive HTML Security Report with embedded
    high-DPI Base64 PNG charts and @media print CSS for 1-click PDF printing.
    """
    qa = report.get("quality_assessment") or {}
    cm = report.get("complexity_metrics") or {}
    sev = report.get("severity_breakdown") or {}
    unified = report.get("unified_findings") or []
    rem_list = report.get("remediation_plan") or []
    rem_map = {r.get("finding_id"): r for r in rem_list}

    filename = str(report.get("filename", "snippet"))
    lang = str(report.get("language", "python")).upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    health_score = float(qa.get("code_health_score", 0.0))
    tech_debt = int(qa.get("technical_debt_minutes", 0))
    grade_info = compute_grade_and_verdict(health_score, sev)

    radar_img = _b64_img_tag(_render_radar_png_bytes(report), "5-Axis Pentagon Quality & Security Radar")
    sev_img = _b64_img_tag(_render_severity_png_bytes(report), "Severity Distribution Chart")

    matrix_rows: List[str] = []
    for item in unified:
        s_lvl = str(item.get("severity", "Medium"))
        s_col = SEVERITY_COLORS.get(s_lvl, "#64748B")
        rule = str(item.get("owasp_category") or item.get("tool_or_standard", "Standard"))
        effort = SEVERITY_EFFORT.get(s_lvl, "10 mins")
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
            '<tr><td colspan="7" style="text-align:center;color:#059669;font-weight:600;">No findings detected — code meets all security and quality benchmarks.</td></tr>'
        )

    deep_cards: List[str] = []
    for item in unified:
        fid = str(item.get("id", "ID"))
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
        verification = (
            f"Re-run CodeGuard AI SAST & unit tests targeting {item.get('line_reference', 'modified lines')} "
            f"to confirm {std_ref} compliance with zero regression."
        )

        deep_cards.append(
            f'<div class="finding-card" style="border-left:4px solid {s_col};">'
            '<div class="finding-head">'
            f'<div><span class="sev-pill" style="background:{s_col};">{html.escape(s_lvl)}</span> '
            f'<strong>[{html.escape(fid)}] {html.escape(v_name)}</strong></div>'
            f'<div class="finding-meta">{html.escape(str(item.get("line_reference", "")))} · <code>{html.escape(std_ref)}</code></div>'
            "</div>"
            f'<p><strong>Root Cause &amp; Exploit Impact:</strong> {html.escape(root_cause)} {html.escape(impact if impact != root_cause else "")}</p>'
            f'<p><strong>Recommended Action:</strong> {html.escape(fix_steps)}</p>'
            '<div class="code-compare">'
            f'<div><div class="code-lbl bad">Vulnerable / Flagged Code</div><pre><code>{html.escape(orig_code)}</code></pre></div>'
            f'<div><div class="code-lbl good">Recommended Secure Fix</div><pre><code>{html.escape(fixed_code)}</code></pre></div>'
            "</div>"
            f'<div class="verify-box"><strong>Verification Step:</strong> {html.escape(verification)}</div>'
            "</div>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>CodeGuard AI Executive Security Report - {html.escape(filename)}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 28px; background: #f8fafc; color: #0f172a; line-height: 1.5; }}
  .container {{ max-width: 1120px; margin: 0 auto; }}
  .banner {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; border-radius: 16px; padding: 26px 30px; margin-bottom: 22px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 18px; }}
  .banner h1 {{ margin: 0 0 6px 0; font-size: 1.55rem; letter-spacing: -0.02em; }}
  .banner-meta {{ font-size: 0.85rem; color: #cbd5e1; }}
  .grade-box {{ display: flex; align-items: center; gap: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.16); padding: 12px 20px; border-radius: 12px; }}
  .grade-letter {{ font-size: 2.3rem; font-weight: 800; line-height: 1; padding: 8px 16px; border-radius: 10px; color: #fff; background: {grade_info['color']}; }}
  .verdict-bar {{ background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid {grade_info['color']}; border-radius: 10px; padding: 14px 18px; margin-bottom: 22px; font-weight: 700; color: #0f172a; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; align-items: center; }}
  .kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px; }}
  .kpi {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 18px; }}
  .kpi-lbl {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; font-weight: 700; }}
  .kpi-val {{ font-size: 1.55rem; font-weight: 800; color: #0f172a; margin-top: 4px; }}
  .section-title {{ font-size: 1.18rem; font-weight: 700; color: #0f172a; margin: 24px 0 12px 0; padding-bottom: 6px; border-bottom: 2px solid #e2e8f0; }}
  .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 16px; }}
  .card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; }}
  .card h3 {{ margin: 0 0 10px 0; font-size: 0.98rem; color: #0f172a; }}
  .chart-img {{ width: 100%; height: auto; display: block; border-radius: 8px; }}
  .telemetry-strip {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
  .tele-item {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px; font-size: 0.84rem; }}
  .tele-item span {{ display: block; font-size: 0.72rem; text-transform: uppercase; color: #64748b; font-weight: 700; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; font-size: 0.85rem; margin-bottom: 22px; }}
  th {{ background: #f1f5f9; color: #334155; text-align: left; padding: 10px 12px; font-weight: 700; font-size: 0.76rem; text-transform: uppercase; }}
  td {{ padding: 10px 12px; border-top: 1px solid #e2e8f0; vertical-align: top; }}
  .sev-pill {{ display: inline-block; padding: 2px 9px; border-radius: 999px; color: #fff; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }}
  .finding-card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; page-break-inside: avoid; }}
  .finding-head {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }}
  .finding-meta {{ font-size: 0.8rem; color: #475569; }}
  .code-compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0; }}
  .code-lbl {{ font-size: 0.75rem; font-weight: 700; padding: 5px 10px; border-radius: 6px 6px 0 0; }}
  .code-lbl.bad {{ background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-bottom: none; }}
  .code-lbl.good {{ background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; border-bottom: none; }}
  pre {{ margin: 0; padding: 12px; background: #0f172a; color: #e2e8f0; border-radius: 0 0 6px 6px; overflow-x: auto; font-family: 'JetBrains Mono', Consolas, monospace; font-size: 0.78rem; white-space: pre-wrap; word-break: break-word; }}
  .verify-box {{ background: #eff6ff; border: 1px solid #bfdbfe; color: #1e3a8a; border-radius: 8px; padding: 9px 12px; font-size: 0.82rem; margin-top: 8px; }}
  .print-btn {{ background: #2563eb; color: #fff; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.84rem; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .no-print {{ display: none !important; }}
    .banner, .sev-pill, .grade-letter {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .charts-grid, .finding-card, table {{ page-break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="banner">
    <div>
      <h1>🛡️ CodeGuard AI — Executive Security &amp; Quality Report</h1>
      <div class="banner-meta">
        File: <strong>{html.escape(filename)}</strong> &nbsp;|&nbsp;
        Language: <strong>{html.escape(lang)}</strong> &nbsp;|&nbsp;
        Scanned: <strong>{html.escape(timestamp)}</strong>
      </div>
    </div>
    <div class="grade-box">
      <div class="grade-letter">{grade_info['grade']}</div>
      <div>
        <div style="font-size:0.74rem;text-transform:uppercase;color:#cbd5e1;font-weight:700;">Code Health Score</div>
        <div style="font-size:1.5rem;font-weight:800;">{health_score}/100</div>
      </div>
    </div>
  </div>

  <div class="verdict-bar">
    <span>Risk Verdict: {html.escape(grade_info['verdict'])}</span>
    <button class="print-btn no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
  </div>

  <div class="kpi-row">
    <div class="kpi"><div class="kpi-lbl">Total Findings</div><div class="kpi-val">{len(unified)}</div></div>
    <div class="kpi"><div class="kpi-lbl">Critical / High</div><div class="kpi-val" style="color:#dc2626;">{int(sev.get('Critical', 0))} / {int(sev.get('High', 0))}</div></div>
    <div class="kpi"><div class="kpi-lbl">Maintainability</div><div class="kpi-val">{qa.get('maintainability_score', 0)}/100</div></div>
    <div class="kpi"><div class="kpi-lbl">Estimated Tech Debt</div><div class="kpi-val">{tech_debt} mins</div></div>
  </div>

  <div class="section-title">1. Visual Analytics Snapshot &amp; Complexity Telemetry</div>
  <div class="charts-grid">
    <div class="card"><h3>5-Axis Quality &amp; Security Pentagon Radar</h3>{radar_img}</div>
    <div class="card"><h3>Color-Coded Severity Distribution</h3>{sev_img}</div>
  </div>
  <div class="telemetry-strip">
    <div class="tele-item"><span>Cyclomatic Complexity</span><strong>{cm.get('cyclomatic_complexity', 1)} ({html.escape(str(cm.get('cyclomatic_rank', 'A')))})</strong></div>
    <div class="tele-item"><span>Cognitive Complexity</span><strong>{cm.get('cognitive_complexity', 0)}</strong></div>
    <div class="tele-item"><span>Time Complexity</span><strong>{html.escape(str(cm.get('time_complexity', 'O(1)')))}</strong></div>
    <div class="tele-item"><span>Space Complexity</span><strong>{html.escape(str(cm.get('space_complexity', 'O(1)')))}</strong></div>
  </div>

  <div class="section-title">2. Prioritized Findings Matrix</div>
  <table>
    <thead>
      <tr>
        <th>Severity</th><th>ID</th><th>Issue / Vulnerability</th><th>Rule / CWE / OWASP</th><th>Category</th><th>Line</th><th>Est. Effort</th>
      </tr>
    </thead>
    <tbody>
      {''.join(matrix_rows)}
    </tbody>
  </table>

  <div class="section-title">3. Actionable Remediation Deep-Dive Cards</div>
  {''.join(deep_cards) if deep_cards else '<div class="card" style="color:#059669;font-weight:600;">No security or code quality issues require remediation.</div>'}
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
        "\t": "    ",
    }
    out = str(text)
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out.encode("latin-1", errors="ignore").decode("latin-1")


def _wrap_long_tokens(text: str, max_len: int = 85) -> str:
    wrapped_lines: List[str] = []
    for line in _sanitize_pdf_text(text).splitlines():
        if len(line) <= max_len:
            wrapped_lines.append(line)
        else:
            words = line.split(" ")
            curr = ""
            for w in words:
                while len(w) > max_len:
                    if curr:
                        wrapped_lines.append(curr)
                        curr = ""
                    wrapped_lines.append(w[:max_len])
                    w = w[max_len:]
                if not curr:
                    curr = w
                elif len(curr) + 1 + len(w) <= max_len:
                    curr += " " + w
                else:
                    wrapped_lines.append(curr)
                    curr = w
            if curr:
                wrapped_lines.append(curr)
    return "\n".join(wrapped_lines)


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
        "# CodeGuard AI — Code Review & Security Analysis Report",
        "",
        "## 1. Executive Summary",
        f"- **Source File:** `{report.get('filename', 'snippet')}`",
        f"- **Language:** `{lang.upper()}`",
        f"- **Generated:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- **Overall Code Health Score:** `{qa.get('code_health_score', 0)}/100` (Security Grade: **{grade_info['grade']}**)",
        f"- **Risk Verdict:** {grade_info['verdict']}",
        "",
        "## 2. Complexity & Quality Telemetry",
        f"- **Maintainability:** `{qa.get('maintainability_score', 0)}/100` | **Complexity Health:** `{qa.get('complexity_score', 0)}/100`",
        f"- **Documentation:** `{qa.get('documentation_score', 0)}%` | **Duplication:** `{qa.get('duplication_percentage', 0)}%`",
        f"- **Cyclomatic:** `{cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})` | **Cognitive:** `{cm.get('cognitive_complexity', 0)}`",
        f"- **Time / Space Complexity:** `{cm.get('time_complexity', 'O(1)')}` / `{cm.get('space_complexity', 'O(1)')}`",
        f"- **Technical Debt:** `{qa.get('technical_debt_minutes', 0)} mins`",
        "",
        "## 3. Severity Breakdown",
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
                f"- **Rule / Standard:** `{s.get('owasp_category') or s.get('tool_or_standard', '')}`\n"
                f"- **Risk Description:** {s.get('description', '')}\n"
                f"- **Recommendation:** {s.get('recommendation', '')}\n"
            )

    md.append("## 5. Code Quality & Smells")
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
                f"- **Fix Steps:** {r.get('fix_steps', '')}\n"
                f"```{lang}\n{r.get('corrected_code', '')}\n```\n"
            )

    return "\n".join(md)


def _build_pure_python_pdf(lines: List[str]) -> bytes:
    wrapped_lines: List[str] = []
    for raw_line in lines:
        clean = _wrap_long_tokens(raw_line, max_len=86)
        if not clean:
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(clean.splitlines())

    lines_per_page = 48
    pages = [
        wrapped_lines[i : i + lines_per_page]
        for i in range(0, max(1, len(wrapped_lines)), lines_per_page)
    ]

    objects: List[bytes] = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    page_obj_indices, content_obj_indices = [], []
    next_obj_num = 4
    for _ in pages:
        page_obj_indices.append(next_obj_num)
        content_obj_indices.append(next_obj_num + 1)
        next_obj_num += 2

    kids_str = " ".join(f"{idx} 0 R" for idx in page_obj_indices)
    objects.append(f"<< /Type /Pages /Kids [{kids_str}] /Count {len(pages)} >>".encode("latin-1"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    for p_idx, page_lines in enumerate(pages):
        p_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_obj_indices[p_idx]} 0 R >>"
        ).encode("latin-1")
        objects.append(p_obj)
        stream_cmds = ["BT", "/F1 10 Tf", "50 745 Td", "14 TL"]
        for ln in page_lines:
            esc = ln.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            stream_cmds.append(f"({esc}) Tj T*")
        stream_cmds.append("ET")
        stream_data = "\n".join(stream_cmds).encode("latin-1")
        c_obj = f"<< /Length {len(stream_data)} >>\nstream\n".encode("latin-1") + stream_data + b"\nendstream"
        objects.append(c_obj)

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj_bytes in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{idx} 0 obj\n".encode("latin-1"))
        out.extend(obj_bytes)
        out.extend(b"\nendobj\n")

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
    out.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin-1"))
    return bytes(out)


def generate_pdf_report(report: Dict[str, Any]) -> bytes:
    """Generates a visual PDF Executive Security Report with embedded charts."""
    qa = report.get("quality_assessment") or {}
    cm = report.get("complexity_metrics") or {}
    sev = report.get("severity_breakdown") or {}
    unified = report.get("unified_findings") or []
    rem_list = report.get("remediation_plan") or []
    filename = report.get("filename", "snippet")
    language = str(report.get("language", "python")).upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    grade_info = compute_grade_and_verdict(float(qa.get("code_health_score", 0.0)), sev)

    temp_files: List[Path] = []
    try:
        import fpdf as fpdf_mod
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        usable_w = pdf.w - pdf.l_margin - pdf.r_margin

        # Header Banner
        pdf.set_fill_color(15, 23, 42)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(usable_w, 12, _sanitize_pdf_text("  CodeGuard AI - Executive Code Review & Security Report"), fill=True)
        pdf.ln(15)

        # Executive Summary
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable_w, 8, "1. Executive Summary & Risk Verdict")
        pdf.ln(8)
        pdf.set_font("Helvetica", "", 9.5)
        overview = (
            f"File: {filename}  |  Language: {language}  |  Generated: {timestamp}\n"
            f"Code Health Score: {qa.get('code_health_score', 0)}/100  |  Security Grade: {grade_info['grade']}  |  "
            f"Tech Debt: {qa.get('technical_debt_minutes', 0)} mins\n"
            f"Verdict: {grade_info['verdict']}\n"
            f"Cyclomatic: {cm.get('cyclomatic_complexity', 1)} ({cm.get('cyclomatic_rank', 'A')})  |  "
            f"Cognitive: {cm.get('cognitive_complexity', 0)}  |  "
            f"Time: {cm.get('time_complexity', 'O(1)')}  |  Space: {cm.get('space_complexity', 'O(1)')}"
        )
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable_w, 5.5, _wrap_long_tokens(overview))
        pdf.ln(3)

        # Embed Pentagon Radar & Severity Charts
        radar_png = _render_radar_png_bytes(report)
        sev_png = _render_severity_png_bytes(report)
        if radar_png and sev_png:
            p1 = Path(tempfile.mkstemp(suffix=".png")[1])
            p2 = Path(tempfile.mkstemp(suffix=".png")[1])
            p1.write_bytes(radar_png)
            p2.write_bytes(sev_png)
            temp_files.extend([p1, p2])

            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(pdf.l_margin)
            pdf.cell(usable_w, 8, "2. Visual Analytics Snapshot")
            pdf.ln(8)
            y_charts = pdf.get_y()
            half_w = (usable_w - 6) / 2.0
            pdf.image(str(p1), x=pdf.l_margin, y=y_charts, w=half_w)
            pdf.image(str(p2), x=pdf.l_margin + half_w + 6, y=y_charts, w=half_w)
            pdf.set_y(y_charts + 68)
            pdf.ln(3)

        # Section 3: Prioritized Findings
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable_w, 8, "3. Prioritized Security & Code Quality Findings")
        pdf.ln(8)
        if not unified:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_x(pdf.l_margin)
            pdf.cell(usable_w, 6, "No security vulnerabilities or code quality issues detected.")
            pdf.ln(6)
        else:
            for item in unified:
                pdf.set_font("Helvetica", "B", 9.5)
                header = f"[{item.get('severity', 'High')}] {item.get('id', '')} - {item.get('vulnerability_name', '')} ({item.get('line_reference', '')})"
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable_w, 5.5, _wrap_long_tokens(header))
                pdf.set_font("Helvetica", "", 9)
                details = (
                    f"Standard: {item.get('owasp_category') or item.get('tool_or_standard', '')} | Effort: {SEVERITY_EFFORT.get(item.get('severity', 'Medium'), '10 mins')}\n"
                    f"Impact: {item.get('description', '')}\n"
                    f"Recommendation: {item.get('recommendation', '')}"
                )
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable_w, 5, _wrap_long_tokens(details))
                pdf.ln(2.5)

        # Section 4: Actionable Remediation Roadmap
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_x(pdf.l_margin)
        pdf.cell(usable_w, 8, "4. Actionable Remediation Roadmap & Patched Code")
        pdf.ln(8)
        for r in rem_list:
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(
                usable_w,
                5.5,
                _wrap_long_tokens(f"Fix for {r.get('finding_id', '')}: {r.get('issue_title', '')} [{r.get('recommendation_category', '')}]"),
            )
            pdf.set_font("Helvetica", "", 9)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(
                usable_w,
                5,
                _wrap_long_tokens(
                    f"Root Cause: {r.get('root_cause', '')}\n"
                    f"Standard: {r.get('best_practice_guideline', '')}\n"
                    f"Action Steps: {r.get('fix_steps', '')}"
                ),
            )
            if r.get("corrected_code"):
                pdf.set_font("Courier", "", 8)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable_w, 4.5, _wrap_long_tokens(f"Patched Code:\n{r.get('corrected_code', '')}", max_len=82))
            pdf.ln(2.5)

        ver = str(getattr(fpdf_mod, "__version__", "1.0"))
        major = int(ver.split(".")[0]) if ver and ver[0].isdigit() else 1
        raw_out = pdf.output() if major >= 2 else pdf.output(dest="S")
        return raw_out.encode("latin-1") if isinstance(raw_out, str) else bytes(raw_out)
    except Exception:
        md_text = generate_full_markdown_report(report)
        return _build_pure_python_pdf(md_text.splitlines())
    finally:
        for tf in temp_files:
            try:
                tf.unlink(missing_ok=True)
            except Exception:
                pass
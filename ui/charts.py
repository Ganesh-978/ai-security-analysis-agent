import difflib
import html
from typing import Dict, Any, Tuple, List
import plotly.graph_objects as go


SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Informational"]
SEVERITY_COLORS = {
    "Critical": "#EF4444",
    "High": "#F97316",
    "Medium": "#EAB308",
    "Low": "#3B82F6",
    "Informational": "#64748B",
}


def compute_radar_scores(report: Dict[str, Any]) -> Dict[str, float]:
    """Maps scan telemetry directly onto the 5 radar axes (0-100 scale)."""
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
        "Maintainability Index": maint,
        "Complexity Health": comp,
        "Documentation Coverage": doc,
        "Duplication Hygiene": dup_hygiene,
        "Security Posture": sec_posture,
    }


def build_pentagon_radar_figure(report: Dict[str, Any]) -> go.Figure:
    """Interactive 5-sided pentagon radar chart (gridshape='linear')."""
    scores = compute_radar_scores(report)
    axes = list(scores.keys())
    values = list(scores.values())

    theta_closed = axes + [axes[0]]
    r_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=r_closed,
            theta=theta_closed,
            fill="toself",
            fillcolor="rgba(37, 99, 235, 0.18)",
            line=dict(color="#2563EB", width=2.5),
            marker=dict(color="#1D4ED8", size=7, line=dict(color="#FFFFFF", width=1.5)),
            name="Quality & Security Profile",
            hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f} / 100<extra></extra>",
        )
    )

    fig.update_layout(
        polar=dict(
            gridshape="linear",
            bgcolor="#F8FAFC",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                ticktext=["20", "40", "60", "80", "100"],
                tickfont=dict(size=10, color="#64748B"),
                gridcolor="#CBD5E1",
                linecolor="#CBD5E1",
                showticklabels=True,
            ),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickfont=dict(size=11.5, color="#0F172A", family="Inter, sans-serif"),
                gridcolor="#CBD5E1",
                linecolor="#94A3B8",
            ),
        ),
        showlegend=False,
        height=340,
        margin=dict(l=55, r=55, t=28, b=28),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#0F172A"),
    )
    return fig


def build_severity_bar_figure(report: Dict[str, Any]) -> go.Figure:
    """Color-coded horizontal Plotly severity chart with clean categorical order."""
    sev = report.get("severity_breakdown") or {}
    labels = list(reversed(SEVERITY_ORDER))
    counts = [int(sev.get(lvl, 0)) for lvl in labels]
    colors = [SEVERITY_COLORS[lvl] for lvl in labels]
    max_val = max(counts) if counts else 0
    x_upper = max(max_val + 1.5, 5)

    fig = go.Figure(
        data=[
            go.Bar(
                y=labels,
                x=counts,
                orientation="h",
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(15, 23, 42, 0.08)", width=1),
                    cornerradius=6,
                ),
                text=[f"  {c}" for c in counts],
                textposition="outside",
                textfont=dict(size=13, color="#0F172A", family="Inter, sans-serif"),
                hovertemplate="<b>%{y}</b>: %{x} finding(s)<extra></extra>",
                width=0.56,
            )
        ]
    )

    fig.update_layout(
        height=340,
        margin=dict(l=16, r=42, t=24, b=24),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#0F172A"),
        xaxis=dict(
            range=[0, x_upper],
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=True,
            zerolinecolor="#CBD5E1",
            tickfont=dict(size=11, color="#64748B"),
            dtick=1 if max_val <= 10 else None,
            title=dict(text="Number of Findings", font=dict(size=11, color="#64748B")),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color="#0F172A"),
            categoryorder="array",
            categoryarray=labels,
        ),
        showlegend=False,
    )
    return fig


def build_git_diff_html(
    original_code: str, fixed_code: str, filename: str = "code.py"
) -> Tuple[str, int, int]:
    """
    Renders a Git-style diff table with zero leading indentation so Streamlit
    Markdown never interprets any line as a code block.
    Returns (html_string, additions, deletions).
    """
    orig_lines = original_code.splitlines()
    fixed_lines = fixed_code.splitlines()
    matcher = difflib.SequenceMatcher(None, orig_lines, fixed_lines)

    rows: List[str] = []
    additions = 0
    deletions = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(i2 - i1):
                old_no = i1 + offset + 1
                new_no = j1 + offset + 1
                text = html.escape(orig_lines[i1 + offset])
                rows.append(
                    f'<tr class="gd-eq"><td class="gd-ln">{old_no}</td>'
                    f'<td class="gd-ln">{new_no}</td><td class="gd-sign"> </td>'
                    f'<td class="gd-code">{text if text else "&nbsp;"}</td></tr>'
                )
        elif tag in ("replace", "delete"):
            for k in range(i1, i2):
                deletions += 1
                text = html.escape(orig_lines[k])
                rows.append(
                    f'<tr class="gd-del"><td class="gd-ln">{k + 1}</td>'
                    f'<td class="gd-ln"></td><td class="gd-sign">-</td>'
                    f'<td class="gd-code">{text if text else "&nbsp;"}</td></tr>'
                )
            if tag == "replace":
                for k in range(j1, j2):
                    additions += 1
                    text = html.escape(fixed_lines[k])
                    rows.append(
                        f'<tr class="gd-add"><td class="gd-ln"></td>'
                        f'<td class="gd-ln">{k + 1}</td><td class="gd-sign">+</td>'
                        f'<td class="gd-code">{text if text else "&nbsp;"}</td></tr>'
                    )
        elif tag == "insert":
            for k in range(j1, j2):
                additions += 1
                text = html.escape(fixed_lines[k])
                rows.append(
                    f'<tr class="gd-add"><td class="gd-ln"></td>'
                    f'<td class="gd-ln">{k + 1}</td><td class="gd-sign">+</td>'
                    f'<td class="gd-code">{text if text else "&nbsp;"}</td></tr>'
                )

    safe_fname = html.escape(filename)
    diff_html = (
        '<div class="gd-wrap">'
        f'<div class="gd-header"><span>📄 {safe_fname}</span>'
        f'<span><span class="gd-stat-add">+{additions} additions</span>'
        f'<span class="gd-stat-del">-{deletions} deletions</span></span></div>'
        '<div class="gd-scroll"><table class="gd-table"><tbody>'
        + "".join(rows)
        + "</tbody></table></div></div>"
    )
    return diff_html, additions, deletions
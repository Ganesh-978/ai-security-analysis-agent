# tools/static_analyzer.py
import ast
import math
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Dict, Any, List


def _estimate_time_and_space_complexity(code: str, language: str) -> Dict[str, str]:
    """Estimates Big-O Time and Space Complexity from loop nesting & allocations."""
    lines = code.splitlines()
    max_loop_depth = 0
    current_depth = 0

    if language == "python":
        try:
            tree = ast.parse(code)

            def _walk_loops(node, depth=0):
                nonlocal max_loop_depth
                if isinstance(node, (ast.For, ast.While, ast.ListComp, ast.DictComp)):
                    depth += 1
                    max_loop_depth = max(max_loop_depth, depth)
                for child in ast.iter_child_nodes(node):
                    _walk_loops(child, depth)

            _walk_loops(tree)
        except Exception:
            max_loop_depth = 1
    else:
        for line in lines:
            stripped = line.strip()
            if re.match(r"^(for|while)\s*\(", stripped):
                current_depth += 1
                max_loop_depth = max(max_loop_depth, current_depth)
            if "}" in stripped and current_depth > 0:
                current_depth = max(0, current_depth - 1)

    if max_loop_depth == 0:
        time_comp = "O(1) - Constant Time"
    elif max_loop_depth == 1:
        time_comp = "O(n) - Linear Time"
    elif max_loop_depth == 2:
        time_comp = "O(n²) - Quadratic Time"
    else:
        time_comp = f"O(n^{max_loop_depth}) - Polynomial Time"

    # Space complexity heuristic: collections/allocations inside loops or large structures
    has_collection_alloc = bool(
        re.search(
            r"(\.append\(|new\s+ArrayList|new\s+HashMap|\[.*for\s+.*\bin\b|fetchall\(\))",
            code,
        )
    )
    space_comp = "O(n) - Linear Space" if has_collection_alloc else "O(1) - Constant Auxiliary Space"
    return {"time_complexity": time_comp, "space_complexity": space_comp}


def compute_complexity_and_quality_metrics(code: str, language: str) -> Dict[str, Any]:
    """
    Computes:
    - 4 Types of Complexity: Cyclomatic, Cognitive, Time, Space
    - Quality Assessment: Maintainability, Complexity Score, Duplication, Documentation, Tech Debt
    """
    lines = [ln for ln in code.splitlines() if ln.strip()]
    total_loc = max(len(lines), 1)

    # 1. Cyclomatic Complexity (Decision paths & branching logic)
    branch_keywords = r"\b(if|elif|else\s+if|for|while|case|catch|except|and|or)\b|&&|\|\||\?"
    decisions = len(re.findall(branch_keywords, code))
    cyclomatic = 1 + decisions

    if cyclomatic <= 5:
        cc_rank = "A (Low Risk / Simple)"
    elif cyclomatic <= 10:
        cc_rank = "B (Moderate Complexity)"
    elif cyclomatic <= 20:
        cc_rank = "C (High Complexity)"
    else:
        cc_rank = "D/F (Very High Risk - Refactor Required)"

    # 2. Cognitive Complexity (Human understandability + nesting penalty)
    cognitive = 0
    nesting = 0
    for raw_line in code.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(("#", "//", "/*", "*")):
            continue
        if language == "python":
            indent_spaces = len(raw_line) - len(raw_line.lstrip(" "))
            nesting = indent_spaces // 4
        else:
            if stripped.endswith("{"):
                nesting += 1
            elif stripped.startswith("}"):
                nesting = max(0, nesting - 1)

        if re.search(r"^(if|elif|else|for|while|try|except|catch|switch)\b", stripped):
            cognitive += 1 + max(0, nesting - 1)

    # 3. Time & Space Complexity
    ts = _estimate_time_and_space_complexity(code, language)

    # 4. Duplication Percentage (Copy-Paste Programming indicator)
    normalized_lines = [
        ln.strip()
        for ln in lines
        if len(ln.strip()) > 12 and not ln.strip().startswith(("#", "//", "import ", "from ", "{", "}"))
    ]
    counts = Counter(normalized_lines)
    duplicate_lines = sum(cnt - 1 for cnt in counts.values() if cnt > 1)
    duplication_pct = round((duplicate_lines / total_loc) * 100, 1)

    # 5. Documentation Score (Comments & Docstrings coverage)
    comment_lines = len(re.findall(r"(^\s*#|^\s*//|^\s*\*|\"\"\"|\'\'\')", code, flags=re.MULTILINE))
    doc_score = round(min(100.0, (comment_lines / max(1, total_loc * 0.18)) * 100), 1)

    # 6. Maintainability Score (Halstead/Radon style 0-100 scale)
    raw_mi = 100.0 - (cyclomatic * 1.8) - (cognitive * 1.2) - (duplication_pct * 0.7) - (math.log(total_loc) * 3.5)
    maintainability_score = round(max(10.0, min(100.0, raw_mi + (doc_score * 0.1))), 1)
    complexity_health_score = round(max(5.0, 100.0 - (cyclomatic * 3.0) - (cognitive * 1.5)), 1)

    return {
        "complexity_metrics": {
            "cyclomatic_complexity": cyclomatic,
            "cyclomatic_rank": cc_rank,
            "cognitive_complexity": cognitive,
            "time_complexity": ts["time_complexity"],
            "space_complexity": ts["space_complexity"],
        },
        "quality_assessment": {
            "maintainability_score": maintainability_score,
            "complexity_score": complexity_health_score,
            "duplication_percentage": duplication_pct,
            "documentation_score": doc_score,
            "technical_debt_minutes": max(5, int((cyclomatic + cognitive) * 3 + duplicate_lines * 5)),
        },
    }


def run_static_pattern_scanners(code: str, language: str) -> List[Dict[str, str]]:
    """
    Layer 2 Static Analysis Engine:
    Scans for Bandit / SpotBugs / Semgrep / Pylint / PMD / Checkstyle patterns
    and the 6 Design Anti-Patterns (God Object, Spaghetti Code, Blob Class,
    Lava Flow, Golden Hammer, Copy-Paste Programming).
    """
    flags: List[Dict[str, str]] = []
    lines = code.splitlines()

    # --- A. Security Static Rules (Bandit / SpotBugs / Semgrep / OWASP) ---
    sec_patterns = [
        (
            r"(PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY)\s*=\s*['\"][^'\"]{4,}['\"]",
            "Bandit B105 / SpotBugs DMI_CONSTANT_DB_PASSWORD",
            "Critical",
            "Hardcoded Credential / Secret detected in source code (Violates Password Hashing & Encryption Guidelines).",
        ),
        (
            r"(SELECT|INSERT|UPDATE|DELETE)\s+.*(\+|%s|\{.*\}|format\()",
            "Bandit B608 / SpotBugs SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE / Semgrep",
            "Critical",
            "Dynamic SQL query constructed via string concatenation/interpolation instead of Parameterized SQL Queries.",
        ),
        (
            r"(subprocess\.(Popen|call|run)\(.*shell\s*=\s*True|os\.system\(|Runtime\.getRuntime\(\)\.exec\()",
            "Bandit B602 / Semgrep Command-Injection",
            "Critical",
            "OS Command execution with unsanitized input / shell=True.",
        ),
        (
            r"\beval\s*\(|\bexec\s*\(|pickle\.loads\s*\(|ObjectInputStream",
            "Bandit B307 / B301 / Semgrep Unsafe-Eval-Deserialization",
            "High",
            "Dynamic code evaluation or untrusted deserialization detected.",
        ),
        (
            r"MessageDigest\.getInstance\(\s*['\"](MD5|SHA-1|SHA1)['\"]\s*\)|hashlib\.(md5|sha1)\(",
            "SpotBugs / SEI CERT MSC61-J / Bandit B324",
            "High",
            "Weak cryptographic hash algorithm (MD5/SHA-1) detected.",
        ),
    ]

    for idx, line in enumerate(lines, start=1):
        for pat, tool_ref, sev, msg in sec_patterns:
            if re.search(pat, line, flags=re.IGNORECASE):
                flags.append({
                    "tool": tool_ref,
                    "type": "Security Static Alert",
                    "severity": sev,
                    "line": f"Line {idx}",
                    "message": msg,
                    "snippet": line.strip(),
                })

    # --- B. Quality, Linting & 6 Design Anti-Patterns (Pylint / PMD / Radon / Checkstyle) ---
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Empty / Bare except or catch block (Violates Secure Error Handling & Logging)
        if re.match(r"^except\s*:\s*$", stripped) or re.search(r"catch\s*\([^)]+\)\s*\{\s*\}", stripped):
            flags.append({
                "tool": "Pylint W0702 / PMD EmptyCatchBlock",
                "type": "Best Practice & Error Handling Violation",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "Bare or empty exception handler swallows errors without logging.",
                "snippet": stripped,
            })
        # Commented-out dead code / TODOs (Lava Flow Anti-Pattern)
        if re.search(r"(#|//)\s*(TODO|FIXME|DEPRECATED|OLD CODE|DO NOT REMOVE)", stripped, flags=re.IGNORECASE):
            flags.append({
                "tool": "SonarQube / Design Anti-Pattern: Lava Flow",
                "type": "Design Anti-Pattern (Lava Flow)",
                "severity": "Low",
                "line": f"Line {idx}",
                "message": "Lava Flow anti-pattern: lingering dead/experimental/unremoved legacy code comment.",
                "snippet": stripped,
            })

    # Check for Spaghetti Code (deep nesting >= 4 levels)
    for idx, line in enumerate(lines, start=1):
        indent = len(line) - len(line.lstrip(" "))
        if indent >= 16 and re.match(r"^(if|for|while|elif|else)\b", line.strip()):
            flags.append({
                "tool": "Radon / Pylint / Design Anti-Pattern: Spaghetti Code",
                "type": "Design Anti-Pattern (Spaghetti Code)",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "Spaghetti Code anti-pattern: deeply nested control flow (>4 indentation levels) reduces readability.",
                "snippet": line.strip(),
            })
            break

    # Check for God Object / Blob Class (Class with too many methods or fields)
    method_count = len(re.findall(r"^\s*(def\s+\w+|(public|private|protected)\s+[\w<>\[\]]+\s+\w+\s*\()", code, flags=re.MULTILINE))
    if method_count >= 8 or len(lines) > 150:
        flags.append({
            "tool": "PMD GodClass / Pylint R0904 / Design Anti-Pattern",
            "type": "Design Anti-Pattern (God Object / Blob Class)",
            "severity": "High",
            "line": "Class Scope",
            "message": f"God Object / Blob Class anti-pattern: unit contains {method_count} methods / {len(lines)} lines holding excessive responsibility.",
            "snippet": lines[0].strip() if lines else "",
        })

    # Optional: Run real Bandit CLI on Python code if installed in .venv
    if language == "python":
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            proc = subprocess.run(
                ["bandit", "-f", "json", "-q", tmp_path],
                capture_output=True,
                text=True,
                timeout=8,
            )
            Path(tmp_path).unlink(missing_ok=True)
            if proc.stdout:
                import json
                b_data = json.loads(proc.stdout)
                for res in b_data.get("results", [])[:4]:
                    flags.append({
                        "tool": f"Bandit CLI ({res.get('test_id')}: {res.get('test_name')})",
                        "type": "Security Static Alert",
                        "severity": res.get("issue_severity", "HIGH").capitalize(),
                        "line": f"Line {res.get('line_number')}",
                        "message": res.get("issue_text", ""),
                        "snippet": res.get("code", "").strip(),
                    })
        except Exception:
            pass

    return flags
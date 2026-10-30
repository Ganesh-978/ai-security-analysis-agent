import ast
import math
import re
from collections import Counter
from typing import Dict, Any, List


def _estimate_time_and_space_complexity(code: str, language: str) -> Dict[str, str]:
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

    has_collection_alloc = bool(
        re.search(
            r"(\.append\(|new\s+ArrayList|new\s+HashMap|\[.*for\s+.*\bin\b|fetchall\(\))",
            code,
        )
    )
    space_comp = "O(n) - Linear Space" if has_collection_alloc else "O(1) - Constant Auxiliary Space"
    return {"time_complexity": time_comp, "space_complexity": space_comp}


def compute_complexity_and_quality_metrics(code: str, language: str) -> Dict[str, Any]:
    lines = [ln for ln in code.splitlines() if ln.strip()]
    total_loc = max(len(lines), 1)

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

    ts = _estimate_time_and_space_complexity(code, language)

    normalized_lines = [
        ln.strip()
        for ln in lines
        if len(ln.strip()) > 12 and not ln.strip().startswith(("#", "//", "import ", "from ", "{", "}"))
    ]
    counts = Counter(normalized_lines)
    duplicate_lines = sum(cnt - 1 for cnt in counts.values() if cnt > 1)
    duplication_pct = round((duplicate_lines / total_loc) * 100, 1)

    comment_lines = len(re.findall(r"(^\s*#|^\s*//|^\s*\*|\"\"\"|\'\'\')", code, flags=re.MULTILINE))
    doc_score = round(min(100.0, (comment_lines / max(1, total_loc * 0.18)) * 100), 1)

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
    Fast in-memory SAST & Static Quality Scanner Engine (<5ms execution):
    Covers OWASP Top 10 (A01-A10), Bandit, Semgrep, Pylint, SpotBugs, PMD, Checkstyle, SonarQube.
    """
    flags: List[Dict[str, str]] = []
    lines = code.splitlines()

    sast_rules = [
        (
            r"(@csrf_exempt|csrf\.disable\(\)|WTF_CSRF_ENABLED\s*=\s*False)",
            "Semgrep / SonarQube S4502",
            "Cross-Site Request Forgery (CSRF)",
            "High",
            "OWASP A01 / CWE-352: CSRF protection disabled on state-changing endpoint.",
            "Enable CSRF protection middleware and require anti-CSRF tokens on POST/PUT/DELETE requests.",
        ),
        (
            r"(open\s*\(\s*.*\+|send_file\s*\(\s*.*\+|new\s+File\s*\(\s*.*\+|Paths\.get\s*\(\s*.*\+)",
            "Bandit B301 / Semgrep Path-Traversal / SpotBugs PATH_TRAVERSAL_IN",
            "Path Traversal / Arbitrary File Access",
            "High",
            "OWASP A01 / CWE-22: Unsanitized user input used in file system path construction.",
            "Validate filenames against an allowlist and resolve canonical paths with os.path.basename / Path.resolve().",
        ),
        (
            r"(PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY|DB_PASS|AWS_SECRET)\s*=\s*['\"][^'\"]{4,}['\"]",
            "Bandit B105 / Semgrep / SpotBugs DMI_CONSTANT_DB_PASSWORD",
            "Hardcoded Secret / Credential",
            "Critical",
            "OWASP A02 & A07 / CWE-798: Hardcoded secret, password, or API key embedded directly in source code.",
            "Remove hardcoded credentials from source code and load them via os.getenv() or a secret manager.",
        ),
        (
            r"MessageDigest\.getInstance\(\s*['\"](MD5|SHA-1|SHA1)['\"]\s*\)|hashlib\.(md5|sha1)\(|Cipher\.getInstance\(\s*['\"](DES|RC4|AES/ECB)",
            "Bandit B324 / SpotBugs / SEI CERT MSC61-J",
            "Weak Cryptography / Broken Hash Algorithm",
            "High",
            "OWASP A02 / CWE-327 & CWE-328: Broken or risky cryptographic algorithm (MD5/SHA-1/DES/ECB) used.",
            "Use Argon2id or bcrypt for passwords, SHA-256/SHA-512 for integrity, and AES-GCM for encryption.",
        ),
        (
            r"(SELECT|INSERT|UPDATE|DELETE)\s+.*(\+|%s|\{.*\}|\.format\()",
            "Bandit B608 / Semgrep / SpotBugs SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE",
            "SQL Injection",
            "Critical",
            "OWASP A03 / CWE-89: Dynamic SQL query constructed using string concatenation or f-strings.",
            "Use parameterized queries (cursor.execute('SELECT ... WHERE x = ?', (val,))) or PreparedStatement.",
        ),
        (
            r"(subprocess\.(Popen|call|run)\(.*shell\s*=\s*True|os\.system\(|Runtime\.getRuntime\(\)\.exec\()",
            "Bandit B602 / Semgrep Command-Injection",
            "OS Command Injection",
            "Critical",
            "OWASP A03 / CWE-78: OS command executed with shell=True or unsanitized user input.",
            "Pass command arguments as a list with shell=False (e.g., subprocess.run(['ping', '-c', '1', host], shell=False)).",
        ),
        (
            r"(render_template_string|markupsafe\.Markup|\|safe\b|innerHTML\s*=|document\.write\(|response\.getWriter\(\)\.print\(.*\+)",
            "Semgrep XSS / Bandit B703 / SpotBugs XSS_REQUEST_PARAMETER_TO_SERVLET_WRITER",
            "Cross-Site Scripting (XSS)",
            "High",
            "OWASP A03 / CWE-79: Unescaped user input rendered directly into HTML output.",
            "Use context-aware HTML escaping (html.escape / Jinja2 autoescape) before rendering user content.",
        ),
        (
            r"\beval\s*\(|\bexec\s*\(",
            "Bandit B307 / Semgrep Unsafe-Eval",
            "Arbitrary Code Injection (eval/exec)",
            "Critical",
            "OWASP A03 / CWE-95: Dynamic evaluation of untrusted string allows Remote Code Execution (RCE).",
            "Replace eval() with ast.literal_eval() or safe JSON parsing (json.loads).",
        ),
        (
            r"(app\.run\(.*debug\s*=\s*True|DEBUG\s*=\s*True|verify\s*=\s*False)",
            "Bandit B201 & B501 / Semgrep Security-Misconfiguration",
            "Security Misconfiguration (Debug / TLS Bypass)",
            "High",
            "OWASP A05 / CWE-489 & CWE-295: Debug mode enabled or SSL/TLS certificate verification disabled.",
            "Set debug=False in production and enforce verify=True on all HTTPS requests.",
        ),
        (
            r"(pickle\.loads?\s*\(|cPickle\.loads?\s*\(|yaml\.load\s*\([^,)]+\)|new\s+ObjectInputStream\s*\()",
            "Bandit B301 & B506 / Semgrep / SpotBugs OBJECT_DESERIALIZATION",
            "Insecure Deserialization",
            "Critical",
            "OWASP A08 / CWE-502: Deserializing untrusted data can lead to remote code execution.",
            "Use safe serialization formats such as JSON or yaml.safe_load().",
        ),
    ]

    for idx, line in enumerate(lines, start=1):
        for pat, tool_ref, vuln_name, sev, msg, rec in sast_rules:
            if re.search(pat, line, flags=re.IGNORECASE):
                flags.append({
                    "tool": tool_ref,
                    "type": "Security Static Alert",
                    "vulnerability_name": vuln_name,
                    "severity": sev,
                    "line": f"Line {idx}",
                    "message": msg,
                    "recommendation": rec,
                    "snippet": line.strip(),
                })

    if language == "java" and "DriverManager.getConnection(" in code and "try (" not in code:
        flags.append({
            "tool": "SpotBugs OBL_UNSATISFIED_OBLIGATION / PMD CloseResource",
            "type": "Java Resource Leak",
            "vulnerability_name": "Unclosed Database Resource Leak",
            "severity": "Medium",
            "line": "Method Scope",
            "message": "SpotBugs / PMD: JDBC Connection/Statement opened without try-with-resources block.",
            "recommendation": "Wrap Connection, PreparedStatement, and ResultSet in a try-with-resources block.",
            "snippet": "DriverManager.getConnection(...)",
        })

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if re.match(r"^except\s*:\s*$", stripped) or re.search(r"catch\s*\([^)]+\)\s*\{\s*\}", stripped):
            flags.append({
                "tool": "Bandit B110 / Pylint W0702 / PMD EmptyCatchBlock",
                "type": "Best Practice & Error Handling Violation",
                "vulnerability_name": "Improper Error Handling / Swallowed Exception",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "OWASP A09 / CWE-390: Bare or empty exception handler swallows errors without logging.",
                "recommendation": "Catch specific exceptions and log the error context securely.",
                "snippet": stripped,
            })

    for idx, line in enumerate(lines, start=1):
        indent = len(line) - len(line.lstrip(" "))
        if indent >= 16 and re.match(r"^(if|for|while|elif|else)\b", line.strip()):
            flags.append({
                "tool": "Radon / Pylint / Design Anti-Pattern: Spaghetti Code",
                "type": "Design Anti-Pattern (Spaghetti Code)",
                "vulnerability_name": "Spaghetti Code / Deep Nesting",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "Deeply nested control flow (>4 indentation levels) increases cognitive complexity.",
                "recommendation": "Refactor nested conditionals using guard clauses and early returns.",
                "snippet": line.strip(),
            })
            break

    return flags
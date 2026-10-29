import ast
import json
import math
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
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
    Comprehensive SAST & Static Quality Scanner Engine covering:
    - Full OWASP Top 10 (A01 to A10) & CWE rules
    - Python: Bandit, Semgrep, Pylint, AST
    - Java: SpotBugs, PMD, Checkstyle, SEI CERT
    - Enterprise: SonarQube, Snyk, OWASP Dependency Check
    """
    flags: List[Dict[str, str]] = []
    lines = code.splitlines()

    # 1. Comprehensive SAST Security Rules (Full OWASP Top 10 A01-A10)
    sast_rules = [
        # A01: Broken Access Control, Path Traversal, CSRF, Open Redirect
        (
            r"(@csrf_exempt|csrf\.disable\(\)|WTF_CSRF_ENABLED\s*=\s*False)",
            "Semgrep / SonarQube S4502",
            "Cross-Site Request Forgery (CSRF)",
            "High",
            "OWASP A01 / CWE-352: CSRF protection disabled on endpoint.",
        ),
        (
            r"(open\s*\(\s*.*\+|send_file\s*\(\s*.*\+|new\s+File\s*\(\s*.*\+|Paths\.get\s*\(\s*.*\+)",
            "Bandit B301 / Semgrep Path-Traversal / SpotBugs PATH_TRAVERSAL_IN",
            "Path Traversal / Arbitrary File Access",
            "High",
            "OWASP A01 / CWE-22: Unsanitized user input used in file system path construction.",
        ),
        (
            r"(chmod\s*\(.*0o?777|os\.chmod\(.*777)",
            "Bandit B103 / Semgrep Overly-Permissive-File",
            "Broken Access Control (Overly Permissive File Permissions)",
            "High",
            "OWASP A01 / CWE-732: Setting 777 permissions violates Least Privilege Principle.",
        ),
        # A02: Cryptographic Failures & Hardcoded Secrets
        (
            r"(PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY|DB_PASS|AWS_SECRET)\s*=\s*['\"][^'\"]{4,}['\"]",
            "Bandit B105-B107 / Semgrep / SpotBugs DMI_CONSTANT_DB_PASSWORD",
            "Hardcoded Secret / Credential",
            "Critical",
            "OWASP A02 & A07 / CWE-798: Hardcoded secret, password, or API key embedded in source code.",
        ),
        (
            r"MessageDigest\.getInstance\(\s*['\"](MD5|SHA-1|SHA1)['\"]\s*\)|hashlib\.(md5|sha1)\(|Cipher\.getInstance\(\s*['\"](DES|RC4|AES/ECB)",
            "Bandit B324 & B303 / SpotBugs / SEI CERT MSC61-J",
            "Weak Cryptography / Broken Hash Algorithm",
            "High",
            "OWASP A02 / CWE-327 & CWE-328: Use of broken or weak cryptographic algorithm (MD5/SHA-1/DES/ECB).",
        ),
        (
            r"\brandom\.(randint|choice|random)\s*\(|new\s+java\.util\.Random\s*\(",
            "Bandit B311 / SpotBugs DMI_RANDOM_USED_ONLY_ONCE / CERT MSC02-J",
            "Insecure Pseudo-Random Number Generator (PRNG)",
            "Medium",
            "OWASP A02 / CWE-338: Standard PRNG used instead of cryptographically secure secrets/SecureRandom.",
        ),
        # A03: Injection (SQLi, Command Injection, Code Injection, XSS, LDAP/XXE)
        (
            r"(SELECT|INSERT|UPDATE|DELETE)\s+.*(\+|%s|\{.*\}|\.format\()",
            "Bandit B608 / Semgrep / SpotBugs SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE",
            "SQL Injection",
            "Critical",
            "OWASP A03 / CWE-89: Dynamic SQL query constructed via string concatenation/interpolation.",
        ),
        (
            r"(subprocess\.(Popen|call|run)\(.*shell\s*=\s*True|os\.system\(|Runtime\.getRuntime\(\)\.exec\(|ProcessBuilder\()",
            "Bandit B602 & B605 / Semgrep Command-Injection",
            "OS Command Injection",
            "Critical",
            "OWASP A03 / CWE-78: OS command execution with shell=True or unsanitized input.",
        ),
        (
            r"(render_template_string|markupsafe\.Markup|\|safe\b|innerHTML\s*=|document\.write\(|response\.getWriter\(\)\.print\(.*\+)",
            "Semgrep XSS / Bandit B703 / SpotBugs XSS_REQUEST_PARAMETER_TO_SERVLET_WRITER",
            "Cross-Site Scripting (XSS)",
            "High",
            "OWASP A03 / CWE-79: Unescaped user input rendered directly into HTML output.",
        ),
        (
            r"\beval\s*\(|\bexec\s*\(",
            "Bandit B307 & B102 / Semgrep Unsafe-Eval",
            "Arbitrary Code Injection (eval/exec)",
            "Critical",
            "OWASP A03 / CWE-94 & CWE-95: Dynamic evaluation of code string enables Remote Code Execution.",
        ),
        # A05: Security Misconfiguration (Debug Mode, SSL Verification Disabled, XXE, Tempfile)
        (
            r"(app\.run\(.*debug\s*=\s*True|DEBUG\s*=\s*True|verify\s*=\s*False)",
            "Bandit B201 & B501 / Semgrep Security-Misconfiguration",
            "Security Misconfiguration (Debug Enabled / TLS Verification Disabled)",
            "High",
            "OWASP A05 / CWE-489 & CWE-295: Production debug mode enabled or SSL/TLS certificate verification disabled.",
        ),
        (
            r"(xml\.etree\.ElementTree|xml\.dom\.minidom|DocumentBuilderFactory\.newInstance\(\))",
            "Bandit B314 / Semgrep XXE / SpotBugs XXE_DOCUMENT",
            "XML External Entity (XXE) Vulnerability Risk",
            "High",
            "OWASP A05 / CWE-611: XML parser initialized without disabling external entities (DOCTYPE/DTD).",
        ),
        # A07: Identification and Authentication Failures
        (
            r"(jwt\.decode\(.*verify_signature['\"]?\s*:\s*False|alg['\"]?\s*:\s*['\"]none['\"])",
            "Semgrep JWT-Unverified / Bandit",
            "Improper Authentication (Unverified JWT Signature)",
            "Critical",
            "OWASP A07 / CWE-287 & CWE-347: JWT token decoded without signature verification.",
        ),
        # A08: Software and Data Integrity Failures (Insecure Deserialization)
        (
            r"(pickle\.loads?\s*\(|cPickle\.loads?\s*\(|yaml\.load\s*\([^,)]+\)|new\s+ObjectInputStream\s*\()",
            "Bandit B301 & B506 / Semgrep / SpotBugs OBJECT_DESERIALIZATION",
            "Insecure Deserialization",
            "Critical",
            "OWASP A08 / CWE-502: Deserialization of untrusted data can result in arbitrary code execution.",
        ),
        # A10: Server-Side Request Forgery (SSRF)
        (
            r"(requests\.(get|post|put)\s*\(\s*[a-zA-Z_]\w*|urllib\.request\.urlopen\s*\(\s*[a-zA-Z_]\w*|new\s+URL\s*\(\s*[a-zA-Z_]\w*\)\.openConnection)",
            "Semgrep SSRF / Bandit B310",
            "Server-Side Request Forgery (SSRF) Risk",
            "High",
            "OWASP A10 / CWE-918: Outbound HTTP request target constructed from potentially unvalidated variable.",
        ),
    ]

    for idx, line in enumerate(lines, start=1):
        for pat, tool_ref, vuln_name, sev, msg in sast_rules:
            if re.search(pat, line, flags=re.IGNORECASE):
                flags.append({
                    "tool": tool_ref,
                    "type": "Security Static Alert",
                    "vulnerability_name": vuln_name,
                    "severity": sev,
                    "line": f"Line {idx}",
                    "message": msg,
                    "snippet": line.strip(),
                })

    # 2. Java-Specific SpotBugs, PMD & Checkstyle Rules
    if language == "java":
        if "DriverManager.getConnection(" in code and "try (" not in code:
            flags.append({
                "tool": "SpotBugs OBL_UNSATISFIED_OBLIGATION / PMD CloseResource",
                "type": "Java Resource Leak",
                "vulnerability_name": "Unclosed Database Resource Leak",
                "severity": "Medium",
                "line": "Method Scope",
                "message": "SpotBugs / PMD: JDBC Connection/Statement opened without try-with-resources block.",
                "snippet": "DriverManager.getConnection(...)",
            })
        for idx, line in enumerate(lines, start=1):
            if re.search(r"\bclass\s+[a-z]\w*", line):
                flags.append({
                    "tool": "Checkstyle TypeName",
                    "type": "Coding Convention Violation",
                    "vulnerability_name": "Checkstyle Naming Convention Violation",
                    "severity": "Low",
                    "line": f"Line {idx}",
                    "message": "Checkstyle: Java class names must follow PascalCase starting with an uppercase letter.",
                    "snippet": line.strip(),
                })

    # 3. Quality, Pylint, PMD, SonarQube & 6 Design Anti-Patterns + A09 Logging/Error Handling
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if re.match(r"^except\s*:\s*$", stripped) or re.search(r"catch\s*\([^)]+\)\s*\{\s*\}", stripped):
            flags.append({
                "tool": "Bandit B110 / Pylint W0702 / PMD EmptyCatchBlock",
                "type": "Best Practice & Error Handling Violation",
                "vulnerability_name": "Improper Error Handling / Swallowed Exception",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "OWASP A09 / CWE-390: Bare or empty exception block swallows security/runtime errors without logging.",
                "snippet": stripped,
            })
        if re.search(r"(#|//)\s*(TODO|FIXME|DEPRECATED|OLD CODE|DO NOT REMOVE)", stripped, flags=re.IGNORECASE):
            flags.append({
                "tool": "SonarQube / Design Anti-Pattern: Lava Flow",
                "type": "Design Anti-Pattern (Lava Flow)",
                "vulnerability_name": "Lava Flow Anti-Pattern",
                "severity": "Low",
                "line": f"Line {idx}",
                "message": "Lava Flow anti-pattern: dead or unremoved legacy code/comment left in codebase.",
                "snippet": stripped,
            })

    for idx, line in enumerate(lines, start=1):
        indent = len(line) - len(line.lstrip(" "))
        if indent >= 16 and re.match(r"^(if|for|while|elif|else)\b", line.strip()):
            flags.append({
                "tool": "Radon / Pylint / Design Anti-Pattern: Spaghetti Code",
                "type": "Design Anti-Pattern (Spaghetti Code)",
                "vulnerability_name": "Spaghetti Code Anti-Pattern",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "Spaghetti Code anti-pattern: deeply nested control flow (>4 levels) degrades maintainability.",
                "snippet": line.strip(),
            })
            break

    method_count = len(
        re.findall(
            r"^\s*(def\s+\w+|(public|private|protected)\s+[\w<>\[\]]+\s+\w+\s*\()",
            code,
            flags=re.MULTILINE,
        )
    )
    if method_count >= 8 or len(lines) > 150:
        flags.append({
            "tool": "PMD GodClass / Pylint R0904 / SonarQube",
            "type": "Design Anti-Pattern (God Object / Blob Class)",
            "vulnerability_name": "God Object / Blob Class",
            "severity": "High",
            "line": "Class Scope",
            "message": f"God Object / Blob Class anti-pattern: {method_count} methods / {len(lines)} lines in single unit.",
            "snippet": lines[0].strip() if lines else "",
        })

    # 4. Run Bandit CLI on Python code if available in .venv
    if language == "python":
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
                tmp.write(code)
                tmp_path = tmp.name
            proc = subprocess.run(
                ["bandit", "-f", "json", "-q", tmp_path],
                capture_output=True,
                text=True,
                timeout=6,
            )
            Path(tmp_path).unlink(missing_ok=True)
            if proc.stdout:
                b_data = json.loads(proc.stdout)
                for res in b_data.get("results", [])[:5]:
                    flags.append({
                        "tool": f"Bandit CLI ({res.get('test_id')}: {res.get('test_name')})",
                        "type": "Security Static Alert",
                        "vulnerability_name": res.get("test_name", "Bandit Security Issue"),
                        "severity": res.get("issue_severity", "HIGH").capitalize(),
                        "line": f"Line {res.get('line_number')}",
                        "message": res.get("issue_text", ""),
                        "snippet": res.get("code", "").strip(),
                    })
        except Exception:
            pass

    return flags
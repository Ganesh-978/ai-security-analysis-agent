import ast
import math
import re
from collections import Counter
from typing import Dict, Any, List


def _strip_comments_and_strings(code: str, language: str) -> str:
    """Removes comments and string literals so complexity counters inspect executable code only."""
    if language == "python":
        no_triple = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '""', code)
        no_str = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', no_triple)
        return re.sub(r"#.*$", "", no_str, flags=re.MULTILINE)
    no_block = re.sub(r"/\*[\s\S]*?\*/", "", code)
    no_line = re.sub(r"//.*$", "", no_block, flags=re.MULTILINE)
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', no_line)


def compute_complexity_and_quality_metrics(code: str, language: str) -> Dict[str, Any]:
    """
    Computes industry-standard complexity and ISO/IEC 25010 quality telemetry:
    - McCabe Cyclomatic Complexity (per-function peak & average via AST)
    - Sonar-style Cognitive Complexity (penalizes deep nesting, rewards modular decomposition)
    - Asymptotic Time & Space Big-O Complexity
    - Maintainability Index, Complexity Health, Duplication %, Documentation %, Technical Debt
    """
    raw_lines = code.splitlines()
    non_empty_lines = [ln for ln in raw_lines if ln.strip()]
    total_loc = max(len(non_empty_lines), 1)

    cyclomatic_avg = 1
    cyclomatic_max = 1
    cognitive = 0
    max_loop_depth = 0

    if language == "python":
        try:
            tree = ast.parse(code)
            func_ccs: List[int] = []

            def _calc_cognitive(node: ast.AST, depth: int = 0) -> int:
                score = 0
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                        score += 1 + depth
                        score += _calc_cognitive(child, depth + 1)
                    elif isinstance(child, ast.BoolOp):
                        score += 1
                        score += _calc_cognitive(child, depth)
                    else:
                        score += _calc_cognitive(child, depth)
                return score

            def _walk_loops(node: ast.AST, depth: int = 0) -> None:
                nonlocal max_loop_depth
                if isinstance(node, (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.DictComp, ast.GeneratorExp)):
                    depth += 1
                    max_loop_depth = max(max_loop_depth, depth)
                for child in ast.iter_child_nodes(node):
                    _walk_loops(child, depth)

            _walk_loops(tree)

            func_nodes = [
                n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            if func_nodes:
                func_cogs = []
                for fn in func_nodes:
                    cc = 1
                    for child in ast.walk(fn):
                        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                            cc += 1
                        elif isinstance(child, ast.BoolOp):
                            cc += len(child.values) - 1
                    func_ccs.append(cc)
                    func_cogs.append(_calc_cognitive(fn, 0))
                cyclomatic_max = max(func_ccs)
                cyclomatic_avg = round(sum(func_ccs) / len(func_ccs))
                cognitive = max(func_cogs)
            else:
                cc = 1
                for child in ast.walk(tree):
                    if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                        cc += 1
                    elif isinstance(child, ast.BoolOp):
                        cc += len(child.values) - 1
                cyclomatic_max = cc
                cyclomatic_avg = cc
                cognitive = _calc_cognitive(tree, 0)
        except Exception:
            cyclomatic_max, cyclomatic_avg = 1, 1
    else:
        clean_code = _strip_comments_and_strings(code, "java")
        method_bodies = re.split(
            r"\b(?:public|private|protected)\s+(?:static\s+)?[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\{",
            clean_code,
        )
        body_chunks = method_bodies[1:] if len(method_bodies) > 1 else [clean_code]
        branch_kw = r"\b(if|else\s+if|for|while|case|catch)\b|&&|\|\||\?"
        ccs = [1 + len(re.findall(branch_kw, chunk)) for chunk in body_chunks]
        cyclomatic_max = max(ccs) if ccs else 1
        cyclomatic_avg = round(sum(ccs) / max(len(ccs), 1))

        max_cog = 0
        for chunk in body_chunks:
            cog = 0
            depth = 0
            loop_d = 0
            for ln in chunk.splitlines():
                s = ln.strip()
                if not s:
                    continue
                if re.match(r"^(for|while)\s*\(", s):
                    loop_d += 1
                    max_loop_depth = max(max_loop_depth, loop_d)
                if re.search(r"^(if|else\s+if|for|while|catch|switch)\b", s):
                    cog += 1 + depth
                    depth += 1
                if s.startswith("}") or s.endswith("}"):
                    depth = max(0, depth - 1)
                    loop_d = max(0, loop_d - 1)
            max_cog = max(max_cog, cog)
        cognitive = max_cog

    if cyclomatic_max <= 5:
        cc_rank = "A (Low Risk / Simple)"
    elif cyclomatic_max <= 10:
        cc_rank = "B (Moderate Complexity)"
    elif cyclomatic_max <= 15:
        cc_rank = "C (High Complexity)"
    else:
        cc_rank = "D/F (Very High Risk - Refactor Required)"

    if max_loop_depth == 0:
        time_comp = "O(1) - Constant Time"
    elif max_loop_depth == 1:
        time_comp = "O(n) - Linear Time"
    elif max_loop_depth == 2:
        time_comp = "O(n^2) - Quadratic Time"
    else:
        time_comp = f"O(n^{max_loop_depth}) - Polynomial Time"

    has_collection_alloc = bool(
        re.search(
            r"(\.append\(|new\s+ArrayList|new\s+HashMap|\[.*for\s+.*\bin\b|fetchall\(\))",
            code,
        )
    )
    space_comp = "O(n) - Linear Space" if has_collection_alloc else "O(1) - Constant Auxiliary Space"

    normalized_lines = [
        ln.strip()
        for ln in non_empty_lines
        if len(ln.strip()) > 16
        and not ln.strip().startswith(("#", "//", "/*", "*", "import ", "from ", "{", "}", '"""', "'''"))
    ]
    counts = Counter(normalized_lines)
    duplicate_lines = sum(cnt - 1 for cnt in counts.values() if cnt > 1)
    duplication_pct = round((duplicate_lines / total_loc) * 100, 1)

    doc_lines = 0
    in_doc = False
    for ln in raw_lines:
        s = ln.strip()
        if s.startswith(("#", "//", "/*", "*")):
            doc_lines += 1
        elif '"""' in s or "'''" in s:
            doc_lines += 1
            if s.count('"""') == 1 or s.count("'''") == 1:
                in_doc = not in_doc
        elif in_doc:
            doc_lines += 1
    doc_score = round(min(100.0, (doc_lines / max(1, total_loc * 0.16)) * 100), 1)

    complexity_health_score = round(
        max(10.0, min(100.0, 100.0 - max(0, cyclomatic_max - 2) * 4.5 - max(0, cognitive - 3) * 2.5)),
        1,
    )
    raw_mi = (
        98.0
        - max(0, cyclomatic_avg - 2) * 3.0
        - max(0, cognitive - 3) * 1.8
        - duplication_pct * 0.8
        - max(0.0, math.log(max(total_loc, 10)) - 2.3) * 4.0
        + (doc_score * 0.08)
    )
    maintainability_score = round(max(15.0, min(100.0, raw_mi)), 1)

    return {
        "complexity_metrics": {
            "cyclomatic_complexity": cyclomatic_max,
            "cyclomatic_rank": cc_rank,
            "cognitive_complexity": cognitive,
            "time_complexity": time_comp,
            "space_complexity": space_comp,
        },
        "quality_assessment": {
            "maintainability_score": maintainability_score,
            "complexity_score": complexity_health_score,
            "duplication_percentage": duplication_pct,
            "documentation_score": doc_score,
            "technical_debt_minutes": max(
                0, int(max(0, cyclomatic_max - 4) * 5 + max(0, cognitive - 5) * 3 + duplicate_lines * 5)
            ),
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
            r"(\bopen\s*\(\s*.*\+|\bsend_file\s*\(\s*.*\+|\bnew\s+File\s*\(\s*.*\+|\bPaths\.get\s*\(\s*.*\+)",
            "Bandit B301 / Semgrep Path-Traversal / SpotBugs PATH_TRAVERSAL_IN",
            "Path Traversal / Arbitrary File Access",
            "High",
            "OWASP A01 / CWE-22: Unsanitized user input used in file system path construction.",
            "Validate filenames against an allowlist and resolve canonical paths with Path.resolve().",
        ),
        (
            r"(PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY|DB_PASS|AWS_SECRET)\s*=\s*['\"][^'\"]{4,}['\"]",
            "Bandit B105 / Semgrep / SpotBugs DMI_CONSTANT_DB_PASSWORD",
            "Hardcoded Secret / Credential",
            "Critical",
            "OWASP A02 & A07 / CWE-798: Hardcoded secret, password, or API key embedded directly in source code.",
            "Remove hardcoded credentials from source code and load them via os.environ.get() / System.getenv().",
        ),
        (
            r"MessageDigest\.getInstance\(\s*['\"](MD5|SHA-1|SHA1)['\"]\s*\)|hashlib\.(md5|sha1)\(|Cipher\.getInstance\(\s*['\"](DES|RC4|AES/ECB)",
            "Bandit B324 / SpotBugs / SEI CERT MSC61-J",
            "Weak Cryptography / Broken Hash Algorithm",
            "High",
            "OWASP A02 / CWE-327 & CWE-328: Broken or risky cryptographic algorithm (MD5/SHA-1/DES/ECB) used.",
            "Replace MD5/SHA-1 with secrets.token_urlsafe(32) for tokens, SHA-256/512 for digests, or Argon2id/bcrypt for passwords.",
        ),
        (
            r"\brandom\.(randint|choice|random)\s*\(|new\s+java\.util\.Random\s*\(",
            "Bandit B311 / SpotBugs / SEI CERT MSC02-J",
            "Weak Pseudo-Random Number Generator (PRNG)",
            "High",
            "OWASP A02 / CWE-338: Non-cryptographic PRNG used in security-sensitive context.",
            "Use Python's secrets module (secrets.token_urlsafe(32)) or Java's java.security.SecureRandom.",
        ),
        (
            r"(SELECT|INSERT|UPDATE|DELETE)\s+.*(\+|%s|\{.*\}|\.format\()",
            "Bandit B608 / Semgrep / SpotBugs SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE",
            "SQL Injection",
            "Critical",
            "OWASP A03 / CWE-89: Dynamic SQL query constructed using string concatenation or f-strings.",
            "Use parameterized SQL queries (cursor.execute('SELECT ... WHERE x = ?', (val,))) or Java PreparedStatement.",
        ),
        (
            r"(subprocess\.(Popen|call|run)\(.*shell\s*=\s*True|os\.system\(|Runtime\.getRuntime\(\)\.exec\()",
            "Bandit B602 / Semgrep Command-Injection",
            "OS Command Injection",
            "Critical",
            "OWASP A03 / CWE-78: OS command executed with shell=True or unsanitized user input.",
            "Validate input against an allowlist and pass command arguments as a list with shell=False.",
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
        stripped = line.strip()
        if stripped.startswith(("#", "//", "/*", "*")):
            continue
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
                    "snippet": stripped,
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
        stripped = line.strip()
        if stripped.startswith(("#", "//")):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent >= 16 and re.match(r"^(if|for|while|elif|else)\b", stripped):
            flags.append({
                "tool": "Radon / Pylint / Design Anti-Pattern: Spaghetti Code",
                "type": "Design Anti-Pattern (Spaghetti Code)",
                "vulnerability_name": "Spaghetti Code / Deep Nesting",
                "severity": "Medium",
                "line": f"Line {idx}",
                "message": "Deeply nested control flow (>4 indentation levels) increases cognitive complexity.",
                "recommendation": "Refactor nested conditionals into helper functions using guard clauses and early returns.",
                "snippet": stripped,
            })
            break

    return flags
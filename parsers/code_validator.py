import ast
import re
from typing import Optional, Tuple
from models.schemas import SyntaxValidationResult

# Optional Tree-sitter incremental parser support (Slide 5: Technologies Used)
_TS_PY_PARSER = None
_TS_JAVA_PARSER = None

try:
    from tree_sitter import Language, Parser
    import tree_sitter_python as tspython
    import tree_sitter_java as tsjava

    _TS_PY_PARSER = Parser(Language(tspython.language()))
    _TS_JAVA_PARSER = Parser(Language(tsjava.language()))
except Exception:
    _TS_PY_PARSER = None
    _TS_JAVA_PARSER = None


def _count_tree_sitter_nodes(root_node) -> Tuple[int, Optional[int]]:
    """Counts total AST nodes and returns first ERROR/MISSING node line if any."""
    count = 0
    error_line = None
    stack = [root_node]
    while stack:
        node = stack.pop()
        count += 1
        if (node.is_error or node.is_missing) and error_line is None:
            error_line = node.start_point[0] + 1
        stack.extend(node.children)
    return count, error_line


def detect_language(code: str, filename: Optional[str] = None) -> str:
    """Auto-detects whether the submitted source code is Python or Java."""
    if filename:
        if filename.lower().endswith(".py"):
            return "python"
        if filename.lower().endswith(".java"):
            return "java"

    if not code or not code.strip():
        return "unknown"

    java_indicators = [
        r"\bpublic\s+class\b",
        r"\bprivate\s+class\b",
        r"\bclass\s+[A-Z]\w*\s*\{",
        r"\bpublic\s+static\s+void\s+main\b",
        r"\bSystem\.out\.print",
        r"\bimport\s+java\.",
        r"\bimport\s+javax\.",
        r"\bpackage\s+[\w\.]+;",
        r"\b(public|private|protected)\s+(static\s+)?[\w<>\[\]]+\s+\w+\s*\(",
        r"\bString\s+\w+\s*=",
        r"\bint\s+\w+\s*=",
    ]

    python_indicators = [
        r"^\s*def\s+\w+\s*\(",
        r"^\s*from\s+[\w\.]+\s+import\b",
        r"^\s*import\s+[a-zA-Z_]\w*",
        r"^\s*elif\b",
        r"\bself\.",
        r"if\s+__name__\s*==\s*['\"]__main__['\"]",
        r"^\s*print\s*\(",
    ]

    java_score = sum(2 for p in java_indicators if re.search(p, code, re.MULTILINE))
    py_score = sum(2 for p in python_indicators if re.search(p, code, re.MULTILINE))

    lines = [line.strip() for line in code.splitlines() if line.strip()]
    java_score += sum(1 for l in lines if l.endswith(";") or l.endswith("{") or l == "}")
    py_score += sum(
        2
        for l in lines
        if l.endswith(":")
        and re.match(r"^(def|class|if|elif|else|for|while|try|except|with)\b", l)
    )

    if java_score == 0 and py_score == 0:
        try:
            tree = ast.parse(code)
            if tree.body and not isinstance(tree.body[0], ast.Expr):
                return "python"
        except SyntaxError:
            pass
        return "unknown"

    return "java" if java_score > py_score else "python"


def validate_python_code(code: str) -> SyntaxValidationResult:
    lines = code.splitlines()
    try:
        tree = ast.parse(code)
        ast_nodes = sum(1 for _ in ast.walk(tree))
        parser_label = "Python AST + Tree-sitter" if _TS_PY_PARSER else "Python AST"

        if (
            len(tree.body) == 1
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Name)
        ):
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="python",
                parser_used=parser_label,
                ast_node_count=ast_nodes,
                error_message="Input is an undefined identifier rather than valid Python code.",
                line_number=1,
                offending_line=lines[0] if lines else "",
            )

        return SyntaxValidationResult(
            is_valid=True,
            detected_language="python",
            parser_used=parser_label,
            ast_node_count=ast_nodes,
        )
    except SyntaxError as e:
        line_no = e.lineno or 1
        bad_line = lines[line_no - 1].strip() if 1 <= line_no <= len(lines) else ""
        return SyntaxValidationResult(
            is_valid=False,
            detected_language="python",
            parser_used="Python AST",
            error_message=f"SyntaxError: {e.msg}",
            line_number=line_no,
            offending_line=bad_line,
        )


def validate_java_code(code: str) -> SyntaxValidationResult:
    lines = code.splitlines()
    parser_label = "Tree-sitter Java + Lexical Validator" if _TS_JAVA_PARSER else "Java Lexical Validator"
    ts_node_count = 0

    # 1. If Tree-sitter Java is installed, parse incremental syntax tree first
    if _TS_JAVA_PARSER is not None:
        tree = _TS_JAVA_PARSER.parse(code.encode("utf-8"))
        ts_node_count, ts_err_line = _count_tree_sitter_nodes(tree.root_node)
        if tree.root_node.has_error and ts_err_line is not None:
            bad_line = lines[ts_err_line - 1].strip() if 1 <= ts_err_line <= len(lines) else ""
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="java",
                parser_used=parser_label,
                ast_node_count=ts_node_count,
                error_message="Tree-sitter Java Syntax Error: Invalid syntax or missing delimiter/semicolon.",
                line_number=ts_err_line,
                offending_line=bad_line,
            )

    # 2. Structural bracket, string literal, and semicolon checks
    pairs = {"}": "{", ")": "(", "]": "["}
    stack = []

    for idx, line in enumerate(lines, start=1):
        clean_line = re.sub(r"//.*$", "", line).strip()
        if not clean_line:
            continue

        clean_no_esc = re.sub(r"\\.", "", clean_line)
        if clean_no_esc.count('"') % 2 != 0:
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="java",
                parser_used=parser_label,
                ast_node_count=ts_node_count,
                error_message="Unclosed string literal.",
                line_number=idx,
                offending_line=line.strip(),
            )

        no_strings = re.sub(r'"[^"]*"|\'[^\']*\'', '""', clean_line)

        for ch in no_strings:
            if ch in "{([":
                stack.append((ch, idx, line.strip()))
            elif ch in "})]":
                if not stack or stack[-1][0] != pairs[ch]:
                    return SyntaxValidationResult(
                        is_valid=False,
                        detected_language="java",
                        parser_used=parser_label,
                        ast_node_count=ts_node_count,
                        error_message=f"Unmatched closing bracket '{ch}'.",
                        line_number=idx,
                        offending_line=line.strip(),
                    )
                stack.pop()

        if (
            not no_strings.startswith("@")
            and no_strings not in ("{", "}", "};")
            and not no_strings.endswith(("{", "}", ";", ",", "(", ":", "+", "-", "*", "/"))
            and not re.match(
                r"^(if|else|for|while|switch|try|catch|finally|do|class|interface|enum|public|private|protected)\b",
                no_strings,
            )
        ):
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="java",
                parser_used=parser_label,
                ast_node_count=ts_node_count,
                error_message="Missing ';' at end of Java statement.",
                line_number=idx,
                offending_line=line.strip(),
            )

        if re.match(
            r"^(public|private|protected)?\s*(static\s+)?(final\s+)?(int|String|boolean|double|float|long)\s+\w+\s*=.*[^;\{]$",
            no_strings,
        ):
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="java",
                parser_used=parser_label,
                ast_node_count=ts_node_count,
                error_message="Missing ';' after variable declaration.",
                line_number=idx,
                offending_line=line.strip(),
            )

    if stack:
        open_ch, open_line, bad_line = stack[-1]
        return SyntaxValidationResult(
            is_valid=False,
            detected_language="java",
            parser_used=parser_label,
            ast_node_count=ts_node_count,
            error_message=f"Unclosed bracket '{open_ch}'.",
            line_number=open_line,
            offending_line=bad_line,
        )

    return SyntaxValidationResult(
        is_valid=True,
        detected_language="java",
        parser_used=parser_label,
        ast_node_count=ts_node_count or len(lines),
    )


def validate_submission(code: str, filename: Optional[str] = None) -> SyntaxValidationResult:
    if not code or not code.strip():
        return SyntaxValidationResult(
            is_valid=False,
            detected_language="unknown",
            error_message="Please paste or upload code first.",
            line_number=1,
        )

    lang = detect_language(code, filename=filename)
    if lang == "python":
        return validate_python_code(code)
    elif lang == "java":
        return validate_java_code(code)

    return SyntaxValidationResult(
        is_valid=False,
        detected_language="unknown",
        error_message="Could not recognize valid Python or Java code.",
        line_number=1,
        offending_line=code.splitlines()[0] if code.splitlines() else "",
    )
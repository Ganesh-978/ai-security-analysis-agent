import ast
import re
from typing import Optional
from models.schemas import SyntaxValidationResult


def detect_language(code: str, filename: Optional[str] = None) -> str:
    """Auto-detects whether the code is Python or Java."""
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
        # Prevent plain single words from passing as valid Python variable expressions
        if (
            len(tree.body) == 1
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Name)
        ):
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="python",
                error_message="Input is not valid Python code.",
                line_number=1,
                offending_line=lines[0] if lines else "",
            )
        return SyntaxValidationResult(is_valid=True, detected_language="python")
    except SyntaxError as e:
        line_no = e.lineno or 1
        bad_line = lines[line_no - 1].strip() if 1 <= line_no <= len(lines) else ""
        return SyntaxValidationResult(
            is_valid=False,
            detected_language="python",
            error_message=f"SyntaxError: {e.msg}",
            line_number=line_no,
            offending_line=bad_line,
        )


def validate_java_code(code: str) -> SyntaxValidationResult:
    lines = code.splitlines()
    pairs = {"}": "{", ")": "(", "]": "["}
    stack = []

    for idx, line in enumerate(lines, start=1):
        # Remove single-line comments for checking
        clean_line = re.sub(r"//.*$", "", line).strip()
        if not clean_line:
            continue

        # Check for unclosed quotes on a single line
        clean_no_esc = re.sub(r'\\.', '', clean_line)
        if clean_no_esc.count('"') % 2 != 0:
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="java",
                error_message="Unclosed string literal.",
                line_number=idx,
                offending_line=line.strip(),
            )

        # Remove string literals before checking brackets and semicolons
        no_strings = re.sub(r'"[^"]*"|\'[^\']*\'', '""', clean_line)

        for ch in no_strings:
            if ch in "{([":
                stack.append((ch, idx, line.strip()))
            elif ch in "})]":
                if not stack or stack[-1][0] != pairs[ch]:
                    return SyntaxValidationResult(
                        is_valid=False,
                        detected_language="java",
                        error_message=f"Unmatched closing bracket '{ch}'.",
                        line_number=idx,
                        offending_line=line.strip(),
                    )
                stack.pop()

        # Check statement termination (missing semicolon)
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
                error_message="Missing ';' at end of Java statement.",
                line_number=idx,
                offending_line=line.strip(),
            )

        # Check variable declaration with '=' missing semicolon
        if re.match(
            r"^(public|private|protected)?\s*(static\s+)?(final\s+)?(int|String|boolean|double|float|long)\s+\w+\s*=.*[^;\{]$",
            no_strings,
        ):
            return SyntaxValidationResult(
                is_valid=False,
                detected_language="java",
                error_message="Missing ';' after variable declaration.",
                line_number=idx,
                offending_line=line.strip(),
            )

    if stack:
        open_ch, open_line, bad_line = stack[-1]
        return SyntaxValidationResult(
            is_valid=False,
            detected_language="java",
            error_message=f"Unclosed bracket '{open_ch}'.",
            line_number=open_line,
            offending_line=bad_line,
        )

    return SyntaxValidationResult(is_valid=True, detected_language="java")


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
import json
import re
from typing import Any, List


def parse_json_safely(raw_text: str, default: Any = None) -> Any:
    if not raw_text:
        return default
    cleaned = raw_text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", cleaned, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        cleaned = fenced.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start_arr, end_arr = cleaned.find("["), cleaned.rfind("]")
        start_obj, end_obj = cleaned.find("{"), cleaned.rfind("}")
        try:
            if start_arr != -1 and end_arr != -1 and (start_obj == -1 or start_arr < start_obj):
                return json.loads(cleaned[start_arr : end_arr + 1])
            if start_obj != -1 and end_obj != -1:
                return json.loads(cleaned[start_obj : end_obj + 1])
        except json.JSONDecodeError:
            pass
    return default


def parse_json_array(raw_text: str) -> List[dict]:
    parsed = parse_json_safely(raw_text, default=[])
    return parsed if isinstance(parsed, list) else []
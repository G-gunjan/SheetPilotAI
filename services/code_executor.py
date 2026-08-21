import pandas as pd

FORBIDDEN_KEYWORDS = [
    "import", "os.", "sys.", "subprocess", "eval(", "exec(",
    "open(", "__", "shutil", "socket", "requests", "urllib"
]

def validate_code(code: str):
    code_lower = code.lower()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword.lower() in code_lower:
            return False, f"Blocked dangerous operation: {keyword}"
    return True, "Code validated"

def execute_code(code: str, df: pd.DataFrame):
    is_valid, message = validate_code(code)
    if not is_valid:
        raise ValueError(message)

    local_scope = {"df": df.copy(), "pd": pd}

    exec(code, {"__builtins__": {}}, local_scope)

    result = local_scope.get("result")

    if result is None:
        # Fallback: take the last non-df/pd variable
        candidates = [k for k in local_scope if k not in ("df", "pd")]
        if candidates:
            result = local_scope[candidates[-1]]

    if result is None:
        raise ValueError("Generated code did not produce a 'result' variable.")

    return result
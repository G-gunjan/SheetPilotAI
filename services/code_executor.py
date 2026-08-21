# import pandas as pd


# ALLOWED_KEYWORDS = [
#     "df",
#     "head",
#     "tail",
#     "sort_values",
#     "groupby",
#     "agg",
#     "mean",
#     "sum",
#     "min",
#     "max",
#     "count",
#     "median",
#     "filter",
#     "query",
#     "loc",
#     "iloc",
#     "dropna",
#     "fillna",
#     "duplicated",
#     "drop_duplicates",
#     "reset_index",
# ]


# FORBIDDEN_KEYWORDS = [
#     "import",
#     "os.",
#     "sys.",
#     "subprocess",
#     "eval(",
#     "exec(",
#     "open(",
#     "__",
#     "shutil",
#     "socket",
# ]


# def validate_code(code):

#     code_lower = code.lower()

#     for keyword in FORBIDDEN_KEYWORDS:
#         if keyword.lower() in code_lower:
#             return False, f"Blocked operation: {keyword}"

#     return True, "Code validated"


# def execute_code(code, df):

#     is_valid, message = validate_code(code)

#     if not is_valid:
#         raise ValueError(message)

#     local_scope = {
#         "df": df.copy(),
#         "pd": pd
#     }

#     exec(
#         code,
#         {"__builtins__": {}},
#         local_scope
#     )

#     result = local_scope.get("result")

#     if result is None:

#         # Fallback: Gemini sometimes names the final output
#         # something other than 'result' (e.g. df_result, output).
#         # Grab the last variable assigned during exec() instead
#         # of hard-failing the whole run.

#         candidate_keys = [
#             k for k in local_scope
#             if k not in ("df", "pd")
#         ]

#         if candidate_keys:
#             result = local_scope[candidate_keys[-1]]

#     if result is None:
#         raise ValueError(
#             "Generated code did not create a 'result' variable."
#         )

#     return result


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
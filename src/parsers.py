import json
import pandas as pd

def safe_json_loads(x):
    """Return (parsed_list, status). status is 'ok', 'missing' or 'failed'."""
    # Missing: null, NaN, empty string
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None, "missing"
    s = str(x).strip()
    if s == "" or s.lower() in {"null", "none", "nan"}:
        return None, "missing"

    # Real JSON parsing (never split on commas)
    try:
        obj = json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None, "failed"

    # Normalize the shape: we expect a list of dicts
    if isinstance(obj, dict):
        obj = [obj]
    if not isinstance(obj, list):
        return None, "failed"
    if len(obj) == 0:           # "[]" means nothing was specified
        return None, "missing"
    return obj, "ok"
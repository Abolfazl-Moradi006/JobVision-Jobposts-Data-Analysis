"""
Persian text normalization tools for the JobVision project.

What the cleaner changes:
    1. Arabic letters -> Persian letters (ي -> ی, ك -> ک, ى -> ی)
    2. Persian / Arabic-Indic digits -> English digits (۱۲۳ -> 123)
    3. Zero-width non-joiner (half-space) -> normal space
    4. Other invisible characters (zero-width space, LTR/RTL marks, BOM) -> removed
    5. Repeated whitespace -> one space, then strip both ends

What it does NOT change:
    - Punctuation, quotes, commas, brackets (so JSON text stays parsable)
    - Missing values (NaN stays NaN, it never becomes the string "nan")
"""

import re

import pandas as pd

# ---------------------------------------------------------------------------
# Character maps
# ---------------------------------------------------------------------------
_LETTER_MAP = {
    "ي": "ی",  # Arabic yeh        -> Persian yeh
    "ى": "ی",  # Arabic alef maksura -> Persian yeh
    "ك": "ک",  # Arabic kaf        -> Persian kaf
}

_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
_ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
_ENGLISH_DIGITS = "0123456789"

_TRANSLATION_TABLE = str.maketrans(
    {
        **_LETTER_MAP,
        **dict(zip(_PERSIAN_DIGITS, _ENGLISH_DIGITS)),
        **dict(zip(_ARABIC_DIGITS, _ENGLISH_DIGITS)),
        "\u200c": " ",  # ZWNJ (half-space) -> normal space (our decision)
    }
)

# Invisible characters that should simply disappear:
# zero-width space, zero-width joiner, LTR mark, RTL mark, BOM
_INVISIBLE_RE = re.compile(r"[\u200b\u200d\u200e\u200f\ufeff]")
_MULTI_SPACE_RE = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# Single value
# ---------------------------------------------------------------------------
def normalize_persian_text(text):
    """Normalize one string. Non-strings (NaN, None, numbers) are returned unchanged."""
    if not isinstance(text, str):
        return text
    text = _INVISIBLE_RE.sub("", text)
    text = text.translate(_TRANSLATION_TABLE)
    text = _MULTI_SPACE_RE.sub(" ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Columns and DataFrames
# ---------------------------------------------------------------------------
def normalize_column(series: pd.Series) -> pd.Series:
    """Apply Persian normalization to a whole column."""
    return series.map(normalize_persian_text)


def strip_english_column(series: pd.Series) -> pd.Series:
    """Only strip outer spaces (for English columns such as Jobpost_BenefitEn).

    For comma-separated lists, also strips spaces around each item.
    """
    def _clean(value):
        if not isinstance(value, str):
            return value
        value = _MULTI_SPACE_RE.sub(" ", value).strip()
        return ",".join(part.strip() for part in value.split(","))

    return series.map(_clean)


def normalize_dataframe(df: pd.DataFrame, persian_cols, english_cols=()) -> pd.DataFrame:
    """Return a copy of df with Persian columns normalized and English columns stripped."""
    out = df.copy()
    for col in persian_cols:
        out[col] = normalize_column(out[col])
    for col in english_cols:
        out[col] = strip_english_column(out[col])
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def unique_count_report(before: pd.DataFrame, after: pd.DataFrame, columns) -> pd.DataFrame:
    """Compare number of unique values before and after cleaning.

    Columns where the count drops are the ones where the same value
    was written in several different ways.
    """
    rows = []
    for col in columns:
        n_before = before[col].nunique(dropna=True)
        n_after = after[col].nunique(dropna=True)
        rows.append(
            {
                "column": col,
                "unique_before": n_before,
                "unique_after": n_after,
                "difference": n_before - n_after,
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values("difference", ascending=False)
        .reset_index(drop=True)
    )


def check_json_still_parses(series: pd.Series, n: int = 200, seed: int = 42) -> float:
    """Share of a random sample of JSON-text rows that still parse with json.loads."""
    import json

    sample = series.dropna().sample(min(n, series.notna().sum()), random_state=seed)
    ok = 0
    for value in sample:
        try:
            json.loads(value)
            ok += 1
        except (ValueError, TypeError):
            pass
    return ok / len(sample) if len(sample) else float("nan")
import pandas as pd


def find_col(df: pd.DataFrame, pattern: str) -> str:
    """
    Return the first column name containing pattern (case-insensitive), else "".
    """
    pat = pattern.lower()
    for c in df.columns:
        if pat in str(c).lower():
            return str(c)
    return ""

import pandas as pd
from .find_col import find_col


def apply_callsign_filter(df: pd.DataFrame, callsign: str) -> pd.DataFrame:
    """
    Filter rows by callsign if provided; raises if no match.
    """
    callsign = (callsign or "").strip()
    if not callsign:
        return df

    col = find_col(df, "callsign")
    if not col:
        raise ValueError("callsign is set but no Callsign column was found.")

    cs = df[col].astype(str).str.replace('"', "", regex=False).str.strip()
    mask = cs == callsign

    if not mask.any():
        print("Unique callsigns found in file:")
        print(sorted(cs.unique()))
        raise ValueError(f'No rows left after callsign filtering. callsign="{callsign}" did not match.')

    return df.loc[mask].reset_index(drop=True)

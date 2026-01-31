import pandas as pd


def parse_time(df: pd.DataFrame, col_utc: str, col_ts: str) -> pd.Series:
    """
    Parse time from either UTC ISO-8601 strings or POSIX timestamps.
    Converts to America/New_York when possible.
    """
    if col_utc:
        t = pd.to_datetime(df[col_utc].astype(str), utc=True, errors="coerce")
        # convert to local timezone for display/plots
        return t.dt.tz_convert("America/New_York")

    if col_ts:
        t = pd.to_datetime(pd.to_numeric(df[col_ts], errors="coerce"), unit="s", utc=True)
        return t.dt.tz_convert("America/New_York")

    # fallback: numeric index
    return pd.Series(range(len(df)))

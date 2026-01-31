from pathlib import Path
import pandas as pd


def read_flight_csv(csv_file: str | Path) -> pd.DataFrame:
    """
    Read CSV into a DataFrame. Supports comma or tab delimiters.
    """
    csv_file = Path(csv_file)
    df = pd.read_csv(csv_file, sep=None, engine="python")  # auto-detect delimiter
    if len(df) < 2:
        raise ValueError("CSV loaded but has too few rows.")
    return df

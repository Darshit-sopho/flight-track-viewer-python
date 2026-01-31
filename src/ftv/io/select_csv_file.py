from __future__ import annotations
from typing import Optional

def select_csv_file() -> Optional[str]:
    """
    Open a native file picker and return selected CSV path or None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return path if path else None

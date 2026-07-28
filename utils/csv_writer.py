"""
utils/csv_writer.py
-------------------
Thin wrapper around the stdlib csv module for writing pipeline output CSVs.
"""

import csv
from pathlib import Path

from config.settings import CSV_ENCODING


def write_csv(
    rows: list[dict],
    path: Path,
    fieldnames: list[str] | None = None,
    encoding: str = CSV_ENCODING,
) -> int:
    """
    Write *rows* (list of dicts) to a CSV file at *path*.

    Parameters
    ----------
    rows:       Records to write.  All dicts should share the same keys.
    path:       Destination file.  Parent directories are created automatically.
    fieldnames: Column order.  Inferred from the first row if not provided.
    encoding:   File encoding (defaults to ``CSV_ENCODING`` in settings).

    Returns
    -------
    Number of data rows written (excluding the header).
    """
    if not rows:
        return 0

    if fieldnames is None:
        fieldnames = list(rows[0].keys())

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def append_csv(
    rows: list[dict],
    path: Path,
    fieldnames: list[str] | None = None,
    encoding: str = CSV_ENCODING,
) -> int:
    """
    Append *rows* to an existing CSV (no header written).
    Creates the file with a header if it does not exist yet.
    """
    if not rows:
        return 0

    if fieldnames is None:
        fieldnames = list(rows[0].keys())

    file_exists = path.exists() and path.stat().st_size > 0
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "a", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

    return len(rows)

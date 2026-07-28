"""Row streaming + deterministic train/test split over the Phase 1 invoice lines."""
import csv
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
INVOICE_LINES = REPO / "data" / "outputs" / "invoice_lines_all_companies.csv"


def iter_rows(path=INVOICE_LINES):
    """Yield each invoice line as a dict (streaming; never loads the 90MB file)."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def split_of(row, test_every=5):
    """Deterministic split by content hash (crc32 is stable across runs; hash() is not).
    ~1/test_every rows -> 'test'. Line-level split mimics 'new receipt for a known company'."""
    key = f"{row['logical_key']}|{row['line_number']}".encode()
    return "test" if zlib.crc32(key) % test_every == 0 else "train"

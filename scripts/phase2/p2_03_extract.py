"""Phase 2 · Stage B2 — OCR extraction cache.

Runs each receipt image through AWS Textract AnalyzeExpense exactly once and caches
the raw JSON response. Idempotent: a cached response is never re-fetched (Phase-1
"extract once, use forever" discipline — keeps us far inside the free tier and makes
every downstream module independent of AWS).

AnalyzeExpense already returns vendor, CIF (TAX_PAYER_ID), date, totals, tax, and
line items whose EXPENSE_ROW carries the per-line VAT bracket letter (A/B) — so no
separate DetectDocumentText pass is needed for the receipts seen so far.
# ponytail: single-API extraction; add a DetectDocumentText fallback only if some
# receipt fails to populate EXPENSE_ROW / SummaryFields.

Usage:  python scripts/phase2/p2_03_extract.py
Requires: configured AWS creds with Textract access, boto3.
"""
import json
import pathlib
import sys

import boto3

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC_DIR = REPO / "Receipts Examples"
CACHE_DIR = REPO / "data" / "outputs" / "phase2" / "textract_raw"
IMAGE_EXT = {".jpg", ".jpeg", ".png"}


def main() -> int:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    images = sorted(p for p in SRC_DIR.iterdir() if p.suffix.lower() in IMAGE_EXT)
    if not images:
        print(f"No images in {SRC_DIR}", file=sys.stderr)
        return 1

    client = None  # lazily created only when there is real work (a cache miss)
    called = cached = 0
    for img in images:
        out = CACHE_DIR / f"{img.stem}.analyze_expense.json"
        if out.exists():
            cached += 1
            print(f"[skip ] {img.name}")
            continue
        if client is None:
            client = boto3.client("textract")  # configured region
        resp = client.analyze_expense(Document={"Bytes": img.read_bytes()})
        out.write_text(json.dumps(resp, indent=2), encoding="utf-8")
        called += 1
        n_items = sum(len(g.get("LineItems", []))
                      for d in resp.get("ExpenseDocuments", [])
                      for g in d.get("LineItemGroups", []))
        print(f"[call ] {img.name}  -> {out.name}  ({n_items} line items)")

    print(f"\nDone. {called} called, {cached} already cached, {len(images)} total.")
    print(f"Cache: {CACHE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

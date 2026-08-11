"""
Regression test for Research Audit finding A5: product_ambiguity.csv's dominant-account
selection must aggregate counts by account_id across all rows for a product before picking
the max, not just take the single largest raw mapping row.

Run: python scripts/test_dataset_intelligence.py
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "dataset_intelligence", ROOT / "scripts" / "03_5_dataset_intelligence.py"
)
dataset_intelligence = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dataset_intelligence)


def _mapping_rows(*, company, product, account_id, count):
    return {
        "company": company,
        "normalized_product": product,
        "account_id": account_id,
        "count": count,
    }


def test_dominant_account_is_aggregated_across_companies_not_row_max():
    # Product X: Company A -> 707 x60, Company B -> 707 x60, Company C -> 704 x70.
    # Aggregated: 707 totals 120, 704 totals 70 => dominant must be 707.
    # The buggy row-level-max logic instead picks 704 (single largest row, 70 > 60).
    mappings = [
        _mapping_rows(company="A", product="Product X", account_id="707", count=60),
        _mapping_rows(company="B", product="Product X", account_id="707", count=60),
        _mapping_rows(company="C", product="Product X", account_id="704", count=70),
    ]
    c4_data = {"vat_by_product": {}}

    with tempfile.TemporaryDirectory() as tmp:
        dataset_intelligence.INTELLIGENCE_DIR = Path(tmp)
        dataset_intelligence.module_c_behavioral(mappings, c4_data)

        with open(Path(tmp) / "product_ambiguity.csv", encoding="utf-8") as f:
            import csv
            rows = list(csv.DictReader(f))

    assert len(rows) == 1, rows
    row = rows[0]
    assert row["dominant_account_id"] == "707", row
    assert row["total_occurrences"] == "190", row
    assert row["determinism_score"] == "0.6316", row


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all dataset_intelligence self-checks passed")

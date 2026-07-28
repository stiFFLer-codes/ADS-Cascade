"""Phase 2 · demo data generator — the single source of truth for every number the
stakeholder demo (docs/demo/index.html) displays.

Reads the committed pipeline outputs and emits data/outputs/phase2/receipts_demo.json.
The demo page is a self-contained file:// document (it cannot fetch at runtime), so the
numbers are inlined there BY HAND — but this script is what they must match. Run it and
reconcile the demo's DATA object against its output; that keeps "every number here is
reproducible" true by construction instead of by care.

Usage:  python scripts/phase2/p2_07_demo_data.py
"""
import csv
import json
from collections import Counter, OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "outputs" / "phase2"


def main():
    rows = list(csv.DictReader(open(OUT / "e2e_classification.csv", encoding="utf-8")))
    tiers = Counter(int(r["tier"]) for r in rows)

    # per-receipt breakdown (true line items, incl. duplicate lines like pall mall x4)
    receipts = OrderedDict()
    for r in rows:
        receipts.setdefault(r["receipt"], {"supplier": r["supplier"], "lines": []})
        receipts[r["receipt"]]["lines"].append(
            {"product": r["normalized_product"], "tier": int(r["tier"]),
             "account": r["predicted_account"] or "-"})

    # determinism at the AUTHORITATIVE unique-product level (matches phase1_final_report.md)
    hi = mid = lo = tot = 0
    for r in csv.DictReader(open(REPO / "data" / "outputs" / "intelligence" / "product_ambiguity.csv",
                                 encoding="utf-8-sig")):
        try:
            v = float(r["determinism_score"])
        except (KeyError, ValueError):
            continue
        tot += 1
        hi += v > 0.95
        mid += 0.50 <= v <= 0.95
        lo += v < 0.50

    rov = next(r for r in rows if "rovinieta" in r["normalized_product"])
    llm = list(csv.DictReader(open(OUT / "llm_tail_proposals.csv", encoding="utf-8")))
    lrov = next(r for r in llm if "rovinieta" in r["product"])

    data = {
        "line_items": len(rows),
        "tier_counts": {str(k): tiers[k] for k in sorted(tiers)},
        "determinism_unique_product": {
            "gt_0_95": hi, "band_0_50_0_95": mid, "lt_0_50": lo, "total": tot,
            "pct": round(100 * hi / tot, 1)},
        "rovinieta": {
            "cascade_account": rov["predicted_account"],
            "candidates": rov["candidate_accounts"],
            "llm_account": lrov["llm_account"] if "llm_account" in lrov else lrov.get("llm_chosen_account", "")},
        "receipts": list(receipts.values()),
    }
    (OUT / "receipts_demo.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    print("line items:", data["line_items"], "| tiers:", data["tier_counts"])
    print("determinism (unique product >0.95): {gt_0_95}/{total} = {pct}%".format(**data["determinism_unique_product"]))
    print("rovinieta: cascade={cascade_account} candidates={candidates} llm={llm_account}".format(**data["rovinieta"]))
    print("-> wrote", OUT / "receipts_demo.json")


if __name__ == "__main__":
    main()

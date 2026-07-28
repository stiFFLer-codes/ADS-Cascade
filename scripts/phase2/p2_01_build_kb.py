"""Phase 2 · Stage A — Build the knowledge base from Phase 1 ground truth.

Streams data/outputs/invoice_lines_all_companies.csv into per-company rules + global
patterns, writes inspectable KB artifacts, and reports the Phase-1 determinism stats as a
sanity check (should reproduce ~91% deterministic products).

Usage:  python scripts/phase2/p2_01_build_kb.py
"""
import csv
import json
from pathlib import Path

from p2lib import kb as kbmod
from p2lib.data import INVOICE_LINES, iter_rows

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "outputs" / "phase2" / "kb"


def _dominant(counter):
    acct, ct = counter.most_common(1)[0]
    return acct, ct, sum(counter.values())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Building KB from {INVOICE_LINES.name} ...")
    kb = kbmod.build_from_rows(iter_rows())
    print(f"  companies={len(kb.company_name)}  (company,product) rules={len(kb.rules)}  "
          f"global products={len(kb.glob)}")

    # --- company_rules.csv: best account per (company, product, direction) ---
    det_products = det_hi = det_mid = det_lo = 0
    with open(OUT / "company_rules.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cui", "company_name", "product", "direction", "account_id",
                    "account_description", "tax_code", "ads", "evidence_count"])
        for (cui, product), r in kb.rules.items():
            # product-level determinism (all directions) for the Phase-1 comparison
            allc = kbmod._dir_counter(r.by_dir, "__all__")
            _, dct, dtot = _dominant(allc)
            ads_all = dct / dtot
            det_products += 1
            det_hi += ads_all > 0.95
            det_mid += 0.50 <= ads_all <= 0.95
            det_lo += ads_all < 0.50
            for direction, counter in r.by_dir.items():
                acct, ct, tot = _dominant(counter)
                w.writerow([cui, r.name, product, direction, acct,
                            kb.acct_desc.get((cui, acct), ""),
                            r.tax[acct].most_common(1)[0][0] if r.tax[acct] else "",
                            f"{ct/tot:.4f}", tot])

    # --- global_patterns.csv ---
    with open(OUT / "global_patterns.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["product", "direction", "dominant_account", "global_ads",
                    "company_count", "distinct_accounts"])
        for product, g in kb.glob.items():
            for direction, counter in g.by_dir.items():
                acct, ct, tot = _dominant(counter)
                w.writerow([product, direction, acct, f"{ct/tot:.4f}",
                            len(g.companies), len(counter)])

    summary = {
        "companies": len(kb.company_name),
        "company_product_rules": len(kb.rules),
        "global_products": len(kb.glob),
        "products_determinism_gt_0.95": det_hi,
        "products_determinism_0.50_0.95": det_mid,
        "products_determinism_lt_0.50": det_lo,
        "pct_deterministic_gt_0.95": round(100 * det_hi / det_products, 1),
    }
    (OUT / "kb_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # NB: this is per-(company, product) PAIR determinism — a different, higher denominator
    # than Phase 1's authoritative UNIQUE-PRODUCT figure (91.2%, product_ambiguity.csv).
    # Per-pair is naturally higher because it doesn't average a product across companies.
    print("\n--- Determinism per (company, product) pair — NOT the same as the 91.2% headline ---")
    print(f"  >0.95 : {det_hi:6d}  ({summary['pct_deterministic_gt_0.95']}%)   [unique-product level = 91.2%, see phase1_final_report.md]")
    print(f"  0.5-0.95: {det_mid:6d}")
    print(f"  <0.50 : {det_lo:6d}")
    print(f"\nArtifacts -> {OUT}")


if __name__ == "__main__":
    main()

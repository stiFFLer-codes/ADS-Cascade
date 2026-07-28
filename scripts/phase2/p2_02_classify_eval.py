"""Phase 2 · Stage A — Held-out evaluation of the RULES_FIRST cascade.

Builds the KB from the train split only, then classifies every test line and compares the
predicted account to the actual (self-labeled) account. This turns the Phase 1 *statistic*
(91% deterministic) into a *running classifier* with measured accuracy and tier routing.

Two streaming passes (train build, test eval) keep memory flat on the 90MB file.

Usage:  python scripts/phase2/p2_02_classify_eval.py
"""
import csv
from collections import defaultdict
from pathlib import Path

from p2lib import cascade
from p2lib import confidence as C
from p2lib import kb as kbmod
from p2lib.data import INVOICE_LINES, iter_rows, split_of

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "outputs" / "phase2"


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("Pass 1/2: building KB from TRAIN split ...")
    kb = kbmod.build_from_rows(iter_rows(), keep=lambda r: split_of(r) == "train")
    print(f"  train rules={len(kb.rules)}  global products={len(kb.glob)}")

    print("Pass 2/2: classifying TEST split ...")
    tier_n = defaultdict(int)
    tier_correct = defaultdict(int)
    per_co = defaultdict(lambda: [0, 0, 0])  # cui -> [n, correct, auto_n]
    total = correct = auto_n = auto_correct = 0

    eval_path = OUT / "classification_eval.csv"
    with open(eval_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cui", "company_name", "product", "direction", "actual_account",
                    "predicted_account", "tier", "method", "confidence", "correct"])
        for row in iter_rows():
            if split_of(row) != "test":
                continue
            actual = row["account_id"]
            pred = cascade.classify(kb, row["cui"], row["normalized_product"],
                                    row["direction"], vat_hint=row["vat_percent"].strip())
            ok = pred["account_id"] == actual and actual != ""
            tier = pred["tier"]

            total += 1
            correct += ok
            tier_n[tier] += 1
            tier_correct[tier] += ok
            co = per_co[row["cui"]]
            co[0] += 1
            co[1] += ok
            if tier in C.AUTO_APPLY_TIERS:
                auto_n += 1
                auto_correct += ok
                co[2] += 1
            w.writerow([row["cui"], row["company_name"], row["normalized_product"],
                        row["direction"], actual, pred["account_id"], tier,
                        pred["method"], pred["confidence"], int(ok)])

    # --- tier_distribution.csv ---
    with open(OUT / "tier_distribution.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tier", "count", "pct_of_total", "accuracy"])
        for t in (1, 2, 3, 4):
            n = tier_n[t]
            acc = (tier_correct[t] / n) if n else 0.0
            w.writerow([t, n, f"{100*n/total:.1f}", f"{acc:.4f}"])

    # --- per_company_accuracy.csv ---
    with open(OUT / "per_company_accuracy.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cui", "company_name", "test_lines", "accuracy", "auto_coverage"])
        for cui, (n, cok, an) in sorted(per_co.items(), key=lambda kv: -kv[1][0]):
            w.writerow([cui, kb.company_name.get(cui, ""), n,
                        f"{cok/n:.4f}", f"{an/n:.4f}"])

    # --- headline ---
    print("\n================ STAGE A RESULTS ================")
    print(f"Test lines            : {total:,}")
    print(f"Overall accuracy      : {correct/total:.1%}")
    print(f"Auto-apply coverage   : {auto_n/total:.1%}   (Tier 1+2, booked with no human)")
    print(f"Auto-apply accuracy   : {auto_correct/auto_n:.1%}   (of those, how often right)")
    print(f"Sent to human review  : {(total-auto_n)/total:.1%}   (Tier 3+4)")
    print("\nTier routing:")
    for t in (1, 2, 3, 4):
        n = tier_n[t]
        acc = (tier_correct[t] / n) if n else 0.0
        print(f"  Tier {t}: {n:7,} ({100*n/total:5.1f}%)  accuracy {acc:.1%}")
    print(f"\nArtifacts -> {OUT}\\{{classification_eval,tier_distribution,per_company_accuracy}}.csv")


if __name__ == "__main__":
    main()

"""Phase 2 · Stage C — End-to-end on the 10 real receipts.

Cached Textract JSON -> structure -> normalize -> classify through the Stage A cascade.
Receipts belong to a NEW client company (no own history), so classification uses the
GLOBAL knowledge base, direction=PURCHASE strict (a receipt purchase must not inherit a
seller's revenue account). This is the honest cold-start regime: it shows which lines the
system can already anchor from cross-company history vs which need the LLM tail + a human.

Usage:  python scripts/phase2/p2_05_end_to_end.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

from p2lib import cascade, structure
from p2lib.data import iter_rows
from p2lib import kb as kbmod
from p2lib.normalize import normalize_product
from p2lib.retrieval import fuzzy_global

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "data" / "outputs" / "phase2" / "textract_raw"
OUT = REPO / "data" / "outputs" / "phase2"
NEW_CLIENT = "NEW_CLIENT_DEMO"   # not in the KB -> forces the cold-start (global) path


def main():
    print("Building full KB (all Phase 1 evidence) ...")
    kb = kbmod.build_from_rows(iter_rows())
    global_pool = list(kb.glob.keys())
    print(f"  {len(kb.rules):,} rules, {len(global_pool):,} global products\n")

    rows_out = []
    tier_n = defaultdict(int)
    receipts = sorted(CACHE.glob("*.analyze_expense.json"))

    for jf in receipts:
        resp = json.loads(jf.read_text(encoding="utf-8"))
        r = structure.parse_analyze_expense(resp)
        if not r:
            continue
        v = structure.validate(r)
        name = jf.stem.replace(".analyze_expense", "")
        print(f"=== {name[:42]:42} | {r['supplier'][:28]:28} "
              f"| total {r['grand_total']} | sum {v['sum_check']} | VAT {v['vat_resolved_by_bracket']}")
        for it in r["items"]:
            norm = normalize_product(it["raw_text"])
            if not norm:
                continue
            pred = cascade.classify(kb, NEW_CLIENT, norm, "PURCHASE",
                                    vat_hint=str(it["vat_percent"] or ""), global_strict=True,
                                    global_pool=global_pool)
            tier_n[pred["tier"]] += 1
            nearest = ""
            if pred["tier"] >= 3:  # review: show what a human/LLM would weigh
                near = fuzzy_global(norm, global_pool, limit=3, cutoff=80)
                nearest = "; ".join(f"{m}({int(s)})" for m, s, _ in near)
            print(f"    T{pred['tier']}  {it['vat_bracket_letter'] or '-'}={it['vat_percent'] or '?':>5}%  "
                  f"acct={pred['account_id'] or '--':>6}  {pred['method']:<18} {norm[:34]}")
            cand = ";".join(f"{a}:{c}" for a, c in pred["candidates"])
            rows_out.append([name, r["supplier"], norm, it["vat_bracket_letter"],
                             it["vat_percent"], pred["tier"], pred["method"],
                             pred["account_id"], pred["confidence"], cand, nearest])

    with open(OUT / "e2e_classification.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["receipt", "supplier", "normalized_product", "vat_bracket", "vat_percent",
                    "tier", "method", "predicted_account", "confidence",
                    "candidate_accounts", "nearest_global"])
        w.writerows(rows_out)

    total = sum(tier_n.values())
    auto = tier_n[1] + tier_n[2]
    print(f"\n================ STAGE C ({len(receipts)} receipts) ================")
    print(f"Receipts: {len(receipts)}   Line items: {total}")
    for t in (1, 2, 3, 4):
        print(f"  Tier {t}: {tier_n[t]:3d} ({(100*tier_n[t]/total if total else 0):4.0f}%)")
    print(f"\nAuto-anchored from cross-company history (T1/2): {auto}/{total}")
    print(f"Need LLM tail + human (T3/4): {total-auto}/{total}  <- Groq plugs in here")
    print(f"\nArtifacts -> {OUT}\\e2e_classification.csv")


if __name__ == "__main__":
    main()

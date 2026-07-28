"""Phase 2 · LLM tail — run the model-agnostic adapter (Groq now) on the review tail only.

For each distinct product that reached review in Stage C, the LLM (a) gives a generic name +
category and (b) re-ranks the *retrieved candidate accounts* (from the cascade, grounded in
precedent) — NOT a generic chart. Every output is a REVIEW suggestion, never auto-applied.

No key? Prints how to enable and exits 0. Interface test (Groq != Haiku), not a quality bench.
Rate limits handled in the adapter (30 RPM / 12K TPM; responses cached so re-runs don't repeat).

Usage:  python scripts/phase2/p2_06_llm_tail.py
"""
import csv
import sys
from collections import Counter
from pathlib import Path

from p2lib.ai import adapter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Romanian diacritics on Windows console

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "outputs" / "phase2"
KB = OUT / "kb" / "company_rules.csv"
E2E = OUT / "e2e_classification.csv"


def load_accounts():
    """account_id -> description, and PURCHASE frequency (for the cold-start fallback chart)."""
    desc, cnt = {}, Counter()
    with open(KB, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["direction"] != "PURCHASE":
                continue
            desc.setdefault(r["account_id"], r["account_description"])
            cnt[r["account_id"]] += int(r["evidence_count"])
    return desc, cnt


def main():
    if not adapter.available():
        print("LLM tier is DISABLED (no GROQ_API_KEY).\n")
        print("Enable (do NOT paste the key in code/chat) — put it in .env at repo root:")
        print("  GROQ_API_KEY=gsk_your_key")
        print("  (or:  setx GROQ_API_KEY \"gsk_...\"  then open a new terminal)")
        print("\nThen re-run. Responses cache to data/outputs/phase2/llm_cache/.")
        return 0

    desc, cnt = load_accounts()
    fallback = [(a, desc.get(a, "")) for a, _ in cnt.most_common(8)]
    print(f"LLM ENABLED (model={adapter.MODEL}, throttle ~{adapter.RPM_LIMIT} RPM).\n")

    seen, rows = set(), []
    with open(E2E, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if int(r["tier"]) >= 3 and r["normalized_product"] not in seen:
                seen.add(r["normalized_product"])
                rows.append(r)

    out = []
    for r in rows:
        prod = r["normalized_product"]
        ctx = f"supplier={r['supplier']}; bracket_VAT={r['vat_percent']}"
        # grounded chart = the cascade's retrieved candidate accounts for THIS product
        cand_ids = [c.split(":")[0] for c in (r.get("candidate_accounts") or "").split(";") if c]
        chart = [(a, desc.get(a, "")) for a in cand_ids] or fallback
        norm = adapter.normalize_product(prod, ctx)           # cached (prompt unchanged)
        prop = adapter.propose_account(prod, chart, ctx)      # grounded chart -> re-rank
        gen, cat = norm.get("generic_name", ""), norm.get("category", "")
        acc, why = prop.get("account_id", ""), prop.get("rationale", "")
        cand_show = ",".join(cand_ids) or "(none)"
        print(f"  {prod[:32]:32} -> {gen[:20]:20} [{cat[:14]:14}]  from[{cand_show:>14}] -> {acc:>6}")
        out.append([prod, r["supplier"], gen, cat, cand_show, acc, why, "REVIEW"])

    with open(OUT / "llm_tail_proposals.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["product", "supplier", "llm_generic_name", "llm_category",
                    "retrieved_candidates", "llm_chosen_account", "llm_rationale", "status"])
        w.writerows(out)
    print(f"\n{len(out)} proposals (all REVIEW) -> {OUT}\\llm_tail_proposals.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

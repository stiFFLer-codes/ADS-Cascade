"""Realized historical decision consistency (ADS), computed TRAIN-ONLY.

research/EXPERIMENT_1_REDESIGN_REVIEW.md §3/§13: the scientific independent
variable is the measured `det_pct` (share of products with per-product
determinism_score > 0.95), computed with the A5-corrected aggregation --
counts summed by account_id across all rows for a product before selecting
the dominant account (scripts/03_5_dataset_intelligence.py Module C.1's fixed
logic) -- and computed ONLY over the train split, never the test split, since
this is meant to model a design-time signal that can only see history.

realized_ads() is the single entrypoint the rest of the harness must call --
it does the train-only filtering itself, so a caller can never accidentally
feed it the full (train+test) row set.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator  # noqa: E402  (ensures scripts/phase2 is on sys.path)

load_generator()  # side effect only: registers scripts/phase2 on sys.path
from p2lib.data import split_of  # noqa: E402


def compute_det_pct(rows, det_threshold=0.95):
    """A5-corrected dataset-level determinism aggregation, applied directly to
    raw invoice-line rows (each row = one occurrence; summing per-line counts
    by account_id is mathematically the same aggregation product_ambiguity.csv
    performs over its pre-aggregated (company, product, account, count) rows).

    Grouped by `product_code` (the stable ground-truth product identity), NOT
    `normalized_product` (the surface string, which the lexical-variation
    condition deliberately perturbs). This was a real pilot finding, not a
    stylistic choice: grouping by the surface string means the VARIED lexical
    condition fragments one true product into several distinct, low-count,
    near-unanimous surface-form "pseudo-products" -- which artificially
    INFLATES det_pct, since a single-occurrence surface variant is trivially
    100% self-consistent. That would make realized_det_pct partly measure
    "how much did the lexical transform fragment the surface key" instead of
    the intended "how consistently does this product map to one account,"
    contaminating the primary IV with the very nuisance factor it's supposed
    to be orthogonal to (research/EXPERIMENT_1_REDESIGN_REVIEW.md §4/§6).
    Grouping by product_code makes realized_det_pct identical whether or not
    lexical variation is on, for the same deterministic_share -- exactly the
    invariant the two-factor design requires."""
    prod_accs = defaultdict(Counter)
    for r in rows:
        if r["product_code"] and r["account_id"]:
            prod_accs[r["product_code"]][r["account_id"]] += 1

    det_sum = 0.0
    n = 0
    dominant_count = 0
    weighted_num = 0.0
    weighted_den = 0
    for counter in prod_accs.values():
        total = sum(counter.values())
        if not total:
            continue
        dominant = counter.most_common(1)[0][1]
        det = dominant / total
        det_sum += det
        n += 1
        if det > det_threshold:
            dominant_count += 1
        weighted_num += det * total
        weighted_den += total

    return {
        "det_pct": (dominant_count / n) if n else 0.0,
        "unweighted_ads": (det_sum / n) if n else 0.0,
        "weighted_ads": (weighted_num / weighted_den) if weighted_den else 0.0,
        "n_products": n,
    }


def compute_cross_company_consistency(rows):
    """Diagnostic/secondary measure only (never the primary IV) -- mirrors
    03_5_dataset_intelligence.py's C.3, restricted to multi-company products.
    Grouped by product_code for the same reason as compute_det_pct above."""
    prod_comp_accs = defaultdict(lambda: defaultdict(Counter))
    for r in rows:
        if r["product_code"] and r["account_id"]:
            prod_comp_accs[r["product_code"]][r["cui"]][r["account_id"]] += 1

    ratios = []
    for by_company in prod_comp_accs.values():
        if len(by_company) < 2:
            continue
        agg = Counter()
        for counter in by_company.values():
            agg.update(counter)
        total = sum(agg.values())
        if not total:
            continue
        ratios.append(agg.most_common(1)[0][1] / total)
    return sum(ratios) / len(ratios) if ratios else 0.0


def realized_ads(lines, det_threshold=0.95):
    """THE entrypoint. Filters to the train split internally -- callers must
    never pre-filter and pass test rows in, and must never call
    compute_det_pct()/compute_cross_company_consistency() directly on an
    unfiltered row set for anything that feeds a decision or an analysis."""
    train_rows = [r for r in lines if split_of(r) == "train"]
    result = compute_det_pct(train_rows, det_threshold)
    result["cross_company_consistency"] = compute_cross_company_consistency(train_rows)
    result["n_train_lines"] = len(train_rows)
    return result


def realized_ads_full_dataset_diagnostic_only(lines, det_threshold=0.95):
    """Non-primary sanity cross-check ONLY (§3) -- computed over train+test
    combined so a large gap vs. realized_ads() can be footnoted. Never used
    for any decision, threshold comparison, or plot axis."""
    return compute_det_pct(lines, det_threshold)

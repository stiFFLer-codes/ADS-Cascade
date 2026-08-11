"""Gate 2 -- dedicated retrieval-cutoff calibration.

research/EXPERIMENT_1_CALIBRATION_REPORT.md Gate 2. Distinct, dedicated
calibration seeds (50001-50005), never touching pilot seeds (101-103, 9001),
ADS-calibration seeds (30001-30010, 40001-40005), or any seed reserved for
the eventual frozen final run.

CRITICAL: does NOT use classification accuracy (whole-set accuracy against
account_id) as the selection criterion -- the approval message explicitly
bans using "mechanism accuracy" to calibrate thresholds. Instead this
calibrates on a RETRIEVAL-QUALITY signal one level below classification:
does the top fuzzy match resolve to the SAME underlying product (product_code)
as the query, at all -- never whether the resulting account_id happens to be
correct. This is standard IR practice for tuning a similarity threshold and
is a strictly weaker, more mechanism-independent signal than classification
accuracy: it never touches account_id, never compares against rules_only,
and never depends on the KB's account-assignment logic.

Run: python scripts/experiments/exp1/calibrate_retrieval_cutoff.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator

gen = load_generator()
from p2lib import kb as kbmod  # noqa: E402
from p2lib.data import split_of  # noqa: E402
from p2lib.retrieval import fuzzy_company, fuzzy_global  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "outputs" / "experiments" / "exp1" / "calibration"

CALIBRATION_SEEDS = list(range(50001, 50006))  # 5 independent seeds, distinct from every other run
CALIBRATION_DET_SHARE = 0.80          # representative mid-range band (not one of the frozen ADS regions)
CALIBRATION_LEXICAL_VARIATION = True  # calibrate where the cutoff actually matters (§ pilot: under
                                       # CLEAN, rules and retrieval tie regardless of cutoff)
CALIBRATION_P_TRANSFORM = 0.3         # frozen value from the pilot session

CANDIDATE_CUTOFFS = [60, 65, 70, 75, 80, 85, 90, 95]
MIN_COVERAGE = 0.30
NEAR_TIE_MARGIN = 0.01  # in hit-rate units, same convention as the pilot's accuracy-curve tie rule


def product_code_lookup(train_rows):
    """normalized_product -> product_code, built ONLY from train (never test).
    One-to-one in practice (see code comment in the calibration report) --
    the numeric product index token is never altered by any lexical
    transform, so collisions across different true products are not expected;
    guarded defensively below regardless."""
    lookup = {}
    for r in train_rows:
        key = r["normalized_product"]
        if key in lookup and lookup[key] != r["product_code"]:
            continue  # keep first-seen mapping; do not silently overwrite on a rare collision
        lookup[key] = r["product_code"]
    return lookup


def retrieval_hit_rate(kb, code_of, test_rows, cutoff):
    """hit = top retrieval match's product_code equals the query's true
    product_code. Abstention (no match above cutoff) and a wrong-product
    match both count as non-hits -- classification/account_id never enters."""
    hits = matched = 0
    for r in test_rows:
        cui, product, direction, true_code = r["cui"], r["normalized_product"], r["direction"], r["product_code"]

        matched_product = None
        company_matches = fuzzy_company(kb, cui, product, cutoff=cutoff)
        if company_matches:
            matched_product = company_matches[0][0]
        else:
            pool = list(kb.glob.keys())
            global_matches = fuzzy_global(product, pool, cutoff=cutoff)
            if global_matches:
                matched_product = global_matches[0][0]

        if matched_product is None:
            continue  # abstain -- non-hit, not counted as "matched" either

        matched += 1
        if code_of.get(matched_product) == true_code:
            hits += 1

    total = len(test_rows)
    return {
        "cutoff": cutoff,
        "hit_rate": hits / total if total else 0.0,
        "coverage": matched / total if total else 0.0,
        "hits": hits, "matched": matched, "total": total,
    }


def calibrate_for_seed(seed):
    _, lines = gen.gen_dataset(seed=seed, deterministic_share=CALIBRATION_DET_SHARE,
                                lexical_variation=CALIBRATION_LEXICAL_VARIATION,
                                p_transform=CALIBRATION_P_TRANSFORM)
    train = [r for r in lines if split_of(r) == "train"]
    test = [r for r in lines if split_of(r) == "test"]
    kb = kbmod.build_from_rows(train)
    code_of = product_code_lookup(train)
    return [retrieval_hit_rate(kb, code_of, test, cutoff) for cutoff in CANDIDATE_CUTOFFS]


def select_cutoff(pooled_curve):
    eligible = [c for c in pooled_curve if c["coverage"] >= MIN_COVERAGE]
    pool = eligible or pooled_curve
    best = max(c["hit_rate"] for c in pool)
    near_ties = [c for c in pool if best - c["hit_rate"] <= NEAR_TIE_MARGIN]
    return max(near_ties, key=lambda c: c["cutoff"])  # conservative: highest near-tied cutoff


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Gate 2 -- dedicated retrieval-cutoff calibration (product-identity hit-rate, "
          "NOT classification accuracy)\n")

    per_seed_curves = {seed: calibrate_for_seed(seed) for seed in CALIBRATION_SEEDS}

    pooled_curve = []
    for i, cutoff in enumerate(CANDIDATE_CUTOFFS):
        total_hits = sum(per_seed_curves[s][i]["hits"] for s in CALIBRATION_SEEDS)
        total_matched = sum(per_seed_curves[s][i]["matched"] for s in CALIBRATION_SEEDS)
        total_n = sum(per_seed_curves[s][i]["total"] for s in CALIBRATION_SEEDS)
        pooled_curve.append({
            "cutoff": cutoff,
            "hit_rate": total_hits / total_n if total_n else 0.0,
            "coverage": total_matched / total_n if total_n else 0.0,
            "hits": total_hits, "matched": total_matched, "total": total_n,
        })

    chosen = select_cutoff(pooled_curve)

    print(f"{'cutoff':>8} {'hit_rate':>10} {'coverage':>10}")
    for c in pooled_curve:
        print(f"{c['cutoff']:>8} {c['hit_rate']:>10.4f} {c['coverage']:>10.4f}")
    print(f"\nSelected cutoff = {chosen['cutoff']} "
          f"(hit_rate={chosen['hit_rate']:.4f}, coverage={chosen['coverage']:.4f})")

    report = {
        "label": "CALIBRATION -- GATE 2, product-identity hit-rate (not classification accuracy)",
        "calibration_seeds": CALIBRATION_SEEDS,
        "calibration_deterministic_share": CALIBRATION_DET_SHARE,
        "calibration_lexical_variation": CALIBRATION_LEXICAL_VARIATION,
        "calibration_p_transform": CALIBRATION_P_TRANSFORM,
        "candidate_cutoffs": CANDIDATE_CUTOFFS,
        "min_coverage_floor": MIN_COVERAGE,
        "near_tie_margin": NEAR_TIE_MARGIN,
        "selection_rule": "max product-identity hit-rate subject to coverage>=0.30; "
                           "ties within 0.01 hit-rate -> highest (most conservative) cutoff",
        "per_seed_curves": {str(s): per_seed_curves[s] for s in CALIBRATION_SEEDS},
        "pooled_curve": pooled_curve,
        "selected_cutoff": chosen["cutoff"],
    }
    (OUT / "retrieval_cutoff_calibration.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n-> {OUT / 'retrieval_cutoff_calibration.json'}")


if __name__ == "__main__":
    main()

"""Experiment 1 PILOT runner.

research/EXPERIMENT_1_REDESIGN_REVIEW.md §17 / Phase D approval message's
"PILOT ONLY" instructions. Purpose: verify the harness mechanics (generator,
realized-ADS measurement, leakage safety, mechanism isolation, lexical
challenge, metrics, reproducibility, runtime) -- NOT to produce an H1 result.

Every output of this script is labeled PILOT -- NOT FINAL EVIDENCE and must
never be cited as evidence for or against H1. The frozen >=20-seed run is a
separate, later, explicitly-approved step.

Run: python scripts/experiments/exp1/run_pilot.py
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator
from consistency import realized_ads
from mechanisms import classify_rules, classify_retrieval
import stats

gen = load_generator()
from p2lib import kb as kbmod  # noqa: E402
from p2lib.data import split_of  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "outputs" / "experiments" / "exp1" / "pilot"

# --- Pilot scope (small, per §17: 1-3 seeds, extremes + threshold band) ---
PILOT_BANDS = [0.60, 0.90, 0.99]
PILOT_SEEDS = [101, 102, 103]
LEXICAL_CONDITIONS = [False, True]

# Frozen from the outcome-independent selection in select_p_transform.py.
FROZEN_P_TRANSFORM = 0.3

# PILOT-only retrieval cutoff calibration (mechanics check, not the frozen
# final threshold -- research/EXPERIMENT_1_REDESIGN_REVIEW.md §12/§23.2: the
# real calibration run needs its own author-approved protocol/seed before the
# frozen sweep. This one reuses the same calibration seed/band as
# select_p_transform.py purely to exercise the calibration code path.)
CALIBRATION_SEED = 9001
CALIBRATION_DET_SHARE = 0.80
CANDIDATE_CUTOFFS = [70, 75, 80, 85, 90]
MIN_COVERAGE = 0.30


def pilot_calibrate_retrieval_cutoff():
    _, lines = gen.gen_dataset(seed=CALIBRATION_SEED, deterministic_share=CALIBRATION_DET_SHARE)
    train = [r for r in lines if split_of(r) == "train"]
    test = [r for r in lines if split_of(r) == "test"]
    kb = kbmod.build_from_rows(train)

    curve = []
    for cutoff in CANDIDATE_CUTOFFS:
        preds, truths = [], []
        for r in test:
            preds.append(classify_retrieval(kb, r["cui"], r["normalized_product"], r["direction"], cutoff=cutoff))
            truths.append(r["account_id"])
        acc = stats.whole_set_accuracy(preds, truths)
        cov = stats.coverage(preds)
        curve.append({"cutoff": cutoff, "accuracy": acc, "coverage": cov})

    eligible = [c for c in curve if c["coverage"] >= MIN_COVERAGE]
    pool = eligible or curve
    best_acc = max(c["accuracy"] for c in pool)
    near_ties = [c for c in pool if best_acc - c["accuracy"] <= 0.01]
    chosen = max(near_ties, key=lambda c: c["cutoff"])  # conservative: highest near-tied cutoff
    return chosen["cutoff"], curve


def run_condition(seed, det_share, lexical_variation):
    p_transform = FROZEN_P_TRANSFORM if lexical_variation else 0.0
    t0 = time.perf_counter()
    _, lines = gen.gen_dataset(seed=seed, deterministic_share=det_share,
                                lexical_variation=lexical_variation, p_transform=p_transform)
    train = [r for r in lines if split_of(r) == "train"]
    test = [r for r in lines if split_of(r) == "test"]

    ads = realized_ads(lines)
    kb = kbmod.build_from_rows(train)

    rules_preds, retrieval_preds, truths = [], [], []
    for r in test:
        rules_preds.append(classify_rules(kb, r["cui"], r["normalized_product"], r["direction"]))
        retrieval_preds.append(classify_retrieval(kb, r["cui"], r["normalized_product"], r["direction"],
                                                    cutoff=RETRIEVAL_CUTOFF))
        truths.append(r["account_id"])

    rules_correct = [1 if (not p["abstain"]) and p["account_id"] == t else 0
                      for p, t in zip(rules_preds, truths)]
    retrieval_correct = [1 if (not p["abstain"]) and p["account_id"] == t else 0
                          for p, t in zip(retrieval_preds, truths)]

    rules_acc = sum(rules_correct) / len(truths) if truths else 0.0
    retrieval_acc = sum(retrieval_correct) / len(truths) if truths else 0.0
    rules_ci = stats.bootstrap_ci(rules_correct, n_resamples=500, seed=seed)
    retrieval_ci = stats.bootstrap_ci(retrieval_correct, n_resamples=500, seed=seed)

    divergent = sum(1 for rp, vp in zip(rules_preds, retrieval_preds)
                     if rp["account_id"] != vp["account_id"] or rp["abstain"] != vp["abstain"])
    divergence_rate = divergent / len(test) if test else 0.0

    winner = stats.empirical_winner(rules_acc, retrieval_acc, rules_ci, retrieval_ci)
    rule_selected = stats.r3_rule_selection(ads["det_pct"])

    elapsed = time.perf_counter() - t0
    return {
        "label": "PILOT -- NOT FINAL EVIDENCE",
        "seed": seed, "target_deterministic_share": det_share,
        "lexical_variation": lexical_variation, "p_transform": p_transform,
        "realized_det_pct": round(ads["det_pct"], 4),
        "weighted_ads": round(ads["weighted_ads"], 4),
        "unweighted_ads": round(ads["unweighted_ads"], 4),
        "cross_company_consistency": round(ads["cross_company_consistency"], 4),
        "n_products_train": ads["n_products"],
        "n_train_lines": len(train), "n_test_lines": len(test),
        "rules_whole_set_accuracy": round(rules_acc, 4),
        "rules_coverage": round(stats.coverage(rules_preds), 4),
        "rules_ci_low": round(rules_ci["ci_low"], 4) if rules_ci else None,
        "rules_ci_high": round(rules_ci["ci_high"], 4) if rules_ci else None,
        "retrieval_whole_set_accuracy": round(retrieval_acc, 4),
        "retrieval_coverage": round(stats.coverage(retrieval_preds), 4),
        "retrieval_ci_low": round(retrieval_ci["ci_low"], 4) if retrieval_ci else None,
        "retrieval_ci_high": round(retrieval_ci["ci_high"], 4) if retrieval_ci else None,
        "mechanism_divergence_rate": round(divergence_rate, 4),
        "empirical_winner": winner,
        "rule_selected": rule_selected,
        "elapsed_seconds": round(elapsed, 3),
    }


def main():
    global RETRIEVAL_CUTOFF
    OUT.mkdir(parents=True, exist_ok=True)

    print("PILOT -- NOT FINAL EVIDENCE\n")
    print("Step 1/2: PILOT retrieval-cutoff calibration (mechanics check only)...")
    RETRIEVAL_CUTOFF, calib_curve = pilot_calibrate_retrieval_cutoff()
    print(f"  pilot-calibrated cutoff = {RETRIEVAL_CUTOFF} (curve: {calib_curve})\n")

    print("Step 2/2: running pilot conditions...")
    results = []
    t0 = time.perf_counter()
    for det_share in PILOT_BANDS:
        for lexical in LEXICAL_CONDITIONS:
            for seed in PILOT_SEEDS:
                r = run_condition(seed, det_share, lexical)
                r["retrieval_cutoff_used"] = RETRIEVAL_CUTOFF
                results.append(r)
                print(f"  band={det_share} lex={lexical} seed={seed}  "
                      f"realized_ADS={r['realized_det_pct']}  "
                      f"rules_acc={r['rules_whole_set_accuracy']}  "
                      f"retrieval_acc={r['retrieval_whole_set_accuracy']}  "
                      f"winner={r['empirical_winner']}  rule={r['rule_selected']}  "
                      f"divergence={r['mechanism_divergence_rate']}  "
                      f"({r['elapsed_seconds']}s)")
    total_elapsed = time.perf_counter() - t0

    fieldnames = list(results[0].keys())
    with open(OUT / "pilot_conditions.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(results)

    agreement = stats.selection_agreement(results)
    n_conditions = len(results)
    n_bands_lex = len(PILOT_BANDS) * len(LEXICAL_CONDITIONS)
    projected_full_sweep_conditions = 6 * 2 * 20  # 6 bands x 2 lexical x >=20 seeds
    projected_seconds = (total_elapsed / n_conditions) * projected_full_sweep_conditions

    summary = {
        "label": "PILOT -- NOT FINAL EVIDENCE",
        "n_pilot_conditions": n_conditions,
        "pilot_bands": PILOT_BANDS, "pilot_seeds": PILOT_SEEDS,
        "frozen_p_transform_used": FROZEN_P_TRANSFORM,
        "pilot_calibrated_retrieval_cutoff": RETRIEVAL_CUTOFF,
        "pilot_calibration_curve": calib_curve,
        "illustrative_selection_agreement_NOT_AN_H1_VERDICT": agreement,
        "total_elapsed_seconds": round(total_elapsed, 2),
        "seconds_per_condition": round(total_elapsed / n_conditions, 3),
        "projected_full_sweep_seconds_6x2x20": round(projected_seconds, 1),
        "projected_full_sweep_minutes_6x2x20": round(projected_seconds / 60, 1),
    }
    (OUT / "pilot_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nTotal pilot runtime: {total_elapsed:.2f}s over {n_conditions} conditions "
          f"({total_elapsed/n_conditions:.3f}s/condition)")
    print(f"Projected full sweep (6 bands x 2 lexical x 20 seeds = {projected_full_sweep_conditions} conditions): "
          f"~{projected_seconds/60:.1f} minutes")
    print(f"\nIllustrative selection agreement (PILOT ONLY, NOT an H1 verdict): {agreement}")
    print(f"\n-> {OUT / 'pilot_conditions.csv'}")
    print(f"-> {OUT / 'pilot_summary.json'}")


if __name__ == "__main__":
    main()

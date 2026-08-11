"""Gate 1 -- mechanism-BLIND ADS generation calibration.

research/EXPERIMENT_1_CALIBRATION_REPORT.md Gate 1. This script NEVER calls
classify_rules/classify_retrieval and NEVER reads account_id for anything
other than the train-only realized-ADS computation itself (which is the
quantity under calibration, not a mechanism's classification correctness).
No accuracy of any kind is computed here.

Sweeps a dense target `deterministic_share` grid, multiple independent seeds
each, records realized train-only ADS (mean/std/min/max), and applies a
purely realized-ADS-based (never mechanism-based) rule to recommend final
experimental ADS regions.

Run: python scripts/experiments/exp1/calibrate_ads.py
"""
import csv
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator
from consistency import realized_ads

gen = load_generator()

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "outputs" / "experiments" / "exp1" / "calibration"

# Dense grid covering >= the original 6 targets plus intermediate values.
# Distinct from every pilot seed (101-103, 9001) and every retrieval-cutoff
# calibration seed (see calibrate_retrieval_cutoff.py) -- documented, fixed,
# not re-picked after seeing results.
TARGET_GRID = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.55, 0.60, 0.65, 0.70,
               0.75, 0.80, 0.85, 0.90, 0.95, 0.99, 1.00]
# Extended below the original [0.60, 0.99] range: a first pass at the original
# grid found the ceiling structurally capped near ~0.90-0.91 regardless of
# target (see report), which motivated checking whether the floor had
# similarly unused headroom -- it did (target=0.0 reaches realized ~0.50),
# so the grid was widened down to 0.0 before freezing this calibration run.
CALIBRATION_SEEDS = list(range(30001, 30011))  # 10 independent seeds per target

R3_RULES_THRESHOLD = 0.90
R3_RETRIEVAL_THRESHOLD = 0.70

N_FINAL_REGIONS = 6  # matches the original design's band count


def run_sweep(lexical_variation=False, p_transform=0.0):
    rows = []
    failures = []
    for target in TARGET_GRID:
        for seed in CALIBRATION_SEEDS:
            try:
                _, lines = gen.gen_dataset(seed=seed, deterministic_share=target,
                                            lexical_variation=lexical_variation, p_transform=p_transform)
                ads = realized_ads(lines)
                if ads["n_products"] == 0 or ads["n_train_lines"] == 0:
                    failures.append({"target": target, "seed": seed, "reason": "empty train/product set"})
                    continue
                rows.append({
                    "target_deterministic_share": target, "seed": seed,
                    "lexical_variation": lexical_variation,
                    "realized_det_pct": ads["det_pct"],
                    "weighted_ads": ads["weighted_ads"],
                    "unweighted_ads": ads["unweighted_ads"],
                    "cross_company_consistency": ads["cross_company_consistency"],
                    "n_products_train": ads["n_products"],
                    "n_train_lines": ads["n_train_lines"],
                })
            except Exception as e:  # noqa: BLE001 -- record and continue, never crash the sweep
                failures.append({"target": target, "seed": seed, "reason": repr(e)})
    return rows, failures


def summarize(rows):
    by_target = {}
    for target in TARGET_GRID:
        vals = [r["realized_det_pct"] for r in rows if r["target_deterministic_share"] == target]
        if not vals:
            continue
        by_target[target] = {
            "target": target,
            "n_seeds": len(vals),
            "mean": statistics.mean(vals),
            "std": statistics.stdev(vals) if len(vals) > 1 else 0.0,
            "min": min(vals),
            "max": max(vals),
        }
    return by_target


def furthest_point_selection(summary, k):
    """Greedy furthest-point selection over realized mean ADS -- purely a
    function of the calibration curve, deterministic, no mechanism signal."""
    targets = sorted(summary.keys(), key=lambda t: summary[t]["mean"])
    if len(targets) <= k:
        return targets
    means = {t: summary[t]["mean"] for t in targets}
    selected = [targets[0], targets[-1]]  # extremes first, maximize range
    remaining = [t for t in targets if t not in selected]
    while len(selected) < k and remaining:
        best_t, best_dist = None, -1
        for t in remaining:
            dist = min(abs(means[t] - means[s]) for s in selected)
            if dist > best_dist:
                best_t, best_dist = t, dist
        selected.append(best_t)
        remaining.remove(best_t)
    return sorted(selected, key=lambda t: means[t])


def anchor_boundary_targets(summary, selected, threshold, tolerance=0.03):
    """If no selected target's realized mean sits within `tolerance` of a
    threshold (0.70 or 0.90), add the single closest candidate from the WHOLE
    grid (not just the selected set) -- still purely realized-mean-distance
    based, never mechanism-based."""
    means = {t: summary[t]["mean"] for t in summary}
    if any(abs(means[t] - threshold) <= tolerance for t in selected):
        return selected, None
    closest = min(means, key=lambda t: abs(means[t] - threshold))
    if closest not in selected:
        return sorted(selected + [closest], key=lambda t: means[t]), closest
    return selected, None


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("Gate 1 -- mechanism-BLIND ADS calibration sweep (CLEAN condition)")
    rows_clean, failures_clean = run_sweep(lexical_variation=False)
    summary_clean = summarize(rows_clean)

    print("Spot-check: VARIED condition at 3 targets, confirming realized ADS "
          "invariance to lexical condition (fixed in the pilot session)...")
    spot_targets = [0.60, 0.80, 0.95]
    rows_varied = []
    for target in spot_targets:
        for seed in CALIBRATION_SEEDS[:3]:
            _, lines = gen.gen_dataset(seed=seed, deterministic_share=target,
                                        lexical_variation=True, p_transform=0.3)
            ads = realized_ads(lines)
            rows_varied.append({"target": target, "seed": seed, "realized_det_pct": ads["det_pct"]})

    invariance_check = []
    for r in rows_varied:
        clean_match = next((c for c in rows_clean
                             if c["target_deterministic_share"] == r["target"] and c["seed"] == r["seed"]), None)
        if clean_match:
            invariance_check.append({
                "target": r["target"], "seed": r["seed"],
                "clean_realized": clean_match["realized_det_pct"],
                "varied_realized": r["realized_det_pct"],
                "match": abs(clean_match["realized_det_pct"] - r["realized_det_pct"]) < 1e-9,
            })

    with open(OUT / "ads_calibration_raw.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_clean[0].keys()))
        w.writeheader()
        w.writerows(rows_clean)

    selected = furthest_point_selection(summary_clean, N_FINAL_REGIONS)
    selected, anchor_70 = anchor_boundary_targets(summary_clean, selected, R3_RETRIEVAL_THRESHOLD)
    selected, anchor_90 = anchor_boundary_targets(summary_clean, selected, R3_RULES_THRESHOLD)

    report = {
        "label": "CALIBRATION -- mechanism-blind, GATE 1",
        "target_grid": TARGET_GRID,
        "calibration_seeds": CALIBRATION_SEEDS,
        "n_seeds_per_target": len(CALIBRATION_SEEDS),
        "failures": failures_clean,
        "summary_by_target": summary_clean,
        "lexical_invariance_spot_check": invariance_check,
        "selection_rule": (
            f"greedy furthest-point selection (k={N_FINAL_REGIONS}) over realized mean ADS, "
            f"then boundary-anchor insertion within 0.03 of {R3_RETRIEVAL_THRESHOLD} and {R3_RULES_THRESHOLD} "
            f"if not already covered by the greedy selection -- never touches mechanism performance"
        ),
        "recommended_final_targets": selected,
        "boundary_anchor_added_for_0.70": anchor_70,
        "boundary_anchor_added_for_0.90": anchor_90,
    }
    (OUT / "ads_calibration_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\n{'target':>8} {'n':>4} {'mean':>8} {'std':>8} {'min':>8} {'max':>8}")
    for t in TARGET_GRID:
        if t in summary_clean:
            s = summary_clean[t]
            print(f"{t:>8} {s['n_seeds']:>4} {s['mean']:>8.4f} {s['std']:>8.4f} {s['min']:>8.4f} {s['max']:>8.4f}")

    print(f"\nFailures: {len(failures_clean)}")
    print(f"Lexical invariance spot-check (all should be match=True): {invariance_check}")
    print(f"\nRecommended final targets (mechanism-blind selection): {selected}")
    if anchor_70:
        print(f"  boundary anchor added near 0.70: {anchor_70}")
    if anchor_90:
        print(f"  boundary anchor added near 0.90: {anchor_90}")
    print(f"\n-> {OUT / 'ads_calibration_raw.csv'}")
    print(f"-> {OUT / 'ads_calibration_summary.json'}")


if __name__ == "__main__":
    main()

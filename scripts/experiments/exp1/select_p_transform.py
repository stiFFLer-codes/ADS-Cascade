"""Outcome-independent P_TRANSFORM candidate selection
(research/EXPERIMENT_1_REDESIGN_REVIEW.md §8; Phase D approval message's
explicit ban on choosing P_TRANSFORM by mechanism accuracy).

Evaluates candidates {0.3, 0.5, 0.7} using ONLY:
  - surface-form disruption rate (target band: 15-40%, midpoint 27.5%)
  - transform-type balance (informational)
  - retrieval-challenge severity (WRatio(original, transformed), informational)
  - semantic-identity preservation (must be True, or the candidate is invalid)

Never reads account_id, never runs classify_rules/classify_retrieval, never
computes any accuracy. Picks the candidate whose disruption_rate lands
closest to 27.5%, ties broken toward the smaller (more conservative)
P_TRANSFORM.

Run: python scripts/experiments/exp1/select_p_transform.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator
from lexical_diagnostics import diagnose

gen = load_generator()

CANDIDATES = [0.3, 0.5, 0.7]
TARGET_MID = 0.275
CALIBRATION_SEED = 9001              # distinct from every seed used in the pilot/frozen run
CALIBRATION_DET_SHARE = 0.80         # generic midpoint band, not one of the 6 official targets

OUT_DIR = Path(__file__).resolve().parents[3] / "data" / "outputs" / "experiments" / "exp1" / "pilot"


def evaluate_candidate(p_transform):
    _, lines = gen.gen_dataset(seed=CALIBRATION_SEED, deterministic_share=CALIBRATION_DET_SHARE,
                                lexical_variation=True, p_transform=p_transform)
    d = diagnose(lines)
    disruption = d["disruption"]["disruption_rate"]
    return {
        "p_transform": p_transform,
        "semantic_identity_preserved": d["semantic_identity"]["preserved"],
        "disruption_rate": disruption,
        "disruptable_test_lines": d["disruption"]["disruptable_test_lines"],
        "distance_from_target_mid": abs(disruption - TARGET_MID) if disruption is not None else None,
        "transform_type_counts": d["balance"]["transform_type_counts"],
        "transformed_share_of_all_lines": d["balance"]["transformed_share"],
        "severity_mean_wratio": d["severity"]["mean_score"],
        "severity_min_wratio": d["severity"]["min_score"],
        "severity_pct_below_70": d["severity"]["pct_below_70"],
    }


def select(results):
    valid = [r for r in results if r["semantic_identity_preserved"] and r["disruption_rate"] is not None]
    if not valid:
        return None
    valid.sort(key=lambda r: (r["distance_from_target_mid"], r["p_transform"]))
    return valid[0]


def main():
    results = [evaluate_candidate(p) for p in CANDIDATES]
    chosen = select(results)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "label": "PILOT -- NOT FINAL EVIDENCE",
        "purpose": "outcome-independent P_TRANSFORM candidate selection",
        "calibration_seed": CALIBRATION_SEED,
        "calibration_deterministic_share": CALIBRATION_DET_SHARE,
        "target_disruption_band": [0.15, 0.40],
        "candidates": results,
        "selected_p_transform": chosen["p_transform"] if chosen else None,
        "selection_rule": "closest disruption_rate to 27.5% midpoint; ties -> smaller p_transform",
    }
    (OUT_DIR / "p_transform_selection.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("PILOT -- NOT FINAL EVIDENCE")
    print(f"{'p_transform':>12} {'disruption_rate':>16} {'mean_wratio':>12} {'preserved':>10}")
    for r in results:
        print(f"{r['p_transform']:>12} {r['disruption_rate']:>16.3f} "
              f"{r['severity_mean_wratio']:>12.1f} {str(r['semantic_identity_preserved']):>10}")
    print(f"\nSelected P_TRANSFORM = {chosen['p_transform']} "
          f"(disruption_rate={chosen['disruption_rate']:.3f}, target midpoint=0.275)")
    print(f"-> {OUT_DIR / 'p_transform_selection.json'}")


if __name__ == "__main__":
    main()

"""Experiment 1 -- FINAL frozen run (H1).

research/EXPERIMENT_1_CALIBRATION_REPORT.md + the Phase D checkpoint commit
(3c6b581178aa7cd3598e112f96f1321d61d60aa9) freeze every configuration value
this script uses. It calls the EXISTING, UNMODIFIED harness modules
(consistency.py, mechanisms.py, stats.py) -- no methodology, threshold,
mechanism, or winner-definition logic is redefined here. This script is
orchestration only: build the seed manifest, run all 240 conditions
uniformly, persist raw artifacts.

Do not inspect intermediate results to change configuration. Do not stop
early. Do not selectively rerun a condition. All 240 conditions are treated
identically.

Run: python scripts/experiments/exp1/run_final.py
"""
import csv
import itertools
import json
import statistics
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
OUT = ROOT / "data" / "outputs" / "experiments" / "exp1" / "final"

# ---------------------------------------------------------------------------
# FROZEN CONFIGURATION -- do not edit without a new, explicitly-approved gate.
# ---------------------------------------------------------------------------
TARGETS = [0.00, 0.20, 0.30, 0.50, 0.75, 1.00]
LEXICAL_CONDITIONS = [False, True]
P_TRANSFORM = 0.3
RETRIEVAL_CUTOFF = 75
SEEDS = list(range(31001, 31021))  # exactly the 20 pre-registered seeds, same list every condition
BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_ALPHA = 0.05
PRACTICAL_EQUIVALENCE_DELTA = stats.PRACTICAL_EQUIVALENCE_DELTA  # 0.02, imported not redefined

assert PRACTICAL_EQUIVALENCE_DELTA == 0.02
assert RETRIEVAL_CUTOFF == 75
assert P_TRANSFORM == 0.3
assert len(SEEDS) == 20
assert stats.R3_RULES_THRESHOLD == 0.90 and stats.R3_RETRIEVAL_THRESHOLD == 0.70


def print_frozen_config():
    cfg = {
        "TARGETS": TARGETS, "LEXICAL_CONDITIONS": LEXICAL_CONDITIONS,
        "P_TRANSFORM": P_TRANSFORM, "RETRIEVAL_CUTOFF": RETRIEVAL_CUTOFF,
        "MECHANISMS": ["rules_only", "retrieval_only"], "LLM": "excluded",
        "PRIMARY_INDEPENDENT_VARIABLE": "realized_train_ADS",
        "PRIMARY_METRIC": "whole_set_accuracy", "WINNER": "paired_bootstrap_winner",
        "BOOTSTRAP_RESAMPLES": BOOTSTRAP_RESAMPLES, "BOOTSTRAP_ALPHA": BOOTSTRAP_ALPHA,
        "PRACTICAL_EQUIVALENCE_DELTA": PRACTICAL_EQUIVALENCE_DELTA,
        "SEEDS": f"{SEEDS[0]}-{SEEDS[-1]} ({len(SEEDS)} seeds)",
        "R3_RULES_THRESHOLD": stats.R3_RULES_THRESHOLD,
        "R3_RETRIEVAL_THRESHOLD": stats.R3_RETRIEVAL_THRESHOLD,
        "TOTAL_CONDITIONS": len(TARGETS) * len(LEXICAL_CONDITIONS) * len(SEEDS),
    }
    print(json.dumps(cfg, indent=2))
    return cfg


def write_seed_manifest():
    path = OUT / "final_seed_manifest.csv"
    rows = []
    for target, lexical in itertools.product(TARGETS, LEXICAL_CONDITIONS):
        for seed in SEEDS:
            rows.append({
                "seed": seed, "target_deterministic_share": target, "lexical_variation": lexical,
            })
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["seed", "target_deterministic_share", "lexical_variation"])
        w.writeheader()
        w.writerows(rows)
    assert len(rows) == len(TARGETS) * len(LEXICAL_CONDITIONS) * len(SEEDS)
    return rows, path


def run_condition(seed, target, lexical):
    p_transform = P_TRANSFORM if lexical else 0.0
    t0 = time.perf_counter()
    try:
        _, lines = gen.gen_dataset(seed=seed, deterministic_share=target,
                                    lexical_variation=lexical, p_transform=p_transform)
        train = [r for r in lines if split_of(r) == "train"]
        test = [r for r in lines if split_of(r) == "test"]
        if not train or not test:
            raise RuntimeError(f"empty split: train={len(train)} test={len(test)}")

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

        rules_acc = stats.whole_set_accuracy(rules_preds, truths)
        retrieval_acc = stats.whole_set_accuracy(retrieval_preds, truths)
        rules_cov = stats.coverage(rules_preds)
        retrieval_cov = stats.coverage(retrieval_preds)

        winner, diff_ci = stats.paired_bootstrap_winner(
            rules_correct, retrieval_correct,
            delta=PRACTICAL_EQUIVALENCE_DELTA, n_resamples=BOOTSTRAP_RESAMPLES,
            alpha=BOOTSTRAP_ALPHA, seed=seed,
        )
        r3_selected = stats.r3_rule_selection(ads["det_pct"])
        if r3_selected == "llm_required":
            agrees = None  # N/A -- rule selects an excluded mechanism (§14 of the redesign review)
        else:
            agrees = (r3_selected == winner) if winner != "tie" else None

        elapsed = time.perf_counter() - t0
        return {
            "status": "ok",
            "seed": seed, "target_deterministic_share": target, "lexical_variation": lexical,
            "p_transform": p_transform,
            "realized_det_pct": ads["det_pct"], "weighted_ads": ads["weighted_ads"],
            "unweighted_ads": ads["unweighted_ads"],
            "cross_company_consistency": ads["cross_company_consistency"],
            "n_products_train": ads["n_products"], "n_train_lines": len(train), "n_test_lines": len(test),
            "rules_whole_set_accuracy": rules_acc, "rules_coverage": rules_cov,
            "retrieval_whole_set_accuracy": retrieval_acc, "retrieval_coverage": retrieval_cov,
            "retrieval_cutoff_used": RETRIEVAL_CUTOFF,
            "paired_diff_point": diff_ci["diff_point"] if diff_ci else None,
            "paired_diff_ci_low": diff_ci["diff_ci_low"] if diff_ci else None,
            "paired_diff_ci_high": diff_ci["diff_ci_high"] if diff_ci else None,
            "empirical_winner": winner,
            "r3_selected_mechanism": r3_selected,
            "r3_agrees_with_empirical": agrees,
            "elapsed_seconds": round(elapsed, 3),
        }
    except Exception as e:  # noqa: BLE001 -- record, never crash the run; all 240 must be attempted
        elapsed = time.perf_counter() - t0
        return {
            "status": "failed", "seed": seed, "target_deterministic_share": target,
            "lexical_variation": lexical, "error": repr(e), "elapsed_seconds": round(elapsed, 3),
        }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 70)
    print("EXPERIMENT 1 -- FINAL FROZEN RUN")
    print("Frozen at commit 3c6b581178aa7cd3598e112f96f1321d61d60aa9")
    print("=" * 70)
    cfg = print_frozen_config()
    (OUT / "final_frozen_config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    manifest_rows, manifest_path = write_seed_manifest()
    print(f"\nSeed manifest: {len(manifest_rows)} rows -> {manifest_path}")

    print(f"\nExecuting {len(manifest_rows)} conditions uniformly (no early stop, no selective rerun)...")
    t_start = time.perf_counter()
    results = []
    for i, row in enumerate(manifest_rows, start=1):
        r = run_condition(row["seed"], row["target_deterministic_share"], row["lexical_variation"])
        results.append(r)
        if i % 20 == 0 or r["status"] == "failed":
            print(f"  [{i:3d}/{len(manifest_rows)}] target={row['target_deterministic_share']} "
                  f"lex={row['lexical_variation']} seed={row['seed']} status={r['status']}")
    total_elapsed = time.perf_counter() - t_start

    ok_results = [r for r in results if r["status"] == "ok"]
    failed_results = [r for r in results if r["status"] != "ok"]

    # final_conditions.csv -- the manifest as actually executed (post-generation realized values)
    with open(OUT / "final_conditions.csv", "w", encoding="utf-8", newline="") as f:
        fieldnames = ["seed", "target_deterministic_share", "lexical_variation", "status",
                      "realized_det_pct", "n_train_lines", "n_test_lines"]
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in results:
            row = dict(r)
            row.setdefault("realized_det_pct", None)
            row.setdefault("n_train_lines", None)
            row.setdefault("n_test_lines", None)
            w.writerow(row)

    # final_condition_results.csv -- full per-condition results (the primary raw artifact)
    if ok_results:
        result_fields = list(ok_results[0].keys())
        with open(OUT / "final_condition_results.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=result_fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(ok_results)

    # final_bootstrap_results.csv -- bootstrap-focused projection
    with open(OUT / "final_bootstrap_results.csv", "w", encoding="utf-8", newline="") as f:
        fieldnames = ["seed", "target_deterministic_share", "lexical_variation",
                      "paired_diff_point", "paired_diff_ci_low", "paired_diff_ci_high",
                      "empirical_winner", "bootstrap_resamples", "bootstrap_alpha", "delta"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in ok_results:
            w.writerow({
                "seed": r["seed"], "target_deterministic_share": r["target_deterministic_share"],
                "lexical_variation": r["lexical_variation"],
                "paired_diff_point": r["paired_diff_point"], "paired_diff_ci_low": r["paired_diff_ci_low"],
                "paired_diff_ci_high": r["paired_diff_ci_high"], "empirical_winner": r["empirical_winner"],
                "bootstrap_resamples": BOOTSTRAP_RESAMPLES, "bootstrap_alpha": BOOTSTRAP_ALPHA,
                "delta": PRACTICAL_EQUIVALENCE_DELTA,
            })

    # final_summary.csv -- aggregated by (target, lexical)
    summary_rows = []
    for target, lexical in itertools.product(TARGETS, LEXICAL_CONDITIONS):
        group = [r for r in ok_results
                 if r["target_deterministic_share"] == target and r["lexical_variation"] == lexical]
        if not group:
            continue
        realized_vals = [r["realized_det_pct"] for r in group]
        rules_accs = [r["rules_whole_set_accuracy"] for r in group]
        retrieval_accs = [r["retrieval_whole_set_accuracy"] for r in group]
        winners = [r["empirical_winner"] for r in group]
        r3_sels = [r["r3_selected_mechanism"] for r in group]
        agree_defined = [r["r3_agrees_with_empirical"] for r in group if r["r3_agrees_with_empirical"] is not None]
        summary_rows.append({
            "target_deterministic_share": target, "lexical_variation": lexical, "n_seeds": len(group),
            "realized_ads_mean": round(sum(realized_vals) / len(realized_vals), 4),
            "realized_ads_std": round(statistics.stdev(realized_vals), 4) if len(realized_vals) > 1 else 0.0,
            "rules_acc_mean": round(sum(rules_accs) / len(rules_accs), 4),
            "retrieval_acc_mean": round(sum(retrieval_accs) / len(retrieval_accs), 4),
            "n_rules_wins": winners.count("rules"), "n_retrieval_wins": winners.count("retrieval"),
            "n_ties": winners.count("tie"),
            "r3_selected_mechanism_mode": max(set(r3_sels), key=r3_sels.count),
            "n_agree": sum(1 for a in agree_defined if a is True),
            "n_disagree": sum(1 for a in agree_defined if a is False),
            "n_na_llm_required": sum(1 for r in group if r["r3_selected_mechanism"] == "llm_required"),
        })
    with open(OUT / "final_summary.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader()
        w.writerows(summary_rows)

    run_meta = {
        "label": "FINAL -- Experiment 1 frozen run",
        "frozen_at_commit": "3c6b581178aa7cd3598e112f96f1321d61d60aa9",
        "total_conditions": len(manifest_rows),
        "successful_conditions": len(ok_results),
        "failed_conditions": len(failed_results),
        "failures": failed_results,
        "total_elapsed_seconds": round(total_elapsed, 2),
        "seconds_per_condition": round(total_elapsed / len(manifest_rows), 3),
    }
    (OUT / "final_run_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    print("\n" + "=" * 70)
    print(f"DONE. {len(ok_results)}/{len(manifest_rows)} conditions succeeded, "
          f"{len(failed_results)} failed, {total_elapsed:.1f}s total "
          f"({total_elapsed/len(manifest_rows):.3f}s/condition)")
    if failed_results:
        print("FAILURES:")
        for f in failed_results:
            print(f"  {f}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()

"""Phase D.1 post-hoc analysis of the FROZEN Experiment 1 final run.

Reads ONLY data/outputs/experiments/exp1/final/final_condition_results.csv
(240 rows, frozen at commit 6fb618838e47c84234dfad85c89b979e96b6c897).
Writes derived, clearly-separated analytical artifacts to
data/outputs/experiments/exp1/posthoc/ -- does not touch anything under
.../exp1/final/. No new data generation, no methodology change: this file
only aggregates/recombines columns that already exist in the frozen CSV.

Run: python scripts/experiments/exp1/analyze_posthoc.py
"""
import csv
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINAL_CSV = ROOT / "data" / "outputs" / "experiments" / "exp1" / "final" / "final_condition_results.csv"
OUT = ROOT / "data" / "outputs" / "experiments" / "exp1" / "posthoc"

R3_RULES_THRESHOLD = 0.90
R3_RETRIEVAL_THRESHOLD = 0.70


def load_rows():
    with open(FINAL_CSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["seed"] = int(r["seed"])
        r["target_deterministic_share"] = float(r["target_deterministic_share"])
        r["lexical_variation"] = r["lexical_variation"] == "True"
        r["p_transform"] = float(r["p_transform"])
        r["realized_det_pct"] = float(r["realized_det_pct"])
        r["weighted_ads"] = float(r["weighted_ads"])
        r["unweighted_ads"] = float(r["unweighted_ads"])
        r["cross_company_consistency"] = float(r["cross_company_consistency"])
        r["n_products_train"] = int(r["n_products_train"])
        r["n_train_lines"] = int(r["n_train_lines"])
        r["n_test_lines"] = int(r["n_test_lines"])
        r["rules_whole_set_accuracy"] = float(r["rules_whole_set_accuracy"])
        r["rules_coverage"] = float(r["rules_coverage"])
        r["retrieval_whole_set_accuracy"] = float(r["retrieval_whole_set_accuracy"])
        r["retrieval_coverage"] = float(r["retrieval_coverage"])
        r["retrieval_cutoff_used"] = int(r["retrieval_cutoff_used"])
        r["paired_diff_point"] = float(r["paired_diff_point"])
        r["paired_diff_ci_low"] = float(r["paired_diff_ci_low"])
        r["paired_diff_ci_high"] = float(r["paired_diff_ci_high"])
        r["r3_agrees_with_empirical"] = (
            None if r["r3_agrees_with_empirical"] == "" else r["r3_agrees_with_empirical"] == "True"
        )
        r["rules_minus_retrieval"] = r["rules_whole_set_accuracy"] - r["retrieval_whole_set_accuracy"]
    return rows


def ads_band(realized_det_pct):
    if realized_det_pct >= R3_RULES_THRESHOLD:
        return ">=0.90"
    if realized_det_pct >= R3_RETRIEVAL_THRESHOLD:
        return "0.70-0.90"
    return "<0.70"


def wilson_ci(k, n, z=1.959963984540054):
    if n == 0:
        return None, None
    p = k / n
    denom = 1 + z ** 2 / n
    center = p + z ** 2 / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))
    return (center - margin) / denom, (center + margin) / denom


def binom_two_sided_p(k, n, p0=0.5):
    """Exact two-sided binomial test p-value, stdlib only (math.comb)."""
    point_prob = lambda x: math.comb(n, x) * (p0 ** x) * ((1 - p0) ** (n - x))
    p_k = point_prob(k)
    total = 0.0
    for x in range(n + 1):
        px = point_prob(x)
        if px <= p_k * (1 + 1e-9):
            total += px
    return min(total, 1.0)


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def spearman_r(xs, ys):
    def rank(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        ranks = [0.0] * len(vals)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[order[k]] = avg_rank
            i = j + 1
        return ranks
    return pearson_r(rank(xs), rank(ys))


def describe(vals):
    if not vals:
        return {"n": 0, "mean": None, "median": None, "std": None, "min": None, "max": None}
    return {
        "n": len(vals),
        "mean": round(sum(vals) / len(vals), 4),
        "median": round(statistics.median(vals), 4),
        "std": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
        "min": round(min(vals), 4),
        "max": round(max(vals), 4),
    }


def group_perf(rows_subset):
    winners = [r["empirical_winner"] for r in rows_subset]
    return {
        "n_conditions": len(rows_subset),
        "rules_acc": describe([r["rules_whole_set_accuracy"] for r in rows_subset]),
        "retrieval_acc": describe([r["retrieval_whole_set_accuracy"] for r in rows_subset]),
        "rules_minus_retrieval": describe([r["rules_minus_retrieval"] for r in rows_subset]),
        "n_rules_wins": winners.count("rules"),
        "n_retrieval_wins": winners.count("retrieval"),
        "n_ties": winners.count("tie"),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    report = {}

    # ---- Step 2: headline reproduction ------------------------------------
    report["step2_completeness"] = {
        "total_rows": len(rows),
        "cells": sorted({(r["target_deterministic_share"], r["lexical_variation"]) for r in rows}),
        "n_per_cell": {
            f"{t}|{lex}": sum(1 for r in rows if r["target_deterministic_share"] == t and r["lexical_variation"] == lex)
            for t, lex in sorted({(r["target_deterministic_share"], r["lexical_variation"]) for r in rows})
        },
    }

    def agreement_block(subset):
        agree = sum(1 for r in subset if r["r3_agrees_with_empirical"] is True)
        disagree = sum(1 for r in subset if r["r3_agrees_with_empirical"] is False)
        na = sum(1 for r in subset if r["r3_selected_mechanism"] == "llm_required")
        tie = sum(1 for r in subset if r["r3_selected_mechanism"] != "llm_required" and r["empirical_winner"] == "tie")
        n_defined = agree + disagree
        assert agree + disagree + tie + na == len(subset), (agree, disagree, tie, na, len(subset))
        out = {
            "n_total": len(subset), "agree": agree, "disagree": disagree, "tie": tie,
            "na_llm_required": na, "n_defined": n_defined,
            "agreement_rate": round(agree / n_defined, 4) if n_defined else None,
        }
        if n_defined:
            lo, hi = wilson_ci(agree, n_defined)
            out["wilson_ci_95"] = [round(lo, 4), round(hi, 4)]
            out["binomial_p_vs_50pct"] = round(binom_two_sided_p(agree, n_defined), 6)
        return out

    report["step2_headline"] = {
        "overall": agreement_block(rows),
        "CLEAN": agreement_block([r for r in rows if not r["lexical_variation"]]),
        "VARIED": agreement_block([r for r in rows if r["lexical_variation"]]),
    }

    per_target_varied = {}
    for t in sorted({r["target_deterministic_share"] for r in rows}):
        subset = [r for r in rows if r["lexical_variation"] and r["target_deterministic_share"] == t]
        per_target_varied[t] = agreement_block(subset)
    report["step2_per_target_varied"] = per_target_varied

    band_varied = {}
    for band in ["<0.70", "0.70-0.90", ">=0.90"]:
        subset = [r for r in rows if r["lexical_variation"] and ads_band(r["realized_det_pct"]) == band]
        band_varied[band] = agreement_block(subset)
    report["step2_band_varied"] = band_varied

    # ---- Step 3: core performance view -------------------------------------
    perf = {}
    for band in ["<0.70", "0.70-0.90", ">=0.90"]:
        clean = [r for r in rows if not r["lexical_variation"] and ads_band(r["realized_det_pct"]) == band]
        varied = [r for r in rows if r["lexical_variation"] and ads_band(r["realized_det_pct"]) == band]
        varied_defined = [r for r in varied if r["empirical_winner"] != "tie"]
        perf[band] = {
            "CLEAN": group_perf(clean),
            "VARIED": group_perf(varied),
            "VARIED_with_defined_winner": group_perf(varied_defined),
            "POOLED": group_perf(clean + varied),
        }
    report["step3_perf_by_realized_ads_band"] = perf

    # by nominal target too (matches final_summary.csv, sanity cross-check)
    perf_by_target = {}
    for t in sorted({r["target_deterministic_share"] for r in rows}):
        clean = [r for r in rows if not r["lexical_variation"] and r["target_deterministic_share"] == t]
        varied = [r for r in rows if r["lexical_variation"] and r["target_deterministic_share"] == t]
        perf_by_target[t] = {"CLEAN": group_perf(clean), "VARIED": group_perf(varied)}
    report["step3_perf_by_target"] = perf_by_target

    # ---- Step 4: ADS x lexical interaction ---------------------------------
    clean_rows = [r for r in rows if not r["lexical_variation"]]
    varied_rows = [r for r in rows if r["lexical_variation"]]
    report["step4_interaction"] = {
        "pearson_r_realized_ads_vs_diff__CLEAN": round(pearson_r(
            [r["realized_det_pct"] for r in clean_rows], [r["rules_minus_retrieval"] for r in clean_rows]), 4),
        "pearson_r_realized_ads_vs_diff__VARIED": round(pearson_r(
            [r["realized_det_pct"] for r in varied_rows], [r["rules_minus_retrieval"] for r in varied_rows]), 4),
        "spearman_r_realized_ads_vs_diff__VARIED": round(spearman_r(
            [r["realized_det_pct"] for r in varied_rows], [r["rules_minus_retrieval"] for r in varied_rows]), 4),
        "mean_diff_by_target_and_lexical": {
            t: {
                "CLEAN": round(statistics.mean(r["rules_minus_retrieval"] for r in clean_rows
                                                if r["target_deterministic_share"] == t), 4),
                "VARIED": round(statistics.mean(r["rules_minus_retrieval"] for r in varied_rows
                                                 if r["target_deterministic_share"] == t), 4),
            }
            for t in sorted({r["target_deterministic_share"] for r in rows})
        },
    }

    # rules/retrieval CLEAN-minus-VARIED accuracy drop, by target (Step 5C/D)
    drop_by_target = {}
    for t in sorted({r["target_deterministic_share"] for r in rows}):
        c = [r for r in clean_rows if r["target_deterministic_share"] == t]
        v = [r for r in varied_rows if r["target_deterministic_share"] == t]
        drop_by_target[t] = {
            "rules_clean_mean": round(statistics.mean(r["rules_whole_set_accuracy"] for r in c), 4),
            "rules_varied_mean": round(statistics.mean(r["rules_whole_set_accuracy"] for r in v), 4),
            "rules_drop": round(statistics.mean(r["rules_whole_set_accuracy"] for r in c)
                                 - statistics.mean(r["rules_whole_set_accuracy"] for r in v), 4),
            "retrieval_clean_mean": round(statistics.mean(r["retrieval_whole_set_accuracy"] for r in c), 4),
            "retrieval_varied_mean": round(statistics.mean(r["retrieval_whole_set_accuracy"] for r in v), 4),
            "retrieval_drop": round(statistics.mean(r["retrieval_whole_set_accuracy"] for r in c)
                                     - statistics.mean(r["retrieval_whole_set_accuracy"] for r in v), 4),
        }
    report["step5_lexical_drop_by_target"] = drop_by_target

    # ---- Step 5G / Step 10: robustness -- who are the 2 agree seeds at target=1.00 VARIED?
    t1_varied = sorted(
        [r for r in rows if r["lexical_variation"] and r["target_deterministic_share"] == 1.00],
        key=lambda r: r["realized_det_pct"],
    )
    report["step5g_target1_varied_rows"] = [
        {
            "seed": r["seed"], "realized_det_pct": round(r["realized_det_pct"], 4),
            "band": ads_band(r["realized_det_pct"]), "r3_selected_mechanism": r["r3_selected_mechanism"],
            "empirical_winner": r["empirical_winner"], "agrees": r["r3_agrees_with_empirical"],
            "rules_acc": round(r["rules_whole_set_accuracy"], 4),
            "retrieval_acc": round(r["retrieval_whole_set_accuracy"], 4),
        }
        for r in t1_varied
    ]

    # target=0.50 VARIED -- the mixed llm_required/retrieval band
    t05_varied = sorted(
        [r for r in rows if r["lexical_variation"] and r["target_deterministic_share"] == 0.50],
        key=lambda r: r["realized_det_pct"],
    )
    report["step5g_target0_50_varied_rows"] = [
        {
            "seed": r["seed"], "realized_det_pct": round(r["realized_det_pct"], 4),
            "band": ads_band(r["realized_det_pct"]), "r3_selected_mechanism": r["r3_selected_mechanism"],
            "empirical_winner": r["empirical_winner"], "agrees": r["r3_agrees_with_empirical"],
        }
        for r in t05_varied
    ]

    # min/max realized ADS per target (band-crossing check, all targets)
    report["step10_realized_ads_range_by_target"] = {
        t: {
            "CLEAN": describe([r["realized_det_pct"] for r in clean_rows if r["target_deterministic_share"] == t]),
            "VARIED": describe([r["realized_det_pct"] for r in varied_rows if r["target_deterministic_share"] == t]),
        }
        for t in sorted({r["target_deterministic_share"] for r in rows})
    }

    # ---- Step 6: CLEAN diff detail (point diff vs delta=0.02) -------------
    report["step6_clean_diff_detail"] = {
        t: describe([r["rules_minus_retrieval"] for r in clean_rows if r["target_deterministic_share"] == t])
        for t in sorted({r["target_deterministic_share"] for r in rows})
    }
    report["step6_clean_paired_ci_width"] = {
        t: describe([r["paired_diff_ci_high"] - r["paired_diff_ci_low"]
                     for r in clean_rows if r["target_deterministic_share"] == t])
        for t in sorted({r["target_deterministic_share"] for r in rows})
    }

    # ---- Step 7: R3 vs actual best mechanism, by band, VARIED -------------
    r3_vs_actual = {}
    for band in ["<0.70", "0.70-0.90", ">=0.90"]:
        subset = [r for r in varied_rows if ads_band(r["realized_det_pct"]) == band]
        winners = [r["empirical_winner"] for r in subset]
        r3_sel = [r["r3_selected_mechanism"] for r in subset]
        actual_best = "retrieval" if winners.count("retrieval") == len(winners) else (
            "rules" if winners.count("rules") == len(winners) else "mixed")
        r3_mode = max(set(r3_sel), key=r3_sel.count) if r3_sel else None
        r3_vs_actual[band] = {
            "n": len(subset), "actual_best_mechanism": actual_best,
            "r3_choice_mode": r3_mode, "r3_choice_breakdown": {m: r3_sel.count(m) for m in set(r3_sel)},
        }
    report["step7_r3_vs_actual"] = r3_vs_actual

    # ---- Step 8: is empirical winner ever NOT constant within a lexical condition? ----
    report["step8_winner_constancy"] = {
        "CLEAN_winner_set": sorted({r["empirical_winner"] for r in clean_rows}),
        "VARIED_winner_set": sorted({r["empirical_winner"] for r in varied_rows}),
        "VARIED_retrieval_win_count": sum(1 for r in varied_rows if r["empirical_winner"] == "retrieval"),
        "VARIED_n": len(varied_rows),
        "CLEAN_tie_count": sum(1 for r in clean_rows if r["empirical_winner"] == "tie"),
        "CLEAN_n": len(clean_rows),
    }

    # ---- Step 9: simple associations ---------------------------------------
    all_x = [r["realized_det_pct"] for r in rows]
    report["step9_associations"] = {
        "pearson_ads_vs_rules_acc__pooled": round(pearson_r(all_x, [r["rules_whole_set_accuracy"] for r in rows]), 4),
        "pearson_ads_vs_retrieval_acc__pooled": round(pearson_r(all_x, [r["retrieval_whole_set_accuracy"] for r in rows]), 4),
        "pearson_ads_vs_rules_acc__CLEAN": round(pearson_r(
            [r["realized_det_pct"] for r in clean_rows], [r["rules_whole_set_accuracy"] for r in clean_rows]), 4),
        "pearson_ads_vs_rules_acc__VARIED": round(pearson_r(
            [r["realized_det_pct"] for r in varied_rows], [r["rules_whole_set_accuracy"] for r in varied_rows]), 4),
        "pearson_ads_vs_retrieval_acc__CLEAN": round(pearson_r(
            [r["realized_det_pct"] for r in clean_rows], [r["retrieval_whole_set_accuracy"] for r in clean_rows]), 4),
        "pearson_ads_vs_retrieval_acc__VARIED": round(pearson_r(
            [r["realized_det_pct"] for r in varied_rows], [r["retrieval_whole_set_accuracy"] for r in varied_rows]), 4),
        "pearson_lexical_dummy_vs_diff__pooled": round(pearson_r(
            [1.0 if r["lexical_variation"] else 0.0 for r in rows], [r["rules_minus_retrieval"] for r in rows]), 4),
    }

    with open(OUT / "posthoc_analysis_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)

    # flat CSV: per-row with derived band + lexical label, for spreadsheet/plot use
    with open(OUT / "posthoc_rows_with_bands.csv", "w", encoding="utf-8", newline="") as f:
        fieldnames = ["seed", "target_deterministic_share", "lexical_variation", "realized_det_pct",
                      "ads_band", "rules_whole_set_accuracy", "retrieval_whole_set_accuracy",
                      "rules_minus_retrieval", "empirical_winner", "r3_selected_mechanism",
                      "r3_agrees_with_empirical"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fieldnames[:4]} | {
                "ads_band": ads_band(r["realized_det_pct"]),
                "rules_whole_set_accuracy": r["rules_whole_set_accuracy"],
                "retrieval_whole_set_accuracy": r["retrieval_whole_set_accuracy"],
                "rules_minus_retrieval": round(r["rules_minus_retrieval"], 4),
                "empirical_winner": r["empirical_winner"],
                "r3_selected_mechanism": r["r3_selected_mechanism"],
                "r3_agrees_with_empirical": r["r3_agrees_with_empirical"],
            })

    print(json.dumps(report, indent=2, default=str))
    print(f"\nWROTE: {OUT / 'posthoc_analysis_report.json'}")
    print(f"WROTE: {OUT / 'posthoc_rows_with_bands.csv'}")


def demo():
    """ponytail: smallest runnable check -- confirms binomial/wilson helpers and
    the frozen 32/50 headline figure reproduce against the actual CSV."""
    rows = load_rows()
    assert len(rows) == 240
    agree = sum(1 for r in rows if r["r3_agrees_with_empirical"] is True)
    disagree = sum(1 for r in rows if r["r3_agrees_with_empirical"] is False)
    assert (agree, disagree) == (32, 18), (agree, disagree)
    lo, hi = wilson_ci(32, 50)
    assert round(lo, 3) == 0.501 and round(hi, 3) == 0.759, (lo, hi)
    p = binom_two_sided_p(32, 50)
    assert round(p, 3) == 0.065, p
    print("demo() OK: 32/50 agreement, Wilson CI, and binomial p all reproduce from the frozen CSV.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        main()

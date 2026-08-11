"""Self-checks for scripts/experiments/exp1/stats.py.

Run: python scripts/experiments/exp1/test_stats.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stats


def test_r3_rule_selection_matches_existing_constants():
    assert stats.r3_rule_selection(0.95) == "rules"
    assert stats.r3_rule_selection(0.90) == "rules"
    assert stats.r3_rule_selection(0.89) == "retrieval"
    assert stats.r3_rule_selection(0.70) == "retrieval"
    assert stats.r3_rule_selection(0.69) == "llm_required"


def test_whole_set_accuracy_penalizes_abstention():
    preds = [{"account_id": "371", "abstain": False},
             {"account_id": "", "abstain": True},
             {"account_id": "608", "abstain": False}]
    truths = ["371", "608", "608"]
    # line 1: correct; line 2: abstained -> incorrect even though truth is 608; line 3: correct
    assert stats.whole_set_accuracy(preds, truths) == 2 / 3


def test_bootstrap_ci_reasonable_on_constant_values():
    ci = stats.bootstrap_ci([0.8] * 50)
    assert abs(ci["mean"] - 0.8) < 1e-9
    assert ci["ci_low"] <= 0.8 <= ci["ci_high"]


def test_empirical_winner_tie_when_cis_overlap():
    rules_ci = {"ci_low": 0.70, "ci_high": 0.85}
    retrieval_ci = {"ci_low": 0.75, "ci_high": 0.90}
    assert stats.empirical_winner(0.78, 0.82, rules_ci, retrieval_ci) == "tie"


def test_empirical_winner_strict_when_cis_disjoint():
    rules_ci = {"ci_low": 0.90, "ci_high": 0.95}
    retrieval_ci = {"ci_low": 0.60, "ci_high": 0.70}
    assert stats.empirical_winner(0.92, 0.65, rules_ci, retrieval_ci) == "rules"


def test_selection_agreement_chance_baseline_is_half_not_third():
    results = [{"rule_selected": "rules", "empirical_winner": "rules"},
               {"rule_selected": "retrieval", "empirical_winner": "rules"}]
    agg = stats.selection_agreement(results)
    assert agg["chance_baseline"] == 0.5
    assert agg["agreement_rate"] == 0.5


def test_paired_bootstrap_winner_detects_clear_difference():
    rules = [1, 1, 1, 1, 1, 0, 0, 0, 1, 1] * 20      # 70% accuracy
    retrieval = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0] * 20  # 20% accuracy
    winner, ci = stats.paired_bootstrap_winner(rules, retrieval)
    assert winner == "rules"
    assert ci["diff_ci_low"] > stats.PRACTICAL_EQUIVALENCE_DELTA


def test_paired_bootstrap_winner_ties_within_practical_equivalence_margin():
    # accuracies differ by exactly 1 point out of 200 -- well inside delta=0.02
    rules = [1] * 101 + [0] * 99
    retrieval = [1] * 100 + [0] * 100
    winner, ci = stats.paired_bootstrap_winner(rules, retrieval)
    assert winner == "tie"


def test_paired_bootstrap_winner_identical_lists_is_always_tie():
    correct = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1] * 30
    winner, ci = stats.paired_bootstrap_winner(correct, correct)
    assert winner == "tie"
    assert ci["diff_point"] == 0.0


def test_paired_bootstrap_reproducible_given_same_seed():
    rules = [1, 0, 1, 1, 0] * 40
    retrieval = [0, 0, 1, 0, 0] * 40
    a = stats.paired_bootstrap_diff_ci(rules, retrieval, seed=5)
    b = stats.paired_bootstrap_diff_ci(rules, retrieval, seed=5)
    assert a == b


def test_selection_agreement_na_and_tie_not_silently_dropped():
    results = [
        {"rule_selected": "llm_required", "empirical_winner": "rules"},  # N/A
        {"rule_selected": "rules", "empirical_winner": "tie"},           # tie
        {"rule_selected": "rules", "empirical_winner": "rules"},         # agree
    ]
    agg = stats.selection_agreement(results)
    assert agg["na_llm_required"] == 1
    assert agg["tie"] == 1
    assert agg["agree"] == 1
    assert agg["n_total"] == 3
    assert agg["n_defined"] == 1  # only the strict agree/disagree row


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all stats self-checks passed")

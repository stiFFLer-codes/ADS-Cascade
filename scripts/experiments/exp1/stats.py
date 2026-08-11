"""stdlib-only bootstrap/agreement statistics for Experiment 1
(research/EXPERIMENT_1_REDESIGN_REVIEW.md §14-16). No numpy/scipy, matching
this repository's existing stdlib-only pipeline convention.
"""
import random

R3_RULES_THRESHOLD = 0.90       # existing scripts/04_architecture_decision.py constants,
R3_RETRIEVAL_THRESHOLD = 0.70   # reused unchanged, never re-derived here.


def bootstrap_ci(values, n_resamples=2000, alpha=0.05, seed=0):
    """Percentile-method bootstrap CI on the mean of `values`. Pure stdlib
    (random.choices), no numpy."""
    if not values:
        return None
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(n_resamples):
        sample = rng.choices(values, k=n)
        means.append(sum(sample) / n)
    means.sort()
    lo_idx = int((alpha / 2) * n_resamples)
    hi_idx = int((1 - alpha / 2) * n_resamples) - 1
    return {
        "mean": sum(values) / n,
        "ci_low": means[max(lo_idx, 0)],
        "ci_high": means[min(hi_idx, n_resamples - 1)],
        "n": n,
    }


def whole_set_accuracy(predictions, truths):
    """Abstentions count as incorrect -- the pre-specified primary performance
    criterion (§14). predictions/truths are parallel lists of
    (account_id, abstain) / account_id."""
    correct = sum(
        1 for pred, truth in zip(predictions, truths)
        if (not pred["abstain"]) and pred["account_id"] == truth
    )
    return correct / len(truths) if truths else 0.0


def coverage(predictions):
    if not predictions:
        return 0.0
    return sum(1 for p in predictions if not p["abstain"]) / len(predictions)


def r3_rule_selection(realized_det_pct):
    """The existing, unmodified R3 constants applied to the train-only
    realized_det_pct. Returns 'rules', 'retrieval', or 'llm_required'."""
    if realized_det_pct >= R3_RULES_THRESHOLD:
        return "rules"
    if realized_det_pct >= R3_RETRIEVAL_THRESHOLD:
        return "retrieval"
    return "llm_required"


def empirical_winner(rules_acc, retrieval_acc, rules_ci, retrieval_ci):
    """SUPERSEDED for the frozen final-run definition -- see
    paired_bootstrap_winner() below (research/EXPERIMENT_1_CALIBRATION_REPORT.md
    Gate 3). Independent-CI-overlap is the wrong test for a paired comparison
    (rules and retrieval are scored on the identical held-out test lines
    within a condition, so their outcomes are correlated, not independent) --
    kept only because the already-run, already-approved pilot
    (run_pilot.py / data/outputs/experiments/exp1/pilot/) used it and is not
    being re-executed this session. Do not use this for the final run."""
    if rules_ci and retrieval_ci:
        overlap = not (rules_ci["ci_high"] < retrieval_ci["ci_low"]
                        or retrieval_ci["ci_high"] < rules_ci["ci_low"])
        if overlap:
            return "tie"
    if rules_acc > retrieval_acc:
        return "rules"
    if retrieval_acc > rules_acc:
        return "retrieval"
    return "tie"


PRACTICAL_EQUIVALENCE_DELTA = 0.02  # whole-set-accuracy points; see Gate 3 justification


def paired_bootstrap_diff_ci(rules_correct, retrieval_correct, n_resamples=2000, alpha=0.05, seed=0):
    """The FROZEN winner-comparison statistic (Gate 3). Paired bootstrap CI on
    (rules_accuracy - retrieval_accuracy): each resample draws a set of
    TEST-LINE INDICES (with replacement) and scores BOTH mechanisms on that
    SAME resampled set, preserving the correlation between them -- they are
    evaluated on identical held-out lines within a condition, so treating
    their accuracies as two independent quantities (as the superseded
    empirical_winner()/CI-overlap approach did) ignores that correlation and
    is the wrong test for paired data."""
    n = len(rules_correct)
    if n == 0 or n != len(retrieval_correct):
        return None
    rng = random.Random(seed)
    diffs = []
    for _ in range(n_resamples):
        idx = [rng.randrange(n) for _ in range(n)]
        r_acc = sum(rules_correct[i] for i in idx) / n
        v_acc = sum(retrieval_correct[i] for i in idx) / n
        diffs.append(r_acc - v_acc)
    diffs.sort()
    lo_idx = max(int((alpha / 2) * n_resamples), 0)
    hi_idx = min(int((1 - alpha / 2) * n_resamples) - 1, n_resamples - 1)
    point = sum(rules_correct) / n - sum(retrieval_correct) / n
    return {
        "diff_point": point, "diff_ci_low": diffs[lo_idx], "diff_ci_high": diffs[hi_idx], "n": n,
    }


def paired_bootstrap_winner(rules_correct, retrieval_correct, delta=PRACTICAL_EQUIVALENCE_DELTA, **kwargs):
    """FROZEN empirical-winner rule for the final run. Rules wins iff the
    ENTIRE paired-difference CI lies above +delta; retrieval wins iff entirely
    below -delta; otherwise TIE -- a difference smaller than the pre-registered
    practical-equivalence margin cannot be ruled out, so it is not reported as
    a winner either way. delta is fixed BEFORE the experiment and is not
    re-tuned after seeing results."""
    ci = paired_bootstrap_diff_ci(rules_correct, retrieval_correct, **kwargs)
    if ci is None:
        return "tie", ci
    if ci["diff_ci_low"] > delta:
        return "rules", ci
    if ci["diff_ci_high"] < -delta:
        return "retrieval", ci
    return "tie", ci


def selection_agreement(condition_results):
    """condition_results: list of dicts with keys
    {'rule_selected': ..., 'empirical_winner': ...} (one per seed/band/lexical
    trial). Returns agreement rate over DEFINED comparisons only -- 'tie' and
    'llm_required' (rule selects the excluded mechanism) are reported
    separately, per §14, never silently dropped or forced into either bucket."""
    agree = disagree = tie = na = 0
    for r in condition_results:
        rule, winner = r["rule_selected"], r["empirical_winner"]
        if rule == "llm_required":
            na += 1
        elif winner == "tie":
            tie += 1
        elif rule == winner:
            agree += 1
        else:
            disagree += 1
    defined = agree + disagree
    return {
        "agreement_rate": (agree / defined) if defined else None,
        "agree": agree, "disagree": disagree, "tie": tie, "na_llm_required": na,
        "n_defined": defined, "n_total": len(condition_results),
        "chance_baseline": 0.5,
    }

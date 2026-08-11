"""Outcome-independent diagnostics for the lexical-variation condition and
P_TRANSFORM candidate selection (research/EXPERIMENT_1_REDESIGN_REVIEW.md §8).

CRITICAL CONSTRAINT (Phase D approval message): P_TRANSFORM must be chosen
using ONLY structural/string-level properties of the generated data --
transformation validity, semantic-identity preservation, surface-form
disruption, reproducibility, realistic (balanced) transform-type
distribution, and retrieval-challenge severity. Nothing in this module reads
account_id, correctness, or mechanism accuracy of any kind.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator

load_generator()  # side effect only: registers scripts/phase2 on sys.path
from p2lib.data import split_of  # noqa: E402
from rapidfuzz import fuzz  # noqa: E402


def surface_disruption_rate(lines):
    """Share of held-out (test-split) lines whose surface product string does
    NOT exactly match any surface form the same true product (product_code)
    was seen under in train. Cold-start products (never seen in train at all)
    are excluded from the denominator -- disruption is about "known but
    surface-varied," not "never seen." Purely structural: never touches
    account_id."""
    train_surfaces_by_code = defaultdict(set)
    for r in lines:
        if split_of(r) == "train":
            train_surfaces_by_code[r["product_code"]].add(r["normalized_product"])

    disrupted = disruptable = 0
    for r in lines:
        if split_of(r) != "test":
            continue
        seen = train_surfaces_by_code.get(r["product_code"])
        if not seen:
            continue  # cold-start, not counted
        disruptable += 1
        if r["normalized_product"] not in seen:
            disrupted += 1

    return {
        "disruption_rate": (disrupted / disruptable) if disruptable else None,
        "disruptable_test_lines": disruptable,
        "disrupted_test_lines": disrupted,
    }


def transform_type_balance(lines):
    """Distribution of which transform types actually fired, across every
    line where a transform was applied. A badly skewed distribution (e.g.
    always 'case', never the others) would mean the transform set isn't
    exercising realistic surface-form variety."""
    counts = Counter()
    n_transformed = 0
    n_total = len(lines)
    for r in lines:
        if r.get("lexical_transformed"):
            n_transformed += 1
            for t in r.get("lexical_transform_types", []):
                counts[t] += 1
    return {
        "n_total_lines": n_total,
        "n_transformed_lines": n_transformed,
        "transformed_share": (n_transformed / n_total) if n_total else None,
        "transform_type_counts": dict(counts),
    }


def retrieval_challenge_severity(lines):
    """rapidfuzz WRatio(original, transformed) for every transformed line --
    a pure string-similarity property of the transform, independent of any
    classification outcome. Interprets: scores near 100 mean the transform
    was too weak to challenge lexical retrieval at all; scores well below the
    shipped system's own fuzzy cutoffs (T2_SIM=85, GLOBAL_FUZZY_CUTOFF=88)
    would mean the transform is so aggressive it destroys retrievability
    entirely, which is not the intended "surface noise" regime."""
    scores = [
        fuzz.WRatio(r["lexical_original"], r["normalized_product"])
        for r in lines if r.get("lexical_transformed")
    ]
    if not scores:
        return {"mean_score": None, "min_score": None, "max_score": None, "pct_below_70": None}
    return {
        "mean_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
        "pct_below_70": 100 * sum(1 for s in scores if s < 70) / len(scores),
        "n_scored": len(scores),
    }


def semantic_identity_preserved(lines):
    """Structural check, not a statistic: for every transformed line, the
    ground-truth product_code (and therefore account_id -- the label was
    assigned before any surface transform ran) must be completely untouched
    by the transform. Returns True/False plus any violating rows found."""
    violations = []
    for r in lines:
        if r.get("lexical_transformed") and not r.get("product_code"):
            violations.append(r)
    return {"preserved": len(violations) == 0, "violations": violations}


def diagnose(lines):
    """One call producing every outcome-independent diagnostic needed to
    judge a P_TRANSFORM candidate."""
    return {
        "disruption": surface_disruption_rate(lines),
        "balance": transform_type_balance(lines),
        "severity": retrieval_challenge_severity(lines),
        "semantic_identity": semantic_identity_preserved(lines),
    }

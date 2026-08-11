"""Isolated mechanism interfaces for Experiment 1.

research/EXPERIMENT_1_REDESIGN_REVIEW.md §11: the cascade's fused,
interleaved fallback logic (scripts/phase2/p2lib/cascade.py) must NOT be
involved in H1 evaluation -- that measures "does our cascade perform well"
(H2, out of scope), not "which mechanism performs best." These two functions
each run ONE mechanism to its own conclusion, built on the existing
kb.py/retrieval.py primitives (no duplicated matching logic).

LLM mechanism is deliberately not implemented here -- excluded from the
primary H1 comparison per the approved redesign (§10): the synthetic product
string carries no signal predictive of the true label, so a from-scratch LLM
classification task on this generator's data is not a scientifically valid
test.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator

load_generator()  # side effect only: registers scripts/phase2 on sys.path
from p2lib.retrieval import fuzzy_company, fuzzy_global  # noqa: E402


def classify_rules(kb, cui, product, direction):
    """Rules-first / exact-lookup mechanism, in isolation: company-scoped
    exact match, then global exact match. Any hit is accepted -- no
    ADS/evidence gating (that is cascade *policy*, not this mechanism's raw
    discriminative capability). No hit -> abstain. No confidence threshold
    exists or needs calibrating for this mechanism (binary match/no-match)."""
    cr = kb.company_lookup(cui, product, direction)
    if cr:
        return {"account_id": cr["account"], "abstain": False, "method": "COMPANY_EXACT"}
    gr = kb.global_lookup(product, direction)
    if gr:
        return {"account_id": gr["account"], "abstain": False, "method": "GLOBAL_EXACT"}
    return {"account_id": "", "abstain": True, "method": "NO_MATCH"}


def classify_retrieval(kb, cui, product, direction, cutoff):
    """Retrieval-primary / similarity-based-retrieval mechanism (rapidfuzz
    lexical similarity -- explicitly NOT semantic embeddings, see §9 of the
    redesign review), used as the PRIMARY classifier, not a rules-miss
    fallback: it is given every test item directly, regardless of whether an
    exact match would also have succeeded. `cutoff` is the one calibrated
    threshold this mechanism needs (§12 of the review)."""
    matches = fuzzy_company(kb, cui, product, cutoff=cutoff)
    if matches:
        best_product, score, _ = matches[0]
        match = kb.company_lookup(cui, best_product, direction)
        if match:
            return {"account_id": match["account"], "abstain": False,
                    "method": "FUZZY_COMPANY", "score": score}

    pool = list(kb.glob.keys())
    global_matches = fuzzy_global(product, pool, cutoff=cutoff)
    if global_matches:
        best_product, score, _ = global_matches[0]
        match = kb.global_lookup(best_product, direction)
        if match:
            return {"account_id": match["account"], "abstain": False,
                    "method": "FUZZY_GLOBAL", "score": score}

    return {"account_id": "", "abstain": True, "method": "NO_MATCH"}

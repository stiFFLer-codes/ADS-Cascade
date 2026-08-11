"""
Mechanism-isolation sanity checks (research/EXPERIMENT_1_REDESIGN_REVIEW.md
§11, §17 pilot criterion 7). Confirms classify_rules/classify_retrieval are
genuinely decoupled from each other and from the shipped cascade's tiering
policy -- not a rename of the same code path.

Run: python scripts/experiments/exp1/test_mechanisms.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator
from mechanisms import classify_rules, classify_retrieval

load_generator()  # side effect only: registers scripts/phase2 on sys.path
from p2lib import kb as kbmod  # noqa: E402


def _kb(rows):
    kb = kbmod.KB()
    for cui, product, direction, account, tax, vat in rows:
        kb.add(cui, "CoName", product, direction, account, tax, vat)
    return kb


def test_rules_exact_hit():
    kb = _kb([("C1", "rovinieta", "PURCHASE", "635", "", "21.00")] * 5)
    r = classify_rules(kb, "C1", "rovinieta", "PURCHASE")
    assert r == {"account_id": "635", "abstain": False, "method": "COMPANY_EXACT"}


def test_rules_abstains_on_typo_no_fuzzy_fallback():
    """Rules-first has NO fuzzy fallback of its own -- a near-miss must abstain,
    not silently degrade into retrieval behavior."""
    kb = _kb([("C1", "servicii contabilitate", "PURCHASE", "628", "", "21.00")] * 9)
    r = classify_rules(kb, "C1", "servici contabilitat", "PURCHASE")  # typo'd
    assert r["abstain"] is True and r["account_id"] == ""


def test_retrieval_recovers_typo_that_rules_misses():
    """The whole point of an isolated retrieval-primary mechanism: it must
    succeed on a near-miss that classify_rules abstains on."""
    kb = _kb([("C1", "servicii contabilitate", "PURCHASE", "628", "", "21.00")] * 9)
    rules_result = classify_rules(kb, "C1", "servici contabilitat", "PURCHASE")
    retrieval_result = classify_retrieval(kb, "C1", "servici contabilitat", "PURCHASE", cutoff=70)
    assert rules_result["abstain"] is True
    assert retrieval_result["abstain"] is False
    assert retrieval_result["account_id"] == "628"


def test_retrieval_used_as_primary_not_gated_behind_a_rules_miss():
    """retrieval_only must be callable directly on an item that ALSO has an
    exact match, without going through classify_rules first -- confirms it's
    not secretly implemented as "call rules, fall back to fuzzy"."""
    kb = _kb([("C1", "rovinieta", "PURCHASE", "635", "", "21.00")] * 5)
    r = classify_retrieval(kb, "C1", "rovinieta", "PURCHASE", cutoff=70)
    assert r["abstain"] is False and r["account_id"] == "635"


def test_mechanisms_diverge_on_a_fuzzy_slice():
    """Pilot acceptance criterion 7 as a standing regression check: rules and
    retrieval must produce DIFFERENT predictions on at least some inputs, or
    isolation has collapsed into one mechanism."""
    kb = _kb([("C1", "servicii contabilitate", "PURCHASE", "628", "", "21.00")] * 9)
    r1 = classify_rules(kb, "C1", "servici contabilitat", "PURCHASE")
    r2 = classify_retrieval(kb, "C1", "servici contabilitat", "PURCHASE", cutoff=70)
    assert r1["account_id"] != r2["account_id"] or r1["abstain"] != r2["abstain"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all mechanism-isolation self-checks passed")

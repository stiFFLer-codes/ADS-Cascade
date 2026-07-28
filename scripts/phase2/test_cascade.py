"""Fast synthetic self-check for the cascade (no data file needed).

Run: python scripts/phase2/test_cascade.py
The real evidence is p2_02's 63k-line eval; this just pins the tier logic so a threshold
edit can't silently break routing.
"""
from p2lib import cascade
from p2lib import kb as kbmod


def _kb(rows):
    kb = kbmod.KB()
    for cui, prod, direction, acct, tax, vat in rows:
        kb.add(cui, "CoName", prod, direction, acct, tax, vat)
    return kb


def test_deterministic_is_tier1():
    # same product -> same account, 5x  => ads 1.0, ev 5 => Tier 1 auto-apply
    kb = _kb([("C1", "rovinieta", "PURCHASE", "635", "301104", "21.00")] * 5)
    r = cascade.classify(kb, "C1", "rovinieta", "PURCHASE")
    assert r["tier"] == 1 and r["account_id"] == "635", r


def test_ambiguous_low_evidence_goes_to_review():
    # 2x -> 628, 1x -> 635  => ads ~0.67, ev 3 => not auto-apply => review
    kb = _kb([("C1", "avans", "PURCHASE", "628", "", "21.00")] * 2
             + [("C1", "avans", "PURCHASE", "635", "", "21.00")])
    r = cascade.classify(kb, "C1", "avans", "PURCHASE")
    assert r["tier"] in (3, 4), r


def test_unseen_product_is_tier4():
    kb = _kb([("C1", "rovinieta", "PURCHASE", "635", "301104", "21.00")] * 5)
    r = cascade.classify(kb, "C1", "something totally new xyz", "PURCHASE")
    assert r["tier"] == 4 and r["account_id"] == "", r


def test_fuzzy_never_auto_applies():
    # near-duplicate product name resolves via fuzzy -> must be review, not auto
    kb = _kb([("C1", "servicii contabilitate", "PURCHASE", "628", "", "21.00")] * 9)
    r = cascade.classify(kb, "C1", "servici contabilitat", "PURCHASE")  # typo'd
    assert r["tier"] >= 3, r


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all cascade self-checks passed")

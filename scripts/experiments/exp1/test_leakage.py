"""
MANDATORY leakage test (research/EXPERIMENT_1_REDESIGN_REVIEW.md §13, and the
explicit "MANDATORY LEAKAGE TEST" requirement in the Phase D approval message).

Proves: realized_ads(train_only) does NOT change when test-split labels
change. Same training data + different test labels => identical design-time
ADS. This is the structural guarantee that the "design-time" consistency
signal can never see the held-out labels it is later judged against.

Run: python scripts/experiments/exp1/test_leakage.py
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator
from consistency import realized_ads

gen = load_generator()
from p2lib.data import split_of  # noqa: E402  (registered on sys.path by load_generator())


def test_realized_ads_unaffected_by_test_label_mutation():
    _, lines = gen.gen_dataset(seed=11, deterministic_share=0.80)
    assert len(lines) > 50, "need enough lines for a real train/test split to exist"

    before = realized_ads(lines)

    mutated = copy.deepcopy(lines)
    n_mutated = 0
    for row in mutated:
        if split_of(row) == "test":
            # deliberately wrong but schema-valid account, distinct from the original
            row["account_id"] = "999999"
            n_mutated += 1
    assert n_mutated > 0, "no test rows found -- split_of()/test data assumption broken"

    after = realized_ads(mutated)

    assert before == after, (
        f"realized_ads() changed after mutating ONLY test-split labels -- leakage.\n"
        f"before={before}\nafter={after}"
    )


def test_realized_ads_full_dataset_diagnostic_DOES_change_with_test_mutation():
    """Sanity converse: the explicitly-non-primary full-dataset diagnostic (§3)
    SHOULD move when test labels change -- confirming the train-only guarantee
    above is actually doing real filtering, not accidentally always returning
    a constant."""
    from consistency import realized_ads_full_dataset_diagnostic_only

    _, lines = gen.gen_dataset(seed=11, deterministic_share=0.80)
    before = realized_ads_full_dataset_diagnostic_only(lines)

    mutated = copy.deepcopy(lines)
    for row in mutated:
        if split_of(row) == "test":
            row["account_id"] = "999999"

    after = realized_ads_full_dataset_diagnostic_only(mutated)
    assert before != after, (
        "full-dataset diagnostic did not change after mutating test labels -- "
        "this would mean the leakage test above is vacuous, not passing for the right reason"
    )


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all leakage self-checks passed")

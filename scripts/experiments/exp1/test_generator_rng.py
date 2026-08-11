"""
RNG-independence tests for the parameterized generator (Experiment 1 harness
requirement -- research/EXPERIMENT_1_REDESIGN_REVIEW.md §5, §17).

A multi-seed sweep is only valid if:
  1. the same seed always reproduces the identical dataset,
  2. different seeds produce genuinely different datasets, and
  3. the order in which seeds are called doesn't change any seed's output
     (proves no shared mutable global RNG state leaks between calls).

Run: python scripts/experiments/exp1/test_generator_rng.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator

gen = load_generator()


def test_same_seed_is_identical():
    _, lines_a = gen.gen_dataset(seed=7, deterministic_share=0.80)
    _, lines_b = gen.gen_dataset(seed=7, deterministic_share=0.80)
    assert lines_a == lines_b


def test_different_seeds_are_independent():
    _, lines_a = gen.gen_dataset(seed=7, deterministic_share=0.80)
    _, lines_b = gen.gen_dataset(seed=8, deterministic_share=0.80)
    assert lines_a != lines_b


def test_execution_order_does_not_affect_results():
    _, first_call_seed1 = gen.gen_dataset(seed=1, deterministic_share=0.80)
    _, _unused_seed2 = gen.gen_dataset(seed=2, deterministic_share=0.80)
    _, second_call_seed1 = gen.gen_dataset(seed=1, deterministic_share=0.80)
    assert first_call_seed1 == second_call_seed1, (
        "seed=1's output changed after generating seed=2 in between -- "
        "the generator is leaking shared mutable RNG state between calls"
    )


def test_lexical_variation_seed_independence_holds_too():
    _, lines_a = gen.gen_dataset(seed=3, deterministic_share=0.80,
                                  lexical_variation=True, p_transform=0.5)
    _, lines_b = gen.gen_dataset(seed=3, deterministic_share=0.80,
                                  lexical_variation=True, p_transform=0.5)
    assert lines_a == lines_b


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all generator RNG self-checks passed")

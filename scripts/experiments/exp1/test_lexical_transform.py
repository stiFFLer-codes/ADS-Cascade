"""
Lexical-transform correctness tests (research/EXPERIMENT_1_REDESIGN_REVIEW.md
§8, §17). Confirms: semantic identity is preserved (ground truth never
touched), transforms are reproducible per (seed, line), and the OFF condition
truly applies zero transforms.

Run: python scripts/experiments/exp1/test_lexical_transform.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _loader import load_generator
from lexical_diagnostics import diagnose, semantic_identity_preserved

gen = load_generator()


def test_reproducible_given_same_seed_and_line():
    a = gen.lexical_variant("SYNTH FUEL 00073", seed=42, logical_key="9900001_31-03-2025", line_number=1, p_transform=0.7)
    b = gen.lexical_variant("SYNTH FUEL 00073", seed=42, logical_key="9900001_31-03-2025", line_number=1, p_transform=0.7)
    assert a == b


def test_different_line_number_can_differ():
    a = gen.lexical_variant("SYNTH FUEL 00073", seed=42, logical_key="9900001_31-03-2025", line_number=1, p_transform=1.0)
    b = gen.lexical_variant("SYNTH FUEL 00073", seed=42, logical_key="9900001_31-03-2025", line_number=2, p_transform=1.0)
    # not asserting inequality (could coincidentally match) -- asserting independence:
    # both must be individually reproducible, which test_reproducible_given_same_seed_and_line
    # already covers; here we only assert both ran without depending on call order.
    assert a[1] is True and b[1] is True  # p_transform=1.0 -> always transforms


def test_p_transform_zero_never_transforms():
    surface, was_transformed, types = gen.lexical_variant(
        "SYNTH FUEL 00073", seed=1, logical_key="k", line_number=1, p_transform=0.0)
    assert was_transformed is False
    assert surface == "SYNTH FUEL 00073"
    assert types == []


def test_p_transform_one_always_transforms_and_types_nonempty():
    surface, was_transformed, types = gen.lexical_variant(
        "SYNTH FUEL 00073", seed=1, logical_key="k", line_number=1, p_transform=1.0)
    assert was_transformed is True
    assert len(types) >= 1


def test_default_generation_applies_zero_transforms_end_to_end():
    _, lines = gen.gen_dataset(seed=5, deterministic_share=0.80, lexical_variation=False)
    assert not any(r.get("lexical_transformed") for r in lines)


def test_lexical_variation_on_produces_a_mix_of_transformed_and_clean_lines():
    _, lines = gen.gen_dataset(seed=5, deterministic_share=0.80,
                                lexical_variation=True, p_transform=0.5)
    transformed = sum(1 for r in lines if r.get("lexical_transformed"))
    clean = len(lines) - transformed
    assert transformed > 0 and clean > 0, (
        f"expected a genuine mix at p_transform=0.5, got transformed={transformed} clean={clean}"
    )


def test_semantic_identity_preserved_structurally():
    _, lines = gen.gen_dataset(seed=5, deterministic_share=0.80,
                                lexical_variation=True, p_transform=0.7)
    result = semantic_identity_preserved(lines)
    assert result["preserved"] is True, result["violations"][:3]


def test_diagnose_runs_end_to_end():
    _, lines = gen.gen_dataset(seed=5, deterministic_share=0.80,
                                lexical_variation=True, p_transform=0.5)
    result = diagnose(lines)
    assert result["disruption"]["disruption_rate"] is not None
    assert result["severity"]["mean_score"] is not None
    assert result["semantic_identity"]["preserved"] is True


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all lexical-transform self-checks passed")

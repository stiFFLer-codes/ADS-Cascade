"""
Regression test for the Experiment 1 generator refactor (RNG fix +
parameterization + lexical variation, research/EXPERIMENT_1_REDESIGN_REVIEW.md).

Proves the refactor did not change the generator's default behavior: calling
gen_dataset() with today's defaults (seed=42, deterministic_share=0.95,
lexical_variation=False) must reproduce the currently-committed
data/outputs/invoice_lines_all_companies.csv exactly, row for row, field for
field -- the same guarantee the old module-level `random.seed(42)` gave, now
from an explicit, independently-seeded random.Random(42) instead of mutated
global state.

Run: python scripts/test_00_generate_synthetic.py
"""
import csv
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "gen_synthetic", ROOT / "scripts" / "00_generate_synthetic.py"
)
gen_synthetic = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen_synthetic)

COMMITTED_LINES = ROOT / "data" / "outputs" / "invoice_lines_all_companies.csv"


def test_default_output_matches_committed_csv():
    """Round-trip through the real CSV writer (not a raw in-memory dict compare --
    the generator legitimately returns line_number as an int; the writer/committed
    file both stringify it, so the writer is the correct place to normalize types)."""
    with open(COMMITTED_LINES, encoding="utf-8-sig", newline="") as f:
        committed = list(csv.DictReader(f))

    _, lines = gen_synthetic.gen_dataset()  # all defaults: seed=42, det_share=0.95, no lexical variation

    with tempfile.TemporaryDirectory() as tmp:
        orig_out = gen_synthetic.OUT
        try:
            gen_synthetic.OUT = Path(tmp)
            path = gen_synthetic.write_invoice_lines(lines)
            with open(path, encoding="utf-8-sig", newline="") as f:
                generated = list(csv.DictReader(f))
        finally:
            gen_synthetic.OUT = orig_out

    assert len(generated) == len(committed), (len(generated), len(committed))
    for i, (g, expected) in enumerate(zip(generated, committed)):
        assert g == expected, f"row {i} differs:\n  generated={g}\n  committed={expected}"


def test_lexical_variation_off_adds_no_extra_fields():
    _, lines = gen_synthetic.gen_dataset(seed=1, lexical_variation=False)
    assert lines, "expected at least one line"
    for extra in ("lexical_original", "lexical_transformed", "lexical_transform_types"):
        assert extra not in lines[0], f"{extra} must not appear when lexical_variation=False"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("all 00_generate_synthetic self-checks passed")

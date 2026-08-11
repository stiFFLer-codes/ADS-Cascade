"""Shared import plumbing for Experiment 1 modules.

00_generate_synthetic.py's filename isn't a valid Python identifier, so it's
loaded via importlib (same pattern as scripts/test_dataset_intelligence.py).
p2lib (scripts/phase2/p2lib) is imported by adding scripts/phase2 to sys.path
(same pattern p2_02_classify_eval.py etc. rely on when run from repo root).
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # exp1 -> experiments -> scripts -> ROOT

if str(ROOT / "scripts" / "phase2") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts" / "phase2"))


def load_generator():
    spec = importlib.util.spec_from_file_location(
        "gen_synthetic", ROOT / "scripts" / "00_generate_synthetic.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# E5.3 — Reproducibility Packaging Correction Pass

> Packaging/documentation only. No scientific content, frozen evidence, manuscript, or contract/lock
> document touched. Not yet committed — this is the pre-commit evidence trail for that decision.

---

## 1. Original E5.3 findings

`research/E5_3_REPRODUCIBILITY_AUDIT.md` (primary pass) and
`research/E5_3_INDEPENDENT_REPRODUCIBILITY_AUDIT.md` (independent `research-code-auditor` pass, both
verdict 🟠 ORANGE/CONDITIONAL) converged on the same root causes: (1) `README.md`/`docs/INDEX.md` never
mention `manuscript/`, `scripts/experiments/exp1/`, or Experiment 1 at all; (2) the independent pass
additionally found README's own "Folder map" *asserts* `requirements.txt` contains `rapidfuzz`,
`boto3`, `pypdf` when the actual file has only `pandas`, `requests`, `tqdm`; (3) `rapidfuzz` — the one
genuine dependency of the documented reproduction command — is absent from `requirements.txt`, so a
clean `pip install -r requirements.txt` does not suffice to run `run_final.py`; (4) a MEDIUM finding
that the exact realized-ADS-band framing behind the manuscript's headline numbers seemed to live only
in unlinked internal `research/*.md` documents.

## 2. Exact corrections

**`requirements.txt`** (+8 lines, 0 deleted): added `rapidfuzz`, **unpinned** — the frozen run's own
`final_run_metadata.json` never recorded which version produced it, so none is asserted (no invented
constraint). Added a commented-out `matplotlib` entry (matching the file's existing pattern for
not-yet-required deps like `lxml`/`openpyxl`) for figure generation, since figures are explicitly
deferred to E5.4 and not required to reproduce Experiment 1's actual results.

**`README.md`** (+35/-3 lines): (a) corrected the Folder map's `requirements.txt` line to list the
file's real contents (`pandas, requests, tqdm, rapidfuzz`) instead of the false `rapidfuzz, requests,
boto3, pypdf`; (b) added a new "Experiment 1 (arXiv-track manuscript)" section — a table pointing to
the final execution script, frozen config, seed manifest, frozen raw results, the headline-statistics
regeneration script, figure generation, and the manuscript source, plus the Python-version and
dependency notes; (c) added Folder-map rows for `manuscript/`, `research/`, and updated the `scripts/`
and `data/` rows to mention `experiments/exp1/`; (d) added one line to "Start here" pointing to the
new section.

**`docs/INDEX.md`** (+2 lines): one new bullet pointing to README's new Experiment 1 section — not a
duplicate of its content.

**No other file touched.** `scripts/experiments/exp1/_loader.py` was investigated (item 5 of the
approved scope) and found to already have an adequate, self-contained docstring explaining its
importlib shim — determined no edit was needed (see §7).

## 3. Dependency verification

Grepped every `.py` file under `scripts/experiments/exp1/` for `^import |^from ` (all 15 modules,
including `run_final.py`, `mechanisms.py`, `consistency.py`, `stats.py`, `analyze_posthoc.py`,
`calibrate_ads.py`, `calibrate_retrieval_cutoff.py`, `run_pilot.py`, `lexical_diagnostics.py`,
`select_p_transform.py`, `_loader.py`, and all four `test_*.py` files) plus the two `p2lib` modules
`run_final.py` directly imports (`kb.py`, `data.py`) and the synthetic generator
(`00_generate_synthetic.py`). **Result: the only non-stdlib import anywhere in the Experiment 1 path
is `rapidfuzz`** (via `mechanisms.py` and `lexical_diagnostics.py`, both through
`p2lib/retrieval.py:8`). `stats.py` and `consistency.py` deliberately use no numpy/scipy (confirmed:
`stats.py`'s only import is `random`). `boto3` is used exclusively by `scripts/phase2/p2_03_extract.py`
(AWS Textract OCR, a Phase 2 feature, not on the Experiment 1 path). `pypdf` is used **nowhere in the
codebase** — grepped case-insensitively across every `.py` file; zero hits. README's former claim
about both packages was unsubstantiated by actual code, confirming the independent auditor's finding.
**Per the approved scope's explicit instruction, neither was added** — only `rapidfuzz` was, because
only `rapidfuzz` is genuinely required by the Experiment 1 execution path.

**Empirically verified the fix, not just asserted it**: created an isolated virtual environment
(scratchpad-only, outside the repo), installed only `rapidfuzz` into it (the exact new
`requirements.txt` line), and successfully imported the full `run_final.py` dependency chain
(`_loader`, `mechanisms`, `consistency`, `stats`) with zero errors:
```
OK: exp1 import chain resolves cleanly with rapidfuzz installed (the fix requirements.txt now declares)
```
This directly proves the documented reproduction command's import chain now resolves from a clean
environment following only the corrected `requirements.txt`.

## 4. README discoverability verification

Read the final `README.md` end to end as a fresh reader would. Confirmed the new "Experiment 1"
section answers, without inference: what Experiment 1 is (one sentence, distinguished from the
Phase 1/2 pipeline above it); where the final script is; where the frozen config, seed manifest, and
frozen results live; how headline statistics regenerate; where figure generation and the manuscript
source live. "Start here" item 5 and the Folder map's `manuscript/`/`research/`/`scripts/` rows give a
second, independent path to the same section. Kept to one table and eight lines of prose — not a
research diary, no internal Phase-lettering or audit jargon imported from `research/`.

## 5. docs/INDEX.md verification

One new bullet, no duplicated content — points back to `README.md`'s section rather than restating it,
consistent with `docs/INDEX.md`'s own stated principle ("nothing is copied here, so nothing drifts").

## 6. Python-version determination

Searched the entire repository for any version pin (`python_requires`, `.python-version`,
`pyproject.toml`, `setup.py`, CI config, shebang version checks) — none found anywhere **except**
`prerun_check.py:44`, which hard-codes `check_python(min_major=3, min_minor=11)` as the minimum for
the Phase 1 pipeline's own pre-flight checks. This is the **only** Python-version floor established
anywhere in this codebase by actual code (not by claim or convention). No separate check exists for
Experiment 1 specifically, and no evidence was found that Experiment 1 requires anything different, so
**this floor was documented in README's new section, attributed honestly to `prerun_check.py`** rather
than presented as if independently verified for Experiment 1. No version was guessed or invented.

## 7. Loader documentation determination

Read `scripts/experiments/exp1/_loader.py` in full (12 lines). Its docstring already states plainly:
*"00_generate_synthetic.py's filename isn't a valid Python identifier, so it's loaded via importlib
(same pattern as scripts/test_dataset_intelligence.py). p2lib (scripts/phase2/p2lib) is imported by
adding scripts/phase2 to sys.path (same pattern p2_02_classify_eval.py etc. rely on when run from
repo root)."* This fully answers "why does this file exist and what does it do" for a reader who has
found the file — the E5.3 audit's own walkthrough (§2, Q5) already concluded this file is
"well-commented." **Determination: no edit needed.** The gap E5.3 actually found was discoverability of
`scripts/experiments/exp1/` as a directory, not clarity of `_loader.py` once found — addressed in §2/§4
above instead.

## 8. Realized-ADS regeneration-path determination

**This finding is resolved, not gapped — no new code was needed.** Read
`scripts/experiments/exp1/analyze_posthoc.py` in full: it is stdlib-only (`csv`, `json`, `math`,
`statistics`), reads exclusively the frozen public `final_condition_results.csv`, and independently
implements `wilson_ci()` and `binom_two_sided_p()` (exact binomial test via `math.comb`) — no
additional dependency beyond what's already in the corrected `requirements.txt` (in fact, none at
all beyond stdlib). Its `main()` computes exactly the quantities in question: `step2_headline`
(the 32/50 aggregate), `step2_band_varied` (the 32/32 and 0/18 realized-ADS-band split),
`step2_per_target_varied` (the by-nominal-target framing, from which 30/30 at targets 0.50+0.75 and
2/20 at target 1.00 are directly readable). It also ships a `demo()` self-check that **hardcodes and
asserts the exact headline figures**: `(agree, disagree) == (32, 18)`, Wilson CI rounding to
`(0.501, 0.759)`, binomial p rounding to `0.065`.

**Ran the existing `--demo` mode this pass** (read-only: reads the frozen CSV, writes nothing, no
side effects) to confirm empirically, not just by code inspection:
```
$ python scripts/experiments/exp1/analyze_posthoc.py --demo
demo() OK: 32/50 agreement, Wilson CI, and binomial p all reproduce from the frozen CSV.
```
This confirms the manuscript's headline numbers **do** regenerate from an existing, already-public,
already-runnable, stdlib-only script — the E5.3 MEDIUM finding overstated the gap; the actual gap was
that this script wasn't *linked* from anywhere public-facing, which is now fixed (§2, README's new
table lists it explicitly). Per the approved scope's explicit instruction, **no new analysis script
was written**, since the existing one already provides this capability.

## 9. Protected/frozen-file verification

```
git diff --quiet -- manuscript/main.tex manuscript/references.bib research/PAPER_CONTRACT.md \
  research/CONTRIBUTION_LOCK.md research/contribution_lock.csv \
  data/outputs/experiments/exp1/final/ scripts/experiments/exp1/
→ exit 0 (clean)

git diff --quiet 6fb6188 -- data/outputs/experiments/exp1/final/  → exit 0 (byte-identical to freeze)
git diff --quiet 7fd1d9a -- manuscript/                            → exit 0 (byte-identical to E5.2 HEAD)
```
`git status --porcelain` confirms only `README.md`, `docs/INDEX.md`, and `requirements.txt` are
modified; no Experiment 1 source file, frozen artifact, manuscript file, or lock/contract document
entered the working tree as changed.

## 10. Test results

`python -m pytest scripts/experiments/exp1/ -q` → **30 passed** (unchanged — no code was touched).
Isolated-venv import-chain check (§3): **passed**, empirically, not just by static inspection.

## 11. Independent auditor verdict

🟢 **PASS** (`research/E5_3_CORRECTION_INDEPENDENT_AUDIT.md`). The auditor approached this exactly as
instructed — "a researcher who has just cloned this repository and has never seen the project before"
— and independently: hand-traced the full import chain from primary source; built its *own* separate
isolated venv (deliberately not reusing this pass's, since `rapidfuzz` was already present in the
ambient environment and could have masked a missing-dependency bug) and confirmed the chain resolves
with only `rapidfuzz` installed; confirmed `boto3`/`pypdf` are genuinely not needed (same conclusion,
independently reached); verified all 8 paths in README's new table exist on disk; confirmed the
Python 3.11+ claim against `prerun_check.py` directly (4 call sites); independently re-ran
`analyze_posthoc.py --demo` and got the same passing result; confirmed the scope boundary holds
(exactly 3 tracked files changed, everything else byte-identical to HEAD); reconfirmed 30/30 tests;
found no secrets. No disagreement with this report on any point.

## 12. Remaining non-blocking issues

- The two other E5.3 LOW findings (no Python-version check specific to Experiment 1 itself, beyond
  the repo-wide floor now documented; the by-nominal-target 30/30 figure requires summing two of
  `analyze_posthoc.py`'s `step2_per_target_varied` entries rather than being pre-aggregated into a
  single reported number) are unchanged — neither was in the approved scope's required-fix list, and
  neither blocks reproduction.
- `boto3` (used by Phase 2's `p2_03_extract.py`, unrelated to Experiment 1) remains undeclared in
  `requirements.txt` — out of scope for this pass (Experiment 1 path only), noted for a future,
  separately-scoped Phase 2 packaging pass if ever needed.

## 13. Exact proposed staging list (not yet staged)

```
README.md
docs/INDEX.md
requirements.txt
research/E5_3_CORRECTION_AUDIT.md
```

Untracked, not part of this proposed staging list (pre-existing or this session's earlier audit trail,
unrelated to this specific correction):
```
research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md
research/E4_CHECKPOINT_MANIFEST_VERIFICATION.md
research/E5_1_E5_2_GPS_CLOSEOUT_AUDIT.md
research/E5_1_GPS_FINAL_PRECOMMIT_AUDIT.md
research/E5_2_CITATION_CLAIM_AUDIT.md
research/E5_2_CORRECTION_INDEPENDENT_AUDIT.md
research/E5_2_FINAL_STAGING_READINESS_AUDIT.md
research/E5_2_INDEPENDENT_CITATION_AUDIT.md
research/E5_GPS_HOUSEKEEPING_AUDIT.md
research/E5_3_REPRODUCIBILITY_AUDIT.md
research/E5_3_INDEPENDENT_REPRODUCIBILITY_AUDIT.md
```

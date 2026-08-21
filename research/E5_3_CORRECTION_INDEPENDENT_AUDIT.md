# E5.3 Correction Pass — Independent Reproducibility Audit

**Auditor stance:** a researcher who has just cloned this repository and has never seen the
project before, asking "can I actually reproduce Experiment 1?" All findings below were formed by
reading primary sources directly (`git diff`, source files, running commands) — `research/
E5_3_CORRECTION_AUDIT.md` (the builder's own write-up) was read only afterward, to check agreement.

---

## 1. What changed (verified via `git diff`, not description)

```
README.md         | 35 ++++++++++++++++++++++++++++++++---
docs/INDEX.md      |  2 ++
requirements.txt  |  8 ++++++++
3 files changed, 42 insertions(+), 3 deletions(-)
```

- **`requirements.txt`**: added one real line, `rapidfuzz` (unpinned, with a comment explaining no
  version was recorded for the frozen run so none was invented), plus a commented-out `matplotlib`
  line for future figure generation. Matches the described change exactly.
- **`README.md`**: (a) fixed the false Folder-map claim (was `rapidfuzz, requests, boto3, pypdf`,
  now correctly `pandas, requests, tqdm, rapidfuzz`); (b) added a new "Experiment 1 (arXiv-track
  manuscript)" section with a table and a Python/dependency note; (c) added `manuscript/` and
  `research/` rows to the Folder map, and touched the `scripts/`/`data/` rows to mention
  `experiments/exp1/`; (d) added one "Start here" bullet. Matches the described change exactly.
- **`docs/INDEX.md`**: one new bullet pointing at README's new section, no duplicated content.
  Matches the described change exactly.

No other tracked file is modified. `git status --porcelain` shows only these three files as `M`;
everything else in the working tree is either clean or a new untracked `research/*.md` audit
document, none of which is manuscript, contract/lock, or frozen-evidence content.

---

## 2. Does the fix actually work? (independently verified, not trusted)

Grepped every top-of-file `import`/`from` statement, by hand, in the full real execution chain of
`python scripts/experiments/exp1/run_final.py`:

- `run_final.py` → stdlib (`csv`, `itertools`, `json`, `statistics`, `sys`, `time`, `pathlib`) +
  `_loader`, `consistency`, `mechanisms`, `stats` (local modules) + `p2lib.kb`, `p2lib.data`.
- `_loader.py` → stdlib only (`importlib.util`, `sys`, `pathlib`). Also dynamically loads
  `scripts/00_generate_synthetic.py` via `importlib` — I checked this file's imports too, since
  it's executed as part of the real chain even though it isn't a normal Python import: stdlib only
  (`csv`, `hashlib`, `random`, `zlib`, `collections`, `datetime`, `pathlib`).
- `mechanisms.py` → stdlib (`sys`, `pathlib`) + `_loader` + `p2lib.retrieval.fuzzy_company,
  fuzzy_global`.
- `consistency.py` → stdlib (`sys`, `collections`, `pathlib`) + `_loader` + `p2lib.data.split_of`.
- `stats.py` → stdlib only (`random`).
- `p2lib/kb.py` → stdlib only (`collections`).
- `p2lib/data.py` → stdlib only (`csv`, `zlib`, `pathlib`).
- `p2lib/retrieval.py` → `from rapidfuzz import fuzz, process` — **the only non-stdlib import in
  the entire chain.**

Conclusion: `rapidfuzz` is genuinely the sole third-party dependency of the documented
reproduction command. No `numpy`, `scipy`, `boto3`, or `pypdf` appears anywhere in this chain.

**Empirical confirmation, not just static reading**: I built my own isolated venv (independent of
the builder's claimed one), installed only `rapidfuzz` into it, and imported the real chain
(`_loader`, `mechanisms`, `consistency`, `stats`) from `scripts/experiments/exp1/`:

```
OK: exp1 import chain resolves cleanly with only rapidfuzz installed in a fresh venv
```

This is a materially useful check because `rapidfuzz` (3.14.5) was already present in this
session's ambient Python environment — running `pytest` or a plain import there would have masked
a missing-dependency problem. The isolated venv removes that confound. Verdict: **the fix works.**

---

## 3. Is boto3/pypdf genuinely not required? (independently verified)

- `grep -rn "boto3\|pypdf" scripts/experiments/exp1/ scripts/phase2/p2lib/` → zero hits.
- `boto3` repo-wide → exactly one file, `scripts/phase2/p2_03_extract.py` (Phase 2 OCR/Textract
  extraction). Confirmed unrelated to Experiment 1's execution path.
- `pypdf` repo-wide, case-sensitive grep across all `.py` files → **zero hits anywhere in the
  codebase.** Confirmed: the old README claim was fabricated/stale, and the correction pass was
  right not to add either package to `requirements.txt`.

---

## 4. README discoverability (read in full as a first-time cloner)

Read `README.md` end to end. The new "Experiment 1 (arXiv-track manuscript)" section (lines
70–88) is one paragraph plus an 8-row table plus one sentence on dependencies. It answers, without
requiring inference: what Experiment 1 is and how it differs from the Phase 1/2 pipeline above it;
the exact final execution command; frozen config path; seed manifest path; frozen results path;
how headline statistics regenerate (including the fast `--demo` self-check); where figure
generation and the manuscript source live. I independently verified every path in that table
resolves to a real file (`final_frozen_config.json`, `final_seed_manifest.csv`,
`final_condition_results.csv`, `generate_figures.py`, `main.tex`, `references.bib`, `run_final.py`,
`analyze_posthoc.py` — all exist). Two independent entry points lead here: "Start here" item 5 and
the Folder map's `manuscript/`/`research/`/`scripts/` rows. The section is concise — one table, a
handful of sentences — consistent with the "don't turn README into a research diary" constraint;
it does not import internal phase-lettering or audit jargon from `research/`.

---

## 5. Python version claim (independently verified)

`grep -n "min_major\|min_minor\|check_python" prerun_check.py` confirms:
```
def check_python(min_major: int = 3, min_minor: int = 11) -> None:
```
called from four separate entry points in that file (lines 126, 163, 255, 362). Searched the
repository for any other version constraint: no `pyproject.toml`, no `setup.py`, no
`.python-version`, no `.github/workflows/` or other CI config anywhere. This is genuinely the only
Python-version floor established by actual code anywhere in the repository, and README's framing
("the one version floor enforced anywhere in this repository, via `prerun_check.py`") is accurate
and appropriately hedged — it doesn't claim Experiment 1 has its own separate check.

---

## 6. `analyze_posthoc.py --demo` claim (independently verified, re-run myself)

Read `scripts/experiments/exp1/analyze_posthoc.py` in full. Confirmed:
- Imports are stdlib-only: `csv`, `json`, `math`, `statistics`, `pathlib`.
- Reads only the frozen `data/outputs/experiments/exp1/final/final_condition_results.csv`, writes
  only to a separate `posthoc/` output directory (not touched when run with `--demo`).
- `demo()` (lines 372–384) literally asserts:
  - `assert len(rows) == 240`
  - `assert (agree, disagree) == (32, 18)`
  - `assert round(lo, 3) == 0.501 and round(hi, 3) == 0.759` (Wilson 95% CI)
  - `assert round(p, 3) == 0.065` (two-sided exact binomial p vs. 0.5, via `math.comb`)

I re-ran it myself:
```
$ python scripts/experiments/exp1/analyze_posthoc.py --demo
demo() OK: 32/50 agreement, Wilson CI, and binomial p all reproduce from the frozen CSV.
```
Confirmed read-only (no output files written by `--demo`; only `main()` writes to `posthoc/`).
Claim accurate in every particular.

---

## 7. Scope boundary (the most important check) — independently verified

```
git diff --stat -- scripts/experiments/exp1/                                  → empty
git diff --stat -- manuscript/                                                → empty
git diff --stat -- data/outputs/experiments/exp1/final/                       → empty
git diff --stat -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md \
                    research/contribution_lock.csv                            → empty
git diff --stat                                                               → exactly the 3 files
git status --porcelain                                                        → M on exactly 3 files,
                                                                                  rest untracked *.md
```
Nothing outside `README.md`, `docs/INDEX.md`, `requirements.txt` is modified, staged, or unstaged.
Frozen evidence, manuscript source, and contract/lock documents are byte-identical to HEAD.

---

## 8. Tests

`python -m pytest scripts/experiments/exp1/ -q` → **30 passed**, unchanged, as expected since no
exp1 source file was touched.

---

## 9. Public-safety scan

Grepped `README.md`, `docs/INDEX.md`, `requirements.txt` for credential patterns (`AKIA`, PEM
headers, `api_key`, `secret_key`, `Bearer `, `password =`), Windows user paths
(`C:\Users\`), Unix home paths, and the operator's own username — zero hits in all three files.

---

## 10. Agreement with the builder's own write-up (`research/E5_3_CORRECTION_AUDIT.md`), read after forming the above

Read after completing the independent checks above. The builder's §3 (dependency verification),
§4 (README discoverability), §6 (Python version), §8 (realized-ADS regeneration / `analyze_posthoc.py`
demo), and §9 (frozen-file verification) all match what I found independently, including the exact
demo output string and the exact Wilson CI / binomial p figures. One difference: the builder's
write-up does not explicitly show having checked `00_generate_synthetic.py`'s own imports (it's
loaded dynamically via `importlib`, not a normal `import` statement, so a naive `grep "^import|^from"`
sweep over `.py` files would still catch it since it's a real file — the builder's §3 does list
`00_generate_synthetic.py` as checked, so this is consistent, just worth confirming explicitly here
since it's the one file in the chain that isn't imported by a plain `import` statement). No
discrepancy found between the builder's claims and the primary sources.

---

## Verdict: **PASS**

All three changed files were independently verified against primary sources: the dependency fix
(`rapidfuzz`) is correct, complete, and sufficient (confirmed via a fresh isolated venv I built
myself, not by trusting the builder's claimed venv); `boto3`/`pypdf` are correctly and verifiably
excluded; the README's new section is accurate, concise, and every path in it resolves to a real
file; the Python-version claim is accurate; the `analyze_posthoc.py --demo` reproducibility claim
is accurate and was re-run successfully; the scope boundary holds exactly (no manuscript, frozen
evidence, or contract/lock file touched); tests remain 30/30; no secrets or local-path leakage in
the three modified files. No REQUIRED NOW findings. Safe to stage and commit exactly the four files
the builder proposed (`README.md`, `docs/INDEX.md`, `requirements.txt`,
`research/E5_3_CORRECTION_AUDIT.md`) — plus this report if the author wants it included.

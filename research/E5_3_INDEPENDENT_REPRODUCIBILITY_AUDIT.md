# E5.3 — Independent Reproducibility Audit (Adversarial Cross-Check)

> Read-only. No file modified, staged, committed, or pushed. No experiment run, no script
> executed (`run_final.py` and `generate_figures.py` explicitly not run, per brief). HEAD verified
> at `7fd1d9a3d478c40d26fa0c73f86990faf96b6a85` before starting (matches the commit named in the
> brief). This audit was formed independently, from primary-source file reads, **before** reading
> `research/E5_3_REPRODUCIBILITY_AUDIT.md` (the primary/builder report) — §7 below is the
> reconciliation pass done only at the end, as instructed.

---

## 1. Independent findings (formed before reading the primary report)

### 1.1 Discoverability — CONFIRMED BROKEN

Read `README.md` and `docs/INDEX.md` in full, directly. Grepped both for `manuscript`,
`Experiment 1`, `arXiv`, `research/`: **zero matches in either file.**

Followed README's own "Start here" instructions literally:
1. `TECHNICAL_REPORT.md` — the original Phase 1/2 production-engineering report, not the arXiv-track
   paper.
2. `docs/demo/index.html` — the production-trace demo.
3. `STATE.md` — grepped in full for `manuscript/main.tex` and `scripts/experiments/exp1`: **zero
   matches.**
4. `docs/INDEX.md` — zero matches, as above.

I then specifically checked the exact section README promises will explain "how to run the
pipeline" — `STATE.md`'s `## How to run / resume (any session or AI)` (lines 197–207). It lists
only:
```
python scripts/phase2/p2_01_build_kb.py
python scripts/phase2/p2_02_classify_eval.py
python scripts/phase2/p2_03_extract.py
python scripts/phase2/p2_05_end_to_end.py
python scripts/phase2/p2_06_llm_tail.py
python scripts/phase2/test_cascade.py
```
No mention of `scripts/experiments/exp1/run_final.py` or `manuscript/main.tex` anywhere in this
section — the exact section a reader is directed to for run instructions omits Experiment 1
entirely. This is a stronger, more concrete confirmation of the discoverability gap than a general
"README doesn't mention it" observation: the specific promised section fails to deliver.

`STATE.md` line 6 (header) and line 236 do eventually point to `ROADMAP.md` for "arXiv-preprint
prep." I followed that chain too: `ROADMAP.md` grepped for `manuscript`, `Experiment 1`,
`run_final` — only 3 hits, none of which name `manuscript/main.tex` or
`scripts/experiments/exp1/run_final.py` by path. `ROADMAP.md`'s own planned directory tree (line
215–226) shows a *stale, pre-implementation* layout (`research/manuscript/outline.md`) that doesn't
match what was actually built (`manuscript/main.tex` at repo root). A reader who follows this far
still would not land on a working path or command — they'd have to browse the GitHub file tree
directly to find `manuscript/` and `scripts/experiments/exp1/`.

**Verdict on this dimension: independently confirmed. A technically competent researcher following
only the documented navigation chain (README → docs/INDEX.md → STATE.md → ROADMAP.md) would never
be told Experiment 1 exists or where its code lives.**

### 1.2 Execution command / dependency chain — CONFIRMED BROKEN

Read `manuscript/main.tex`'s Reproducibility Statement (line 1429 onward) and
`scripts/experiments/exp1/run_final.py`'s docstring directly. Both state the identical command:
`python scripts/experiments/exp1/run_final.py`. Consistent.

Traced every import in the direct dependency chain by direct file read/grep:
- `run_final.py` → `_loader.py` (stdlib only), `consistency.py` (stdlib + `p2lib.data`),
  `mechanisms.py` → `p2lib.retrieval` → **`from rapidfuzz import fuzz, process`**, `stats.py`
  (stdlib only — confirmed: only `import random`), `p2lib.kb` (stdlib only).
- `scripts/00_generate_synthetic.py` (loaded via `_loader.py`'s importlib shim): stdlib only
  (`csv`, `hashlib`, `random`, `zlib`, `collections`, `datetime`, `pathlib`).

Read `requirements.txt` directly — its actual, complete contents:
```
pandas==2.2.2
requests==2.32.5
tqdm==4.67.3
```
`rapidfuzz` is **absent**. A clean environment doing exactly `pip install -r requirements.txt` then
running the documented command would fail with `ModuleNotFoundError: No module named 'rapidfuzz'`
on import of `mechanisms.py`. I did not execute this (per the read-only/no-run mandate) — this is a
static-analysis conclusion from direct inspection of every import statement against the actual
`requirements.txt` file, which is sufficient to establish the gap without running anything.

Notable additional detail: **none** of `pandas`, `requests`, or `tqdm` — the three packages that
*are* declared — are actually imported anywhere in the Experiment 1 code path I traced. The
declared dependencies and the actually-required dependency are disjoint sets. `requirements.txt`'s
own header comment ("Step 1 — build_inventory") and content confirm it was written for an earlier
Phase-1-era pipeline stage and never updated for Phase 2 (`p2lib.retrieval`, which also needs
`rapidfuzz`) or Experiment 1.

Also checked `calibrate_ads.py`, `calibrate_retrieval_cutoff.py`, `run_pilot.py`,
`analyze_posthoc.py` as instructed: `calibrate_retrieval_cutoff.py` also imports
`p2lib.retrieval` (same `rapidfuzz` requirement). `run_pilot.py` mirrors `run_final.py`'s chain
exactly (same `rapidfuzz` requirement). `analyze_posthoc.py` and `calibrate_ads.py` are stdlib-only
beyond the shared `consistency.py`/`_loader.py` chain. No dependency beyond `rapidfuzz` and (for
figures only) `matplotlib` was found anywhere in the exp1 tree.

**Separately, I found a discrepancy the brief didn't specifically ask about**: `README.md`'s own
"Folder map" table (line 81) describes `requirements.txt` as containing
*"standard library first; rapidfuzz, requests, boto3, pypdf"* — this does not match the actual file
content at all (`pandas`, `requests`, `tqdm`; no `rapidfuzz`, no `boto3`, no `pypdf`). README is
describing a `requirements.txt` that does not exist in this repository state. This is a second,
independent documentation-drift defect on top of the missing-`rapidfuzz` gap itself — ironically,
README's stale description *names* `rapidfuzz` as present when it is in fact the one thing proven
to be missing.

### 1.3 Frozen artifact integrity — CONFIRMED CORRECT

- `final_condition_results.csv`: `wc -l` = 241 lines = 240 data rows + 1 header. Matches the
  manuscript's "240 conditions" claim exactly.
- `final_frozen_config.json` read directly and cross-checked field-by-field against
  `manuscript/main.tex` lines 851–856 (Table) and the frozen-config `assert` statements in
  `run_final.py` (lines 50–54):
  - Targets `{0.00, 0.20, 0.30, 0.50, 0.75, 1.00}` — match.
  - Seeds `31001–31020` (20 seeds) — match.
  - Retrieval cutoff `75` — match.
  - R3 thresholds `0.90` / `0.70` — match.
  - `δ = 0.02`, 2000 bootstrap resamples, α = 0.05 — match.
  - `TOTAL_CONDITIONS: 240` — matches CSV row count.

No discrepancy found between the frozen JSON, the CSV, and the manuscript's stated experimental
design.

### 1.4 Figures — GAP CONFIRMED, BUT PRE-AUTHORIZED AS DEFERRED

Read `manuscript/figures/generate_figures.py` directly. Its own docstring discloses matplotlib was
never actually run in the authoring environment (`ModuleNotFoundError` self-reported). Confirmed
`matplotlib` is not in `requirements.txt`. Grepped `main.tex` for `includegraphics` — **zero
matches**; all four figure references (lines 833, 918, 952, 1004) are captioned placeholders, not
rendered images.

Checked `research/PAPER_CONTRACT.md` directly: line 239–240 states "a placeholder may be a
draft-quality figure or an explicit note" as satisfying the E3 definition of done. Checked
`research/RESEARCH_GPS.md` directly: line 60/111 lists "E5.4 Generate real figures" as an explicit,
not-yet-reached future checkpoint, distinct from the current E5.3 phase.

**Verdict: this is an already-acknowledged, explicitly deferred gap, not an undisclosed defect.**
The underlying dependency gap (matplotlib missing from `requirements.txt`) is real but shares the
same root cause and fix as the `rapidfuzz` gap — not a separate, hidden problem.

### 1.5 Production/confidentiality boundary — CONFIRMED CLEAN

Grepped `manuscript/main.tex` directly for `91.2`, `0.847`, `0.964`, `0.695`. Found at lines 100,
586, 1314–1315 (four numeric occurrences across three locations: Introduction §1.1, Experimental
Design §4.2 for the 0.695 generator-fixed-parameter, Limitations §7.3). Independently located the
`\section{}` boundaries (Results = lines 868–1120) and confirmed none of the four production
statistics fall inside that range. Every occurrence I found carries an explicit "confidential" /
"not independently reproducible" qualifier in the same sentence or paragraph (lines 113–114,
586–587, 813–814, 1314–1322, 1437). No leak found.

### 1.6 Other checks

- **Python version**: grepped `requirements.txt`, `manuscript/main.tex`, `README.md`, `STATE.md`,
  `docs/INDEX.md`, `AGENTS.md` for any version pin (`python 3.x`, `python_requires`,
  `python-version`) — zero matches. Globbed for `pyproject.toml`, `setup.py`, `.python-version`,
  `runtime.txt`, `setup.cfg` — none exist. **Confirmed: no Python version is specified anywhere in
  this repository.**
- **Other undocumented dependencies**: none found beyond `rapidfuzz` and `matplotlib`. Every
  exp1-tree script's import list was read directly (not inferred).
- **`ROADMAP.md` staleness**: its planned repo tree doesn't reflect the actual built structure
  (worth flagging as a minor, separate documentation-drift issue, not a reproducibility blocker).

---

## 2. Independent tier/severity assessment (before reading the primary report)

| Claim | My independent verdict |
|---|---|
| Experiment 1 evidence is deterministically regenerable from public code | TRUE, but blocked in practice by one undocumented import (`rapidfuzz`) |
| A reader can discover Experiment 1 exists by following README's documented path | FALSE — confirmed via literal walkthrough of README → docs/INDEX.md → STATE.md → ROADMAP.md |
| Frozen artifacts match the manuscript's stated design | TRUE — verified field-by-field |
| Figures are a defect | FALSE as a hidden defect — TRUE as a real but pre-authorized, explicitly-deferred (E5.4) gap |
| Production/confidentiality boundary is respected | TRUE — verified at every occurrence |
| No research-integrity violation (no fabricated/altered evidence, no rejected-claim resurrection, no frozen-artifact tampering) | TRUE — nothing found in this pass touches those axes |

My independent conclusion, reached before reading the builder's report: the two real, concrete,
externally-verifiable defects are (1) the discoverability gap and (2) the missing `rapidfuzz`
declaration — both pure documentation/packaging gaps, not integrity problems. This would put the
overall state at **CONDITIONAL (ORANGE)**: specific, fixable, non-blocking-to-science issues that
should be closed before this repository can honestly claim "one command reproduces this" to an
external reader.

---

## 3. Reconciliation with `research/E5_3_REPRODUCIBILITY_AUDIT.md` (read after forming the above)

Read the primary report in full after completing my own independent pass. Comparison:

**Agreement (full):**
- Discoverability failure — identical root cause, identical evidence (README/docs/INDEX.md zero
  hits), identical conclusion.
- `rapidfuzz` missing from `requirements.txt`, reached via the same import chain
  (`run_final.py → mechanisms.py → p2lib.retrieval`).
- 240-row CSV count, frozen config field-by-field match against `main.tex` §4 — identical numbers,
  independently re-verified by me via direct `wc -l` and direct file reads (not by trusting the
  primary report's counts).
- Figures: matplotlib undocumented, but figure-wiring gap correctly scored as pre-authorized/
  deferred to E5.4 per `PAPER_CONTRACT.md` §11 — same conclusion, same citation.
- Production/confidentiality boundary — same four statistics, same occurrences, same "no leak"
  conclusion.
- Python version unspecified — same conclusion.
- No stdlib-only claim violated for `stats.py`/`consistency.py` — same conclusion.

**What the primary report found that I had not specifically flagged:**
- The `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md` banding/framing gap (§4.E, §5 of the primary
  report) — that the manuscript's exact headline percentages require reading an unlinked internal
  document to see the precise realized-ADS-band aggregation logic, even though the underlying CSV
  columns needed are present. I did not independently pursue recomputing the headline percentages
  from the raw CSV in this pass (out of scope of my walkthrough, which focused on the six items the
  brief enumerated), so I cannot independently confirm or refute this specific claim — noting it as
  **unverified by me**, not confirmed.
- The 56-question structured framework and reproducibility-tier (T1–T5) classification scheme are
  the primary report's own organizing device; I did not replicate that structure, but my six
  targeted checks map onto the same underlying facts and reached the same conclusions wherever they
  overlap.

**What I found that the primary report did not call out explicitly:**
- README's "Folder map" table (line 81) misdescribes `requirements.txt`'s actual contents
  (claims `rapidfuzz, requests, boto3, pypdf`; actual file has `pandas, requests, tqdm`). The
  primary report notes `requirements.txt` is stale/written-for-Phase-1 via its header comment, but
  didn't specifically flag that README's own folder-map entry is *also* wrong, independently, in a
  different and more misleading way (it names the exact missing package as if it were present).
- The specific `STATE.md` `## How to run / resume` section (lines 197–207) as the concrete
  confirming instance of the discoverability gap — the primary report makes the same general point
  via the README-level walkthrough but didn't cite this specific section, which is a stronger,
  line-level piece of evidence since it's the exact section README promises will cover "how to run
  the pipeline."
- `ROADMAP.md`'s stale planned-tree structure (doesn't match the actual built `manuscript/`
  location) — a minor documentation-drift note, not independently raised in the primary report.

**No disagreement found** on any verdict, severity ranking, or the "not a research-integrity
violation" conclusion. Both passes converge on the same two HIGH-severity, non-blocking-to-science
findings.

---

## 4. Findings

1. **REQUIRED NOW.** `README.md` and `docs/INDEX.md` — the repository's only two navigation entry
   points — never mention `manuscript/`, `scripts/experiments/exp1/`, `research/`, "Experiment 1,"
   or an arXiv preprint. `STATE.md`'s own "How to run / resume" section (lines 197–207), the exact
   section README promises covers "how to run the pipeline," lists only the Phase 1/2 pipeline
   scripts and omits Experiment 1 entirely. A reader following the documented path cannot discover
   Experiment 1 exists. (`README.md` lines 28–36, 68–82; `STATE.md` lines 197–207;
   `docs/INDEX.md` full file.)
2. **REQUIRED NOW.** `requirements.txt` (repo root) does not declare `rapidfuzz`, which is a
   required, direct-chain import for the manuscript's sole documented reproduction command
   (`python scripts/experiments/exp1/run_final.py`, via `mechanisms.py` → `p2lib/retrieval.py`
   line 8). A clean `pip install -r requirements.txt` followed by the documented command fails with
   `ModuleNotFoundError`. (`requirements.txt`; `scripts/phase2/p2lib/retrieval.py:8`.)
3. **REQUIRED NOW** (same root cause as #2, separate artifact). `matplotlib` is not declared in
   `requirements.txt` either, required only for `manuscript/figures/generate_figures.py`. Lower
   urgency than #2 since figures are not yet wired into `main.tex` via `\includegraphics{}` (an
   explicitly pre-authorized, deferred gap per `PAPER_CONTRACT.md` §11 and `RESEARCH_GPS.md`'s
   E5.4 checkpoint) — but the dependency-declaration gap itself is real today, independent of the
   wiring question. (`requirements.txt`; `manuscript/figures/generate_figures.py:1-22`.)
4. **OPTIONAL FUTURE WORK.** `README.md`'s own "Folder map" entry for `requirements.txt` (line 81)
   describes contents (`rapidfuzz, requests, boto3, pypdf`) that do not match the file's actual
   contents (`pandas, requests, tqdm`). This is a documentation-drift bug distinct from #2/#3, and
   should be corrected in the same pass since the fix is adjacent. (`README.md:81`.)
5. **OPTIONAL FUTURE WORK.** No Python version is specified anywhere in the repository (no
   `pyproject.toml`, `setup.py`, `.python-version`, `runtime.txt`, and no version mentioned in any
   doc checked). Not observed to cause a failure during static inspection, but unverified beyond
   that — worth pinning for a genuinely locked reproducibility claim.
6. **OPTIONAL FUTURE WORK.** `ROADMAP.md`'s planned directory tree (lines 215–226) shows a stale,
   pre-implementation layout that doesn't match the manuscript's actual built location
   (`manuscript/main.tex` at repo root, not `research/manuscript/outline.md`). Minor, cosmetic,
   doesn't block reproduction since the manuscript itself states the correct path.
7. **OPTIONAL FUTURE WORK** (raised by the primary report, unverified by me this pass). The exact
   realized-ADS-band aggregation behind the manuscript's headline percentages is documented only in
   `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`, not linked publicly and not a single runnable
   script. I did not independently recompute this in my pass; flagging as inherited-from-primary,
   not independently confirmed.

No finding in either pass touches frozen-evidence integrity, resurrects a rejected claim, or
indicates a fabricated/altered number. Every finding above is a documentation/packaging
completeness gap.

---

## 5. Verdict

**ORANGE (CONDITIONAL)**

Justification: The underlying science is genuinely sound — frozen artifacts, seeds, configuration,
and the manuscript's stated experimental design all cross-check exactly, independently verified by
direct file inspection rather than trust in either document's self-description. The
confidentiality/production boundary is correctly and consistently maintained everywhere checked.
No research-integrity violation, no altered frozen evidence, no resurrected rejected claim, and no
unsafe git state was found in this pass. However, the manuscript's implicit promise — that a
competent external researcher can find and reproduce Experiment 1 using this repository as
published — is not currently true in practice: the documented navigation path never surfaces
Experiment 1's existence, and the single documented reproduction command fails on a clean
`pip install -r requirements.txt` environment due to a missing `rapidfuzz` declaration. These are
concrete, specific, narrowly-scoped fixes (two `requirements.txt` additions, one discoverability
pointer in `README.md`/`docs/INDEX.md`) — not a research-integrity failure — which is exactly the
CONDITIONAL band: safe to close with named fixes, not safe to claim "reproducibility verified" as a
checkpoint until they land.

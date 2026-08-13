# E3 Statistical Reconciliation — Independent Audit

> Read-only independent audit of `research/E3_STATISTICAL_RECONCILIATION.md`'s claims and of the
> current state of `manuscript/main.tex`. All numbers below were recomputed from scratch, in a
> fresh hand-rolled script, directly against the frozen CSV — no number was copied from the
> reconciliation document, `stats.py`, or any `research/*.md` prose without independent
> recomputation. No file other than this one was written or modified during this audit.

## 1. Method

Wrote a standalone script (kept in the session scratchpad, not committed to the repo — see
provenance note at the end of this document) that:

- reads `data/outputs/experiments/exp1/final/final_condition_results.csv` directly via
  `csv.DictReader`, independent of `scripts/experiments/exp1/stats.py`;
- implements its own exact two-sided binomial test (`comb`-based point-probability method) and its
  own Wilson-interval formula, from stdlib `math` only;
- recomputes every count, rate, p-value, and CI cited in the task from the raw rows, with no
  intermediate reliance on any `research/*.md` document.

## 2. Recomputation results (independent, this audit)

### 2.1 Realized-ADS-band agreement (per-row `realized_det_pct`, R3 thresholds 0.70/0.90), VARIED only

| Band | agree | disagree | n_defined | rate |
|---|---:|---:|---:|---:|
| 0.70–0.90 | 32 | 0 | 32 | 100% |
| ≥0.90 | 0 | 18 | 18 | 0% |

Matches the task's expected 32/32 and 0/18 exactly. CLEAN independently confirmed to contribute
zero defined comparisons at every band (all 120 CLEAN rows have blank `r3_agrees_with_empirical`,
`empirical_winner == "tie"` for all 120).

### 2.2 By-nominal-target agreement, VARIED only

| Target group | agree | disagree | n_defined | rate |
|---|---:|---:|---:|---:|
| {0.50, 0.75} | 30 | 0 | 30 | 100% |
| {1.00} | 2 | 18 | 20 | 10% |

Matches the task's expected 30/30 and 2/20 exactly.

### 2.3 Exact two-sided binomial p-values (vs. p0=0.5), independently computed

| Count pair | p (this audit) | Rounds to |
|---|---:|---|
| 32/32 (realized-band) | 4.656613×10⁻¹⁰ | 4.7×10⁻¹⁰ |
| 0/18 (realized-band) | 7.629395×10⁻⁶ | 7.6×10⁻⁶ |
| 30/30 (by-target) | 1.862645×10⁻⁹ | **1.9×10⁻⁹** |
| 2/20 (by-target) | 4.024506×10⁻⁴ | **4.0×10⁻⁴** |

**Confirmed: p≈1.9×10⁻⁹ belongs to 30/30 (by-nominal-target), not 32/32 (realized-band). p≈4.0×10⁻⁴
belongs to 2/20 (by-nominal-target), not 0/18 (realized-band).** These are mathematically distinct
values (32/32 gives 4.66×10⁻¹⁰, an order of magnitude different from 1.9×10⁻⁹; 0/18 gives
7.63×10⁻⁶, also clearly distinct from 4.0×10⁻⁴), so the pairing is unambiguous on numerical
grounds alone, independent of any document's labeling. This exactly matches
`E3_STATISTICAL_RECONCILIATION.md` §2.D's own values (4.657×10⁻¹⁰, 7.629×10⁻⁶, 1.863×10⁻⁹,
4.025×10⁻⁴) to the precision both computations report.

### 2.4 Overall aggregate

- Row counts (recounted directly, not assumed): agree=32, disagree=18, tie=120 (all CLEAN),
  N/A/`llm_required`=70 (all VARIED rows with `target_deterministic_share` realizing below 0.70).
  32+18+120+70 = 240. ✅
- Denominator 50 = 32 + 18, independently confirmed to exclude exactly the 120 tie rows and 70 N/A
  rows (counted directly from the CSV, not inferred).
- 32/50 = **64.0000%** — exact match.
- Exact two-sided binomial p = **0.064909**, rounds to the manuscript's stated **0.0649** — exact
  match.
- Wilson 95% CI (z=1.959964) = **[0.5014, 0.7586]** = **[50.14%, 75.86%]** — exact match.

### 2.5 Supporting micro-facts cited in the reconciliation, independently spot-checked

- Target 0.50, VARIED: exactly 10/20 seeds realize below 0.70, 10/20 realize ≥0.70. ✅ matches
  §2.B/§3's claim.
- Target 1.00, VARIED, realized < 0.90: exactly 2 rows, seeds 31007 (realized 0.893536...) and
  31012 (realized 0.894057...). ✅ matches the reconciliation's cited seed values exactly.

**Conclusion:** every numerical claim in `research/E3_STATISTICAL_RECONCILIATION.md` §2, §4, and §6
is independently reproduced exactly by this second, from-scratch implementation. No discrepancy
found in the underlying statistics.

## 3. Manuscript (`manuscript/main.tex`) verification

Grepped the full file for every occurrence of `32/32`, `0/18`, `30/30`, `2/20`, `32 of 32`,
`0 of 18`, `30 of 30`, `2 of 20`, the two p-values, `64.0%`, and `32/50` (18 distinct line hits
across the file — none in the abstract, which states rates only, not exact counts or p-values).
Read every hit in full sentence/row context:

| Location | Content | Verdict |
|---|---|---|
| §5.4 line 989–999 (first paragraph) | States 32/32 (100%) and 0/18 (0%) for the realized-ADS-band framing, and separately 30/30 (100%) and 2/20 (10%) for the by-target framing — no p-value attached to either sentence | ✅ correct, no p-value present |
| §5.4 line 1001–1013 (aggregate paragraph) | "the per-row realized-ADS bands are exceptionless (32 of 32 and 0 of 18), and the corresponding by-nominal-target counts are independently significant at exact binomial p=1.9×10⁻⁹ (30 of 30) and p=4.0×10⁻⁴ (2 of 20)" | ✅ correct — p-values are in-line, parenthetically attached to 30 of 30 / 2 of 20, not to 32 of 32 / 0 of 18 |
| Figure F3 caption, line 1029–1032 | "100% (32/32)... versus 0% (0/18)" — descriptive only | ✅ correct, no p-value |
| Table T4 caption, line 1038–1043 | Explicitly states 32/32 and 0/18 are reported in §5.4 and that "no independently frozen p-value exists for those exact counts, so none is stated here" | ✅ correct |
| Table T4 rows, line 1049–1051 | "Overall agreement (32/50) → 64.0%, p=0.0649"; "By target, targets 0.50/0.75 (30/30) → 100%, p=1.9×10⁻⁹"; "By target, target 1.00 (2/20) → 10%, p=4.0×10⁻⁴" | ✅ correct on all three rows; no row pairs a p-value with 32/32 or 0/18 |
| §5.6 "Statistical Interpretation", line 1112–1121 | "Both individual by-nominal-target bands are far more statistically significant... (p=1.9×10⁻⁹ for the 30/30 retrieval-region band and p=4.0×10⁻⁴ for the 2/20 rules-region band...). The sharper per-row realized-ADS bands (32/32 and 0/18, Section 5.4) are exceptionless but... are not independently paired with a frozen p-value" | ✅ correct and explicit — this is the strongest, most unambiguous statement in the file |
| §5.7 "Summary of Findings", line 1136 | "64.0% aggregate agreement rate" — aggregate only, no band number | ✅ correct |
| §6.3 "What the Original Hypothesis Got Right", line 1185–1190 | "one full realized-ADS band shows perfect, exceptionless agreement (32 of 32, Section 5.4), with the corresponding by-nominal-target count independently significant at p=1.9×10⁻⁹ (Section 5.6)" | ✅ correct — "32 of 32" is stated with no p-value; "the corresponding by-nominal-target count" (i.e., 30/30, not 32/32) is the antecedent of the p-value, worded unambiguously |

**Independently confirmed:** as the file currently stands, no p-value is attached (in the same
sentence, parenthetical, or table row) to the 32/32 or 0/18 counts anywhere in the manuscript.
1.9×10⁻⁹ and 4.0×10⁻⁴ are attached exclusively, and always explicitly, to the 30/30 and 2/20 counts
respectively. This matches `E3_STATISTICAL_RECONCILIATION.md` §5's table exactly — independently
re-derived, not merely re-read.

### 3.1 Note on the frozen source document's own ambiguous labeling (not a manuscript defect)

`research/EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` (frozen, Phase D) itself contains the ambiguity that
most likely caused the original manuscript bug: its own summary table (lines 85–87) labels the
30/30 and 2/20 rows as **"ADS 0.70–0.90 (targets 0.50, 0.75)"** and **"ADS ≥0.90 (target 1.00)"** —
i.e., it uses realized-ADS-band language for counts that are actually by-nominal-target counts. That
document predates the sharper realized-vs-nominal distinction introduced later in
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9–10. This is not something this audit or the reconciliation
pass may fix (it is frozen evidence, outside the allowed edit scope), but it is worth flagging
explicitly: `manuscript/main.tex` correctly resolves the ambiguity by always saying **"By target"**
(not "ADS band") wherever it attaches these two p-values (Table T4 rows, §5.6), so the manuscript
itself is not ambiguous even though its ultimate source document is loosely worded. This is an
**OPTIONAL FUTURE WORK** note, not a defect in the current manuscript text.

### 3.2 Note on `PAPER_CONTRACT.md`'s canonical numerical list

`research/PAPER_CONTRACT.md` §7 ("Numerical rule") lists 32/32 and 0/18 as canonical Experiment 1
values but does **not** list 30/30, 2/20, 1.9×10⁻⁹, or 4.0×10⁻⁴ anywhere in its "Canonical
(citable)" bullet list, even though these four values are now used extensively in the manuscript
(Table T4, §5.4, §5.6, §6.3) and do genuinely trace to frozen evidence
(`EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` lines 85–87, independently verified as mathematically
correct in §2.3 above). This reads as an incompleteness in `PAPER_CONTRACT.md`'s curated list
rather than a fabrication risk — the values are real, sourced, and independently recomputed exact —
but since §7 frames itself as an allowlist ("Only canonical, verified values may enter the
manuscript"), a strict reading could flag these four values as absent from the list. **OPTIONAL
FUTURE WORK**: the human author may wish to add 30/30, 2/20, and the two p-values to
`PAPER_CONTRACT.md` §7's canonical list for completeness, since the manuscript now depends on them
this heavily. Not a blocking finding — `PAPER_CONTRACT.md` was not part of this task's edit scope
and was not modified by the reconciliation pass, and the values are independently traceable to
frozen evidence regardless of the list's completeness.

## 4. Figure-script audit (`manuscript/figures/generate_figures.py`)

Re-read the file in full, independently of the reconciliation document's own §8:

- **Read-only, single frozen source:** only path opened is
  `data/outputs/experiments/exp1/final/final_condition_results.csv`; grepped the file for `"w"`,
  `"a"`, `open(` — the only `open()` call is the CSV read in `load_rows()`, no write mode anywhere.
  `savefig()` calls target only `OUT_DIR` (`manuscript/figures/`). Confirmed no writes into
  `data/outputs/experiments/`.
- **No hardcoded scientific results:** the only numeric constants in the file are `R3_LOW = 0.70`
  and `R3_HIGH = 0.90` (frozen R3 threshold configuration, reused unchanged elsewhere in the
  repository) — confirmed by reading the full file; no headline number (64.0, 32/50, 1.9e-9, 4.0e-4,
  0.9031, etc.) appears anywhere in the script.
- **No new statistical computation:** `make_f2`/`make_f3`/`make_f4` compute only raw scatter
  coordinates, simple counts, and a rate (`agree/n`) — no p-value, correlation coefficient, or CI
  computed anywhere in the file.
- **Deterministic:** no `random`, no sampling, no bootstrap — confirmed by full read.
- **Not executed in this environment, and disclosed:** `python -c "import matplotlib"` independently
  re-run in this audit → `ModuleNotFoundError: No module named 'matplotlib'`. The script's own
  docstring (lines 8–17) discloses this explicitly and names the reason. Not hidden.

**No issues found**, independently confirming `E3_STATISTICAL_RECONCILIATION.md` §8.

## 5. Git-state verification (frozen-artifact protection)

Independently run, this audit:

- `git status --porcelain data/outputs/experiments/` → **empty output** (no modifications to any
  frozen experiment artifact, including `final_condition_results.csv`).
- `git diff --stat HEAD -- TECHNICAL_REPORT.md README.md METHODOLOGY.md` → **empty** (unchanged).
- `git log --follow --oneline -- data/outputs/experiments/exp1/final/final_condition_results.csv` →
  single commit `6fb6188 Phase D: freeze Experiment 1 evidence`, no subsequent commits or working-tree
  modifications.
- Full `git status --porcelain`: only `manuscript/main.tex` shows as modified (`M`); all other
  touched paths (`manuscript/figures/`, and ten `research/*.md` files including
  `E3_STATISTICAL_RECONCILIATION.md`) are untracked new files (`??`), not modifications of existing
  tracked files. No existing `research/*.md` file (other than the newly-created
  `E3_STATISTICAL_RECONCILIATION.md`) shows as modified.

**No frozen artifact was altered.** The only tracked file modified is `manuscript/main.tex`, which
is the file this whole exercise concerns and is explicitly in scope for editing under
`PAPER_CONTRACT.md`.

## 6. Findings

1. **[OPTIONAL FUTURE WORK]** `research/EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` lines 85–87 labels the
   30/30 and 2/20 counts with "ADS 0.70–0.90"/"ADS ≥0.90" language that is properly by-target, not
   realized-band, language — the likely root cause of the original manuscript bug. Frozen; cannot be
   edited under this task's or this audit's permissions. The manuscript itself has already resolved
   this ambiguity correctly by using "By target" phrasing wherever these counts/p-values appear.
2. **[OPTIONAL FUTURE WORK]** `research/PAPER_CONTRACT.md` §7's "Canonical (citable)" list omits
   30/30, 2/20, and both p-values (1.9×10⁻⁹, 4.0×10⁻⁴), even though the manuscript now cites them
   repeatedly and they are independently verified to be real, correctly-computed, frozen-evidence-
   sourced numbers. Worth adding to the canonical list for completeness, but not a defect in the
   manuscript text and not something this read-only audit may fix itself.

No REQUIRED NOW findings.

## 7. Required fixes

None. No discrepancy was found between the independent recomputation and either
`research/E3_STATISTICAL_RECONCILIATION.md`'s claims or the current state of `manuscript/main.tex`.

## 8. Verdict

## 🟢 PASS_WITH_NOTES

**Justification:** Every quantitative claim in `research/E3_STATISTICAL_RECONCILIATION.md` (the
realized-ADS-band counts 32/32 and 0/18, the by-nominal-target counts 30/30 and 2/20, all four exact
binomial p-values, the overall 32/50 aggregate, its Wilson CI, and its p-value) was independently
reproduced exactly by a second, from-scratch implementation in this audit, reading only the frozen
CSV. `manuscript/main.tex` was independently re-read at every one of the 18 lines matching the
disputed value patterns, and in every case the two p-values (1.9×10⁻⁹, 4.0×10⁻⁴) are attached
exclusively and unambiguously to the by-nominal-target counts (30/30, 2/20), never to the
realized-ADS-band counts (32/32, 0/18) — the original defect the E3 draft audit found is fully
corrected and does not recur anywhere else in the document. `manuscript/figures/generate_figures.py`
is read-only against frozen evidence, introduces no new statistic, is deterministic, and its
non-execution in this environment is disclosed rather than hidden. No frozen artifact (the CSV, any
pre-existing `research/*.md` file, `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`) was
modified. The two notes above (an ambiguous label in a frozen source document, and an incomplete
canonical-value list in `PAPER_CONTRACT.md`) are pre-existing documentation-completeness gaps that
do not affect the correctness of the current manuscript text and are recorded as optional future
work, not blockers — hence PASS_WITH_NOTES rather than a plain PASS.

---

*Provenance note: this audit's recomputation script was written to and run from the session
scratchpad directory (outside the repository), consistent with the constraint that only this file
was to be written under `research/`. It is not part of the repository and leaves no trace in `git
status`.*

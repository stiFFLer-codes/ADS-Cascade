# E3 Statistical Reconciliation — Independent Verification of the Realized-ADS-Band /
# By-Target-Band / p-value Pairing

> Read-only reconciliation audit, requested before the E3 checkpoint, of the numerical-pairing
> defect the E3 draft auditor found and this session corrected (`manuscript/main.tex`, Sections
> 5.4/5.6/6.3 and Table T4). Independently re-derives every number from the frozen CSV using a
> second, hand-rolled implementation (not the harness's `stats.py`, not any `research/*.md`
> report), cross-checks every occurrence of the disputed values in the current manuscript text, and
> re-invokes the independent auditor for a final verdict. No manuscript prose was changed by this
> document; two small wording fixes it identifies in §5/§7 below were applied directly to
> `manuscript/main.tex` as part of this same pass (see those sections for exactly what changed and
> why — both are re-attributions of already-sourced numbers to their correct counts, not new
> computations or new claims). No frozen artifact was modified.

---

## 1. Source artifact used

`data/outputs/experiments/exp1/final/final_condition_results.csv` — the frozen, 240-row, 24-column
primary Experiment 1 output. Read directly via Python's stdlib `csv.DictReader`; no other file was
used as a source of numbers for §2 below (not `EXPERIMENT_1_FINAL_RESULTS.md`, not
`EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`, not `EXPERIMENT_1_POSTHOC_ANALYSIS.md`, and not the
manuscript's own prose) — those documents were consulted only afterward, in §5, to cross-check the
independently-derived numbers against what has already been reported elsewhere.

The recomputation script (`check_underscore_v2.py`-style scratch script, not committed to the
repository) used a hand-rolled exact two-sided binomial test and a hand-rolled Wilson-interval
formula, implemented from scratch in this session — not an import of, or call into,
`scripts/experiments/exp1/stats.py`. This makes it a genuinely independent second implementation of
the statistics, not a re-run of the same code path that produced the manuscript's numbers.

---

## 2. Independent recomputation

### 2.A — Realized-ADS-band agreement (per-row `realized_det_pct`, binned against R3's own
thresholds 0.70/0.90), by lexical condition

| Lexical | Band | n (rows) | agree | disagree | blank (tie or N/A) | n\_defined | rate |
|---|---|---:|---:|---:|---:|---:|---:|
| CLEAN | <0.70 | 70 | 0 | 0 | 70 | 0 | undefined |
| CLEAN | 0.70–0.90 | 32 | 0 | 0 | 32 | 0 | undefined |
| CLEAN | ≥0.90 | 18 | 0 | 0 | 18 | 0 | undefined |
| VARIED | <0.70 | 70 | 0 | 0 | 70 (all N/A, `llm_required`) | 0 | undefined |
| **VARIED** | **0.70–0.90** | 32 | **32** | **0** | 0 | **32** | **1.0000 (100%)** |
| **VARIED** | **≥0.90** | 18 | **0** | **18** | 0 | **18** | **0.0000 (0%)** |

Confirms the manuscript's stated **32/32 (100%)** and **0/18 (0%)** exactly. CLEAN independently
confirmed to contribute zero defined comparisons at any band (all 120 CLEAN rows are ties).

### 2.B — Nominal-target-band agreement (`target_deterministic_share`, binned into R3's
retrieval-recommended region {0.50, 0.75} and rules-recommended region {1.00}), VARIED only

| Target group | n (rows) | agree | disagree | blank | n\_defined | rate |
|---|---:|---:|---:|---:|---:|---:|
| Retrieval-region targets {0.50, 0.75} | 40 | **30** | 0 | 10 (`llm_required`, target 0.50 seeds realizing <0.70) | **30** | **1.0000 (100%)** |
| Rules-region target {1.00} | 20 | **2** | **18** | 0 | **20** | **0.1000 (10%)** |

Confirms the manuscript's stated **30/30 (100%)** and **2/20 (10%)** exactly.

### 2.C — Exact sample sizes / success-failure counts (summary of 2.A/2.B, restated for clarity)

| Framing | Successes | Trials | Failures |
|---|---:|---:|---:|
| Realized-ADS band, 0.70–0.90 (per-row) | 32 | 32 | 0 |
| Realized-ADS band, ≥0.90 (per-row) | 0 | 18 | 18 |
| By-nominal-target, retrieval region {0.50, 0.75} | 30 | 30 | 0 |
| By-nominal-target, rules region {1.00} | 2 | 20 | 18 |

### 2.D — p-value mapping (exact two-sided binomial test vs. $p_0=0.5$, independently computed)

| Count pair | Exact two-sided binomial $p$ | Matches manuscript's cited value? |
|---|---:|---|
| Realized-ADS band 0.70–0.90 (32/32) | $4.657\times10^{-10}$ | **No** — manuscript (pre-fix) had cited $1.9\times10^{-9}$ next to this pair; that value belongs to the row below |
| Realized-ADS band ≥0.90 (0/18) | $7.629\times10^{-6}$ | **No** — manuscript (pre-fix) had cited $4.0\times10^{-4}$ next to this pair; that value belongs to the row below |
| By-nominal-target, retrieval region (30/30) | $1.863\times10^{-9}$ | **Yes** — rounds to $1.9\times10^{-9}$, exactly matching `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7's own stated value for this exact count pair |
| By-nominal-target, rules region (2/20) | $4.025\times10^{-4}$ | **Yes** — rounds to $4.0\times10^{-4}$, exactly matching `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7's own stated value for this exact count pair |

**Conclusion of §2:** independently confirms, from the raw CSV alone, using a second
implementation, exactly what the E3 draft auditor found: the two p-values $1.9\times10^{-9}$ and
$4.0\times10^{-4}$ belong to the **by-nominal-target** counts (30/30 and 2/20), not to the
**realized-ADS-band** counts (32/32 and 0/18). No independently frozen p-value exists anywhere in
`research/EXPERIMENT_1_*.md` for the exact realized-ADS-band counts (32/32, 0/18) — those two
documents' own tables (`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9) report the 32/32 and 0/18 counts
themselves but do not attach a p-value column to them.

---

## 3. Count definitions

- **Realized-ADS band (per-row, "primary framing" per the manuscript's own §5.4 language):**
  computed from each row's own `realized_det_pct` (the measured, train-only historical-consistency
  statistic), binned against R3's own thresholds ($<0.70$, $[0.70,0.90)$, $\geq0.90$). This is the
  sharper of the two framings because it groups by the exact value R3's threshold rule acts on.
- **By-nominal-target band ("secondary framing"):** computed from `target_deterministic_share` (the
  generator's *input* control knob, not the measured outcome), grouped by which of the six nominal
  targets a condition was generated at (0.50/0.75 → the two targets whose realized values land in
  R3's retrieval region on average; 1.00 → the target whose realized values land in R3's rules
  region on average).
- **Why they differ:** nominal target and per-row realized ADS do not always coincide (confirmed
  directly in §2.B: 10 of the 20 seeds at nominal target 0.50 realize *below* 0.70 and are excluded
  as `llm_required`, N/A; the remaining 10 realize at or above 0.70). At nominal target 1.00, two of
  the twenty seeds realize *below* 0.90 (confirmed by direct inspection of the CSV: seeds with
  realized ADS 0.8935 and 0.8941) and therefore fall in the $[0.70,0.90)$ realized-band under the
  per-row framing while still sharing the 1.00 nominal target under the by-target framing — this is
  exactly the mechanism the manuscript's §4.4/§5.4 prose already describes, and this reconciliation
  confirms it holds for exactly the rows the manuscript implies.

---

## 4. p-value mapping (restated as the direct answer to Task 1.D)

**$p=1.9\times10^{-9}$ belongs to the by-nominal-target 30/30 count. $p=4.0\times10^{-4}$ belongs to
the by-nominal-target 2/20 count. Neither belongs to the realized-ADS-band 32/32 or 0/18 counts.**
No independently frozen p-value exists for the realized-ADS-band counts in any `research/*.md`
document; if one is wanted, it would have to be newly computed ($p\approx4.7\times10^{-10}$ for
32/32, $p\approx7.6\times10^{-6}$ for 0/18 — see §2.D), which `PAPER_CONTRACT.md` §7's numerical
rule treats as "not canonical by default" unless and until a human author decides to add it as a new
canonical value. This reconciliation does not add it; see §7 for the decision this pass actually
made (re-attribute, don't invent).

---

## 5. Manuscript occurrences checked

Every occurrence of `32/32`, `0/18`, `30/30`, `2/20`, the two p-values, `64.0%`, and `32/50` in
`manuscript/main.tex`, checked line-by-line against the independent recomputation in §2. State is
**after** the two fixes described in §7 (both already applied to `manuscript/main.tex` as part of
this pass).

| Value | Section/Table | Interpretation | Source | Correct? |
|---|---|---|---|---|
| 32/32, 0/18 | §5.4 prose, "primary framing" sentence | Per-row realized-ADS-band agreement (100%, 0%) | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9 | ✅ Correct, and — after the fix — no p-value is attached to this sentence |
| 30/30, 2/20 | §5.4 prose, "secondary framing" sentence | By-nominal-target agreement (100%, 10%) | `EXPERIMENT_1_FINAL_RESULTS.md` §5 | ✅ Correct |
| 32/32, 0/18 | §5.4 prose, aggregate-explanation paragraph | Restated as "exceptionless," explicitly **not** paired with a p-value; the by-nominal-target counts (30/30, 2/20) in the same sentence are the ones paired with $p=1.9\times10^{-9}$/$p=4.0\times10^{-4}$ | Same as above | ✅ Correct (fixed this pass, see §7) |
| 1.9e-9, 4.0e-4 | §5.4 prose | Explicitly attached to "(30 of 30)" and "(2 of 20)" respectively, in-line | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7 | ✅ Correct |
| 32/32, 0/18 | Figure F3 caption | Descriptive only ("100% (32/32)... versus 0% (0/18)"), no p-value stated | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4-5 | ✅ Correct |
| 32/32, 0/18 | Table T4 caption | Explicitly states these are reported in §5.4 and that "no independently frozen $p$-value exists for those exact counts, so none is stated here" | — | ✅ Correct |
| 30/30, 2/20 + 1.9e-9, 4.0e-4 | Table T4 rows | "By target, targets 0.50/0.75 (30/30)" → $1.9\times10^{-9}$; "By target, target 1.00 (2/20)" → $4.0\times10^{-4}$ | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §6-7 | ✅ Correct |
| 32/50, 64.0% | Table T4 row 1 | Overall agreement, Wilson CI [50.14%, 75.86%], $p=0.0649$ | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §6 | ✅ Correct — see §6 below |
| 1.9e-9, 4.0e-4 | §5.6 "Statistical Interpretation" | **Fixed this pass** (was ambiguous — see §7). Now explicitly reads "for the 30/30 retrieval-region band" / "for the 2/20 rules-region band," and separately states the 32/32/0/18 per-row bands "are exceptionless but... are not independently paired with a frozen $p$-value" | Same evidence as above | ✅ Correct (fixed this pass) |
| 32/32, 0/18 (as "30 and 20"/"32 and 18") | §5.6 | "The number of defined comparisons is small in both informative bands (30 and 20 by the by-target framing; 32 and 18 by the per-row framing)" | — | ✅ Correct — both framings' sample sizes stated, no p-value misattached |
| 64.0% | §5.7 "Summary of Findings" | "the flat 64.0% aggregate agreement rate alone under-communicates..." | — | ✅ Correct, no band-level number attached here |
| 32/32 (as "32 of 32") + 1.9e-9 | §6.3 "What the Original Hypothesis Got Right" | **Fixed this pass** (was "perfect, highly significant agreement" with no number — ambiguous enough to imply an untested significance claim for 32/32 itself). Now explicitly reads "perfect, exceptionless agreement (32 of 32, Section 5.4), with the corresponding by-nominal-target count independently significant at $p=1.9\times10^{-9}$" | — | ✅ Correct (fixed this pass) |
| 64.0% | §6.3 | "The point estimate, 64.0%,..." | — | ✅ Correct, aggregate only |
| 32/50 | §1 header comment | "% Governed by..." — unrelated; not a data value | — | N/A (false-positive grep match, comment text) |

**Confirmed:** 32/32 and 0/18 are used exclusively as descriptive realized-ADS-band results
throughout the current text; 30/30 and 2/20 are the only counts any p-value is now attached to; no
sentence implies 32/32 or 0/18 were formally significance-tested by a frozen artifact.

---

## 6. Aggregate 64% verification

Independently recomputed directly from all 240 rows (not from `EXPERIMENT_1_FINAL_RESULTS.md`):

- **agree = 32, disagree = 18, tie = 120, N/A (`llm_required`) = 70. Total = 240.**
- **Denominator 50 = agree (32) + disagree (18)** — i.e., only the conditions with a *defined*
  comparison (a strict, non-tied empirical winner *and* an R3 recommendation other than the
  excluded `llm_required` band).
- **Excluded rows and why:** 120 rows are ties (all 120 CLEAN rows — rules and retrieval are within
  the pre-registered $\delta=0.02$ practical-equivalence margin at every CLEAN condition, confirmed
  directly: 0 CLEAN rows have a non-blank `r3_agrees_with_empirical` flag). 70 rows are N/A because
  R3 itself recommends the excluded `llm_required` band (every VARIED row with `target_deterministic_share
  < 0.70` that also realizes below 0.70 lands here, plus all 70 CLEAN rows in the same nominal
  region — but those 70 CLEAN rows are already counted under "tie," not double-counted; the 70 N/A
  rows are specifically the VARIED `<0.70`-realized rows).
- **32/50 = 64.00%** — independently recomputed, exact match to the manuscript's stated 64.0%.
- **Exact two-sided binomial $p$ (vs. 0.5) on 32/50 = 0.064909**, rounding to the manuscript's
  stated $p=0.0649$ — exact match.
- **Wilson 95% CI on 32/50 = [0.5014, 0.7586]**, i.e. **[50.14%, 75.86%]** — exact match to the
  manuscript's stated Wilson CI.

**No discrepancy found.** The manuscript's Wilson CI and p-value correspond exactly to this precise
32/50 framing; nothing was changed.

---

## 7. Claim-strength findings

Searched `manuscript/main.tex` for every term in the task's list (`p=`, `significant`,
`significance`, `statistically significant`, `supports`, `strongly supports`, `contradicts`,
`confirms`, `proves`, `validates`, `causes`, `causal`, `independent`, `orthogonal`, `entirely`,
`governs`, `determines`) and inspected every occurrence connected to Experiment 1.

**Two genuine issues found and fixed in this pass (both re-attributions of already-sourced numbers,
not new computations, not new claims — consistent with the task's "do not invent a new statistical
test" instruction):**

1. **§5.6 "Statistical Interpretation"** previously read: *"Both individual realized-ADS bands are
   far more statistically significant than the flat aggregate ($p=1.9\times10^{-9}$ and
   $p=4.0\times10^{-4}$ respectively...)"* — ambiguous, because "realized-ADS bands" could be
   (mis)read as the 32/32/0/18 per-row counts introduced two subsections earlier, even though the
   very next sentence clarified the sample sizes belonged to "the by-target framing." **Fixed** to
   read: *"Both individual by-nominal-target bands are far more statistically significant than the
   flat aggregate ($p=1.9\times10^{-9}$ for the 30/30 retrieval-region band and $p=4.0\times10^{-4}$
   for the 2/20 rules-region band...). The sharper per-row realized-ADS bands (32/32 and 0/18,
   Section 5.4) are exceptionless but... are not independently paired with a frozen $p$-value
   anywhere in this paper's evidence base."*
2. **§6.3 "What the Original Hypothesis Got Right"** previously read: *"...one full realized-ADS
   band shows perfect, highly significant agreement"* — no specific number was misattached, but the
   unqualified phrase "highly significant" attached to an unnamed "realized-ADS band" (i.e., the
   32/32 count, introduced by context) reads as asserting a significance claim for that exact count
   without a frozen test backing it. **Fixed** to read: *"...one full realized-ADS band shows
   perfect, exceptionless agreement (32 of 32, Section 5.4), with the corresponding by-nominal-target
   count independently significant at $p=1.9\times10^{-9}$ (Section 5.6)."*

**Everything else checked and found correctly scoped (no change needed):**

- No sentence describes the experiment as causally *proving* that lexical/representation stability
  is the universal cause of mechanism ranking. The one causal-mechanism account in the paper (§6.4,
  "Why Consistency Predicts Difficulty but Not Ranking") is explicitly labeled "inferred from
  exhaustive but post-hoc inspection... not... a second, independently designed confirmatory
  experiment," never "proven" or "demonstrated."
- "Governed by"/"governs" (§5.3, §6.1, §6.7, Conclusion) is used only for the (manipulated lexical
  condition) → (empirical winner) relationship, which §5.3 explicitly justifies as licensed because
  the lexical condition is "a manipulated, controlled experimental factor, not merely an
  observational correlate" — matching `CONTRIBUTION_LOCK.md` §5's own statement that "the 'governed
  by' half rests on experimental, not merely correlational, evidence." It is never used for the
  (ADS blindness to surface form) → (outcome) causal account, which remains hedged as inferred
  throughout.
- Scope qualifiers ("in this generator," "in this experiment," "under the tested... perturbation
  model," "in both lexical conditions") are present at the sentence level everywhere a
  generalization risk exists — confirmed unchanged from the E3 draft audit's own finding.
- H1 = PARTIALLY\_SUPPORTED is stated explicitly and consistently (5 occurrences, §6.3, §7 header
  comment, §7.10 heading and body, Conclusion) — never softened toward "confirmed."
- Formulation #2 (the 6a/6b split plus the exact synthesis sentence) is preserved verbatim in
  substance throughout the Abstract, §1.6, §6.1, and the Conclusion. The manuscript does not use the
  internal `C2b` label anywhere (a deliberate E1/E2 architecture decision to keep internal Gate-4
  bookkeeping vocabulary out of reader-facing prose, not an omission) — its substance (the
  unconditional form falsified, the narrower conditional form supported) is present via the 6a/6b
  framing, which is the form `CONTRIBUTION_LOCK.md` §12 itself says the manuscript should converge
  on.

---

## 8. Figure-script audit

`manuscript/figures/generate_figures.py`, re-inspected line by line:

- **Reads only frozen evidence:** the only input path is `data/outputs/experiments/exp1/final/final_condition_results.csv`
  (`RESULTS_CSV`), opened once, read-only (`open(RESULTS_CSV, newline="", encoding="utf-8")`, no
  mode argument other than the implicit read mode — confirmed no `"w"`/`"a"` mode anywhere in the
  file, confirmed by direct grep).
- **No manually hard-coded scientific results:** grepped for every headline number
  (64.0, 32/50, 1.9e-9/1.9×10⁻⁹, 4.0e-4, 0.9031, 0.9597, 87.56, 91.2) — zero matches. The only
  hard-coded constants are `R3_LOW = 0.70` and `R3_HIGH = 0.90`, which are the frozen R3 threshold
  *configuration* (already fixed, versioned constants reused unchanged throughout the harness and
  the manuscript, not a "result").
- **Cannot silently generate numbers different from the manuscript:** every plotted quantity (F2's
  accuracy scatter, F3's per-band agreement rate, F4's accuracy-difference scatter) is computed at
  runtime directly from the same CSV rows the manuscript's own numbers were recomputed from in §2
  above, using the same band-definition logic (`ads_band()`, thresholds 0.70/0.90) — not a separate,
  divergent definition.
- **Deterministic:** no random-number generation, no sampling, no bootstrap resampling anywhere in
  the script (confirmed by reading the file in full) — identical output on every run given the same
  input CSV.
- **Does not modify any frozen artifact:** confirmed above (read-only open of `RESULTS_CSV`); all
  `savefig()` calls write only into `OUT_DIR` (`manuscript/figures/`), never into
  `data/outputs/experiments/exp1/`.
- **Does not introduce a new statistical analysis:** the script computes only counts, means, and
  simple differences (a bar chart of already-observed agreement rates, a scatter of already-observed
  accuracy values, a scatter of an already-observed accuracy difference) — no p-value, no
  correlation coefficient, no confidence interval, no hypothesis test is computed anywhere in this
  script. It is a visualization layer only, exactly as required.
- **Not executed in this environment:** confirmed again this pass (`python -c "import matplotlib"`
  → `ModuleNotFoundError`), consistent with the script's own docstring disclosure and the E3 draft
  audit's prior finding. Not run.

**No issues found.**

---

## 9. Auditor verdict

Invoked the independent `research-code-auditor` after completing §1–8 above, specifically to review
this numerical reconciliation (not to re-run the full E3 audit from scratch). Full independent
report: `research/E3_STATISTICAL_RECONCILIATION_AUDIT.md`.

**Verdict: 🟡 PASS\_WITH\_NOTES.**

The auditor independently recomputed every disputed number from the frozen CSV using its own
fresh, hand-rolled script (no import of `stats.py`), and every result matched this document's §2–6
exactly: realized-ADS-band 32/32 (100%) / 0/18 (0%); by-nominal-target 30/30 (100%) / 2/20 (10%);
$p=1.9\times10^{-9}$ mathematically belongs to 30/30 (not 32/32, which gives $4.66\times10^{-10}$);
$p=4.0\times10^{-4}$ belongs to 2/20 (not 0/18, which gives $7.63\times10^{-6}$); the 32/50=64.0%
aggregate, its Wilson CI, and its denominator breakdown (120 ties + 70 N/A = 190 excluded, verified
by direct row count). The auditor independently re-read every disputed-value occurrence in
`manuscript/main.tex` and confirmed no p-value is attached to 32/32 or 0/18 anywhere, and that
$1.9\times10^{-9}$/$4.0\times10^{-4}$ are always explicitly attached to 30/30/2/20 in the same
sentence or table row. `manuscript/figures/generate_figures.py` was independently re-confirmed
read-only, free of hardcoded results, free of any new statistical computation, deterministic, and
its non-execution (matplotlib absent) correctly disclosed. Git state confirmed no frozen artifact
was touched by this reconciliation pass.

Two non-blocking notes recorded by the auditor (neither requires a manuscript change):

1. The frozen `research/EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7 itself labels its table "VARIED
   sub-band," which is ambiguous with the per-row realized-ADS-band language used elsewhere in the
   same evidence base — plausibly the root cause of the original splice error. That document is
   frozen evidence and outside this pass's edit scope; the manuscript has already resolved the
   ambiguity correctly on its own side.
2. `research/PAPER_CONTRACT.md` §7's canonical-value list does not currently enumerate 30/30, 2/20,
   or the two p-values by name, even though the manuscript now relies on them explicitly. Worth
   adding for completeness in a future contract-maintenance pass; not a defect in the manuscript and
   not required for the E3 checkpoint.

---

## 10. Remaining issues

None block the E3 checkpoint. The two wording fixes in §7 (already applied to `manuscript/main.tex`)
and the auditor's two non-blocking notes above (§9) are the only findings from this reconciliation.
No frozen artifact was modified. No new statistical test was introduced into the manuscript. No
number was changed without first being traced to, and independently re-confirmed against, its
correct source in the frozen evidence.

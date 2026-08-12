# Experiment 1 Evidence Checkpoint

> Freezes the evidence produced by the frozen 240-condition final run. Every number in this
> document was independently recomputed from `data/outputs/experiments/exp1/final/final_condition_results.csv`
> during this checkpoint audit (not copied from `EXPERIMENT_1_FINAL_RESULTS.md`) and reconciled
> against it — see §11. No manuscript file was modified to produce this checkpoint.

---

## 1. Experiment objective

Test H1 (as reworded in `research/EXPERIMENT_1_REDESIGN_REVIEW.md` §2): a pre-specified
consistency-based decision rule (R3, thresholds 0.90/0.70 on realized train-only ADS) selects the
mechanism (`rules` vs. `retrieval`) that agrees with the empirically best-performing mechanism
more often than chance (50%).

## 2. Frozen design

Frozen at commit `3c6b581178aa7cd3598e112f96f1321d61d60aa9`. 6 target `deterministic_share` bands
× 2 lexical conditions (CLEAN / VARIED) × 20 seeds = 240 conditions. Rules and retrieval mechanisms
are isolated (bypass the shipped cascade), LLM excluded, winner determined by paired bootstrap
with a δ=0.02 practical-equivalence margin. Full design rationale:
`research/EXPERIMENT_1_REDESIGN_REVIEW.md`; calibration of P_TRANSFORM, ADS target bands, and
retrieval cutoff: `research/EXPERIMENT_1_CALIBRATION_REPORT.md`.

## 3. 240-condition matrix

Mechanically verified against `final_condition_results.csv` (240 rows) during this audit:

| target | lexical=False (seeds) | lexical=True (seeds) |
|---:|---:|---:|
| 0.00 | 20 | 20 |
| 0.20 | 20 | 20 |
| 0.30 | 20 | 20 |
| 0.50 | 20 | 20 |
| 0.75 | 20 | 20 |
| 1.00 | 20 | 20 |

12 cells × 20 seeds = 240. Every cell's seed set equals exactly `{31001, ..., 31020}`.

## 4. Completeness verification

| Check | Result |
|---|---|
| Total rows | 240 |
| Unique (seed, target, lexical) keys | 240 / 240 — 0 duplicates |
| Target values seen | exactly `{0.0, 0.2, 0.3, 0.5, 0.75, 1.0}` — no unexpected values |
| Lexical values seen | exactly `{False, True}` |
| Seeds seen | exactly `{31001..31020}` — 0 unexpected, 0 missing |
| Every (target, lexical) cell has exactly 20 seeds matching the frozen manifest | 12/12 cells OK |
| `status` field | `ok` in all 240 rows (0 failures) |

## 5. Frozen configuration — traced to code and artifacts, not memory

| Parameter | Frozen value | Traced to |
|---|---|---|
| P_TRANSFORM | 0.3 (VARIED) / 0.0 (CLEAN) | `run_final.py:43`; actual data confirms exactly these two (lexical, p_transform) pairs occur, no others |
| Retrieval cutoff | 75 | `run_final.py:44`; `final_condition_results.csv.retrieval_cutoff_used` is `75` in all 240 rows |
| Mechanisms | `classify_rules`, `classify_retrieval` only | `mechanisms.py` defines exactly these two; no LLM function exists in the file (explicit exclusion comment in the module docstring) |
| LLM | excluded | confirmed above; no LLM import/call anywhere in `run_final.py` |
| Winner rule | paired bootstrap, δ=0.02, 2000 resamples, α=0.05 | `run_final.py:122-126` calls `stats.paired_bootstrap_winner`; `final_bootstrap_results.csv` shows exactly one value each for `delta` (0.02), `bootstrap_resamples` (2000), `bootstrap_alpha` (0.05) across all 240 rows |
| ADS | train-only | `consistency.py:106`: `train_rows = [r for r in lines if split_of(r) == "train"]` computed before any aggregation |
| Target regions | 0.00, 0.20, 0.30, 0.50, 0.75, 1.00 | `run_final.py:41`; matches §3/§4 |
| Seeds per condition | 20 (31001-31020) | `run_final.py:45`; matches §3/§4 |
| Harness modules unmodified since freeze | `consistency.py`, `mechanisms.py`, `stats.py` | `git status --porcelain` on these three files returns empty — byte-identical to the frozen commit as of this audit |

`run_final.py` additionally hard-asserts (lines 50-54) `delta==0.02`, `cutoff==75`,
`p_transform==0.3`, `len(seeds)==20`, and the R3 thresholds — all assertions passed on the run that
produced this data (run did not crash).

## 6. Headline results (independently reconciled — see §11)

| Slice | agree | disagree | tie | N/A (llm_required) | n_defined | n_total | agreement rate | chance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Overall | 32 | 18 | 50 | 140 | 50 | 240 | 64.0% | 50% |
| CLEAN | 0 | 0 | 50 | 70 | 0 | 120 | undefined | 50% |
| VARIED | 32 | 18 | 0 | 70 | 50 | 120 | 64.0% | 50% |

Overall agreement rate 64.0% (32/50), Wilson 95% CI **[50.14%, 75.86%]**. Exact two-sided
binomial test against p=0.5 on the 32/50: **p = 0.0649** (not significant at α=0.05).

## 7. Band-specific results

| VARIED sub-band | agree | disagree | n_defined | rate | exact binomial p vs. 50% |
|---|---:|---:|---:|---:|---:|
| ADS 0.70–0.90 (targets 0.50, 0.75) | 30 | 0 | 30 | **100%** | 1.9×10⁻⁹ (highly significant, supports H1) |
| ADS ≥0.90 (target 1.00) | 2 | 18 | 20 | **10%** | 4.0×10⁻⁴ (highly significant, **contradicts** H1) |

Both bands are individually far more significant than the aggregate 64%/p=0.065 figure — the
aggregate is a near-cancellation of two large, opposite, real effects, not a single moderate
effect.

## 8. CLEAN vs. VARIED results

- **CLEAN**: rules and retrieval accuracy are within the δ=0.02 practical-equivalence margin at
  every one of the 6 targets (`final_summary.csv`: all 6 CLEAN rows show `n_ties=20`). Zero
  conditions produce a defined empirical winner. H1 cannot be evaluated in this condition — not
  because it fails, but because the premise (a distinguishable empirical winner) never obtains.
- **VARIED**: retrieval wins on raw accuracy in all 120 conditions (never rules, never tie).
  Whether that win *agrees with R3's selection* depends entirely on which ADS band: yes in the
  0.70–0.90 band (R3 itself recommends retrieval there), no in the ≥0.90 band (R3 recommends
  rules, but retrieval still wins due to noise robustness).

## 9. H1 verdict

**PARTIALLY_SUPPORTED.**

This is not reducible to the 64% aggregate figure. Per §6-8:

- **Overall agreement (64.0%, n=50)**: directionally consistent with H1, but the exact binomial
  test does not clear conventional significance (p=0.065) and the Wilson CI lower bound sits
  essentially on the chance baseline (50.14%). Aggregated alone, this is **inconclusive**.
- **ADS-band effect**: the aggregate figure is the arithmetic average of two individually
  highly-significant, opposite effects — R3 is essentially always right in the 0.70-0.90 band and
  essentially always wrong in the ≥0.90 band. Collapsing these into one number obscures both.
- **CLEAN vs. VARIED**: the CLEAN condition provides **zero** evidence either way (no defined
  comparisons exist). All measurable H1 evidence comes from the VARIED condition.
- **The high-ADS reversal** (§7, ≥0.90 band, 10% agreement) is itself a highly significant
  effect (p=4.0×10⁻⁴) and is evidence *against* R3's core assumption in exactly the band where R3
  is most confident (highest realized consistency → strongest recommendation for `rules`).

Given a band that strongly and significantly supports H1, a band that strongly and significantly
contradicts it, a condition (CLEAN) that is entirely uninformative, and an aggregate statistic
that does not itself reach significance, the honest verdict is **PARTIALLY_SUPPORTED**, not
SUPPORTED and not simply INCONCLUSIVE — the sub-band evidence is too strong in both directions to
call this "no evidence either way."

## 10. Limitations

- Single synthetic generator family; 240 conditions are not independent replications of an
  external population, only of the seeded RNG.
- n_defined is small in the two informative bands (30 and 20) — enough for the binomial tests
  above to be decisive, but not enough to further subdivide.
- δ=0.02 (frozen at Gate 3) is the reason CLEAN is entirely uninformative; a different (also
  legitimate) δ could change which conditions are "tied" vs. "defined." Not re-tuned here.
- R3's thresholds (0.90/0.70) were not re-tuned against this outcome data — the reversal at ≥0.90
  is a property of those pre-existing thresholds interacting with lexical noise, not something
  selected post hoc.
- LLM excluded; this checkpoint says nothing about LLM performance in the band where retrieval
  currently wins.
- Retrieval coverage is 1.0 in all 240 conditions (never abstains at cutoff=75); rules coverage is
  always <1.0. This asymmetry is part of why retrieval wins under noise, not an artifact.

## 11. Integrity checks

| Check | Result |
|---|---|
| Realized ADS computed from training data only | Verified in code: `consistency.py:106` filters to `split_of(r)=="train"` before any aggregation |
| Test account labels not used to select mechanism | Verified in code: `stats.r3_rule_selection(realized_det_pct)` takes only the train-only ADS scalar; no test-set data reaches it |
| Retrieval cutoff not tuned during the final run | Verified: single hardcoded constant (75) used in all 240 conditions, sourced from the pre-existing Gate 2 calibration, not varied or reselected here |
| No mechanism-specific tuning after seeing final results | Harness files (`consistency.py`, `mechanisms.py`, `stats.py`) are git-clean (byte-identical to the frozen commit) as of this audit, and this session made no edits to them after the run completed. Cannot rule out edit-then-revert activity entirely outside this session's visibility, but there is no evidence of it in the working tree or file history. |
| No condition manually rerun for an interesting result | The full script was run twice at whole-run granularity (first attempt interrupted by session compaction before producing any output rows; second attempt completed cleanly). No selective per-condition reruns occurred — `run_final.py` executes all 240 in one uninterrupted loop with no early-stop or retry logic. All 5 post-loop CSV/JSON artifacts share an identical write timestamp cluster (10:12:11, within ~21ms of each other), consistent with a single atomic batch write at the end of one pass, not an accumulation across multiple runs. |
| No result rows manually edited | All rows within each output file share the file's single write timestamp; no editor backup/temp files (`.bak`/`.swp`/`.orig`/`.tmp`) found in the output directory |
| Reconciliation of headline numbers | Independently recomputed via `stats.selection_agreement()` directly from `final_condition_results.csv` during this audit — see §6-7. All numbers matched `EXPERIMENT_1_FINAL_RESULTS.md` exactly; no discrepancy found. |
| Research-safety scan | No API keys / secrets / credentials / bearer tokens / private-key blocks, no local Windows paths or usernames, no signed/presigned URL patterns found in any of `data/outputs/experiments/exp1/final/`, `research/EXPERIMENT_1_FINAL_RESULTS.md`, or `scripts/experiments/exp1/run_final.py` |
| Manuscript files untouched | `git status`/`git diff` on `README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md` show zero changes |

## 12. Reproducibility

```
python scripts/experiments/exp1/run_final.py
```
Deterministic given the frozen constants (seeds 31001-31020, targets, cutoff=75,
P_TRANSFORM=0.3, per-call `random.Random(seed)` isolation). Raw artifacts:
`data/outputs/experiments/exp1/final/` (see `EXPERIMENT_1_FINAL_RESULTS.md` §11 for the full
per-file manifest and evidence-bearing vs. intermediate classification).

## 13. Freeze statement

This checkpoint freezes the experimental evidence. No manuscript conclusions have been rewritten
from these results.

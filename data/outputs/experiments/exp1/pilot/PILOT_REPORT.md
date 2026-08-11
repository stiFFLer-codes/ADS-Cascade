# Experiment 1 — PILOT REPORT

**PILOT — NOT FINAL EVIDENCE. Not an H1 result. 3 seeds only. Do not cite.**

Produced under the Phase D "harness + pilot only" approval. Verifies the harness described in
`research/EXPERIMENT_1_REDESIGN_REVIEW.md`; does not test H1.

## Scope run

- Bands (target `deterministic_share`): 0.60, 0.90, 0.99
- Lexical conditions: CLEAN, VARIED (`P_TRANSFORM = 0.3`, frozen via outcome-independent selection,
  see `p_transform_selection.json`)
- Seeds: 101, 102, 103
- 18 conditions total, all rules-only and retrieval-only mechanisms evaluated independently

## Acceptance criteria (§17 of the redesign review)

| # | Criterion | Result |
|---|---|---|
| 1 | Independent seeds produce independent runs | PASS — `test_generator_rng.py` (4/4), plus distinct realized ADS per seed within a band |
| 2 | Target and realized ADS recorded | PASS — both columns in `pilot_conditions.csv` |
| 3 | ADS is train-only | PASS — `consistency.realized_ads()` filters to train before any computation |
| 4 | Train/test leakage test passes | PASS — `test_leakage.py` (2/2), including the converse sanity check |
| 5 | Lexical transformation behaves as intended | PASS — semantic identity preserved, reproducible, moderate severity (mean WRatio ≈85, see `p_transform_selection.json`) |
| 6 | Retrieval receives a genuine surface-form challenge | PASS — mechanism divergence jumps from ~4-5% (CLEAN) to ~22-25% (VARIED) at every band; retrieval accuracy clears rules accuracy by 10-17 points under VARIED |
| 7 | Rules/retrieval evaluated independently | PASS — `test_mechanisms.py` (5/5) |
| 8 | Metrics are correct | PASS — `test_stats.py` (7/7) |
| 9 | Outputs are reproducible | PASS — deterministic generation, no live API calls in the primary comparison |
| 10 | Runtime acceptable | PASS — 40.5s / 18 conditions ≈ 2.25s/condition → ~9 min projected for the full 6×2×20=240-condition sweep |

**All 10 criteria pass.**

## Notable pilot finding (not an H1 result — a harness-correctness finding)

The first pilot run surfaced a real bug: `consistency.py` originally grouped by the surface string
(`normalized_product`) when computing realized ADS. Under the VARIED lexical condition this
fragmented a single true product into several low-count, trivially-self-consistent surface-form
"pseudo-products," artificially *inflating* realized ADS — e.g. target=0.60 realized ~0.87-0.90
under VARIED vs ~0.71-0.76 under CLEAN, at matched seeds. Fixed by grouping on `product_code` (the
stable ground-truth identity) instead. After the fix, realized ADS is now identical between CLEAN
and VARIED at every matched (seed, band) pair, confirming the two factors are properly orthogonal
again. See the code comment in `consistency.py::compute_det_pct` for the full explanation.

## Illustrative pattern (NOT an H1 verdict — 3 seeds, informational only)

- Every CLEAN-condition comparison came out a **tie** (9/9) — rules and retrieval are statistically
  indistinguishable when there is no surface noise to bridge, exactly as the redesign review's §9
  concern anticipated. This confirms the CLEAN condition is doing its intended job as a diagnostic
  control, and that the VARIED condition is necessary for this experiment to have any power at all.
- Under VARIED, retrieval beat rules in 8 of 9 conditions, with one case where the R3 rule
  (realized ADS ≥ 0.90 → "rules") disagreed with the empirical winner (retrieval, decisively).
- None of this is evidence for or against H1. It is reported here only to confirm the harness
  produces mechanically sensible, non-degenerate output.

## Realized-vs-target ADS compression (flagged for the frozen-run design, not fixed here)

Realized ADS did not spread out as much as the three target bands suggest: target 0.60 realized
~0.71-00.76; target 0.90 realized ~0.85-0.88; target 0.99 realized ~0.88-0.90. The top two bands
compress toward a similar realized range. This is consistent with the `CROSS_COMPANY_ALIGN=0.695`
ceiling effect flagged in `research/EXPERIMENT_1_REDESIGN_REVIEW.md` §4/§7. The frozen run should
measure the realized-ADS curve across all 6 target bands before finalizing which target values to
use — this is a generation-diagnostic tuning question (does the target grid actually cover a useful
spread of realized values), not a mechanism-accuracy-based one, and is listed as a remaining risk
in the session's final report.

## Retrieval-cutoff calibration (mechanics check only, NOT the frozen threshold)

Ran the calibration protocol end-to-end on its own dedicated seed (9001, det_share=0.80) to confirm
it works: chose cutoff=90 (all candidates had 100% coverage on this pilot slice; accuracy was flat
70-80, rose slightly at 85/90). **This is not the frozen calibration** — the real one needs its own
author-approved protocol per §23.2 of the redesign review before the final run.

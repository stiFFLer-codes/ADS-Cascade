# Phase D Checkpoint — Experiment 1 Harness, Pilot, Calibration

> Checkpoint of Phase D's pre-frozen-experiment state. Read this before resuming Phase D in a new
> session. Companion documents: `research/EXPERIMENT_1_REDESIGN_REVIEW.md` (the frozen design) and
> `research/EXPERIMENT_1_CALIBRATION_REPORT.md` (Gates 1-3 closure). This document does not
> duplicate their content — it records what state the repository is in and what remains.

---

## 1. Phase D purpose

Test H1 — the sole surviving, PROMISING research contribution from Phase C's stress test
(`research/contribution_stress_test.md`): *"Under controlled synthetic conditions, higher historical
decision consistency will be associated with predictable changes in the relative performance of
classification mechanisms, such that the mechanism selected by a pre-specified consistency-based
decision rule will agree with the empirically best-performing mechanism more often than chance."*
H2 and H3 are explicitly out of scope for the current Phase D pass.

## 2. Work completed

1. Repository/implementation review against the original `experimental_design.md` (gap analysis,
   methodological concerns, LLM-validity concerns) — no code written.
2. A revised, tightened experimental design (`EXPERIMENT_1_REDESIGN_REVIEW.md`): scoped IV, retrieval
   mechanism naming, LLM exclusion rationale, mechanism-isolation architecture, calibration
   protocol, primary/secondary metrics, falsification criteria, reproducibility requirements.
3. Harness implementation (generator fix, mechanism isolation, statistics) — §3 below.
4. A pilot run (3 seeds × 3 bands × 2 lexical conditions = 18 conditions) verifying harness mechanics
   — not evidence for H1.
5. Three calibration gates closed (`EXPERIMENT_1_CALIBRATION_REPORT.md`): mechanism-blind ADS region
   selection, dedicated retrieval-cutoff calibration, and a frozen empirical-winner/tie/CI
   definition.

**No final ≥20-seed experiment has been executed.**

## 3. Harness architecture

- `scripts/00_generate_synthetic.py` (modified, not forked) — `random.seed(42)` at module scope
  replaced with a per-call `random.Random(seed)` threaded through every generation function;
  `gen_dataset()`/`main()` gained `seed`, `deterministic_share`, `lexical_variation`, `p_transform`
  parameters, all defaulting to today's values. Default-call output verified byte-identical to the
  currently-committed `data/outputs/invoice_lines_all_companies.csv`.
- `scripts/experiments/exp1/` (new package):
  - `_loader.py` — shared import plumbing (loads the digit-prefixed generator module via
    `importlib`, registers `scripts/phase2` on `sys.path` for `p2lib`).
  - `consistency.py` — train-only realized-ADS computation (`realized_ads()`), the harness's single
    entrypoint for the primary independent variable.
  - `mechanisms.py` — isolated `classify_rules()` / `classify_retrieval()`, built on the existing
    `p2lib/kb.py` / `p2lib/retrieval.py` primitives; no LLM interface (excluded, §11).
  - `lexical_diagnostics.py` — outcome-independent diagnostics (surface-disruption rate,
    transform-type balance, retrieval-challenge severity via rapidfuzz `WRatio`, semantic-identity
    check) used to select `P_TRANSFORM` without ever reading `account_id`.
  - `stats.py` — stdlib-only bootstrap statistics: `whole_set_accuracy`, `coverage`,
    `r3_rule_selection`, `selection_agreement`, and the frozen `paired_bootstrap_winner` /
    `paired_bootstrap_diff_ci` (replacing an earlier CI-overlap heuristic that was statistically
    wrong for this paired design — see §5).
  - `select_p_transform.py`, `calibrate_ads.py`, `calibrate_retrieval_cutoff.py`, `run_pilot.py` —
    orchestrator scripts, each producing committed CSV/JSON artifacts under `data/outputs/`.
  - 5 test files (`test_generator_rng.py`, `test_leakage.py`, `test_mechanisms.py`,
    `test_lexical_transform.py`, `test_stats.py`) plus `scripts/test_00_generate_synthetic.py` — 37
    assert-based self-checks total, matching this repository's existing lightweight test convention
    (no framework). All passing as of this checkpoint.

## 4. Pilot status

3 seeds (101-103) × 3 bands (0.60, 0.90, 0.99 target) × 2 lexical conditions = 18 conditions.
All 10 pre-registered acceptance criteria passed (`data/outputs/experiments/exp1/pilot/PILOT_REPORT.md`).
Runtime: ~2.25s/condition, projecting ~9 minutes for the eventual 240-condition frozen sweep.
**Explicitly labeled PILOT — NOT FINAL EVIDENCE everywhere it appears; not cited as an H1 result.**

## 5. Bugs discovered and fixed (by the pilot and calibration process itself)

1. **Lexical case-transform neutralization.** The transform was originally applied to the raw
   uppercase product name and then unconditionally lowercased when building `normalized_product` —
   silently erasing the "case variation" transform type's entire effect on the field mechanisms
   actually match on. Fixed by applying the transform to the already-lowercased base string instead.
2. **Realized-ADS contamination by the lexical-noise factor.** `consistency.py` originally grouped
   the ADS aggregation by the surface string (`normalized_product`), which under lexical variation
   fragmented one true product into several trivially-self-consistent surface-form pseudo-products,
   artificially inflating realized ADS in the VARIED condition relative to CLEAN at the same target.
   Fixed by grouping on the stable `product_code` instead. Verified afterward: realized ADS is now
   identical between CLEAN and VARIED at every matched (seed, band) pair (Gate 1's 9-point spot
   check, all exact matches).
3. **CI-overlap winner rule was statistically wrong for this design.** `empirical_winner()` compared
   two independently-computed bootstrap CIs for overlap; since rules and retrieval are scored on the
   identical held-out test lines within a condition, their outcomes are correlated, not independent.
   Replaced (not just justified) with `paired_bootstrap_winner()` — a paired bootstrap on the
   accuracy difference. The old function is retained, marked superseded, only because the
   already-approved pilot output depends on it and was not re-run.

## 6. ADS calibration findings (Gate 1)

Mechanism-blind sweep: 17 target values × 10 seeds (170 conditions, 0 failures), CLEAN condition,
plus a 9-point VARIED spot-check (all exact matches, confirming fix #2 above holds across the full
grid). Full table: `data/outputs/experiments/exp1/calibration/ads_calibration_raw.csv` /
`ads_calibration_summary.json`.

- Realized ADS descends smoothly to ~0.49 at target=0.00 (floor has real headroom the original
  [0.60, 0.99] design left unused).
- Realized ADS is **structurally capped near ~0.907-0.908** — target=0.99 and target=1.00 realize to
  essentially the same value. No generation parameter can push it higher.
- Root cause (diagnosed by reading the generator, not by running mechanisms): `CROSS_COMPANY_ALIGN
  =0.695` — the actual production-observed cross-company consistency figure, not an arbitrary
  synthetic constant — caps the ~12% multi-company share of the catalog regardless of
  `deterministic_share`. Recommendation: do not tune this constant to raise the ceiling; report it as
  a substantive finding (production-realistic cross-company disagreement structurally bounds
  achievable dataset-level determinism, plausibly explaining why production's own R3 decision sits so
  close to its own 0.90 threshold).
- Mechanism-blind furthest-point selection recommends final regions:
  `[0.00, 0.20, 0.30, 0.50, 0.75, 1.00]` (target) → realized means
  **`[0.4859, 0.5645, 0.6156, 0.6977, 0.8015, 0.9076]`**.

## 7. Retrieval calibration findings (Gate 2)

5 dedicated seeds (50001-50005), disjoint from every pilot and ADS-calibration seed. Calibration
condition: `deterministic_share=0.80`, VARIED lexical (`P_TRANSFORM=0.3`) — chosen because the pilot
showed CLEAN-condition rules and retrieval tie regardless of cutoff. Criterion: **product-identity
hit rate** (does the top fuzzy match resolve to the same true `product_code`?) — explicitly *not*
classification accuracy against `account_id`, per the constraint against using mechanism accuracy to
calibrate thresholds. Candidates `{60,65,70,75,80,85,90,95}`; selected via max hit-rate subject to
coverage ≥0.30, ties within 0.01 broken toward the highest (most conservative) cutoff.

**Selected cutoff = 75** (hit-rate 0.9116, coverage 1.0000) — supersedes the pilot's mechanics-check
value (90), which was never meant to be frozen.

## 8. Final proposed ADS regions

```
target -> realized mean
0.00 -> 0.4859
0.20 -> 0.5645
0.30 -> 0.6156
0.50 -> 0.6977   (~0.70 R3 boundary)
0.75 -> 0.8015
1.00 -> 0.9076   (~0.90 R3 boundary, at the achievable ceiling — see §6)
```

## 9. Retrieval cutoff

**`RETRIEVAL_CUTOFF = 75`** (rapidfuzz `WRatio` scale), frozen per Gate 2 (§7).

## 10. Winner definition

**Paired bootstrap on the accuracy difference (`rules_accuracy − retrieval_accuracy`)**, 2,000
resamples, 95% percentile interval, resampling shared test-line indices so both mechanisms are
scored on the identical resampled set each iteration. **Practical-equivalence margin δ = 0.02**
(whole-set-accuracy points), anchored to this repository's own precedent for what it has previously
treated as a meaningful accuracy gap. Rules wins iff the entire CI lies above +δ; retrieval wins iff
entirely below −δ; otherwise **tie**. Implemented as `stats.paired_bootstrap_winner()`, unit-tested
(4 tests, `test_stats.py`).

## 11. LLM exclusion rationale

Excluded from the primary H1 comparison. The synthetic product string's only human-readable token
(the category word, e.g. `"FUEL"`) is assigned in `gen_products()` **independently** of the account
pool actually sampled for that product — there is no code path making a category word predictive of
the true label. An LLM reasoning "fuel → fuel-expense account" would be reasoning from a regularity
the generator does not implement; including it risks a confound (an accuracy pattern driven by the
LLM's real-world semantic priors colliding with an unrelated random assignment) unrelated to the
independent variable, not just a weak result. The `LLM_REQUIRED` band (`det_pct < 0.70`) has also
never been empirically triggered by either the production or synthetic system in this repository's
history (`RESEARCH_AUDIT.md` finding A4) — excluding it removes an already-untested region, not a
validated one. Full reasoning: `EXPERIMENT_1_REDESIGN_REVIEW.md` §10.

## 12. Current final-experiment configuration (proposed, not executed)

```python
FINAL_TARGETS = [0.00, 0.20, 0.30, 0.50, 0.75, 1.00]   # realized means: see §8
LEXICAL_CONDITIONS = [False, True]
P_TRANSFORM = 0.3                  # frozen, outcome-independent, pilot session
RETRIEVAL_CUTOFF = 75              # frozen, Gate 2
PRIMARY_METRIC = "whole_set_accuracy"
WINNER_RULE = "paired_bootstrap_winner"
PRACTICAL_EQUIVALENCE_DELTA = 0.02
BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_ALPHA = 0.05
MECHANISMS = ["rules_only", "retrieval_only"]   # LLM excluded
N_SEEDS_PER_CONDITION = 20          # minimum
# 6 regions x 2 lexical x >=20 seeds = >=240 conditions
```

## 13. What remains unresolved

- **Seed-manifest generation rule** — how the ≥20 seeds per condition are chosen (a simple
  deterministic range vs. a hash-derived list). Carried over unresolved from
  `EXPERIMENT_1_REDESIGN_REVIEW.md` §23.4; the only open item blocking the final run per
  `EXPERIMENT_1_CALIBRATION_REPORT.md` §13's GO recommendation.
- No region reaches a comfortable-margin "deep rules-first" condition (§6/§8) — an accepted,
  documented limitation, not something to re-tune.
- The retrieval cutoff was calibrated at one representative band/lexical condition, not
  re-validated at each of the 6 final regions individually (deliberate, to avoid an unequal-tuning
  confound — `EXPERIMENT_1_CALIBRATION_REPORT.md` §11).
- The 240-condition frozen run has not been separately timed with the final regions/cutoff (only
  extrapolated from the pilot and from the calibration sweeps, both of which ran in well under a
  minute).

## 14. No final ≥20-seed experiment has been executed.

## 15. Next gate

**Human approval before final experiment execution** — specifically: (a) resolve the seed-manifest
rule (§13), and (b) explicit sign-off to run the frozen ≥20-seed sweep. No further methodology
changes, no manuscript changes, and no new experiments are in scope until that approval is given.

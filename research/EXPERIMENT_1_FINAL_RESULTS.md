# Experiment 1 Final Results — H1

> Reports the frozen, 240-condition final run of Experiment 1. Methodology frozen at commit
> `3c6b581178aa7cd3598e112f96f1321d61d60aa9`
> (`research/EXPERIMENT_1_REDESIGN_REVIEW.md` + `research/EXPERIMENT_1_CALIBRATION_REPORT.md`).
> No threshold, mechanism, retrieval-cutoff, winner-definition, or generator change was made to
> produce these results — `scripts/experiments/exp1/run_final.py` is orchestration only and calls
> the existing, unmodified `consistency.py` / `mechanisms.py` / `stats.py`. This document does not
> modify the manuscript, README, or METHODOLOGY, and does not open Phase E.
>
> Raw artifacts: `data/outputs/experiments/exp1/final/`. This report has **not** been staged,
> committed, or pushed — pending review of the evidence below.

---

## 1. Executive summary

H1 (reworded): *a pre-specified consistency-based decision rule (R3) will select the mechanism
(rules vs. retrieval) that agrees with the empirically best-performing mechanism more often than
chance.*

Across all 240 conditions, R3's selection agreed with the empirical winner in **32/50 = 64.0%**
of the conditions where agreement is even definable (chance baseline 50%; Wilson 95% CI
**[50.1%, 75.9%]**) — the rest of the 240 conditions are either N/A (R3 selected the excluded
`llm_required` band) or ties (rules and retrieval were within the pre-registered δ=0.02 practical-
equivalence margin, so there is no single "empirical winner" to agree or disagree with).

That 64% headline number is **not uniform** — it is the average of two opposite behaviors:

- At mid-high realized ADS (targets 0.5, 0.75) under lexical noise, R3 agreed with the empirical
  winner **100% of the time** (30/30 defined conditions).
- At the highest realized ADS band (target 1.00) under lexical noise, R3 agreed only **10% of the
  time** (2/20) — R3 selects `rules` because consistency is high, but the empirically best
  mechanism is `retrieval`, because lexical noise breaks exact-string rule matching regardless of
  how consistent the underlying account assignment is.

Under the **clean** (no lexical noise) lexical condition, rules and retrieval were *tied* (within
δ=0.02) in every single one of the 120 CLEAN conditions where R3 selected a defined mechanism —
there is no discriminating signal at all in that condition; `agreement_rate` is undefined
(`None`), not zero. See §5-6.

## 2. Run provenance and integrity checks

**First attempt** (background task, prior session) was interrupted mid-run by a session
compaction event: it wrote the pre-loop artifacts (`final_frozen_config.json`,
`final_seed_manifest.csv`, both correct and complete) but produced zero stdout/stderr and no
post-loop artifacts, consistent with external termination rather than a script defect. No code was
changed. It was re-run unmodified with unbuffered output for a clean audit trail.

**Second attempt** (this report): completed cleanly.

```
DONE. 240/240 conditions succeeded, 0 failed, 1093.6s total (4.557s/condition)
```

Automated integrity checks performed against `final_condition_results.csv` post-run:

| Check | Result |
|---|---|
| All 240 (seed, target, lexical) triples unique, no duplicates | ✅ 240/240 unique |
| 0 failed conditions | ✅ `final_run_metadata.json`: `failed_conditions: 0` |
| Realized ADS invariant to lexical condition at matched (target, seed) | ✅ exact match, all 6 targets — `realized_ads_mean`/`std` identical between CLEAN and VARIED in `final_summary.csv` (e.g. target=0.75: 0.7973/0.0105 both conditions) |
| Realized ADS consistent with Gate-1 calibration curve (different seed pool, same targets) | ✅ within 0.1-0.6pp of the Gate-1 means at every target |
| No NaN / degenerate accuracy values | ✅ `rules_acc` ∈ [0.474, 0.970], `retrieval_acc` ∈ [0.601, 0.967] |
| `retrieval_coverage` | 1.0 in all 240 conditions (retrieval, primary not fallback, never abstains at cutoff=75) |
| `rules_coverage` | < 1.0 in all 240 conditions (rules abstains whenever no exact match; range not degenerate) |
| Frozen-config assertions (`run_final.py` lines 50-54) | ✅ all passed at both run attempts (δ=0.02, cutoff=75, P_TRANSFORM=0.3, 20 seeds, R3 thresholds 0.90/0.70) |
| Full harness test suite (37 tests, 8 files) | ✅ all pass, re-run after the final data was produced |

Dataset scale per condition: 4,214–12,484 train lines, 1,153–3,767 test lines, 683–889 distinct
train products. 430,324 test-line classifications performed in total across the sweep (240
conditions × 2 mechanisms).

## 3. Frozen configuration (recap)

| Parameter | Value |
|---|---|
| Targets (`deterministic_share`) | 0.00, 0.20, 0.30, 0.50, 0.75, 1.00 |
| Lexical conditions | CLEAN (`False`), VARIED (`True`, P_TRANSFORM=0.3) |
| Seeds | 31001–31020 (20 seeds, identical set across every condition) |
| Retrieval cutoff | 75 (Gate 2) |
| R3 thresholds | rules ≥ 0.90, retrieval ≥ 0.70, else `llm_required` |
| Winner rule | `paired_bootstrap_winner`, 2000 resamples, α=0.05, δ=0.02 (Gate 3) |
| Primary metric | whole-set accuracy (abstention counts as incorrect) |
| LLM | excluded (§9 of the redesign review) |
| Total conditions | 6 targets × 2 lexical × 20 seeds = 240 |

## 4. Primary results table

From `final_summary.csv` (aggregated by target × lexical, n=20 seeds per row):

| target | lexical | realized ADS (mean±std) | rules acc | retrieval acc | rules wins | retrieval wins | ties | R3 selects (mode) |
|---:|:---:|---:|---:|---:|---:|---:|---:|:---|
| 0.00 | CLEAN  | 0.479 ± 0.024 | 0.690 | 0.686 | 0 | 0 | 20 | llm_required |
| 0.00 | VARIED | 0.479 ± 0.024 | 0.506 | 0.631 | 0 | 20 | 0 | llm_required |
| 0.20 | CLEAN  | 0.570 ± 0.025 | 0.735 | 0.731 | 0 | 0 | 20 | llm_required |
| 0.20 | VARIED | 0.570 ± 0.025 | 0.549 | 0.682 | 0 | 20 | 0 | llm_required |
| 0.30 | CLEAN  | 0.613 ± 0.022 | 0.762 | 0.757 | 0 | 0 | 20 | llm_required |
| 0.30 | VARIED | 0.613 ± 0.022 | 0.560 | 0.706 | 0 | 20 | 0 | llm_required |
| 0.50 | CLEAN  | 0.696 ± 0.019 | 0.821 | 0.816 | 0 | 0 | 20 | mixed (10 llm_required / 10 retrieval) |
| 0.50 | VARIED | 0.696 ± 0.019 | 0.610 | 0.765 | 0 | 20 | 0 | mixed (10 llm_required / 10 retrieval) |
| 0.75 | CLEAN  | 0.797 ± 0.011 | 0.896 | 0.891 | 0 | 0 | 20 | retrieval |
| 0.75 | VARIED | 0.797 ± 0.011 | 0.670 | 0.844 | 0 | 20 | 0 | retrieval |
| 1.00 | CLEAN  | 0.908 ± 0.009 | 0.953 | 0.947 | 0 | 0 | 20 | rules |
| 1.00 | VARIED | 0.908 ± 0.009 | 0.714 | 0.897 | 0 | 20 | 0 | rules |

Two things stand out immediately, independent of R3 at all:

- **Under VARIED, retrieval wins on raw accuracy in every single one of the 120 conditions**,
  across the entire realized-ADS range from 0.48 to 0.91. Rules accuracy drops sharply under
  lexical noise (e.g. 0.953 → 0.714 at target=1.00) while retrieval degrades much less
  (0.947 → 0.897) — exactly what fuzzy matching is for.
- **Under CLEAN, rules and retrieval are statistically tied at every single target** (all
  differences are within the δ=0.02 practical-equivalence margin) — there is no accuracy
  advantage to either mechanism when there is no lexical noise for retrieval to be robust to.

## 5. Primary H1 analysis: selection agreement vs. chance

Computed via the existing, unmodified `stats.selection_agreement()` over all 240 conditions.

| Slice | agree | disagree | tie | N/A (llm_required) | n_defined | n_total | agreement rate | chance baseline |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Overall** | 32 | 18 | 50 | 140 | 50 | 240 | **64.0%** | 50% |
| CLEAN | 0 | 0 | 50 | 70 | **0** | 120 | **undefined** | 50% |
| VARIED | 32 | 18 | 0 | 70 | 50 | 120 | **64.0%** | 50% |

The entire H1 signal comes from the VARIED condition — CLEAN produces zero conditions where R3's
selection can be checked against a defined empirical winner, because rules and retrieval are
always tied there. Restricting to VARIED (n_defined=50), the Wilson 95% CI on the observed
64.0% agreement rate is **[50.1%, 75.9%]** — the lower bound sits essentially on top of the 50%
chance baseline. This is directionally consistent with H1 (point estimate above chance) but weak:
the interval only barely excludes 50%, and it excludes it only because of rounding at the third
decimal.

### Per-target breakdown, VARIED only (this is where the 64% average is actually coming from)

| target | agree | disagree | n_defined | agreement rate |
|---:|---:|---:|---:|---:|
| 0.00 | 0 | 0 | 0 | N/A (all `llm_required`) |
| 0.20 | 0 | 0 | 0 | N/A (all `llm_required`) |
| 0.30 | 0 | 0 | 0 | N/A (all `llm_required`) |
| 0.50 | 10 | 0 | 10 | **100%** |
| 0.75 | 20 | 0 | 20 | **100%** |
| 1.00 | 2 | 18 | 20 | **10%** |

## 6. Key finding: R3 agreement is not monotonic in ADS — it reverses at the high end under noise

This is the substantive result of the run, and it directly instantiates the concern the redesign
review raised about conflating "high historical consistency" with "rules is the right mechanism."

- In the **retrieval band** (realized ADS 0.70–0.90, R3 selects `retrieval`), R3 agrees with the
  empirical winner **100%** of the time under lexical noise (30/30 defined conditions across
  targets 0.50 and 0.75). This is the part of H1 that holds cleanly.
- In the **rules band** (realized ADS ≥ 0.90, R3 selects `rules`), R3 agrees only **10%** of the
  time (2/20) under lexical noise. High historical account-assignment consistency does not imply
  that an exact-match rules mechanism will win empirically once the *surface form* of the product
  string is noisy — retrieval's fuzzy matching wins on accuracy (0.897 vs. 0.714) regardless of how
  deterministic the underlying account mapping is.

ADS (realized decision consistency) and lexical-surface robustness are two different, orthogonal
properties of the data. R3 is a function of ADS alone. It predicts the right mechanism well when
the true tie-breaker (surface noise) happens to favor retrieval anyway (bands 0.50, 0.75), and
predicts poorly in the one band (≥0.90) where its own recommended mechanism (rules) is the one
that surface noise specifically defeats.

## 7. Falsification criteria

The pre-registered falsification framing (redesign review, negative-result handling) treats "R3
selection is not more accurate than chance" as a valid, reportable outcome rather than something
to explain away. Applying that here:

- H1 is **not falsified** — the point estimate (64.0%) is above the 50% chance baseline in the
  only slice where agreement is measurable (VARIED), and two of three defined ADS bands show
  perfect agreement.
- H1 is **not cleanly confirmed** either — the aggregate CI barely clears chance, the CLEAN
  condition contributes zero discriminating evidence, and the one band where R3 fails (≥0.90) is
  the specific band the R3 rule itself is most confident in (highest-consistency → `rules`).
- The correct characterization is **effect modification**: R3's validity depends on a factor
  (surface/lexical noise) that the current H1 wording and the R3 rule itself do not parameterize.
  A cleaner test of the underlying idea would need either (a) an R3 variant that also conditions on
  a noise/robustness signal, or (b) restricting the claim to "R3 predicts well conditional on low
  lexical noise," which this dataset does not support either (CLEAN gives no signal because
  nothing loses there).

## 8. Critical interpretation rule (explicit statement, per protocol)

**Higher realized ADS does not mean rules is automatically the better mechanism.** ADS measures
how consistently a product has historically mapped to one account — a property of the *label*
distribution. It says nothing about how much surface-string variation the *matching text* will
exhibit at inference time. §4 and §6 show these are separable: at ADS≈0.91 with lexical noise
present, retrieval outperforms rules by 18 points of whole-set accuracy despite rules being the
R3-recommended mechanism precisely because ADS is high. Any downstream reading of this experiment
that shortcuts to "high ADS ⇒ pick rules" is not supported by this data; the correct reading is
"high ADS ⇒ pick rules **conditional on low expected lexical noise**," which is a materially
different, narrower claim than the one R3 currently encodes.

## 9. Threats to validity / limitations

- **n_defined is small in the slice that matters.** Only 50 of 240 conditions produce a strict,
  non-tied, non-N/A comparison, and only 20 of those are in the high-ADS band driving the
  disagreement finding. This is a single synthetic generator family, not independent replications.
- **δ=0.02 practical-equivalence margin drives most of the CLEAN "no signal" result.** A tighter δ
  would likely produce non-tied outcomes even under CLEAN and change the CLEAN slice's
  informativeness; this was frozen at Gate 3 and not re-tuned here, per the freeze.
  Correspondingly, a *looser* δ under VARIED could shrink `n_defined` and change the 64% point
  estimate — the reported number is specific to the frozen δ.
  This is a fair scope statement, not a proposal to change the frozen definition.
  See `research/EXPERIMENT_1_CALIBRATION_REPORT.md` §Gate 3 for the justification of δ=0.02.
- **R3 thresholds (0.90 / 0.70) were not re-tuned against this outcome data**, consistent with the
  freeze — they are reused unmodified from `scripts/04_architecture_decision.py`. The fact that R3
  fails specifically in its highest-confidence band is a property of those pre-existing thresholds
  interacting with lexical noise, not of anything selected post hoc in this run.
  This is exactly the sort of asymmetric edge-case a fixed threshold rule can develop.
- **LLM excluded** — this experiment says nothing about whether an LLM mechanism would out-agree
  R3 in the band where retrieval currently wins; that is out of scope for H1 as reworded (redesign
  review §9).
- **Retrieval coverage is 1.0 in all 240 conditions.** Retrieval never abstains at cutoff=75.
  Combined with retrieval's accuracy advantage under noise, this means retrieval essentially always
  answers and is usually right; rules abstains more but is not more accurate when it doesn't
  abstain, under lexical noise.

## 10. Reproducibility

```
python scripts/experiments/exp1/run_final.py
```

Deterministic given the frozen constants in that file (seeds 31001–31020, targets, cutoff=75,
P_TRANSFORM=0.3). Re-running reproduces `final_condition_results.csv` exactly (per-call
`random.Random(seed)` isolation, verified by `test_generator_rng.py`).

## 11. Raw artifact manifest

All under `data/outputs/experiments/exp1/final/` (not yet staged/committed):

- `final_frozen_config.json` — the config block printed and asserted at run start
- `final_seed_manifest.csv` — 240 rows, the (seed, target, lexical) manifest as planned
- `final_conditions.csv` — the manifest as executed, with status and realized_det_pct
- `final_condition_results.csv` — full per-condition raw results (primary artifact, 240 rows, 24 columns)
- `final_bootstrap_results.csv` — bootstrap-focused projection (diff point/CI, winner) per condition
- `final_summary.csv` — aggregated by (target, lexical), 12 rows (§4 above)
- `final_run_metadata.json` — run-level metadata (success/failure counts, timing)

## 12. Scope / stop condition

This document reports exactly what the frozen run produced. No manuscript, README, or
METHODOLOGY file was touched. No Phase E work was started. No condition was selectively rerun —
all 240 were executed identically in one pass after the clean re-run described in §2. Per
instruction, **nothing in this experiment has been staged, committed, or pushed** — that is a
separate, explicit approval step.

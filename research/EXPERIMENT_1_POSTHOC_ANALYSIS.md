# Experiment 1 — Post-hoc Analysis & Interpretation (Phase D.1)

> Analyzes the FROZEN 240-condition Experiment 1 final run (commit
> `6fb618838e47c84234dfad85c89b979e96b6c897`). No new data was generated, no seed/target/
> threshold/delta/cutoff/generator/mechanism change was made. All numbers below are recomputed
> directly from `data/outputs/experiments/exp1/final/final_condition_results.csv` by
> `scripts/experiments/exp1/analyze_posthoc.py` (stdlib-only; run with `--demo` for a self-check
> that reproduces the frozen 32/50 headline figure). Full machine-readable output:
> `data/outputs/experiments/exp1/posthoc/posthoc_analysis_report.json` and
> `posthoc_rows_with_bands.csv`. `README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md`, and every
> file under `.../exp1/final/` were not touched.

---

## 1. Objective

Determine what the frozen 240-condition experiment tells us about the relationship between
historical decision consistency (realized ADS), input representation (lexical/surface-form)
stability, and classification-mechanism suitability — specifically, to explain the observed
reversal (R3-vs-empirical agreement 100% in the ADS 0.70–0.90 band vs. 10% in the ADS ≥0.90 band)
and determine whether it is a genuine interaction, a generator artifact, a mechanism-behavior
artifact, an R3-thresholding artifact, or a combination — without assuming the answer in advance.

## 2. Frozen evidence used

- `data/outputs/experiments/exp1/final/final_condition_results.csv` (240 rows, primary input)
- `final_summary.csv`, `final_bootstrap_results.csv`, `final_run_metadata.json` (cross-checks only)
- `research/EXPERIMENT_1_FINAL_RESULTS.md`, `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` (prior reports,
  used only to verify this analysis reconciles with them — never as a source of new numbers)
- Code read for mechanism/definition ground truth (not modified):
  `scripts/experiments/exp1/{consistency,mechanisms,stats,run_final}.py`

## 3. Data reconstruction

See `research/EXPERIMENT_1_DATA_DICTIONARY.md` for the full column-by-column trace. Two facts
matter most for everything below:

- **`realized_det_pct`** ("realized ADS") is computed **train-only** and grouped by the stable
  `product_code`, never by the perturbable surface string (`normalized_product`). It is therefore
  **invariant to the lexical condition by construction** — confirmed in the data (`realized_ads_mean`
  is byte-identical between CLEAN and VARIED at every target).
- **`empirical_winner`** comes from a **paired** bootstrap (rules and retrieval scored on identical
  held-out test lines within a condition) with a pre-registered δ=0.02 practical-equivalence margin.

## 4. Headline result verification

Independently recomputed from the raw 240-row CSV (manual counting, not by re-calling
`stats.selection_agreement()`):

| Slice | agree | disagree | tie | N/A | n_defined | agreement rate | Wilson 95% CI | binomial p (vs. 50%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Overall | 32 | 18 | 50 | 140 | 50 | 64.0% | [50.14%, 75.86%] | 0.0649 |
| CLEAN | 0 | 0 | 50 | 70 | 0 | undefined | — | — |
| VARIED | 32 | 18 | 0 | 70 | 50 | 64.0% | [50.14%, 75.86%] | 0.0649 |

**Exact match to `EXPERIMENT_1_FINAL_RESULTS.md` §5 and `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §6-7.
No discrepancy found; not stopping.** `scripts/experiments/exp1/analyze_posthoc.py --demo` encodes
this as a runnable assertion.

## 5. ADS-region performance (CLEAN / VARIED / VARIED-with-defined-winner / pooled)

Bucketed by **per-row realized ADS** against the R3 thresholds (`<0.70`, `0.70–0.90`, `≥0.90`) —
not by nominal target (see §10 for why these differ).

| Realized ADS band | Lexical | n | rules acc (mean) | retrieval acc (mean) | rules−retrieval (mean) | rules wins | retrieval wins | ties |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| <0.70 | CLEAN | 70 | 0.7431 | 0.7383 | +0.0048 | 0 | 0 | 70 |
| <0.70 | VARIED | 70 | 0.5493 | 0.6867 | −0.1374 | 0 | 70 | 0 |
| 0.70–0.90 | CLEAN | 32 | 0.8742 | 0.8687 | +0.0055 | 0 | 0 | 32 |
| 0.70–0.90 | VARIED | 32 | 0.6529 | 0.8207 | −0.1678 | 0 | 32 | 0 |
| ≥0.90 | CLEAN | 18 | 0.9534 | 0.9471 | +0.0063 | 0 | 0 | 18 |
| ≥0.90 | VARIED | 18 | 0.7130 | 0.8980 | −0.1851 | 0 | 18 | 0 |

`VARIED_with_defined_winner` is identical to `VARIED` in every band — every single VARIED condition
produces a defined (non-tie) winner, so no rows are dropped. Ties are never hidden: CLEAN produces
120/120 ties and zero defined winners across every band; VARIED produces zero ties across every
band.

## 6. CLEAN vs. VARIED

CLEAN's zero defined winners are **not** evidence that rules and retrieval are "equivalent
mechanisms" in general — it is evidence that they are equivalent **for this generator's clean
condition, within δ=0.02**, and that this is a genuine near-tie, not an artifact of a wide CI
hiding a real gap:

- The raw point difference (`rules − retrieval`) in CLEAN is small and **consistently positive**
  (rules very slightly ahead) at every target, growing mildly with ADS: mean diff 0.0046 (target
  0.00) → 0.0066 (target 1.00), std ≈ 0.003 at each target. This is a real, reproducible, tiny
  rules edge — just one far below the pre-registered δ=0.02 practical-equivalence margin.
- The paired bootstrap CI width on that difference is itself narrow (mean ≈ 0.008–0.010 across
  targets) — **not** a wide, uninformative CI that happens to straddle zero. The mechanisms are
  measurably, precisely close to each other in CLEAN, not merely "impossible to distinguish."
- So: CLEAN tells us the two mechanisms perform almost identically **when there is no lexical
  noise for retrieval's fuzzy matching to be robust to** — an accurate, narrow, well-supported
  reading. It tells us nothing about mechanism selection in general, and nothing about what
  happens once surface noise is present (that's VARIED's job).

## 7. ADS × lexical interaction

| Statistic | CLEAN | VARIED |
|---|---:|---:|
| Pearson r(realized ADS, rules−retrieval) | +0.230 | **−0.803** |
| Spearman r(realized ADS, rules−retrieval) | — | −0.799 |

Mean `rules − retrieval` by target × lexical (identical to §5-6, shown together for the trend):

| target | CLEAN diff | VARIED diff |
|---:|---:|---:|
| 0.00 | +0.0046 | −0.1251 |
| 0.20 | +0.0045 | −0.1329 |
| 0.30 | +0.0049 | −0.1456 |
| 0.50 | +0.0052 | −0.1553 |
| 0.75 | +0.0055 | −0.1738 |
| 1.00 | +0.0066 | −0.1832 |

**Finding: the interaction is real, monotonic, and continuous — not threshold-like — in the
underlying accuracy gap.** Under VARIED, retrieval's advantage over rules widens smoothly and
monotonically as realized ADS increases (r=−0.80, both Pearson and Spearman agree it's not just a
linear artifact). There is no point in the realized-ADS range where the *empirical* gap flips
sign, plateaus, or reverses. The only thing that is threshold-like/discontinuous is **R3's own
selection rule** (a step function with a hard edge at 0.90), which is compared against a smoothly
diverging continuous quantity. The "reversal" is a property of R3's categorical decision colliding
with a monotonic trend, not a property of the trend itself.

## 8. High-ADS reversal — mechanistic explanation

Answering the pre-registered sub-questions directly from the data, not conceptually:

- **(A) Does rules accuracy actually decrease at high ADS?** No. Under VARIED, rules accuracy
  rises monotonically with target ADS: 0.506 → 0.549 → 0.560 → 0.610 → 0.670 → 0.714. Rules gets
  *better* as ADS increases, just not as fast as retrieval does.
- **(B) Does retrieval accuracy increase?** Yes, also monotonically: 0.631 → 0.682 → 0.706 → 0.765
  → 0.844 → 0.897 — and it is higher than rules' accuracy at every single ADS level under VARIED.
- **(C) Does lexical variation disproportionately hurt rules at high ADS?** Yes, and this is the
  crux. The CLEAN-minus-VARIED accuracy drop for rules **grows** with ADS: 0.184 (target 0.00) →
  0.186 → 0.202 → 0.211 → 0.227 → **0.239** (target 1.00). The more deterministic the underlying
  account mapping, the *more* absolute accuracy rules loses to lexical noise — because more of its
  exact-match "wins" are products where, absent surface noise, it would have nailed the answer,
  and each one lexical noise breaks becomes a lost point it otherwise would have kept.
- **(D) Does lexical variation help retrieval, relatively?** Retrieval's own CLEAN-minus-VARIED
  drop stays roughly flat regardless of ADS (0.055, 0.049, 0.051, 0.050, 0.047, 0.049 — no trend).
  Fuzzy matching absorbs surface noise at an approximately constant cost independent of how
  deterministic the labels are. Combined with (C), the rules/retrieval gap under noise widens in
  retrieval's favor specifically because rules' noise-vulnerability scales with ADS while
  retrieval's doesn't.
- **(E) Is the R3 threshold itself selecting the wrong mechanism?** Yes, mechanically. R3 flips its
  recommendation from `retrieval` to `rules` at realized ADS=0.90 — but the *empirical* retrieval
  advantage is largest, not smallest, right at and above that point (§7). R3's 0.90 threshold
  (inherited unmodified from `scripts/04_architecture_decision.py`, not re-derived here) implicitly
  assumes "more determinism ⇒ favor rules," which is exactly backwards in the noisy regime.
- **(F) Is high ADS measuring historical label consistency while ignoring surface-form
  instability?** Yes, and this is true **by construction**, not just empirically: `realized_det_pct`
  is computed by grouping on `product_code` (stable identity), never on `normalized_product` (the
  string the lexical transform perturbs) — see §3 and the Data Dictionary. ADS structurally cannot
  see the very perturbation that determines the winner under VARIED.
- **(G) Is the result driven by a small number of seeds or target regions?** No — see §10. When
  binned by each row's *own* realized ADS rather than its nominal target, the reversal is not
  10%-vs-100% but a clean **0% (0/18) vs. 100% (32/32)** split with zero exceptions in either
  direction (§9). This is a deterministic consequence of the design, not a fragile, seed-sensitive
  pattern.

## 9. R3 vs. actual mechanism performance

Rebinned by each row's own realized ADS (not nominal target) against the R3 thresholds R3 itself
uses — this is a sharper cut than the nominal-target table in `EXPERIMENT_1_FINAL_RESULTS.md` §5,
which mixes rows that nominally share a target but sit on opposite sides of a threshold in their
*realized* value (see §10):

| Realized ADS band | Actual best mechanism (VARIED) | R3's choice | Agreement | Likely explanation |
|---|---|---|---:|---|
| <0.70 | retrieval (70/70) | `llm_required` | N/A (70 rows excluded) | R3 abstains entirely from a comparison here; the excluded LLM mechanism was never tested |
| 0.70–0.90 | retrieval (32/32) | `retrieval` | **100% (32/32)** | R3's rule happens to output the mechanism that always wins here |
| ≥0.90 | retrieval (18/18) | `rules` | **0% (0/18)** | R3 flips to `rules` purely because realized ADS crossed 0.90; the empirical winner never changes |

This is a cleaner and starker split than the previously reported 100%/10% (30/30, 2/20) figure,
because that figure grouped rows by nominal target (0.50, 0.75 → "0.70–0.90"; 1.00 → "≥0.90"),
while 2 of the 20 target=1.00 seeds have *realized* ADS (0.8935, 0.8941) that actually falls below
0.90 (§10). Rebinned by the value R3 itself acts on, those 2 rows belong in the 0.70–0.90 band,
where they trivially agree (R3 correctly says `retrieval`, and retrieval wins everywhere under
VARIED) — not in the ≥0.90 band as a genuine 2/20 "partial success." **The true realized-ADS-band
reversal is 100% vs. 0%, not 100% vs. 10%.** The 10%-vs-100% framing in the frozen report is not
wrong (it correctly describes the nominal-target grouping it used and states its own numbers
accurately), but the per-row realized-band view in this analysis is the more mechanistically
correct one, since it groups by exactly the variable R3's threshold operates on.

Separating "does the mechanism itself misbehave" from "does R3 map ADS to the wrong mechanism"
(§Step 7 of the brief): the mechanisms behave exactly as expected throughout (§8A-D, monotonic,
explicable, no surprises). The failure is entirely in **R3's mapping** — a categorical, ADS-only
threshold rule applied to a domain where the actual winner is governed by a variable (lexical
noise) that ADS cannot observe.

## 10. Robustness across seeds and regions

Realized ADS range by target (`min`–`max` across the 20 seeds), same for CLEAN and VARIED (§3):

| target | realized ADS range | crosses 0.70? | crosses 0.90? |
|---:|---|:---:|:---:|
| 0.00 | 0.441 – 0.527 | no | no |
| 0.20 | 0.522 – 0.615 | no | no |
| 0.30 | 0.569 – 0.649 | no | no |
| 0.50 | 0.659 – 0.727 | **yes** (10/20 seeds land ≥0.70) | no |
| 0.75 | 0.773 – 0.817 | no (all ≥0.70) | no |
| 1.00 | 0.894 – 0.926 | no (all ≥0.70) | **yes** (2/20 seeds land <0.90) |

Only the two targets nominally closest to an R3 threshold (0.50→0.70 boundary, 1.00→0.90 boundary)
straddle it — an expected consequence of ≈1–2.5pp generator calibration noise sitting near a hard
cutoff, not an anomaly. At target=1.00/VARIED, the 2 seeds that land below 0.90 (31007: 0.8935,
31012: 0.8941) are the *only* two of the 20 with `r3_agrees_with_empirical=True`; all other 18
(realized ADS 0.901–0.926) disagree, with zero exceptions. At target=0.50/VARIED, the 10 seeds
below 0.70 are `llm_required` (excluded, not a tie or disagreement); the 10 at or above 0.70 are
`retrieval` and all 10 agree. In both cases the outcome is a perfectly deterministic function of
which side of the threshold each seed's realized ADS falls on, combined with the fact that
retrieval wins 120/120 VARIED conditions unconditionally (§11). This is **not** driven by a small
or idiosyncratic subset of seeds or by one anomalous target region — every seed in every target
behaves consistently with the single explanatory mechanism in §8/§11, and the pattern is exactly,
deterministically reproducible (fixed seeds, `run_final.py` re-run is byte-identical).

## 11. Interpretation

The single fact that explains the entire headline result:

> **Under VARIED, `empirical_winner == "retrieval"` in all 120/120 conditions — every target, every
> seed, no exceptions. Under CLEAN, `empirical_winner == "tie"` in all 120/120 conditions — same.**

The empirical winner in this experiment is a **constant function of the lexical condition alone**,
completely unconditional on realized ADS across its entire observed range (0.44–0.93). R3's
agreement rate with that winner is therefore entirely mechanical: it equals the fraction of
conditions where R3's own ADS-threshold output happens to be `retrieval` (its output under
`0.70 ≤ ADS < 0.90`) rather than `rules` (`ADS ≥ 0.90`) or `llm_required` (`ADS < 0.70`) — not a
measure of how well ADS tracks the true winner, since the true winner never moves.

This is *not* the same finding as "ADS carries no information at all." Pearson correlations
(§9 of the brief, computed in `step9_associations`) show ADS strongly predicts **each mechanism's
own accuracy level**: r(ADS, rules_acc) = 0.96 within CLEAN / 0.91 within VARIED; r(ADS,
retrieval_acc) = 0.95 within CLEAN / 0.95 within VARIED. ADS is a good predictor of *how hard the
classification task is* for both mechanisms, roughly symmetrically. What it does not predict, in
this experiment, is *which mechanism does relatively better* — that is governed almost entirely by
lexical condition (r(lexical, rules−retrieval) = −0.97 pooled), a variable ADS is constructed to be
blind to.

So: the observed reversal is (per the pre-registered candidate explanations in the brief)
**primarily explanation (1) — a genuine interaction** between historical consistency and
representation stability, **compounded by (4) — an R3-thresholding artifact**: the interaction
exists in the continuous, monotonic accuracy-gap data (§7), and R3's categorical 0.90/0.70
threshold turns that continuous, monotonic relationship into a step function that happens to point
the wrong direction above 0.90. It is not (2) a generator-construction artifact (ADS's
train/product_code invariance to lexical noise is a deliberate, documented, correct design choice
— see Data Dictionary — not a bug), and it is not (3) purely a rules/retrieval mechanism-behavior
artifact (§8A-D shows both mechanisms behave exactly as their definitions predict).

## 12. Minimum defensible scientific claim

> In this single synthetic product-classification generator, under a controlled lexical/surface-
> form noise perturbation (`p_transform=0.3`, rapidfuzz-based fuzzy matching), realized historical
> decision consistency (ADS) is strongly predictive of each mechanism's own classification
> accuracy (Pearson r ≈ 0.91–0.96) but carries **no information about which of two mechanisms
> (exact-match rules vs. fuzzy retrieval) will outperform the other** — that ranking is fully
> determined, independent of ADS across the observed range (0.44–0.93), by whether lexical/surface
> noise is present at all: retrieval wins on whole-set accuracy in 120/120 noisy conditions, and
> the two mechanisms are statistically indistinguishable (within a pre-registered δ=0.02 margin) in
> 120/120 noise-free conditions. A pre-specified consistency-only decision rule (R3, thresholds
> 0.90/0.70 on ADS) consequently agrees with the empirical winner in 100% of conditions where its
> ADS-driven recommendation happens to be `retrieval` and in 0% of conditions where it recommends
> `rules`, because ADS is computed (by design) from a stable product identity that cannot observe
> the surface-form instability that actually determines the outcome. This is evidence for a
> narrower, more specific claim than "historical consistency selects the right mechanism": **it is
> informative about task difficulty, not about mechanism ranking, when mechanism ranking is
> governed by an orthogonal representation-stability property the consistency signal cannot see.**
> This finding is scoped to one synthetic generator family, one lexical-perturbation model, and one
> classification-style domain (Romanian-fiscal-style product/account mapping); the previously
> reported production case study is a motivating example only and was not re-examined in this
> analysis.

## 13. Claims we must NOT make

- That ADS predicts which classification mechanism to use, unconditionally — false in this
  experiment; ADS alone predicts task difficulty/accuracy level, not relative mechanism ranking.
- That higher historical consistency means an exact-match/rules approach is better — the opposite
  holds under lexical noise in this data: retrieval's advantage over rules *widens*, not narrows,
  as ADS increases (§7-8).
- That this experiment validates R3 or the shipped architecture-decision procedure — it does not;
  R3 is empirically wrong in exactly the band (`≥0.90`) where it is most confident.
- That this generalizes beyond the tested setting — one synthetic generator family, one lexical-
  perturbation model (`p_transform=0.3`, rapidfuzz cutoff=75), one domain style. No claim about
  enterprise AI, other document types, other noise models (e.g. real OCR error distributions), or
  other languages is supported.
- That the production deployment confirms this finding — the production case study is a motivating
  example elsewhere in the project, not statistical evidence, and was not touched in this phase.
- That ADS itself, or the ADS-Cascade architecture as a whole, is a novel contribution — already
  settled as out of scope in prior literature-verification work (Rice's Algorithm Selection
  Problem / meta-learning framing).
- That the synthetic `p_transform=0.3` perturbation model is representative of real-world surface
  noise (OCR errors, typos, vendor-specific naming) — it is a controlled synthetic stand-in, not a
  validated noise model.
- That the CLEAN condition proves rules and retrieval are equivalent mechanisms in general — it
  shows near-equivalence specifically in the absence of lexical noise, for this generator (§6).

## 14. Is another experiment necessary?

**A. NO FURTHER EXPERIMENT NEEDED** to support the minimum defensible claim in §12.

Reasoning: the observed reversal is not a residual mystery requiring more data to resolve — §8-11
above trace it to a single, fully mechanistic, deterministically reproducible cause (ADS's
by-construction blindness to surface-form instability, colliding with a hard categorical threshold
applied to a smoothly monotonic underlying trend), verified at the level of individual seeds
(§10), not inferred statistically. There is no unresolved uncertainty in the existing 240
conditions that a 241st condition, a new seed, or a new target band would address. The scientific
question this phase was scoped to answer ("what does the frozen experiment tell us about the
ADS/representation-stability/mechanism-suitability relationship") has a complete, evidence-backed
answer from the existing data.

A **genuinely different** research question — "can a decision rule that conditions on both ADS and
a lexical/robustness signal recover R3's accuracy in the high-ADS band?" — is a legitimate, well-
scoped follow-up, but it is a new hypothesis about a *new* rule, not a gap in evidence about *this*
one. Per the project's stopping rule, this belongs in future-work language, not in an immediate
Phase D.2 experiment. See `research/RESEARCH_GPS.md`'s "DO NOT CHASE" list.

## 15. Recommended research direction

Not to be executed now. For the record, and for a future-work paragraph:

- An R3 variant that conditions its mechanism recommendation on both realized ADS and a measured
  (not assumed) lexical/surface-form stability signal — the natural next hypothesis this experiment
  motivates, since §11 shows ADS and the true winner are governed by orthogonal variables here.
- Whether the specific numeric pattern (retrieval's noise-drop staying flat while rules' noise-drop
  grows with ADS, §8C-D) is a property of rapidfuzz-style token similarity specifically, or would
  hold for other retrieval implementations — untested, out of scope for this frozen experiment.

## 16. Manuscript implications

Not a manuscript rewrite (none of README/TECHNICAL_REPORT/METHODOLOGY were touched). For the
Phase E author's use when drafting:

- The finding in §11 gives the paper's revised conceptual chain a specific, data-backed mechanism,
  not just a plausible-sounding causal story: ADS predicts *task difficulty*, not *mechanism
  ranking*; mechanism ranking here is governed by a representation-stability property that this
  particular consistency signal is constructed to be blind to. This is the "Historical decisions →
  decision consistency + representation stability → mechanism suitability" framing sketched in
  session context, and this analysis is now direct evidentiary support for it, not speculation.
  This can be substituted into the "Implication" beat of the paper's working narrative.
- The paper's honest headline finding is narrower and more specific than "ADS works" or "ADS
  doesn't work": it is "ADS is a within-mechanism accuracy predictor, not a between-mechanism
  ranking predictor, when ranking depends on a variable orthogonal to the one ADS measures." That
  framing is defensible directly from §12 without further hedging.
- §9's sharper 100%-vs-0% realized-band split (vs. the previously reported 100%-vs-10% nominal-
  target split) is available as an alternative, more mechanistically precise way to present the
  reversal, if the manuscript author prefers it — both are correct given their respective binning
  choices; the realized-band split groups by the exact variable R3 acts on.
- §13's "claims we must not make" list should directly inform the Limitations section.

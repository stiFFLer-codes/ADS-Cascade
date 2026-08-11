# Experiment 1 Calibration Report — Gates 1-3

> Closes the three methodological gates required before Experiment 1's frozen ≥20-seed run:
> mechanism-blind ADS calibration (Gate 1), dedicated retrieval-cutoff calibration (Gate 2), and a
> frozen empirical-winner/tie/CI definition (Gate 3). Produced under a "harness + calibration only"
> approval — **the final experiment has not been run.** H1 is unchanged from
> `research/EXPERIMENT_1_REDESIGN_REVIEW.md` §2. This document does not modify that file, the
> pilot's own approved output, or any manuscript file.
>
> Supporting code: `scripts/experiments/exp1/calibrate_ads.py`,
> `calibrate_retrieval_cutoff.py`, updated `stats.py`. Raw artifacts:
> `data/outputs/experiments/exp1/calibration/`.

---

## 1. ADS calibration methodology (Gate 1)

`calibrate_ads.py` sweeps a dense target `deterministic_share` grid — 17 points from 0.00 to 1.00,
covering and extending well past the original [0.60, 0.99] range — with **10 independent seeds per
target** (seeds 30001-30010, disjoint from every pilot seed and every other calibration's seeds).
For each (target, seed), it generates a dataset and computes `realized_ads()` (train-only, the same
function the harness uses everywhere else) — **nothing else**. The script imports only the
generator and `consistency.py`; it never imports `mechanisms.py`, never calls
`classify_rules`/`classify_retrieval`, and reads `account_id` only inside the ADS aggregation
itself (never as a classification target). Grep-verifiable: no `mechanisms` import anywhere in the
file.

A first pass at the original [0.50, 0.99] range found the ceiling structurally capped near the R3
rules threshold regardless of target — see §2 — which motivated extending the grid down to 0.00
before freezing this run, to check whether the floor had unused headroom (it did).

A 9-point spot-check re-generated 3 targets under the VARIED lexical condition and compared their
realized ADS against the matched CLEAN-condition seed — all 9 matched **exactly** (not approximately
— identical floats), confirming the pilot-session fix (grouping by `product_code`, not
`normalized_product`) has fully decoupled the primary IV from the lexical-noise nuisance factor
across the whole calibration grid, not just the 3 pilot bands checked earlier.

Zero failed/invalid generations across all 170 (target, seed) runs.

## 2. Target → realized ADS results

| target | n | mean | std | min | max |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 10 | 0.4859 | 0.0309 | 0.4402 | 0.5253 |
| 0.10 | 10 | 0.5253 | 0.0252 | 0.4931 | 0.5618 |
| 0.20 | 10 | 0.5645 | 0.0235 | 0.5215 | 0.5955 |
| 0.30 | 10 | 0.6156 | 0.0157 | 0.5887 | 0.6420 |
| 0.40 | 10 | 0.6626 | 0.0219 | 0.6244 | 0.6940 |
| 0.50 | 10 | 0.6977 | 0.0235 | 0.6646 | 0.7304 |
| 0.55 | 10 | 0.7191 | 0.0216 | 0.6928 | 0.7553 |
| 0.60 | 10 | 0.7369 | 0.0194 | 0.7114 | 0.7725 |
| 0.65 | 10 | 0.7578 | 0.0120 | 0.7394 | 0.7746 |
| 0.70 | 10 | 0.7783 | 0.0122 | 0.7639 | 0.8055 |
| 0.75 | 10 | 0.8015 | 0.0198 | 0.7694 | 0.8424 |
| 0.80 | 10 | 0.8185 | 0.0119 | 0.7995 | 0.8362 |
| 0.85 | 10 | 0.8391 | 0.0144 | 0.8072 | 0.8639 |
| 0.90 | 10 | 0.8664 | 0.0152 | 0.8396 | 0.8876 |
| 0.95 | 10 | 0.8890 | 0.0115 | 0.8689 | 0.9035 |
| 0.99 | 10 | 0.9063 | 0.0077 | 0.8954 | 0.9211 |
| 1.00 | 10 | 0.9076 | 0.0078 | 0.8947 | 0.9188 |

Text plot (mean realized ADS vs. target; `.` = 0.01 realized-ADS units):

```
target  realized mean
 0.00   0.4859  |------------------------------------.
 0.10   0.5253  |----------------------------------------.
 0.20   0.5645  |--------------------------------------------.
 0.30   0.6156  |------------------------------------------------.
 0.40   0.6626  |----------------------------------------------------.
 0.50   0.6977  |-------------------------------------------------------.
 0.55   0.7191  |---------------------------------------------------------.
 0.60   0.7369  |----------------------------------------------------------.
 0.65   0.7578  |------------------------------------------------------------.
 0.70   0.7783  |--------------------------------------------------------------.
 0.75   0.8015  |----------------------------------------------------------------.
 0.80   0.8185  |------------------------------------------------------------------.
 0.85   0.8391  |--------------------------------------------------------------------.
 0.90   0.8664  |-----------------------------------------------------------------------.
 0.95   0.8890  |-------------------------------------------------------------------------.
 0.99   0.9063  |---------------------------------------------------------------------------.
 1.00   0.9076  |---------------------------------------------------------------------------.
                0.45                                                                     0.92
```

**Two findings, both load-bearing for the final design:**

- **The floor has real headroom.** Realized ADS descends smoothly and monotonically to ~0.49 at
  target=0.00 — the original [0.50, 0.99] range was leaving a genuinely reachable low region
  (0.49-0.70) unused.
- **The ceiling is structurally capped, not a tuning artifact.** target=0.99 and target=1.00 realize
  to essentially the same value (0.9063 vs 0.9076 — within noise of each other, and *below* target=0.99's
  own max of 0.9211). Pushing the generation knob to its absolute maximum buys almost nothing beyond
  what target=0.99 already achieves. **No adjustment of `deterministic_share` can push mean realized
  ADS meaningfully above ~0.91.**

**Why the ceiling exists (mechanism-blind diagnosis, from reading the generator, not from running
mechanisms):** `CROSS_COMPANY_ALIGN=0.695` is fixed across every target (by design, §4 of the
redesign review — it is the one nuisance variable explicitly held constant so the ADS sweep isn't
confounded with a second moving parameter). ~12% of products are shared across multiple companies;
for those products, only 69.5% of companies agree on the dominant account regardless of how high
`deterministic_share` is set — that 12% of the catalog structurally cannot exceed roughly a
0.695-driven determinism ceiling, dragging the dataset-level `det_pct` down no matter how
deterministic the other 88% of (single-company) products are. Back-of-envelope: max achievable
`det_pct` ≈ 0.88 × (share of single-company products crossing 0.95) ≈ 0.88 × ~1.0 ≈ 0.88-0.91,
matching the empirical ceiling closely.

**Important framing, not a defect to engineer around:** `CROSS_COMPANY_ALIGN=0.695` is not an
arbitrary synthetic constant — it is the actual production-observed cross-company consistency figure
(`EVIDENCE_BASELINE.md`, canonical). This calibration is therefore not revealing a generator bug; it
is revealing that **a dataset shaped like this repository's real production data structurally cannot
reach a comfortable-margin "deep rules-first" region** (e.g. realized ADS ≥ 0.93-0.95), regardless of
how individually deterministic each company's own booking behavior is. This plausibly explains why
the production system's own R3 decision (91.2%) sits so close to its own 0.90 threshold, and why the
synthetic run's independently-observed "R3 flip" (87.56%) landed exactly in this same narrow zone —
not a fluke of small-scale synthetic sampling, but closer to a structural property of any dataset
with production-realistic cross-company disagreement. This is argued as a plausible interpretation
the calibration curve supports, not as a proven causal claim — worth stating explicitly in any future
manuscript discussion of the ceiling, with that distinction preserved.

## 3. Recommended final ADS regions

**Mechanism-blind selection algorithm** (implemented in `calibrate_ads.py::furthest_point_selection`
+ `anchor_boundary_targets`, entirely a function of the table in §2):

1. Greedy furthest-point selection over realized **mean** ADS, k=6 (matching the original design's
   band count): start from the two extremes, repeatedly add whichever remaining candidate has the
   largest minimum distance to the already-selected set.
2. Check whether any selected target's realized mean sits within 0.03 of the R3 thresholds (0.70,
   0.90); if not, add the single closest whole-grid candidate to that threshold. (Not needed here —
   see below.)

**Result:** `[0.00, 0.20, 0.30, 0.50, 0.75, 1.00]` → realized means **[0.4859, 0.5645, 0.6156,
0.6977, 0.8015, 0.9076]**.

- Reasonably even spacing (gaps of 0.079, 0.051, 0.082, 0.104, 0.106 realized-ADS units).
- One region sits almost exactly on the 0.70 boundary (0.6977, 0.0023 away — the greedy algorithm
  found this without any boundary-anchor intervention needed).
- One region sits at the achievable ceiling (0.9076, 0.0076 above 0.90) — the best available
  approximation to "rules-first, R3-approved," though see §11 for what this region can and cannot
  support.
- No region is deep in comfortable rules-first territory (≥0.93) — **unreachable by this generator**,
  per §2.

## 4. Evidence that the recommendation is mechanism-blind

- `calibrate_ads.py` has zero import of, or reference to, `mechanisms.py`, `classify_rules`, or
  `classify_retrieval` — verifiable by reading the file.
- The only place `account_id` is read is inside `consistency.compute_det_pct()`, which aggregates it
  by dominant-account share per `product_code` — the same train-only ADS computation used everywhere
  else in the harness, not a classification outcome.
- The selection algorithm (`furthest_point_selection`/`anchor_boundary_targets`) takes only
  `{target: {mean, std, min, max}}` as input — a pure function of the calibration table in §2, with
  no accuracy, coverage, or winner information anywhere in its call signature or body.
- The recommended targets were fixed by running the algorithm once, deterministically, on the
  calibration table — no manual override, no re-running with different `k` or tolerance after
  inspecting downstream mechanism behavior (none was computed).

## 5. Retrieval calibration methodology (Gate 2)

`calibrate_retrieval_cutoff.py` uses **5 dedicated calibration seeds (50001-50005)** — disjoint from
every pilot seed, every Gate-1 ADS-calibration seed, and every seed the eventual frozen final run
will use. Calibration condition: `deterministic_share=0.80` (a representative mid-range point, not
one of the six recommended final regions), **VARIED lexical condition, `P_TRANSFORM=0.3`** (the
frozen value from the pilot session) — chosen because the pilot showed CLEAN-condition rules and
retrieval tie regardless of cutoff (no surface noise for a threshold to matter against), so
calibrating under CLEAN would tell us nothing about where the cutoff actually matters.

**Critical scope note, addressing the approval message's "do not use mechanism accuracy to calibrate
thresholds":** this calibration does **not** use classification accuracy (whether the resulting
`account_id` matches the true label). It uses a strictly lower-level, retrieval-only signal —
**product-identity hit rate**: does the top fuzzy match resolve to the *same underlying product*
(`product_code`) as the query, at all? This is standard information-retrieval practice for tuning a
similarity threshold, and it is more mechanism-independent than accuracy-based tuning, not less: it
never reads `account_id`, never invokes the KB's account-assignment logic, and never compares against
`classify_rules`'s output. A wrong-product match and an abstention both count as non-hits; a
right-product match counts as a hit regardless of what account that product happens to be booked to.

Candidate cutoffs: `{60, 65, 70, 75, 80, 85, 90, 95}` (rapidfuzz `WRatio` scale). Selection criterion,
fixed before running: maximize pooled hit-rate subject to coverage ≥ 0.30; ties within 0.01 hit-rate
broken toward the **highest** (most conservative) cutoff — same precedent as the pilot's mechanics
check and the original design's calibration-instability rule (§12 of the redesign review).

## 6. Selected retrieval cutoff

| cutoff | hit_rate | coverage |
|---:|---:|---:|
| 60 | 0.9134 | 1.0000 |
| 65 | 0.9136 | 1.0000 |
| 70 | 0.9134 | 1.0000 |
| **75** | **0.9116** | **1.0000** |
| 80 | 0.9006 | 1.0000 |
| 85 | 0.9000 | 0.9980 |
| 90 | 0.9018 | 0.9638 |
| 95 | 0.8794 | 0.8936 |

Best raw hit-rate is at cutoff=65 (0.9136); cutoffs {60, 65, 70, 75} are all within the 0.01 near-tie
margin, so the highest of that group wins.

**Selected: `RETRIEVAL_CUTOFF = 75`.** This supersedes the pilot's mechanics-check value (90), which
was explicitly never meant to be frozen. Full per-seed and pooled curves:
`data/outputs/experiments/exp1/calibration/retrieval_cutoff_calibration.json`.

## 7. Retrieval failure/abstention behavior

`classify_retrieval(kb, cui, product, direction, cutoff)` (`mechanisms.py`) abstains — returns
`{"account_id": "", "abstain": True}` — **iff both** of the following hold:

1. Company-scoped fuzzy search (`fuzzy_company`) finds no candidate in the company's own product
   catalog scoring ≥ `cutoff`, **and**
2. Global-scoped fuzzy search (`fuzzy_global`) finds no candidate across the entire KB scoring ≥
   `cutoff`.

There is no secondary fallback beyond these two searches for the isolated `retrieval_only` mechanism
(unlike the shipped cascade, which has additional tiers) — per §11 of the redesign review, this
mechanism is evaluated in isolation, not as part of the fallback chain. An abstention is graded as
incorrect under the primary whole-set-accuracy metric (§8), identically to a wrong answer — the
metric does not distinguish "declined to guess" from "guessed wrong" for the primary comparison,
though coverage (§9) reports the distinction separately.

## 8. Final winner definition (Gate 3, item 4)

**Frozen: `stats.paired_bootstrap_winner()`, not the pilot's CI-overlap rule.**

The pilot used `empirical_winner()`: compute each mechanism's own bootstrap CI independently, declare
a tie if the two CIs overlap. This is now explicitly flagged in `stats.py` as **superseded, do not
use for the final run** — it is the wrong test for this design. Rules and retrieval are evaluated on
the *identical* held-out test lines within a condition (a paired design), so their per-line
correctness is correlated, not independent; comparing two separately-computed marginal CIs for
overlap ignores that correlation and is a recognized statistical anti-pattern for paired comparisons.

**Frozen instead:** a **paired bootstrap CI on the accuracy difference**
(`rules_accuracy − retrieval_accuracy`). Each bootstrap resample draws a set of test-line indices
(with replacement) and scores **both** mechanisms on that same resampled set — preserving the
correlation between them exactly, since they are literally being asked to classify the same
resampled items each iteration. 2,000 resamples, 95% percentile interval, `random.Random(seed)`
(stdlib only, reproducible given a fixed seed).

## 9. Final metric definitions (Gate 3, items 1, 2, 3, 5, 6)

1. **Primary performance metric: whole-set accuracy**, unchanged from the redesign review — a
   prediction counts correct only if the mechanism both answered and was right; abstention counts as
   incorrect. Retained because it is a single, pre-specified number that already composes accuracy
   and coverage without inventing an ad hoc weighted formula.
2. **Retrieval abstention:** exactly as defined in §7.
3. **Coverage: secondary**, reported per mechanism per condition (share of test lines not abstained
   on) — used to *interpret* a result (did a mechanism lose by answering wrong, or by refusing to
   answer?), never to compute the primary metric or the winner directly.
4. **Empirical winner: the paired bootstrap decision rule**, §8.
5. **Tie handling / practical-equivalence margin:** **δ = 0.02** (2 whole-set-accuracy percentage
   points), fixed before the final run. Rules wins iff the entire paired-difference CI lies above
   +δ; retrieval wins iff entirely below −δ; otherwise **tie** — a difference smaller than δ cannot
   be ruled out at the pre-registered confidence level, so it is not reported as a winner either way.
   *Justification for δ=0.02:* no formal minimum-important-difference exists for this synthetic task,
   so δ is anchored to this repository's own existing precedent for what it has historically treated
   as a meaningful accuracy gap — the Stage-A calibration that motivated `FUZZY_AUTO_APPLY=False`
   treated a ~4-point gap (45%→49%) as decision-changing, and this calibration report's own
   near-tie rule (§5/§6) used a 1-point margin for a *different* (hit-rate) quantity. δ=0.02 sits
   between those two precedents — conservative enough not to manufacture false wins from noise, small
   enough not to mask a real difference at the scale this repository has previously acted on.
6. **Confidence intervals:** paired bootstrap on the accuracy difference (§8), 2,000 resamples, 95%
   percentile interval, computed once per condition per seed and then reported per band via the same
   percentile-bootstrap convention already used for the crossover-point analysis in the redesign
   review (§16, unchanged).

## 10. Final proposed experimental matrix

```
ADS regions (target -> realized mean, from §3):
  0.00 -> 0.4859
  0.20 -> 0.5645
  0.30 -> 0.6156
  0.50 -> 0.6977   (~0.70 boundary)
  0.75 -> 0.8015
  1.00 -> 0.9076   (~0.90 boundary, at the achievable ceiling)

lexical conditions: [CLEAN, VARIED]
P_TRANSFORM: 0.3   (frozen, outcome-independent, pilot session)
RETRIEVAL_CUTOFF: 75   (frozen, Gate 2, product-identity hit-rate)
seeds: >=20 per (region, lexical) condition -- manifest rule still needs sign-off (open item, unchanged
       from the redesign review §23.4)
mechanisms: rules_only, retrieval_only  (LLM excluded from primary comparison, unchanged)
primary metric: whole-set accuracy
winner rule: paired_bootstrap_winner(), delta=0.02, 2000 resamples  (Gate 3, FROZEN)
6 regions x 2 lexical x >=20 seeds = >=240 conditions
```

Note the target list changed from the redesign review's illustrative `[0.60, 0.70, 0.80, 0.90, 0.95,
0.99]` to `[0.00, 0.20, 0.30, 0.50, 0.75, 1.00]` — the realized-ADS values are what matter (§3), and
this set was chosen purely from the calibration curve, not to preserve the original target numbers
for their own sake.

## 11. Remaining threats to validity

- **No region with a comfortable rules-first margin exists.** The best achievable region (realized
  mean 0.9076) sits barely above the 0.90 threshold, with a std of 0.0078 meaning individual seeds
  will straddle both sides of it. Any "rules wins decisively at high ADS" finding from this region
  will necessarily be a boundary-adjacent result, not a deep-rules-first one. This must be stated
  explicitly wherever this region's results are reported — it is not a limitation to hide, and per
  §2, arguably reflects something true about production-realistic data rather than a generator flaw.
- **δ=0.02 is a judgment call**, anchored to precedent (§9.5) rather than derived from a formal
  cost model of misclassification — reasonable, not provably optimal.
- **The retrieval-cutoff calibration used one representative band (0.80) and lexical condition
  (VARIED)**, not calibrated separately per final region — consistent with the "calibrate once,
  freeze, apply evenhandedly" principle (§12 of the redesign review, avoiding per-band tuning
  advantages), but means the frozen cutoff=75 was not verified to be optimal at, say, the 0.00 or
  1.00 regions specifically. Not fixed here — recalibrating per-region would reintroduce the unequal-
  tuning-effort confound the original design was built to avoid.
- **Product-identity hit-rate is a proxy, not identical to classification accuracy.** A retrieval
  mechanism that reliably finds the right *product* could still occasionally book to the wrong
  *account* if that product's own history is itself ambiguous — the calibration optimizes the
  retrieval step in isolation, which is the correct scope for calibrating a *retrieval* threshold,
  but means cutoff=75 is not guaranteed to also maximize whole-set classification accuracy. This is
  a deliberate, documented scope boundary, not an oversight.
- **17-point, 10-seed, mechanism-blind sweep (170 conditions) plus 5-seed retrieval calibration (40
  conditions) is itself unexercised at the eventual 240-condition frozen scale for runtime purposes**
  — both calibration sweeps ran in well under a minute each; no reason to expect the frozen run
  (previously projected at ~9-11 minutes from the pilot) to behave differently, but this has not been
  separately re-timed with the new regions/cutoff.

## 12. Exact configuration that will be frozen

```python
# Gate 1 -- ADS regions (mechanism-blind, §3)
FINAL_TARGETS = [0.00, 0.20, 0.30, 0.50, 0.75, 1.00]
# realized means (informational, re-measured per-seed at execution time, never assumed):
# [0.4859, 0.5645, 0.6156, 0.6977, 0.8015, 0.9076]

LEXICAL_CONDITIONS = [False, True]
P_TRANSFORM = 0.3                 # frozen, pilot session

# Gate 2 -- retrieval mechanism (§6)
RETRIEVAL_CUTOFF = 75              # frozen, this report

# Gate 3 -- metrics/winner (§8-9)
PRIMARY_METRIC = "whole_set_accuracy"
WINNER_RULE = "paired_bootstrap_winner"
PRACTICAL_EQUIVALENCE_DELTA = 0.02
BOOTSTRAP_RESAMPLES = 2000
BOOTSTRAP_ALPHA = 0.05

MECHANISMS = ["rules_only", "retrieval_only"]   # LLM excluded, unchanged

N_SEEDS_PER_CONDITION = 20          # minimum; manifest generation rule still open (§13)
```

## 13. GO / NO-GO recommendation

**GO for the final ≥20-seed experiment, once the one remaining open item (the seed-manifest
generation rule, carried over unresolved from the redesign review §23.4) is settled** — everything
else Gates 1-3 were asked to resolve is now frozen, evidenced, and reproducible from committed
artifacts.

**Explicitly not a "generator is broken, STOP" verdict.** The calibration did surface a genuine,
load-bearing constraint — no comfortable-margin deep-rules-first region is reachable — but the
achievable realized-ADS range (~0.49 to ~0.91) is wide, well-separated at 6 chosen points including
near both R3 thresholds, and directly usable for testing H1's core claim (the rules-vs-retrieval
crossover). The ceiling is best treated as a real, reportable finding about production-realistic
cross-company disagreement structurally bounding achievable determinism — not a defect to engineer
around by adjusting `CROSS_COMPANY_ALIGN` or the multi-company product share, both of which are
grounded in real production evidence and must not be tuned merely to reach a higher ceiling (that
would be exactly the outcome-directed tuning this whole process has been designed to avoid).

Still not executed, still awaiting explicit approval: the frozen ≥20-seed run itself, and the
seed-manifest decision it needs first.

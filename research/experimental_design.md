# Experimental Design — Phase C

> Full protocols for the three experiments named in `experimental_hypotheses.md`. **Design only —
> none of these experiments have been run.** All three are designed to reuse the existing synthetic
> pipeline (`scripts/00_generate_synthetic.py` → `03_5_dataset_intelligence.py` →
> `04_architecture_decision.py` → `scripts/phase2/p2lib/*`) rather than build new infrastructure —
> the generator already exposes the one parameter each experiment needs to sweep
> (`DETERMINISTIC_SHARE` in `00_generate_synthetic.py`, currently a single hardcoded value). No new
> external dependency, no client data, offline except where explicitly noted for the LLM condition.

---

## Experiment 1 — Does historical decision consistency predict which mechanism should be used? (tests H1 / C2)

### Purpose

The current R1/R3 decision rule has been *exercised* twice (once on production data, once on
synthetic data) and never *validated* — no run has ever checked whether the mechanism the rule
selects actually outperforms the alternatives it wasn't given a chance to try. This experiment
builds that check.

### Independent variables

- **Primary — target ADS band** (categorical, 6 levels): ≈0.60, 0.70, 0.80, 0.90, 0.95, 0.99.
  Realized by generalizing `00_generate_synthetic.py`'s single hardcoded `DETERMINISTIC_SHARE`
  constant into a sweep parameter (the generator already produces the target consistency level by
  construction — no new generation logic is needed, only parameterizing an existing constant).
- **Secondary — label-noise structure** (categorical, 2 levels, to test robustness): uniform noise
  (each non-dominant account equally likely) vs. skewed noise (one runner-up account absorbs most
  of the disagreement, matching the qualitative pattern seen in `product_ambiguity.csv`). Run as a
  robustness check, not the primary axis.
- **Held fixed across all runs:** company count (60), product vocabulary size (1,200), invoice
  volume, VAT/purchase-sale distributions — everything `00_generate_synthetic.py` currently
  targets except the swept parameter(s), so that only the intended variable moves.

### Dependent variables

For each of three mechanism classes, actually built and evaluated (not merely the selection rule)
on the same held-out split at each band:

1. **Rules-first / exact-lookup mechanism** — the existing Tier-1 exact `(company, product)` →
   account lookup already implemented in `scripts/phase2/p2lib/cascade.py` / `kb.py`.
2. **Embedding-primary / retrieval mechanism** — the existing fuzzy/global-pool retrieval bridge
   already implemented in `cascade.py` (`retrieval.py`), used as the primary classifier rather than
   a fallback.
3. **LLM-required mechanism** — the existing Groq adapter (`p2lib/ai/adapter.py`) used as a direct
   classifier rather than a candidate-reranker, OR (see Confounders, below) a calibrated synthetic
   proxy if live-API reproducibility is a blocker.

Measured per mechanism per band: held-out accuracy, coverage (share of items the mechanism is
willing to answer, for mechanisms with a confidence floor), and cost proxy (lookups are ~free;
retrieval is O(vocabulary); LLM calls are metered — record call count as the cost unit).

**Primary derived DV:** rank agreement between (a) the mechanism the current 0.90/0.70 threshold
rule selects at that band and (b) the mechanism with the best accuracy (or best cost-adjusted
accuracy) actually measured at that band.

### Baselines

- **Always-rules, always-retrieval, always-LLM** (single mechanism applied at every band) — these
  are the same three points the primary DVs already measure, reused as baselines for the ranking
  comparison rather than as a separate run.
- **Random mechanism selection** (choose one of the three uniformly at random per band) — a null
  model; the threshold rule must beat this by a wide margin to be worth reporting at all.
- **Oracle** (post-hoc, pick whichever of the three actually scored best at that band) — an upper
  bound, not a fair comparison; included only to show how much headroom exists between the
  threshold rule and a cheating best-case selector.

### Controls

- Same synthetic seed used for the underlying company/product/invoice generation across mechanism
  conditions at a given band, so the compared mechanisms see identical data — only the mechanism
  differs, not the dataset instance.
- Same train/held-out split logic and split ratio at every band (matches the existing 80/20
  convention in `p2_02_classify_eval.py`).
- Fixed, un-tuned confidence thresholds per mechanism, set once before the sweep begins and not
  re-tuned per band — tuning thresholds per band would let the "always beats" result be an artifact
  of unequal tuning effort rather than a genuine mechanism-vs-consistency relationship.

### Confounders

- **Dataset size vs. determinism interaction.** Smaller multi-company overlap at low consistency
  could itself reduce measured consistency independent of the true injected noise rate — hold
  company/product counts fixed (see Independent variables) to isolate this.
- **Embedding quality depends on product-string diversity**, not just label noise — the retrieval
  mechanism's performance could vary with vocabulary structure in ways unrelated to determinism.
  Mitigate by holding vocabulary generation parameters fixed across bands (only the label-assignment
  noise parameter moves).
- **LLM performance depends on prompt design and candidate-list quality**, which would confound
  "LLM as direct classifier" with "retrieval quality feeding the LLM" if the LLM condition is fed
  retrieved candidates. For a clean test of "LLM as its own mechanism class," the LLM condition
  must classify from the raw product string, not from cascade-retrieved candidates — this is a
  deliberate deviation from ADS-Cascade's own production design (which always feeds the LLM
  retrieved candidates) and must be flagged in the write-up as testing the mechanism class in
  isolation, not testing ADS-Cascade's actual Tier-3 behavior.
- **Live-LLM reproducibility.** Six bands × two noise structures × multiple seeds (see Statistical
  evaluation) run against a live API is expensive and not fully reproducible without a shared key.
  Two acceptable resolutions, to be decided before execution (not here): (a) run the LLM condition
  once per band with results cached (matching the existing `llm_cache/` convention), accepting
  reduced statistical power on that one mechanism only; or (b) build a calibrated synthetic proxy
  for LLM classification accuracy vs. noise level, using the already-observed Groq tail results
  (`llm_tail_proposals.csv`) to set the proxy's error characteristics, and flag it explicitly as a
  simulation, not a live measurement. Do not silently choose (b) and report it as equivalent to (a).

### Expected outcomes (if H1 holds)

Monotonic dominance: rules-first mechanism has the best accuracy at ADS≈0.90-0.99; embedding
mechanism has the best accuracy at ADS≈0.70-0.90; at ADS≈0.60, either the LLM mechanism is needed
to clear an acceptable accuracy floor, or all three mechanisms converge to similarly poor accuracy
(a valid H1-consistent outcome, since low consistency data may simply be hard for everything,
which is itself informative). Crossover points between mechanisms should fall close to the existing
0.90 and 0.70 constants.

### Failure conditions (falsification)

- Any band where the rule-selected mechanism is not empirically best, especially near ADS≈0.87-0.91
  where real production/synthetic evidence already disagrees (the "R3 flip").
- A non-monotonic relationship (e.g., embedding-primary is best at both ADS=0.65 and ADS=0.95, with
  rules-first only winning in between) — this would undermine the entire "consistency predicts
  mechanism" framing, not just the specific threshold values.
- All three mechanisms performing statistically indistinguishably across all bands — this would
  mean ADS carries no predictive signal for mechanism choice at all, the strongest possible
  falsification of C2.

### Statistical evaluation

- Minimum 20 independent synthetic-generation seeds per band (addresses the Phase A finding, F42,
  that the existing single-seed synthetic run cannot support any "0.76-0.80 across seeds" claim —
  this experiment must not repeat that gap).
- Report mean ± 95% bootstrap CI for each mechanism's accuracy at each band.
- Report the empirical crossover ADS value between adjacent mechanism classes (e.g., where the
  retrieval-vs-rules accuracy curves cross), with a bootstrap CI on that crossover point, for direct
  comparison against the fixed 0.90/0.70 constants.
- Rank-agreement statistic (e.g., a simple match/mismatch count, or Kendall's tau if more than a
  best-mechanism ranking is reported) between rule-selected and empirically-best mechanism across
  the 6 bands × 2 noise structures = 12 conditions.

### Reproducibility requirements

- All generation and evaluation code changes stay inside the existing `scripts/` tree, reusing
  `00_generate_synthetic.py`, `03_5_dataset_intelligence.py`, `04_architecture_decision.py`, and
  `scripts/phase2/p2lib/*` — no new dependency, no client data, offline except the LLM condition
  (see Confounders).
- Every seed and band combination's raw output committed as CSV (matching the existing
  `data/outputs/` convention), so the crossover-point statistic is independently recomputable
  without rerunning generation.
- If the LLM proxy resolution (b) above is used, the proxy's calibration procedure and its inputs
  must be committed and documented as clearly as the rest of the pipeline — a hidden or undocumented
  proxy would break the paper's existing reproducibility discipline.

---

## Experiment 2 — Does the heterogeneous cascade provide value over simpler alternatives? (tests H2 / C6)

### Purpose

No baseline comparison of any kind currently exists for the combined system. This experiment builds
one, using the same held-out synthetic split the current cascade evaluation already uses.

### Independent variable

**Architecture** (categorical, 5 levels):

- **B1 — Rules-only.** Exact `(company, product)` lookup; unmatched items go straight to human
  review (no retrieval, no LLM).
- **B2 — Retrieval-only.** Embedding/fuzzy match against the full KB; no exact-lookup shortcut, no
  LLM; a fixed similarity floor gates auto-apply vs. review.
- **B3 — LLM-only.** Every item classified directly by the LLM from the raw product string
  (matching Experiment 1's isolated LLM condition, reused here); no rules, no retrieval bridge.
- **B4 — Fixed rules→retrieval→LLM cascade.** The same three mechanisms as ADS-Cascade, run in a
  fixed order with fixed confidence floors, but **no evidence-driven (ADS-based) gating** — i.e.,
  every item always tries rules, then retrieval, then LLM, regardless of that product's historical
  determinism. This is the critical baseline: it isolates the value of evidence-driven *routing*
  from the value of simply *having* multiple mechanisms available.
- **B5 — ADS-Cascade (evidence-driven).** The current shipped system: tier selection informed by
  each item's historical determinism, dual unblended confidence signals, reranking-only LLM,
  permanent promotion loop (loop held constant/disabled for this experiment — feedback effects are
  Experiment 3's variable, not this one's).

### Dependent variables

Accuracy, coverage (share auto-decided without human review), automation rate, human-review rate,
escalation rate (share reaching the terminal/LLM tier), compute/model-call cost (lookup ≈ free;
retrieval ≈ O(vocabulary) per query; LLM ≈ metered calls), and error severity (a weighted metric:
misrouting to a materially wrong account class, e.g. expense vs. asset, counted as more severe than
a near-miss within the same account family — reuses the account-type taxonomy already present in
`00_generate_synthetic.py`'s `ACCT_DESC` structure).

### Baselines

B1-B4 are themselves the baselines against which B5 is evaluated; there is no additional baseline
layer beyond these five architectures.

### Controls

- Identical held-out split and identical underlying synthetic dataset (a single fixed band, e.g.
  the current default `DETERMINISTIC_SHARE`, or — better — run across the same 6 ADS bands as
  Experiment 1, so the two experiments share raw data and this one can additionally report whether
  B5's advantage over B4 varies by determinism band, directly connecting the two experiments).
- Confidence-floor/threshold values for B1-B4 set once, via the same calibration effort already
  documented for the shipped system (`EVIDENCE_BASELINE.md`'s note that `FUZZY_AUTO_APPLY` was
  disabled after a calibration run found it unsafe) — applied evenhandedly, not tuned harder for B5
  than for the baselines, which would bias the comparison in B5's favor.

### Confounders

- **Unequal tuning effort.** B5 has already been calibrated once in production; B1-B4 have not.
  Giving B5 a tuning advantage would manufacture its own result. Mitigate by using the same
  calibration *procedure* (a single held-out calibration sweep, same data volume) for every
  baseline, not hand-picked thresholds for B1-B4.
- **Cost-model weighting.** A pure model-call count under-weights human-review time, which is the
  most expensive resource in the real system. The error-severity and human-review-rate DVs must be
  read together with cost, not cost alone, or B1 (rules-only, cheapest, lowest coverage) could look
  artificially favorable on cost while being worst on coverage.
- **B4 is the load-bearing baseline; get it right.** If B4 is built loosely (e.g. with worse
  thresholds than B5 "by accident"), any B5 win over B4 is uninformative. This baseline deserves the
  most implementation scrutiny of the five.

### Expected outcomes (if H2 holds)

B5 Pareto-dominates B1-B3 (no single mechanism should beat a cascade that includes it as one tier).
B5 shows a measurably better accuracy-cost or accuracy-human-review-rate frontier than B4
specifically — this isolates evidence-driven gating's marginal value over simply having all three
mechanisms available in a fixed order.

### Failure conditions (falsification)

B4 matches B5 within the experiment's confidence interval on the primary accuracy-cost frontier →
evidence-driven gating adds no demonstrated value over a static pipeline (see
`experimental_hypotheses.md` H2 falsification criterion for the full statement, including the
weaker "B5 beats B1-B3 but not B4" partial-failure case).

### Statistical evaluation

Multiple seeds per architecture (matching Experiment 1's ≥20-seed standard if run on the same data);
report accuracy/coverage/cost with bootstrap CIs per architecture; primary comparison is B5 vs. B4
paired on the same seeds (paired bootstrap or paired permutation test on the accuracy-cost frontier,
not independent-sample tests, since both architectures run on identical data per seed).

### Reproducibility requirements

Reuses `scripts/phase2/p2lib/cascade.py`, `p2_02_classify_eval.py`; B1-B4 are subsets/reconfigurations
of the same module (a rules-only run is the existing cascade with retrieval/LLM tiers disabled, not
new code) — implementation should be a configuration flag, not a parallel codebase, to guarantee B4
and B5 differ only in the gating logic under test, per the ponytail-style principle of minimum new
surface area for a fair comparison.

---

## Experiment 3 — Does the T4→T1 feedback loop improve the system over time? (tests H3 / C5)

### Purpose

No before/after measurement of the feedback loop exists anywhere in this repository. This
experiment simulates a transaction stream with known ground truth (available because synthetic data
carries true labels) to measure the loop's effect directly.

### Independent variables

- **Feedback loop state** (2 levels): enabled (T4 corrections permanently promote to T1, as shipped)
  vs. disabled (T4 items are reviewed but never written back to the KB).
- **Promotion rule** (3 levels, only under "enabled"): the shipped evidence-weighted rule; a naive
  "always trust the most recent human correction" rule with no evidence weighting; and a
  false-promotion-injection condition (a controlled fraction, e.g. 2%/5%/10%, of simulated "human
  corrections" are deliberately wrong, to test robustness — real human error is not zero).

### Dependent variables

Accuracy and automation rate measured per simulated period (a period = one batch of transactions
processed in sequence, e.g. matching a monthly invoice-processing cadence); number of items
promoted; number of *false* promotions (known exactly, since synthetic ground truth is available);
periods-to-stabilization (the period index at which automation rate plateaus within a small
tolerance band).

### Baselines

The loop-disabled condition is the primary baseline. The naive last-correction-wins rule is a
secondary baseline that isolates whether the shipped rule's evidence-weighting adds value over the
simplest possible feedback mechanism.

### Controls

Same underlying synthetic product/company population and same simulated transaction order across
loop-enabled/disabled/naive conditions, so only the feedback mechanism differs. A fixed, documented
review-tail sampling procedure (which T4 items get "corrected" by the simulated human each period)
applied identically across conditions.

### Confounders

- **Simulated-human accuracy assumption.** If the simulated corrections are always ground-truth
  correct (except in the deliberate false-promotion-injection condition), the experiment measures
  an optimistic ceiling, not real human behavior. State this assumption explicitly in the write-up
  rather than implying the result generalizes to noisy real human review.
- **Order effects.** Which items appear in early vs. late periods could bias stabilization-time
  measurements if the simulated stream isn't randomized per seed. Mitigate with multiple random
  orderings, not a single fixed transaction sequence.
- **Determinism-band interaction.** A feedback loop plausibly matters more at low-ADS bands (more to
  learn) than high-ADS bands (already mostly deterministic). Consider running this experiment at
  2-3 of Experiment 1's bands rather than only the default, to check whether the loop's value is
  uniform or concentrated in the low-consistency tail.

### Expected outcomes (if H3 holds)

Automation rate rises monotonically over periods under the enabled condition and plateaus once the
correctable tail is exhausted; the disabled condition shows no such rise (flat automation rate).
The evidence-weighted rule degrades more gracefully than the naive rule as the false-promotion
injection rate increases (fewer wrong permanent promotions per unit of injected error).

### Failure conditions (falsification)

No measurable automation-rate or accuracy difference between enabled and disabled conditions over
the simulated stream → the mechanism's value is undemonstrated. The naive rule matches the
evidence-weighted rule's robustness under injected false corrections → the "evidence-driven"
framing adds nothing over a trivial write-through cache (see `experimental_hypotheses.md` H3
falsification criterion).

### Statistical evaluation

Multiple random stream orderings per condition (≥20, matching the other two experiments' standard);
report automation-rate trajectories with CIs per period; compare enabled-vs-disabled final-period
automation rate via paired bootstrap (same seed/ordering across conditions); report
false-promotion count as a function of injection rate for the evidence-weighted vs. naive rule,
with a simple regression or direct rate comparison.

### Reproducibility requirements

Simulated stream generation reuses `00_generate_synthetic.py`'s invoice-line generation logic
(replaying lines in batches rather than all at once); the promotion-rule logic under test is
already implemented in the shipped KB code (`p2lib/kb.py`/`cascade.py`) — the naive-rule and
loop-disabled conditions are configuration variants of the same code path, not new implementations,
for the same fairness reason given in Experiment 2.

---

## Cross-experiment notes

- Experiments 1 and 2 can share the same underlying 6-band synthetic dataset generation if run
  together, reducing total new generation code to one parameterization of
  `00_generate_synthetic.py`'s `DETERMINISTIC_SHARE` constant.
- All three experiments deliberately avoid new external dependencies, client data, or non-reproducible
  infrastructure, consistent with this repository's existing reproducibility discipline
  (`EVIDENCE_BASELINE.md`, `METHODOLOGY.md`) — the one flagged exception is Experiment 1's live-LLM
  condition, which needs an explicit author decision before execution (see Experiment 1,
  Confounders).
- None of these experiments were run as part of this Phase C pass. Execution is out of scope per
  the mission's explicit "STOP after designing the experiments" instruction.

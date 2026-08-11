# Experimental Hypotheses — Phase C

> Formal statement of the three falsifiable hypotheses this stress test identifies as necessary
> (H1) or useful (H2, H3) to make the manuscript defensible. Full protocols —
> independent/dependent variables, baselines, controls, confounders, statistics, reproducibility —
> are in `experimental_design.md`. This document states only the claim, the prediction, and the
> falsification criterion, for quick reference. **Design only — none of these have been run.**

---

## H1 — Historical consistency predicts mechanism-class performance (tests C2)

**Hypothesis.** At a given per-product historical label-consistency level (ADS band), the
classification mechanism class that empirically performs best (highest accuracy at acceptable
coverage, or best cost-adjusted accuracy) is the mechanism class the existing 0.90/0.70 threshold
rule would select: rules-first lookup at high consistency, embedding-primary retrieval at medium
consistency, LLM-required reasoning at low consistency.

**Prediction.** A monotonic relationship across six controlled ADS bands (≈0.60, 0.70, 0.80, 0.90,
0.95, 0.99): rules-first dominates at 0.90-0.99, embedding-primary dominates at 0.70-0.90, and
either LLM-required is necessary to reach acceptable accuracy, or all three converge, below 0.70.
The empirical crossover points should land near the existing 0.90 and 0.70 thresholds, not far from
them.

**Falsification criterion.** The hypothesis is falsified if, at any band, the empirically
best-performing mechanism is not the mechanism the current threshold rule would select for that
band — especially if this happens at the two bands adjacent to production and synthetic evidence
already gathered (≈0.87-0.91, where the real "R3 flip" occurred). A single crossed band with a wide
margin is a warning sign; crossed bands at multiple points, or a non-monotonic relationship, are
grounds to reject H1 in its current threshold-based form.

**This is the single required experiment.** See `experimental_design.md` Experiment 1.

---

## H2 — The evidence-driven cascade beats simpler baselines (tests C6)

**Hypothesis.** The full ADS-Cascade system (B5: evidence-driven tier selection, dual signals,
reranking-only LLM, feedback loop) achieves a better accuracy/automation-rate/cost frontier than
each of four simpler baselines (B1 rules-only, B2 retrieval-only, B3 LLM-only, B4 fixed-order
rules→retrieval→LLM cascade with no evidence-driven gating) on the same held-out data.

**Prediction.** B5 Pareto-dominates B1-B3 (higher accuracy at any coverage level, or higher
coverage at any accuracy level). B5 shows measurably better cost-per-correct-classification and/or
lower human-review rate than B4, isolating the value of *evidence-driven* gating specifically
(since B4 already has the same mechanism stack, just without the ADS-based routing decision).

**Falsification criterion.** If B4 (fixed order, no evidence-driven gating) matches B5 on the
accuracy-cost frontier within the experiment's confidence interval, evidence-driven gating adds no
demonstrated value over a static pipeline — falsifying the strong form of C6. A weaker but still
informative failure: if B5 beats B1-B3 but not B4, the paper's defensible claim narrows to "a
multi-mechanism cascade beats any single mechanism," which is already well-precedented (per
`contribution_status.md` C3/C4) and not itself a new finding.

**Recommended, not required.** See `experimental_design.md` Experiment 2.

---

## H3 — The T4→T1 feedback loop measurably improves the system over time (tests C5)

**Hypothesis.** Enabling permanent human-correction promotion produces measurable improvement in
automation rate and/or accuracy over a simulated multi-period transaction stream, relative to the
same system with the loop disabled, and relative to a naive "trust the most recent correction, no
evidence weighting" baseline.

**Prediction.** Automation rate rises monotonically over simulated periods with the loop enabled,
plateauing as the correctable long tail is exhausted; the loop-disabled control shows no such rise.
The evidence-weighted promotion rule resists a controlled rate of injected incorrect corrections
(false promotions) better than the naive last-correction-wins baseline.

**Falsification criterion.** If loop-enabled and loop-disabled runs show no measurable difference
in automation rate or accuracy over the simulated stream, the mechanism's value is undemonstrated.
If the naive baseline matches the evidence-weighted rule's robustness to injected errors, the
"evidence-driven" framing of the promotion rule adds nothing over a trivial cache.

**Recommended, not required.** See `experimental_design.md` Experiment 3.

---

## Priority if resources are limited

Run H1 first and alone if only one experiment is feasible — it is the only hypothesis whose
outcome changes a claim's status from PROMISING toward either STRONG_CANDIDATE or REJECTED (see
`contribution_stress_test.md` conclusion 6). H2 and H3 upgrade WEAK claims at best; H1 is the
paper's only claim that is not already weak or rejected.

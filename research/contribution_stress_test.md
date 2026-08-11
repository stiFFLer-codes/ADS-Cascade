# Contribution Stress Test — Phase C

> Applies the A-H framework (claim / prior-art overlap / distinctive element / technical
> significance / testability / falsification test / current evidence / missing evidence) to each
> candidate contribution named in the Phase C mission, using Phase B's closed literature audit
> (`literature/contribution_status.md`, `literature/prior_art_map.md`,
> `literature/ads_metric_prior_art.md`, `literature/llm_advisory_prior_art.md`) as the evidence
> base. Machine-readable form: `contribution_stress_test.csv`. This document does not rewrite the
> manuscript and does not declare ADS-Cascade novel — it scores what survives.
>
> **ID mapping note:** this document's C1/C2/C3/C5/C6/C8 follow the Phase C mission's own
> numbering, which differs from Phase B's `contribution_status.md` numbering in two places: this
> C2 subsumes Phase B's C2 (general pattern, CHALLENGED) and C2b (narrower combination,
> PARTIALLY_SUPPORTED); this C3 corresponds to Phase B's **C3b** (dual signals), not Phase B's C3
> (the general cascade pattern, which is CHALLENGED outright and not re-litigated here). Phase B's
> C4 (LLM reranking-only constraint) and C7 (cross-company threshold) are not re-scored as separate
> rows here, per the mission's "do not add new contributions unless strongly justified" instruction
> — C7 is subsumed into C2 below (it is a specific instance of historical-consistency-driven
> architecture selection), and C4 is discussed under C6 (it is one of the four elements the
> combination claim rests on).

---

## C1 — The ADS metric itself

**A. Claim.** `ADS(p) = max(c_i) / sum(c_i)` over an item's historical label-assignment counts is
a measurement contribution — "turns 'is this dataset learnable, and by what' into a measured
quantity" (`TECHNICAL_REPORT.md` §2.2).

**B. Prior art overlap.** Direct, Tier 1. Two independent literatures converge on the identical
closed-form expression:
- Cluster purity (`purity = max_j(class-j count) / cluster-size`) — Manning, Raghavan & Schütze
  2008; Amigó, Gonzalo, Artiles & Verdejo 2009 (DOI `10.1007/s10791-008-9066-8`); Zhao & Karypis
  2003.
- Majority-vote-agreement proportion, the universal naive baseline throughout the Dawid & Skene
  (1979) truth-inference descendant literature — confirmed independently by Uma et al. 2021 and
  Davani, Díaz & Prabhakaran 2021.
- Fleiss (1971)'s inter-rater-agreement lineage carries a near-identical informal "percent
  agreement with the majority label" construct.

**C. What is genuinely different.** Nothing mathematical. Only the unit of analysis changes
("cluster" → "an item's historical booking multiset"), which is a relabeling of an existing
formula, not a new one.

**D. Technically meaningful?** No. A formula that is provably identical to an established metric
under substitution is not a technical contribution regardless of the new name attached to it.

**E. Empirically testable?** Not applicable — this is a closed-form mathematical-identity finding,
not an empirical hypothesis. No experiment can change whether two formulas are the same formula.

**F. Falsification test.** None needed; already resolved by direct algebraic comparison
(`ads_metric_prior_art.md`).

**G. Evidence that exists.** `ads_metric_prior_art.md` / `ads_metric_prior_art.csv`, rows
G1-01 through G1-09, produced by the 2026-08-11 targeted gap-verification pass.

**H. Evidence still needed.** None. This question is closed, not open.

**Verdict: REJECTED as a novelty claim**, as expected going into this pass. The metric should be
cited in the manuscript as "cluster purity applied to historical per-item label distributions"
(citing Manning et al. 2008 / Amigó et al. 2009 / Dawid & Skene 1979), with zero novelty weight.
Any surviving novelty argument must relocate entirely to C2 (the metric's *application* as a
design-time signal), never to the metric's construction.

---

## C2 — Historical decision consistency as a design-time architecture/mechanism-class selector

**A. Claim.** Aggregating ADS across a dataset and comparing it to fixed thresholds (0.90, 0.70),
*once, before deployment*, is a valid procedure for choosing which class of classification
mechanism to build: rules-first lookup, embedding-primary retrieval, or LLM-required reasoning.
This is the mission's designated "potentially distinctive hypothesis."

**B. Prior art overlap.** The *general* pattern — measure evidence once, choose system design
before serving — is not novel and dates to Rice (1976)'s Algorithm Selection Problem, with an
unbroken lineage through Smith-Miles (2009), Ali & Smith (2006), Khan et al. (2020), Barbudo et
al. (2023, explicitly naming ASP as "superseded by workflow composition"), and the self-designed
data-systems literature (Idreos & Kraska 2019; Kraska 2021) — though the latter's dominant
philosophy is *continuous* self-adaptation, the opposite temporal structure from ADS-Cascade's
one-time pre-deployment gate (a genuine, citable point of contrast, not a similarity).

**C. What is genuinely different.** The narrower combination — (a) the evidence signal is
restricted specifically to historical label *consistency* (not workload frequency, not
cross-validated task performance, not generic statistical meta-features), combined with (b) the
decision output is a qualitative choice among mechanism *classes* (rules vs. embedding vs. LLM),
not an algorithm or hyperparameter choice within one fixed class — was not found combined
anywhere in the 79 reviewed sources. This is Phase B's C2b, and it is the only PARTIALLY_SUPPORTED
finding among the "general pattern" claims (C2, C3, C7 in Phase B's numbering are all CHALLENGED
outright as broadly stated).

**D. Technically meaningful?** Conditionally. It is meaningful *if and only if* the ADS value
actually predicts, in a measurable sense, which mechanism class will perform best or most
cost-effectively. As currently evidenced, this has never been checked — R1 and R3 are threshold
comparisons applied to a single number per dataset, not predictions validated against measured
mechanism performance.

**E. Empirically testable?** Yes — cleanly. See `experimental_design.md`, Experiment 1.

**F. Falsification test.** If, at a controlled ADS band, the mechanism that empirically performs
best (accuracy, coverage, or cost-adjusted accuracy) is not the mechanism the 0.90/0.70 threshold
rule would select — e.g. embedding-primary retrieval beats a rules-first lookup at ADS ≈ 0.95, or
a rules-first lookup beats an LLM at ADS ≈ 0.60 — the specific threshold values are falsified, and
if the mismatch is large and consistent across bands and seeds, the qualitative claim itself is
falsified.

**G. Evidence that exists.** Exactly two real data points, both single-run, both the decision rule
being *exercised*, not *validated*:
- Production: det_pct = 91.2% → RULES_FIRST (`reports/phase1_final_report.md` §8).
- Synthetic: det_pct = 87.56% → EMBEDDING_PRIMARY, the "R3 flip"
  (`research/r3_threshold_analysis.md`, `EVIDENCE_BASELINE.md`).

Neither run measured whether RULES_FIRST actually outperformed EMBEDDING_PRIMARY or LLM_REQUIRED
at 91.2%, or whether EMBEDDING_PRIMARY actually outperformed RULES_FIRST at 87.56% — no
alternative mechanism was ever built and measured on either dataset. The rule has never been given
a chance to be wrong.

**H. Evidence still needed.** A controlled sweep across ADS bands with all three mechanism classes
actually built and measured head-to-head on the same data — Experiment 1 specifies this in full.

**Verdict: PROMISING.** This is the strongest candidate among the six, and the only one whose core
empirical claim (not just its literature framing) has a clean falsifiable test. It is not yet
STRONG_CANDIDATE because "survives a literature challenge" and "is empirically validated" are
different things, and only the former has happened.

---

## C3 — Dual independent confidence signals

**A. Claim.** Extraction confidence (from OCR/structuring) and classification confidence (from the
product→account cascade) are computed by architecturally separate subsystems and never blended,
specifically to avoid conflating two different failure modes (ADR-007).

**B. Prior art overlap.** Liu, Gallego & Barbieri (2022, B5-06) is a genuine near-miss: it uses two
related uncertainty terms to modulate a single deferral decision.

**C. What is genuinely different.** B5-06's two terms both originate from the *same* model's
internal uncertainty; ADS-Cascade's two signals originate from two *architecturally separate*
subsystems (a third-party OCR provider vs. an internal classification pipeline). Real, but narrow.

**D. Technically meaningful?** Marginal. "Don't blend two differently-sourced confidence signals"
is defensible engineering practice, but no evidence in this repository shows blending them would
actually route items worse.

**E. Empirically testable?** Yes in principle — an ablation (blended single score vs. the current
two-signal design) measured on routing accuracy/coverage. Not built in this repository.

**F. Falsification test.** If a single blended confidence score routes items with equal or better
accuracy/coverage than the current two-signal design, the distinction is cosmetic.

**G. Evidence that exists.** ADR-007's design rationale (a documented decision, not a measurement).

**H. Evidence still needed.** The blended-vs-unblended ablation itself.

**Verdict: WEAK.** A real but narrow architectural distinction, undermined by the closest
adversarial paper found in the entire sweep, with no ablation showing it matters in practice.

---

## C5 — Permanent T4→T1 promotion via human correction

**A. Claim.** Every Tier-4 human resolution permanently promotes that product to Tier-1 for that
company, with no retraining step — framed in the manuscript as the system's growth mechanism, not
a failure state.

**B. Prior art overlap.** "Human correction changes future system behavior" is a broad, decades-old
genre (active learning, interactive ML, machine teaching — Mosqueira-Rey et al. 2022 survey), but
that literature is almost entirely about the *training* loop, not an inference-time correction that
instantly changes future *routing* for one specific item without retraining. Beede et al. (2020)
independently shows that naive reject-to-human handoffs degrade without such a mechanism — useful
motivating evidence, not a competing method.

**C. What is genuinely different.** The specific mechanism — permanent, per-item, per-company
promotion into an exact-match lookup tier, without retraining — was not found described as such
anywhere in the 79 sources.

**D. Technically meaningful?** Real for this system's own engineering correctness, but the
mechanism itself is a write-through cache keyed by a human-verified label. Its value over that
plainer framing (an exception cache / rule-override table, common in production rule engines
generally) has never been measured against a baseline.

**E. Empirically testable?** Yes — feedback loop enabled vs. disabled over a simulated transaction
stream. See Experiment 3.

**F. Falsification test.** If disabling the loop produces no measurable degradation in automation
rate or accuracy over a simulated multi-period stream, the mechanism's value is undemonstrated. If
a trivial "always trust the most recent human correction, no evidence weighting" baseline performs
equivalently to the actual (evidence-weighted, permanent) promotion rule, the specific design adds
nothing over the naive version.

**G. Evidence that exists.** A description in the tier table / ADR. No before/after measurement
exists anywhere in this repository.

**H. Evidence still needed.** The full before/after + false-promotion-robustness protocol in
Experiment 3.

**Verdict: WEAK.** The highest reviewer-perception risk of the six: even a fully successful
experiment demonstrates the mechanism *works*, which a reviewer may still reasonably characterize
as production-engineering competence rather than a research contribution. Experiment 3 is designed
to produce the evidence needed to argue either way, not to guarantee a positive outcome.

---

## C6 — The combined evidence-driven cascade (Part 1 + Part 2 as one system)

**A. Claim.** The full pipeline — design-time architecture selection (Part 1) driving a runtime
multi-tier cascade with dual confidence signals, an advisory-only LLM tier, and a permanent
feedback loop (Part 2) — is presented as one coherent method whose value exceeds its
individually-precedented parts.

**B. Prior art overlap.** Every individual component is separately precedented (see C1/C2/C3/C5
above, and the LLM-reranking-only constraint and cross-company threshold discussed in
`literature/contribution_status.md` C4/C7). Monteiro et al. (2021, B2-07) is the closest
*structural* analog — an independently-proposed two-phase (design-time selection + runtime
adaptation) shape — but its runtime phase is concept-drift retraining, a materially different
mechanism from a human-escalation cascade.

**C. What is genuinely different.** Zero Tier-1 sources combine all four elements (design-time
label-consistency gate + dual-signal unblended cascade + reranking-only LLM constraint + permanent
human-promotion loop) into one system. This is combination novelty, not component novelty.

**D. Technically meaningful?** Combination novelty is intrinsically the weakest form of novelty
claim available and is routinely discounted by reviewers unless it is paired with demonstrated
empirical value the individual parts lack on their own — i.e. the combined system needs to beat
the best available simple baseline on a real accuracy/cost frontier, not merely differ from it on
paper.

**E. Empirically testable?** Yes — exactly what the cascade experiment (Experiment 2, baselines
B1-B5) is designed to test.

**F. Falsification test.** If a simpler baseline — most damagingly B4, a fixed rules→retrieval→LLM
order with no evidence-driven gating at all — matches ADS-Cascade's accuracy-cost frontier, the
evidence-driven gating step adds no demonstrated value over a static pipeline, and the combination
claim reduces to "a reasonable engineering pipeline," not a research contribution.

**G. Evidence that exists.** A held-out cascade evaluation exists (Tier-1 98.4% accuracy @ 42%
coverage; full cascade 98.1% accuracy @ 42.8% coverage — `EVIDENCE_BASELINE.md`), but it has never
been compared against any of the four simpler baselines on the same data. This is a description of
what the system does, not evidence that it does it better than the alternatives.

**H. Evidence still needed.** The full B1-B5 head-to-head comparison in Experiment 2.

**Verdict: WEAK.** This is the single largest evidentiary gap of the six candidates — no baseline
comparison of any kind has ever been run, despite the combined-system claim being the paper's
central empirical pitch.

---

## C8 — Romanian fiscal-document classification as a case study

**A. Claim.** D406/SAF-T product→GL-account classification is presented as a real-world case study
establishing the method's applicability, in a domain the manuscript implies commercial vendors
"typically ship a single learned classifier chosen up front rather than derived from a measured
determinism distribution" (`TECHNICAL_REPORT.md` §1/§5).

**B. Prior art overlap.** No peer-reviewed academic paper doing SAF-T/D406-specific ML
classification was found — genuine academic under-coverage. But three independent commercial
AP-automation vendors (Ken From Finance, Peakflo, Ramp) publicly describe confidence-tiered
auto-apply/human-review cascades with correction feedback loops for invoice GL-coding *today*, and
one (Ken From Finance) explicitly recommends a pre-deployment historical-consistency audit —
closely mirroring ADS-Cascade's own Part 1.

**C. What is genuinely different.** The academic niche (Romanian D406 specifically) is genuinely
under-served in the peer-reviewed literature.

**D. Technically meaningful?** Not as a methodology claim — this is inherently an application/case-
study contribution, not a technique contribution. Its value is empirical grounding, not novelty.

**E. Empirically testable?** Not applicable as a novelty claim. The underlying production numbers
are already the paper's strongest, most-scrutinized evidence category (`EVIDENCE_BASELINE.md`),
but they support "this works in one real deployment," not "this is a new method."

**F. Falsification test.** The case-study framing itself is not falsifiable in the usual sense. The
narrower factual sub-claim — "vendors don't measure history before choosing" — is already
falsified by Ken From Finance's public materials (B8-04) and needs correcting regardless of any
other finding in this document.

**G. Evidence that exists.** Production figures: 296,648 invoice lines, 169 companies, 91.2%
deterministic, 76,843 mappings, Tier-1 98.4% accuracy @ 42% coverage in live production use
(`reports/phase1_final_report.md`, `EVIDENCE_BASELINE.md`).

**H. Evidence still needed.** A direct, sourced check of what `TECHNICAL_REPORT.md` §5 actually
claims about vendor practice, against B8-04/05/06, before publication — a manuscript-editing task,
not a research question, and out of scope for this Phase C document to perform.

**Verdict: CASE_STUDY_ONLY.** Legitimate and valuable as empirical grounding; illegitimate as
support for a "no comparable practice" novelty claim, which must be corrected regardless of what
Phase C concludes about the other five contributions.

---

## Report conclusions

**1. Which claims are rejected.** C1 (the ADS metric as a novel measurement) is rejected outright —
this was the expected, and now confirmed, outcome. It is mathematically identical to cluster
purity and to the majority-vote-agreement baseline used throughout crowdsourcing/truth-inference
research since 1979. No further work can change this; the only remaining action is citing it
correctly and stripping any novelty language from the manuscript.

**2. Which claims are weak.** Three of six: C3 (dual confidence signals), C5 (T4→T1 promotion), and
C6 (the combined system). All three share the same underlying problem — each rests on a real but
narrow architectural distinction from prior art, and none has any experimental evidence beyond a
single description of "this is what the system does." None has ever been compared against the
simpler alternative that would make the distinction matter (a blended signal for C3, a naive
last-correction cache for C5, a fixed-order pipeline for C6). They are weak because they are
untested, not because they have been tested and failed.

**3. Which are promising.** One: C2, historical decision consistency as a design-time
mechanism-class selector. It is the only claim among the six whose *core empirical content* — not
just its literature positioning — survived Phase B's adversarial search as a narrower but genuine
gap (Phase B's C2b), and it is the only one with a clean, single, falsifiable experimental design
(Experiment 1) capable of turning "promising" into either "confirmed" or "falsified" without
requiring the paper's other claims to be true.

**4. Which deserve experimental validation.** All three of the designed experiments target real
gaps, but they are not equally load-bearing. Experiment 1 (C2) is the paper's single most important
missing result — without it, the paper's central pitch ("historical consistency should guide
architecture choice") is asserted, not shown. Experiments 2 (C6, cascade baselines) and 3 (C5,
feedback loop) are secondary: valuable for the paper's completeness and honesty, but even a
successful outcome only elevates WEAK claims, not REJECTED ones, and a paper can be defensible
without them if scoped honestly as "we built and deployed this system; here is the one causal claim
we tested."

**5. Which are only case-study contributions.** C8. The Romanian D406 domain is legitimate,
valuable, and under-covered academically — but it is evidence *for* the method's applicability, not
a contribution *of* the method. Trying to claim it as a novelty point (via the "no comparable
vendor practice" framing) is the one place in the current manuscript with an easily-checked factual
error that should be fixed independent of everything else in this document.

**6. The minimum experiment set required to make the paper defensible.** One experiment,
non-negotiably: **Experiment 1** (the C2 ADS-band mechanism-performance sweep). Without it, the
paper's only PROMISING claim remains a threshold heuristic exercised twice, not a tested
hypothesis, and the paper's title-level pitch is unsupported by anything beyond two data points.
Experiments 2 and 3 are recommended but not minimum-required: they upgrade WEAK claims toward
PROMISING, they do not create the paper's core contribution. If resources only permit one
experiment, run Experiment 1.

**Overall framing recommendation.** After this stress test, ADS-Cascade does not currently support
a "novel methodology" framing across the board — five of six candidate contributions are REJECTED,
WEAK, or CASE_STUDY_ONLY, and the sixth (C2) is PROMISING but unvalidated. The paper is currently
strongest as **a real production deployment (C8) that motivates and instantiates one specific,
narrow, testable hypothesis (C2)** — not as a general new method with several independent
contributions. If Experiment 1 is run and confirms C2, the paper has a legitimate, evidence-backed
methodological claim to make, scoped narrowly to design-time evidence-driven mechanism selection,
with the production case study as motivating context rather than the main event. If Experiment 1 is
not run, or falsifies C2, the paper should be repositioned as a methodological case study — "here
is a real system, the design decisions it made, and the honest results, including where the
threshold heuristic disagreed with itself across two datasets" — rather than a methodology paper
claiming a validated general procedure. This is not a hedge added to soften a weak scorecard; it is
the conclusion the scorecard actually supports.

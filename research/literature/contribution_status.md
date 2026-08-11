# Contribution Status — Phase B

> Per the mission's explicit stopping condition: **this document does not declare ADS-Cascade
> novel.** It scores each candidate contribution claim against the verified literature in
> `literature_matrix.csv` / `prior_art_map.md` and reports where each one currently stands.
> Phase C (Contribution Positioning) is the phase authorized to draw conclusions and rewrite
> claims; this document hands it a factual starting point, not a verdict.
>
> **Update (2026-08-11, gap-verification pass):** C1 and C4 were originally scored
> NOT_YET_DETERMINED because the main Phase B sweep never targeted them directly. A follow-up
> targeted adversarial pass has now closed both gaps — see `ads_metric_prior_art.md` /
> `ads_metric_prior_art.csv` (Gap 1) and `llm_advisory_prior_art.md` / `llm_advisory_prior_art.csv`
> (Gap 2). Both entries below are updated in place; nothing else in this document changed. C1 moves
> to **CHALLENGED** (the ADS metric is mathematically a known metric under a different name).
> C4 moves to **PARTIALLY_SUPPORTED**, revised down from an implicit assumption of stronger
> novelty (the reranking-only half of the constraint has no defensible novelty claim at all; the
> never-auto-applied half is well-precedented but diffusely sourced; only the full four-part
> combination remains unprecedented as a whole).

## Status definitions used below

- **SUPPORTED** — the adversarial search found no prior art anticipating this claim as stated; it
  appears to survive as a genuine (possibly narrow) point of difference, pending Phase C.
- **PARTIALLY_SUPPORTED** — the *general* pattern the claim rests on is well-precedented (not
  novel on its own), but a narrower, more specific formulation of the claim was not found
  anticipated by anything in this sweep.
- **CHALLENGED** — the literature substantially anticipates, subsumes, or empirically pre-dates
  this claim as currently stated in `TECHNICAL_REPORT.md`; the claim needs to be narrowed,
  reframed, or dropped in its current form.
- **NOT_YET_DETERMINED** — Phase B's search coverage for this specific claim was insufficient to
  make a call (a gap, not a finding); it needs a targeted follow-up search before Phase C treats it
  as settled.

---

## C1 — The Automated Determinism Score (ADS) as a metric

**Current claim** (`TECHNICAL_REPORT.md` §2.2, Contribution 1): a per-product determinism metric —
`max(count_i) / sum(count_i)` over historical label assignments — "turns 'is this dataset
learnable, and by what' into a measured quantity."

**Status: CHALLENGED** *(updated 2026-08-11 — was NOT_YET_DETERMINED; gap now closed, see
`ads_metric_prior_art.md`)*

- **Supporting literature:** none — the gap-verification pass found direct mathematical matches.
- **Challenging literature:** **G1-01/G1-02/G1-03** (cluster purity — Manning, Raghavan & Schütze
  2008; Amigó, Gonzalo, Artiles & Verdejo 2009, DOI `10.1007/s10791-008-9066-8`; Zhao & Karypis
  2003) define, per cluster, `purity = max_j(class-j count) / cluster-size` — the **identical
  closed-form expression** as ADS's `max(c_i)/sum(c_i)`, under the substitution "cluster" ↔
  "an item's historical booking multiset." Independently, **G1-04** (Dawid & Skene 1979) and its
  large descendant literature (**G1-05** Uma et al. 2021; **G1-06** Davani, Díaz & Prabhakaran
  2021) confirm the same quantity — raw majority-vote-agreement proportion — is the universal
  naive baseline in crowdsourcing/truth-inference research since 1979, informally named but never
  independently cited. Two independent literatures converge on the same mathematical identity.
- **Evidence:** `ads_metric_prior_art.csv` rows G1-01 through G1-04; `ads_metric_prior_art.md`
  verdict section.
- **What remains uncertain:** nothing about whether the metric's mathematical construction is
  novel — it is not; this is now a closed question, not an open one. What Phase C must decide is
  how to reframe C1: the metric should be positioned as "cluster purity applied to historical
  per-item label distributions" (citing Manning et al. 2008 / Amigó et al. 2009 / Dawid & Skene
  1979), with any novelty claim relocated entirely to C2b (the metric's *application* as a
  design-time architecture-selection signal), not claimed for the metric itself.

---

## C2 — Design-time architecture selection from historical evidence (general pattern)

**Current claim** (implicit throughout §2.3, and the paper's core framing): measuring dataset
properties before choosing a classification architecture is a novel-ish "evidence-first
discipline."

**Status: CHALLENGED**

- **Supporting literature:** none that treats this as novel.
- **Challenging literature:** B2-02 (Barbudo et al. 2023 — AutoML "workflow composition"), B2-10 /
  B2-11 (Ali & Smith 2006; Khan et al. 2020 — meta-learning for classifier selection, same
  application domain: classification), B7-01 / B7-05 (Idreos & Kraska 2019; Kraska 2021 —
  self-designed / instance-optimized data systems). Four independently-verified, well-cited lines
  of work, spanning three different fields (AutoML, meta-learning, database systems), all doing
  "measure historical evidence once, choose system design before serving" as an established
  research program, one dating to 2006 and the underlying Rice (1976) lineage to nearly 50 years
  ago.
- **Evidence:** `prior_art_map.md` Tier 2, "Design-time architecture selection" subsection.
- **What remains uncertain:** nothing about whether the *general* pattern is novel — it is not.
  What's uncertain is only whether the paper currently over-claims this generality anywhere in its
  prose (Phase E's job to check against `claim_evidence_matrix.csv`-style discipline).

---

## C2b — The *specific* combination: label-consistency evidence → qualitative mechanism-class choice (narrower form of C2)

**Current claim:** not currently stated as a distinct, narrower claim in `TECHNICAL_REPORT.md` —
this is the claim Phase C should consider stating explicitly, since C2 as broadly framed does not
survive (see above).

**Status: PARTIALLY_SUPPORTED**

- **Supporting literature:** none of the 56 sources combines (a) a historical **label-consistency**
  evidence signal specifically (as opposed to workload frequency, cross-validated task performance,
  or generic statistical meta-features) with (b) a choice among qualitatively different **mechanism
  classes** (rules-first vs. embedding-primary vs. hybrid retrieval, as opposed to choosing among
  interchangeable ML algorithms or tuning one model's hyperparameters).
- **Challenging literature:** B8-01 (Jørgensen & Igel 2021) comes closest by empirically showing the
  *cross-company* half of this pattern (see C7 below) in the same domain, but without a rules/LLM
  choice-space or a named metric.
- **Evidence:** `literature_matrix.csv` `ClosestADSComponent = Part 1` rows; `prior_art_map.md`
  Tier 2.
- **What remains uncertain:** whether this narrower framing is precise enough to survive peer
  review, or whether a reviewer familiar with B2-11/B7-05 will still consider it an incremental
  variation rather than a distinct contribution. This is a judgment call for Phase C, not something
  further literature search can resolve.

---

## C3 — Runtime multi-tier confidence cascade (general pattern)

**Current claim** (§2.4, Contribution 2, implicit): a four-tier confidence cascade that routes
between auto-apply, spot-check, human review, and manual entry.

**Status: CHALLENGED**

- **Supporting literature:** none that treats multi-tier confidence-gated cascading itself as novel.
- **Challenging literature:** B3-02 (Chen et al. 2023, FrugalGPT — historically-calibrated LLM
  cascade), B4-01/B4-02/B4-05 (Chow 1970 through the 2024 Hendrickx survey — the entire
  reject-option/selective-classification lineage), B6-02/B6-03/B6-04 (LLM routing/cascading
  literature). Multi-tier, confidence-gated escalation is a mature pattern across at least three
  independent sub-fields.
- **Evidence:** `prior_art_map.md` Tier 2 and Tier 3, "Runtime confidence cascade" subsections.
- **What remains uncertain:** nothing about the general pattern. See C3b for the narrower surviving
  claim.

---

## C3b — Two independently-tracked, never-blended confidence signals (narrower form of C3)

**Current claim** (§2.4): "extraction_confidence... and classification_confidence... computed
**independently and never blended**," explicitly justified as avoiding conflating opposite failure
modes (ADR-007).

**Status: PARTIALLY_SUPPORTED**

- **Supporting literature:** none of the 56 sources describes two *architecturally separate*
  subsystems' confidence signals (an OCR/extraction provider vs. a classification pipeline) kept
  unblended through a routing decision.
- **Challenging literature:** B5-06 (Liu, Gallego & Barbieri 2022) is a genuine near-miss — it uses
  two related uncertainty terms to modulate one deferral decision, which weakens a claim that
  "more than one confidence signal informing routing" is itself new — but both of its terms come
  from the *same* model's internal uncertainty, not from two separate subsystems as in ADS-Cascade.
- **Evidence:** `literature_matrix.csv` row B5-06; `prior_art_map.md` Tier 3.
- **What remains uncertain:** whether "architecturally separate, never-blended" is a meaningful
  enough distinction from "two related uncertainty terms from one model" to hold up under review,
  or whether a reviewer would treat both as instances of the same underlying idea (multi-signal
  deferral). Recommend the manuscript cite and explicitly distinguish B5-06 rather than claim this
  point silently.

---

## C4 — LLM constrained to re-ranking retrieved candidates only, never auto-applied

**Current claim** (§2.4, Contribution 2): "an LLM call, when it happens, is fed the cascade's
already-retrieved candidate accounts and asked to re-rank precedent, never asked to classify from a
blank product string," and LLM proposals are "never auto-applied."

**Status: PARTIALLY_SUPPORTED** *(updated 2026-08-11 — was NOT_YET_DETERMINED; gap now closed, see
`llm_advisory_prior_art.md`)*

- **Supporting literature:** none of the 16 gap-verification sources describes all four
  sub-constraints assembled together (candidates-only + never-blank-slate + never-auto-applied +
  100%-human-routed, as the terminal tier of a broader deterministic cascade).
- **Challenging literature, by sub-constraint:**
  - *Candidates-only / never blank-slate*: **CHALLENGED outright.** **G2-01** (Sun et al. 2023,
    "RankGPT," DOI `10.18653/v1/2023.emnlp-main.923`, 590 citations) and its large descendant
    literature (**G2-02, G2-03, G2-04**) establish LLM-reranks-a-pre-fetched-candidate-list as
    commodity IR technique since 2023. No defensible novelty claim is available for this half in
    isolation.
  - *Never auto-applied / always human-routed*: well-precedented as a **general principle**, but
    diffusely sourced across independent literatures — automation-bias research two decades old
    (**G2-15**, Cummings 2004), clinical decision support (**G2-16**, Khera et al. 2023, JAMA),
    learning-to-defer (**G2-08/G2-09/G2-10/G2-11**), and explicit authority taxonomies (**G2-05**
    Singh & Szajnfarber 2025; **G2-06** Hu et al. 2025). Too diffuse to cite as a single "prior
    art" paper, but not a gap either — it is field-standard doctrine.
  - *The full four-part combination*: **not found assembled anywhere.** Closest single-paper
    matches (**G2-09** Strong, Men & Noble 2025 — LLM + human deferral, but classifies directly
    rather than reranking; **G2-10** Lykouris & Weng 2024 — cascade shape, but permits
    high-confidence auto-decisions without human review, the opposite of ADS-Cascade's invariant)
    each capture roughly half the combination.
- **Evidence:** `llm_advisory_prior_art.csv` full table; `llm_advisory_prior_art.md` verdict
  section (verdict: **C — partially established**).
- **What remains uncertain:** whether the surviving narrow claim (the specific four-part
  combination, not any individual piece) is precise and defensible enough to state in the
  manuscript at all, given that its two largest components (reranking-only; advisory-only) are
  each independently well-precedented. This is a Phase C framing decision, not something further
  search can resolve.

---

## C5 — Human correction (T4) permanently promotes an item to Tier 1 (feedback loop)

**Current claim** (§2.4, Tier table): "every T4 resolution permanently promotes that product to T1
for that company" — framed as "the knowledge base's growth mechanism, not a failure state."

**Status: PARTIALLY_SUPPORTED**

- **Supporting literature:** none found describes this *specific* mechanism (permanent, per-item,
  per-company promotion into an exact-match tier, without model retraining).
- **Challenging literature:** B5-03 (Mosqueira-Rey et al. 2022, HITL survey) establishes that
  "human correction changes future system behavior" is a broad, decades-old genre (active learning,
  interactive ML, machine teaching) — but that literature is almost entirely about the *training*
  loop, not an inference-time correction that instantly changes future *routing* for one specific
  item without retraining. B4-10 (Beede et al. 2020) provides motivating field evidence for *why*
  such a mechanism is needed (naive reject-to-human handoffs fail without one) but doesn't propose
  one.
- **Evidence:** `literature_matrix.csv` rows B5-03, B4-10; `terminology_map.md` "Human correction
  permanently promotes" section.
- **What remains uncertain:** whether a reviewer would characterize this specific mechanism as a
  research contribution at all, or as a well-known production-engineering pattern (an
  exception-cache / rule-override, common in rule-engine systems generally) dressed in ML-paper
  language. This is a genuine risk flagged for Phase C's judgment, not resolved by further search.

---

## C6 — The Part 1 + Part 2 combination as one integrated system

**Current claim** (Abstract, throughout): the two-phase pipeline — determinism-driven architecture
selection followed by a confidence cascade with human feedback — presented as a single coherent
method.

**Status: PARTIALLY_SUPPORTED**

- **Supporting literature:** no single source among the 56 combines a design-time,
  historical-evidence-driven architecture-selection phase with a runtime multi-tier human-escalation
  cascade with a feedback loop back into the same evidence base. B2-07 (Monteiro et al. 2021) is the
  closest **structural** analog — it independently proposes a two-phase (design-time selection +
  runtime adaptation) shape — but its runtime phase handles concept-drift retraining, a different
  mechanism entirely.
- **Challenging literature:** every component individually is well-precedented (see C2, C3, C5
  above); a "novel combination of known parts" claim is intrinsically the weakest form of novelty
  claim and is frequently discounted by reviewers unless paired with new empirical value.
- **Evidence:** `prior_art_map.md` headline finding (Tier 1 = 0 sources); B2-07 in Tier 3.
- **What remains uncertain:** whether Phase C should lean on this combination claim at all, given
  its structural weakness as a novelty argument, or whether the paper's actual defensible
  contribution is better framed as empirical (a real production case study + honest
  production-vs-synthetic evaluation, including the R3 threshold-sensitivity finding) rather than
  methodological novelty. This is squarely a Phase C framing decision.

---

## C7 — Cross-company consistency threshold as the reason for hybrid (not global) retrieval

**Current claim** (§2.3, R1): cross-company consistency of 0.695 (production) "rules out a
global-only classifier" and justifies the hybrid per-company/global architecture.

**Status: CHALLENGED**

- **Supporting literature:** none that treats this specific empirical justification as novel.
- **Challenging literature:** B8-01 (Jørgensen & Igel 2021) measures and reports the **exact
  phenomenon** in the **same application domain** (financial transaction-to-account
  classification): a global classifier generalizes far worse across companies than per-company
  models (64.6% leave-one-company-out vs. 80.5% within-company). Published 2021, three years before
  this finding would appear in ADS-Cascade's own report.
- **Evidence:** `literature_matrix.csv` row B8-01; `terminology_map.md` "Cross-company consistency
  threshold" section.
- **What remains uncertain:** nothing about whether the underlying empirical phenomenon was already
  documented — it was. What ADS-Cascade adds beyond B8-01 (a named, thresholded, versioned
  consistency *metric* driving an explicit decision *procedure*, rather than a one-off reported
  accuracy gap) is a legitimate but narrower claim Phase C should state precisely.

---

## C8 — Novelty of the application domain (Romanian fiscal-document / invoice GL-account classification)

**Current claim** (§1, Introduction; §5, Related Work): implies commercial invoice-classification
vendors "typically ship a single learned classifier... chosen up front rather than derived from a
measured determinism distribution."

**Status: PARTIALLY_SUPPORTED**

- **Supporting literature (academic under-coverage):** no peer-reviewed paper doing SAF-T/Romanian
  D406-specific ML classification was found by the B6/B8 agent despite a dedicated search pass —
  this specific niche does appear genuinely academically under-served.
- **Challenging literature (industry coverage):** B8-04, B8-05, B8-06 (Ken From Finance, Peakflo,
  Ramp — three independent AP-automation vendors) all describe, in commercial production today,
  confidence-tiered auto-apply/human-review cascades with correction feedback loops for invoice
  GL-coding; B8-04 specifically also independently recommends a pre-deployment historical-
  consistency audit. This directly contradicts a claim that vendors "choose a classifier up front
  rather than deriving it from measured data" — at least one vendor's public materials describe
  almost exactly that measurement step.
- **Evidence:** `prior_art_map.md` Tier 2, "Application domain" subsection; `literature_matrix.csv`
  rows B8-04/05/06.
- **What remains uncertain:** whether `TECHNICAL_REPORT.md` §5's characterization of commercial
  vendors was based on actually surveying vendor practice or was an unverified assumption — this
  needs a direct check against §5's sourcing before Phase E, since B8-04 in particular appears to
  falsify the "vendors don't measure before choosing" framing as currently written. Academic
  novelty of the *domain* survives; "no comparable practice exists" does not.

---

## Summary table

| ID | Claim | Status |
|---|---|---|
| C1 | ADS metric itself | **CHALLENGED** *(was NOT_YET_DETERMINED)* |
| C2 | Design-time architecture selection (general pattern) | CHALLENGED |
| C2b | ...specific label-consistency → mechanism-class combination | PARTIALLY_SUPPORTED |
| C3 | Runtime multi-tier confidence cascade (general pattern) | CHALLENGED |
| C3b | ...two independently-tracked, never-blended signals | PARTIALLY_SUPPORTED |
| C4 | LLM constrained to re-ranker-only, never auto-applied | **PARTIALLY_SUPPORTED** *(was NOT_YET_DETERMINED)* |
| C5 | Human correction permanently promotes item to T1 | PARTIALLY_SUPPORTED |
| C6 | Part 1 + Part 2 as one integrated combination | PARTIALLY_SUPPORTED |
| C7 | Cross-company consistency → hybrid retrieval | CHALLENGED |
| C8 | Application-domain novelty | PARTIALLY_SUPPORTED |

**No candidate contribution scores a clean SUPPORTED, as of the 2026-08-11 gap-verification
update.** Three now score CHALLENGED outright (C1, C2, C3 — each as broadly stated in the current
manuscript prose; C1's metric-construction claim is now a *closed* question, not narrowable the
way C2/C3 are via C2b/C3b). Zero claims remain NOT_YET_DETERMINED — both gaps flagged at the end of
the main Phase B sweep (C1, C4) have been closed by the targeted follow-up pass documented in
`ads_metric_prior_art.md` and `llm_advisory_prior_art.md`. Phase C now has a complete, gap-free
evidence base to work from.

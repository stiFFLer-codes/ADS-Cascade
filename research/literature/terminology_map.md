# Terminology Map — ADS-Cascade vs. Established Literature

> Maps ADS-Cascade's internal vocabulary against the terminology the literature sweep actually
> found. Where no real equivalence exists, this says so explicitly rather than forcing one — per
> the mission's instruction not to force equivalence where none exists.

## How to read this

Each entry: **ADS-Cascade term** → what it means in this project → closest established term(s) →
research family → how close the equivalence actually is, and why.

---

### "Automated Determinism Score (ADS)"

**ADS-Cascade meaning:** per-product empirical probability that a historical occurrence was booked
to its modal (most common) account — `max(count_i) / sum(count_i)` over the item's full historical
label distribution.

> **Update (2026-08-11, gap-verification pass):** the label-agreement gap flagged below as
> unsearched has now been closed — see `ads_metric_prior_art.md`. The equivalence is **not** low;
> it is a direct mathematical match. The entry below is retained for its original reasoning but is
> superseded by the finding immediately following it.

**Established terms found (post gap-verification):**
- **"Cluster purity"** (Manning, Raghavan & Schütze 2008, *Introduction to Information Retrieval*
  Ch. 16.3; Amigó, Gonzalo, Artiles & Verdejo 2009, *Information Retrieval*, DOI
  `10.1007/s10791-008-9066-8`) — **mathematically identical**: `purity = max_j(class-j count) /
  cluster-size`, the same closed-form expression as ADS under "cluster" ↔ "item's historical
  booking multiset." Not an analogy. This is now the term ADS should be positioned against
  explicitly in the manuscript, not silently.
- **Raw majority-vote-agreement proportion** (informal, no single dedicated citation — circulates
  throughout the Dawid & Skene 1979 crowdsourcing/truth-inference descendant literature as the
  standard naive baseline; also appears undercited in the Fleiss 1971 inter-rater-reliability
  lineage as "percent agreement with the majority label") — also mathematically identical to ADS,
  and closer in unit-of-analysis (per-item, repeated historical labels) than cluster purity, but
  lacking cluster purity's clean, dedicated citation. Both should be cited together — see
  `ads_metric_prior_art.md` for full reasoning.

**Original (superseded) reasoning, retained for the record:**
- **"Meta-feature" / "landmarking feature"** (meta-learning literature, B2 — Rivolli et al. 2022,
  Smith-Miles 2009) — the general category ADS belongs to (a summary statistic computed from
  historical data before a decision); still correct as a genus-level classification, just no
  longer the *closest* match now that cluster purity has been found.
- **"Empirical hardness"** (B1 — Xu et al. 2008, SATzilla) is a false-friend: it predicts *runtime*
  from instance features via a trained regression model, not *label consistency* from a counted
  historical distribution. Don't conflate the two despite both being "historical-data-derived
  per-item statistics."

**Equivalence strength:** **High** (mathematically identical to cluster purity and to the raw
majority-vote-agreement proportion baseline, confirmed by two independent literatures). Previously
recorded as Low-Medium before the gap-verification pass closed this question — see
`contribution_status.md` C1, now CHALLENGED.

---

### "Design-time architecture selection" (ADS-Cascade Part 1)

**ADS-Cascade meaning:** a one-time, pre-deployment decision procedure that thresholds aggregate
ADS/consistency statistics to choose the overall system composition (rules-first vs.
embedding-primary vs. hybrid retrieval) before any classifier is built.

**Closest established terms:**
- **"Algorithm Selection Problem"** (Rice 1976, B1) — the foundational ancestor vocabulary, but
  Rice's framework selects a single algorithm per problem *instance*, not a whole system's
  architecture once per *deployment*. One level of abstraction below ADS-Cascade's Part 1.
- **"Workflow composition"** (Barbudo et al. 2023, B2) — the field's own successor term for
  algorithm selection, and the closest terminological match found — but in the AutoML literature
  this means automated search over a combinatorial pipeline-configuration space optimized for
  benchmarked task performance, not a hand-designed threshold rule driven by an interpretable
  historical-consistency metric.
- **"Meta-learning for classifier/algorithm selection"** (Ali & Smith 2006, Khan et al. 2020, B2)
  — the closest match found *outside databases*: design-time, historical-evidence-driven,
  same domain (classification). Selects a single ML algorithm via generic statistical
  meta-features, not a rules/embedding/LLM mechanism class via a label-consistency metric.
- **"Self-designed / instance-optimized systems"** (Idreos & Kraska 2019, Kraska 2021, B7) — the
  strongest *structural* analog: measure historical evidence once, choose system composition
  before serving. But the evidence type is workload/query *frequency* statistics, not label
  *consistency*, and the temporal structure is explicitly continuous/self-adapting rather than a
  one-shot gate in most of this literature (Idreos & Kraska's own stated thesis is to *remove* the
  one-time human design step).
- **"CASH problem" (Combined Algorithm Selection and Hyperparameter optimization)** (Thornton et
  al. 2013, B2) — design-time, one-shot, but selects (algorithm, hyperparameters), not a
  qualitative architecture class, and is driven by cross-validated performance search, not a
  historical-consistency threshold rule.

**Equivalence strength:** Medium. No single established term captures "one-time, pre-deployment,
historical-label-consistency-driven, qualitative mechanism-class selection" as a unit. The closest
composite is: Rice's *selection* + Barbudo's *workflow/architecture* framing + a
historical-consistency (not performance-search) *evidence signal* that appears novel in
combination, per this sweep.

---

### "Runtime confidence cascade" (ADS-Cascade Part 2, T1–T4)

**ADS-Cascade meaning:** per-item routing at inference time through four tiers (auto-apply /
auto-apply-with-spot-check / human review / manual entry), gated by two independently-tracked,
never-blended confidence signals (extraction confidence, classification confidence).

**Closest established terms:**
- **"Reject option" / "selective classification"** (Chow 1970, El-Yaniv & Wiener 2010, B4) — the
  foundational single-threshold accept/reject ancestor. ADS-Cascade's cascade is a multi-tier,
  multi-signal elaboration of this lineage, not a new primitive.
- **"Model cascade" / "LLM cascade"** (Chen et al. 2023 — FrugalGPT, B3) — the closest *structural*
  match: a historically-calibrated multi-tier escalation path. FrugalGPT never involves a human
  tier; its terminal escalation is always another model.
- **"Learning to defer" (L2D)** (Madras et al. 2018, Mozannar & Sontag 2020, B5) — the closest
  match for the *human-escalation* half specifically: a trained/rule-based function deciding
  whether to defer to a human, informed by historical decision data. The L2D literature's unit of
  decision is a single binary defer/not-defer, not a 4-tier structure, and none of the surveyed
  L2D papers describe a permanent per-item promotion mechanism.
- **"Early exit" / "split computing"** (Matsubara et al. 2022, B6) — same tiered-confidence *shape*,
  applied within a single model's own layers (compute-depth routing) rather than across
  heterogeneous mechanism types. A false-friend if cited without this distinction.
- **"Query routing" (LLM routing literature)** (RouteLLM, Hybrid LLM, cascade routing — B3/B6) —
  same runtime-routing shape, applied to choosing among multiple LLMs of varying cost/capability,
  not among heterogeneous mechanism *types* (rules vs. retrieval vs. LLM vs. human).

**Equivalence strength:** Medium-High for the general shape (multi-tier confidence-gated escalation
is well-precedented); Low for the specific combination (dual independently-tracked signals +
heterogeneous mechanism-class tiers + terminal human tier + permanent feedback promotion) — no
single paper in this sweep combines all four.

---

### "Two independently-tracked confidence signals, never blended" (OCR/extraction confidence vs. classification confidence)

**Closest established term:** No exact match found. The closest precedent is **Liu, Gallego &
Barbieri (2022)**'s uncertainty-aware learning-to-defer loss (B5-06), which uses two related
uncertainty terms to modulate a deferral decision — but both terms there derive from the *same*
model's internal uncertainty estimates, not from two architecturally separate subsystems (an OCR
provider and a classification pipeline). This is the strongest single adversarial precedent found
and should be explicitly distinguished from ADS-Cascade's claim, not ignored.

**Equivalence strength:** Low. Genuinely narrower/more specific than anything found.

---

### "LLM re-ranks retrieved candidates only, never classifies from blank input, never auto-applied" (Tier-3 constraint)

> **Added 2026-08-11, gap-verification pass.** See `llm_advisory_prior_art.md` for full reasoning.

**Closest established terms, by sub-piece:**
- **"LLM as re-ranking agent"** (Sun et al. 2023, "RankGPT," EMNLP, DOI
  `10.18653/v1/2023.emnlp-main.923`, and a large descendant literature: RankZephyr, RankVicuna,
  RankLLaMA, FIRST, ListT5, PE-Rank, REARANK) — **essentially exact match** for the
  "candidates-only, never blank-slate" half. This is commodity information-retrieval technique by
  2023, not a novel restriction, and should be cited as the direct methodological ancestor of
  ADS-Cascade's Tier-3 mechanism.
- **"AI Supports Human Decisions" mode** (Hu, Navas, Gaube, Mozannar, Taylor, Dvijotham &
  Bondi-Kelly 2025, *AI Magazine*, DOI `10.1002/aaai.70043`) and **"human selector" architecture**
  (Singh & Szajnfarber 2025, *Systems Engineering*, DOI `10.1002/sys.70024`) — the closest named,
  citable general vocabulary for "AI proposes, human always decides," for the "never auto-applied"
  half. Neither is LLM- or reranking-specific.
- **"Learning to defer" (L2D)** (Mozannar & Sontag 2020 and descendants) — the standard academic
  term of art for confidence-gated human handoff generally; the field a reviewer would expect
  ADS-Cascade's Tier 3 positioned against.
- **"Automation bias" / advisory-automation literature** (Cummings 2004; Khera et al. 2023, JAMA)
  — establishes "automation only recommends, operator/clinician decides" as 20+-year-old,
  heavily-cited human-factors and clinical-decision-support doctrine.

**No single term captures the full four-part combination** (candidates-only + never-blank-slate +
never-auto-applied + 100%-human-routed, as the terminal tier of a broader deterministic cascade).
Each piece, individually, has a name and precedent; the assembly does not.

**Equivalence strength:** High for the individual pieces (especially LLM-as-reranker, which has no
defensible novelty claim available at all); Low-Medium for the full combination as assembled in
this cascade position.

---

### "Human correction permanently promotes an item to Tier 1" (T4 → T1 feedback loop)

**Closest established terms:**
- **"Active learning" / "interactive ML" / "machine teaching"** (Mosqueira-Rey et al. 2022, B5) —
  the broad genus of "human correction changes future system behavior," but this literature is
  almost entirely about the *training* loop (query strategies, label acquisition for retraining),
  not an inference-time correction that instantly and permanently changes future *routing* for
  that specific item without retraining.
- **Exception-cache / rule-override pattern** (not an academic literature match — a long-standing
  production-systems engineering pattern: a correction becomes a cached exact-match rule going
  forward). No academic citation found for this specifically; it plausibly reads to a reviewer as
  a well-known operational engineering choice rather than a research contribution in itself.

**Equivalence strength:** Low as a research contribion; the *general* idea (corrections update
future behavior) is old and broad, but the specific mechanism (permanent T1 promotion, keyed
per-item-per-company, without retraining) was not found named or evaluated anywhere in this sweep.

---

### "Cross-company consistency threshold" (R1 — the retrieval-strategy decision rule)

**Closest established term:** No named term in the algorithm-selection or AutoML literature. The
closest match is empirical, not terminological: **Jørgensen & Igel (2021)** (B8-01) measure and
report the *exact phenomenon* this threshold encodes (global classifiers generalize far worse
across companies than per-company models: 64.6% vs. 80.5% in their data) in the *same application
domain* — but they do not name or formalize a "cross-company consistency" statistic or threshold
rule; they report the accuracy gap directly and choose an architecture from it informally.

**Equivalence strength:** Medium (empirically anticipated in the same domain, not formally named).

---

## Terms this project should consider adopting

Based on where the closest established vocabulary sits, `TECHNICAL_REPORT.md` §5 (Related Work)
should likely adopt, not avoid, these established terms when positioning ADS-Cascade — using them
precisely and then stating the delta, rather than inventing parallel vocabulary that obscures the
lineage:

- **"Algorithm Selection Problem"** (Rice 1976) — as the acknowledged root, with an explicit note
  that ADS-Cascade operates at the *architecture*/*workflow* level Barbudo et al. (2023) describe
  the field moving toward, not the per-instance level Rice originally posed.
- **"Workflow composition"** (Barbudo et al. 2023) — as the AutoML-literature term closest to
  ADS-Cascade's Part 1, explicitly distinguished by evidence type (label-consistency vs. benchmarked
  performance search) and mechanism (interpretable threshold rule vs. automated search).
- **"Meta-feature"** (Rivolli et al. 2022) — as the genus ADS belongs to, with ADS positioned as a
  specific, previously-uncataloged species (label-consistency/determinism) rather than claiming a
  wholly new category of thing.
- **"Reject option" / "selective classification"** (Chow 1970 lineage) and **"learning to defer"**
  (Madras 2018 / Mozannar & Sontag 2020 lineage) — as the acknowledged roots of Part 2, with the
  specific delta (dual independent signals, heterogeneous mechanism-class tiers, permanent
  feedback promotion) stated explicitly rather than implied by silence.
- **"Model cascade"** (Chen et al. 2023 — FrugalGPT) — as the closest LLM-systems-literature term
  for the overall T1–T4 structure, again with the human-tier and feedback-loop delta stated
  explicitly.
- **"Instance-optimized systems"** (Kraska 2021) — worth citing as the closest non-ML research
  *program* analog for the overall project philosophy, useful for framing even where the specific
  mechanism differs.
- **"Cluster purity"** (Manning, Raghavan & Schütze 2008; Amigó et al. 2009) — *(added
  2026-08-11)* as the direct mathematical citation for ADS's formula; alongside the Dawid & Skene
  (1979) crowdsourcing-baseline lineage for the metric's closest unit-of-analysis match. Silence on
  this point is the single highest-risk omission a literature-aware reviewer would flag.
- **"LLM as re-ranking agent"** (Sun et al. 2023, "RankGPT") — *(added 2026-08-11)* as the direct
  methodological ancestor of the Tier-3 cascade mechanism; and **"learning to defer"** /
  **"automation bias"** vocabulary (Mozannar & Sontag 2020; Cummings 2004) for the never-auto-
  applied design principle — again, both should be cited explicitly rather than left implicit.

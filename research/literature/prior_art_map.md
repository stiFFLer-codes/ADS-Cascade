# Prior-Art Map — Phase B

> Organizes all 56 sources in `literature_matrix.csv` into five overlap tiers. Tier assignment
> comes directly from each source's `OverlapType`/`OverlapStrength` columns, computed independently
> by four adversarial research passes (see `search_protocol.md`). For every Tier 1/2 entry, the
> "why" is stated explicitly, per the mission's requirement — not left as a label.

## Headline finding

**Zero sources qualify as Tier 1 direct prior art for ADS-Cascade as a *whole combined system*** —
no single paper describes (a) a per-item historical label-consistency score, (b) aggregated and
thresholded once, pre-deployment, to select a qualitative system-architecture class, (c) paired
with a runtime cascade that keeps two independently-tracked confidence signals unblended, gates an
LLM to re-ranking-only, and (d) permanently promotes human-corrected items into the historical
evidence base without retraining. This whole-combination finding is unchanged by the 2026-08-11
gap-verification pass.

> **Update (2026-08-11):** the gap-verification pass (see `ads_metric_prior_art.md` and
> `llm_advisory_prior_art.md`) found direct prior art at the **component** level that the original
> sweep missed, because it never searched the label-noise/inter-annotator-agreement literature.
> **The ADS metric itself now has Tier 1 (direct prior art)** — see the new subsection below.
> This does not change the whole-system finding above (no paper combines all four elements), but it
> materially weakens the metric-level contribution claim (C1 in `contribution_status.md`, now
> CHALLENGED) and should be read alongside it.

---

## Tier 1 — Direct prior art

**None found for ADS-Cascade as a whole system.** This means ADS-Cascade's contribution claim
cannot rest on "this exact method exists already, cite it" being false — but it also means the
claim must be argued precisely as a *combination* novelty, not a *component* novelty, because
nearly every component has close Tier 2 prior art (below) — and, as of the 2026-08-11
gap-verification pass, **one component has direct Tier 1 prior art of its own**:

### Component-level Tier 1: the ADS metric

- **G1-01/G1-02/G1-03 — Cluster purity** (Manning, Raghavan & Schütze 2008, *Introduction to
  Information Retrieval*, Ch. 16.3; Amigó, Gonzalo, Artiles & Verdejo 2009, *Information
  Retrieval*, DOI `10.1007/s10791-008-9066-8`; Zhao & Karypis 2003). *Why direct, not strong-overlap:*
  `purity(cluster) = max_j(class-j count) / cluster-size` is the **identical closed-form
  expression** as `ADS(p) = max(c_i)/sum(c_i)`, under the substitution "cluster" ↔ "an item's
  historical booking multiset." Not an analogy — the same formula, relabeled unit of analysis,
  independently confirmed by three separate citation lineages (IR-textbook, formal-metrics-paper,
  CLUTO-toolkit). See `ads_metric_prior_art.md` for full reasoning.

This is a genuine Tier 1 finding **at the metric level only** — it does not extend to
ADS-Cascade's *use* of the metric (design-time architecture-selection signal), which remains
without direct prior art; see the Tier 2 entry for Dawid & Skene (1979) below and
`contribution_status.md` C1/C2b for the resulting claim-scoping implications.

---

## Tier 2 — Strong conceptual overlap (17 sources)

### Design-time architecture selection (ADS-Cascade Part 1)

- **B2-02 — Barbudo, Ventura & Romero (2023), "Eight years of AutoML"** (Knowledge and Information
  Systems). *Why:* states verbatim that "the algorithm selection problem has gradually been
  superseded by the challenge of workflow composition" — the single closest terminological echo of
  ADS-Cascade's own framing found anywhere in this sweep. Distinguishing factor: Barbudo's
  "workflow composition" is automated, benchmarked-performance-driven search over a combinatorial
  pipeline space; ADS-Cascade's Part 1 is an interpretable, hand-designed threshold rule driven by
  a historical label-consistency metric. Must be explicitly cited and distinguished, not ignored.
- **B2-11 — Khan, Zhang, Rehman & Ali (2020), meta-learning for classifier selection survey**
  (IEEE Access). *Why:* the closest match found to "measure historical evidence once, then pick an
  architecture before serving traffic" **outside databases**, and in ADS-Cascade's own domain
  (classification). Distinguishing factor: selects a generic ML algorithm via statistical
  meta-features, not a rules/embedding/LLM mechanism class via label-consistency.
- **B2-10 — Ali & Smith (2006)**, same genus as B2-11, 14 years earlier — confirms the pattern is
  20+ years old, not merely recently converged upon.
- **B7-01 — Idreos & Kraska (2019), self-designed/learned data systems** (SIGMOD). *Why:*
  strongest **non-ML structural analog** — measure historical evidence, choose whole-system
  composition. Distinguishing factor: evidence type is workload/query *frequency*, not label
  *consistency*; and the paper's own thesis is *continuous* self-adaptation, explicitly rejecting a
  one-time human design gate — the opposite temporal structure from ADS-Cascade's stated "ONE TIME
  before deployment."
- **B7-05 — Kraska (2021), "Towards Instance-Optimized Data Systems"** (PVLDB). *Why:* names the
  closest research *program* to ADS-Cascade's overall philosophy ("systems that self-adjust to a
  given workload and data distribution"). Distinguishing factor: performance/cost specialization to
  workload distribution, not label-consistency-driven choice between qualitatively different
  architectures for a classification task.
- **B7-06 — Pavlo et al. (2017), Peloton self-driving DBMS** (CIDR) — flagged strong overlap *as
  contrast*: independently confirms the DB-systems literature's dominant philosophy is continuous
  reconfiguration, not a one-shot gate, strengthening the case that ADS-Cascade's one-time-gate
  choice is a deliberate, citable departure from the nearest systems-literature tradition rather
  than an oversight.

### Runtime confidence cascade (ADS-Cascade Part 2)

- **B3-02 — Chen, Zaharia & Zou (2023/2024), FrugalGPT** (TMLR). *Why:* the single closest
  **structural** match to Part 2 found anywhere — a multi-tier cascade, composed and calibrated
  from historical accuracy data, applied per query. Distinguishing factor: FrugalGPT never involves
  a human tier at all; its terminal escalation is always another (more expensive) LLM. ADS-Cascade's
  cascade exists specifically to gate access to a human.
- **B3-06 — Yue et al. (2023), LLM cascades with "answer consistency"** (arXiv). *Why:* a near-miss
  on ADS-Cascade's Tier-1 "near-unanimous match" logic — but the consistency signal is computed
  live via repeated sampling of the *same model right now*, not from a historical record of
  repeated *human* labeling of the same item over time. Different sense of "consistency."
- **B4-02 — El-Yaniv & Wiener (2010), foundations of selective classification** (JMLR). *Why:*
  originates the risk-coverage formalism the entire modern reject-option field cites.
  Distinguishing factor: single reject threshold with theoretical guarantees, no multi-tier
  structure, no dual signals, no design-time architecture selection, no human-correction loop.
- **B4-05 — Hendrickx et al. (2024, journal; arXiv 2021), reject-option survey** (Machine
  Learning). *Why:* the most recent, most comprehensive survey of the entire reject-option field
  found (72 citations) — and it contains nothing isomorphic to ADS-Cascade's specific 4-tier +
  historical-determinism combination. This functions as a **negative-result check**: if the
  combination were already documented, this survey would very likely reference it.
- **B4-09 — Kompa, Snoek & Beam (2021), "Second opinion needed"** (npj Digital Medicine). *Why:*
  closest B4 match to ADS-Cascade's human-escalation *framing* specifically (abstention as
  explicit escalation to a clinician). Distinguishing factor: a general perspective/argument piece,
  not a specific mechanism — no multi-tier cascade, no dual-signal architecture, no
  design-time selection procedure, no permanent-promotion mechanism.
- **B5-01 — Madras, Pitassi & Zemel (2018), "Predict Responsibly" (learning to defer)** (NeurIPS).
  *Why:* closest single paper to "runtime deferral informed by [a specific] human's past
  decisions." Distinguishing factor: a single binary defer/not-defer decision, end-to-end trained,
  not a 4-tier structure; no design-time whole-architecture-selection analog; no permanent-promotion
  mechanism.
- **B5-02 — Mozannar & Sontag (2020), consistent L2D estimators** (ICML). *Why:* the foundational
  paper the entire modern learning-to-defer sub-literature (Verma & Nalisnick 2022, Keswani et al.
  2021, Liu et al. 2022, and others found in this sweep) builds directly on — establishes that
  "defer decisions informed by past expert behavior" is a mature, heavily-elaborated research
  program. None of its extensions found here add a design-time architecture-selection layer or a
  permanent per-item promotion mechanism — that combination looks like an actual gap.
- **B6-01 — Kierner, Kucharski & Kierner (2023), hybrid rules+ML architecture taxonomy**
  (J. Biomedical Informatics). *Why:* catalogs 71 existing hybrid rule+ML clinical-decision
  architectures chosen at design time — establishes "hybrid architecture chosen at design time" as
  a populated space. Distinguishing factor: none of the 71 reviewed systems use a determinism-score-
  driven selection criterion; this is a taxonomy of outcomes, not a method that anticipates ADS.
- **B6-02 — Dekoninck, Baader & Vechev (2024), unified routing+cascading for LLMs** (arXiv). *Why:*
  provides a more rigorous, theoretically-optimal formalization of exactly the confidence-gated
  escalation pattern ADS-Cascade's Part 2 implements informally. Distinguishing factor: purely
  runtime, among LLMs of varying size, no rules-vs-ML distinction, no human tier, no design-time
  phase.

### Application domain (ADS-Cascade's specific niche)

- **B8-01 — Jørgensen & Igel (2021), cross-company financial transaction classification**
  (Intelligent Systems in Accounting, Finance and Management). *Why:* empirically demonstrates the
  **exact phenomenon** ADS-Cascade's cross-company-consistency threshold rule encodes (global
  classifiers generalize far worse across companies: 64.6% vs. 80.5%), **in the same application
  domain**. Distinguishing factor: pure ML, no rules or LLM layer; reports the accuracy gap
  directly rather than formalizing a named, thresholded consistency metric or a rules-vs-ML-vs-LLM
  decision procedure.
- **B8-04 — "Ken From Finance" practitioner blog, invoice GL-coding automation** (industry, no
  DOI). *Why:* the single closest artifact found in the **entire sweep** to ADS-Cascade's combined
  two-part shape — pre-deployment historical vendor-coding-consistency audit *and* a 3-tier runtime
  confidence cascade, independently arrived at, in the same domain. Distinguishing factor: informal,
  no formal aggregate score, no rules-vs-ML-vs-LLM architecture-selection procedure, no academic
  rigor or evaluation. This is folk/industry wisdom, not a research method — but its existence
  substantially weakens any claim that the *general shape* of ADS-Cascade is novel to this domain.

---

## Tier 2 additions from the 2026-08-11 gap-verification pass (12 sources)

Full detail in `ads_metric_prior_art.md` / `ads_metric_prior_art.csv` and
`llm_advisory_prior_art.md` / `llm_advisory_prior_art.csv`.

### ADS metric (Gap 1)

- **G1-04 — Dawid & Skene (1979), repeated-labeling truth-inference model** (*JRSS-C*). *Why:*
  the raw majority-vote-agreement proportion used as the universal naive baseline throughout this
  model's large descendant literature (confirmed independently by G1-05 Uma et al. 2021 and G1-06
  Davani et al. 2021) is mathematically identical to ADS and matches its unit of analysis exactly
  (per-item, repeated historical judgments) — closer in *shape* than cluster purity, though
  informally named rather than independently cited.
- **G1-09 — Fleiss (1971), inter-rater agreement** (*Psychological Bulletin*). *Why:* the most
  important "near miss" found — Fleiss's own per-item statistic is a pairwise-agreement fraction
  (Analogous, not equivalent), but the informal "percent agreement with the majority label"
  construct circulating in this same lineage is mathematically equivalent to ADS, again with no
  dedicated citation distinct from kappa.

### LLM advisory constraint (Gap 2)

- **G2-01 — Sun et al. (2023), "RankGPT"** (EMNLP, DOI `10.18653/v1/2023.emnlp-main.923`, 590
  citations), plus its direct descendants **G2-02, G2-03, G2-04**. *Why:* establishes
  LLM-reranks-a-pre-fetched-candidate-list as commodity IR technique since 2023 — the exact
  "candidates-only, never blank-slate" half of ADS-Cascade's Tier-3 constraint, with no defensible
  novelty claim available for that half in isolation.
- **G2-05 — Singh & Szajnfarber (2025)** and **G2-06 — Hu et al. (2025)**. *Why:* both
  independently name general "AI proposes, human always decides" authority-split architectures —
  the closest citable vocabulary for the "never auto-applied" half — without being LLM-reranking-
  specific.
- **G2-09 — Strong, Men & Noble (2025)** and **G2-10 — Lykouris & Weng (2024)**. *Why:* closest
  single-paper matches combining an LLM/AI classifier with confidence-gated human deferral in a
  cascade shape; each misses one of ADS-Cascade's four sub-constraints (candidates-only, or
  100%-not-conditional human-routing, respectively).
- **G2-15 — Cummings (2004)** and **G2-16 — Khera et al. (2023, JAMA)**. *Why:* establish
  "AI/automation advises, human/operator decides" as two-decades-old, heavily-cited human-factors
  and clinical-decision-support doctrine — directly weakens any claim that the general
  advisory-only principle itself is a contribution.

---

## Tier 3 — Partial overlap (28 original + 5 gap-pass additions = 33 sources)

Individual mechanism-level precedents that share one dimension with ADS-Cascade (evidence type,
decision timing, or tiered structure) but not the combination. Grouped by which ADS-Cascade
component they partially anticipate — full detail and per-paper `KeyDifference` in
`literature_matrix.csv`.

**Partially anticipate Part 1** (design-time, historical-evidence-driven, but different evidence
type or decision grain): B2-01 (Smith-Miles 2009), B2-03 (Auto-WEKA/CASH), B2-04 (Auto-sklearn),
B2-05 (meta-feature taxonomy), B2-06 (Vanschoren meta-learning chapter), B2-07 (Monteiro et al.,
independently structurally analogous two-phase framework), B7-03 (learned index structures — same
one-shot-from-data-distribution shape, component not system grain), B7-04 (OtterTune — same
measure-once-before-serving shape, config not architecture grain).

**Partially anticipate Part 2** (confidence-gated tiering or deferral, but missing a dimension —
no multi-tier, no dual signal, no human tier, or no historical-evidence basis): B1-02 (SATzilla),
B1-04, B1-05 (algorithm-selection surveys), B3-01 (Adaptive-RAG — predicted not historical
complexity), B3-05 (RouteLLM — preference-trained, no human fallback), B3-07 (LLM routing survey),
B4-03, B4-04, B4-06, B4-07 (reject-option/selective-classification variants), B5-03 (HITL survey —
training-loop not inference-loop), B5-04, B5-05 (L2D extensions), B6-03, B6-04 (two-tier LLM
routing), B8-03, B8-05, B8-06 (AP-automation vendor sources — confidence-tiered runtime cascades,
none paired with a formal pre-deployment determinism audit).

**Adversarial counter-evidence, not competing method:** B4-10 (Beede et al. 2020) empirically shows
a *naive* reject-to-human handoff fails in practice without a feedback mechanism — motivating
evidence for why something like ADS-Cascade's T4→T1 promotion is needed, not a paper proposing one.
**B5-06 (Liu, Gallego & Barbieri 2022) is the single strongest adversarial hit against the
"two independently-tracked confidence signals" claim** — flagged at Tier 3 rather than Tier 2
because its two uncertainty terms come from the *same* model, not architecturally separate
subsystems, but it should be read carefully before the manuscript asserts that dual-signal tracking
is unprecedented.

---

## Tier 4 — Distant analogy (10 sources)

Foundational or terminologically-adjacent work with genuine historical/conceptual lineage but no
meaningful mechanistic overlap: B1-01 (Rice 1976 — the root vocabulary, one abstraction level below
ADS-Cascade's Part 1), B1-03 (algorithm runtime prediction), B2-08, B2-09 (human-AutoML partnership
arguments, no mechanism), B3-03 (Graves 2016, Adaptive Computation Time — anchors "adaptive
computation" terminology), B3-04 (early-exit survey), B4-01 (Chow 1970 — the 55-year-old ancestor of
the entire reject-option lineage; foundational but mechanistically minimal on its own), B4-08 (SVM
reject option), B6-05 (split computing/early exiting), B7-02 (Database Cracking — valuable
specifically as a *philosophical foil*: the opposite temporal structure, continuous vs. one-shot).

---

## Tier 5 — Clearly distinct (mechanism) / same domain only (1 source)

- **B8-02 — Bakumenko & Elragal (2022), ML anomaly/fraud detection on GL journal entries**
  (Systems). Same data type and professional audience as ADS-Cascade, but a different task
  (anomaly detection, not item→account classification) with no architecture-selection or cascade
  mechanism at all. Included to establish that GL-data ML research is an active academic area
  generally, not because it overlaps mechanistically.

---

## Summary table

*(updated 2026-08-11 to include the 23 gap-verification-pass sources; original Phase B counts in
parentheses)*

| Tier | Count | Share |
|---|---:|---:|
| 1 — Direct prior art (component-level: the ADS metric only) | 3 (0) | 4% |
| 2 — Strong conceptual overlap | 29 (17) | 37% |
| 3 — Partial overlap | 33 (28) | 42% |
| 4 — Distant analogy | 13 (10) | 16% |
| 5 — Clearly distinct | 1 (1) | 1% |
| **Total** | **79 (56)** | 100% |

**The whole-system headline finding is unchanged: zero sources combine all of ADS-Cascade's
claimed elements.** The new Tier 1 entries are a metric-level finding only (see the "Component-level
Tier 1" subsection above) and should not be read as contradicting that headline — they sharpen it:
the metric ADS-Cascade builds on has direct prior art, so the whole-system contribution claim now
depends even more specifically on the *application* of that metric (design-time architecture
selection) and its combination with the runtime cascade, not on the metric's construction.

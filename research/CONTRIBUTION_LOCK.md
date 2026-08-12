# Contribution Lock — Gate 4

> Decision and synthesis document. Determines the smallest, strongest, evidence-supported research
> contribution that survives Phases A-D.1. Does not modify `TECHNICAL_REPORT.md`, `README.md`, or
> `METHODOLOGY.md`, runs no new experiment, and invents no stronger contribution than the evidence
> chain below supports. Reviewed by the `research-code-auditor` before being presented as final —
> see the end of this document for the audit verdict.

---

## 1. Current research question

**Broad framing (settled, `STATE.md`'s "Literature review + paper-positioning conclusions"):** Can
historical decision consistency be used to guide AI system composition for classification problems
that possess large amounts of historical supervisory data?

**Operational framing actually tested (H1, `EXPERIMENT_1_REDESIGN_REVIEW.md` §2):** Does a
pre-specified, frozen, consistency-based decision rule (R3: realized ADS ≥0.90 → rules, [0.70,0.90)
→ retrieval, <0.70 → LLM-required/excluded) select the mechanism (rules-first exact match vs.
retrieval-primary fuzzy match) that agrees with the empirically best-performing mechanism more
often than chance?

Gate 4's job is to answer, from everything produced answering that operational question: **what is
the strongest contribution ADS-Cascade can defend**, not what would sound strongest in an abstract.

---

## 2. Evidence chain

Each step tagged **OBSERVED** (a fact directly measured or read from committed artifacts/code),
**INFERRED** (a conclusion drawn from observed facts, not itself directly measured), **HYPOTHESIZED**
(an untested proposition, stated as a hypothesis, not evidence), or **FUTURE WORK** (explicitly not
attempted).

1. **Original research motivation** — *HYPOTHESIZED.* Enterprise classification systems often treat
   architecture choice as fixed; historical decisions plausibly contain information about how
   deterministic a classification problem is, and could inform which mechanism class to build. This
   is the project's founding narrative, carried over from the production engineering work
   (Phase 1/2), not itself a finding.
2. **Phase A empirical discovery** — *OBSERVED, but only two data points.* `04_architecture_decision.py`'s
   R3 rule, applied to production (91.2% deterministic, post-hoc, pre-A5-fix, "likely understated,
   unverified" per `EVIDENCE_BASELINE.md`) selects RULES_FIRST; applied to the synthetic branch
   (87.56% deterministic, post-A5-fix) selects EMBEDDING_PRIMARY — the "R3 flip"
   (`r3_threshold_analysis.md`). Neither run ever measured whether the *selected* mechanism actually
   performed best (`contribution_stress_test.md` C2.G: "the rule has never been given a chance to be
   wrong").
3. **Initial architecture hypothesis** — *HYPOTHESIZED.* The general claim behind R3's existing
   0.90/0.70 thresholds (pre-dating this research retrofit): historical consistency alone is a valid
   design-time signal for choosing among qualitatively different mechanism classes. This is
   Phase B/C's "C2" candidate contribution.
4. **Literature challenge** — *OBSERVED (via 79-source adversarial search).* C1 (the ADS metric
   itself) is mathematically identical to cluster purity (Manning et al. 2008; Amigó et al. 2009)
   and the majority-vote-agreement baseline (Dawid & Skene 1979 lineage) — REJECTED as a novelty
   claim. C2 as a *general* pattern (measure history once, choose architecture before serving) is
   CHALLENGED (Rice 1976, Barbudo et al. 2023, Idreos & Kraska 2019). A *narrower* form — C2b:
   label-consistency evidence specifically, driving a qualitative mechanism-*class* choice
   specifically — has no direct anticipation in the 79-source sweep: PARTIALLY_SUPPORTED at the
   literature level.
5. **Contribution stress test** — *INFERRED (Phase C decision).* Of six candidate contributions
   (C1, C2/C2b, C3/C3b, C5, C6, C8), only C2 was scored **PROMISING** — the sole candidate with a
   clean, falsifiable empirical test and a real (if untested) gap in the literature. The other five
   were scored REJECTED, WEAK, or CASE_STUDY_ONLY. Conclusion: Experiment 1 (testing C2/C2b) is the
   single non-negotiable experiment required for a defensible paper (`contribution_stress_test.md`
   §6, "The minimum experiment set required").
6. **Experiment 1 hypothesis** — *HYPOTHESIZED, pre-registered.* H1 (revised): the frozen R3 rule
   agrees with the empirically best mechanism (rules vs. retrieval; LLM excluded for a documented,
   principled reason — the synthetic product string carries no signal predictive of the true label,
   `EXPERIMENT_1_REDESIGN_REVIEW.md` §10) more often than chance. Falsification criteria fixed in
   advance (§18 of that document), before any data existed.
7. **Experiment 1 result** — *OBSERVED, 240/240 conditions succeeded.* Overall: 32/50=64.0% agreement
   (Wilson CI [50.1%,75.9%], barely excludes chance, p=0.065). Decomposed: 100% agreement in the
   realized 0.70-0.90 band (30/30 by nominal target, 32/32 by realized-per-row band), 10% in the
   nominal ≥0.90 band (2/20) — sharpened by D.1 to **0%** (0/18) when binned by each row's own
   realized ADS. CLEAN produced zero defined comparisons (mechanisms tie in all 120 conditions).
   Matches the pre-registered **PARTIALLY SUPPORTED** row of §18's falsification table ("agreement
   significantly above chance overall, but only in one lexical condition... OR the relationship
   holds with a systematic minority of disagreeing bands rather than uniformly") — not a post-hoc
   reinterpretation of the criteria, the observed pattern was one of the four pre-specified possible
   outcomes.
8. **D.1 post-hoc explanation** — *OBSERVED (exhaustive, not sampled) + INFERRED (the causal
   account).* Re-derived independently by this session and again by the `research-code-auditor`'s
   first real audit (PASS, `research/AUDIT_REPORT.md`): under VARIED, `empirical_winner=="retrieval"`
   in 120/120 conditions, zero exceptions, unconditional on realized ADS (0.44-0.93); under CLEAN,
   `empirical_winner=="tie"` in 120/120, also zero exceptions. ADS correlates strongly with each
   mechanism's own accuracy (r≈0.91-0.96, both lexical conditions) but the *relative ranking* is a
   constant function of the lexical condition — a **manipulated, controlled experimental factor**,
   not an observational one — independent of ADS. The causal account (ADS is computed on the stable
   `product_code`, structurally blind to the perturbable surface string) is INFERRED from direct code
   inspection, not itself a second controlled experiment — but it is exhaustive over all 240 rows,
   not a sampled or cherry-picked subset, and the audit independently re-verified the exceptionless
   claim from the raw CSV.
9. **Current surviving contribution** — *INFERRED, this document's synthesis.* Not "C2 as originally
   framed" — that unconditional form is falsified in the ≥0.90 band by C2b's own pre-registered
   falsification test (`contribution_stress_test.md` C2.F: "if the mismatch is large and consistent
   across bands and seeds, the qualitative claim itself is falsified" — 18/18 disagreement,
   exceptionless, is exactly that). What survives is a narrower, more precise descriptive finding:
   historical consistency predicts mechanism-level accuracy but not mechanism *ranking*, when, as
   observed in this synthetic experiment, ranking is governed by a representation-stability property
   the consistency signal is blind to by construction. See §5-6.

---

## 3. Candidate contribution analysis

Re-scored against the Phase B (`contribution_status.md`) / Phase C (`contribution_stress_test.md`)
baseline, updated only where Experiment 1 / D.1 actually bears on the claim. Claims Experiment 1 does
not touch (C1, C3, C3b, C4, C5, C6-as-a-whole, C7, C8) are **carried forward unchanged** — Gate 4
does not re-litigate them without new evidence, and inventing a reason to upgrade one would itself be
scope creep.

- **C1 — ADS as a novel metric.** Unaffected by Experiment 1 (Exp1 tests whether ADS is a *useful
  selection signal*, not whether its formula is *original*). Baseline: **REJECTED** (mathematically
  identical to cluster purity / majority-vote agreement). Unchanged.
- **C2 — design-time architecture selection, general pattern.** Baseline: **CHALLENGED** (Rice 1976,
  Barbudo 2023, Idreos & Kraska 2019). Unchanged — Exp1 never tested the *general* pattern, only its
  narrower C2b instance.
- **C2b — label-consistency evidence → qualitative mechanism-class choice (the claim Exp1 actually
  tests).** Baseline: PARTIALLY_SUPPORTED/PROMISING at the *literature* level, explicitly flagged as
  untested (`contribution_stress_test.md`: "the rule has never been given a chance to be wrong").
  **Updated by Exp1+D.1: CONDITIONAL.** The *unconditional* form ("ADS thresholds alone select the
  right mechanism") is falsified by its own pre-registered test in the ≥0.90 band. A *narrower*,
  conditional form ("ADS predicts each mechanism's accuracy; ranking is governed by a
  separately-manipulated (in this factorial design), ADS-blind representation-stability factor") is
  well-evidenced within this experiment. See §5-6.
- **C3 — runtime multi-tier confidence cascade, general pattern.** Baseline: **CHALLENGED** (FrugalGPT,
  reject-option/selective-classification lineage, LLM routing literature). Unaffected — Exp1
  explicitly bypasses the shipped cascade entirely (`EXPERIMENT_1_REDESIGN_REVIEW.md` §11). Unchanged.
- **C3b — two independently-tracked, never-blended confidence signals.** Baseline: **WEAK** (real but
  narrow distinction from B5-06; no blended-vs-unblended ablation ever run). Unaffected. Unchanged.
- **C4 — LLM constrained to re-ranking only, never auto-applied.** Baseline: **PARTIALLY_SUPPORTED**
  (candidates-only half CHALLENGED outright by RankGPT-lineage; never-auto-applied half diffusely
  precedented; the four-part combination not found assembled elsewhere). Unaffected — LLM was
  excluded from Exp1 by design. Unchanged.
- **C5 — permanent T4→T1 promotion via human correction.** Baseline: **WEAK** (real but narrow
  mechanism; no before/after measurement exists, Experiment 3 never run). Unaffected by Exp1.
  Unchanged.
- **C6 — the combined Part 1 + Part 2 system as one contribution.** Baseline: **WEAK** (no B1-B5
  baseline comparison ever run, Experiment 2 never run; combination novelty is the weakest available
  novelty form). Unaffected directly — Exp1 evaluates isolated mechanisms, not the combined runtime
  system. **Worth noting, not a formal reclassification:** Exp1's finding that ADS alone doesn't
  reliably predict mechanism ranking further weakens C6's premise that evidence-driven gating adds
  demonstrated value over a static pipeline — this makes Experiment 2 (never run) more, not less,
  important if C6 is ever revisited, but does not change C6's current WEAK status, since it was
  already WEAK on evidentiary grounds before Exp1.
- **C7 — cross-company consistency threshold (R1).** Baseline: **CHALLENGED** (Jørgensen & Igel 2021,
  same phenomenon, same domain). Subsumed into C2 per Phase C's own numbering note. Unaffected by
  Exp1 (Exp1 tests R3, not R1). Unchanged.
- **C8 — Romanian fiscal-document application domain.** Baseline: **CASE_STUDY_ONLY**. Academic-niche
  novelty survives; the "no comparable vendor practice" sub-claim is factually contradicted by
  B8-04 (Ken From Finance) and is **still uncorrected in `TECHNICAL_REPORT.md` §5** (verified this
  pass — line 289-291 still reads "...typically ships a single learned classifier... chosen up front
  rather than derived from a measured determinism distribution"). Unaffected by Exp1. Unchanged, and
  flagged again here as a known, still-open Phase E manuscript fix (not new to this pass — see §9).

**No claim was upgraded because it would help the narrative.** C2b is the only claim Experiment 1 or
D.1 bears on at all, and its unconditional form moves *down* (falsified in part), not up.

---

## 4. The ADS-predicts-accuracy vs. ADS-predicts-ranking distinction

Evaluated explicitly, not collapsed, per the brief's requirement — verified directly against the
frozen evidence, not asserted:

- **ADS predicts mechanism performance:** OBSERVED. Pearson r(realized ADS, rules accuracy) = 0.959
  (CLEAN) / 0.909 (VARIED); r(realized ADS, retrieval accuracy) = 0.955 (CLEAN) / 0.948 (VARIED) —
  independently recomputed by the `research-code-auditor`'s first audit and matched to stated
  precision. **True, strongly supported, in both lexical conditions.**
- **ADS predicts which mechanism should be selected:** OBSERVED to be **false** in this experiment.
  `empirical_winner` is `"retrieval"` in 120/120 VARIED conditions and `"tie"` in 120/120 CLEAN
  conditions — a constant function of the (controlled, manipulated) lexical factor, with zero
  variation attributable to realized ADS across its full 0.44-0.93 observed range. R3's own
  agreement rate (100% vs. 0%) is fully explained by this constancy plus R3 being a step function of
  ADS: R3 "succeeds" only in the sub-range where its ADS-driven output happens to equal the
  constant true winner (`retrieval`), and fails wherever it doesn't.

These are not the same claim, do not stand or fall together, and this document does not merge them.
Any future prose that states "ADS predicts mechanism suitability" without this qualification is a
collapse of the distinction and must be corrected.

---

## 5. Candidate contribution formulations (conservative → ambitious)

| # | Claim | Supporting evidence | Limiting evidence | Relevant prior art | Publishable as stated? | Reviewer-attack risk | Required qualification |
|---|---|---|---|---|---|---|---|
| **1 (conservative)** | A pre-specified historical-consistency-only threshold rule (R3), while directionally associated with overall mechanism performance, fails to reliably select the empirically best mechanism once lexical/surface-form noise is present. | 32/50=64.0% aggregate; 0% (0/18) exceptionless disagreement in R3's own highest-confidence band under noise; mechanistically explained (§8). | Single synthetic generator; single lexical-perturbation model (p_transform=0.3, rapidfuzz); two mechanisms only; not replicated in production. | None contradicts a negative/boundary result about this specific rule; consistent with the project's own falsification-first design (`EXPERIMENT_1_REDESIGN_REVIEW.md` §18-19). | Yes — safest framing. | Low — hard to attack a narrow, well-evidenced negative finding; risk is "is this interesting enough," not "is this true." | Scope explicitly to this generator/R3/perturbation model; do not imply any consistency-based selector would fail this way. |
| **2 (conservative-plus, RECOMMENDED — see §6)** | Historical consistency (ADS) predicts each mechanism's own accuracy but not which of two mechanisms outperforms the other; that ranking is governed by a separately-manipulated (in this factorial design) representation-stability factor (lexical/surface-form noise) the consistency signal does not capture. | §4's correlations (r≈0.91-0.96); exceptionless 120/120-vs-120/120 winner constancy; lexical condition is a **manipulated, controlled** factor, not observational — the "governed by" half rests on experimental, not merely correlational, evidence. | Same generator/perturbation-model scope as #1; the causal mechanism (ADS's blindness to surface form) is INFERRED from code inspection + exhaustive matching, not a second independently-designed confirmatory experiment. | Refines, does not contradict, the algorithm-selection/meta-learning lineage (Rice 1976; Smith-Miles 2009) by identifying a specific failure mode of a single-feature, label-consistency-only selector. | Yes — this is the recommended core finding. | Medium — a reviewer may ask whether this is an artifact of exactly how ADS is computed, or a general property of any design-time signal blind to the axis that later varies; the paper should preempt this, not claim the general case was tested. | State plainly that "predicts own accuracy" is correlational and "governs ranking" rests on a controlled 2-level factor within one generator; do not generalize to other consistency metrics or noise models. |
| **3 (moderate)** | This case study shows a design-time selection rule based solely on historical label consistency can be systematically miscalibrated for a real mechanism trade-off once representation instability is present, suggesting design-time selectors for hybrid classification systems should account for representation stability alongside label consistency. | Same as #2. | The prescriptive "should account for representation stability" clause was never built or tested — no two-feature selector exists anywhere in this repository. | Same as #2, but the prescriptive framing edges toward proposing a method that doesn't exist yet. | Marginally — only if the prescriptive clause is explicitly hedged as motivation for future work, never implied as demonstrated. | Medium-high — biggest risk is a reviewer conflating "found a limitation" with "proposed and validated a fix." | Repeated, explicit "not built, not tested here" framing every time the two-feature idea is mentioned. |
| **4 (ambitious — NOT RECOMMENDED, listed to name and reject it)** | ADS-Cascade's determinism-driven design-time architecture-selection procedure is validated as an effective method for hybrid classification-system composition. | None — the *unconditional* form of this claim is exactly what Exp1's ≥0.90-band result falsifies (0/18, exceptionless). | Directly contradicted by this experiment's own data; C1 already REJECTED for novelty; C2 general pattern already CHALLENGED; C6 combined-system claim already WEAK/untested. | Heavily contradicted/subsumed by the entire Phase B sweep (Rice 1976, Barbudo 2023, Idreos & Kraska 2019, meta-learning lineage). | **No.** | Certain — this is precisely the claim five phases of audit work (A-D.1) have progressively disproven; using it would contradict this project's own frozen evidence. | N/A — do not use this formulation. |

---

## 6. Recommended contribution

**Formulation #2** is the locked contribution. Exact wording (two explicitly separated sub-claims,
per §4, plus one synthesis sentence — this is the wording to be carried into Phase E, tightened from
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §12, which the `research-code-auditor` already independently
verified line-by-line against the frozen CSV):

> **6a (supported).** In this synthetic product-classification generator, realized historical
> decision consistency (ADS) is strongly predictive of each classification mechanism's own accuracy
> (exact-match rules and fuzzy retrieval alike; Pearson r ≈ 0.91-0.96 in both the noise-free and
> noisy lexical conditions).
>
> **6b (the limiting/negative finding).** ADS is **not** predictive of which of the two mechanisms
> will outperform the other: under a controlled lexical/surface-form perturbation, retrieval wins on
> whole-set accuracy in 120/120 conditions and the two mechanisms are statistically indistinguishable
> (within a pre-registered δ=0.02 margin) in 120/120 noise-free conditions — in both cases
> independent of realized ADS across its full observed range (0.44-0.93). A pre-specified
> consistency-only decision rule (R3) consequently agrees with the empirical winner only in the
> sub-range where its own ADS-threshold output happens to coincide with the constant true winner,
> because ADS is computed from a stable product identity and is blind, by construction, to the
> surface-form instability that actually determines the outcome here.
>
> **Synthesis.** In this synthetic experiment, historical decision consistency is informative about
> classification-mechanism *difficulty*, not about mechanism *ranking*, when — as observed here —
> ranking is governed by a representation-stability property the consistency signal does not
> observe — a narrower, more specific, and empirically falsifiable-and-partly-falsified refinement of
> the original "historical consistency selects the right architecture" hypothesis, not a confirmation
> of it.

**Why #2 over #1 or #3:** #1 alone under-states the positive half (§4's correlations are real and
worth reporting, not just a negative result); #3 over-states by implying a fix was designed and
tested when it was not. #2 states exactly what was measured, no more, and matches the wording
already produced and independently audited in Phase D.1 — Gate 4 is locking that wording, not
inventing new phrasing that would need to be re-verified from scratch.

---

## 7. Claims explicitly rejected

Verified this pass by grepping `research/*.md`, `research/literature/*.md`, `STATE.md`, `ROADMAP.md`,
`TECHNICAL_REPORT.md`, and `README.md` for resurrection — see the check log at the end of this
section.

- **"ADS is a novel metric."** REJECTED (C1) — mathematically identical to cluster purity and the
  majority-vote-agreement baseline. Not found asserted anywhere in current research documentation.
- **"ADS universally selects the correct architecture."** Directly falsified in the ≥0.90 band
  (0/18, exceptionless) under lexical noise. Not found asserted.
- **"The cascade architecture itself (Part 1 + Part 2 combined) is novel."** WEAK (C6) — no baseline
  comparison ever run; combination novelty is the weakest available form and is unvalidated. Not
  found asserted as a settled claim (framed correctly as untested throughout the stress test).
- **"The method generalizes to enterprise AI broadly."** Out of scope per the project's own settled
  positioning (`STATE.md`); the four stated preconditions (repeated historical decisions, observable
  labels, measurable consistency, sufficient historical coverage) bound this explicitly. Not found
  asserted.
- **"Production data independently validates the synthetic finding."** False if implied — production
  never ran a lexical-noise sweep at all; only two single-run data points feed the "R3 flip"
  narrative (§2 step 2), and production's own ADS figures remain flagged "likely understated,
  unverified" pending an A5-fix rerun that has not happened (`EVIDENCE_BASELINE.md` §1). Not found
  asserted.
- **"The experiment proves that consistency alone is sufficient for architecture selection."** This
  is the *opposite* of what Experiment 1 + D.1 show. Not found asserted.
- **"Higher ADS means rules is better."** Reversed under noise in this data (retrieval's advantage
  over rules *widens*, not narrows, as ADS increases under VARIED). Not found asserted.
- **"CLEAN implies the two mechanisms are equivalent in general."** CLEAN shows near-equivalence
  specifically absent lexical noise, for this generator — not a general-equivalence claim. Not found
  asserted.
- **"The synthetic `p_transform=0.3` perturbation represents real-world OCR/typo noise."** An
  unvalidated synthetic stand-in, not a measured noise model. Not found asserted.

**One pre-existing, already-documented manuscript issue reconfirmed, not newly created by this
pass:** `TECHNICAL_REPORT.md` §5 (lines 289-291) still states commercial vendors "typically ship a
single learned classifier... chosen up front rather than derived from a measured determinism
distribution" — directly contradicted by B8-04 (Ken From Finance's public materials, which already
describe a pre-deployment historical-consistency audit). This was already flagged in
`RESEARCH_AUDIT.md` (F7/F8) and `contribution_stress_test.md` (C8) as an outstanding Phase E fix. Not
a new violation, not something this document is authorized to fix (manuscript edits are out of
scope for Gate 4), but restated here so it is not lost before Phase E begins.

**Grep check log (this pass):** searched `research/*.md`, `research/literature/*.md`, `STATE.md`,
`ROADMAP.md`, `TECHNICAL_REPORT.md`, `README.md` for `novel metric|our novel|is novel|proves that|
validates R3|independently validat|universally|enterprise AI broadly|no vendor|no comparable
vendor|consistency alone is sufficient` and related terms. Matches found only inside
`AUDIT_REPORT.md`, `EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `prior_art_map.md`, `contribution_status.md`
— in every case as part of a correctly-negated disclaimer ("...is a novel contribution — already
settled as out of scope"), never as an assertion. `TECHNICAL_REPORT.md`/`README.md` matched none of
these specific phrases; the one substantive issue found (the vendor-practice sentence, different
wording) was located by direct read of §5, not by this grep, and is pre-existing.

---

## 8. Scope

The locked contribution (§6) is bounded to exactly what the evidence covers — no broader:

- **One application domain:** Romanian fiscal/invoice product-to-GL-account classification.
- **One motivating production case study** (confidential, cited not reproduced): establishes the
  research question's real-world origin and the "R3 flip" observation, but contributes no
  statistical evidence to §6 — see §7's "production data independently validates" rejection.
- **One controlled synthetic experimental environment:** the Experiment 1 generator (60-1,200-product
  scale synthetic invoice-line data), not real invoice text.
- **Specific mechanisms:** exact-match `rules_only` lookup vs. rapidfuzz-based `retrieval_only`
  fuzzy matching (cutoff=75). Not embeddings, not an LLM, not the shipped multi-tier cascade.
- **Specific lexical-perturbation model:** `p_transform=0.3`, five fixed transform types (case,
  punctuation, token-reorder, abbreviation, whitespace), pilot-tuned to a target corruption-share
  band, not derived from measured real-world OCR/typo error rates.
- **Specific realized-ADS range:** 0.44-0.93, structurally capped below ~0.91 by the fixed
  `CROSS_COMPANY_ALIGN=0.695` nuisance parameter (`EXPERIMENT_1_CALIBRATION_REPORT.md` §2) — no
  "deep rules-first" (≥0.93) region was reachable or tested.

---

## 9. Limitations

- Single synthetic generator family; 240 conditions replicate a seeded RNG, not an external
  population.
- δ=0.02 practical-equivalence margin and R3's 0.90/0.70 thresholds are judgment calls anchored to
  this repository's own precedent, not derived from a formal cost model — frozen before the run, not
  re-tuned after.
- LLM mechanism excluded from the primary comparison for a documented, principled reason (§10 of the
  redesign review), not evaluated at all in Experiment 1.
- Retrieval coverage is 1.0 in all 240 conditions (never abstains at cutoff=75); rules coverage is
  always <1.0 — a real asymmetry, part of the explanation, not an artifact to normalize away.
- The realized-ADS ceiling (~0.91) means the "rules-first, comfortable margin" region (≥0.93) was
  never reachable by this generator — any claim about *that* region is untested, not merely
  unfavorable.
- D.1's causal account (ADS's blindness to surface form) is a well-evidenced, exhaustively-checked,
  but **post-hoc** explanation of already-frozen data, not a fresh prospective confirmation — a
  future study that pre-registers this exact causal claim and tests it on new data would strengthen
  it further.
- Production ADS figures (91.2%/0.847/0.964) were generated by the pre-A5-fix script version and
  remain "likely understated, unverified" — not re-run against corrected code, since no production
  data exists in this repository (`EVIDENCE_BASELINE.md` §1, Note 1).
- `TECHNICAL_REPORT.md` §5's vendor-practice sentence remains factually uncorrected (§7) — a known,
  pending Phase E fix, not resolved by this document.

---

## 10. Future work

Named, not built, not started:

- A decision rule that conditions mechanism selection on **both** realized ADS and a measured (not
  assumed) lexical/representation-stability signal — the direct next hypothesis this experiment
  motivates (Formulation #3, §5, deliberately not adopted as the current claim).
- Whether the specific pattern (retrieval's noise-cost staying flat while rules' noise-cost grows
  with ADS) is specific to rapidfuzz-style token similarity or holds for other retrieval
  implementations (e.g. embedding-based retrieval, explicitly deferred as a future upgrade in
  `EXPERIMENT_1_REDESIGN_REVIEW.md` §9).
- A real (not synthetic) noise/OCR-error model calibrated against an actual document corpus, to test
  whether `p_transform=0.3`'s pattern generalizes beyond this pilot-tuned synthetic stand-in.
- Experiment 2 (C6, cascade baseline comparison against simpler pipelines) and Experiment 3 (C5,
  feedback-loop before/after measurement) — recommended by `contribution_stress_test.md` §6 for
  upgrading WEAK claims, but **explicitly not required** for the current, narrower, minimum
  defensible contribution locked in §6; the paper can be defensible without them if scoped honestly.
- Re-running the corrected (post-A5-fix) intelligence pipeline against production data, to resolve
  whether production ADS figures are also understated (currently unverifiable — no production data
  in this repository).

None of these are authorized or begun by this document. Per `RESEARCH_GPS.md`'s DO NOT CHASE list,
none should be started before Phase E unless one is found to materially affect the research
question, the surviving contribution, Experiment 1's validity, or the paper's central conclusion.

---

## 11. One-sentence paper pitch

**A. Research question.** Can historical decision consistency, measured before deployment, be used
to select between qualitatively different classification mechanisms (exact-match rules vs.
retrieval-based fuzzy matching)?

**B. One-sentence contribution.** We show, via a pre-registered 240-condition synthetic experiment,
that a historical-consistency-only design-time selection signal is informative about a mechanism's
own expected accuracy but not about which of two mechanisms will outperform the other once
surface-form/representation instability is present.

**C. One-sentence result.** In this experiment, the consistency-based decision rule agreed with the
empirically best mechanism in 100% of definable comparisons in the 0.70–0.90 realized-ADS band, but
in 0% of definable comparisons in the ≥0.90 realized-ADS band; under the tested synthetic
perturbation, the empirical winner was separated by the lexical-noise condition, which the
consistency signal did not observe.

**D. One-sentence limitation.** This finding comes from one synthetic generator, one lexical-
perturbation model, and one motivating (statistically non-contributing) production case study, and
does not establish that the same failure mode occurs under real-world surface noise or for other
consistency-style metrics.

**E. One-sentence future direction.** A natural next step is a decision rule that conditions on both
historical consistency and a measured representation-stability signal, though no such rule was built
or tested here.

---

## 12. Gate-4 decision

**Adopted.** Formulation #2 (§6) is locked as ADS-Cascade's surviving research contribution. C1, C2
(general), C3, C3b, C4, C5, C6, C7, C8 retain their pre-Experiment-1 classifications from Phase B/C
(§3) — none upgraded, none invented. C2b moves from "PARTIALLY_SUPPORTED/untested" to "CONDITIONAL,
empirically grounded, unconditional form falsified" — a downgrade in ambition, not an upgrade in
strength. §7's rejected-claims list is the authoritative negative space for Phase E's Limitations
section.

**This document is the reference Phase E must draft against.** Its wording (§6, §11) is what
`TECHNICAL_REPORT.md`'s Abstract/Introduction/Results/Discussion should converge on — Gate 4 does not
draft that prose itself.

**Gate 4 is complete pending the auditor verdict below.** Phase E is unblocked only if that verdict
is PASS or PASS_WITH_NOTES.

---

## Auditor verdict

🟢 **PASS.** Independently audited by the `research-code-auditor` (full report:
`research/AUDIT_REPORT.md`). The auditor re-derived §4's Pearson correlations, the 120/120-VARIED /
120/120-CLEAN winner-constancy claim, and the realized-ADS-band 32/32 (100%) vs. 0/18 (0%) split
directly from `final_condition_results.csv`, independently of this document's own restated numbers
— all matched exactly. It confirmed §7's grep-check claim by re-running an equivalent grep itself,
confirmed the observed Experiment 1 pattern is an accurate match to `EXPERIMENT_1_REDESIGN_REVIEW.md`
§18's pre-registered PARTIALLY SUPPORTED row (not a post-hoc fit), confirmed Formulation #4 is
correctly marked not-recommended and not adopted, and confirmed §3/`contribution_lock.csv`'s status
table matches the Phase B/C source documents without narrative-favoring rounding. Three
non-blocking notes were raised (this placeholder needing resolution — now resolved; `STATE.md`'s
pre-existing staleness; the CSV's cross-document status-vocabulary reconciliation being implicit
rather than documented) — none affect Formulation #2's validity. **Formulation #2 survives
adversarial review. Gate 4 is complete.**

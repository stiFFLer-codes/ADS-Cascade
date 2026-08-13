# Manuscript Claim → Evidence Map (Phase E, Task 4)

> Maps every major claim the Phase E manuscript is permitted (or forbidden) to make to its exact
> source document and, where applicable, exact experiment/artifact. Classification vocabulary:
> **OBSERVED** (directly measured, in a committed artifact), **INFERRED** (a conclusion drawn from
> observed facts, not itself directly measured), **CASE_STUDY** (from the confidential production
> engagement, cited not reproduced), **LIMITATION** (a boundary/negative statement about scope),
> **FUTURE_WORK** (explicitly not attempted). This document is the authoritative check for Phase E4
> (internal scientific audit) — every sentence in the eventual manuscript should trace to a row here.
> Does not modify `TECHNICAL_REPORT.md`, `CONTRIBUTION_LOCK.md`, or any frozen evidence.

---

## 1. Claims permitted, by manuscript section (per `PHASE_E_PLAN.md` §3.3's hierarchy)

### §1 Introduction

| Claim | Class | Exact source | Artifact |
|---|---|---|---|
| Research question: "Can historical decision consistency be used to select between qualitatively different classification mechanisms?" | — (question, not a claim) | `CONTRIBUTION_LOCK.md` §11.A | — |
| Four preconditions (repeated historical decisions / observable labels / measurable consistency / sufficient historical coverage) bound the scope | LIMITATION | `STATE.md` "Literature review + paper-positioning conclusions" | — |
| The production system observed an "R3 flip" between two single runs (production RULES_FIRST at 91.2%, synthetic EMBEDDING_PRIMARY at 84.1%) that motivated this study | CASE_STUDY | `METHODOLOGY.md` real-vs-synthetic table; `r3_threshold_analysis.md` | Two single data points — never framed as statistical evidence |
| Explicitly out of scope: generative writing, open-ended reasoning, planning, creative design, negotiation, exploratory analysis | LIMITATION | `STATE.md` (settled positioning) | — |

### §2 Related Work

| Claim | Class | Exact source | Artifact |
|---|---|---|---|
| ADS is mathematically identical to cluster purity (Manning et al. 2008) and the majority-vote-agreement baseline (Dawid & Skene 1979 lineage) | OBSERVED (literature fact) | `CONTRIBUTION_LOCK.md` §3 (C1), `contribution_stress_test.md` | `research/literature/ads_metric_prior_art.md`/`.csv` |
| Design-time whole-architecture selection from historical consistency (general form, C2) is anticipated in spirit by Rice 1976 / Smith-Miles 2009 / Barbudo et al. 2023 / Idreos & Kraska 2019 | INFERRED (positioning) | `CONTRIBUTION_LOCK.md` §3 (C2, CHALLENGED) | `research/literature/citation_ledger.csv` rows B1-01, B2-01, B2-02, B7-01 (all VERIFIED) |
| The narrower claim (C2b: label-consistency evidence specifically driving a qualitative mechanism-*class* choice) has no direct anticipation found in the 79-source sweep | OBSERVED (absence-of-evidence, literature search) | `contribution_status.md`, `prior_art_map.md` | `citation_ledger.csv` (full 59-row ledger) |
| Closest ML analog is reject-option/two-stage/selective-classification literature, but that gates *inference-time* per-item abstention, not *design-time* whole-architecture selection | INFERRED (positioning) | `STATE.md`, `CONTRIBUTION_LOCK.md` §3 | `citation_ledger.csv` B4-01 through B4-10 (VERIFIED) |
| Commercial invoice/GL-classification practice (Ken From Finance, Peakflo, Ramp) exhibits similar shapes informally, without formal determinism metrics | OBSERVED (industry-source fact) | `citation_ledger.csv` B8-04/05/06 | Verified via WebFetch, industry sources, not peer-reviewed — must be labeled as such in-text |

### §3 Problem Setting

| Claim | Class | Exact source | Artifact |
|---|---|---|---|
| ADS formula and definition | OBSERVED (definitional) | `TECHNICAL_REPORT.md` §2.2 | — |
| H1 (revised): the frozen R3 rule agrees with the empirically best mechanism more often than chance; pre-registered before data existed | — (hypothesis statement) | `EXPERIMENT_1_REDESIGN_REVIEW.md` §2, §18 | Pre-registration is itself the artifact — dated before the run |

### §4 Experimental Design

| Claim | Class | Exact source | Artifact |
|---|---|---|---|
| Generator/mechanism/perturbation-model description (60-1,200 product scale, exact-match rules vs. rapidfuzz retrieval cutoff=75, five fixed transform types at p_transform=0.3) | OBSERVED (design fact) | `EXPERIMENT_1_REDESIGN_REVIEW.md`, `EXPERIMENT_1_CALIBRATION_REPORT.md` | `scripts/experiments/exp1/*` |
| LLM mechanism excluded for a documented, principled reason (synthetic product string carries no signal predictive of true label) | INFERRED (design justification) | `EXPERIMENT_1_REDESIGN_REVIEW.md` §10 | — |
| δ=0.02 practical-equivalence margin, R3 thresholds (0.90/0.70), retrieval cutoff (75) are frozen, judgment-call parameters, not derived from a formal cost model | LIMITATION | `CONTRIBUTION_LOCK.md` §9 | `EXPERIMENT_1_CALIBRATION_REPORT.md` |

### §5 Results

| Claim | Class | Exact source | Artifact |
|---|---|---|---|
| Overall agreement 32/50 = 64.0%, Wilson CI [50.1%, 75.9%], p=0.065 vs. chance | OBSERVED | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4; independently re-derived by `AUDIT_REPORT.md` | `final_condition_results.csv` (240 rows) |
| 100% agreement (32/32) in the realized 0.70-0.90 ADS band; 0% (0/18) in the realized ≥0.90 band | OBSERVED | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5 | Same CSV, per-row realized-ADS binning |
| CLEAN condition produces zero defined comparisons (120/120 ties, δ=0.02 margin) | OBSERVED | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4-5 | Same CSV |
| Pearson r(realized ADS, rules accuracy) ≈ 0.909-0.959; r(realized ADS, retrieval accuracy) ≈ 0.948-0.955, both lexical conditions | OBSERVED | `CONTRIBUTION_LOCK.md` §4 (6a); independently recomputed by `AUDIT_REPORT.md` | `final_condition_results.csv` |
| `empirical_winner` == "retrieval" in 120/120 VARIED conditions, exceptionless, unconditional on realized ADS across its full 0.44-0.93 observed range | OBSERVED (exhaustive, not sampled) | `CONTRIBUTION_LOCK.md` §4 (6b); `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §6 | Same CSV; re-verified by auditor from raw data |
| Causal account: ADS is computed on the stable `product_code`, structurally blind to the perturbable surface string, which is why it cannot predict the noise-driven ranking | INFERRED (from direct code inspection, exhaustive matching — not a second controlled experiment) | `CONTRIBUTION_LOCK.md` §2 step 8; `EXPERIMENT_1_DATA_DICTIONARY.md` | `scripts/experiments/exp1/consistency.py` |
| The observed pattern matches the pre-registered PARTIALLY SUPPORTED row of the falsification table exactly (not a post-hoc reinterpretation) | OBSERVED (procedural fact) | `EXPERIMENT_1_REDESIGN_REVIEW.md` §18; confirmed by `AUDIT_REPORT.md` | — |

### §6 Discussion

| Claim | Class | Exact source | Artifact |
|---|---|---|---|
| Synthesis: historical consistency is informative about mechanism *difficulty*, not mechanism *ranking*, when ranking is governed by a representation-stability property the signal doesn't observe | INFERRED (this document's/Gate 4's synthesis, locked) | `CONTRIBUTION_LOCK.md` §6 (exact wording to reuse verbatim) | — |
| This refines, does not contradict, the algorithm-selection/meta-learning lineage by identifying a specific failure mode of a single-feature, label-consistency-only selector | INFERRED (positioning) | `CONTRIBUTION_LOCK.md` §5, row 2 | — |
| The production R3 flip (§1) is consistent with, but does not itself provide statistical evidence for, this finding | CASE_STUDY | `CONTRIBUTION_LOCK.md` §8 | — |

### §7 Limitations

Every bullet in `CONTRIBUTION_LOCK.md` §9 is LIMITATION-class and must appear, undiluted:

- Single synthetic generator family; 240 conditions replicate a seeded RNG, not an external population.
- δ=0.02 and R3's 0.90/0.70 thresholds are judgment calls, frozen before the run, not re-tuned after.
- LLM mechanism excluded entirely, not evaluated.
- Retrieval coverage is 1.0 in all 240 conditions; rules coverage is always <1.0 — a real asymmetry.
- The realized-ADS ceiling (~0.91) means the "deep rules-first" (≥0.93) region was never reachable —
  untested, not merely unfavorable.
- D.1's causal account is post-hoc, not a fresh prospective confirmation.
- Production ADS figures (91.2%/0.847/0.964) are pre-A5-fix and remain "likely understated,
  unverified."
- `TECHNICAL_REPORT.md` §5's vendor-practice sentence is still factually uncorrected — a known Phase E
  prose fix (not itself a research claim, but must be resolved before the manuscript cites that
  report's positioning language).

### §8 Future Work

All FUTURE_WORK-class, from `CONTRIBUTION_LOCK.md` §10, must be phrased as "not built, not tested
here": (1) a decision rule conditioning on both ADS and a measured representation-stability signal;
(2) whether the pattern is specific to rapidfuzz-style retrieval or holds for embeddings; (3) a real
(not synthetic) noise/OCR-error model; (4) Experiment 2 (C6 baseline comparison) and Experiment 3 (C5
feedback-loop measurement) — named as recommended-but-not-required.

### §9 Conclusion

No new claims — restates `CONTRIBUTION_LOCK.md` §11.B/§11.C exactly. This is the highest-risk section
for claim inflation (a common drafting failure mode: conclusions restate findings more confidently
than the results section supports) — flag explicitly at Phase E4.

---

## 2. Claims that must NOT appear (from `CONTRIBUTION_LOCK.md` §7, reproduced here as the manuscript's
   negative checklist — Phase E4/E5 should grep drafts against this list)

| Forbidden claim | Why rejected | Where this was settled |
|---|---|---|
| "ADS is a novel metric" | Mathematically identical to cluster purity / majority-vote agreement (C1) | `CONTRIBUTION_LOCK.md` §3, §7 |
| "ADS universally selects the correct architecture" | Directly falsified, 0/18 exceptionless in the ≥0.90 band under noise | §7 |
| "The cascade architecture (Part 1+2 combined) is novel" | C6, WEAK, no baseline comparison ever run | §3 (C6), §7 |
| "The method generalizes to enterprise AI broadly" | Out of scope per settled positioning; four preconditions bound it explicitly | `STATE.md`, §7 |
| "Production data independently validates the synthetic finding" | Production never ran a lexical-noise sweep; only two single-run data points feed the R3-flip narrative | §7 |
| "The experiment proves consistency alone is sufficient for architecture selection" | Opposite of what Exp1+D.1 show | §7 |
| "Higher ADS means rules is better" | Reversed under noise — retrieval's advantage *widens*, not narrows, as ADS increases under VARIED | §7 |
| "CLEAN implies the two mechanisms are equivalent in general" | CLEAN shows near-equivalence specifically absent lexical noise, for this generator — not a general-equivalence claim | §7 |
| "The synthetic p_transform=0.3 perturbation represents real-world OCR/typo noise" | Unvalidated synthetic stand-in, not a measured noise model | §7 |
| "A design-time selector should account for representation stability" stated as demonstrated (rather than motivated future work) | The two-feature idea was never built or tested (Formulation #3, explicitly NOT RECOMMENDED) | `CONTRIBUTION_LOCK.md` §5 row 3, row 4 |
| "ADS predicts mechanism suitability" (unqualified, collapsing accuracy-prediction and ranking-prediction into one claim) | The two are empirically distinct — one holds, one is falsified — and must never be merged in prose | `CONTRIBUTION_LOCK.md` §4 |
| Commercial vendors "typically ship a single learned classifier... chosen up front rather than derived from a measured determinism distribution" (current `TECHNICAL_REPORT.md` §5, lines 289-291) | Factually contradicted by B8-04 (Ken From Finance's public materials, which already describe a pre-deployment historical-consistency audit) | `CONTRIBUTION_LOCK.md` §7, `RESEARCH_AUDIT.md` F7/F8 — **known outstanding fix, not yet corrected anywhere** |

## 3. Special-attention flags (per the brief's explicit list)

- **ADS novelty:** rejected (C1) — see §2 above. Any mention of ADS in §3 (Problem Setting) must be
  paired with the equivalence-to-cluster-purity sentence, not left as a bare definition that a reader
  could mistake for a novelty claim by omission.
- **Architecture novelty:** rejected (C1, C2 general, C6) — the paper's contribution is the *empirical
  finding about* a decision rule, not the rule/architecture itself being new.
- **Enterprise-wide generalization:** out of scope, four preconditions bound it — never implied.
- **Production validation claims:** the case study is context, never evidence — every appearance of a
  production number must carry a "cited, not reproduced" qualifier, matching `TECHNICAL_REPORT.md`
  §3.1's existing pattern.
- **Causal representation-stability claims:** INFERRED, post-hoc, exhaustive-but-not-a-second-
  experiment — must be phrased with that exact epistemic weight (`CONTRIBUTION_LOCK.md` §2 step 8),
  never upgraded to "we prove" or "we demonstrate causally."
- **Unsupported historical production numbers:** the ~55,394 mapping-count figure remains UNRESOLVED
  (`mapping_count_provenance.md`) — **must not appear in the manuscript at all**; only 76,843 is
  canonical and citable.
- **Superseded numbers:** pre-A5-fix synthetic figures (weighted ADS 0.8094, unweighted 0.9310,
  deterministic-share 84.12%) are `SUPERSEDED — DO NOT CITE` per `EVIDENCE_BASELINE.md`; canonical
  post-fix values are weighted 0.9031, unweighted 0.9597, deterministic-share 87.56%. **Phase E must
  verify `TECHNICAL_REPORT.md` §3.2/§3.3 are updated to the canonical figures before any manuscript
  text cites or paraphrases that report** — this was flagged as outstanding in `ROADMAP.md` Phase A
  and is still open as of this pass (verified by direct read, 2026-08-12: `TECHNICAL_REPORT.md` §3.2's
  table still shows 84.1%/0.809/0.931, the pre-fix values).

## 4. Outstanding pre-Phase-E-drafting fixes surfaced by this map

Two factual issues in `TECHNICAL_REPORT.md` are reconfirmed by this pass (not new findings — both were
already flagged in `RESEARCH_AUDIT.md` and `CONTRIBUTION_LOCK.md` §7, restated here because they will
otherwise be silently inherited into the new manuscript's Related Work / motivating-context sections if
copied without re-checking):

1. §5's vendor-practice sentence (contradicted by B8-04).
2. §3.2/§3.3's synthetic figures are the superseded pre-A5-fix values, not the canonical 0.9031/
   0.9597/87.56% figures.

Neither is fixed by this document (out of scope — `TECHNICAL_REPORT.md` edits are prohibited in this
pass). Both must be resolved either in `TECHNICAL_REPORT.md` directly or by the new manuscript simply
not inheriting the stale numbers/sentence — whichever the human author decides — before Phase E3.

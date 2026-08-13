# Manuscript Architecture (Phase E1)

> **No prose is written here.** This document decides the paper's narrative, section structure,
> figures, tables, equations, and evidence flow — E2 (skeleton) and E3 (first complete draft) build
> from this, not from a fresh reading of the evidence. Governed by `research/PAPER_CONTRACT.md`,
> which remains binding; where anything below appears to conflict with the contract, the contract
> wins and this document is wrong, not the other way around. Built from: `CONTRIBUTION_LOCK.md`,
> `contribution_lock.csv`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PHASE_E_PLAN.md`,
> `MANUSCRIPT_FORMAT_RESEARCH.md`, `PUBLIC_RELEASE_BOUNDARY.md`, `literature/contribution_status.md`,
> `literature/prior_art_map.md`, `literature/terminology_map.md`, `literature/citation_ledger.csv`,
> `EXPERIMENT_1_REDESIGN_REVIEW.md`, `EXPERIMENT_1_CALIBRATION_REPORT.md`,
> `EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `EVIDENCE_BASELINE.md`, `RESEARCH_AUDIT.md`. Does not modify
> `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`, or any frozen evidence. Creates no
> `manuscript/` directory, no `.tex` file, no figure, no bibliography, no prose.

---

## 1. Title candidates (ranked, most defensible → most ambitious)

| # | Title | Why it's safe / risk |
|---|---|---|
| 1 | **"Historical Consistency Predicts Classifier Accuracy, Not Classifier Ranking: Evidence from a Controlled Synthetic Study"** | Leads with the exact locked finding (§6a/§6b split preserved in the title itself); "Evidence from a Controlled Synthetic Study" pre-empts any implication of production validation. Most defensible — nothing in it could be read as overclaiming. |
| 2 | **"When Historical Consistency Fails to Select the Right Classification Mechanism: A Study of Representation Stability"** | Question/failure-framed, matches STATE.md's settled "question-first" pitch. Slightly more narrative than #1, still fully bounded — names the actual mechanism (representation stability) rather than a vague "limits." |
| 3 | **"Difficulty, Not Ranking: What Historical Label Consistency Can and Cannot Tell You About Classification-Mechanism Selection"** | More literary framing of the same 6a/6b split. Marginally more ambitious in tone (a colon-and-clause title reads more like a position paper) but makes no claim beyond #1/#2. |
| 4 | **"Rules Before Models, Except When They Aren't: Determinism, Representation Stability, and Mechanism Selection"** | Keeps a lexical link to `TECHNICAL_REPORT.md`'s existing title for cross-document continuity. Riskier only in tone (the "except when they aren't" clause could read as glib to a reviewer) — no claim risk. |
| 5 | **"Design-Time Architecture Selection from Historical Label Consistency: A Negative Result Under Lexical Noise"** | Most ambitious because "design-time architecture selection" echoes the general C2 framing that Phase B/C found CHALLENGED (`contribution_lock.csv` row C2) — safe only because the subtitle immediately narrows it to "a negative result," but a reader who stops at the colon could misread the scope. Kept as a candidate because it is the most literature-legible title (uses the field's own vocabulary, `terminology_map.md`'s "terms this project should adopt" list), not because it is the recommended choice. |

**Recommendation: #1.** It is the only title that states both halves of the locked contribution (6a positive, 6b negative) without relying on a reader continuing past a colon to find the qualifier. #5 is retained only to name and explicitly not choose the more field-jargon-forward option, per the brief's request for a ranked ambitious end.

**Forbidden title patterns** (per `PAPER_CONTRACT.md` §3): anything containing "novel," "validated," "selects the right architecture," or "enterprise" unqualified.

---

## 2. Abstract content specification (not the abstract itself)

The abstract must contain exactly these seven elements, in this order, and nothing else:

1. **Problem.** One sentence: classification systems are usually built by choosing a mechanism (rules, retrieval, a model) up front, without a measured signal for whether that choice fits the data.
2. **Research question.** Exactly `CONTRIBUTION_LOCK.md` §11.A: can historical decision consistency, measured before deployment, be used to select between qualitatively different classification mechanisms?
3. **Method.** One sentence naming the design: a pre-registered, 240-condition synthetic factorial experiment (20 seeds × 6 nominal-consistency targets × 2 lexical conditions), comparing exact-match rules against fuzzy retrieval.
4. **Experimental evidence.** The two headline statistics only (see "Which numbers belong in the abstract," below) — not the full results table.
5. **Main finding.** The 6a/6b synthesis sentence, verbatim in spirit from `CONTRIBUTION_LOCK.md` §6's synthesis: consistency predicts each mechanism's own accuracy but not which mechanism wins; ranking is governed by a lexical/representation-stability factor the consistency signal cannot observe.
6. **Limitation.** One sentence: single synthetic generator, single perturbation model, one motivating (non-evidentiary) production case study.
7. **Implication.** One sentence, forward-looking but explicitly not a built/tested claim: design-time selectors that condition on consistency alone may need a second, representation-stability signal — named as a direction, not a result.

**Which numbers belong in the abstract vs. staying in the body:**

| Number | Abstract? | Why |
|---|---|---|
| Pearson r ranges (0.909–0.959 rules / 0.948–0.955 retrieval) | **Yes**, as one compressed statement ("strongly correlated, r > 0.9 in both lexical conditions") | This is the headline positive half (6a) — needs to be visible at the abstract level, exact per-mechanism split can stay in the body. |
| Band-specific agreement (100% at 0.70–0.90 vs. 0% at ≥0.90) | **Yes** | This is the headline negative half (6b) and the paper's central surprising fact — an abstract that omits it undersells the paper's actual contribution. |
| Overall aggregate agreement (64.0%, 32/50) | **No — body only.** | Per the brief's explicit instruction not to overemphasize the aggregate when the regime-specific structure is more informative (see §4 of this document); the aggregate number without the band breakdown is actively misleading on its own (it hides that agreement is 100% in one band and 0% in another) and does not belong in a 150–250-word abstract that has no room for the caveat that makes it interpretable. |
| Wilson CI / p-value (p=0.065) | **No — body only.** | Statistical-test detail, not abstract-level. |
| 120/120 vs. 120/120 winner-constancy claim | **No — body only**, but its *conclusion* ("ranking is governed by the lexical condition, not by consistency") is exactly element 5 above, stated in words not numbers. |
| Production case-study numbers (91.2%, 0.847, etc.) | **No.** | Per the Production Data Rule (`PAPER_CONTRACT.md` §5), the case study is motivation, and motivation-only numbers do not belong in an abstract whose numerical content should be the paper's actual evidence. A brief non-numeric mention ("motivated by an observed discrepancy in a real deployment") is acceptable in the Introduction, not the Abstract. |

---

## 3. Section architecture

### 3.1 Hierarchy (9 major sections — merges argued below)

```
Title / Abstract
1. Introduction
2. Related Work
3. Problem Setting and Signal Definition
4. Experimental Design
5. Results
6. Discussion
7. Limitations
8. Future Work
9. Conclusion
References
Reproducibility (dedicated subsection, placed at the end of §4 — see §12 of this document)
```

**Merge/rename decisions relative to the brief's 10 "required scientific sections":**

- **METHOD / SIGNAL DEFINITION** and **PROBLEM SETTING** are merged into one section, **§3 "Problem
  Setting and Signal Definition."** Reasoning: the brief lists them separately, but this paper has
  exactly one signal (ADS) and one problem statement (H1) — splitting them into two sections each
  a paragraph long would fragment the narrative for no benefit; ADS's formal definition *is* the
  formal problem setting here, not a separate method contributed on its own (ADS is explicitly not
  a novel-metric claim, `contribution_lock.csv` row C1). A paper with a genuinely separate "Method"
  (e.g., a new algorithm) would keep these apart; this paper doesn't have one.
- **EXPERIMENTAL DESIGN** stays its own section (not merged into Results) because the design itself
  — the factorial structure, the pre-registration, the falsification table — is a load-bearing part
  of the paper's credibility (per `PAPER_CONTRACT.md` §9's "no new experiments" stance and the
  project's own repeated emphasis on pre-registration as evidence of rigor, `CONTRIBUTION_LOCK.md`
  §2 step 6). Reviewers checking whether this is a post-hoc-fit result need the pre-registration
  visible as its own section, not folded into Results where it could read as an afterthought.
  Reproducibility (what a reader can and cannot re-run) is placed as the final subsection of §4
  rather than its own top-level section — it is about *this* experiment's reproducibility
  specifically, not a general statement, so it belongs adjacent to the design it describes.
- **RESULTS** is not split into "accuracy results" and "ranking results" as two top-level sections —
  it is one section with four subsections (§5 of this document, "Results architecture") because the
  two halves need to sit next to each other for the reader to see the contrast directly; separating
  them into different top-level sections would let a skimming reader read only the positive half.
- Everything else (Introduction, Related Work, Discussion, Limitations, Future Work, Conclusion)
  maps one-to-one onto the brief's list, unmerged and unrenamed.

**9 major sections total** (Introduction through Conclusion), matching the brief's "approximately
8-10" instruction.

### 3.2 Per-section design table

| Section | Purpose | Question answered | Claims allowed | Evidence sources | Figures/tables used | Claims that must NOT appear |
|---|---|---|---|---|---|---|
| **1. Introduction** | Motivate the question from a real observation, without using that observation as proof. State the four preconditions and explicit out-of-scope list. | Why does this problem matter? | The production R3-flip is a *motivating observation*, cited not proven; the four preconditions (`STATE.md`) bound scope explicitly from the first page. | `METHODOLOGY.md` real-vs-synthetic table (context only, cited numbers per `PAPER_CONTRACT.md` §7); `STATE.md` settled positioning | Table T1 (optional, small — production-vs-synthetic R3 flip, 4-5 rows) — see §8 | "Production data independently validates..."; "enterprise AI broadly"; any implication the case study is evidence |
| **2. Related Work** | Position against Rice/meta-learning/AutoML-workflow-composition/self-designed-systems/reject-option/L2D/LLM-routing lineages, using the field's own vocabulary. | What did prior work already establish? | Positioning only — "the closest work does X, this differs by Y," never "no prior work exists." ADS = cluster purity/majority-vote-agreement, stated plainly, not defended. | `citation_ledger.csv` (VERIFIED/-INDUSTRY/-PREPRINT rows only); `ads_metric_prior_art.md`; `contribution_status.md`; `prior_art_map.md`; `terminology_map.md` | Table T2 (literature positioning) — see §8 | "ADS is a novel metric"; "no prior work anticipates design-time architecture selection"; any claim the *general* C2 pattern is new |
| **3. Problem Setting and Signal Definition** | Define ADS formally, paired immediately with its equivalence citation. State H1 exactly as pre-registered. | What question remains, precisely? | ADS formula (descriptive); H1 (revised) exactly as `EXPERIMENT_1_REDESIGN_REVIEW.md` §2 states it. | `TECHNICAL_REPORT.md` §2.2 (formula only, not its framing prose); `EXPERIMENT_1_REDESIGN_REVIEW.md` §2 | Equation E1 (ADS formula) — see §9 | Any bare ADS definition without the equivalence-to-cluster-purity sentence in the same paragraph |
| **4. Experimental Design** | Full method transparency: generator, mechanisms, perturbation model, pre-registration, falsification table, calibration, reproducibility. | What exactly did we test? | Design description only, no results yet. Explicit statement that the LLM mechanism was excluded for a documented reason, not omitted by oversight. | `EXPERIMENT_1_REDESIGN_REVIEW.md` (§§2-20); `EXPERIMENT_1_CALIBRATION_REPORT.md` | Figure F1 (experimental design diagram); Table T3 (experimental configuration) — see §7-8; Reproducibility subsection (§12) | Any result, even in passing ("...which turned out to..."); any claim about what the LLM *would* have shown |
| **5. Results** | Report both halves of the accuracy/ranking distinction without merging them; regime-specific structure over the flat aggregate. | What did we find? | Exactly `CONTRIBUTION_LOCK.md` §4/§6a/§6b, same numbers, same CIs. See §4 of this document for full subsection design. | `final_condition_results.csv`; `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4-6; `AUDIT_REPORT.md` (independent re-derivation) | Figures F2, F3, F4; Tables T4, T5 — see §7-8 | "ADS predicts mechanism suitability" (unqualified); "higher ADS means rules is better"; any framing that leads with the flat 64.0% before the band structure |
| **6. Discussion** | Synthesize; relate to literature; place the case study as brief context; state what practitioners should NOT infer. | What does it mean? | Exactly `CONTRIBUTION_LOCK.md` §6's synthesis sentence, no stronger. Explicit "what this does not license" subsection. | `CONTRIBUTION_LOCK.md` §5-6; `terminology_map.md`'s adoption list | none required; may reuse Table T2 by reference | Any claim that a two-feature (ADS + representation-stability) selector was built or tested; any generalization beyond the tested generator/mechanisms/perturbation |
| **7. Limitations** | Every item in `CONTRIBUTION_LOCK.md` §9 and `PAPER_CONTRACT.md` §6, undiluted. | What are the limits? | Negative/boundary statements only. | `CONTRIBUTION_LOCK.md` §9; `PAPER_CONTRACT.md` §6 | Table T6 (optional, if the limitations list is long enough to benefit from tabular form) — see §8 | Any hedge that softens a limitation into a strength ("...though this suggests...") |
| **8. Future Work** | Named, not built, explicitly hedged. | What comes next? | Every item phrased "not built, not tested here." | `CONTRIBUTION_LOCK.md` §10 | none | Presenting the two-feature selector as designed, prototyped, or partially validated |
| **9. Conclusion** | One paragraph, restates the finding — the highest-risk section for claim inflation. | What is genuinely new/useful? | No new claims — exact restatement of `CONTRIBUTION_LOCK.md` §11.B/§11.C. | `CONTRIBUTION_LOCK.md` §11 | none | Any sentence not traceable to a Results/Discussion claim already made earlier in the paper |

---

## 4. Results architecture

**Governing rule (per the brief, restated as a structural constraint):** Results must never collapse
**(A) ADS → individual mechanism accuracy** with **(B) ADS → empirical mechanism ranking**. They are
different claims with different truth values (A holds, B is falsified) and get different
subsections, in this order:

### §5.1 Overview and regime structure (not "headline aggregate")

Leads with the **band structure**, not the flat 64.0%. Framing: "Agreement between the frozen
consistency-based rule and the empirically best mechanism is not uniform — it is 100% in one regime
and 0% in another." The 32/50 = 64.0% aggregate (Wilson CI [50.1%, 75.9%], p=0.065) is reported
*after* the band table, explicitly labeled as a summary statistic that obscures the structure just
shown — this directly implements the brief's "do not overemphasize the 64% aggregate" instruction as
a section-ordering decision, not just a stylistic note.

### §5.2 A — ADS predicts mechanism accuracy (6a)

Pearson r(realized ADS, rules accuracy) ≈ 0.909–0.959; r(realized ADS, retrieval accuracy) ≈
0.948–0.955, both lexical conditions (CLEAN, VARIED) reported side by side. Framed explicitly as
*correlational*, per mechanism, never merged into a single "ADS predicts performance" sentence that
elides which mechanism.

### §5.3 CLEAN vs. VARIED (the manipulated factor)

Reports the exceptionless winner-constancy finding as its own subsection, because it is the causal
hinge the rest of the paper depends on: `empirical_winner == "retrieval"` in 120/120 VARIED
conditions; `empirical_winner == "tie"` in 120/120 CLEAN conditions (δ=0.02 practical-equivalence
margin) — both exhaustive over the 240 frozen conditions, unconditional on realized ADS across its
full 0.44–0.93 observed range. States plainly: the lexical condition is a *manipulated, controlled*
experimental factor, not an observational one — this is what licenses the "governed by" language in
6b, not merely "correlated with."

### §5.4 B — ADS does not predict mechanism ranking (6b)

Direct statement of the negative finding, using §5.3's constancy result as its evidentiary basis:
because the empirical winner is constant within each lexical condition regardless of realized ADS,
and ADS itself does not vary with the lexical condition (it is computed on the stable `product_code`,
never the perturbed surface string — restated from `CONTRIBUTION_LOCK.md` §2 step 8), ADS
structurally cannot track the quantity that actually determines the winner.

### §5.5 Mechanism-winner behavior and R3 agreement by realized-ADS region

The band table itself, presented in full: realized ADS <0.70 / 0.70–0.90 / ≥0.90, rules vs. retrieval
mean accuracy and the rules−retrieval gap, per lexical condition (the six-row table from
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5). Explicitly names the **high-ADS reversal**: under VARIED, the
rules−retrieval gap *widens* (from −0.137 at <0.70 to −0.185 at ≥0.90) as ADS increases — the opposite
of what R3's threshold design assumes, and the direct mechanical explanation for why R3's agreement
rate is 100% in the middle band and 0% at the top.

### §5.6 Uncertainty and statistical treatment

Wilson CIs on all agreement rates, the paired-bootstrap tie definition, and the binomial test against
chance (p=0.5, not 1/3, since the LLM leg is excluded — `EXPERIMENT_1_REDESIGN_REVIEW.md` §14).
Placed last so the statistical machinery doesn't precede the substantive finding it supports.

**What is explicitly excluded from Results** (per §3.2's forbidden-claims column and
`PAPER_CONTRACT.md` §6): any sentence generalizing beyond the tested generator, the two tested
mechanisms, the tested `p_transform=0.3` perturbation, or the tested 240-condition factorial design.

---

## 5. Discussion architecture

Eight subsections, directly answering the brief's eight questions, in order:

| Discussion question | Content | Source |
|---|---|---|
| 1. What did we learn? | The 6a/6b synthesis: consistency is informative about difficulty, not ranking, in this experiment. | `CONTRIBUTION_LOCK.md` §6 synthesis, verbatim in spirit |
| 2. What did the original hypothesis get right? | H1 (revised)'s weaker form — "better-than-chance agreement" — is not cleanly confirmed or rejected; it matches the pre-registered PARTIALLY SUPPORTED row exactly (`EXPERIMENT_1_REDESIGN_REVIEW.md` §18), and the paper should say so explicitly rather than let a reader infer either "worked" or "failed." | `EXPERIMENT_1_REDESIGN_REVIEW.md` §18; `EXPERIMENT_1_POSTHOC_ANALYSIS.md` |
| 3. What did it get wrong? | The *unconditional* form ("ADS thresholds alone select the right mechanism") is falsified, exceptionlessly, in the realized ≥0.90 band. | `CONTRIBUTION_LOCK.md` §3 (C2b downgrade) |
| 4. Why is ADS informative about difficulty but insufficient for ranking? | The mechanistic account: ADS is computed on the stable `product_code`, structurally blind to the surface-form perturbation that actually drives the ranking outcome. Stated as INFERRED from exhaustive-but-post-hoc code inspection, not a second confirmatory experiment. | `CONTRIBUTION_LOCK.md` §2 step 8 |
| 5. What does representation stability reveal? | Retrieval's accuracy cost stays flat under noise while rules' cost grows with ADS (the widening gap, §5.5) — the perturbation degrades an exact-match mechanism's precondition (identical surface strings) in a way a fuzzy mechanism is partly robust to; framed as a property of *this* perturbation model and *this* retrieval implementation (rapidfuzz), not fuzzy/embedding retrieval generally. | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5-6 |
| 6. How does this relate to algorithm-selection/meta-learning? | Refines, does not contradict: identifies a specific failure mode of a single-feature, label-consistency-only design-time selector, situated against Rice 1976 / Smith-Miles 2009 / Barbudo et al. 2023's workflow-composition framing. | `CONTRIBUTION_LOCK.md` §5 row 2; `terminology_map.md` |
| 7. What should practitioners NOT infer? | A dedicated, explicit paragraph (not left implicit): do not infer that ADS-style consistency signals are useless (6a still holds), that this generalizes to other noise models or retrieval implementations, that a two-feature fix exists, or that production data confirms this finding. | `PAPER_CONTRACT.md` §3, §6 (the negative checklist, restated in the reader's terms) |
| 8. What future research naturally follows? | Named only: a decision rule conditioning on both ADS and a measured representation-stability signal (explicitly **not built here**); whether the pattern holds for embedding-based retrieval; a real (not synthetic) noise model. | `CONTRIBUTION_LOCK.md` §10 |

**Explicit guardrail for §Discussion.8 / the paper's Future Work section:** the two-feature selector
is named as a *direction*, in future tense, with no implementation detail beyond "condition on both
signals" — no pseudocode, no proposed threshold values, no partial results. Introducing any of those
would cross from "naming a direction" into "presenting an untested method as if scoped," which
`PAPER_CONTRACT.md` §3 row 12 and the brief's own explicit instruction both forbid.

---

## 6. Production case study placement

**Placement: Introduction (primary) + one short Discussion subsection (secondary). Never Results.**

- **Introduction:** the production system's single-run "R3 flip" (RULES_FIRST at 91.2% in
  production vs. EMBEDDING_PRIMARY at 84.1%/87.56%-corrected in the initial synthetic run) motivates
  the research question — stated as an *observation that prompted the question*, with an explicit
  sentence that it is cited, not evidence, and is not independently reproducible from this
  repository (per `PUBLIC_RELEASE_BOUNDARY.md` §3, tier "case-study only / confidential").
- **Discussion (§6.1 or a clearly labeled short subsection):** one paragraph noting that the
  production observation is *consistent with* 6a (ADS did correlate with something real in
  production) but was never itself a controlled test of 6b (production never ran a lexical-noise
  sweep) — explicitly framed as "this experiment does not confirm the production observation, it
  investigates the more general question the observation raised."
- **What can be stated from confidential production data (exhaustive list, per
  `PAPER_CONTRACT.md` §5 and `EVIDENCE_BASELINE.md` §1):** the canonical aggregate statistics —
  91.2% deterministic products, weighted ADS 0.847 (with the "likely understated, unverified"
  caveat, since these are pre-A5-fix production figures with no production data available in this
  repository to re-run), unweighted ADS 0.964, cross-company consistency 0.695, the R1/R3/R4/R5
  decisions. **What cannot be stated:** row-level data, any accuracy number implying the production
  system's cascade was itself validated by this experiment, or any sentence suggesting the case
  study underwent the same lexical-noise manipulation as Experiment 1.
- **Never a pseudo-Results section:** no table in the case study may be formatted or captioned in a
  way that visually resembles Table T4/T5 (the Experiment 1 results tables) — this is a Table-design
  constraint carried into §8 below, not just a prose instruction.

---

## 7. Figure plan

| # | Title | Scientific purpose | X-axis | Y-axis | Grouping | Source artifact | Why the reader needs it |
|---|---|---|---|---|---|---|---|
| **F1** | Experimental design and pre-registration flow | Shows the factorial structure (6 targets × 2 lexical conditions × 20 seeds) and the pre-registration → falsification-table pipeline before any result is shown. | — (flow diagram, no axes) | — | Two lexical conditions as parallel tracks | `EXPERIMENT_1_REDESIGN_REVIEW.md` §6, §18 | Without this, a reader cannot assess whether the eventual result was possible to have come out differently — it is the paper's credibility anchor. |
| **F2** | ADS vs. mechanism accuracy | Visualizes §5.2's 6a correlations directly — the positive half of the finding needs a figure, not just an r value. | Realized ADS (0.44–0.93) | Whole-set accuracy | Two lines/series (rules, retrieval), faceted or colored by lexical condition (CLEAN/VARIED) | `final_condition_results.csv` | A reader should be able to see the strong, roughly linear relationship, not just read "r=0.91–0.96." |
| **F3** | R3 agreement by realized-ADS region | The paper's headline finding — 100% (32/32) at 0.70–0.90 vs. 0% (0/18) at ≥0.90. | Realized-ADS band (<0.70, 0.70–0.90, ≥0.90) | Agreement rate (%) | CLEAN vs. VARIED as separate bars/panels | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4-5 | A single bar chart communicates the reversal instantly; the number alone ("100% vs 0%") undersells how stark and legible the pattern is visually. |
| **F4** | Mechanism-ranking constancy across the lexical condition | Visualizes the exceptionless 120/120 (VARIED, retrieval) vs. 120/120 (CLEAN, tie) winner-constancy claim that grounds 6b's causal account. | Realized ADS (0.44–0.93) | rules − retrieval accuracy difference | Two series (CLEAN, VARIED), zero-line marked | `final_condition_results.csv` | Shows *directly* that the sign of the accuracy difference never crosses zero within a lexical condition regardless of ADS — the single most important figure for the paper's central claim, second only to F3. |
| **F5 (candidate — table preferred)** | ADS × lexical-condition interaction, decomposed | Would show the widening rules−retrieval gap under VARIED as ADS rises. | Realized-ADS band | rules−retrieval accuracy gap | CLEAN vs. VARIED | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5 table | **Kept as Table T5, not a figure** (see §8) — the exact numbers (six rows, two lexical conditions) communicate more precisely than a small multi-line plot would at this data density; a figure here would be decorative, not informative, given F3/F4 already carry the visual weight. |
| **F6 (candidate — rejected)** | Production-vs-synthetic conceptual framework / evidence-to-mechanism pipeline | Would diagram how production motivated the question, and how ADS "flows into" mechanism selection generally. | — | — | — | — | **Rejected.** Per `PHASE_E_PLAN.md`'s own prior F6/F7 analysis, this risks re-introducing the *general* C2/C3 architecture claims (CHALLENGED) as if they were this paper's subject, and edges toward the "research architecture" project-history framing explicitly forbidden by this task's brief. If Introduction-section readability genuinely needs a visual, a small inline schematic of *just* the R3 decision rule (three bands, three outcomes) could substitute — deferred to E2/E3 drafting judgment, not pre-committed here. |

**Minimum figure set for E3: F1, F2, F3, F4.** Four figures, all directly evidentiary, none
decorative — matches `PHASE_E_PLAN.md`'s prior figure plan and is not revised upward or downward by
this pass; this document confirms rather than re-derives that conclusion, now organized against the
Results architecture in §4 above.

---

## 8. Table plan

| # | Title | Contents | Placement | Why this table, not a figure or prose |
|---|---|---|---|---|
| **T1 (optional)** | Production case study snapshot | 4-5 rows: production vs. initial-synthetic R3 flip (deterministic-share, weighted/unweighted ADS, R3 decision), each cell tagged "cited" or "computed here" | Introduction | Small enough that prose could carry it, but a table makes the "cited vs. computed" distinction visually unambiguous — directly supports the Production Data Rule (`PAPER_CONTRACT.md` §5). Visually distinct in style from T4/T5 (per §6's constraint) — no shared caption template, no shared column layout. |
| **T2** | Literature/contribution positioning | Rows = research families (Algorithm Selection Problem, meta-learning/AutoML, workflow composition, self-designed data systems, reject-option/selective classification, learning-to-defer, LLM routing/cascading); columns = "what prior art does," "what we do not claim," "the narrow delta" | Related Work | This is exactly the structure `terminology_map.md` and `contribution_status.md` already organize their findings around — reusing that structure as a table is the most honest, least-invented way to present positioning; prose alone would either compress it lossily or run long. |
| **T3** | Experimental configuration | Generator scale (60 companies, 1,200 products), mechanisms (rules_only/retrieval_only, cutoff=75), perturbation (`p_transform=0.3`, 5 transform types), factorial design (6×2×20=240), frozen thresholds (0.90/0.70), δ=0.02 | Experimental Design | A reader auditing reproducibility needs every frozen parameter in one place, not scattered across paragraphs. |
| **T4** | Main results table | Overall agreement (32/50, 64.0%, CI, p); band-level split (32/32 vs 0/18); Pearson r ranges (6a) | Results §5.1/§5.2 | The paper's central quantitative claim belongs in one canonical table other sections can point back to, rather than being restated with slightly different rounding in multiple places. |
| **T5** | Mechanism-winner behavior by ADS region | The six-row table from `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5: realized-ADS band × lexical condition → rules acc, retrieval acc, gap | Results §5.5 | Exact numbers matter here (the widening-gap pattern is the mechanistic explanation for 6b) — a figure would lose precision a reviewer checking the claim would want. |
| **T6 (optional)** | Limitations/reproducibility summary | One row per limitation category, tagged by which of `CONTRIBUTION_LOCK.md` §9's items it is, plus a "reproducible?" column | Limitations or Reproducibility subsection | Only include if the prose list (§11 of this document) reads as too long to scan — a judgment call deferred to E3 drafting, not decided now. |

**No redundant tables:** T1 and T4/T5 never share numbers (T1 is production-only, T4/T5 are
synthetic-only, per the Production Data Rule) — this is a deliberate non-overlap, not an oversight.

---

## 9. Equation plan

| # | Equation | Role | Novelty framing |
|---|---|---|---|
| **E1** | ADS definition: $\text{ADS}(p) = \dfrac{\max_i c_i}{\sum_i c_i}$ | Formalizes the one signal the entire paper is about; needed so Results/Discussion can refer to "ADS" precisely rather than only descriptively. | **Not presented as novel.** Introduced in the same paragraph as its citation to cluster purity (Manning et al. 2008; Amigó et al. 2009) and the majority-vote-agreement baseline (Dawid & Skene 1979 lineage) — per `terminology_map.md`'s explicit recommendation that silence on this point is "the single highest-risk omission a literature-aware reviewer would flag." |
| **E2** | R3 mechanism-selection rule: a step function of realized ADS mapping `≥0.90 → rules`, `[0.70,0.90) → retrieval`, `<0.70 → excluded (LLM_REQUIRED)` | Needed to state precisely what the frozen decision rule *is* before Results reports its agreement with the empirical winner — without this, "R3" is an opaque label. | Not a contribution — an existing, frozen, pre-dating-this-research artifact (`04_architecture_decision.py`'s thresholds), stated for precision, not claimed as new. |
| **E3** | Empirical winner / tie definition: mechanism with strictly higher whole-set accuracy wins; a TIE if the paired-bootstrap 95% CI on the accuracy difference overlaps zero within δ=0.02 | Needed for Results to be checkable — "winner" is a defined statistical procedure, not a judgment call, and the definition must be visible near where it's first used. | Standard practical-equivalence testing, not presented as a methodological contribution. |
| **E4 (optional)** | Agreement-rate aggregation: agreement = (# rule-selected == empirical-winner) / (# conditions with a defined comparison, excluding ties and N/A) | Could be stated as an equation or as prose; include only if E3 drafting finds the prose version ambiguous. | Not novel — standard conditional-proportion definition. |

**Explicit framing rule for this whole section (per the brief):** ADS is not a novel mathematical
contribution. Every equation above is either (a) a restatement of an existing, cited construct (E1),
(b) a precise restatement of an existing, frozen, pre-dating-this-research procedure (E2), or (c) a
standard statistical definition (E3/E4) — none is introduced as this paper's contribution. The
paper's actual contribution is entirely empirical (the 6a/6b finding), not mathematical.

---

## 10. Related Work positioning

Structured around exactly the research families `contribution_status.md`/`prior_art_map.md`/
`terminology_map.md` already established — no new family is invented, no new gap is claimed beyond
what Phase B/C already found.

| Research family | What prior art already does | What this paper does NOT claim | The narrow delta that remains |
|---|---|---|---|
| **Cluster purity / majority-vote agreement** (Manning et al. 2008; Amigó et al. 2009; Dawid & Skene 1979 lineage) | Defines the exact closed-form expression ADS uses, under "cluster" ↔ "item's historical booking multiset." | That ADS is a novel metric. | None at the metric level — the delta, if any, is entirely in what the metric is *used for* (see next row), not its formula. |
| **Algorithm Selection Problem** (Rice 1976) and its **meta-learning** descendants (Smith-Miles 2009; Ali & Smith 2006; Khan et al. 2020) | Selects a single algorithm/ML model per instance or per dataset via historical performance or generic statistical meta-features. | That design-time selection from historical evidence is itself new (C2, CHALLENGED). | This paper studies whether a *label-consistency-specific* signal (not generic meta-features, not performance search) predicts a *qualitative mechanism-class* choice — the C2b framing — and reports where that narrower claim holds and where it doesn't. |
| **AutoML / workflow composition** (Barbudo et al. 2023) | Automated, benchmarked-performance-driven search over combinatorial pipeline configurations. | That this paper's simple, interpretable threshold rule is a competing AutoML method. | The delta is evidence type (label-consistency vs. benchmarked search) and interpretability (a named threshold vs. an optimization search) — stated as a difference in kind, not a claim of superiority. |
| **Self-designed / instance-optimized data systems** (Idreos & Kraska 2019; Kraska 2021) | Measure historical workload/query-frequency evidence to choose system composition, typically continuously, not as a one-shot gate. | That the "one-shot before deployment" design is itself a contribution (already the opposite of this literature's stated thesis, cited as contrast). | This paper's experiment is about the *specific signal type* (label consistency, not workload frequency) and its specific limitation (blindness to representation instability), not about defending the one-shot-gate design pattern generally. |
| **Reject option / selective classification** (Chow 1970; El-Yaniv & Wiener 2010; Hendrickx et al. 2024 survey) | Single-threshold accept/reject decisions on live posterior confidence, inference-time. | That this paper introduces a new reject-option variant. | Not directly relevant to Experiment 1 at all (Experiment 1 tests a design-time rule, not a runtime reject threshold) — mentioned only to establish the *inference-time vs. design-time* distinction the paper's framing depends on (per `STATE.md`'s settled positioning), not as a competing method. |
| **Learning to defer** (Madras et al. 2018; Mozannar & Sontag 2020) | Trained/rule-based deferral to a human, informed by historical decision data, as a single binary per-item decision. | That this experiment's mechanism-selection rule is a learning-to-defer instance. | Same as above — establishes the design-time/inference-time boundary the paper's scope sits on one side of; the production cascade (not tested here) sits closer to this literature, but that system is out of scope for Experiment 1. |
| **LLM routing / model cascades** (Chen et al. 2023, FrugalGPT; Dekoninck et al. 2024) | Historically-calibrated, confidence-gated escalation across models of varying cost/capability. | That Experiment 1's two-mechanism comparison is a cascade contribution. | Not directly relevant — the LLM mechanism is explicitly excluded from Experiment 1 (`EXPERIMENT_1_REDESIGN_REVIEW.md` §10); this family is cited only for completeness of the design-time/runtime distinction, not engaged as a comparison point for the actual experiment. |
| **Domain-specific practice** (Jørgensen & Igel 2021; Ken From Finance / Peakflo / Ramp industry sources) | Empirically documents the same cross-company generalization phenomenon (Jørgensen & Igel) and similar informal historical-consistency-audit practice (industry sources) in the same/adjacent domain. | That the application domain itself is unprecedented, or that no vendor measures before choosing (industry sources directly contradict that framing — `contribution_status.md` C8). | The domain remains academically under-served (no peer-reviewed SAF-T/D406-specific ML paper found), which is a narrow, honest niche-novelty claim — separate from and much weaker than any methodological novelty claim. |

**No new gap is claimed.** The "narrow delta" column in every row restates, does not extend, Phase
B/C's own findings. This section's job in the manuscript is to make the paper's positioning legible
to a reviewer who knows this literature, not to argue for a bigger gap than Phase B/C already found.
Citations themselves are not written here (per the brief) — this table is the *structure* Related
Work's prose will follow in E2/E3.

---

## 11. Limitations structure

One paragraph or bullet per item, all drawn from `CONTRIBUTION_LOCK.md` §9 / `PAPER_CONTRACT.md` §6,
organized into four groups so the section doesn't read as an undifferentiated list:

**A. Scope of the case study (motivation, not evidence)**
1. Validated in one application domain (Romanian fiscal-document / invoice GL-account
   classification) — the case study, not the experiment, which is domain-agnostic by construction.
2. The production motivation is confidential, cited not reproduced; production ADS figures are
   pre-A5-fix and "likely understated, unverified."

**B. Scope of the synthetic experiment**
3. Single synthetic generator family; 240 conditions replicate a seeded RNG, not an external
   population.
4. Single lexical-perturbation model (`p_transform=0.3`, five fixed transform types), pilot-tuned to
   a target corruption-share band, not derived from measured real-world OCR/typo error rates.
5. Only two mechanisms compared (exact-match rules vs. rapidfuzz retrieval, cutoff=75) — not
   embeddings, not the shipped production cascade.
6. The LLM mechanism was excluded from H1 for a documented, principled reason (the synthetic
   product string carries no signal predictive of the true label), not because it was inconvenient.
7. The realized-ADS ceiling (~0.91, from the fixed `CROSS_COMPANY_ALIGN=0.695` nuisance parameter)
   means the "deep rules-first" region (≥0.93) was never reachable — untested, not merely
   unfavorable.

**C. Scope of the statistical finding**
8. H1 (revised) is only *partially* supported, matching the pre-registered PARTIALLY SUPPORTED row
   exactly — this is stated as the honest verdict, not softened toward either "confirmed" or
   "refuted."
9. Retrieval coverage is 1.0 in all 240 conditions (never abstains at cutoff=75); rules coverage is
   always <1.0 — a real asymmetry, part of the explanation, not normalized away.
10. D.1's causal account (ADS's blindness to surface form) is a well-evidenced, exhaustive, but
    **post-hoc** explanation of already-frozen data, not a fresh prospective confirmation.

**D. Scope of what is not built**
11. No two-feature (ADS + representation-stability) selector was designed, prototyped, or tested —
    named only as future work.
12. No deployment or generalization claim: the finding describes this experiment, not a
    recommendation for how to build classification systems in general.

**Negative finding is not hidden anywhere in this structure** — group C explicitly leads with the
"partially supported, not confirmed" verdict rather than burying it after a list of scope caveats
that could read as excuse-making.

---

## 12. Reproducibility (subsection of §4 Experimental Design)

Four-part structure, directly reusing `PHASE_E_PLAN.md`'s Task 6 reproducibility tiers, restated
here in the manuscript's own voice:

1. **What is public.** The Experiment 1 generator, mechanisms, perturbation model, calibration
   scripts, and analysis code (`scripts/experiments/exp1/*`) — all offline, no API keys, no cost,
   already committed and tested (`test_generator_rng.py`, `test_leakage.py`, `test_mechanisms.py`,
   `test_lexical_transform.py`, `test_stats.py`, all passing per the E0 checkpoint audit).
2. **What is synthetic.** The 240-condition dataset itself is generated, not collected — a reader
   re-running the committed seed manifest reproduces the identical `final_condition_results.csv`
   this paper's Results section reports.
3. **What is confidential.** The production case study (Introduction, Discussion §6.1) — cited
   aggregate statistics only, no row-level data, explicitly and repeatedly labeled non-reproducible
   from this repository.
4. **What readers can and cannot reproduce**, stated as a direct pair of sentences: *can* — the
   entire statistical evidence base for 6a/6b, end-to-end, from public code with no client data;
   *cannot* — the production motivating observation, which is cited, not offered as something to
   re-run. **Where the public artifacts live:** the paper's own public GitHub repository (name/URL
   deferred to E7's arXiv-package assembly, per `PUBLIC_RELEASE_BOUNDARY.md` §3.B's
   recommendation to link rather than bundle the raw CSV).

---

## 13. E3 storyline test (7-10 sentences, NOT manuscript prose)

Classification systems are usually built by picking a mechanism — rules, retrieval, a model — before
measuring whether the data actually supports that choice. We ask whether a simple, pre-deployment
signal of historical label consistency can be used to pick the right mechanism ahead of time. We test
this with a pre-registered, 240-condition synthetic experiment comparing exact-match rules against
fuzzy retrieval under two lexical conditions, using a frozen consistency-threshold rule that a real
production system already uses. We find that the consistency signal strongly predicts each
mechanism's own accuracy, but does not predict which mechanism actually wins — the winner is instead
a constant function of a separately-manipulated lexical-noise condition, exceptionlessly, across the
signal's entire observed range. As a result, the frozen rule agrees with the true winner 100% of the
time in one consistency band and 0% of the time in another, because the signal is blind, by
construction, to the surface-form instability that actually decides the outcome. This is a real but
narrow limitation: consistency is informative about difficulty, not about which mechanism to deploy,
at least under the noise model and mechanisms tested here. We do not claim this generalizes beyond
this synthetic setting, and we do not propose or test a fix — only that a design-time selector built
on consistency alone should not be trusted to pick a winner without also accounting for representation
stability. The contribution is this precise, evidenced boundary on what a historical-consistency
signal can and cannot tell a system designer, not a new metric, a new architecture, or a validated
selection method.

**Coherence check (per the brief's instruction — revise the architecture if this story cannot be told
without overclaiming):** every sentence above maps to an already-allowed claim in
`PAPER_CONTRACT.md` §2 (rows 3, 4, 5, 6, 7) or an already-required limitation (§11 groups B-D above).
No sentence needed softening or removal to pass this check — the architecture in §§1-12 is consistent
with this story as written, so no revision was required.

---

## 14. Remaining human decisions

Carried forward, unresolved by this document (not this phase's job to resolve):

1. Whether Figure F6 (a small inline R3-decision-rule schematic, discussed and provisionally
   rejected in §7) is worth adding once §Introduction is actually drafted in E2/E3 — a drafting-time
   call, not an architecture-time one.
2. Whether Table T1 (production snapshot) and T6 (limitations summary) are worth including as tables
   versus staying as prose — both marked optional, deferred to E2 skeleton review.
3. Final title choice among the five ranked candidates (§1) — this document recommends #1 but does
   not select it unilaterally.
4. The three open items already carried from `MANUSCRIPT_FORMAT_RESEARCH.md` §3 (endorsement
   contact, license choice, AI-assistance disclosure wording) remain open and are unaffected by this
   architecture pass.

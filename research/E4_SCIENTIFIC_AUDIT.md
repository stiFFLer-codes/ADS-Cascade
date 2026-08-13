# E4 — Adversarial Scientific Manuscript Audit

> Phase E4: determines whether the Phase E3 manuscript checkpoint (`manuscript/main.tex` @ commit
> `95c2b18b7a49898233a1d0d44e4cfbae1fb7c071`) is scientifically coherent, evidence-grounded, and
> defensible to a skeptical external researcher. This is a **review-only** phase: no experiment was
> run, no frozen evidence was modified, no methodology was altered, no citation was searched for or
> added, and `manuscript/main.tex`/`manuscript/references.bib` were not edited. Two independent
> reviewers contributed: this document's Parts A, C, D, H, J, K, L were written directly by the
> primary session (a fresh, critical read of the manuscript as a standalone document, then
> cross-checked against repository artifacts); Parts B, E, F, G, I were performed independently by
> the `research-code-auditor` subagent and are reproduced/summarized below from its full report,
> `research/E4_ARTIFACT_AUDIT.md` (read in full and verified before being incorporated here — not
> merely trusted from its summary).

---

## PART A — External Reviewer Assessment

*Read as a standalone document: title, abstract, and body prose only — not the `%` development
comments, which never appear in a compiled PDF.*

**1. What is the paper's central question?**
Can historical decision consistency, measured before deployment, be used to select between
qualitatively different classification mechanisms (exact-match rules vs. retrieval-based fuzzy
matching)? This is stated identically, almost word-for-word, in the Abstract, §1.4, and the
Contribution statement (§1.7) — a reviewer would have no trouble identifying the question, because
it is repeated verbatim rather than paraphrased differently each time.

**2. What does the reader think the contribution is?**
A precise negative-plus-positive boundary result: a historical-consistency signal (ADS) is a good
predictor of how well each of two mechanisms individually performs, but a bad predictor of *which*
one wins, because the thing that actually decides the winner (surface-form/lexical stability) is a
variable the signal cannot see. The reader comes away thinking this is fundamentally a **negative,
scope-narrowing result about one specific pre-existing threshold rule** (R3), dressed in the
vocabulary of a positive contribution ("a precise, evidenced boundary"). That framing is honest but
worth naming plainly: this is not a method paper or a new-metric paper: it is a targeted falsification
study.

**3. Is the contribution actually clear?**
Yes — arguably to a fault. The same sentence (consistency predicts difficulty, not ranking) appears
near-verbatim in the Abstract, §1.6, §1.7, §5.7, §6.1, and the Conclusion. Clarity is not the
problem; **repetition** is (see Part J).

**4. What is the strongest claim?**
The exceptionless 120/120 (VARIED → retrieval always wins) / 120/120 (CLEAN → always tie)
winner-constancy result (§5.3). It requires no confidence interval, no p-value, and no statistical
argument at all — it is a deterministic pattern over every condition actually run, and it is the
fact the entire negative finding is built on. It is also the easiest claim in the paper for a
reader to independently verify (public code, public seed manifest).

**5. What is the weakest / most vulnerable claim?**
Two candidates, and a reviewer would likely go after the first:
- The retrieval mechanism's comparative robustness to lexical noise (§5.5, §6.5) risks reading as
  close to true by construction: the perturbation was designed to attack exact-string matching
  (case/punctuation/reorder/abbreviation/whitespace), and the comparison mechanism is *specifically*
  a fuzzy-string matcher built to be robust to exactly that class of noise. The paper does scope this
  carefully ("a property of this specific perturbation model and this specific retrieval
  implementation," §6.5) but does not explicitly anticipate the "isn't this expected by design"
  objection anywhere in the text — see Part K, Objection 1.
- The "governed by a representation-stability property" language (§6.1, Conclusion) is the paper's
  central rhetorical phrase, and it does the work of sounding like an explanation while the paper's
  own §6.4 explicitly labels the underlying causal account as *inferred, post-hoc, not a second
  confirmatory experiment*. The two halves are logically consistent (the paper is careful never to
  say "we prove" or "we demonstrate causally"), but a reader who reads the Conclusion in isolation,
  without §6.4's hedge freshly in mind, could walk away with more causal confidence than the
  evidence supports.

**6. What evidence is convincing?**
The pre-registration/falsification-table discipline (§4.11, matching a table fixed before any data
existed); the exceptionless per-condition winner constancy; the mechanism-blind calibration of both
the ADS target bands and the retrieval cutoff (neither was tuned using mechanism-accuracy outcomes);
and the explicit, code-verified train/test separation. These are the marks of a genuinely
careful experiment, not a post-hoc narrative fitted to convenient data.

**7. What evidence is missing?**
A second, independently generated dataset (acknowledged explicitly as future work, §8.4) — so every
claim, including the "structurally capped ceiling" and "widening gap" patterns, rests on **one**
generator family. No sensitivity analysis on the practical-equivalence margin δ=0.02 (would a
different, still-defensible δ change which conditions are "tied" enough to matter?). No actual
rendered figures — all four figure slots are `TODO` placeholder boxes, not charts (see Part H). A
reader cannot visually confirm the pattern the text describes; they must trust the tables and prose.

**8. What seems overclaimed?**
Nothing rises to a forbidden-claim violation (independently checked, five separate times across this
project's history — see Part B/E below) — but "governed by" (used for both the licensed,
manipulated-factor relationship *and*, more loosely, as a paraphrase in the Conclusion) sits close
enough to the causal-language line that a careful reviewer would ask the authors to justify the verb
choice explicitly rather than infer the justification from an earlier subsection.

**9. What seems underexplained?**
Why δ=0.02 specifically (the manuscript states it was "anchored to precedent" without saying what
precedent, inside the paper itself — the actual justification lives only in a supporting document,
`EXPERIMENT_1_CALIBRATION_REPORT.md`, not in the manuscript text a reader has in front of them).
Why exactly six nominal targets, and why $P_{\mathrm{TRANSFORM}}=0.3$ specifically rather than the
other two pilot-tested candidates (0.5, 0.7) — the paper states these were chosen by calibration but
does not show the reader the calibration curve or acceptance criterion inline.

**10. What would a skeptical reviewer attack first?**
Almost certainly external validity: one synthetic generator, one perturbation model, one motivating
domain, no second dataset, no real-noise validation. The paper's own Limitations section pre-empts
much of this, which blunts but does not eliminate the attack (see Part K, Objection 4).

**11. Is the negative H1 result intellectually integrated or merely tolerated?**
**Integrated.** This is a genuine strength. Results leads with the band structure before the flat
aggregate (a deliberate ordering choice, explained in-text); Discussion has dedicated,
adjacently-placed subsections for "What the Original Hypothesis Got Right" and "...Got Wrong"; the
Limitations section leads with the honest PARTIALLY_SUPPORTED verdict rather than burying it after a
list of scope caveats. A reader cannot come away thinking the negative result was minimized.

**12. Does the paper explain why mechanism-level accuracy and mechanism ranking are different
scientific quantities?**
Yes, explicitly, before any result is shown (§3.5, "Mechanism Accuracy vs. Mechanism Ranking") and
reinforced in Discussion (§6.4). This is one of the paper's best-executed structural decisions.

**13. Does the production case study blur into experimental evidence?**
No, with one narrow exception at the sourcing-precision level (not a blurring into "evidence" —
see Part F below, Finding F3: one production-derived parameter is missing its confidentiality
qualifier at one location, a compliance-precision gap, not a case of production data functioning as
statistical evidence).

**14. Is the scope honestly bounded?**
Yes — this is the paper's other clear strength. Ten distinct Limitations subsections, six Future
Work items all explicitly hedged as "not built, not tested here," and a "What Practitioners Should
NOT Infer" subsection that states four negative inferences explicitly rather than leaving them
implicit.

**15. Does the conclusion follow from the results?**
Yes. The Conclusion's five numbered points map one-to-one onto claims already established in Results
and Discussion; no new claim, number, or scope expansion appears for the first time in the
Conclusion.

---

## PART B — Claim/Evidence Audit (independent pass; full detail in `research/E4_ARTIFACT_AUDIT.md`)

Performed independently by the `research-code-auditor`, read and verified in full before inclusion
here. **27 substantive claims audited** across Introduction, Related Work, Problem Setting,
Experimental Design, Results, Discussion, and Limitations:

- **24 SUPPORTED** — number/definition/scope all verified against the named frozen artifact.
- **2 CASE_STUDY_ONLY / CONDITIONALLY_SUPPORTED** — the Dawid–Skene equivalence sentence (§2.1)
  slightly compresses the literature ledger's own "Analogous vs. Equivalent" nuance (Finding F1,
  non-blocking, under-claims if anything); the production-case-study claim as a whole is correctly
  scoped except one location missing its qualifier (Finding F3, **required**, see Part F).
- **1 AMBIGUOUS** — the realized-ADS-range sentence ("ranges 0.44–0.93... capped below ~0.91") is
  numerically self-consistent (mean ceiling vs. individual-seed maximum) but reads as
  self-contradictory on first pass; wording is inherited verbatim from `CONTRIBUTION_LOCK.md` §8 and
  `PAPER_CONTRACT.md` §6/§7, not manuscript-introduced (Finding F2, non-blocking).
- **0 UNSUPPORTED, 0 SUPERSEDED.** No stale pre-A5-fix number (0.8094 / 0.9310 / 84.12%) or the
  unresolved ~55,394 figure appears anywhere in the manuscript body.

---

## PART C — Scientific Logic Audit

Chain: motivation → question → literature → hypothesis → experimental design → result →
interpretation → contribution.

| Transition | Rating | Why |
|---|---|---|
| motivation → question | 🟢 GREEN | The production R3-flip observation directly and narrowly motivates the stated question; no unjustified leap. |
| question → literature | 🟢 GREEN | The question is situated precisely in the Algorithm Selection / meta-learning lineage and narrowed to the specific C2b instance, matching the literature ledger's own gap analysis. |
| literature → hypothesis | 🟡 YELLOW | "No direct anticipation found in the literature sweep" → "therefore worth testing" is a reasonable, standard inferential step for a paper's motivation, but absence-of-evidence is not itself evidence the question is important — a normal, not unusually risky, inferential step. |
| hypothesis → experimental design | 🟢 GREEN | H1 (revised) is operationalized precisely — R3 vs. empirical winner, explicit chance baseline, explicit falsification table — with no daylight between what was hypothesized and what was tested. |
| experimental design → result | 🟢 GREEN | Results are reported exactly as pre-registered; the observed pattern matches one of four pre-specified possible falsification-table outcomes, not a post-hoc reinterpretation. |
| result → interpretation | 🟠 ORANGE | The 6a/6b split itself is directly supported (GREEN-level); the causal "why" (ADS's blindness to surface form) requires, and receives, an explicit inferred/post-hoc qualification every time it appears — correctly handled, but this is inherently the paper's most qualification-dependent step. |
| interpretation → contribution | 🟢 GREEN | The contribution statement adds nothing beyond what the interpretation already established; no inflation. |

**Specific items requested:**

1. "Historical consistency → mechanism difficulty": 🟢 GREEN — Pearson r ≈ 0.91–0.96, both lexical
   conditions, correctly labeled correlational throughout.
2. "Historical consistency → mechanism ranking" (does not predict): 🟢 GREEN — exceptionless
   120/120 + 120/120, the paper's strongest and least qualification-dependent claim.
3. Representation stability: 🟠 ORANGE — this is an interpretive label attached to what the
   manipulated lexical condition represents, not itself an independently measured variable; the
   paper's scoping language ("this specific perturbation model and this specific retrieval
   implementation") is the correct and necessary qualification, and it is present every time the
   concept is invoked.
4. Lexical perturbation: 🟢 GREEN as a designed experimental factor (clearly defined, controlled,
   reproducible); any claim connecting it to *real-world* OCR/typo noise is explicitly and correctly
   disclaimed rather than asserted.
5. R3 interpretation: 🟢 GREEN — R3 is treated throughout as a pre-existing, unmodified production
   artifact being tested, not redesigned or moralized; its failure is reported mechanically.
6. "ADS alone is insufficient" conclusion: 🟢 GREEN — directly follows from 6a+6b+the R3-agreement
   band structure; no leap beyond what those three already establish.
7. Any causal-explanation statement: 🟠 ORANGE, consistently — every instance (§6.4 explicitly, and
   the "governed by" language elsewhere) carries or immediately follows an inferred/post-hoc hedge.
   No instance found where causal language appears unhedged (would be RED if found; none was found).

---

## PART D — H1 Audit

Checked every Results, Discussion, Abstract, and Conclusion statement for consistency with
H1 = **PARTIALLY_SUPPORTED** (not SUPPORTED, not FALSIFIED ENTIRELY):

- Abstract: does not use the label "H1" but states both halves (strong accuracy correlation; no
  ranking prediction) without asserting either "confirmed" or "refuted" — consistent.
- §4.1 (Research Hypothesis): states H1 revised exactly, with falsification criteria fixed in
  advance — procedural, not a verdict, consistent.
- §4.11 (Preregistration and Freeze Discipline), line 815: "matches the pre-registered
  PARTIALLY~SUPPORTED row exactly" — explicit, correct.
- §6.3 (What the Original Hypothesis Got Right): "This is not nothing: it is not, however, evidence
  that H1 as originally intended was confirmed" — explicitly blocks the SUPPORTED misreading.
- §6.4 (What the Original Hypothesis Got Wrong): "the *unconditional form* of the original
  hypothesis... is falsified, exceptionlessly, in the realized ≥0.90 band" — the falsification is
  correctly scoped to the unconditional form and to one band, never generalized to "H1 falsified
  entirely."
- §7.10 (H1 Only Partially Supported): leads Limitations with the honest verdict, "not softened
  toward either 'confirmed' or 'refuted.'"
- Conclusion: "H1 overall is only partially supported, not confirmed" — final, unambiguous
  restatement.

**No location found where H1 drifts toward SUPPORTED or toward FALSIFIED ENTIRELY.** The manuscript
consistently preserves: (a) strong relation to individual mechanism accuracy, (b) no ranking
prediction under the tested perturbation model, (c) representation stability as the exposed
limitation of ADS-only selection. **Part D: clean.**

---

## PART E — Novelty / Prior-Art Audit (independent pass; full detail in `E4_ARTIFACT_AUDIT.md`)

Checked against `contribution_status.md`/`citation_ledger.csv` for all ten listed concepts (ADS,
cluster purity/majority agreement, Algorithm Selection Problem, meta-learning, workflow composition,
model cascades, selective classification, reject option, LLM ranking, human deferral).

**No novelty-inflation violation found for any of the ten concepts.** Every Related Work subsection
follows the same disciplined pattern — name the closest prior art, state explicitly what is *not*
claimed, state the narrow delta actually tested — applied exhaustively, not selectively, across all
eight subsections and Table T2. The one precision note (the Dawid–Skene compression, Finding F1) is
a Part B finding restated here because it is Part E-relevant; it does not create a false novelty
claim in either direction (if anything, it slightly under-claims).

---

## PART F — Production Case-Study Audit (independent pass; full detail in `E4_ARTIFACT_AUDIT.md`)

Every production-sourced number/statement's location and framing was checked. **Never observed:** a
production number used as statistical support inside Results, described as "validated," "confirmed,"
or "independently reproduced," or silently reused without its caveat after having carried it once.

**One required finding (F3):** §4.2, line 600 — the cross-company-alignment parameter (0.695) is
introduced as "the production-observed value" **without** the confidentiality/reproducibility
qualifier that every other production figure in the manuscript carries at its point of use, and that
`PAPER_CONTRACT.md` §5 requires at "every" appearance. Not a scientific error (0.695 is correctly
used only as a fixed generator nuisance parameter, never as evidence) — a compliance-precision gap
against the contract's own blanket rule.

---

## PART G — Results/Statistics Audit (independent pass, sixth verification of these numbers this
session; full detail in `E4_ARTIFACT_AUDIT.md`)

- 32/32, 0/18 (realized-ADS-band, per-row): confirmed correctly stated as **not** paired with any
  p-value anywhere in the manuscript.
- 30/30, 2/20 (by-nominal-target): confirmed exact match to `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`.
- 64.0% (32/50): recomputed exactly.
- Wilson CI [50.14%, 75.86%]: independently re-derived by hand from the Wilson formula —
  [50.14%, 75.87%], a 0.01-percentage-point rounding difference, immaterial.
- p=1.9×10⁻⁹ (30/30) and p=4.0×10⁻⁴ (2/20): both independently re-derived from first principles
  ($2^{-29}$ and $422/2^{20}$ respectively) and matched exactly.
- p-value/count pairing: confirmed correct everywhere — 1.9×10⁻⁹/4.0×10⁻⁴ are always attached to
  "30 of 30"/"2 of 20" language, never to 32/32 or 0/18.
- Nominal-target vs. realized-ADS-band framing: confirmed never conflated silently; every use names
  which convention it is using.

**No discrepancy found. This is the highest-confidence section of the entire E4 audit** — these
specific numbers have now been independently re-derived six separate times across this project's
history (five during the E3 checkpoint process, once more here), by six independently-written
scripts, with unanimous agreement.

---

## PART H — Figure / Table Audit

**Table T2** (Related Work positioning): answers a real question (what's the delta vs. each research
family); data traceable to `MANUSCRIPT_ARCHITECTURE.md` §10 / the literature ledgers; caption
accurate; not misleading; not redundant; appropriate density for qualitative claims.

**Table T3** (Experimental configuration): answers "what was frozen"; traceable to
`EXPERIMENT_1_FINAL_RESULTS.md`/`EVIDENCE_CHECKPOINT.md`; accurate; appropriate for a short parameter
list.

**Table T4** (Main results): answers the headline question; traceable; caption is unusually careful
— it explicitly states what is *not* shown (a p-value for 32/32/0/18) and why, which is exemplary
of avoiding misleading-by-omission rather than an instance of it; not redundant; appropriate.

**Table T5** (mechanism-winner behavior by ADS region): answers the mechanistic "why" question;
verbatim-reproduced from frozen evidence; accurate; mildly redundant with §5.5's prose, which
restates several of the same gap values already in the table (`-0.137`, etc.) — a minor stylistic
overlap, not a correctness issue; appropriate density for six rows of precise numbers (a figure
here, per the manuscript's own architecture decision recorded in `MANUSCRIPT_ARCHITECTURE.md` §7,
would lose exactly the precision a reviewer checking this claim would want).

**Figures F1–F4:** all four are, as rendered, `\fbox{...}` **TODO placeholder boxes**, not actual
charts. This is the single most visible incompleteness signal in the current draft to an external
reviewer. Assessed individually:
- Each figure targets a real, distinct scientific question (F1 design flow, F2 ADS-vs-accuracy, F3
  R3-agreement-by-band, F4 ranking constancy) — not decorative, and not redundant with each other.
- Underlying data is traceable: `manuscript/figures/generate_figures.py` (new this checkpoint, not
  yet executed — matplotlib unavailable in this environment, disclosed honestly in its own
  docstring) reads only `final_condition_results.csv` and reproduces the same band thresholds
  (0.70/0.90) and same column (`realized_det_pct`) independently confirmed correct by two separate
  audits this session.
- Captions are scientifically accurate descriptions of what the (not-yet-rendered) figure will show.
- Not misleading as currently labeled — the placeholder text is honestly marked "TODO," not disguised
  as a finished figure.
- **But:** a reader cannot visually verify any of the four claims these figures are meant to support
  until they are actually generated. This is explicitly permitted at the E3 stage per
  `PAPER_CONTRACT.md` §11's definition of done (a captioned placeholder is a valid slot), but it is a
  real completeness gap by the time a document is being evaluated for external-reviewer
  defensibility, which is exactly what E4 asks.

`manuscript/figures/generate_figures.py` was inspected, not executed (matplotlib remains unavailable
in this environment — confirmed again this pass). Consumes only the frozen, approved CSV; introduces
no new statistic; deterministic; independently corroborated three separate times this session
(E3 checkpoint audits + this pass) as reading the correct column and thresholds.

---

## PART I — Reproducibility Audit (independent pass; full detail in `E4_ARTIFACT_AUDIT.md`)

Every element of Experiment 1 itself — seeds, target bands, realized-ADS definition, lexical
conditions, mechanism definitions, retrieval cutoff, winner/tie rule, statistical test, train/test
separation, calibration, and the named entry-point script — is **FULLY REPRODUCIBLE**, independently
confirmed by checking that every named script/file actually exists at its stated repository path,
not merely trusting the manuscript's own claim.

Production case study: **CONFIDENTIAL / CASE-STUDY ONLY**, correctly and consistently labeled as
such throughout.

One **non-blocking gap**: the synthetic-branch 87.56% figure cited in §1.1 is reproducible in
principle from this repository, but via a *different* script chain
(`00_generate_synthetic.py → 03_5_dataset_intelligence.py → 04_architecture_decision.py`) than the
one the Reproducibility Statement names (`run_final.py`, correctly scoped there to "every number in
Section 5" only) — a motivated reader has no signpost to the right entry point for that one
Introduction figure. Not a false claim; a completeness gap (Finding F5, optional).

---

## PART J — Writing / Structure Audit

This is a scientific-writing audit, not copy-editing.

**The dominant structural issue: over-segmentation.** The manuscript contains roughly 65 numbered
`\subsection`s across 9 sections for what is, in content terms, a single-experiment paper. The
Introduction alone has 9 subsections (Real-world motivation / General problem / Existing
algorithm-selection framing / Specific research question / Why historical consistency is attractive
/ What is actually tested / Main findings / Contribution statement / Paper roadmap) — most published
papers in this area cover the same ground in 3–5 flowing paragraphs under one Introduction heading,
not nine separately-titled subsections. Experimental Design has 14. Limitations has 10, several of
which are a single sentence and could be merged (e.g., "Synthetic Generator Scope," "Lexical
Perturbation Model," "Single Application Domain," and "Only Two Mechanisms Compared" are all
instances of one idea — "the tested scope is narrow" — and currently read as four separate headers
each carrying one or two sentences). This structure is a direct, unmodified inheritance from the
Phase E2 skeleton's per-idea draftnote scaffolding (deliberately granular so an auditor could
evidence-anchor each idea independently) — it was never re-flowed into natural prose density once
real content replaced the draftnotes at E3. It does not create a scientific-correctness problem, but
it reads as an audit trail wearing the shape of a paper rather than as a naturally composed paper,
and a copy-editing/E-later pass should consolidate it.

**Repetition.** The 6a/6b synthesis sentence appears in substance at least six times (Abstract, §1.6,
§1.7, §5.7, §6.1, Conclusion) in near-identical phrasing. This aids an auditor tracing claims but
would read as repetitive to a human reviewer reading start to finish.

**Formulaic Related Work.** All eight Related Work subsections follow an identical three-beat
rhetorical template (name the prior art → "we do not claim..." → narrow delta). This is excellent
for auditability and is exactly why Part E found zero novelty-inflation violations — but stylistically
monotonous across eight consecutive instances.

**Buried findings:** none found — the ordering discipline (band-before-aggregate in Results,
honest-verdict-first in Limitations) is a genuine strength, not a weakness.

**Unclear transitions:** none major; section-to-section flow is logical (Introduction → Related Work
→ Problem Setting → Experimental Design → Results → Discussion → Limitations → Future Work →
Conclusion), aided by the explicit roadmap in §1.9.

**Excessive project-history framing:** not present — the paper correctly avoids "Phase 1 → Phase 2 →
Experiment 1" internship-report framing (an explicit, successfully-executed E1/E2 architecture
decision).

**Jargon / missing definitions:** none found; ADS, realized ADS vs. nominal target, R3, and both
mechanisms are each defined precisely before first substantive use.

**Weak opening:** no — the first sentence is concrete and specific, not a generic throat-clearing
statement.

**Conclusion stronger than results:** no (see Part A, Q15 and Part D).

---

## PART K — Reviewer Stress Test

**Objection 1 (generator / lexical perturbation).** *"Isn't 'retrieval beats rules under lexical
noise' close to true by construction? The perturbation (case, punctuation, reorder, abbreviation,
whitespace) is exactly the class of surface noise a fuzzy-string matcher is built to be robust to,
and rules is exact-match by definition. Have you shown anything beyond 'a tool designed for a job
does that job'?"*
- Evidence supporting the objection: the transform set (§4.6) and the retrieval mechanism's own
  definition (rapidfuzz `WRatio`, §3.4) are both explicitly lexical/surface-form constructs; the
  paper never argues the noise model was chosen independently of the retrieval mechanism's known
  strengths.
- Valid? Partially. It is a fair characterization of *why* the mechanistic direction of the result is
  unsurprising, but it does not undermine the paper's actual novel claim, which is not "retrieval
  beats rules under noise" (unsurprising) but "ADS cannot see this coming, and a fixed
  consistency-only threshold fails specifically and predictably in its highest-confidence region"
  (§5.4, §6.4) — that failure mode is not obvious in advance from "fuzzy matching handles fuzzy
  noise."
- How the current paper addresses it: §6.5 scopes the finding to "this specific perturbation model
  and this specific retrieval implementation" — present, but the paper never states the objection
  explicitly or explains why the R3-threshold failure is still the interesting part even if the
  mechanism-level direction is expected.
- What must change: **recommended, not required** — add one or two sentences to §6.5 or §6.7
  explicitly anticipating this objection ("that fuzzy matching tolerates the specific noise types
  tested here is expected; what is not obvious in advance is that a historical-consistency signal
  computed independently of surface form would fail to detect this, and would fail specifically in
  its own highest-confidence band").

**Objection 2 (negative finding / statistical framing).** *"The aggregate agreement (64.0%, p=0.0649)
doesn't clear α=0.05. Is 'PARTIALLY_SUPPORTED' a face-saving redescription of what is, in the
aggregate, a null result?"*
- Evidence supporting the objection: the manuscript itself states the aggregate is "not significant
  at α=0.05" (§5.4).
- Valid? No, on inspection — and the paper's own framing (leading with the band structure, not the
  aggregate) is precisely the correct rebuttal, not a face-saving one: the two individual bands are
  independently significant at p=1.9×10⁻⁹ and p=4.0×10⁻⁴ in *opposite directions*, which is a
  genuine, informative, and pre-registered-possible outcome (the falsification table's own
  PARTIALLY_SUPPORTED row anticipates exactly this pattern, §4.11) — not a post-hoc excuse invented
  after seeing an inconvenient aggregate.
- How addressed: extensively — §5.4, §5.6, §6.3 all state this explicitly and consistently.
- What must change: nothing required; this is the objection the manuscript is best prepared for.

**Objection 3 (novelty / prior art).** *"What is genuinely novel here beyond a negative result about
one specific, already-existing production threshold rule (R3), tested on one synthetic dataset?"*
- Evidence supporting the objection: C1 (ADS as a metric) is explicitly rejected as novel by the
  paper itself; C2 (design-time selection generally) is explicitly stated as well-established;
  R3 itself is a pre-existing, unmodified production artifact, not something this paper designed.
- Valid? Partially — this is a fair characterization of the paper's *ambition level*, and the paper
  does not dispute it (§1.7: "not a new metric... it is a bounded empirical finding about where one
  specific, already-used signal succeeds and where it fails"). The paper's defense is that this is a
  deliberate, stated choice (a narrow, well-evidenced negative/boundary finding over an ambitious but
  under-evidenced positive one), not an oversight.
- How addressed: directly and repeatedly — the paper never claims more novelty than this.
- What must change: nothing required for scientific defensibility; a venue-fit/positioning question
  (is a narrow negative result "publishable" at a given venue) rather than a correctness question,
  and explicitly out of scope for E4 per the brief.

**Objection 4 (external validity).** *"One synthetic generator family, one perturbation model, one
domain-style motivation, no second dataset. How much does this finding generalize even within its own
stated scope?"*
- Evidence supporting the objection: Limitations §7.1–7.2, 7.9 concede exactly this; Future Work
  §8.4 names an independent-dataset replication as not yet done.
- Valid? Yes, and the paper concedes it fully rather than disputing it — this is the strongest
  legitimate objection to the paper's scope, not its correctness.
- How addressed: the paper's own Limitations/Future Work sections state this more thoroughly than
  most papers do, and no sentence in Results/Discussion/Conclusion oversteps this bound.
- What must change: nothing required (already fully conceded); this is inherent to the current
  evidence base, not fixable by prose editing.

**Objection 5 (production/synthetic split).** *"Does the production case study do genuine epistemic
work, or is it decorative motivation that primes the reader to see the synthetic result as somehow
about production, even though the paper disclaims this?"*
- Evidence supporting the objection: the production "R3 flip" observation opens the paper (§1.1) and
  reappears in Discussion (§6.2) before the disclaimer is repeated; a reader could form an
  impression from the framing before reaching the caveat.
- Valid? Partially. The paper's own discipline (never in Results, caveated at every appearance,
  explicit "this experiment does not confirm the production observation" sentence in §6.2) is
  unusually careful and was independently verified clean across every location but one (Part F,
  Finding F3). The residual risk is one of *framing/ordering* (motivation-first), not of an actual
  evidentiary conflation.
- How addressed: thoroughly, with one compliance gap (F3, required — see Part F) and one
  terminology-precision gap that is closely related to this same objection (see below).
- What must change: **required** — fix F3 (missing confidentiality qualifier, §4.2). **Also
  required**, surfaced by the independent artifact audit and directly relevant to this objection:
  §1.1's phrase "the same rule selected a retrieval-based mechanism instead" (describing the
  production/synthetic decision procedure's `EMBEDDING_PRIMARY` output) uses language that overlaps
  with, but does not match, the name of Experiment 1's actually-tested "retrieval" mechanism, which
  §3.4 goes out of its way to define as *not* an embedding model. This creates exactly the kind of
  implicit production↔synthetic-experiment bridge Objection 5 worries about, even though no sentence
  anywhere claims it outright. See `research/E4_ARTIFACT_AUDIT.md` Finding F4 for the precise
  location and suggested rewording.

---

## PART L — E4 Verdict

## 🟡 YELLOW — substantial but non-fatal revisions required

Both independent reviews of this checkpoint — the primary session's literary/structural/logic read
(Parts A, C, D, H, J, K) and the `research-code-auditor`'s independent artifact-verification pass
(Parts B, E, F, G, I) — converge on the same conclusion: **the manuscript's scientific core is
sound and does not require revision.** Six independent numerical re-derivations across this
project's history (five during the E3 checkpoint, one more in this audit's Part G) unanimously
confirm every headline statistic; zero forbidden claims, zero novelty-inflation violations, and zero
instances of production data functioning as experimental evidence were found across two independent
sweeps; the 6a/6b distinction is never merged; H1's PARTIALLY_SUPPORTED status is preserved without
drift in every location checked; Formulation #2 is intact; and Experiment 1's evidentiary core is
fully reproducible from public code and named, verified-to-exist files.

Against that, this audit found concrete, narrow issues that should be fixed before this checkpoint
would be recommended GREEN:

### Required changes (block GREEN)

1. **(F3)** `manuscript/main.tex` line 600 (§4.2, "Synthetic Generator"): add the standard
   confidentiality/reproducibility qualifier to the cross-company-alignment sentence ("0.695, the
   production-observed value"), matching the pattern every other production-sourced figure in the
   manuscript already carries at its point of use.
2. **(F4)** `manuscript/main.tex` lines ~101–103 (§1.1, "Real-world motivation"): revise "the same
   rule selected a retrieval-based mechanism instead" to name the actual decision-procedure output
   (`EMBEDDING_PRIMARY`) and explicitly distinguish it from Experiment 1's lexical-similarity
   "retrieval" mechanism, consistent with the discipline §3.4 already establishes. This is directly
   relevant to Part K, Objection 5 — closing it removes the one place a reader could conflate the
   motivating case study's untested outcome with Experiment 1's actually-tested mechanism.

Both are narrow, targeted prose edits — no architecture change, no new evidence, no new citation, no
revisiting of any locked number or the contribution formulation itself.

### Recommended, non-blocking (do not require a re-audit to apply; author's discretion)

3. **(F1, F2, F6)** — see `research/E4_ARTIFACT_AUDIT.md` for full detail: tighten the Dawid–Skene
   equivalence sentence's precision (F1); consider a one-clause gloss on the mean-ceiling-vs.-
   individual-seed-max distinction where realized ADS's range is first stated (F2); and, as a
   contract-maintenance item outside this manuscript's own edit scope, correct the stale 84.1%
   figure still present in `PAPER_CONTRACT.md` §2 row 9 and `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §1
   (F6 — the manuscript itself never inherited this stale number, but the governing contract
   document should be corrected so future drafting sessions don't).
4. **(Part J)** Consider consolidating the most granular subsection runs (Introduction's 9,
   Experimental Design's 14, Limitations' 10) into fewer, denser subsections or flowing paragraphs —
   a structural inheritance from the E2 skeleton's per-idea draftnote scaffolding that was never
   re-flowed once real prose replaced the draftnotes. Purely a readability/polish matter, not a
   scientific-defensibility one.
5. **(Part K, Objection 1)** Consider one or two sentences in §6.5/§6.7 explicitly anticipating the
   "isn't retrieval's noise-robustness expected by construction" objection, to preempt rather than
   only implicitly address it.
6. **(Part H)** Execute `manuscript/figures/generate_figures.py` and replace the four `TODO`
   placeholder figure boxes with real, rendered charts once an environment with `matplotlib`
   available is accessible — permitted to remain placeholders at E3 per `PAPER_CONTRACT.md` §11, but
   worth resolving before a venue-facing or arXiv-facing pass.

### Explicitly not required

No re-derivation of any statistic, no new experiment, no new dataset, no literature search, no
rewriting of the locked contribution, and no change to H1's PARTIALLY_SUPPORTED verdict or to
Formulation #2. This E4 pass found no evidentiary or research-integrity problem — only two narrow
prose-precision gaps and a set of optional structural/polish recommendations.

**If the two required changes (F3, F4) are applied, this document's independent judgment is that
the resulting draft would be ready for E5.** No further recomputation, re-verification of statistics,
or re-audit of the evidence base would be needed to reach that determination — both required fixes
are prose-only and outside the load-bearing scientific content this audit spent most of its effort
verifying.

---

## Summary of source documents

- This document (`research/E4_SCIENTIFIC_AUDIT.md`) — primary E4 deliverable, Parts A/C/D/H/J/K/L.
- `research/E4_ARTIFACT_AUDIT.md` — independent `research-code-auditor` deliverable, Parts B/E/F/G/I
  in full detail, including the complete 27-row claim table and all six findings (F1–F6).

Neither document was staged, committed, or pushed. `manuscript/main.tex`, `manuscript/references.bib`,
`research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, and all Phase A–D frozen artifacts
were read only, never modified.

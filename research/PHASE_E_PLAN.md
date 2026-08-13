# Phase E Plan — Manuscript Architecture, Reproducibility, Figures, Workflow, Milestones

> Optional Phase E planning document (Tasks 3, 6-9 of the Phase E kickoff brief). No prose is
> drafted here — this is structure, not content. Does not modify `TECHNICAL_REPORT.md`, `README.md`,
> `METHODOLOGY.md`, or any frozen evidence. Everything below is designed to converge on the locked
> contribution in `research/CONTRIBUTION_LOCK.md` §6/§11 — that document, not this one, is the source
> of truth for what the paper is allowed to claim.

---

## Task 3 — Manuscript structure

### 3.1 Title direction(s)

Evidence-first, not case-study-first, per the brief's requirement. Candidates:

1. *"Historical Consistency Predicts Classifier Accuracy, Not Classifier Ranking: A Controlled Study
   of Design-Time Mechanism Selection"* — leads with the actual finding (§6b of
   `CONTRIBUTION_LOCK.md`), safest and most defensible.
2. *"When Does Historical Label Consistency Select the Right Classification Mechanism? A Negative
   Result Under Lexical Noise"* — question-first, matches STATE.md's settled "question-first, not
   claim-first" pitch decision.
3. *"Rules Before Models, Except When They Aren't: Determinism, Representation Stability, and
   Mechanism Selection in Classification Pipelines"* — keeps a link to `TECHNICAL_REPORT.md`'s
   existing title ("Rules Before Models") for continuity across the two documents, while flagging the
   qualifier up front.

**Recommendation: #1 for the arXiv title, #2 as a strong alternate.** Reject any title implying
"validated method" or "novel metric" (both rejected claims, `CONTRIBUTION_LOCK.md` §7).

### 3.2 Abstract information requirements

Must state, in order, per the locked pitch (`CONTRIBUTION_LOCK.md` §11):

1. The research question (A).
2. The method: pre-registered 240-condition synthetic factorial experiment (n conditions, 2
   mechanisms, 2 lexical conditions, ADS range).
3. The result, both halves, not collapsed (B/C — accuracy-prediction holds, ranking-prediction
   fails, mechanism named: representation-stability blindness).
4. The one qualifying limitation sentence (D): single generator, single perturbation model, one
   motivating (non-evidentiary) case study.
5. Must **not** contain: "novel metric," "validates," "enterprise AI," any unqualified "ADS selects
   the right architecture" phrasing (`CONTRIBUTION_LOCK.md` §7's rejected-claims list — the Abstract
   is the highest-leverage place for one of these to slip back in, so it gets its own explicit check
   at Phase E4).

### 3.3 Section hierarchy

```
Title / Abstract
1. Introduction
2. Related Work
3. Problem Setting and Research Question
4. Experimental Design
   4.1 Generator and factorial design
   4.2 Mechanisms compared
   4.3 Lexical perturbation model
   4.4 Pre-registered hypothesis and falsification criteria
5. Results
   5.1 Headline agreement result
   5.2 ADS predicts mechanism accuracy (6a)
   5.3 ADS does not predict mechanism ranking (6b)
   5.4 Mechanistic explanation (why: ADS's blindness to surface form)
6. Discussion
   6.1 Synthesis (what survives, framed exactly as CONTRIBUTION_LOCK §6's synthesis sentence)
   6.2 Relation to algorithm-selection / meta-learning literature
   6.3 Motivating case study (production R3 flip) — contextual, not evidentiary
7. Limitations
8. Future Work
9. Conclusion
References
Appendix / Supplementary (Task 3.10)
```

Deliberately **not** structured as "Phase 1 engineering → Phase 2 engineering → then research" —
that would be the internship/project-history framing the brief explicitly forbids. The production
system appears only in §6.3 (Discussion, as motivating context) and briefly in §1 (Introduction, as
the origin of the research question) — never as an evaluation section.

### 3.4-3.6 Purpose, allowed claims, and evidence per section

| Section | Purpose | Claims allowed | Evidence/artifacts |
|---|---|---|---|
| 1. Introduction | Motivate the research question from the production observation (the "R3 flip") without presenting it as evidence. State the four preconditions (repeated decisions, observable labels, measurable consistency, sufficient coverage) and explicit out-of-scope list. | The R3 flip is a *motivating observation*, cited not proven. Research question exactly as `CONTRIBUTION_LOCK.md` §11.A. | `METHODOLOGY.md` real-vs-synthetic table (R3 row); `STATE.md` "Literature review + paper-positioning conclusions" |
| 2. Related Work | Position against Rice 1976 / meta-learning / AutoML-workflow-composition / self-designed data systems / reject-option-selective-classification lineages. State what's *not* anticipated (C2b's narrow gap). | Positioning claims only — never "no prior work exists," always "the closest work does X, differs by Y." | `research/literature/citation_ledger.csv` (VERIFIED rows only — exclude NOT FOUND / UNVERIFIED entries or mark them explicitly as such if cited), `prior_art_map.md`, `contribution_status.md` |
| 3. Problem Setting | Define ADS formally (the metric itself, not claimed novel). State H1 exactly as pre-registered. | ADS definition (descriptive, not a novelty claim — pair with an explicit "mathematically equivalent to cluster purity/majority-vote agreement, see Related Work" sentence so C1's rejection is visible in the paper itself, not just in internal docs). | `TECHNICAL_REPORT.md` §2.2 (formula), `EXPERIMENT_1_REDESIGN_REVIEW.md` §2 (H1) |
| 4. Experimental Design | Full method transparency: generator, mechanisms, perturbation model, pre-registration, falsification table. | Design description only — no results yet. | `EXPERIMENT_1_REDESIGN_REVIEW.md`, `EXPERIMENT_1_CALIBRATION_REPORT.md`, `EXPERIMENT_1_DATA_DICTIONARY.md` |
| 5. Results | Report both halves of §4's distinction (accuracy vs. ranking) without merging them. Report the exceptionless 120/120 + 120/120 pattern and the banded 32/32 vs. 0/18 split. | Only what's in `CONTRIBUTION_LOCK.md` §4/§6a/§6b, with the same numbers, same CIs, same p-value. | `final_condition_results.csv`, `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4-6, `AUDIT_REPORT.md` (independent re-derivation) |
| 6. Discussion | Synthesize; relate back to literature; introduce the case study as context. | Exactly `CONTRIBUTION_LOCK.md` §6's synthesis sentence — no stronger. | `CONTRIBUTION_LOCK.md` §6, §11 |
| 7. Limitations | Every item in `CONTRIBUTION_LOCK.md` §9, undiluted. | Negative/boundary statements only. | `CONTRIBUTION_LOCK.md` §9 |
| 8. Future Work | Named, not built. | Explicitly hedge every item as "not built, not tested here." | `CONTRIBUTION_LOCK.md` §10 |
| 9. Conclusion | One paragraph, restates §11's B/C exactly. | No new claims introduced here — a common place for scope creep to sneak in during drafting; flag at Phase E4. | `CONTRIBUTION_LOCK.md` §11 |

### 3.7 Figures required

See Task 7 below (kept in one place to avoid duplication).

### 3.8 Tables required

See Task 7 below.

### 3.9 Equations required

Exactly one: the ADS formula (`CONTRIBUTION_LOCK.md`/`TECHNICAL_REPORT.md` §2.2,
$\text{ADS}(p) = \max_i c_i / \sum_i c_i$). Optionally a second, short equation for the paired-
bootstrap δ-margin decision rule (empirical winner definition) if Reviewers would otherwise have to
infer it from prose — worth drafting once §4 text exists, not decided now.

### 3.10 Supplementary material candidates

- Full 240-row `final_condition_results.csv` (or a link to the public repo path — see
  `PUBLIC_RELEASE_BOUNDARY.md` for what's public already).
- `EXPERIMENT_1_DATA_DICTIONARY.md` (column definitions) — useful as a supplementary appendix so the
  main text isn't burdened with column-level detail.
- The full pre-registration/falsification table (`EXPERIMENT_1_REDESIGN_REVIEW.md` §18) as an
  appendix table, since pre-registration transparency is a strength worth showing in full, not just
  summarizing.
- Full citation ledger as supplementary (the paper's Related Work section only needs the
  VERIFIED/high-relevance subset in-line).

---

## Task 6 — Public reproducibility strategy

| Tier | What | Reproducible by a stranger? |
|---|---|---|
| **1. Fully reproducible** | The Experiment 1 generator, mechanisms, perturbation model, and analysis scripts (`scripts/experiments/exp1/*`), run end-to-end offline, no keys, no cost. Produces the exact 240-condition table the paper's Results section reports (same seed). This is the paper's *primary* evidence tier and should be stated as such explicitly in the paper's Reproducibility section. | Yes, exactly. |
| **2. Reproducible using synthetic/public data** | The Phase 1/2 synthetic pipeline (`METHODOLOGY.md`'s reproduction path) — different generator, different (motivating, not evidentiary) numbers, same qualitative shape. Useful context, not the paper's statistical evidence. | Yes, qualitatively (different seed → different exact figures, same shape, per `METHODOLOGY.md`'s own caveat). |
| **3. Case-study-only / confidential** | The production R3-flip observation, the 91.2%/0.847/0.964 production ADS figures, the 10-receipt OCR trace. Cited, never re-computable by a reader. | No — and the paper must say so explicitly every time these numbers appear (already the pattern in `TECHNICAL_REPORT.md` §3.1/§3.2; carry it forward). |
| **4. Not reproducible** | Nothing currently in the locked contribution falls here — flagged as an empty category deliberately, so a future draft that adds an unreproducible claim has to justify why it's not in tier 1-3. | N/A |

**Rule for the manuscript's Reproducibility section (carried from `TECHNICAL_REPORT.md`'s existing
pattern, do not weaken it):** never state or imply that confidential production data or the case
study is independently reproducible. Every table that mixes production and synthetic numbers (like
`METHODOLOGY.md`'s comparison table) must visually/textually separate "cited" from "computed here."

---

## Task 7 — Figure/table plan

Evaluated against the brief's candidate list; only recommending what earns its place in the
evidence-first narrative (Task 3's structure), not decorative or engineering-history figures.

| # | Candidate | Recommend? | Why / why not | Section |
|---|---|---|---|---|
| F1 | Experiment design diagram (factorial: 2 mechanisms × 2 lexical conditions × ADS sweep, pre-registration → falsification-table flow) | **Yes** | Readers need the design before the result; this is the paper's methodological backbone, not decoration. | §4 |
| F2 | ADS vs. mechanism accuracy scatter/regression (rules and retrieval, both lexical conditions) | **Yes** | Directly visualizes §6a's r≈0.91-0.96 correlations — the positive half of the finding needs a figure, not just a number. | §5.2 |
| F3 | Realized-ADS-band × R3-agreement bar chart (32/32 vs. 0/18, CLEAN vs. VARIED) | **Yes** | This *is* the paper's headline finding; a single reviewer-legible figure beats several tables. | §5.1/§5.3 |
| F4 | Mechanism-ranking-vs-lexical-condition figure (empirical winner constant at 120/120 and 120/120) | **Yes** | Visualizes the exceptionless winner-constancy claim that grounds §6b's causal account — the second most important figure after F3. | §5.3-5.4 |
| F5 | Production-vs-synthetic ADS/decision comparison (the "R3 flip" table from `METHODOLOGY.md`) | **Conditional — table, not figure** | Belongs in §1/§6.3 as *context*, not as evidence; a small table suffices, a figure would visually overweight a non-evidentiary data point next to F2-F4. | §1, §6.3 |
| F6 | Evidence-to-mechanism pipeline / conceptual framework diagram (ADS → decision rule → mechanism) | **Conditional** | Useful for readers unfamiliar with the cascade concept, but risks re-introducing the *general* C2/C3 architecture claims (already CHALLENGED, `CONTRIBUTION_LOCK.md` §3) as if they were this paper's subject. If included, must be captioned to scope it to "the specific rule tested here," not the shipped production cascade. | §3, if included |
| F7 | "Research architecture" / project-history diagram (Phase 1 → Phase 2 → Experiment 1 → D.1) | **No** | This is exactly the internship/project-history framing the brief prohibits. Belongs in `STATE.md`/internal docs, not the paper. | — |
| F8 | Mechanism winner behavior detail (accuracy-gap-vs-ADS lines, from `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5's table) | **Yes, as a table, optionally a figure** | The rules−retrieval gap *widening* with ADS under VARIED is a specific, citable pattern worth showing precisely; a table (as already drafted in `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5) may communicate the exact numbers better than a figure — decide once drafting §5 makes clear which reads better. | §5.3 |

**Minimum set for the first complete draft (Task 9's E3 milestone): F1, F2, F3, F4, plus the F5/F8
tables.** F6/F7 deferred — F6 only if drafting §3 shows readers need it, F7 never.

---

## Task 8 — Manuscript workflow

Recommended repository structure (not created yet, per the brief's file-allowlist — this is the plan
for Phase E2):

```
manuscript/
├── main.tex              # article class, \input{} each section
├── references.bib        # compiled from research/literature/citation_ledger.csv (Phase B verified rows)
├── sections/
│   ├── 01_introduction.tex
│   ├── 02_related_work.tex
│   ├── 03_problem_setting.tex
│   ├── 04_experimental_design.tex
│   ├── 05_results.tex
│   ├── 06_discussion.tex
│   ├── 07_limitations.tex
│   ├── 08_future_work.tex
│   └── 09_conclusion.tex
├── figures/               # F1-F4 (+F8 if figure, not table) as vector PDF, generated by one script
│   └── generate_figures.py    # stdlib+matplotlib, reads committed CSVs only, no new experiments
└── tables/                 # optional: .tex table fragments \input{} into sections, if tables get long
```

- **LaTeX engine:** pdfLaTeX (per §2.3 of `MANUSCRIPT_FORMAT_RESEARCH.md`).
- **Bibliography system:** `natbib` + BibTeX, `.bbl` precompiled and committed alongside `.bib`
  (avoids the Biber/BibTeX version-mismatch failure mode documented in that same file §1.4/§1.6).
- **Figure format:** vector PDF for all plots (`matplotlib` `savefig(..., format="pdf")`); PNG only if
  a raster is unavoidable (none currently expected — all four required figures are scatter/bar plots
  matplotlib renders natively as vector).
- **Equation conventions:** standard `amsmath` (`align`/`equation` environments); numbered equations
  only for the two that are actually referenced by number in prose (ADS formula, and the δ-margin
  rule if it becomes its own display equation per Task 3.9).
- **Citation workflow:** `research/literature/citation_ledger.csv` is the single source of truth
  (already the project's own stated convention, `ROADMAP.md` Phase B); `references.bib` is a
  generated/derived export from the VERIFIED subset of that ledger, regenerated whenever the ledger
  changes rather than hand-edited independently — avoids the ledger and the `.bib` drifting apart.
- **Versioning strategy:** manuscript lives in the same git repo/history as the rest of the research
  artifacts (no separate manuscript repo) — consistent with this project's existing single-repo
  convention (`STATE.md`'s "single committed handoff file" philosophy applied to the manuscript too).
  Tag the commit that produces each milestone's draft (E3, E4, etc.) rather than relying on branch
  names, so "what did the first complete draft look like" stays answerable from git history alone.
- **PDF compilation workflow:** local `pdflatex → bibtex → pdflatex → pdflatex` (standard four-pass
  LaTeX+BibTeX cycle) as the authoritative local build; arXiv's own compile-on-submit step (§1.2 of
  `MANUSCRIPT_FORMAT_RESEARCH.md`) is the final verification, not the primary one — don't discover
  compile errors for the first time at submission.

---

## Task 9 — Phase E milestones

| Milestone | Objective | Deliverables | Stop condition | Explicitly out of scope |
|---|---|---|---|---|
| **E0 — Format & readiness** | Establish format/structure/boundaries before any prose. **This document + its siblings.** | `MANUSCRIPT_FORMAT_RESEARCH.md`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PUBLIC_RELEASE_BOUNDARY.md`, this plan. | Auditor verdict PASS or PASS_WITH_NOTES on all four. | Any prose, any LaTeX file, any figure. |
| **E1 — Manuscript architecture** | Confirm/refine Task 3's structure against author feedback on this document; resolve any open decisions flagged in §3 of `MANUSCRIPT_FORMAT_RESEARCH.md` (endorsement contact, license choice, AI-disclosure wording). | Updated structure (if changed), endorsement contact initiated. | Author has approved the section hierarchy and the three open decisions are resolved or explicitly deferred with an owner. | Drafting section text. |
| **E2 — Skeleton** | Create `manuscript/` per Task 8, with section files containing headers + bullet-point claim outlines (from Task 3.4-3.6's tables) but no full prose. | Empty-but-structured `.tex` tree; `references.bib` generated from the ledger; figure-generation script stubbed against real committed CSVs (can run and produce placeholder-quality F1-F4). | `main.tex` compiles to a PDF with correct section order, real citations resolving, and real (even if unpolished) figures. | Polished prose; final figure styling. |
| **E3 — First complete draft** | **The hard milestone.** Full prose in every section, matching Task 3's claim/evidence table exactly. | Complete, compiling `manuscript/main.tex` → PDF. | Every section has real prose; every claim in it traces to a row in `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`; document compiles cleanly start to finish. | Adversarial audit, citation verification beyond what Phase B already ledger-verified, figure aesthetic polish, public-release re-check. |
| **E4 — Internal scientific audit** | Check the draft against `CONTRIBUTION_LOCK.md` — no claim upgraded, no rejected claim returned, Abstract/Conclusion checked with special care (Task 3.2/3.6's known risk points). | Audit notes (findings + fixes applied). | `research-code-auditor` PASS/PASS_WITH_NOTES on the full draft's claim set. | Re-opening Gate 4's contribution decision itself (frozen; only prose can be fixed, not the underlying finding). |
| **E5 — Adversarial claim/citation audit** | Re-verify every in-text citation against `citation_ledger.csv`'s VERIFIED status; hunt for any claim that reads stronger in prose than in the source table (a common drift when turning tables into sentences). | Citation cross-check log. | Every citation in the PDF is VERIFIED in the ledger (or explicitly flagged as lower-confidence in-text, matching the ledger's own UNVERIFIED-PARTIAL notes); no claim-strength drift found. | New literature search (Phase B is closed per `RESEARCH_GPS.md`'s DO NOT CHASE list). |
| **E6 — Public reproducibility audit** | Confirm the Reproducibility section matches Task 6's tiers exactly; re-run `PUBLIC_RELEASE_BOUNDARY.md`'s repo sweep against the final manuscript + intended arXiv source package. | Reproducibility-audit note; confirmed-clean release-boundary re-check. | Independent (or the auditor's) confirmation that every reproducible claim in the PDF actually reproduces from the committed public scripts, and no confidential content is staged for the arXiv package. | Building new reproducibility tooling beyond what already exists. |
| **E7 — arXiv submission package** | Assemble the actual `.tar`/`.zip` source package per `MANUSCRIPT_FORMAT_RESEARCH.md` §1.4; secure endorsement (§1.14); finalize license/AI-disclosure/ORCID metadata. | Submission-ready archive; endorsement obtained; metadata fields drafted. | Package compiles standalone from a clean extraction; endorsement secured; author has approved final metadata. | Submitting. |
| **E8 — arXiv submission** | Submit; confirm successful announcement and (later) Scholar indexing; cross-link Zenodo/GitHub/ORCID per `ROADMAP.md`'s existing Track A plan. | Live arXiv identifier. | Paper is live on arXiv with correct metadata and no moderation hold. | Any journal-migration work (`ROADMAP.md` Phase I's "later adapt to a journal" — explicitly a separate future phase). |

**Hard milestone: E3 (first complete draft).** Per the brief: formatting perfection must not delay
reaching E3 — E4-E6 exist specifically to catch what E3 doesn't get right the first time, not to be
front-loaded into E2.

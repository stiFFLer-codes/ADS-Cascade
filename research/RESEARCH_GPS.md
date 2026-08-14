# Research GPS

> Not manuscript content. A living pointer to where the research stands, so a session doesn't
> re-derive state or re-open settled questions. Update the "CURRENT LOCATION" / "CURRENT GATE"
> sections at the end of each research (not engineering) session.

## NORTH STAR

Complete a defensible first manuscript draft → prepare reproducible public artifacts → arXiv
preprint. Not an indefinitely expanding research program.

## CURRENT LOCATION

**Phase E5 — Manuscript Refinement: IN PROGRESS (E5.1 complete, E5.2 current).**

The contribution is locked (`research/CONTRIBUTION_LOCK.md`: Formulation #2 **Adopted**, auditor
verdict "Formulation #2 survives adversarial review. Gate 4 is complete."). Phase E has produced a
first complete manuscript draft (`manuscript/main.tex`, E3) that survived an independent adversarial
scientific audit (E4: two required prose corrections applied at E4.1 — a production-data
confidentiality qualifier and an `EMBEDDING_PRIMARY`/`retrieval` terminology fix — both independently
re-verified; checkpoint committed/pushed at `fa55ef6`). H1 remains stated as **PARTIALLY_SUPPORTED**
in the manuscript, not upgraded or fully falsified; the 6a (accuracy-prediction) / 6b
(ranking-prediction) separation is intact.

**E5.1 (readability/structure pass) is complete**, committed/pushed at `83ee5d3`: merged 68
`\subsection`s down to 43 (37% reduction) by combining adjacent, thematically-related subsections
under shared headers, per the E3/E4 audit trail's own finding that excessive segmentation and
repetition was the manuscript's main presentation weakness. No prose was rewritten, no content
deleted, no scientific claim or numerical value changed. One subsection was reordered (H1's
partially-supported verdict now leads Limitations instead of trailing it, matching that section's
own pre-existing design comment). Two pre-existing broken internal `Section~X.Y` cross-references
(predating this session, present since the E4-audited draft — pointers to where R3 and the
mechanistic representation-stability account are actually defined) were found and fixed as a
byproduct of the required renumbering; a third reference was correct in the E4 draft and only needed
updating because this session's own H1 reorder moved its target subsection. Independently audited:
PASS (`research/E5_1_MANUSCRIPT_AUDIT.md`) — 6a/6b
separation intact, no rejected claim reappeared, all protected numbers and citation/label sets
byte-identical, H1 still PARTIALLY_SUPPORTED, test suite 30/30.

**E5.2 (citation + claim audit) is the current active gate — audit phase complete, correction
pass pending.** All 14 citation keys were independently re-verified against `citation_ledger.csv`
(and the two literature gap-verification CSVs) by both a primary pass
(`research/E5_2_CITATION_CLAIM_AUDIT.md`) and an independent `research-code-auditor` pass
(`research/E5_2_INDEPENDENT_CITATION_AUDIT.md`, verdict 🟠 ORANGE/CONDITIONAL). Finding: 14/14
citations FULLY_SUPPORTED, no claim-strength drift, novelty guardrail intact, contribution-lock
compliance PASS on all 7 checks — but three VERIFIED-INDUSTRY ledger sources (B8-04/05/06) are used
substantively in §2.4 prose without a formal `\citep{}`/`references.bib` entry, flagged as the audit's
one required (bounded, ledger-only, no new search) fix. No manuscript edit has been made yet — the
bounded E5.2 correction pass is pending human review of the audit findings. No new experiment is
being run; no frozen evidence is being touched.

### Locked E5+ sequence (author-specified, authoritative — supersedes `PHASE_E_PLAN.md` Task 9's
### original E5/E6 milestone labels, which used "E5" for what is now E5.2)

```
E5.0 GPS/status hygiene              — done (commit 4d031ab)
E5.1 Readability / structure         — done (commit 83ee5d3)
E5.2 Citation / claim audit          — CURRENT (audit done, ORANGE, fix pending)
E5.3 Public reproducibility audit    — next
E5.4 Generate real figures
E5.5 Final prose polish
E6   Final adversarial review
E7   Public release package
     → arXiv-ready → publication
```

**Governing rule from E5 onward ("do no harm" phase):** every proposed change must answer "does
this improve clarity/reproducibility without changing the scientific meaning?" If yes, consider it.
If it would change the experiment, frozen evidence, the contribution, hypothesis status, numerical
results, or statistical interpretation, STOP and open a new scientific decision gate instead of
making the change inline. No incidental "while we're here" edits beyond each checkpoint's declared
scope.

## COMPLETED

- Phase A — Evidence & reproducibility audit
- Phase B — Literature verification
- Phase C — Contribution stress test
- Experiment 1 design, pilot, calibration, 240-condition final run, evidence freeze
- Phase D.1 — Post-hoc analysis & interpretation of Experiment 1
- **Phase D — Contribution lock** (Formulation #2 adopted, Gate 4 complete)
- **Phase E0 — Manuscript format/structure/boundary planning** (`MANUSCRIPT_FORMAT_RESEARCH.md`,
  `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PUBLIC_RELEASE_BOUNDARY.md`, `PHASE_E_PLAN.md`)
- **Phase E1 — Manuscript architecture** (`MANUSCRIPT_ARCHITECTURE.md`, audited)
- **Phase E2 — Manuscript skeleton** (`manuscript/` tree established)
- **Phase E3 — First complete manuscript draft** (full prose, all sections, `manuscript/main.tex`)
- **Phase E4 — Adversarial scientific manuscript audit + E4.1 corrections + release hygiene
  checkpoint** (committed/pushed at `fa55ef6`)
- **Phase E5.0 — GPS/status hygiene checkpoint** (committed/pushed at `4d031ab`)
- **Phase E5.1 — Readability/structure pass** (68→43 subsections, auditor PASS, committed/pushed
  at `83ee5d3`)

## CURRENT GATE

**E5.2 — Citation + Claim Audit.** Audit phase complete (see CURRENT LOCATION above for the full
finding); what remains is a bounded correction pass — adding `references.bib` entries and in-text
`\citep{}` citations for B8-04/B8-05/B8-06 (Ken From Finance, Peakflo, Ramp; all already
VERIFIED-INDUSTRY in `citation_ledger.csv`, no new search required), each carrying the required
not-peer-reviewed label per `PAPER_CONTRACT.md` §2 row 11 — then a re-audit, then human approval
before commit. Two bibliography metadata TODOs (`dawidskene1979`, `rankgpt2023`) remain optionally
open, not blocking. Same workflow as E5.0/E5.1: bounded change → test/structural check → auditor →
fix verified findings → re-audit → stage → commit only with explicit approval.

## NEXT GATE

**E5.3 — Public Reproducibility Audit.** Confirm the Reproducibility Statement matches the tiered
reproducibility claims in `PHASE_E_PLAN.md` Task 6 exactly (Tier 1: Experiment 1 code, fully
reproducible; Tier 2: synthetic Phase 1/2 pipeline, reproducible with different exact numbers; Tier
3: production case study, cited only, never reproducible); re-run the release-boundary sweep
(`research/PUBLIC_RELEASE_BOUNDARY.md`) against the current manuscript and the files that would ship
in an arXiv source package. After that: E5.4 (generate the real F1-F4 figures + F5/F8 tables via
`manuscript/figures/generate_figures.py`, currently placeholder-only), E5.5 (final prose polish),
E6 (final adversarial review of the whole manuscript end-to-end), E7 (public release package —
endorsement, license, AI-disclosure, ORCID metadata, arXiv source tarball), then arXiv submission.

## RESEARCH COMPLETION SCORECARD

**Gate 1 — Evidence:** ✅ production evidence audited · ✅ synthetic pipeline reproducible ·
✅ final experiment reproducible · ✅ raw results frozen

**Gate 2 — Literature:** ✅ broad prior-art search · ✅ ADS prior art identified ·
✅ contribution claims stress-tested · ✅ terminology corrected

**Gate 3 — Experimental validation:** ✅ hypothesis formalized · ✅ experiment preregistered
internally · ✅ calibration completed · ✅ 20-seed × 6-region × 2-condition experiment completed ·
✅ results frozen · ✅ interpretation completed (Phase D.1)

**Gate 4 — Contribution:** ✅ surviving claim formally adopted (Formulation #2,
`CONTRIBUTION_LOCK.md` §6) · ✅ unsupported claims formally removed (§7 rejected-claims list) ·
✅ scope/domain explicitly bounded in manuscript · ✅ limitations documented in manuscript ·
✅ contribution statement locked — **Adopted**, auditor-verified PASS

**Gate 5 — Manuscript:** ✅ Introduction · ✅ Related Work · ✅ Problem Setting · ✅ Experimental
Design · ✅ Results · ✅ Discussion · ✅ Limitations · ✅ Future Work · ✅ Conclusion · ✅ References ·
✅ readability/structure pass (E5.1, 68→43 subsections, auditor PASS) · ⬜ citation/claim audit
(E5.2, current) · ⬜ public-reproducibility audit (E5.3) · ⬜ Figures/tables (E5.4, deferred) ·
⬜ final prose polish (E5.5)

**Gate 6 — Public release:** ⬜ public synthetic reproduction · ⬜ code cleanup ·
⬜ reproducibility instructions · ⬜ no client/confidential information · ⬜ final technical audit ·
⬜ arXiv submission

## DO NOT CHASE

Per the project's stopping rule: only investigate something new if it can change (1) the research
question, (2) the surviving contribution, (3) the validity of Experiment 1, or (4) the paper's
central conclusion. If it cannot affect one of those four, it goes here, not into active work.

- Unnecessary new experiments (Experiment 1 is closed; §14 of the post-hoc analysis found no
  residual uncertainty a new run would resolve)
- Endless novelty searches (Phase B/C already settled the novelty framing — Rice's Algorithm
  Selection Problem / meta-learning, design-time workflow composition)
- Vendor/model experimentation (LLM mechanism, alternative retrieval libraries, etc. — explicitly
  out of scope for H1 as reworded)
- Manuscript polishing before the contribution is formally locked (Gate 4)
- An ADS-and-lexical-noise-conditioned R3 variant (`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §15) — a
  legitimate future-work idea, not a gap in the current evidence; do not build it now
- Re-tuning R3's thresholds (0.90/0.70), δ (0.02), or the retrieval cutoff (75) against the
  post-hoc findings — all three are frozen per Gate 3 and were deliberately not re-derived here
- During E5.2 specifically: figure generation (E5.4), reproducibility-sweep work (E5.3), abstract
  optimization or final publication polish (E5.5+), or arXiv submission-package prep (E7) — each is
  a separate later checkpoint per the locked E5+ sequence above, not part of the citation/claim audit
- Any edit whose only justification is "while we're here" rather than the current checkpoint's
  declared scope — the E5+ governing rule (see CURRENT LOCATION) requires stopping and opening a new
  scientific decision gate for anything that would touch the experiment, frozen evidence, the
  contribution, hypothesis status, numerical results, or statistical interpretation

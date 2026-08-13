# Research GPS

> Not manuscript content. A living pointer to where the research stands, so a session doesn't
> re-derive state or re-open settled questions. Update the "CURRENT LOCATION" / "CURRENT GATE"
> sections at the end of each research (not engineering) session.

## NORTH STAR

Complete a defensible first manuscript draft → prepare reproducible public artifacts → arXiv
preprint. Not an indefinitely expanding research program.

## CURRENT LOCATION

**Phase E5 — Manuscript refinement: IN PROGRESS.**

The contribution is locked (`research/CONTRIBUTION_LOCK.md`: Formulation #2 **Adopted**, auditor
verdict "Formulation #2 survives adversarial review. Gate 4 is complete."). Phase E has produced a
first complete manuscript draft (`manuscript/main.tex`, E3) that survived an independent adversarial
scientific audit (E4: two required prose corrections applied at E4.1 — a production-data
confidentiality qualifier and an `EMBEDDING_PRIMARY`/`retrieval` terminology fix — both independently
re-verified). The E4 checkpoint (commit `fa55ef6`) is committed and pushed; it also closed a
provenance/hygiene pass over the accumulated E0-E4.1 audit trail (no local paths, credentials, or
confidential material in any committed file). H1 remains stated as **PARTIALLY_SUPPORTED** in the
manuscript, not upgraded or fully falsified; the 6a (accuracy-prediction) / 6b (ranking-prediction)
separation is intact.

Current manuscript state: 9 numbered `\section`s (Introduction through Conclusion, plus an
unnumbered Reproducibility Statement) and 68 `\subsection`s, complete prose in every section,
scientifically sound per E4 but over-fragmented — the E3/E4 audit trail flagged excessive
subsection segmentation and repetition as the manuscript's main presentation weakness. **E5.1
(bounded readability/structure pass — merge fragmented subsections, cut repetition, improve
section-to-section transitions, no content/claim/number changes) is the active work.** No new
experiment is being run; no frozen evidence is being touched.

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

## CURRENT GATE

**Gate 5 — Manuscript, readability sub-gate.** All nine manuscript sections have real prose and
passed the E4 scientific audit (claim/evidence integrity, no rejected claims, numbers correct). What
remains before Gate 5 closes is a structural/readability pass (E5.1) — reducing subsection
fragmentation and repetition without altering scientific content — followed by the citation and
reproducibility audits already planned for Phase E (see `PHASE_E_PLAN.md` Task 9's E5/E6 milestones,
renumbered below under this project's actual E5 = readability, not that document's original
"adversarial claim/citation audit" label — see note).

> **Note on milestone naming:** `PHASE_E_PLAN.md`'s Task 9 table used "E5" for an
> adversarial claim/citation audit. The session that is actually running now (this repo's current
> "Phase E5") is a manuscript **readability/structure** pass instead, per direct author instruction.
> The citation/reproducibility audits `PHASE_E_PLAN.md` called E5/E6 still need to happen — they are
> just sequenced after this readability pass, not before it. Treat `PHASE_E_PLAN.md`'s milestone
> letters as the original plan, and this file's CURRENT LOCATION as the authoritative live state.

## NEXT GATE

After E5.1 (readability/structure pass) closes: an adversarial claim/citation audit (re-verify every
in-text citation against `citation_ledger.csv`'s VERIFIED status; hunt for claim-strength drift), then
a public-reproducibility audit (confirm the Reproducibility section matches the tiered claims in
`PHASE_E_PLAN.md` Task 6, re-run the release-boundary sweep against the final manuscript + intended
arXiv source package), then figure generation (`manuscript/figures/generate_figures.py`, F1-F4 +
F5/F8 tables — deferred, not started), then arXiv submission-package assembly (endorsement, license,
AI-disclosure, ORCID metadata) and submission itself.

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
⬜ Figures/tables (deferred to a later Phase E checkpoint, not E5.1) · ⬜ readability/structure pass
(E5.1, in progress) · ⬜ adversarial claim/citation audit · ⬜ public-reproducibility audit

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
- During E5.1 specifically: figure generation, citation expansion, abstract optimization, final
  publication polish, or arXiv submission-package prep — each is a separate later checkpoint, not
  part of the bounded readability/structure pass

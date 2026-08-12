# Research GPS

> Not manuscript content. A living pointer to where the research stands, so a session doesn't
> re-derive state or re-open settled questions. Update the "CURRENT LOCATION" / "CURRENT GATE"
> sections at the end of each research (not engineering) session.

## NORTH STAR

Complete a defensible first manuscript draft → prepare reproducible public artifacts → arXiv
preprint. Not an indefinitely expanding research program.

## CURRENT LOCATION

**Phase D.1 — Post-hoc analysis of Experiment 1: COMPLETE.**

`research/EXPERIMENT_1_POSTHOC_ANALYSIS.md` + `research/EXPERIMENT_1_DATA_DICTIONARY.md` fully
explain the observed reversal (100% agreement at ADS 0.70–0.90, 10% at ADS ≥0.90) from the frozen
240-condition data: the empirical winner is a constant function of the lexical/noise condition
alone (retrieval wins 120/120 VARIED conditions, ties 120/120 CLEAN conditions), unconditional on
ADS across its full observed range. R3's agreement rate is mechanical — it equals the fraction of
conditions where R3's ADS-threshold output happens to be `retrieval`. This is a fully traced,
deterministically-reproducible mechanism (verified seed-by-seed), not an unresolved pattern.
Decision: **no further experiment needed** (Gate 3 is closed; see scorecard below).

## COMPLETED

- Phase A — Evidence & reproducibility audit
- Phase B — Literature verification
- Phase C — Contribution stress test
- Experiment 1 design, pilot, calibration, 240-condition final run, evidence freeze
- **Phase D.1 — Post-hoc analysis & interpretation of Experiment 1**

## CURRENT GATE

**Contribution lock.** Phase D.1 produced the evidence (`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §12-13:
minimum defensible claim + claims that must not be made). What remains before Phase E can start is
a human decision to formally adopt that claim (or a narrower version of it) as the paper's locked
contribution statement — not new analysis.

## NEXT GATE

Phase E — Manuscript drafting (Introduction, Related Work, Methodology, Experimental Setup,
Results, Discussion, Limitations, Conclusion, References, Figures/tables), built on the locked
contribution.

## RESEARCH COMPLETION SCORECARD

**Gate 1 — Evidence:** ✅ production evidence audited · ✅ synthetic pipeline reproducible ·
✅ final experiment reproducible · ✅ raw results frozen

**Gate 2 — Literature:** ✅ broad prior-art search · ✅ ADS prior art identified ·
✅ contribution claims stress-tested · ✅ terminology corrected

**Gate 3 — Experimental validation:** ✅ hypothesis formalized · ✅ experiment preregistered
internally · ✅ calibration completed · ✅ 20-seed × 6-region × 2-condition experiment completed ·
✅ results frozen · ✅ interpretation completed (Phase D.1)

**Gate 4 — Contribution:** ⬜ surviving claim formally adopted (draft exists,
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §12) · ⬜ unsupported claims formally removed (draft exists, §13)
· ⬜ scope/domain explicitly bounded in manuscript · ⬜ limitations documented in manuscript ·
⬜ contribution statement locked

**Gate 5 — Manuscript:** ⬜ Introduction · ⬜ Related Work · ⬜ Methodology · ⬜ Experimental Setup
· ⬜ Results · ⬜ Discussion · ⬜ Limitations · ⬜ Conclusion · ⬜ References · ⬜ Figures/tables

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

# Audit Report — Phase E1 (Manuscript Architecture)

> Independent verification of `research/MANUSCRIPT_ARCHITECTURE.md` against `research/PAPER_CONTRACT.md`
> (the binding anti-drift contract) and `research/CONTRIBUTION_LOCK.md` (Formulation #2, the locked
> contribution). This is a planning-document review — no manuscript prose, `.tex` file, figure, or
> bibliography exists yet, so no code review or experimental-integrity review applies. This report is
> written only to `research/MANUSCRIPT_ARCHITECTURE_AUDIT.md`. `research/AUDIT_REPORT.md` (the frozen
> Gate 4 artifact), `research/PAPER_CONTRACT_AUDIT_REPORT.md`, and `research/E0_CHECKPOINT_AUDIT.md`
> were read for context only and were not written to. No file was edited, staged, or committed by this
> pass.

---

## 1. Repository state

Branch `main`, HEAD `eaaa139` ("Phase E.0: establish manuscript paper contract"), working tree
otherwise clean per `git status` except for untracked files (see §10). Diffed/read directly rather than
trusted: `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`, `RESEARCH_GPS.md`, `EVIDENCE_BASELINE.md`,
`EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `EXPERIMENT_1_REDESIGN_REVIEW.md` (§18 excerpt),
`data/outputs/experiments/exp1/posthoc/posthoc_analysis_report.json`,
`data/outputs/experiments/exp1/final/final_condition_results.csv` (row count / freeze-diff check only),
`PHASE_E_PLAN.md`, `PUBLIC_RELEASE_BOUNDARY.md`, `MANUSCRIPT_FORMAT_RESEARCH.md`,
`E0_CHECKPOINT_AUDIT.md`, `PHASE_E_AUDIT_REPORT.md`, and the full text of `MANUSCRIPT_ARCHITECTURE.md`
itself (423 lines, read in full).

By mtime, `MANUSCRIPT_ARCHITECTURE.md` (17:09:33) is the only file newer than the last commit's
newest file (`PAPER_CONTRACT_AUDIT_REPORT.md`, 15:30:26) other than `E0_CHECKPOINT_AUDIT.md`
(16:19:26), which predates the commit and is leftover Phase-E0 process documentation, not part of this
pass. `find . -newer research/PAPER_CONTRACT_AUDIT_REPORT.md` returns exactly those two files. No
`manuscript/` directory and no `.tex` file exist anywhere in the tree.

## 2. Current research GPS

`RESEARCH_GPS.md` still shows Gate 4 as open (unchecked boxes) even though `CONTRIBUTION_LOCK.md`
(committed) records Gate 4 as Adopted/PASS and Phase E as unblocked. This staleness is pre-existing,
already flagged twice before this pass (`PAPER_CONTRACT.md` §4, `PHASE_E_AUDIT_REPORT.md` finding 1),
not introduced or worsened by `MANUSCRIPT_ARCHITECTURE.md`. North-star distance: on track —
Phase E1 (manuscript architecture, no prose) is exactly the next step the locked contribution and
`PHASE_E_PLAN.md`'s Task 9 milestone table call for.

## 3. Changed files

- **Docs (planning only):** `research/MANUSCRIPT_ARCHITECTURE.md` — the only file created by this
  pass, confirmed by mtime sweep (§1).
- **Code:** none changed.
- **Experimental artifacts:** none changed — `git diff 6fb6188 HEAD -- data/outputs/experiments/exp1/final/`
  is empty, `git status --porcelain` on that path is empty, row count is 241 (240 data rows + header),
  matching the documented 240-condition design.
- **Manuscript:** none — no `manuscript/` directory, `.tex` file, figure, or bibliography exists
  anywhere in the tree.
- **Other:** none. (Six other untracked `research/*.md` files exist in the working tree but predate
  this pass — see §10.)

## 4. Research integrity

No new quantitative claim is introduced. Grepped `MANUSCRIPT_ARCHITECTURE.md` directly for the
`CONTRIBUTION_LOCK.md` §7 / `PAPER_CONTRACT.md` §3 rejected-claim phrases (`novel metric`,
`validates R3`, `universally`, `enterprise AI broadly`, `no vendor`/`no comparable vendor`,
`consistency alone is sufficient`, `selects the right/correct architecture`, `higher ADS means...`).
Every match occurs strictly inside a "Claims that must NOT appear" column, a "Forbidden title
patterns" line, or a correctly-negated sentence ("that no vendor measures before choosing (industry
sources directly contradict that framing)") — never asserted as the document's own position. No
rejected claim from the known list (ADS-as-novel-metric, general design-time-selection novelty, the
combined-system novelty claim, "no comparable vendor practice," universal/enterprise applicability,
"R3 selects the right mechanism") reappears positively anywhere in the 423-line document.

Independently re-derived, not merely trusted from the document's own restatement:

- Six-row band table (§4/§5.5): rules/retrieval mean accuracy and gap by realized-ADS band × lexical
  condition, cross-checked against `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5 and the underlying
  `posthoc_analysis_report.json` — exact match, including the widening-gap figures cited in §5.5
  (−0.1374 → −0.1678 → −0.1851 under VARIED, rounded to −0.137/−0.168/−0.185 in the document).
- Pearson r ranges: `posthoc_analysis_report.json` gives `pearson_ads_vs_rules_acc__VARIED=0.9091`,
  `__CLEAN=0.9592` (range 0.909–0.959, exact match) and `pearson_ads_vs_retrieval_acc__VARIED=0.9476`,
  `__CLEAN=0.9549` (range 0.948–0.955, exact match).
- 32/32 (100%) vs. 0/18 (0%) band-agreement split: confirmed directly against
  `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9's realized-ADS-band table (0.70–0.90 → 32/32 = 100%;
  ≥0.90 → 0/18 = 0%) — exact match, correctly described as the "sharper," realized-band split rather
  than the looser nominal-target 30/30-vs-2/20 framing.
- 91.2%/0.847/0.964/0.695/R1-R3-R4-R5 production figures (§6): cross-checked directly against
  `EVIDENCE_BASELINE.md` §1 — all five values and all four decisions match exactly, and the document
  correctly attaches the "likely understated, unverified" caveat to the ADS/deterministic-share
  figures (Note 1 in `EVIDENCE_BASELINE.md`).
- Frozen evidence: `data/outputs/experiments/exp1/final/` confirmed byte-identical to the
  `6fb6188` freeze commit (empty diff, empty status) — not touched by this document or this pass.

## 5. Scientific consistency

The Results architecture (§4 of the document) keeps 6a ("ADS predicts mechanism accuracy," §5.2) and
6b ("ADS does not predict mechanism ranking," §5.4) as structurally separate subsections, with §5.3
(the CLEAN-vs-VARIED constancy finding) placed between them as the evidentiary hinge — this matches
`CONTRIBUTION_LOCK.md` §4's explicit instruction that these are "not the same claim, do not stand or
fall together" and matches §6's two-part Formulation #2 wording exactly. The Discussion architecture
(§5 of the document) answers all eight of the brief's questions in the same order the brief specifies,
sourcing each row to a specific `CONTRIBUTION_LOCK.md` section rather than inventing new synthesis.

The document's title/abstract/section/table/figure choices trace cleanly to `CONTRIBUTION_LOCK.md`
§6/§11 and `PAPER_CONTRACT.md` throughout; no chain-break of the kind that produced the historical
A5/A6 findings (a script's behavior silently diverging from what a doc claims, or a stat re-derived
differently in two places) was found — every number in the document is a restatement of an
already-independently-verified figure (§4 above), not a fresh computation this document performs
itself.

One traceability nit found (see §11, finding F1): §12's citation of "`MANUSCRIPT_FORMAT_RESEARCH.md`
§1.15's recommendation to link rather than bundle the raw CSV" attributes a recommendation to the
wrong section. That recommendation is actually made in `PUBLIC_RELEASE_BOUNDARY.md` §3.B (which itself
cites `MANUSCRIPT_FORMAT_RESEARCH.md` §1.7's 50MB-cap discussion, not §1.15, as its size rationale).
§1.15 lists what should *not* enter the arXiv package (build artifacts, discarded figures, confidential
data, internal audit reports) and does not itself discuss CSV bundling vs. linking. The underlying
claim (link, don't bundle, the raw CSV) is correct and traceable — only the section citation is
mis-pointed.

## 6. Evidence/claim traceability

Every quantitative claim in the changed document traces to a currently-committed artifact, verified
directly rather than by trusting the document's own citation:

- Band table and Pearson r's → `data/outputs/experiments/exp1/posthoc/posthoc_analysis_report.json`
  (re-opened and grepped this pass) and `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5/§7/§9/§11.
- 32/32 vs. 0/18 split → `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9, itself derived from the frozen CSV.
- Production figures → `EVIDENCE_BASELINE.md` §1, byte-for-byte match.
- "Exactly `CONTRIBUTION_LOCK.md` §11.A" research-question wording (§2 item 2 of the document) →
  grepped `CONTRIBUTION_LOCK.md` line 360, verbatim match confirmed.
- H1 PARTIALLY SUPPORTED framing (§11 group C, §5 Discussion row 2) → grepped
  `EXPERIMENT_1_REDESIGN_REVIEW.md` line 555, the pre-registered row text matches what the document
  describes as the "exact language" it is honoring.
- Reproducibility claims (§12: "all passing per the E0 checkpoint audit") → confirmed against
  `E0_CHECKPOINT_AUDIT.md` item 3, which recorded 4/4, 2/2, 5/5, 8/8, 11/11 passes for exactly the five
  named test files.
- Open items carried forward (§14 item 4) → confirmed against `MANUSCRIPT_FORMAT_RESEARCH.md` §3's
  three-item list (endorsement, license, AI-disclosure wording), verbatim match.

No number in the document was found that isn't traceable to `CONTRIBUTION_LOCK.md`,
`EVIDENCE_BASELINE.md`, or the frozen Experiment 1 artifacts (the only exception being the one
mis-cited section number in §5/§11 finding F1, which does not change the underlying fact's
correctness).

## 7. Code review

Not applicable — no code was written or modified by this pass.

## 8. Experimental integrity

Not applicable in the sense of new experimental work (none was run, none was authorized to be run).
Confirmed as a boundary check: `data/outputs/experiments/exp1/final/` is byte-identical to the freeze
commit; no frozen parameter (δ=0.02, cutoff=75, thresholds 0.90/0.70, seeds, targets) is referenced by
`MANUSCRIPT_ARCHITECTURE.md` with any value other than the frozen ones (§3 Section-architecture table,
§8 Table plan T3, §9 Equation plan E2/E3 all restate the frozen values exactly, no re-tuning proposed).

## 9. Scope/GPS alignment

**PASS.** This document is exactly Phase E1's authorized scope per `PHASE_E_PLAN.md` Task 9's
milestone table ("Confirm/refine Task 3's structure... Drafting section text [is] out of scope") and
`PAPER_CONTRACT.md` §1's north star (defensible draft → audit → arXiv). No prose, no `.tex`, no figure,
no bibliography was created — confirmed directly, not merely asserted by the document's own header. The
document explicitly defers four items to a human decision (§14) rather than deciding them itself,
consistent with `PAPER_CONTRACT.md` §12's stop-rule spirit of not front-loading judgment calls that
belong to a later phase. `RESEARCH_GPS.md`'s DO NOT CHASE list is respected: no new experiment is
proposed or implied as needed by this document (§F6's rejection, §9's "no genuine evidence gap"
reasoning throughout, matches `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §14's "no further experiment needed"
finding). The one live tension is that `RESEARCH_GPS.md` itself is stale on current phase (§2) — a
pre-existing, already-twice-flagged issue, not something this document should have fixed (manuscript
architecture is not `RESEARCH_GPS.md`'s owner) and not a defect in this document.

## 10. Git hygiene

`git status --porcelain` shows one modified-state item of note: **seven** untracked `research/*.md`
files currently sit in the working tree — `E0_CHECKPOINT_AUDIT.md`, `MANUSCRIPT_ARCHITECTURE.md`,
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_AUDIT_REPORT.md`,
`PHASE_E_PLAN.md`, `PUBLIC_RELEASE_BOUNDARY.md`. Six of these predate this pass (leftover from Phase
E0, already flagged by `E0_CHECKPOINT_AUDIT.md` and `PHASE_E_AUDIT_REPORT.md` as "not part of this
checkpoint" / to be staged with a targeted `git add`, not `git add .`/`-A`). Only
`MANUSCRIPT_ARCHITECTURE.md` was added by this specific pass. Nothing is staged; nothing was committed
or pushed by this audit. Grepped `MANUSCRIPT_ARCHITECTURE.md` for credential/secret/AWS-key/CUI/
local-path patterns — none found (the document contains no data, only prose/tables referencing other
docs by name). No `.bak`/`.swp`/`.orig`/`.tmp` files found. `README.md`, `TECHNICAL_REPORT.md`, and
`METHODOLOGY.md` are unmodified (`git diff HEAD` on each is empty).

**Recommendation for a future commit:** stage exactly the files the human intends for that checkpoint
by name (e.g. `git add research/MANUSCRIPT_ARCHITECTURE.md`) — a broad `git add .`/`-A` would sweep in
the six pre-existing untracked files as well, none of which have been independently checkpoint-audited
as a group.

## 11. Findings

1. **[OPTIONAL FUTURE WORK]** `research/MANUSCRIPT_ARCHITECTURE.md` §12, line ~375: cites
   "`MANUSCRIPT_FORMAT_RESEARCH.md` §1.15's recommendation to link rather than bundle the raw CSV" —
   that recommendation actually appears in `PUBLIC_RELEASE_BOUNDARY.md` §3.B (which cites
   `MANUSCRIPT_FORMAT_RESEARCH.md` §1.7's 50MB-cap discussion, not §1.15, for its size rationale).
   `MANUSCRIPT_FORMAT_RESEARCH.md` §1.15 covers a different topic (what must not enter the arXiv
   package generally). The underlying claim is correct; only the section pointer is wrong. Low
   severity — a reader following the citation to verify it would find a real but different section on
   the same page, not a fabricated claim.
2. **[OPTIONAL FUTURE WORK]** Title candidate #5 in §1 ("Design-Time Architecture Selection from
   Historical Label Consistency: A Negative Result Under Lexical Noise") uses the exact phrase
   "design-time architecture selection" that echoes the CHALLENGED general C2 framing
   (`PAPER_CONTRACT.md` §3 row 3). The document itself flags this risk explicitly, does not recommend
   the title (recommends #1), and argues the subtitle narrows it — this reviewer agrees the hedge is
   adequate (a reader who reads the full title, not just the pre-colon clause, gets the negative-result
   framing), but flags it because a title is a place where a "reader who stops at the colon" risk is
   real and the document's own text concedes as much. No action required unless this title is
   eventually selected, in which case the subtitle's narrowing role becomes load-bearing and should be
   re-checked at drafting time.
3. **[OPTIONAL FUTURE WORK, PRE-EXISTING]** `research/RESEARCH_GPS.md`'s Gate 4 checklist remains
   stale (unchecked boxes) relative to `CONTRIBUTION_LOCK.md`'s "Adopted" status. Not introduced or
   worsened by this pass; already flagged by two prior audits (`E0_CHECKPOINT_AUDIT.md`,
   `PHASE_E_AUDIT_REPORT.md` finding 1). Restated here only so it remains visible; not this document's
   responsibility to fix.
4. **[OPTIONAL FUTURE WORK, PRE-EXISTING]** Six untracked `research/*.md` files from Phase E0 remain
   uncommitted alongside the new `MANUSCRIPT_ARCHITECTURE.md`. Not a defect of this pass (nothing was
   staged or committed), but worth the human's attention before any checkpoint commit — see §10's
   recommendation.

No REQUIRED NOW findings were identified. All eight of the launching task's explicit verification
points (PAPER_CONTRACT match, CONTRIBUTION_LOCK match on the 6a/6b split, no rejected claim reappearing
positively, production data confined to motivation/context with correct numbers and caveats, honest H1
partial-support framing, non-overclaiming titles, storyline coherence against frozen evidence, and
arXiv/public-release file boundaries) were independently checked and confirmed accurate. The six-row
band table, Pearson r ranges, and 32/32-vs-0/18 split were independently recomputed/cross-checked
against `EXPERIMENT_1_POSTHOC_ANALYSIS.md` and the underlying `posthoc_analysis_report.json` and match
exactly.

## 12. Required fixes

None. (Empty — no REQUIRED NOW findings.)

## 13. Verdict

## 🟡 PASS_WITH_NOTES

`research/MANUSCRIPT_ARCHITECTURE.md` is an accurate, well-bounded Phase E1 planning document. It
respects every clause of `PAPER_CONTRACT.md` checked (§2 claims-may-make, §3 claims-must-not-make, §5
production-data rule, §6 generalization rule, §7 numerical rule, §8 contribution rule), preserves the
6a/6b accuracy-vs-ranking distinction from `CONTRIBUTION_LOCK.md` §4/§6 as a structural boundary (not
merely a caveat), states H1's PARTIALLY_SUPPORTED verdict honestly without softening, confines the
production case study to motivation/context with correctly-caveated numbers, and creates no
manuscript/LaTeX/figure/bibliography file — confirmed directly, not merely asserted by the document's
own header. The E3 storyline test in §13 was checked sentence-by-sentence against
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` and holds without overclaiming. The two findings raised (a
mis-pointed section citation; one title candidate whose hedge this reviewer independently judges
adequate but worth re-checking if selected) are both non-blocking and do not affect the document's
validity as a planning artifact. The two pre-existing, already-flagged issues (`RESEARCH_GPS.md`
staleness; six untracked Phase-E0 files) are restated for visibility, not newly created by this pass.
Safe to proceed to Phase E2 once the human has reviewed the open decisions in §14 of the audited
document.

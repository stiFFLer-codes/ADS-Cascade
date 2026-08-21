# E5.0 GPS Housekeeping Audit

> Lightweight review of a single pending edit to `research/RESEARCH_GPS.md` (uncommitted at audit
> time). Scope: factual accuracy of the new pointer-document text, no scope creep beyond a
> status/pointer update, no rewriting of history. Not a full seven-dimension research audit — no
> code or experimental artifact changed, so those categories are not applicable.

---

## 1. Repository state

- Branch: `main`. `HEAD` = `fa55ef6` ("Phase E4: complete manuscript audit and release hygiene
  checkpoint"), confirmed identical to `origin/main` (verified via `git branch -vv` and
  `git log --all -1 origin/main`) — the E4 checkpoint is genuinely committed and pushed, as the
  edited text claims.
- Working tree: one modified file, `research/RESEARCH_GPS.md` (`git status --porcelain` shows
  ` M research/RESEARCH_GPS.md`), plus two pre-existing untracked files
  (`research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md`, `research/E4_CHECKPOINT_MANIFEST_VERIFICATION.md`)
  that are untouched by this change (not part of the diff, not staged, not referenced by the new
  GPS text).
- Diffed: `git diff -- research/RESEARCH_GPS.md` (full diff reviewed line by line), plus
  `git show --stat fa55ef6` and `git show fa55ef6 -- manuscript/main.tex` to independently
  re-derive the claims the new text makes about that commit.

## 2. What changed (categorization)

Docs/pointer-document only. `CURRENT LOCATION`, `COMPLETED`, `CURRENT GATE`, `NEXT GATE`,
`RESEARCH COMPLETION SCORECARD`, and `DO NOT CHASE` sections of `research/RESEARCH_GPS.md` were
rewritten to reflect Phase D (contribution lock) and Phase E0-E4 as complete and Phase E5
(readability pass) as in progress. No manuscript prose, no code, no experimental artifact, no
`CONTRIBUTION_LOCK.md` / `PAPER_CONTRACT.md` / frozen-evidence file was touched — confirmed by
`git status` showing exactly one modified file.

## 3. Independent fact-checks

**Verified accurate:**

- **Gate 4 "Adopted" status.** `research/CONTRIBUTION_LOCK.md` §12 reads "**Adopted.** Formulation
  #2 (§6) is locked..." and the Auditor verdict section reads "🟢 **PASS.**...**Formulation #2
  survives adversarial review. Gate 4 is complete.**" — matches the new GPS text's quoted wording
  exactly.
- **Commit `fa55ef6` content.** `git show --stat fa55ef6` and the commit message independently
  confirm: two E4.1 prose corrections (confidentiality qualifier + terminology fix), a provenance/
  hygiene pass, and committing the previously-uncheckpointed `MANUSCRIPT_ARCHITECTURE.md` (Phase
  E1's artifact) — all claims in the new GPS text about this commit check out against the commit
  itself, not just its message.
- **The two E4.1 fixes, verified in the actual diff** (`git show fa55ef6 -- manuscript/main.tex`):
  - Confidentiality qualifier: `main.tex` now reads "...fixed at 0.695 -- the production-observed
    value, cited from a confidential engagement and not independently reproducible from this
    repository -- so that..." — matches the claimed "production-data confidentiality qualifier."
  - Terminology fix: `main.tex` now reads "...the same rule selected its embedding-based branch
    (`EMBEDDING_PRIMARY`) instead -- a different mechanism from the lexical-similarity `retrieval`
    mechanism this paper's Experiment~1 tests..." — matches the claimed
    `EMBEDDING_PRIMARY`/`retrieval` terminology fix.
- **68 `\subsection`s.** `grep -c '^\\subsection{' manuscript/main.tex` → 68. Exact match.
- **H1 stated as PARTIALLY_SUPPORTED.** Confirmed present in `manuscript/main.tex` via direct grep.
- **PHASE_E_PLAN.md's E5/E6 milestone-naming claim.** `research/PHASE_E_PLAN.md` Task 9 table
  literally labels "E5 — Adversarial claim/citation audit" and "E6 — Public reproducibility audit"
  — the new GPS note's explanation of the renaming (this project's live "Phase E5" = readability,
  not that document's original E5 label) is an accurate, non-fabricated reconciliation, not an
  invented distinction.
- **DO NOT CHASE new bullet.** The new E5.1-scoped bullet ("figure generation, citation expansion,
  abstract optimization, final publication polish, or arXiv submission-package prep") matches
  exactly the deferred items described in the same edit's own `NEXT GATE` section and in
  `PHASE_E_PLAN.md`'s Task 9 — no new restriction was invented beyond what's independently
  documented elsewhere.
- Referenced future-gate artifacts exist: `manuscript/figures/generate_figures.py` (exists);
  `citation_ledger.csv` exists at `research/literature/citation_ledger.csv` (GPS text doesn't claim
  a specific path, so this isn't a discrepancy).

**Discrepancy found — factual inaccuracy in the new text itself:**

- **"10 `\section`s" (line 27) does not match the manuscript.** `grep -c '^\\section{'
  manuscript/main.tex` → **9**, not 10 (`Introduction`, `Related Work`, `Problem Setting and Signal
  Definition`, `Experimental Design`, `Results`, `Discussion`, `Limitations`, `Future Work`,
  `Conclusion`). The References list is produced by `\bibliographystyle{plainnat}` /
  `\bibliography{references}`, not a literal `\section{References}` macro — so "10 `\section`s" is
  incorrect as a literal claim about the LaTeX source (there are 9 `\section` macros; References is
  a 10th *rendered* heading generated a different way).
- **This is also an internal self-contradiction within the same edit.** Two lines apart in the
  diff, `CURRENT GATE` (line 52) says "**All nine manuscript sections** have real prose," while
  `CURRENT LOCATION` (line 27) says "10 `\section`s." The scorecard (lines 94-95) lists 10 checked
  items (9 named sections + References) without flagging that References isn't a `\section` macro.
  The underlying substance (9 `\section` commands + an auto-generated References list = 10
  conceptual/rendered sections) is defensible, but the text as written asserts two different literal
  section counts in the same file and states the backtick-quoted `\section` figure imprecisely.

## 4. Research integrity

Not applicable in the deep sense (no research content changed), but the specific check requested —
no rejected claim quietly resurrected — passes: the new text does not touch H1's wording, does not
call ADS a novel metric, does not claim general applicability, and explicitly preserves "H1 remains
stated as PARTIALLY_SUPPORTED... not upgraded or fully falsified" and the 6a/6b separation, which is
consistent with `CONTRIBUTION_LOCK.md` §6 and §4's explicit warning against collapsing that
distinction.

## 5. Scientific consistency

Not applicable — no research-question/hypothesis/design/results/interpretation chain was altered.
The edit's own internal chain (Gate 4 closed → Phase E drafted → E4 audited → E5 readability pass
next) is consistent with `CONTRIBUTION_LOCK.md`, `fa55ef6`'s commit message, and `PHASE_E_PLAN.md`,
modulo the section-count slip in §3 above.

## 6. Evidence/claim traceability

All quantitative/status claims in the diff were traced to a live, currently-committed artifact
(`CONTRIBUTION_LOCK.md`, `fa55ef6`'s actual diff, `manuscript/main.tex`, `PHASE_E_PLAN.md`) rather
than to another document's prose restating it once removed, with one exception: the "10
`\section`s" figure does not trace cleanly to the source file (see §3). No number in the diff is
presented as settled without a source; the section-count issue is an accuracy slip, not an
untraceable claim.

## 7. Code review

Not applicable — no code changed.

## 8. Experimental integrity

Not applicable — no experimental artifact changed.

## 9. Scope/GPS alignment

The edit is exactly what it claims to be: a status/pointer correction, not new research. It
correctly resolves the staleness previously flagged as `PHASE_E_AUDIT_REPORT.md` §11 finding 1
(Phase D.1 shown complete but Gate 4/Phase E not reflected). The new DO NOT CHASE bullet keeps E5.1
bounded to a readability/structure pass, consistent with the project's stopping rule and north star
(defensible draft → reproducibility package → arXiv preprint). No detour, no unrequested new
experimentation, no premature optimization.

## 10. Git hygiene

`git status --porcelain` shows exactly one modified file (`research/RESEARCH_GPS.md`) and two
pre-existing untracked audit files that are unrelated to and untouched by this edit. No secrets,
credentials, client data, real-company names, local Windows paths, or usernames found in the diff
(the diff is prose about phase status only). No `README.md`, `TECHNICAL_REPORT.md`, or
`METHODOLOGY.md` changes. Nothing staged. A safe `git add` for this change would be
`git add research/RESEARCH_GPS.md` alone; the two untracked audit files are a separate, pre-existing
matter not part of this review's scope.

## 11. Findings

1. **[CONDITIONAL — REQUIRED NOW]** `research/RESEARCH_GPS.md` line 27 states "10 `\section`s,"
   which does not match `manuscript/main.tex` (9 `\section{}` macros; References is generated via
   `\bibliography`, not a `\section` macro). The same file's line 52 says "nine manuscript
   sections," contradicting line 27 two sections later. Fix: make the two lines agree, and phrase
   the References item precisely (e.g., "9 `\section` commands plus an auto-generated References
   list from `\bibliography` = 10 rendered sections") so a future session doesn't inherit an
   internally inconsistent count.
2. **[OPTIONAL FUTURE WORK]** None beyond the above — no other inaccuracy, scope creep, or
   history-rewrite was found in this edit.

## 12. Required fixes

- Correct the section-count inconsistency between `CURRENT LOCATION` (line 27, "10 `\section`s")
  and `CURRENT GATE` (line 52, "nine manuscript sections") in `research/RESEARCH_GPS.md`, stating
  precisely how the 10th "section" (References) is produced.

## 13. Verdict

🟡 **PASS_WITH_NOTES.** Every substantive factual claim in the diff (Gate 4 "Adopted" status,
commit `fa55ef6`'s content and push status, the two E4.1 prose fixes, the 68-subsection count, the
H1/PARTIALLY_SUPPORTED preservation, the PHASE_E_PLAN.md E5/E6 milestone-naming reconciliation, and
the DO NOT CHASE bullet's accuracy) independently re-verified against live repository state. No
historical research decision was rewritten — only `research/RESEARCH_GPS.md`'s status/pointer
content changed, and git status confirms no other file is touched. No rejected claim was
resurrected, no scope creep introduced, git hygiene is clean. The single finding — a "10
`\section`s" figure that both slightly misdescribes how the manuscript's References section is
generated and directly contradicts this same edit's own "nine manuscript sections" phrase two
sections later — is a minor, easily-fixed accuracy/self-consistency slip in a pointer document, not
a research-integrity or hygiene problem. Safe to checkpoint; fix the count discrepancy
opportunistically (or in the same commit, since it's a one-line change) rather than as a blocker.

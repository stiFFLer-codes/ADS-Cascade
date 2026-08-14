# E5.1 Closeout / E5.2 Gate-Open — RESEARCH_GPS.md Housekeeping Audit

> Pre-commit review of a single pending edit to `research/RESEARCH_GPS.md`: closes out E5.1
> (readability/structure pass, committed/pushed at `83ee5d3`) and opens E5.2 (citation + claim
> audit) as the current gate, recording the author-locked E5.0→E7 sequence and a new "do no harm"
> governing rule. Lightweight housekeeping review, not a full seven-dimension research audit — no
> re-verification of frozen Experiment 1 evidence or test suite (E5.1's own audit already did that
> and nothing code-related changed here).

---

## 1. Scope — confirmed

`git status --porcelain` shows exactly one modified file: `research/RESEARCH_GPS.md`. Three
untracked files are present (`research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md`,
`research/E4_CHECKPOINT_MANIFEST_VERIFICATION.md`, `research/E5_GPS_HOUSEKEEPING_AUDIT.md`) —
all pre-existing from prior sessions (timestamps 13 Aug 16:25–17:08, before this edit), not touched
or created by this edit, out of scope for this review per the task brief.

`git diff --stat` confirmed **zero changes** (staged, unstaged, or otherwise) in:
`manuscript/main.tex`, `references.bib`, `research/PAPER_CONTRACT.md`,
`research/CONTRIBUTION_LOCK.md`, `data/outputs/experiments/exp1/final/`. All empty diffs. This is
a pure status/pointer update — no forbidden file was touched.

(Note: the session-start `gitStatus` snapshot shown in this conversation's system context listed
`manuscript/main.tex` as modified. Independently re-run `git status`/`git diff --stat` at audit
time shows `main.tex` clean with zero diff against HEAD — that snapshot was stale relative to
current repo state, not a discrepancy in the edit under review.)

## 2. Factual accuracy of new claims — verified

| Claim in new GPS text | Verification method | Result |
|---|---|---|
| Commit `83ee5d3` exists, on `main`, message = "Phase E5.1: manuscript readability/structure pass" | `git show --stat 83ee5d3`, `git branch --contains 83ee5d3` | Confirmed. Commit message body also states "68 to 43 subsections (37%)" and per-section breakdown, matching GPS prose. |
| 68→43 subsection count | Independent `grep` for `^\\subsection\{` on current `manuscript/main.tex` (not trusting the file's own prose) | **43**, exact match. (`^\\subsubsection\{` = 0, so no double-count risk.) |
| `research/E5_1_MANUSCRIPT_AUDIT.md` verdict = auditor PASS | Read the file directly, §13 | Verdict is **🟢 PASS**, explicitly: "Safe to stage and checkpoint as-is." Matches GPS's "Independently audited: PASS" claim. |
| H1 still stated `PARTIALLY_SUPPORTED` in current `manuscript/main.tex` | `grep -i "partially supported"` on current file | Confirmed at lines 1267–1269 (`\subsection{H1 Only Partially Supported}`, "H1 (revised) is only partially supported, matching the pre-registered PARTIALLY\_SUPPORTED row...") and reiterated at line 1409. Not upgraded, not softened. |
| Three pre-existing broken `Section~X.Y` cross-references fixed | Cross-checked against `E5_1_MANUSCRIPT_AUDIT.md` §3, then independently re-derived against `git show fa55ef6:manuscript/main.tex` (the E4-audited draft) | **Mostly confirmed, one imprecision** — see Finding F1 below. |

## 3. No historical research decision rewritten — confirmed

The diff only touches `CURRENT LOCATION`, `COMPLETED`, `CURRENT GATE`, `NEXT GATE`, the scorecard's
Gate 5 row, and `DO NOT CHASE`. No frozen artifact, no `CONTRIBUTION_LOCK.md` wording, and no past
phase's description of *what happened* was altered — the E3/E4 narrative (contribution lock,
adversarial audit, two E4.1 corrections, H1 status) is carried forward unchanged, only appended to.
The old "Note on milestone naming" blockquote (which flagged `PHASE_E_PLAN.md`'s Task 9 using "E5"
for the citation/claim audit) is fully removed and replaced by the new "Locked E5+ sequence" block,
which explicitly states it supersedes that original labeling — this is the ambiguity note being
resolved as intended, not silently dropped.

## 4. Internal consistency — confirmed

CURRENT LOCATION (E5.1 complete @ `83ee5d3`, E5.2 current), COMPLETED (lists both E5.0 @ `4d031ab`
and E5.1 @ `83ee5d3`), CURRENT GATE (E5.2 — Citation + Claim Audit), NEXT GATE (E5.3 — Public
Reproducibility Audit, then E5.4→E5.5→E6→E7), and the RESEARCH COMPLETION SCORECARD's Gate 5 row
(✅ readability/structure pass E5.1 · ⬜ citation/claim audit E5.2 current · ⬜ E5.3 · ⬜ E5.4 · ⬜
E5.5) all agree with each other on what's done vs. current vs. next. No stale reference to the old
milestone-naming ambiguity note remains anywhere in the file (full read of all 157 lines).
`DO NOT CHASE` was updated in the same edit to reference the new E5.2 scope and the new governing
rule, consistently with the rest of the document.

## 5. Git hygiene — confirmed clean

`git diff` on `research/RESEARCH_GPS.md` grepped for password/secret/API-key/token/bearer patterns
and for local Windows paths / the committer's username: no matches. This is a prose-only status-doc
edit; no risk vectors present.

---

## Findings

**F1 — OPTIONAL FUTURE WORK (minor factual imprecision, not blocking).** GPS line 31–32 states:
"Three pre-existing broken internal `Section~X.Y` cross-references (predating this session, present
since the E4-audited draft) were found and fixed as a byproduct of the required renumbering." This
is accurate for two of the three bundled fixes but overstated for part of the third.

Independently re-derived against `git show fa55ef6:manuscript/main.tex` (the actual E4-audited
draft, pre-E5.1):

- **Fix 1** (R3 definition, old `Section~4.10`→ new `4.7`): genuinely pre-existing broken. Old
  `Section~4.10` = "Paired Comparison and Winner/Tie Definition" (line 738), but R3's threshold
  definition actually lived in old `Statistical Analysis` (old 4.11, line 769). Confirmed broken
  in the E4 draft, independent of this session's edits.
- **Fix 2** (whole-set-accuracy metric, old `Section~4.9`→ new `4.7`): genuinely pre-existing
  broken. Old `Section~4.9` = "Train/Test Separation" (line 722); the metric is actually defined in
  old `Statistical Analysis` (4.11, line 769). Confirmed broken in the E4 draft.
- **Fix 3** as described bundles two different reference sites, and they don't both fit the
  "pre-existing broken" description:
  - The `Section~6.5`→`6.4` legs (old lines 1085, 1385, both "the mechanistic account... developed
    in Section~6.5"): genuinely pre-existing broken. Old `Section~6.5` = "Why Consistency Predicts
    Difficulty but Not Ranking," not the representation-stability mechanistic account, which was
    old `6.6`. Confirmed broken in the E4 draft.
  - The `Section~7.10`→`7.1` leg (old line 1225, "...would strengthen it further
    (Section~7.10)"): old `Section~7.10` was in fact **"H1 Only Partially Supported"** — the
    correct target. This reference was **correct in the E4-audited draft** and only became
    numerically wrong because *this session's own edit* moved that subsection from position 10 to
    position 1 within Limitations. It is a self-caused renumbering consequence of E5.1's authorized
    reorder, not a bug "predating this session."

Net effect: the GPS's blanket characterization ("three pre-existing broken... references... present
since the E4-audited draft") slightly overstates one of the three bundled items. This is an
editorial/narrative imprecision in a historical-summary paragraph, not a claim with scientific
consequence — it doesn't touch evidence, results, or the contribution, and `E5_1_MANUSCRIPT_AUDIT.md`
itself (§3) describes the `7.10`→`7.1` fix accurately (as pointing at "the now-first Limitations
subsection," without asserting it was previously broken), so the underlying audit trail is not at
fault — only this GPS paragraph's compressed summary. Recommend tightening the wording at the next
opportunity that touches this paragraph (e.g., "two pre-existing broken references, plus one
cross-reference update required by this session's own H1 reorder") — not urgent enough to block
this checkpoint.

No other findings. No rejected claim reappeared, no frozen evidence touched, no scope creep, no git
hygiene issue.

---

## Required fixes

None. F1 is optional future-work wording polish, not a blocking condition.

---

## Verdict

🟡 **PASS_WITH_NOTES.**

The edit is exactly what it claims to be: a pure status/pointer update to `research/RESEARCH_GPS.md`
that closes out E5.1, opens E5.2, records the author-locked E5+ sequence, and adds the "do no harm"
governing rule — with zero changes to any other file, including all explicitly protected paths.
Every checkable factual claim in the new text was independently verified against live repo state
(commit hashes, subsection count, H1 status, the E5.1 audit's own PASS verdict) and matches. The
document is internally self-consistent across CURRENT LOCATION / COMPLETED / CURRENT GATE / NEXT
GATE / SCORECARD, and the old milestone-naming ambiguity note is cleanly resolved rather than left
stale. The single finding (F1) is a minor overstatement in one clause of a historical-summary
paragraph — real but non-blocking, with no research-integrity, evidence, or scope consequence. Safe
to stage and commit as-is; F1 is worth a wording tweak next time this paragraph is touched, not a
reason to hold the checkpoint.

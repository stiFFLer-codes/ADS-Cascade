# E4 Checkpoint Hygiene Audit — Independent Challenge Pass

> Independent, from-scratch re-verification of `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` (the
> primary session's hygiene/classification pass). Every one of the 14 files that document
> classified was re-read in full by this pass, independently of the primary document's summaries.
> Read-only throughout: nothing staged, committed, or pushed; `manuscript/main.tex`,
> `manuscript/references.bib`, `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, and all
> frozen evidence were read only, never modified. No experiment was run (`pytest` only).

---

## 0. Framing correction on the primary document's own count

The task brief and the primary document both say "14 currently-untracked `research/*.md` files."
`git status --short --untracked-files=all` at the time **this** pass ran shows **15** untracked
`research/*.md` files, plus the unrelated tracked modification to `manuscript/main.tex`:

```
?? research/E0_CHECKPOINT_AUDIT.md
?? research/E2_FINAL_CHECKPOINT_AUDIT.md
?? research/E3_FINAL_AUDIT_V2.md
?? research/E3_FINAL_CHECKPOINT_AUDIT.md
?? research/E4_ARTIFACT_AUDIT.md
?? research/E4_CHECKPOINT_HYGIENE_AUDIT.md      <- the primary document itself
?? research/E4_RESOLUTION_AUDIT.md
?? research/E4_RESOLUTION_AUDIT_INDEPENDENT.md
?? research/E4_SCIENTIFIC_AUDIT.md
?? research/MANUSCRIPT_ARCHITECTURE.md
?? research/MANUSCRIPT_ARCHITECTURE_AUDIT.md
?? research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md
?? research/MANUSCRIPT_FORMAT_RESEARCH.md
?? research/PHASE_E_AUDIT_REPORT.md
?? research/PHASE_E_PLAN.md
?? research/PUBLIC_RELEASE_BOUNDARY.md
```

This is not a discrepancy in substance: `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` is the primary
session's own deliverable, necessarily written (and therefore appearing as untracked) *after* the
14-file snapshot its own §1 `git status` block records. The 14-file inventory in the primary
document is internally consistent with itself. Not a finding against the primary document — recorded
here only so a reader comparing today's live `git status` to the document's own text isn't confused
by the apparent off-by-one.

All 14 files in the primary document's inventory were independently read in full by this pass. The
primary document itself (the 15th file) was also read in full, per the task's instructions, as the
object of this challenge.

---

## 1. Independent classification — do I agree with 14-for-14 KEEP+COMMIT?

**Outcome: yes, on all 14, but not for a uniform reason, and with one weaker pair flagged
explicitly.** Reading each file in full turned up no exact or near-exact duplicate of any other
untracked file or of any already-committed file (`PAPER_CONTRACT_AUDIT_REPORT.md`,
`MANUSCRIPT_SKELETON_AUDIT.md`, `E3_DRAFT_AUDIT_REPORT.md`, `E3_STATISTICAL_RECONCILIATION.md`,
`E3_STATISTICAL_RECONCILIATION_AUDIT.md`, `E3_CHECKPOINT_STAGED_AUDIT.md` — all six read/confirmed
via `git show --stat` on the three relevant commits). Every file contributes something the others
don't. That said, the 14 files fall into three genuinely different classes, and the primary document
flattens them into one undifferentiated "KEEP+COMMIT, not duplicated" bucket without naming the
distinction — a real gap in its own reasoning, even though it doesn't change the outcome:

**Class A — cited-by-manuscript, load-bearing planning artifacts** (`MANUSCRIPT_ARCHITECTURE.md`,
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_PLAN.md`,
`PUBLIC_RELEASE_BOUNDARY.md`). Independently verified via `grep` against the current
`manuscript/main.tex` (not trusted from the primary document's claim):

| File | Times referenced in `main.tex` |
|---|---|
| `MANUSCRIPT_ARCHITECTURE.md` | 10 |
| `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` | 2 |
| `MANUSCRIPT_FORMAT_RESEARCH.md` | 3 |
| `PHASE_E_PLAN.md` | 1 |
| `PUBLIC_RELEASE_BOUNDARY.md` | 2 |

This confirms the primary document's core claim: these five are genuinely cited by name from
`manuscript/main.tex`'s own header/section `% EVIDENCE:` anchors, and none of them has ever been
committed (confirmed independently below, §2). This is the strongest class — real citation-to-nowhere
risk if not committed. **One precision correction to the primary document, not a disagreement in
outcome:** it states `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` is "cited by name in `manuscript/main.tex`
body prose (§2.8, the vendor-practice hedge)." Direct inspection (line 425-430) shows the citation is
inside a `%`-comment `% EVIDENCE:` block immediately following the §2.8 prose paragraph, not inside
the compiled body prose itself — the E4 audit's own Part A explicitly distinguishes "body prose" from
"`%` development comments, which never appear in a compiled PDF" (a distinction the project itself
insists matters). This is a minor overstatement in the primary document's own citation of its
evidence, worth correcting, but does not weaken the underlying provenance-gap argument: a reader of
the public `.tex` *source* (not just the PDF) would still find a comment pointing at a file that does
not exist in the committed tree.

**Class B — audit documents that found and closed a real defect** (`E3_FINAL_CHECKPOINT_AUDIT.md`,
`E3_FINAL_AUDIT_V2.md`, `E4_ARTIFACT_AUDIT.md`, `E4_SCIENTIFIC_AUDIT.md`,
`E4_RESOLUTION_AUDIT_INDEPENDENT.md`). Read in full and confirmed each contains content no other
committed or uncommitted file duplicates:
- `E3_FINAL_CHECKPOINT_AUDIT.md` is the sole record of three real hardcoded cross-reference errors
  (`Section~6.2`→6.3, `Section~6.4`→6.5 ×2) that three prior E3 audits missed.
- `E3_FINAL_AUDIT_V2.md` is the sole record confirming those three fixes landed correctly, plus an
  independently-surfaced (and separately resolved) citation slip in a *different* audit report.
- `E4_ARTIFACT_AUDIT.md` is the source of Findings F1-F6, including the two REQUIRED NOW findings
  (F3, F4) that blocked E4 GREEN until fixed — this is the actual evidentiary backbone for why E4
  wasn't a bare rubber-stamp.
- `E4_SCIENTIFIC_AUDIT.md` is the primary E4 deliverable containing the literary/structural/logic
  review (Parts A, C, D, H, J, K) that `E4_ARTIFACT_AUDIT.md` doesn't cover.
- `E4_RESOLUTION_AUDIT_INDEPENDENT.md` independently caught two precision gaps in
  `E4_RESOLUTION_AUDIT.md`'s own self-reporting (the "identically" overstatement, an undercounted
  H1-location tally) — real, if minor, corroborating value a bare re-confirmation wouldn't add.

This is unambiguously KEEP+COMMIT-grade material under the task's own instruction not to delete
historical audit reports that contain unique evidence of a correction.

**Class C — pure verification passes that found nothing wrong (or only optional notes)**
(`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`, `E4_RESOLUTION_AUDIT.md`,
`MANUSCRIPT_ARCHITECTURE_AUDIT.md`, `PHASE_E_AUDIT_REPORT.md`). These do not document a *correction*
in the sense Class B does — `E0_CHECKPOINT_AUDIT.md` found zero issues, `E2_FINAL_CHECKPOINT_AUDIT.md`
found one optional documentation-legibility gap, `MANUSCRIPT_ARCHITECTURE_AUDIT.md` found one
mis-pointed section citation and one already-adequately-hedged title risk. Read on their own, a
legitimate alternative classification exists for at least the weakest two of these
(`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`): **KEEP LOCAL** rather than KEEP+COMMIT,
since a public reader gains little from a document whose entire content is "ran the test suite, it
passed; checked hygiene, it was clean" — a public reader can just run the (already-public) test suite
themselves. I do not overturn the primary document's recommendation here, for a specific reason the
primary document itself half-states but doesn't fully argue: this project has, without exception,
committed exactly this class of document at every other checkpoint (`PAPER_CONTRACT_AUDIT_REPORT.md`
at E0, `MANUSCRIPT_SKELETON_AUDIT.md` at E2, four separate audit docs at E3). Selectively excluding
just these two would create an unexplained gap in an otherwise-uniform governance pattern, which is
itself confusing to a future reader reconstructing "was every checkpoint actually independently
audited before staging, or only some?" This is a defensible reason to keep them — but it is a
*process-consistency* argument, not a *unique-scientific-evidence* argument, and conflating the two
(as the primary document's flat table does) overstates how load-bearing these two specific files are.
`PHASE_E_AUDIT_REPORT.md` is the one Class C file I'd actively argue is *more* valuable than the
primary document credits it: it is the sole record of a real near-miss (an audit subagent briefly
overwrote the frozen `research/AUDIT_REPORT.md` Gate-4 artifact before the mistake was caught and
reverted) — this is exactly the kind of "evidence of a correction" the task's own instruction protects,
and the primary document's one-line summary doesn't foreground it.

**Net verdict on classification: agree with all 14 KEEP+COMMIT outcomes.** The disagreement is with
the primary document's flattened, undifferentiated justification, not with any individual outcome.

---

## 2. `MANUSCRIPT_ARCHITECTURE.md` / `MANUSCRIPT_ARCHITECTURE_AUDIT.md` — "no corresponding commit" claim

Independently verified, not trusted from the primary document:

```
git log --oneline --all -30 -- research/MANUSCRIPT_ARCHITECTURE.md research/MANUSCRIPT_ARCHITECTURE_AUDIT.md
```
returns **no output** — confirmed these two files have never been committed at any point in this
repository's history, on any branch. Separately, `git log --oneline -20` shows the full commit
sequence from `98b386f` through `95c2b18` with **no "Phase E.1" commit anywhere** — `eaaa139` (Phase
E.0) is followed directly by `b776a5e` (Phase E.2). This independently confirms the primary document's
claim: the E1 architecture pass happened in-session but was never checkpointed, even though
`manuscript/main.tex` cites `MANUSCRIPT_ARCHITECTURE.md` by name ten times in its own `%` comments
(§1 above). This is a genuine provenance gap in the currently-public `.tex` source, not an overstated
finding.

---

## 3. The "6 files" / deliberate-exclusion claim for `E3_FINAL_CHECKPOINT_AUDIT.md` and `E3_FINAL_AUDIT_V2.md`

**Partially verifiable from repository artifacts; the specific "explicit user instruction" quote is
not.** What I *can* independently confirm:
- `git show --stat 95c2b18` (the actual E3 commit) shows exactly 6 changed paths:
  `manuscript/figures/generate_figures.py`, `manuscript/main.tex`,
  `research/E3_CHECKPOINT_STAGED_AUDIT.md`, `research/E3_DRAFT_AUDIT_REPORT.md`,
  `research/E3_STATISTICAL_RECONCILIATION.md`, `research/E3_STATISTICAL_RECONCILIATION_AUDIT.md` — no
  more, no fewer, and neither `E3_FINAL_CHECKPOINT_AUDIT.md` nor `E3_FINAL_AUDIT_V2.md` is among them.
- `E3_FINAL_CHECKPOINT_AUDIT.md`'s own §1 states, of its own accord (i.e., written by the auditor
  performing that 4th independent pass, not retroactively): "Staged... exactly 6 paths... Unstaged/
  untracked at the time of this audit (not part of the commit under review, noted for completeness
  only): [it lists itself and eight other files]." This is self-consistent: the document is
  necessarily describing a state in which it existed but was not part of the 6-file staged set —
  i.e., it was written *after* the "exactly 6" boundary had already been fixed, which is structurally
  incompatible with it having been part of that boundary in the first place.
- `E3_FINAL_AUDIT_V2.md` (the 5th pass) independently reproduces the same 6-path staged list and
  states the same untracked-files framing.

This sequencing is internally consistent and independently reconstructable from the files' own content
and the commit's actual diff — it supports the primary document's account that the two files postdate
a fixed 6-file staging boundary. **What I cannot verify:** whether a human gave an "explicit
instruction" using language resembling "commit ONLY these 6 files," since no conversation transcript
is available to this pass and neither file quotes such an instruction verbatim. This is an unverified
historical claim, not a false one — flagging per the task's own instruction to say so when a historical
claim can't be fully confirmed. It does not change the recommendation (KEEP+COMMIT), since the
underlying fact that matters — these two files postdate and were never part of the E3 staged set,
and each contains unique content (a real bug, and its confirmed fix) — is independently verified
regardless of the precise wording of whatever decision excluded them at the time.

---

## 4. Protected-artifact integrity — independently re-run

```
git diff --stat HEAD -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md research/contribution_lock.csv TECHNICAL_REPORT.md README.md METHODOLOGY.md manuscript/references.bib
```
→ **empty.**
```
git diff 6fb6188 -- data/outputs/experiments/exp1/final/
```
→ **empty.**

Both confirmed independently, matching the primary document's §7 exactly. **All protected artifacts
intact.**

---

## 5. Manuscript integrity — independently re-run

```
git diff --stat 95c2b18 -- manuscript/main.tex
```
→ `1 file changed, 9 insertions(+), 5 deletions(-)`, matching the primary document exactly. Read the
full diff directly (not trusted from any report): exactly two hunks —

- §4.2 (~line 600-606): the 0.695 cross-company-alignment sentence now reads "...fixed at 0.695 --
  the production-observed value, cited from a confidential engagement and not independently
  reproducible from this repository -- so that it does not become a second, uncontrolled independent
  variable..." — F3 confirmed present.
- §1.1 (~lines 100-106): "...the same rule selected its embedding-based branch
  (`\texttt{EMBEDDING\_PRIMARY}`) instead -- a different mechanism from the lexical-similarity
  `\texttt{retrieval}` mechanism this paper's Experiment~1 tests (Section~3.4); no embedding-based
  mechanism is evaluated anywhere in this paper." — F4 confirmed present.

Independently grepped for H1 status and Formulation #2's synthesis sentence — both sit well outside
either touched hunk (line ranges ~817-819 for H1, line 1154 for "governed by a [representation-
stability property]"), confirming both are unchanged. H1 is stated as `PARTIALLY~SUPPORTED` (line
817-819); the synthesis sentence at line 1154 is present and untouched. **Manuscript integrity
confirmed exactly as the primary document states.**

---

## 6. E4 GREEN status — independently read and assessed

Read `research/E4_SCIENTIFIC_AUDIT.md` and `research/E4_RESOLUTION_AUDIT_INDEPENDENT.md` in full,
independently of the primary document's summary. Findings:

- `E4_SCIENTIFIC_AUDIT.md`'s own verdict is **🟡 YELLOW — substantial but non-fatal revisions
  required**, not GREEN, with two REQUIRED NOW findings (F3, F4) explicitly blocking a GREEN
  recommendation. This is accurately characterized by the primary document and by the task's own
  framing ("Phase E4 ... reached GREEN after two required corrections (E4.1)") — the sequence is:
  E4 → YELLOW with F3/F4 required → E4.1 fix pass → E4.1 independent re-verification → PASS. The
  "GREEN" language describes the *post-E4.1* state, not E4's own verdict label, and both audit
  documents are consistent about this staging; no overstatement found.
- `E4_RESOLUTION_AUDIT_INDEPENDENT.md`'s verdict is **PASS**, independently re-derived (not merely
  re-read) against the live `manuscript/main.tex`: both F3 and F4 sub-requirements checked
  individually and confirmed present; a whole-document `retrieval`/`embedding` terminology sweep
  independently reproduced; both diff hunks independently located and matched to the resolution
  audit's own claims; two non-blocking precision gaps (the "and" vs. comma phrasing, the "identically"
  overstatement) correctly caught and correctly *not* treated as blocking.
- No overclaiming found in either document's own verdict language relative to what its evidence
  supports.

**E4 GREEN status is accurately represented by the primary document and the underlying audit chain.**

---

## 7. Public-release safety — independently re-run

Grepped all 14 untracked files plus `manuscript/main.tex` for AWS key patterns
(`AKIA`), literal secret/password/API-key assignments, PEM/private-key headers,
`amazonaws.com`/`s3://`/`X-Amz-`, and the operator's local Windows path/username
(`C:\Users\Maitreya`, `MaitreyaSapariya`). Ten total hits, all manually inspected:

- 4 hits are prose *describing* what a prior scan searched for (`E0_CHECKPOINT_AUDIT.md`,
  `E3_FINAL_CHECKPOINT_AUDIT.md`, `PHASE_E_AUDIT_REPORT.md` ×2, `PUBLIC_RELEASE_BOUNDARY.md` ×2) —
  not leaked values.
- 3 hits in `E3_FINAL_AUDIT_V2.md` are the literal local Windows path (an absolute path rooted at
  the operator's home directory, including their real username), but all three are inside that
  document's own **Findings** section, citing the absolute path of a *gitignored scratch file* and
  of two repo-relative files as the finding's location pointer (a normal audit-report convention, not
  an operational secret) — not a credential, not a leaked deployment detail, and this local-username
  path was itself the audit's own finding about a stray pycache file, not something newly introduced.
  Still worth naming explicitly since the task asked for a targeted local-path grep: **these three
  lines do contain the operator's real local Windows path and username, verbatim, inside a document
  slated for KEEP+COMMIT.** This is low-severity (a username, not a secret) but is a genuine local
  path leaking into what would become a public file if committed as-is, and the primary document's own
  §5 "Local paths: none found" claim is **incorrect** for this specific file — it says "a targeted
  grep for `C:\Users\<name>` and `/home/<user>/` patterns returned zero matches across all 15 files,"
  which does not hold for `E3_FINAL_AUDIT_V2.md` lines 173, 271, 276, 281 (line 173 also contains the
  bare pattern `C:\Users\Maitreya`).

This is the one concrete factual correction this pass makes to the primary document's git-hygiene
section. It does not change the overall verdict on whether to keep the file (the finding itself — a
stray `.pyc` — is legitimate and worth recording), but the local-path strings should be redacted or
paraphrased (e.g., "a leftover compiled-bytecode file under `scratchpad/__pycache__/`" without the
absolute drive path) before this file is committed to a public repository, consistent with this
project's own public/confidential boundary discipline.

No other secret, credential, real company/CUI identifier, or signed-URL pattern was found in any of
the 14 files or in `manuscript/main.tex`.

---

## 8. Accidental artifacts — independently re-run

```
find . -iname "__pycache__" / -iname "*.pyc"  (excluding .git/)
```
finds pycache directories at 7 locations and `.pyc` files at 25 locations, including
`scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc` (the same stray file
`E3_FINAL_AUDIT_V2.md` documents). No `.bak`/`.swp`/`.orig`/`.tmp`/`~` files found anywhere.

Decisive check, run directly rather than inferred from `.gitignore` inspection:
```
git add -A --dry-run
```
returns exactly the 17 expected paths (`manuscript/main.tex` + the 14 untracked `.md` files) and
**nothing else** — no pycache, no `.pyc`, no stray file would be swept into a commit by a broad
`git add -A`. This independently confirms the primary document's §5 conclusion. **No accidental
artifact requiring cleanup; nothing would be accidentally staged.**

---

## 9. Test suite — independently re-run

```
python -m pytest scripts/experiments/exp1/ -q
```
→ **30 passed.** Matches the expected count and every prior checkpoint audit this session.

---

## 10. Would deletion lose evidence? Explicit, per-file answer

**No file in this set is pure disposable scratch debris** — all 14 contain independently-authored
narrative reasoning (verdicts, findings, cross-checks) that could not be regenerated identically by
re-running any script. But "would deletion destroy evidence of a correction or decision" has a real
gradient across the set:

**Would destroy unique evidence of a correction/decision if deleted (do not delete):**
- `research/E3_FINAL_CHECKPOINT_AUDIT.md` — the only record of the exact cross-reference bug (which
  lines, which subsections, why they were wrong).
- `research/E3_FINAL_AUDIT_V2.md` — the only record confirming that fix and closing a separate
  citation slip found along the way.
- `research/E4_ARTIFACT_AUDIT.md` — source of Findings F1-F6, including both findings that blocked
  E4 GREEN.
- `research/E4_SCIENTIFIC_AUDIT.md` — the E4 YELLOW verdict and its full reasoning (Parts A/C/D/H/J/K);
  without it there is no record of *why* E4 wasn't a bare pass.
- `research/E4_RESOLUTION_AUDIT.md` and `research/E4_RESOLUTION_AUDIT_INDEPENDENT.md` — together, the
  only record of the exact F3/F4 before/after wording and its independent confirmation.
- `research/MANUSCRIPT_ARCHITECTURE.md` — cited 10 times from the currently-public `.tex` source;
  deleting it (rather than committing it) would leave those ten citations pointing at nothing.
- `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `research/MANUSCRIPT_FORMAT_RESEARCH.md`,
  `research/PHASE_E_PLAN.md`, `research/PUBLIC_RELEASE_BOUNDARY.md` — each is cited by name from
  `manuscript/main.tex`'s own comments; same reasoning.

**Lower-stakes — losing these would not destroy evidence of a correction (none was found), only
evidence that verification happened:**
- `research/E0_CHECKPOINT_AUDIT.md` — found zero issues; its only content is confirmation that tests
  passed and hygiene was clean at that specific checkpoint. Deleting it loses a data point in the
  "was every gate independently checked" record, not a correction.
- `research/E2_FINAL_CHECKPOINT_AUDIT.md` — found one optional, non-blocking documentation gap.
  Similar profile to the above; the one substantive fact it independently re-confirms (the E2 fixes
  were real) is also stated in `research/MANUSCRIPT_SKELETON_AUDIT.md`'s own resolution, already
  committed.
- `research/MANUSCRIPT_ARCHITECTURE_AUDIT.md` — PASS_WITH_NOTES with two low-severity findings
  (a mis-pointed citation, an already-hedged title risk). Losing it loses the independent
  cross-check of `MANUSCRIPT_ARCHITECTURE.md`, not the architecture document itself.

**A genuine near-miss record, worth calling out specifically:**
- `research/PHASE_E_AUDIT_REPORT.md` — documents a real incident (an audit subagent briefly
  overwrote the frozen `research/AUDIT_REPORT.md` Gate-4 artifact, caught and reverted before
  delivery). This is exactly the class of "evidence of an important correction" the task's own
  instruction protects, even though it's filed as a Class C (no defect *in the audited documents*)
  file. Recommend treating this one as higher-priority-to-keep than its Class C peers, contrary to the
  primary document's flat, undifferentiated treatment of all 14 as equally load-bearing.

**Bottom line:** nothing in the current 14-file set is safe to delete in the sense of "would lose zero
information" — but if the human wants to reduce the volume of committed audit-trail documents,
`E0_CHECKPOINT_AUDIT.md` and `E2_FINAL_CHECKPOINT_AUDIT.md` are the two where the cost of not
committing (losing a "verification happened, nothing was wrong" record) is lowest, and
`MANUSCRIPT_ARCHITECTURE.md` plus the four other Class A files are the ones where NOT committing would
create an active, already-existing citation-to-nowhere defect in the public repository right now.

---

## 11. Verdict

## 🟡 CONDITIONAL

**Justification.** The primary document's classification work is substantively sound: independently
reading all 14 files confirms no duplicate, no scratch debris, no resurrected rejected claim, no
research-integrity violation, and a genuinely accurate account of E4's YELLOW→fix→PASS sequence and
the manuscript's exactly-two-hunk diff. The "no corresponding commit" claim for
`MANUSCRIPT_ARCHITECTURE.md`/`MANUSCRIPT_ARCHITECTURE_AUDIT.md` is independently confirmed via `git
log`, and the citation counts in `manuscript/main.tex` independently corroborate the provenance-gap
argument. Protected artifacts, frozen Experiment 1 evidence, and the test suite (30/30) are all
independently confirmed intact. `RESEARCH_GPS.md`'s staleness is real and independently reproducible
from its own text against the commit log.

This does not round up to a bare PASS for two concrete reasons, both narrow and both fixable without
re-doing any of the underlying classification work:

1. **A factual error in the primary document's own git-hygiene sweep.** Its §5 states "a targeted
   grep for `C:\Users\<name>` and `/home/<user>/` patterns returned zero matches across all 15 files."
   This is false: `research/E3_FINAL_AUDIT_V2.md` contains the operator's real local Windows path and
   username verbatim at four locations (lines 173, 271, 276, 281), inside its own Findings section.
   Low severity (a username, not a secret), but it directly contradicts the primary document's own
   "none found" claim on the exact check the task asked it to run, in a file the document recommends
   committing to a public repository as-is.
2. **A citation-accuracy overstatement.** The primary document states `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`
   is cited in `manuscript/main.tex` "body prose" — it is cited only inside a `%`-comment `% EVIDENCE:`
   block, which the E4 audit's own methodology explicitly treats as a different category from body
   prose (comments never appear in a compiled PDF). Minor, does not change the underlying
   provenance-gap argument, but is an inaccurate characterization of its own evidence.

**Required before this checkpoint's hygiene pass is closed out (both are edits the human, not this
auditor, should make — this pass does not edit anything):**
- Redact or paraphrase the four local-path occurrences in `research/E3_FINAL_AUDIT_V2.md` (lines 173,
  271, 276, 281) before that file is committed to the public repository.
- Correct `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` §5's "Local paths: none found" claim and, if the
  document is to remain the canonical hygiene record, its §6 characterization of the
  `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` citation as "body prose" rather than a development comment.

Everything else in the primary document's classification, verdict, and recommendations is
independently confirmed accurate. No BLOCK-level finding exists: no resurrected rejected claim, no
frozen-evidence modification, no unsafe git state beyond the one local-path leak named above, and no
research-integrity violation in either the manuscript diff or the 14 audit documents themselves.

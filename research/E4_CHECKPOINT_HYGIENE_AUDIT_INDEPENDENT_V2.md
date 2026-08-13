# E4 Checkpoint Hygiene Audit — Independent Challenge Pass, V2

> Independent, from-scratch re-verification of `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` (the
> rewritten/superseding version of the primary session's hygiene pass, produced after the prior
> independent audit `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` returned CONDITIONAL on
> a leaked local path). This pass re-reads every file itself rather than trusting either document's
> summary. Read-only throughout: nothing staged, committed, or pushed; `manuscript/main.tex`,
> `manuscript/references.bib`, `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`,
> `research/contribution_lock.csv`, and all frozen evidence were read only, never modified.
> `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` and `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`
> were both read but not overwritten — the latter is preserved as-is per instruction, as the
> historical record of the original CONDITIONAL finding. Only `python -m pytest` was executed; no
> experiment was run.

---

## 1. Was the E3_FINAL_AUDIT_V2.md redaction done correctly?

**Yes, verified directly.** Read `research/E3_FINAL_AUDIT_V2.md` in full and grepped it independently
for `C:\Users\` and `MaitreyaSapariya`. Exactly one match: line 173, inside prose describing what
grep pattern a prior scan searched for (`` `C:\Users\Maitreya`, `MaitreyaSapariya` `` as a pattern
name, not a value bound to any real path) — read in context, this is unambiguously a description of
a search pattern, not a leaked value; correctly left untouched. Lines 271, 276, 281 (the three
Findings-section location pointers previously containing the operator's real absolute path) now read
`scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc`,
`manuscript/figures/generate_figures.py (no requirements.txt entry)`, and `research/RESEARCH_GPS.md`
respectively — repository-relative, no absolute path, no username. Comparing the surrounding text at
each of the three edit sites against what a pure string-substitution would produce: no other content
changed; the substitutions are minimal, self-contained, and don't alter any finding's substance,
tag, or verdict. **This specific redaction is complete and correct.**

---

## 2. Independent public-release scan — a real problem, not fully closed

Ran an independent scan (not the same grep invocation the primary document used) across all 16
currently-untracked files plus `manuscript/main.tex`, for absolute Windows/Unix paths, the username
`MaitreyaSapariya`, `file://` URLs, AWS key/signed-URL patterns, literal secret/password/API-key/
bearer-token assignments, and email addresses.

**Result: `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` §5's claim "Windows/Unix absolute local paths
... Zero matches across all 17 files (the redaction in §2/§3 closed the only prior instance)" is
false.** Direct grep and direct read-in-context confirm:

- `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` lines 32–34 — its own §2 redaction table's **"Before"**
  column reproduced the exact literal strings that were redacted out of `E3_FINAL_AUDIT_V2.md`,
  verbatim, three times (an absolute path rooted at the operator's home directory, including their
  real username, pointing in turn at the gitignored pycache file, the new figure script, and
  `RESEARCH_GPS.md`). This was a genuine, real occurrence of the operator's local Windows path and
  username in a file this same document proposes for KEEP+COMMIT / public release (§12's staging
  list includes `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` itself).
- `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` (the prior independent audit, preserved
  unedited per this task's instruction, also proposed KEEP+COMMIT in the primary document's own
  §5 table) contained the same literal path pattern at line 266, quoted inside its own explanation
  of the original finding.

Both of these are inside documents that are (a) untracked, (b) explicitly proposed for public commit
in `E4_CHECKPOINT_HYGIENE_AUDIT.md` §12's staging list, and (c) the exact class of artifact the whole
redaction pass exists to make safe. **The redaction fixed the one file it targeted
(`E3_FINAL_AUDIT_V2.md`) but did not fix — and its own closing verification claim incorrectly asserts
it fixed — the fact that the identical leaked string now also lives in the redaction table of the
document performing the fix, and still lives, unredacted, in the preserved independent audit that
first found it.** This is low-severity (a username plus a local folder path, not a credential or
secret — consistent with every prior pass's severity assessment) but it directly falsifies the
specific "zero matches ... across all 17 files" sentence the primary document uses to declare the
scan clean. This is the same class of self-report-vs-reality gap the original CONDITIONAL finding
was about, recurring in the very document written to close it out.

All other categories independently checked and confirmed clean: no `file://` URLs, no AWS/signed-URL
patterns, no literal secret/password/API-key/bearer-token assignments, no email addresses, in any of
the 16 files or `manuscript/main.tex`. The `GROQ_API_KEY=gsk_...` hit in
`research/PUBLIC_RELEASE_BOUNDARY.md` line 13 is confirmed, by direct read, to be prose describing a
pattern a prior scan searched for, not a literal key — correct as claimed.

**Separate, minor, non-blocking observation:** git commit authorship on every commit in this
repository's history is `Maitreya Sapariya <maitreyasapariya@gmail.com>` — real name and real email,
in git metadata, not file content. This is outside the scope of the file-content redaction this pass
was about, and may be entirely intended for a repository the operator plans to publish under their
own name (common for academic preprints/GitHub repos) — flagged only so the human can confirm that's
a deliberate choice, not an oversight, before any public push. Not treated as a finding against this
hygiene pass, since it is git identity, not something any of the audited files control.

---

## 3. Classification table — independent spot-check, 5 files

Read five files in full and independently applied the five-question provenance test, without relying
on the primary document's characterization:

| File | My independent read | Agree with KEEP+COMMIT? |
|---|---|---|
| `research/E0_CHECKPOINT_AUDIT.md` | Contains 12 specific, independently-run verification items (exact test file pass counts, exact grep results, exact diff-emptiness checks) at a specific point in the project's history. No other file states these exact results at this exact checkpoint. | **Yes**, though it is genuinely the weaker of the two flagged files — its content is "verification happened, nothing was wrong," not a discovered defect. |
| `research/E2_FINAL_CHECKPOINT_AUDIT.md` | Ten independently re-verified numbers, a 14-entry bibliography cross-check against the citation ledger, and confirmation of three specific prior fixes (with exact line numbers) — none of this exact content is reproduced verbatim anywhere else. | **Yes**, same caveat as above — genuinely the second-weakest file in the set, but not empty of content. |
| `research/E4_ARTIFACT_AUDIT.md` | A 27-row claim/evidence table (Part B) plus novelty audit (Part E) plus production-case-study audit (Part F) plus independent statistics re-derivation (Part G) — this is the actual evidentiary record of Findings F3/F4, the two REQUIRED NOW findings that blocked E4 GREEN. Deleting it would delete the only record of *why* those two fixes were required. | **Yes, clearly** — this is Class-B-strength material, not a marginal case. |
| `research/PHASE_E_AUDIT_REPORT.md` | Documents a real near-miss: a subagent briefly overwrote the frozen `research/AUDIT_REPORT.md` Gate-4 artifact before being caught and reverted (§1). This is exactly the kind of process-correction evidence that should not be lost, and is nowhere else recorded. | **Yes** — I'd go further than the primary document and call this one of the more load-bearing "found nothing wrong with the audited content, but something real happened during the audit" files in the set. |
| `research/MANUSCRIPT_ARCHITECTURE.md` | Independently grepped `manuscript/main.tex` and confirmed 10 `%`-comment references to this exact filename, none resolvable if the file is not committed. `git log --oneline --all -30 -- research/MANUSCRIPT_ARCHITECTURE.md` returns nothing — confirmed never committed at any point in this repository's history. A live provenance gap exists right now in the tracked tree. | **Yes, clearly** — the strongest case in the set; not committing this file leaves ten dangling internal citations in the currently-public `.tex` source. |

**On the specific question of whether `E0_CHECKPOINT_AUDIT.md` / `E2_FINAL_CHECKPOINT_AUDIT.md`
should be KEEP LOCAL instead:** I independently form the same view the prior independent audit and
the primary document both already state — these two are the weakest-justified pair, their unique-
provenance answer is genuinely "partial, not full," but I do not recommend overturning KEEP+COMMIT
for them. The concrete, content-based reason: both contain specific, timestamped verification detail
(exact test-suite results, exact numeric spot-checks, exact fix confirmations) that a bare "the
build passed" note would not carry, and this project has committed an audit document of this exact
class (found-nothing-wrong-but-verified) at every other checkpoint in its history
(`PAPER_CONTRACT_AUDIT_REPORT.md`, `MANUSCRIPT_SKELETON_AUDIT.md`, four separate E3 audits).
Excluding just these two now, on the basis of "found nothing," would create the only gap in an
otherwise-complete governance record, and a future reader auditing "was every gate actually
independently checked" would not be able to tell whether E0/E2 were skipped or merely not committed.
This is a process-consistency argument, not a strong content argument, and I agree with the prior
audit that the primary document should not present this as equally weighted against the other twelve
files, but the bottom-line KEEP+COMMIT recommendation itself is defensible and I do not overturn it.

---

## 4. Manuscript provenance reference-type claim — independently verified, with one arithmetic note

Grepped `manuscript/main.tex` directly (not from either audit document's summary) for each of the
five filenames:

| File | Occurrences found | All inside `%`-comment lines? |
|---|---|---|
| `MANUSCRIPT_ARCHITECTURE.md` | 10 (lines 6, 41, 45, 85, 124, 455, 511, 902, 1182, 1500) | Yes — every one of the 10 lines begins with `%`. |
| `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` | 2 (lines 12, 430) | Yes — both begin with `%`. |
| `MANUSCRIPT_FORMAT_RESEARCH.md` | 3 (lines 24, 44, 49) | Yes — all three begin with `%`. |
| `PHASE_E_PLAN.md` | 1 (line 849) | Yes. |
| `PUBLIC_RELEASE_BOUNDARY.md` | 2 (lines 850, 1501) | Yes — both begin with `%`. |

**Zero occurrences resolve to `\citep{}`/`\citet{}` (Class A) and zero occurrences sit inside
rendered body-text paragraphs (Class C).** Every single hit is a `%`-prefixed development/provenance
comment (Class B), confirming `E4_CHECKPOINT_HYGIENE_AUDIT.md` §6's core claim and its stated
correction of the prior version's "body prose" mischaracterization of the
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §2.8 reference — independently confirmed at line 430, which sits
in a `% - research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md Sec.4` comment line, not inside the §2.8
paragraph text itself. This correction is accurate.

**Minor, non-blocking arithmetic error found:** `E4_CHECKPOINT_HYGIENE_AUDIT.md` §6's table states
"All **17** occurrences — `MANUSCRIPT_ARCHITECTURE.md` ×10, `MANUSCRIPT_FORMAT_RESEARCH.md` ×3,
`PUBLIC_RELEASE_BOUNDARY.md` ×2, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` ×2, `PHASE_E_PLAN.md` ×1." The
listed per-file breakdown sums to 10+3+2+2+1 = **18**, not 17, and my independent count (above) also
totals 18. The per-file counts are individually correct; only the stated total is off by one. Does
not change the substance of the claim (all Class B, zero Class A/C) but is exactly the kind of
self-report arithmetic slip worth naming.

---

## 5. Protected-artifact and frozen-evidence integrity — independently re-run

```
git diff --stat HEAD -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md research/contribution_lock.csv manuscript/references.bib TECHNICAL_REPORT.md README.md METHODOLOGY.md
```
→ **empty.**

```
git diff 6fb6188 -- data/outputs/experiments/exp1/final/
```
→ **empty.** Frozen Experiment 1 evidence byte-identical to the freeze commit.

```
git diff --stat 95c2b18 -- manuscript/main.tex
```
→ `1 file changed, 9 insertions(+), 5 deletions(-)`. Read the full diff directly: exactly two
hunks, matching the already-approved E4.1 corrections —

- §4.2 (~line 600–606): the 0.695 cross-company-alignment sentence now carries "cited from a
  confidential engagement and not independently reproducible from this repository" (F3).
- §1.1 (~lines 100–106): the 87.56% synthetic figure is now explicitly named as selecting
  `EMBEDDING_PRIMARY`, a different mechanism from the `retrieval` mechanism Experiment 1 actually
  tests, with an explicit "no embedding-based mechanism is evaluated anywhere in this paper" (F4).

Independently grepped and confirmed both outside these two hunks:
- `PARTIALLY~SUPPORTED` — present at lines 817–819, stated as the H1 verdict, matching the
  pre-registered falsification table.
- The Formulation #2 synthesis sentence ("...ranking is governed by a [representation-stability
  property]...") — present at line 1154, unchanged.

**All protected artifacts and manuscript-integrity claims confirmed intact and accurate.**

---

## 6. Test suite — independently re-run

```
python -m pytest scripts/experiments/exp1/ -q
```
→ **30 passed in 8.35s.** Matches the expected count.

---

## 7. Assessment of the proposed checkpoint (Section 12's staging list)

**The 16-file (+2, counting this document and its predecessor) staging list is not excessive
hoarding.** Every file independently spot-checked (five files, §3 above) contains content that is
not reproduced verbatim elsewhere and that a future reader reconstructing "what happened during
Phase E, and why" would lose if the file were dropped. The project's own established pattern —
committing exactly this class of audit-trail document at every prior checkpoint (E0, E2, E3 each
committed 4–6 audit/planning documents alongside the substantive change) — supports treating this
set the same way rather than introducing a new, unexplained exception now. I do not recommend
trimming the list.

**However, the list is not safe to stage as currently written**, for the concrete reason in §2
above: two of the files on it (`research/E4_CHECKPOINT_HYGIENE_AUDIT.md` and
`research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`) still contain the operator's real local
Windows path and username, verbatim, and the primary document's own closing "public-release scan:
clean" declaration is incorrect on this exact point. Staging the list as-is would commit that leak
into the public history. This is the one concrete blocker; nothing else found in this pass requires
a change to the proposed list, its members, or the underlying redaction/classification work.

---

## 8. Verdict

## 🟠 CONDITIONAL

**Justification.** The redaction of `research/E3_FINAL_AUDIT_V2.md` itself is complete and correct —
independently re-verified by direct read and grep, with the one remaining `C:\Users\Maitreya` hit at
line 173 confirmed to be a pattern-description false positive, not a leak. The classification table
is independently confirmed sound on all five spot-checked files, including the two files the primary
document itself flags as weakest (`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`) — I do
not recommend reclassifying either to KEEP LOCAL. The manuscript-provenance Class-B claim is
independently confirmed exactly as stated (all 18 — not 17, a minor arithmetic slip — occurrences
are `%`-comments, none are academic citations or body prose). Protected artifacts, frozen Experiment
1 evidence, H1's PARTIALLY_SUPPORTED status, the Formulation #2 synthesis sentence, and the exact
two-hunk/9-insertion/5-deletion manuscript diff are all independently confirmed intact and accurately
described. The test suite passes 30/30.

This does not round up to PASS because the primary document's own closing public-release-safety
claim — "Windows/Unix absolute local paths ... Zero matches across all 17 files" — is factually
false, independently disproven by direct grep: the exact local path and username the redaction pass
was created to remove is still present, verbatim, inside `research/E4_CHECKPOINT_HYGIENE_AUDIT.md`'s
own §2 redaction table (the "Before" column, lines 32–34) and inside
`research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` (line 266, the preserved historical record).
Both files are proposed for KEEP+COMMIT and appear on the Section 12 staging list. This is low
severity — a username and local folder path, not a credential or secret, consistent with every prior
pass's severity read — but it is a concrete, actionable, unresolved instance of exactly the category
of leak this entire hygiene pass exists to close out, and the document's own verification section
currently asserts the opposite of what a direct scan shows.

**Required before this checkpoint's hygiene pass is closed out** (both are edits for the human/
builder to make, not this auditor — this pass changes nothing):
1. Paraphrase or otherwise remove the literal absolute-path strings in
   `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` §2's redaction table (lines 32–34), e.g. by showing only
   the relative suffix (`...\scratchpad\__pycache__\staged_generate_figures.cpython-314.pyc`) or a
   generic placeholder for the "Before" column, and correct §5/§7's "zero matches" / "clean" claims
   to acknowledge this once fixed.
2. Decide, and document the decision, on `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` line
   266: either accept that this specific historical-record file will carry the literal path into the
   public repository (a defensible choice, since it is explicitly a preserved record of a past
   finding — but then §12's "public-release scan: clean" statement in the newer document needs to
   name this as a known, accepted exception rather than an absence), or have the human apply the same
   kind of relative-path paraphrase to it that was applied to `E3_FINAL_AUDIT_V2.md`, understanding
   that doing so slightly alters the literal wording of a document this task described as needing to
   stay "as-is."
3. Optional, non-blocking: correct the "17" vs. actual-18 arithmetic in
   `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` §6's occurrence-count table.

No BLOCK-level issue exists: no credential or secret was found, no resurrected rejected claim, no
frozen-evidence modification, no unsafe git state beyond the one local-path leak named above, and no
research-integrity or manuscript-integrity violation in either the manuscript diff or the audit
documents themselves.

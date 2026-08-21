# E4 Checkpoint — Final Independent Staging Audit (Third-Pass, From Scratch)

> Fully independent, read-only, from-scratch re-verification of the exactly-19-file staged
> checkpoint (`manuscript/main.tex` + 18 `research/*.md` files). Does not trust any prior audit's
> summary — every claim below was re-derived by exporting the exact staged blob content via
> `git show ":<path>"` into a scratch directory and grepping/reading that export directly, not the
> working tree. Nothing staged, unstaged, committed, pushed, or modified. No experiment was run;
> only `python -m pytest` was executed. This report is a new file and was not staged by this pass.

---

## 1. The critical check — reproduced local-path leak

Exported the exact staged content of all 19 files (`git show :<path>`) to a scratch directory and
grepped that export (not the working tree) for `C:\Users\` + `Maitreya`/`MaitreyaSapariya`,
case-insensitively, plus broader variants (`(?i)maitreya`, `(?i)sapariya`, `Desktop\personal`,
`AppData\Local`, `C:\Users\[A-Za-z]+\`).

**Result: only 4 of the 19 files contain the string "maitreya" in any form, and every single match
is pattern-description prose, not a reproduced absolute path.** Confirmed by direct read of each
hit in context:

- `research/E3_FINAL_AUDIT_V2.md:173` — prose describing the grep pattern a prior scan searched
  for. The three previously-leaked lines (271, 276, 281) were independently re-read in full and now
  contain only repo-relative paths (`scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc`,
  `manuscript/figures/generate_figures.py`, `research/RESEARCH_GPS.md`) — no home-directory prefix,
  no username.
- `research/E4_CHECKPOINT_HYGIENE_AUDIT.md:20,53,326` — all three are pattern-description prose
  (backtick-quoted search-pattern names). The "Before" column at line ~32 (the table documenting the
  E3_FINAL_AUDIT_V2.md redaction) now *describes* the removed content ("An absolute local Windows
  path rooted at the operator's home directory (including their real username), pointing at...")
  instead of quoting it — confirmed by direct read of lines 25-44.
- `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md:260,278` — same pattern-description form.
  The narrative at lines 265-278 that originally reproduced the leaked path verbatim now describes
  it in prose ("the literal local Windows path (an absolute path rooted at the operator's home
  directory, including their real username)") — confirmed by direct read.
- `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:20,21,38,76,216` — all pattern-description
  prose or the git-metadata email note (see below); none is a reproduced file-content path.

A broader sweep for `/home/[a-zA-Z]+/` and `C:\Users\[A-Za-z]+\` (i.e., a username followed by a
continuing path separator, which any *real* leaked path would have) returned **zero matches across
all 19 files** — consistent with there being no actual reproduced absolute path anywhere in the
staged content, only bare pattern-name mentions.

**Verdict on this check: PASS. Zero actual reproduced absolute paths remain. The third redaction
round closed the issue.**

## 2. Full public-release scan (independent, all 19 files)

Grepped the same export for: AWS key patterns (`AKIA...`), `aws_secret`, `X-Amz-`, `s3://`,
`amazonaws.com`, bearer-token assignments, `api_key=`/`password=`/`secret=` assignments, PEM/RSA/
OpenSSH/PGP private-key headers, GitHub/OpenAI-style token prefixes (`ghp_`, `sk-`), `file://` URLs,
email-address syntax, and real Romanian company/CUI identifiers (`Rompetrol`, `OMV Petrom`, `CUI`/
`CIF` + digit patterns).

- **Zero actual credentials, secrets, keys, or tokens found.** The only "hits" are: (a) prose
  describing what a prior scan searched for (`GROQ_API_KEY=gsk_...` in
  `PUBLIC_RELEASE_BOUNDARY.md:13` and echoed in `E4_CHECKPOINT_HYGIENE_AUDIT.md:188` — both
  confirmed by direct read to be a pattern description, not a literal key), and (b) the string
  `s3://` inside a documented f-string template in `PHASE_E_AUDIT_REPORT.md:145-146`
  (`s3_uri = f"s3://{bucket}/{key}"`), not a hardcoded bucket or credential.
- **Zero `file://` URLs.**
- **Zero real company names or CUI/CIF identifiers.** The only matches are `Rompetrol`/`OMV Petrom`
  inside `PUBLIC_RELEASE_BOUNDARY.md:14`, itself describing what pattern a safety sweep searched
  for (confirmed by direct read of surrounding context — this is the audit document naming the
  patterns it checked, not data output).
- **One email match**, in `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:76`: `Maitreya Sapariya
  <maitreyasapariya@gmail.com>`, in a sentence explicitly noting this is git commit-author metadata
  ("real name and real email, in git metadata, not file content... may be entirely intended for a
  repository the operator plans to publish under their own name"). This matches the out-of-scope
  note in the task brief exactly — git authorship on every commit already carries the operator's
  real name/email, independent of file content, and is not a new file-content leak. **Confirmed,
  not re-flagged.**

**Verdict on this check: PASS.**

## 3. Provenance completeness

Cross-referenced the staged 18 `research/*.md` files against `research/E4_CHECKPOINT_HYGIENE_AUDIT.md`'s
own KEEP+COMMIT classification table (§ around line 107-123): 15 originally-classified files
(`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`, `E3_FINAL_CHECKPOINT_AUDIT.md`,
`E3_FINAL_AUDIT_V2.md`, `E4_ARTIFACT_AUDIT.md`, `E4_RESOLUTION_AUDIT.md`,
`E4_RESOLUTION_AUDIT_INDEPENDENT.md`, `E4_SCIENTIFIC_AUDIT.md`, `MANUSCRIPT_ARCHITECTURE.md`,
`MANUSCRIPT_ARCHITECTURE_AUDIT.md`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`,
`MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_AUDIT_REPORT.md`, `PHASE_E_PLAN.md`,
`PUBLIC_RELEASE_BOUNDARY.md`) plus the two hygiene-pass documents themselves
(`E4_CHECKPOINT_HYGIENE_AUDIT.md`, `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`) = 17, plus the
legitimate new addition `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md` = 18. This matches exactly
the 18 staged research files. **Nothing from the agreed set is missing; nothing unexplained is
present.**

`E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md` is a reasonable inclusion, not scope creep: it is
the second independent audit's own report, documenting a real defect it found (the leak-reproduction
error in two other staged files) and the subsequent fix. This is the same class of document as
`E3_FINAL_AUDIT_V2.md` and `E4_RESOLUTION_AUDIT_INDEPENDENT.md` — an audit-trail record of a real
correction, consistent with this project's established pattern of committing this class of document
at every prior checkpoint (E0, E2, E3 each committed 4-6 audit/planning documents alongside
substantive changes, per `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:196-197`).

`git status --porcelain --untracked-files=all` shows **zero files outside the 19 staged ones** —
no leftover untracked debris, no orphaned draft of a fourth audit round.

**Verdict on this check: PASS.**

## 4. Manuscript integrity

`git diff --cached --stat -- manuscript/main.tex` → `1 file changed, 9 insertions(+), 5 deletions(-)`,
exactly as claimed. Read the full diff directly:

- **Hunk 1** (Introduction, §1.1 "Real-world motivation", around line 100-108): replaces "the same
  rule selected a retrieval-based mechanism instead" with "the same rule selected its
  embedding-based branch (`EMBEDDING_PRIMARY`) instead -- a different mechanism from the
  lexical-similarity `retrieval` mechanism this paper's Experiment 1 tests (Section 3.4); no
  embedding-based mechanism is evaluated anywhere in this paper." This is F4 (EMBEDDING_PRIMARY
  terminology correction), confirmed present and correctly worded.
- **Hunk 2** (Experimental Design, §3.2 "Synthetic Generator", around line 600-606): adds "-- the
  production-observed value, cited from a confidential engagement and not independently
  reproducible from this repository --" as a qualifier on the 0.695 cross-company-alignment figure.
  This is F3 (confidentiality qualifier), confirmed present and correctly worded. (The task brief's
  label "section 4.2" does not match this section's actual numbering — it is in §3, "Experimental
  Design" — but the diff *content* is exactly as described; this is a labeling mismatch in the task
  prompt, not a defect in the staged file.)
- **H1 status**: confirmed `\subsection{H1 Only Partially Supported}` (line 1380) and body text "H1
  (revised) is only partially supported, matching the pre-registered..." (line 1382) and "H1 overall
  is only partially supported, not confirmed" (line 1468) — stated as PARTIALLY_SUPPORTED throughout,
  not upgraded.
- **Formulation #2 synthesis sentence**: not touched by either hunk (both hunks are confined to
  §1.1 and §3.2; the synthesis sentence lives in §6 Discussion, untouched in this diff).
- **6a/6b separation**: confirmed intact via distinct `%` comment markers at lines 934 (`(6a)`) and
  969 (`(6b)`) — not merged.
- **No production number in Results**: located the `\section{Results}` boundary (line 895) through
  `\section{Discussion}` (line 1147) and confirmed none of `91.2`, `87.56`, or `0.695` appear inside
  that range. All three occurrences are outside Results: `91.2`/`87.56` in Introduction §1.1
  (lines 100, 103) and Limitations §7.6 "Production Confidentiality" (line 1344, citing back to
  §1.1); `0.695` in Experimental Design §3.2 (line 603).

**Verdict on this check: PASS.**

## 5. Frozen evidence and protected files

- `git diff 6fb6188 -- data/outputs/experiments/exp1/final/` → **empty**. Frozen Experiment 1
  evidence is byte-identical to the Phase D freeze commit.
- `git diff --cached --name-only | grep -iE "PAPER_CONTRACT|CONTRIBUTION_LOCK|contribution_lock\.csv|references\.bib|TECHNICAL_REPORT\.md|README\.md|METHODOLOGY\.md"` → **no match** (grep exit 1).
- `git status --porcelain` on those same seven paths (staged or unstaged) → **empty**. None of
  `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, `research/contribution_lock.csv`,
  `manuscript/references.bib`, `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md` are staged,
  modified, or touched in any way.

**Verdict on this check: PASS.**

## 6. No accidental artifacts

`git diff --cached --name-only | grep -iE "__pycache__|\.pyc$|\.bak$|\.swp$|\.orig$|\.tmp$|scratchpad"`
→ no match. Full `git status --porcelain` output lists **exactly** the 19 expected files (18 `A`,
1 `M`) and nothing else — no cache directories, no compiled bytecode, no editor temp files staged.

**Verdict on this check: PASS.**

## 7. Test suite

`python -m pytest scripts/experiments/exp1/ -q` → **30 passed in 18.71s**. Matches the expected
30/30 count.

## 8. E4 checkpoint completeness

Taken as a whole, the 19 staged files form a coherent, chronologically legible record of Phase E4
(adversarial audit) through E4.1 (corrections) through this session's hygiene/redaction pass:
`E4_ARTIFACT_AUDIT.md` and `E4_SCIENTIFIC_AUDIT.md` establish the original E4 findings (F1-F6,
including F3/F4 that blocked a clean pass); `E4_RESOLUTION_AUDIT.md` and
`E4_RESOLUTION_AUDIT_INDEPENDENT.md` document the F3/F4 fix and its independent confirmation;
`E4_CHECKPOINT_HYGIENE_AUDIT.md`, `_INDEPENDENT.md`, and `_INDEPENDENT_V2.md` document three
successive rounds of the redaction saga (leak found → redacted → redaction itself found to have
leaked into two other files → re-redacted → independently re-verified clean, which is what this
report itself is the fourth link in); `PUBLIC_RELEASE_BOUNDARY.md` defines the public/confidential
boundary the whole pass operates under; the `MANUSCRIPT_ARCHITECTURE*`, `MANUSCRIPT_FORMAT_RESEARCH.md`,
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PHASE_E_PLAN.md`, and earlier `E0`/`E2`/`E3` checkpoint audits
supply the manuscript-drafting provenance trail that `manuscript/main.tex`'s own internal `%`
comments cite 18 times (independently recounted, matching the corrected figure in
`E4_CHECKPOINT_HYGIENE_AUDIT.md` §11 point 2). No gap was found: every file either supplies unique
provenance not reproduced elsewhere, or documents a real correction in the audit process itself.

**One informational note, not a defect:** `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md`, as
staged, states its own verdict as `CONDITIONAL` (§8, referencing the leak in
`E4_CHECKPOINT_HYGIENE_AUDIT.md` and `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` that existed at
the time that document was written). Per this repo's established convention of preserving
audit-trail documents as historical records rather than silently rewriting them after their finding
is fixed (the same pattern already applied to `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`'s
preserved CONDITIONAL verdict about `E3_FINAL_AUDIT_V2.md`), this is intentional and expected — the
fix was applied and independently re-verified (by this very pass, §1 above) *after* that document
was finalized, in the two files it named, not in itself. A future reader should not mistake this
document's own `CONDITIONAL` verdict field for the current state of the repository; the current
state is clean, as directly re-verified in §1-2 of this report. Not a blocking issue.

---

## Summary of findings

No REQUIRED NOW findings. All eight checks independently re-verified from the exact staged blob
content, not from any prior audit's narrative.

One OPTIONAL/INFORMATIONAL note (not blocking): the stale-by-design `CONDITIONAL` verdict field
preserved inside `E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md` (§8 of that file) no longer
reflects the current (now-clean) state of the two files it names — this is expected given this
project's audit-trail-preservation convention, but worth flagging so a human skimming verdict
fields in isolation doesn't misread it as an open blocker.

---

## Final Verdict: PASS

This staged checkpoint (19 files: `manuscript/main.tex` + 18 `research/*.md` audit/planning
documents) is safe to commit as-is. The critical local-path leak that took three rounds to close is
independently confirmed closed — zero actual reproduced absolute paths remain anywhere in the exact
staged content, verified via direct export of `git show ":<path>"` blobs and multiple independent
grep sweeps, not by trusting any prior pass's self-report. The full public-release scan found no
credentials, secrets, keys, tokens, real company/CUI data, or `file://` URLs. Provenance is
complete: no agreed file is missing, nothing unexplained is present, and the one new addition
(`E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md`) is a legitimate audit-trail record, not scope
creep. The manuscript diff is exactly the two pre-approved E4.1 hunks (9/5), H1 remains
PARTIALLY_SUPPORTED, Formulation #2's synthesis sentence and the 6a/6b separation are untouched, and
no production number leaks into the Results section. Frozen Experiment 1 evidence and all seven
protected files are byte-unchanged. No accidental artifacts are staged. The test suite passes
30/30.

# E4 Checkpoint — Repository Hygiene, Public-Release Review, and Checkpoint Plan

> Read-only classification, redaction, and hygiene pass. Supersedes the prior version of this same
> file (which reached CONDITIONAL) after applying the one required redaction that verdict named.
> Does not stage, commit, or push anything. Does not modify `manuscript/main.tex` beyond what was
> already approved at E4.1, `manuscript/references.bib`, any frozen evidence,
> `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, or `research/contribution_lock.csv`.
> Does not run experiments, generate figures, compress sections, or begin E5.

---

## 1. Original finding

The prior independent audit of this same hygiene pass (`research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`,
verdict CONDITIONAL) found that `research/E3_FINAL_AUDIT_V2.md` contained the operator's real local
Windows path and username, verbatim, at three locations (its own §14 Findings list, lines 271, 276,
281), and that the prior version of this document's own git-hygiene section incorrectly claimed
"local paths: none found... across all 15 files." A fourth location (line 173) was correctly
identified by that same audit as a false positive — it is prose *describing* the grep pattern a
prior scan searched for (`` `C:\Users\Maitreya`, `MaitreyaSapariya` ``), not a leaked value, and was
correctly left untouched.

---

## 2. Redaction performed

Three absolute local-path strings in `research/E3_FINAL_AUDIT_V2.md` §14 were replaced with
repository-relative paths, with no other change to surrounding content:

| Line | Before (redacted here — see note) | After |
|---|---|---|
| 271 | An absolute local Windows path rooted at the operator's home directory (including their real username), pointing at `scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc` | `` `scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc` `` |
| 276 | Same absolute-path pattern, pointing at `manuscript/figures/generate_figures.py` (no requirements.txt entry) | `` `manuscript/figures/generate_figures.py` (no requirements.txt entry) `` |
| 281 | Same absolute-path pattern, pointing at `research/RESEARCH_GPS.md` | `` `research/RESEARCH_GPS.md` `` |

**Note:** the "Before" values above are described, not quoted verbatim, precisely so that this
document itself — proposed for public commit — does not reproduce the same local-path/username
string it documents the removal of. (An earlier version of this table quoted the un-redacted strings
directly; that was itself a leak-reproduction error, caught by a second independent audit pass and
fixed here — see §11.)

Line 173 (the grep-pattern description inside that document's own §7/§10-style methodology prose)
was left unchanged — it is not a leak, and altering it would misrepresent what pattern that audit
pass actually searched for.

---

## 3. Verification of redaction

- Direct re-read of `research/E3_FINAL_AUDIT_V2.md` lines 265–284 confirms exactly the three
  intended substitutions, nothing else in the file altered (three targeted `Edit` operations, each
  matched on unique surrounding text).
- `grep -n "C:\\Users\\Maitreya|MaitreyaSapariya" research/E3_FINAL_AUDIT_V2.md` → **one remaining
  match, line 173 only** (the correctly-preserved pattern-description false positive). **Zero actual
  local Windows paths or usernames remain.**
- A combined fresh scan (Windows/Unix absolute paths, `file://` URLs, AWS key patterns, signed-URL
  patterns, literal secret/password/token/API-key assignments, email addresses) run across
  **all 16 currently-untracked files plus `manuscript/main.tex`** (§7 below) found no credential or
  secret introduced by, or remaining after, this redaction.
- No scientific/audit content was altered — the redaction touched only the three absolute-path
  strings, which existed purely as location-pointers inside Findings entries, not as part of any
  claim, verdict, or numerical statement.

---

## 4. Complete file inventory (fresh, post-redaction)

`git status --short --untracked-files=all`:

```
 M manuscript/main.tex
?? research/E0_CHECKPOINT_AUDIT.md
?? research/E2_FINAL_CHECKPOINT_AUDIT.md
?? research/E3_FINAL_AUDIT_V2.md
?? research/E3_FINAL_CHECKPOINT_AUDIT.md
?? research/E4_ARTIFACT_AUDIT.md
?? research/E4_CHECKPOINT_HYGIENE_AUDIT.md
?? research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md
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

16 untracked files (14 from the prior pass, plus this document and its independent companion, both
newly created by the prior hygiene pass) + the one tracked modification (`manuscript/main.tex`, the
already-approved E4.1 fixes, unchanged since the last checkpoint).

---

## 5. Classification table (with the 5-question provenance test)

For every file proposed KEEP+COMMIT: (1) unique methodological/scientific provenance? (2) referenced
by another permanent research artifact? (3) documents a decision/correction/audit/evidence
interpretation a future researcher may need? (4) superseded by a later canonical document? (5) would
deletion lose unreconstructable information? Same five questions answered for every other
recommendation.

| Path | Class | (1) Unique provenance | (2) Referenced elsewhere | (3) Documents a decision/correction | (4) Superseded | (5) Unreconstructable if deleted |
|---|---|---|---|---|---|---|
| `research/E0_CHECKPOINT_AUDIT.md` | **KEEP + COMMIT** | Partial — the 2 fixes it confirms are also noted in the already-committed `PAPER_CONTRACT_AUDIT_REPORT.md` resolution note, but the test-suite/frozen-evidence/git-hygiene/public-safety verification is unique to this document | No | Confirms, not discovers, a correction | No | Yes, for the independent test/hygiene verification specifically |
| `research/E2_FINAL_CHECKPOINT_AUDIT.md` | **KEEP + COMMIT** | Yes — 10 independently spot-checked numbers, 14-entry bib cross-check, 17-item checklist not present elsewhere | No | Confirms 3 fixes (1 required, 2 optional) from the already-committed `MANUSCRIPT_SKELETON_AUDIT.md` | No | Yes, for the independent numerical re-derivation specifically |
| `research/E3_FINAL_CHECKPOINT_AUDIT.md` | **KEEP + COMMIT** | Yes — sole record of 3 real cross-reference defects (exact lines, exact subsections) | No | **Yes — discovers** the defect later fixed in the committed manuscript | No, this *is* the original discovery | Yes — no other file states what the bug actually was |
| `research/E3_FINAL_AUDIT_V2.md` | **KEEP + COMMIT** *(now redacted, ready)* | Yes — sole confirmation the 3 fixes landed correctly, plus a separately-caught citation slip | No | Confirms the correction found above | No | Yes |
| `research/E4_ARTIFACT_AUDIT.md` | **KEEP + COMMIT** | Yes — 27-claim evidence table, novelty audit, 6th independent statistics re-derivation; source of Findings F1–F6 (including the two that blocked E4 GREEN) | Referenced by `research/E4_SCIENTIFIC_AUDIT.md` and this document | **Yes — discovers** F3/F4 | No, original discovery | Yes — the evidentiary backbone of why E4 wasn't a rubber-stamp |
| `research/E4_RESOLUTION_AUDIT.md` | **KEEP + COMMIT** | Yes — the only before/after wording record for the F3/F4 fix | Referenced by this document | Documents the correction itself | No | Yes |
| `research/E4_RESOLUTION_AUDIT_INDEPENDENT.md` | **KEEP + COMMIT** | Yes — independent re-derivation confirming the fix, plus 2 precision corrections to the resolution audit's own self-report | Referenced by this document | Confirms the correction | No | Yes |
| `research/E4_SCIENTIFIC_AUDIT.md` | **KEEP + COMMIT** | Yes — the literary/logic/H1/figure/writing/stress-test review (Parts A,C,D,H,J,K) found nowhere else | Referenced by `research/E4_ARTIFACT_AUDIT.md` (companion) | The E4 YELLOW verdict and its full reasoning | No | Yes — without it there is no record of *why* E4 wasn't a bare pass |
| `research/MANUSCRIPT_ARCHITECTURE.md` | **KEEP + COMMIT** | Yes — the entire E1 section/claim/evidence architecture | **Yes — cited 10 times by `manuscript/main.tex`'s own internal `%` comments** (see §6) | Documents the E1 architectural decisions the committed manuscript implements | No — never committed at all (see §6) | Yes, severely |
| `research/MANUSCRIPT_ARCHITECTURE_AUDIT.md` | **KEEP + COMMIT** | Yes — independent audit of the above (2 findings) | No | Confirms the E1 architecture is sound | No | Yes, for the independent cross-check |
| `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` | **KEEP + COMMIT** | Yes — the E0 claim-to-evidence mapping and classification (SUPPORTED/INFERRED/CASE_STUDY/etc.) | **Yes — cited by `manuscript/main.tex`'s internal `%` comments** (2 occurrences, §6) | Documents the E0 evidence-mapping decision | No | Yes |
| `research/MANUSCRIPT_FORMAT_RESEARCH.md` | **KEEP + COMMIT** | Yes — live-verified arXiv submission requirements and the LaTeX-template decision rationale | **Yes — cited by `manuscript/main.tex`'s internal `%` comments** (3 occurrences, §6) | Documents the E0 format decision | No | Yes |
| `research/PHASE_E_AUDIT_REPORT.md` | **KEEP + COMMIT** | Yes — sole record of a real near-miss (an audit subagent briefly overwrote the frozen `research/AUDIT_REPORT.md`, caught and reverted) | No | **Yes — documents a real process correction**, not merely a clean-pass confirmation | No | Yes — this specific incident and its resolution exist nowhere else |
| `research/PHASE_E_PLAN.md` | **KEEP + COMMIT** | Yes — manuscript structure, reproducibility tiers, figure/table plan, Phase E milestone definitions | **Yes — cited by `manuscript/main.tex`'s internal `%` comments** (1 occurrence, §6) | Documents the E0 planning decisions | No | Yes |
| `research/PUBLIC_RELEASE_BOUNDARY.md` | **KEEP + COMMIT** | Yes — the actual public/confidential boundary definition and direct repo safety sweep | **Yes — cited by `manuscript/main.tex`'s internal `%` comments** (2 occurrences, §6) | Documents what may/may not enter the public arXiv package | No | Yes |
| `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` (this file) | **KEEP + COMMIT** | Yes — this pass's own classification, redaction, and provenance work | N/A (newly created) | Documents this hygiene decision | Supersedes its own prior version (see header) | Yes |
| `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` | **KEEP + COMMIT** | Yes — the independent challenge that found the redaction requirement and other precision gaps | Referenced by this document | Documents the correction this pass applied | No | Yes |

**No file classified KEEP LOCAL, ARCHIVE/CONSOLIDATE, or DELETE.** Applying the five-question test
individually to every file, none fails questions (1), (3), or (5) — every file contains
non-duplicated content, documents or confirms a real decision, and cannot be reconstructed by
re-running any script. This is not "commit everything by default": each row above shows the actual
per-file reasoning, and two files (`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`) are
explicitly flagged as the *weakest*-justified pair — their unique-provenance answer is "partial," not
"yes" — while still landing on KEEP + COMMIT for the process-consistency reason given in §6 of the
prior version of this document (this project has, without exception, committed exactly this class of
pre-stage gate audit at every prior checkpoint; excluding just these two now would create an
unexplained gap in an otherwise-uniform governance record, not a content-driven reason to keep them
equally weighted against the other fourteen).

---

## 6. Manuscript provenance check (`manuscript/main.tex` references, by type)

Grepped `manuscript/main.tex` for every one of the five Class-A planning documents' filenames and
classified each hit:

| Reference type | Definition | Count found |
|---|---|---|
| **A. Reader-visible academic citations** | `\citep{}`/`\citet{}` calls resolving to `manuscript/references.bib` | **0** for any of the five planning documents — the paper's only reader-visible citations are its 14 literature entries (`rice1976`, `smithmiles2009`, etc.), which are unaffected by anything in this pass |
| **B. Internal `% EVIDENCE` / provenance comments** | `%`-prefixed lines, never rendered in a compiled PDF, used throughout this project as the audit-trail mechanism (`% EVIDENCE:` blocks, header-comment governance chain) | **All 18 occurrences** — `MANUSCRIPT_ARCHITECTURE.md` ×10, `MANUSCRIPT_FORMAT_RESEARCH.md` ×3, `PUBLIC_RELEASE_BOUNDARY.md` ×2, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` ×2, `PHASE_E_PLAN.md` ×1 |
| **C. Ordinary prose references** | Mentions of a filename inside actual paragraph text a PDF reader would see | **0** — confirmed by direct line-by-line inspection; every hit's line begins with `%` |

**Correction to this document's own prior version:** the prior version characterized
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`'s §2.8 reference as appearing in "body prose." Direct re-inspection
confirms this is **incorrect** — the reference sits in the `% EVIDENCE:` comment block immediately
following the §2.8 paragraph, not inside the paragraph itself. It is Class B, like every other
occurrence. This does **not** mean the reference is a "broken academic citation" — it was never an
academic citation in the first place (Class A), so that framing does not apply. It is, precisely, an
internal provenance/evidence-anchor comment, exactly the mechanism this project has used
consistently since Phase E0 to make every claim in `main.tex` traceable to a named source document.

**Does `MANUSCRIPT_ARCHITECTURE.md`'s presence in the repository matter, given its only references
are internal comments (Class B), never Class A or C?** Yes, for a reason distinct from "broken
citation": this repository is a **public** research repository whose own stated design goal (per
`PUBLIC_RELEASE_BOUNDARY.md` and `research/PHASE_E_PLAN.md`'s reproducibility tiers) is that a reader
can inspect the `.tex` **source**, not merely the compiled PDF. A reader doing exactly that — opening
`manuscript/main.tex` in the public GitHub repository, which is a normal and expected action for a
repository explicitly built around source-level auditability — would see `main.tex`'s own header
comment naming `research/MANUSCRIPT_ARCHITECTURE.md` as one link in its documented authority chain
("Governed by, in this order of authority: ... > `research/MANUSCRIPT_ARCHITECTURE.md` (E1
architecture) > ...") and find that file absent from the repository entirely. This is a **provenance
completeness gap in a source-transparency sense**, not a citation-integrity defect in the
academic-paper sense — the distinction the task asked this pass to preserve. The same reasoning
applies, with lower multiplicity (1–3 references each), to `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`,
`MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_PLAN.md`, and `PUBLIC_RELEASE_BOUNDARY.md`.

---

## 7. Public-release scan (fresh, post-redaction, all 16 untracked files + `manuscript/main.tex`)

Ran targeted greps (not just keyword occurrence checks — every match was opened and read in context)
for: Windows absolute paths, usernames, home directories, `file://` URLs, AWS access-key patterns,
literal API-key/secret/password/bearer-token assignments, signed-URL query parameters, email
addresses, and local-machine metadata.

| Check | Result |
|---|---|
| Windows/Unix absolute local paths (`C:\Users\<name>`, `/home/<user>/`, `/Users/<name>/`) | **Zero matches** across all 17 files (the redaction in §2/§3 closed the only prior instance) |
| `file://` URLs | Zero matches |
| AWS access-key patterns (`AKIA...`), signed-URL patterns (`X-Amz-Signature`, `amazonaws.com/...Signature`) | Zero matches |
| Literal secret/password/API-key/bearer-token assignments | One surface hit, inspected and confirmed a false positive: `research/PUBLIC_RELEASE_BOUNDARY.md` line 13, `` `GROQ_API_KEY=gsk_...` `` — this is prose *describing the pattern a prior safety scan searched for* (an environment-variable name plus its expected literal-key prefix format), not an actual key value. Consistent with the same false positive independently confirmed by two prior audits this session. |
| Email addresses | Zero matches |
| Real company/CUI identifiers | Not re-scanned in this pass (already independently confirmed clean twice this session — `research/PHASE_E_AUDIT_REPORT.md` §10, `research/PUBLIC_RELEASE_BOUNDARY.md` itself); no new file in this inventory introduces production/company data of any kind |

**Public-release scan: clean.** No credential, secret, signed URL, real local path, username, or
personal identifier remains in any of the 16 untracked files or in `manuscript/main.tex` as they
currently stand.

---

## 8. Protected-artifact verification

- `git diff --stat HEAD -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md research/contribution_lock.csv manuscript/references.bib TECHNICAL_REPORT.md README.md METHODOLOGY.md`
  → **empty**. All seven confirmed byte-unchanged since `HEAD` (`95c2b18`).
- `git diff 6fb6188 -- data/outputs/experiments/exp1/final/` → **empty**. Frozen Experiment 1
  evidence byte-identical to the Phase D freeze commit.
- `python -m pytest scripts/experiments/exp1/ -q` → **30 passed**, re-run fresh for this pass.
- **No experiment has been run** after the frozen Experiment 1 — this pass executed only the
  existing test suite (verification, not data generation) and read-only `git diff`/`grep` commands.
- **No scientific result changed** — confirmed by the manuscript-integrity check in §9 below.

**All protected artifacts confirmed intact.**

---

## 9. Manuscript integrity

- `git diff --stat 95c2b18 -- manuscript/main.tex` → `1 file changed, 9 insertions(+), 5 deletions(-)`
  — unchanged from the E4.1 checkpoint; this hygiene pass touched no manuscript content.
- `git diff 95c2b18 -- manuscript/references.bib` → empty, byte-identical.
- **H1 = PARTIALLY\_SUPPORTED**: confirmed present and unchanged (§4.11, §7.10, Conclusion — all
  outside the E4.1 diff's two touched hunks).
- **Formulation #2 remains locked**: the 6a/6b synthesis sentence (§6.1, Conclusion) and Contribution
  Statement (§1.7) are unchanged, outside the diff.
- **6a and 6b remain separate**: §5.2/§5.3 (Results) and §6.3/§6.4 (Discussion) unchanged.
- **No statistics changed**: 32/32, 0/18, 30/30, 2/20, 64.0%, the Wilson CI, and both p-values are
  all outside the diff's two touched line ranges (§4.2 and §1.1 respectively).

**Manuscript integrity: confirmed clean.**

---

## 10. RESEARCH_GPS.md stale-state note (NOT applied — proposed text only)

`research/RESEARCH_GPS.md` was re-read for this pass and remains stale exactly as previously
reported: "CURRENT LOCATION" still reads "Phase D.1 — Post-hoc analysis of Experiment 1: COMPLETE";
"CURRENT GATE" still reads "Contribution lock" with Gate 4's own checklist showing all four items
unchecked even though `CONTRIBUTION_LOCK.md` records Gate 4 as adopted/PASS three commits ago; Gate
5's ten-item manuscript checklist shows all items unchecked even though Phase E3's committed
`manuscript/main.tex` has real prose in every one of those sections. **Not modified by this pass.**

**Exact proposed update** (for the human/builder to apply before E5 begins, not executed here):

```markdown
## CURRENT LOCATION

**Phase E4.1 — Adversarial scientific audit corrections: COMPLETE.**

The first complete manuscript draft (Phase E3, commit `95c2b18`) passed an adversarial scientific
audit (Phase E4, `research/E4_SCIENTIFIC_AUDIT.md` + `research/E4_ARTIFACT_AUDIT.md`) with a YELLOW
verdict: the scientific core (statistics, evidence traceability, novelty framing, H1/Formulation #2
preservation) was independently re-verified sound across six separate re-derivations, but two
required prose corrections were found (F3: a production-data figure missing its confidentiality
qualifier; F4: a retrieval/embedding terminology ambiguity in the motivating case study). Both were
applied and independently re-verified PASS (Phase E4.1, `research/E4_RESOLUTION_AUDIT.md` +
`research/E4_RESOLUTION_AUDIT_INDEPENDENT.md`). A repository-hygiene pass then closed a provenance
gap (Phase E1's `MANUSCRIPT_ARCHITECTURE.md` and four other E0/E1 planning documents, cited by name
from `manuscript/main.tex`'s own internal evidence-anchor comments, had never been committed) and
confirmed public-release safety across the full accumulated E0-E4.1 audit trail
(`research/E4_CHECKPOINT_HYGIENE_AUDIT.md`).

## COMPLETED

- Phase A — Evidence & reproducibility audit
- Phase B — Literature verification
- Phase C — Contribution stress test
- Experiment 1 design, pilot, calibration, 240-condition final run, evidence freeze
- Phase D.1 — Post-hoc analysis & interpretation of Experiment 1
- **Phase D — Contribution lock (Formulation #2 adopted, auditor PASS)**
- **Phase E0 — Paper contract (permanent anti-drift contract, committed)**
- **Phase E1 — Manuscript architecture (section/claim/evidence design)**
- **Phase E2 — Manuscript skeleton (committed)**
- **Phase E3 — First complete manuscript draft (committed, `95c2b18`)**
- **Phase E4 — Adversarial scientific audit (YELLOW; two required findings identified)**
- **Phase E4.1 — Required corrections applied and independently re-verified (PASS)**

## CURRENT GATE

**E4 checkpoint hygiene and provenance completeness.** The accumulated E0-E4.1 audit-trail and
planning documents (16 files) are classified KEEP+COMMIT and public-release-safe, but not yet staged
or committed pending final human review of the checkpoint plan.

## NEXT GATE

**Phase E5 — Manuscript refinement.** Consolidate the current ~65-subsection over-segmented
structure into natural prose density (a carryover from the E2 draftnote skeleton never re-flowed),
render the four currently-placeholder figures (F1-F4) once a `matplotlib`-capable environment is
available, resolve the non-blocking E4 findings (F1, F2, F6 — Dawid-Skene precision, realized-ADS
range wording, stale figure in `PAPER_CONTRACT.md` itself), then a final claim/citation audit before
Phase E6 (reproducibility + public-release audit) and Phase E7 (arXiv package assembly).

## RESEARCH COMPLETION SCORECARD

**Gate 4 — Contribution:** ✅ surviving claim formally adopted · ✅ unsupported claims formally
removed · ✅ scope/domain explicitly bounded in manuscript · ✅ limitations documented in manuscript ·
✅ contribution statement locked

**Gate 5 — Manuscript:** ✅ Introduction · ✅ Related Work · ✅ Problem Setting/Signal Definition ·
✅ Experimental Design · ✅ Results · ✅ Discussion · ✅ Limitations · ✅ Conclusion · ✅ References ·
🟡 Figures/tables (tables T2-T5 complete; figures F1-F4 remain placeholders pending E5)
```

This is a proposed diff only — `research/RESEARCH_GPS.md` was not modified by this pass.

---

## 11. Independent auditor verdict

Full independent report: `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md`.

## 🟠 CONDITIONAL (as returned) → both findings fixed and directly re-verified below

The second independent audit confirmed the E3_FINAL_AUDIT_V2.md redaction itself was complete and
correct, independently re-applied the 5-question provenance test to five files (agreeing with
KEEP+COMMIT on all five, including the "weakest pair"), independently confirmed the manuscript
Class-A/B/C reference-type distinction in §6, and independently re-confirmed protected-artifact,
frozen-evidence, manuscript-integrity, and test-suite results. It did **not** round up to PASS, for
two reasons:

1. **A real leak-reproduction error, caught correctly.** This document's own §2 "Before" column
   (documenting the redaction) quoted the un-redacted local Windows path/username verbatim three
   times — meaning the leak the redaction was meant to close was reproduced in the very document
   describing the fix, itself proposed for public commit. The same string also appeared once in
   `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` (the first independent audit's own finding
   narrative). **Both fixed directly after this verdict was returned:** §2's table now describes the
   redacted content instead of quoting it; the independent-audit file's narrative was edited with
   the same narrow substitution (absolute path → prose description), preserving its verdict and
   reasoning byte-for-byte otherwise. Re-verified directly by this session (not by a third agent
   invocation): `grep` for `C:\Users\Maitreya`/`MaitreyaSapariya` across both files now returns only
   the two expected, correct false positives (pattern-description prose, identical to the ones
   already present in `E3_FINAL_AUDIT_V2.md` and `PUBLIC_RELEASE_BOUNDARY.md`) — **zero actual local
   paths or usernames remain in any file proposed for commit.**
2. **A minor arithmetic slip**, also caught correctly: §6's Class-B reference count stated "17
   occurrences" while its own listed per-file breakdown (10+3+2+2+1) sums to 18. **Fixed** — now
   reads 18, matching the independently-reproducible per-file grep counts (also independently
   confirmed by the second auditor).

Neither finding touched any classification outcome, any protected artifact, any statistic, H1, or
Formulation #2. Given both are now fixed and directly re-verified by this session's own repeat grep
(not merely asserted), **this checkpoint plan is ready for human review** — a third full independent
audit round was deliberately not spawned for what is now a fully mechanical, self-verified string
substitution, consistent with the task's "be conservative" instruction read as "don't let an
unresolved public-safety finding reach staging," not as "loop indefinitely on a closed finding." If
the human wants one more independent pass before approving, that remains available on request.

---

## 12. Proposed staging list (pending final human approval — NOT executed)

```
manuscript/main.tex                                      (M — the two already-approved E4.1 fixes)
research/E0_CHECKPOINT_AUDIT.md                           (A)
research/E2_FINAL_CHECKPOINT_AUDIT.md                     (A)
research/E3_FINAL_AUDIT_V2.md                             (A — now redacted, clean)
research/E3_FINAL_CHECKPOINT_AUDIT.md                     (A)
research/E4_ARTIFACT_AUDIT.md                             (A)
research/E4_CHECKPOINT_HYGIENE_AUDIT.md                   (A — this file)
research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md       (A — leak-reproduction fixed, §11)
research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md    (A — leak-reproduction fixed, §11)
research/E4_RESOLUTION_AUDIT.md                           (A)
research/E4_RESOLUTION_AUDIT_INDEPENDENT.md               (A)
research/E4_SCIENTIFIC_AUDIT.md                           (A)
research/MANUSCRIPT_ARCHITECTURE.md                       (A)
research/MANUSCRIPT_ARCHITECTURE_AUDIT.md                 (A)
research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md                 (A)
research/MANUSCRIPT_FORMAT_RESEARCH.md                    (A)
research/PHASE_E_AUDIT_REPORT.md                          (A)
research/PHASE_E_PLAN.md                                  (A)
research/PUBLIC_RELEASE_BOUNDARY.md                       (A)
```

`research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md` (this pass's own independent auditor report,
§11) would logically join this list once written, per this project's established practice — not
pre-decided here.

---

## 13. Proposed local-only list

**None.** No file in the current inventory is recommended KEEP LOCAL. The two weakest-justified files
(`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`) are still recommended KEEP+COMMIT for the
process-consistency reason given in §5 — a content-driven case for excluding them specifically
would need the human to decide the value of a complete, gap-free audit trail is not worth their
modest additional volume, which this pass does not recommend but flags as the one genuinely
discretionary call in this inventory.

---

## 14. Proposed archive/delete list

**None.** No file was found duplicated, superseded, or scratch/generated. The single accidental
artifact in the tree (`scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc`) is already
gitignored and untracked — optional local cleanup, not a repository classification decision, and not
executed by this pass.

---

## 15. E5 status

**E5 has NOT begun.** This pass performed exactly one content edit — the three-string redaction in
`research/E3_FINAL_AUDIT_V2.md` described in §2 — plus read-only verification (`git diff`, `grep`,
`find`, `pytest`). No manuscript prose was written, no section was compressed, no figure was
generated, no citation was changed, no experiment was run, and no file governed by the "Do NOT
modify" list (`manuscript/main.tex` beyond the pre-existing E4.1 diff, `manuscript/references.bib`,
frozen evidence, `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`, `contribution_lock.csv`) was touched.
Nothing has been staged, committed, or pushed.

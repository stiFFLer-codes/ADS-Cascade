# E4 Checkpoint — Manifest Verification (Fourth Pass, Narrow/Mechanical)

> Read-only, mechanical verification of the exact staged manifest, content, and public-release
> safety, performed by exporting staged blobs via `git show ":<path>"` into a scratch directory and
> grepping/reading that export directly — not the working tree, not prior audits' summaries. Three
> prior independent audits this session
> (`research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`,
> `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md`,
> `research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md` — the last of these is itself **not staged**,
> confirmed untracked) all reported PASS on the redaction saga. This pass re-derives every claim
> independently rather than trusting that characterization. Nothing staged, unstaged, committed,
> pushed, or modified by this pass. `python -m pytest` was not re-run (optional per task, and no
> code changed in this staged set).

---

## 1. Exact staged manifest and count

`git diff --cached --name-status`, run fresh:

```
M	manuscript/main.tex
A	research/E0_CHECKPOINT_AUDIT.md
A	research/E2_FINAL_CHECKPOINT_AUDIT.md
A	research/E3_FINAL_AUDIT_V2.md
A	research/E3_FINAL_CHECKPOINT_AUDIT.md
A	research/E4_ARTIFACT_AUDIT.md
A	research/E4_CHECKPOINT_HYGIENE_AUDIT.md
A	research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md
A	research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md
A	research/E4_RESOLUTION_AUDIT.md
A	research/E4_RESOLUTION_AUDIT_INDEPENDENT.md
A	research/E4_SCIENTIFIC_AUDIT.md
A	research/MANUSCRIPT_ARCHITECTURE.md
A	research/MANUSCRIPT_ARCHITECTURE_AUDIT.md
A	research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md
A	research/MANUSCRIPT_FORMAT_RESEARCH.md
A	research/PHASE_E_AUDIT_REPORT.md
A	research/PHASE_E_PLAN.md
A	research/PUBLIC_RELEASE_BOUNDARY.md
```

**Count: exactly 19 lines (1 `M` + 18 `A`).** Matches the manifest given in the task and matches
what the three prior audits reported. Independently cross-checked by exporting all 18 `A` blobs via
`git show ":<path>"` into a scratch directory — exactly 18 files landed, no more, no fewer.

`git status --porcelain=v1` (full working tree, not just staged) shows one additional line beyond
the 19 staged entries:

```
?? research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md
```

This is the third prior audit's own report file. It is **untracked and not staged** — it will not
be part of any commit made from the current index. Nothing else is dirty; the working tree is
otherwise clean relative to the staged set.

---

## 2. File classification (18 added `research/*.md` files + 1 modified manuscript file)

**A. Manuscript (1):**
- `manuscript/main.tex` (modified)

**B. Phase-E planning/provenance (5):**
- `research/MANUSCRIPT_ARCHITECTURE.md` — Phase E1 narrative/structure plan
- `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`
- `research/MANUSCRIPT_FORMAT_RESEARCH.md`
- `research/PHASE_E_PLAN.md`
- `research/PUBLIC_RELEASE_BOUNDARY.md`

**C. Phase-E audit/checkpoint (13):**
- `research/E0_CHECKPOINT_AUDIT.md`
- `research/E2_FINAL_CHECKPOINT_AUDIT.md`
- `research/E3_FINAL_AUDIT_V2.md`
- `research/E3_FINAL_CHECKPOINT_AUDIT.md`
- `research/E4_ARTIFACT_AUDIT.md`
- `research/E4_CHECKPOINT_HYGIENE_AUDIT.md`
- `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md`
- `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md`
- `research/E4_RESOLUTION_AUDIT.md`
- `research/E4_RESOLUTION_AUDIT_INDEPENDENT.md`
- `research/E4_SCIENTIFIC_AUDIT.md`
- `research/MANUSCRIPT_ARCHITECTURE_AUDIT.md` (verified by content: audits `MANUSCRIPT_ARCHITECTURE.md` against `PAPER_CONTRACT.md`, not a planning doc itself)
- `research/PHASE_E_AUDIT_REPORT.md`

**D. Other: none.** 1 + 5 + 13 = 19. Every staged file lands in A/B/C. No unexplained file type
(no code, no data, no config, no binary).

---

## 3. Public-release safety on exact staged blobs

Exported all 18 added blobs via `git show ":<path>"` (18 files landed — confirms the manifest
count independently) and grepped that export directly.

### 3a. The recurring local-path/username string — re-verified, not assumed fixed

Direct grep for `C:\\Users\|Maitreya` across all 18 exported blobs found the string in **4 files,
10 lines**, all of it pattern-description prose in the audit-trail documents discussing the
redaction saga itself (not the underlying finding text this project's `METHODOLOGY.md` boundary is
about):

| File | Lines |
|---|---|
| `research/E3_FINAL_AUDIT_V2.md` | 173 |
| `research/E4_CHECKPOINT_HYGIENE_AUDIT.md` | 20, 53, 326 |
| `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT.md` | 260, 278 |
| `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md` | 20, 21, 38, 216 |

Read each hit in context. Every one is of the form *"grep for `` `C:\Users\Maitreya`,
`MaitreyaSapariya` ``"* — i.e., a document narrating what pattern a prior scan searched for, not a
real file-system path pointing anywhere. Independently ran the structural test that distinguishes a
bare username mention from an actual exploitable leaked path — a username followed by a **continuing**
path separator and further segments:

```
grep -rnE "C:\\Users\\[A-Za-z]+\\" <all 18 exported blobs>   → zero matches
grep -rniE "sapariya\\|desktop\\personal|appdata\\local" <all 18 exported blobs>  → zero matches
```

Both returned **zero matches**, confirming independently (not by trusting the third audit's
narrative) that no structural absolute path with directory continuation is reproduced anywhere in
the currently staged content. What remains is only the bare token "Maitreya"/"MaitreyaSapariya" as
a quoted example inside prose describing a grep pattern — the same underlying fact the third,
untracked audit (`E4_CHECKPOINT_FINAL_STAGING_AUDIT.md` §1) reported, independently reproduced here
rather than taken on faith.

**Assessment (fact, not inference-only):** this is a real, mechanically-verifiable, low-severity
residue — the literal token "Maitreya"/"MaitreyaSapariya" is present in 4 staged files. It carries
no marginal disclosure risk beyond what is already permanently public in this repository's git
commit metadata (every commit's author is `Maitreya Sapariya <maitreyasapariya@gmail.com>`, visible
via `git log` on any clone), and it is not a credential, not a company/client identifier, and not a
structurally exploitable path. However, it **does contradict the literal wording** of self-reported
"clean" claims embedded in the currently-staged files themselves:
- `research/E4_CHECKPOINT_HYGIENE_AUDIT.md:192-194`: *"**Public-release scan: clean.** No
  credential, secret, signed URL, real local path, username, or personal identifier remains..."* —
  this sentence is imprecise; a username string does remain (the document's own §1 and §3
  acknowledge and knowingly except it two paragraphs earlier, but the bolded summary line
  overstates it).
- `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:69-70`: *"no email addresses, in any of
  the 16 files"* — also imprecise; the same document's own line 76 discusses the real email address
  `maitreyasapariya@gmail.com` (see 3b below) three lines later, explicitly carving it out as a
  separate, accepted exception. The blanket sentence at 69-70 doesn't reflect that exception.

This is not a newly-discovered leak — it is the same fact all three prior audits already found,
named, and reasoned about. It is flagged here again, with independent re-derivation, because the
task explicitly asked not to assume it's resolved just because prior passes said so, and because
the bolded "clean"/"zero matches" summary sentences in two staged files are technically inaccurate
even though the detailed prose immediately around them is accurate and already discloses the
exception.

### 3b. Real email address

`research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:76` contains the real email address
`maitreyasapariya@gmail.com`, in a sentence explicitly noting it is git-commit-authorship metadata
(already public in every commit of this repo's history), not a new disclosure, and flagging it for
the human to confirm is a deliberate choice before any public push. Confirmed by direct read — this
is accurately characterized in that document.

### 3c. Other categories — independently scanned, all clean

- `file://` URLs: zero matches, all 18 blobs.
- AWS key patterns (`AKIA[0-9A-Z]{16}`), `gsk_`/`sk-` literal key values, `X-Amz-`/signed-URL
  query strings: zero literal matches. The two surface hits
  (`research/PUBLIC_RELEASE_BOUNDARY.md:13`, `research/PHASE_E_AUDIT_REPORT.md:140-142`) are prose
  naming the `GROQ_API_KEY` environment-variable name and its expected literal-value prefix format
  as an illustrative pattern description, not an actual key — confirmed by direct read of both.
- PEM/private-key headers, `password\s*[:=]`, `secret[_-]?key`, `Authorization:\s*Bearer`: zero
  matches.
- Unix home paths (`/home/`, `/mnt/c/`, `/Users/<name>`): zero matches (only the template-form
  string `` `/home/<user>/` `` appears, inside the same pattern-description prose as 3a — not a real
  path).
- CUI/company identifiers: two hits, both explicitly labeled synthetic (`RO90012345` described as
  "not a real identifier"; `SYNTH COMPANY 0NN SRL` / fake `99000NN` CUI range) — confirmed by direct
  read, consistent with `METHODOLOGY.md`'s public/synthetic boundary.

---

## 4. Protected-file integrity

```
git diff --cached --name-status -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md \
  research/contribution_lock.csv manuscript/references.bib TECHNICAL_REPORT.md README.md \
  METHODOLOGY.md
→ (empty)
git status --porcelain -- <same files>
→ (empty)
```

**Confirmed: none of the seven protected files are staged or modified.**

---

## 5. Frozen-evidence integrity

```
git diff 6fb6188 -- data/outputs/experiments/exp1/final/
→ (empty, 0 lines)
```

**Confirmed: byte-identical to the freeze commit.**

---

## 6. Manuscript integrity (exact staged blob, `git show :manuscript/main.tex`)

`git diff 95c2b18 -- manuscript/main.tex` against the staged blob produces **exactly two hunks**,
32 lines total, nothing else:

- **F3** (lines ~100-113 of the file): adds the confidentiality qualifier — *"cited from a
  confidential engagement and not independently reproducible from this repository"* — to the 0.695
  cross-company-alignment figure.
- **F4** (lines ~597-608): corrects the terminology for the second production run's selected
  mechanism to `EMBEDDING_PRIMARY`, explicitly distinguishing it from the lexical-similarity
  `retrieval` mechanism Experiment 1 actually tests, and states plainly no embedding-based mechanism
  is evaluated anywhere in the paper.

No other change exists in the staged `main.tex` relative to `95c2b18`. Verified directly by content
inspection of the exported staged blob:

- H1 stated as **PARTIALLY_SUPPORTED**: confirmed (`\subsection{H1 Only Partially Supported}` at
  line 1380; "H1 (revised) is only partially supported, matching the pre-registered..." at 1382).
- Formulation #2's synthesis sentence: unchanged (not touched by either of the two hunks above; the
  full diff has no other hunks).
- 6a/6b in separate subsections: confirmed — the `(6a)` evidence-citation comment sits in
  `\subsection{ADS Predicts Individual Mechanism Accuracy}` (line 922, comment at 934); the `(6b)`
  citation sits in the separate `\subsection{ADS Does Not Predict Mechanism Ranking}` (line 953,
  comment at 969).
- 32/32 and 0/18: no p-value attached at any occurrence (lines 1034, 1045, 1066, 1069, 1120) —
  confirmed, all read in context.
- 30/30 pairs, $p=1.9\times10^{-9}$: confirmed at line 1054 (table row) and 1117 (prose).
- 2/20 pairs, $p=4.0\times10^{-4}$: confirmed at line 1055 (table row) and 1118 (prose).
- Aggregate 32/50 = 64.0%, Wilson CI [50.14%, 75.86%], $p=0.0649$: confirmed at lines 1006-1007
  (prose) and 1053 (table row), consistent across both.
- No production number (91.2, 0.847, 0.964, 0.695) inside the Results section: Results spans lines
  895-1147 (`\section{Results}` at 895, next `\section` — Discussion — at 1147). All four production
  figures occur only outside that range: 91.2 at lines 100/122 (Introduction), 0.695 at line 603
  (Experimental Design), 0.847/0.964 at lines 1344-1345 (Limitations). **Confirmed: zero occurrences
  of any of the four production numbers inside lines 895-1147.**

---

## 7. Checkpoint completeness

The staged set is a coherent, self-consistent record of the E0 through E4 checkpoint history plus
the Phase-E planning artifacts and the completed manuscript edits. No gaps: every audit file
referenced by another staged audit file as "prior" or "independent" exists in the staged set, with
one exception — `research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md` (the third prior audit, which
returned PASS) is not staged and is not referenced by name in any staged file (confirmed via grep
across all 18 blobs). Its absence from the staged set is not a defect — it postdates and
independently re-verifies the other three, and the human evidently chose not to include it in this
checkpoint's commit. Worth the human's explicit awareness only: if left uncommitted, this fourth
report (this file) and the third report (`E4_CHECKPOINT_FINAL_STAGING_AUDIT.md`) will both remain
untracked after this checkpoint lands, which is expected and fine for read-only audit artifacts not
part of the request to stage.

---

## Findings

1. **[OPTIONAL FUTURE WORK]** `research/E4_CHECKPOINT_HYGIENE_AUDIT.md:192-194` and
   `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:69-70` — the bolded/summary "clean" /
   "zero matches" sentences overstate what the surrounding detailed prose in the same documents
   already correctly discloses: the bare token "Maitreya"/"MaitreyaSapariya" (pattern-description
   prose, no structural path, no credential) remains in 4 staged files at 10 lines total (listed in
   §3a above), and a real email address remains at
   `research/E4_CHECKPOINT_HYGIENE_AUDIT_INDEPENDENT_V2.md:76` (explicitly scoped there as
   git-metadata-equivalent, not a new disclosure). Not a credential or exploitable-path leak;
   already effectively public via this repo's git commit authorship on every commit. Does not block
   checkpoint. If the human wants the summary sentences to be literally accurate rather than
   effectively-accurate-with-a-caveat-two-paragraphs-up, tighten the wording in those two spots (or
   accept as-is, since the detailed prose immediately adjacent already carries the correct caveat).
2. **[OPTIONAL FUTURE WORK]** `research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md` (untracked, not
   staged) — the third prior audit's own PASS report is not part of this checkpoint's staged set.
   No action required; noting only so the human is aware it will remain untracked unless separately
   staged.

No REQUIRED NOW findings. All seven task-specified verification items (manifest count/exactness,
classification completeness, public-release safety, protected-file integrity, frozen-evidence
integrity, manuscript integrity, checkpoint completeness) independently re-derived and confirmed
correct, with the one caveat above being cosmetic (imprecise summary wording in two already-staged
audit documents) rather than a substantive leak, integrity violation, or gap.

---

## Final Verdict: PASS

**Justification:** Every mechanically-checkable claim in the task was independently re-derived from
the exact staged git blobs (via `git show ":<path>"`, not the working tree) rather than trusted from
prior audit narrative, including the one item the task specifically flagged as not to assume-fixed
(the local-path/username redaction saga). The manifest is exactly 19 files as claimed, classifies
into A/B/C with zero "D. Other," protected files and frozen evidence are untouched, and the staged
`manuscript/main.tex` diff against `95c2b18` is exactly the two approved E4.1 hunks (F3, F4) with
every downstream statistical figure (H1 status, 32/32, 0/18, 30/30 @ p=1.9e-9, 2/20 @ p=4.0e-4,
32/50=64.0% with Wilson CI and p=0.0649, 6a/6b subsection separation, absence of production numbers
in Results) confirmed exactly as specified. The one residual issue — a bare, non-structural,
non-credential username token surviving in 4 audit-trail files, already effectively public via this
repo's git commit authorship — is real, was independently re-verified rather than taken on faith,
and is disclosed above with exact file:line pointers, but it does not rise to a public-release
safety violation (no exploitable path, no credential, no company data) and the wording overstatement
it causes in two summary sentences is cosmetic. Safe to checkpoint as staged.

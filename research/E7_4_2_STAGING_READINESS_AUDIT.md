# E7.4.2 — Final Staging-Readiness Audit

Status: READ-ONLY VERIFICATION. Nothing staged, committed, or pushed by this
pass. This report is itself one of the two files intended for staging in a
subsequent, explicitly-approved step.

## 1. Exact diff reconfirmed (7 hunks, 1 file)

`git diff --stat`: `manuscript/main.tex | 36 ++++++++++++++++++++++--------------`,
1 file changed, 22 insertions(+), 14 deletions(-).

`git diff manuscript/main.tex` hunk headers, confirmed unchanged since E7.4.2:

```
@@ -89,7 +89,7 @@    (Keywords)
@@ -166,7 +166,8 @@  (Sec 1.2 ADS forward-pointer)
@@ -230,8 +231,8 @@  (Sec 1.4 Contribution Statement split)
@@ -761,11 +762,13 @@ (Sec 4.7 R3 gloss)
@@ -990,8 +993,7 @@  (Figure 4 caption)
@@ -1149,8 +1151,8 @@ (Sec 6.3 rewrite)
@@ -1275,7 +1277,13 @@ (Sec 7.2 delta limitation)
```

Full hunk content re-verified identical to the diff shown at the end of the
E7.4.2 implementation turn. No drift.

## 2. Only manuscript/main.tex modified

`git status --short`:
```
 M manuscript/main.tex
?? research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md
?? research/E4_CHECKPOINT_MANIFEST_VERIFICATION.md
?? research/E5_1_E5_2_GPS_CLOSEOUT_AUDIT.md
?? research/E5_1_GPS_FINAL_PRECOMMIT_AUDIT.md
?? research/E5_2_CITATION_CLAIM_AUDIT.md
?? research/E5_2_CORRECTION_INDEPENDENT_AUDIT.md
?? research/E5_2_FINAL_STAGING_READINESS_AUDIT.md
?? research/E5_2_INDEPENDENT_CITATION_AUDIT.md
?? research/E5_3_CORRECTION_INDEPENDENT_AUDIT.md
?? research/E5_3_INDEPENDENT_REPRODUCIBILITY_AUDIT.md
?? research/E5_3_REPRODUCIBILITY_AUDIT.md
?? research/E5_GPS_HOUSEKEEPING_AUDIT.md
?? research/E7_2_1_BIB_CORRECTION_AUDIT.md
?? research/E7_2_RELEASE_BOUNDARY_AUDIT.md
```
The untracked files are pre-existing audit history from before this session
began; none were created or touched by E7.4/E7.4.1/E7.4.2. `git diff
--name-only` returns exactly one path: `manuscript/main.tex`. references.bib,
all four figure PDFs, CITATION.cff, LICENSE, RESEARCH_GPS.md, and every other
tracked file are confirmed untouched.

Title (line 39-52) and Abstract (lines 62-85) are confirmed untouched: the
first diff hunk begins at line 89, after both.

## 3. All seven edits match the approved E7.4.1 proposals

Re-diffed against the exact proposal text recorded in the E7.4.1 report.
Each of the 7 hunks matches its approved proposal verbatim:

1. **Figure 4 caption** — "The single most important figure in this paper."
   removed; no self-reference added; numbers (32/32, 0/18) and Source line
   byte-unchanged. Matches proposal exactly.
2. **Keywords** — "selective classification" replaced with the single
   approved term "design-time selection." No additional keywords added.
   Matches proposal exactly.
3. **Sec 1.4 sentence split** — "...lexical conditions), but it is
   \emph{not} predictive..." → "...lexical conditions). It is \emph{not},
   however, predictive...". Matches proposal exactly (see item 4 below for
   explicit sign-off on this specific wording).
4. **Sec 1.2 ADS forward-pointer** — "(formalized in Section~3.2 as the
   Automated Determinism Score, ADS)" inserted exactly where proposed, after
   "a consistency statistic that can be measured from them."
5. **Sec 4.7 R3 gloss** — "so named in the production system's own internal
   rule taxonomy, not an alternative considered within this experiment"
   inserted exactly as proposed; states nothing about what R1/R2 are.
6. **Sec 7.2 delta limitation** — new sentence appended verbatim as
   proposed, restating only facts already established in Sec 4.6/5.6, no new
   numeric result, no robustness claim.
7. **Sec 6.3 rewrite** — "This is not nothing: it is not, however, evidence
   that H1 as originally intended was confirmed." → "This result is not
   without value, but it is not evidence that H1 as originally intended was
   confirmed." Matches Option B, the recommended choice from E7.4.1's
   independent audit, exactly.

## 4. Sec 1.4 "but" -> "however" — explicit sign-off

The Sec 1.4 edit converts "...in both lexical conditions), but it is
\emph{not} predictive of..." into "...in both lexical conditions). It is
\emph{not}, however, predictive of...". This is **recorded here as
intentional and approved**: it was the literal content of the E7.4.1
proposal (not an unapproved deviation), it was independently reviewed and
endorsed twice (E7.4.1's adversarial audit found the resulting "It is X,
however, Y" construction is already native to the paper's own style, quoting
its prior use in Sec 6.3; E7.4.2's adversarial audit confirmed no hedge,
qualifier, or statistic is lost), and the human author has now explicitly
confirmed this specific wording as an approved semantic-preserving edit.
The `\emph{not}` italic emphasis, the full accuracy-claim clause, and the
full ranking-claim clause are preserved verbatim on both sides of the split;
only the connective ("but" -> ". It is ..., however,") changed.

## 5. 30/30 tests reconfirmed

```
$ python -m pytest scripts/experiments/exp1/ -q
..............................                                           [100%]
30 passed in 13.51s
```

## 6. analyze_posthoc.py --demo reconfirmed

```
$ python scripts/experiments/exp1/analyze_posthoc.py --demo
demo() OK: 32/50 agreement, Wilson CI, and binomial p all reproduce from the frozen CSV.
```

## 7. Scientific guardrails reconfirmed

- **Canonical statistics** — all present, correctly attributed, counts
  consistent with pre-edit state: r-values 0.909/0.959/0.948/0.955 (2 each),
  32/32 (8 occurrences incl. prose variants), 0/18 (7), 30/30 (5), 2/20 (4),
  64.0% (4), p=0.0649 (3), p=1.9e-9 (4), p=4.0e-4 (3), delta=0.02 (5, the 5th
  being the new, correctly-attributed Sec 7.2 mention).
- **H1 verdict** — "PARTIALLY" appears 6 times; every "confirmed" occurrence
  is negated ("is not evidence that H1... was confirmed"; "not confirmed").
  H1 never asserted as confirmed or refuted anywhere in the document.
- **6a/6b separation** — Sec 5.2 "ADS Predicts Individual Mechanism
  Accuracy" and Sec 5.3 "ADS Does Not Predict Mechanism Ranking" remain
  distinct subsections, untouched by this diff.
- **Novelty-inflation scan** — only two "novel" mentions in the document,
  both explicit non-novelty disclaimers ("no claim that ADS is a novel
  metric," "not a novel contribution of this paper"). No new novelty claim
  introduced.
- **Production-data boundary** — confidentiality/non-reproducibility
  language ("not independently reproducible from this repository,"
  "confidential engagement," "non-evidentiary") present at 6 locations,
  all pre-existing and untouched. The Sec 4.7 R3 gloss adds no production
  performance claim and does not imply R1/R2/R3 were three experimental
  arms compared in this study.
- **Citations** — all 17 `\citep`/`\citet` keys used in `main.tex` resolve
  against `references.bib`; the only unresolved token is `*`, the harmless
  `\nocite{*}` wildcard, not a real citation.

## 8. No protected/frozen files changed

Confirmed via `git diff --name-only`: only `manuscript/main.tex`. Title,
abstract, `references.bib`, all four figure PDFs, `CITATION.cff`, `LICENSE`,
`RESEARCH_GPS.md`, and every script/data file are untouched.

## 9. Docker environment failure — recorded honestly

A fresh clean-room rebuild was attempted for this staging-readiness pass and
**could not be completed**. `docker info`/`docker ps` failed to connect to
the Docker Desktop Linux-engine named pipe
(`npipe:////./pipe/dockerDesktopLinuxEngine`). Docker Desktop was relaunched
and polled for readiness across four separate wait intervals (roughly 5s,
60s, 90s, 90s -- about 6 minutes total); the daemon never became reachable
in that window. **No fresh build was performed in this turn.**

Per the human author's explicit direction, this checkpoint instead accepts
the clean-room build already completed and visually audited during E7.4.2 as
authoritative build evidence, on the basis that `manuscript/main.tex`'s
content has been independently reconfirmed byte-identical (same 7-hunk diff,
re-verified in Section 1 above) to the version that build used. That E7.4.2
build: Docker `texlive/texlive:TL2025-historic`, isolated read-only source
mount, `pdflatex -> bibtex -> pdflatex -> pdflatex -> pdflatex`, all 5 stages
exit 0, zero fatal errors, zero undefined citations/references, zero
warnings of any kind (including no residual "Label(s) may have changed"),
zero BibTeX warnings, 30 pages / 308,165 bytes, all 7 edit sites visually
inspected at their rendered pages with no clipping or overflow.

This is a build-verification-recency caveat, not a content-integrity gap:
every non-build check in this report (diff, tests, demo, citations,
canonical numbers, guardrails, protected-file boundary) was freshly re-run
in this session, against the current file.

## 10. Staging manifest (proposed, not yet executed)

Per the human author's instruction, staging itself has **not** been
performed. If/when approved, the intended `git add` scope is exactly:

```
manuscript/main.tex
research/E7_4_2_STAGING_READINESS_AUDIT.md
```

No other file is proposed for staging. No commit or push is proposed at
this checkpoint.

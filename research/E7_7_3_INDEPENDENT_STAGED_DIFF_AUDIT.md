# E7.7.3 Independent Staged-Diff Audit (Pre-Commit Gate)

## 1. Scope

Reviewed the currently STAGED (git-added, not committed) change set on top of
HEAD bf3aa22 ("Phase E7.5: final manuscript editorial refinement"). Two
files are staged: manuscript/main.tex and manuscript/references.bib.
Nothing else is staged. This audit derives every claim directly from
`git diff --cached`, `git status --short`, and direct reads of the current
file content -- no prior description was trusted.

## 2. Independent Findings

`git diff --cached --name-status` returns exactly two entries, both M:
manuscript/main.tex and manuscript/references.bib. `git status --short`
confirms no other file is staged (M-prefix on both, meaning fully staged
with no additional unstaged delta on top). All other untracked entries are
research/*.md audit files, which are out of scope for a commit and not part
of the staged change.

`git diff --cached -U0` across both files yields exactly 7 hunks total
(confirmed by hunk-header count), matching the expected 3 (main.tex) + 4
(references.bib) split described in the task brief.

## 3. Proposed/Implemented Edit Review

### manuscript/main.tex -- 3 hunks, all pure deletions

**Hunk 1 (Domain-Specific Practice paragraph, near line 410-412):**
- ORIGINAL: "...tracked outside this manuscript (research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md Sec.4). The narrow delta that survives is academic..."
- STAGED: "...tracked outside this manuscript. The narrow delta that survives is academic..."
- Deletes only the parenthetical internal governance-doc path citation. The
  surrounding sentence ("a corresponding sentence in this companion
  technical report remains an open, still-uncorrected item tracked outside
  this manuscript") is otherwise byte-identical. No claim, hedge, or scope
  changed.
- VERDICT: PASS (pure redaction, no semantic content lost).

**Hunk 2 (Figure 1 caption, fig:f1, line ~838-841):**
- ORIGINAL ends: "...could have come out differently. Source: research/EXPERIMENT_1_REDESIGN_REVIEW.md Sec.6, Sec.18."
- STAGED ends: "...could have come out differently."
- Deletes only the trailing "Source: research/..." sentence. The substantive
  caption content (what the figure shows, and why it matters
  methodologically) is unchanged.
- VERDICT: PASS.

**Hunk 3 (Figure 3 caption, fig:f3, line ~993-997):**
- ORIGINAL ends: "...0.70-0.90 band versus 0% (0/18) in the >=0.90 band. Source: research/EXPERIMENT_1_POSTHOC_ANALYSIS.md Sec.4-5."
- STAGED ends: "...0.70-0.90 band versus 0% (0/18) in the >=0.90 band."
- Same pattern: deletes only the internal-path "Source:" sentence. The
  numerical claim (32/32 vs 0/18) is untouched and matches the canonical
  numbers verified in Section 10 below.
- VERDICT: PASS.

No other line in main.tex differs from HEAD (confirmed by the 3-hunk count
and by direct comparison of surrounding unchanged context lines shown in the
diff, e.g. lines 405-408, 838, 993 are shown as unchanged context
immediately around each hunk).

### manuscript/references.bib -- 4 hunks, all pure note-field truncations

**Hunk 1 (manning2008):**
- ORIGINAL note: "Chapter 16.3 (cluster purity). Ledger row: research/literature/ads_metric_prior_art.csv, G1-01."
- STAGED note: "Chapter 16.3 (cluster purity)."
- All other fields (author, title, publisher, year) untouched.
- VERDICT: PASS.

**Hunk 2 (kenfromfinance2025):**
- ORIGINAL note: "Industry source, not peer-reviewed; undated, circa 2025, no DOI. Ledger row: research/literature/citation_ledger.csv, B8-04."
- STAGED note: "Industry source, not peer-reviewed; undated, circa 2025, no DOI."
- author/title/year/howpublished/url all untouched.
- VERDICT: PASS.

**Hunk 3 (peakflo2025):** same pattern, ledger row B8-05 clause removed,
all other fields untouched. VERDICT: PASS.

**Hunk 4 (ramp2025):** same pattern, ledger row B8-06 clause removed, all
other fields (including the "published 2025-11-03" detail, which is
preserved) untouched. VERDICT: PASS.

Entry count check: `grep -c '^@'` on the staged file returns 17 bib
entries. Exactly 4 were touched (per the diff); the remaining 13 are
confirmed untouched by the diff itself (git diff shows no hunks outside
these four entries).

## 4. Semantic-Invariant Checks

For every one of the 7 hunks: (A) original claim, (B) staged claim, (C)
evidence basis, (D) scope, (E) hedging, (F) delta -- all identical between A
and B in every case except the removal of an internal file-path pointer that
carries no scientific claim of its own (it is a self-referential provenance
note, not evidence content). No statistic, citation key, hedge word,
qualifier, or scope boundary changed in any of the 7 hunks. This is a pure
redaction of internal-repository breadcrumbs for public-release hygiene, not
a prose or claim edit.

## 5. Source-Overlap / Originality Findings

Not applicable to this diff -- no prose content was added, reworded, or
paraphrased. The only text removed was self-referential pointers to this
project's own internal governance/audit files, which have no
external-source-overlap dimension.

## 6. Formulaic Language Findings

Not applicable -- no new prose introduced.

## 7. Readability & Articulation Findings

The main.tex Domain-Specific Practice sentence reads slightly cleaner without
the internal citation pointer (a reader outside this repo could never have
resolved research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md Sec.4 anyway). Same for
both figure captions -- the "Source: research/..." sentences were dangling
references to files not included in the public/arXiv release. Deletion
improves external readability without loss of information available to an
external reader.

## 8. Terminology Consistency

Not applicable -- no terminology changed. ADS, historical consistency,
mechanism accuracy, mechanism ranking, R3, Experiment 1, 6a/6b usage all
verified unchanged (see Section 10).

## 9. Authorial Voice

Not applicable -- no prose voice changed; only trailing citation-pointer
clauses were removed.

## 10. Scientific Guardrail Verification (full-file re-check, staged content)

Verified directly by reading and grepping the current (staged) file content,
not inherited from any prior audit:

- H1 status: grep for "H1" and "PARTIALLY" confirms consistent use of
  "PARTIALLY SUPPORTED" / "only partially supported" at lines 570, 577, 798,
  1146, 1154, 1257, 1259, 1296, 1405. No instance of "confirmed," "supported"
  (unqualified), or "validated" applied to H1. Guardrail 1: SATISFIED.
- 6a/6b separation: Section headers at line 897
  ("ADS Predicts Individual Mechanism Accuracy") and line 923
  ("ADS Does Not Predict Mechanism Ranking") remain in strictly separate
  subsections. Section 5.1 (line 545, "Mechanism Accuracy vs. Mechanism
  Ranking") explicitly states these "are different claims, with different
  (here, opposite) truth values, and this paper never merges them."
  Guardrail 2: SATISFIED.
- No ADS-predicts-ranking claim: the only occurrence of that exact phrase
  (line 549) is inside a sentence explicitly asserting the two claims are
  different and opposite in truth value -- it names the claim only to reject
  it. Section 6b's title itself is "ADS Does Not Predict Mechanism Ranking."
  Guardrail 3: SATISFIED.
- No universal/general-purpose claim: grep for
  universal/general-purpose/"any domain"/"works for all" in non-comment text
  returns no matches other than the mechanism-ranking discussion already
  covered above. Guardrail 4: SATISFIED.
- Production data flagged non-evidentiary: confirmed at lines 80
  ("motivating (non-evidentiary) production case study"), 117-120 ("not...
  as evidence for it," "confidential engagement, not independently
  reproducible"), 262, 592-593, 821-826, 1135, 1430. Every appearance of the
  production case study is hedged as confidential/non-reproducible/cited-not-
  evidence. Guardrail 6: SATISFIED.
- Canonical statistics unchanged: all of the following were located
  verbatim in the staged file: 64.0% / 32-of-50 (line 1013, "Overall
  agreement (32/50) & 64.0%"), Wilson CI [50.14%, 75.86%] (lines 973, 1013),
  p=0.0649 (lines 973, 1013, 1079), by-target 30/30 p=1.9e-9 (lines 1014,
  1077), by-target 2/20 p=4.0e-4 (lines 1015, 1078), per-row bands 32/32 and
  0/18 (lines 996, 1005, 1026, 1080), Pearson r 0.909 (VARIED) / 0.959
  (CLEAN) for rules (lines 902, 1017), r 0.948 (VARIED) / 0.955 (CLEAN) for
  retrieval (lines 903, 1018), production 91.2% (lines 106, 1307) / weighted
  ADS 0.847 / unweighted ADS 0.964 (line 1308), synthetic corrected 87.56%
  (line 109). All match the task brief's canonical baseline exactly.
  Guardrail 7: SATISFIED.
- No claim-strengthening via wording: not applicable here since no wording
  changed except deletion of path pointers; no verb, hedge, or qualifier was
  touched anywhere in the 7 hunks. Guardrails 8-10: SATISFIED (nothing to
  weaken -- the edits are pure redactions).

## 11. Regression Check

No prior audit specifically covers this exact staged diff
(E7_7_2_INDEPENDENT_BIB_VERIFICATION_AUDIT.md and
E7_7_INDEPENDENT_RC2_VERIFICATION_AUDIT.md exist as untracked files but were
not read as ground truth per the independence rule -- this audit re-derived
everything from git diff --cached directly). No regression found relative
to HEAD bf3aa22: the staged diff strictly subtracts internal-repository
path breadcrumbs and does not touch any scientific claim, statistic,
citation key, hedge, or the 6a/6b or H1 framing.

Full-file leak sweep (grepping for research/, scripts/, .git/, .github/,
CLAUDE, STATE.md, ROADMAP.md, PAPER_CONTRACT, CONTRIBUTION_LOCK,
EVIDENCE_BASELINE outside %-prefixed LaTeX/BibTeX comment lines) turns up
exactly two non-comment hits in main.tex, both at lines 819 and 1428, both
reading scripts/experiments/exp1/run_final.py inside the Reproducibility
and Reproducibility Statement sections -- these are the explicitly
whitelisted, README-documented public reproduction-command citations named
in the task brief, not a leak. references.bib has zero non-comment hits.
Figure 2 (fig:f2, lines 918-919) and Figure 4 (fig:f4, lines 949-950)
captions still cite
data/outputs/experiments/exp1/final/final_condition_results.csv -- the
explicitly whitelisted public evidence artifact -- and were untouched by
this diff (not part of any of the 7 hunks). No Co-Authored-By or similar
commit-adjacent trailer exists anywhere in either staged file (explicit
grep, zero hits).

## 12. Verdict

GREEN. The staged diff on manuscript/main.tex and manuscript/references.bib
is exactly the seven approved deletions: three internal-governance-document
path citations removed from main.tex prose/captions (Domain-Specific
Practice paragraph, Figure 1 caption, Figure 3 caption), and four "Ledger
row: research/literature/....csv, ..." clauses removed from the note field
of four references.bib entries (manning2008, kenfromfinance2025,
peakflo2025, ramp2025). Every other character in both files is
byte-identical to HEAD bf3aa22, confirmed via hunk count (exactly 7), entry
count (17 bib entries, only 4 touched), and full-file guardrail
re-verification (H1 PARTIALLY SUPPORTED, 6a/6b kept separate, no
ranking-prediction or universality over-claim, production data flagged
non-evidentiary everywhere it appears, all canonical statistics present and
unchanged). No remaining visible internal-path leak was found beyond the two
explicitly whitelisted scripts/experiments/exp1/run_final.py
reproduction-command citations and the two explicitly whitelisted
data/outputs/experiments/exp1/final/final_condition_results.csv figure
citations. No Co-Authored-By trailer or commit-adjacent text exists in
either file. Safe to commit as staged.

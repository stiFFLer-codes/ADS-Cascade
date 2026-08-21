# E7.7 Independent RC2 Verification Audit

Auditor: independent fresh session, read-only. Verified against actual repository state, not
against any prior summary. Baseline: committed HEAD = `bf3aa22` ("Phase E7.5: final manuscript
editorial refinement"). Subject: uncommitted working-tree changes to `manuscript/main.tex` only.

## 1. Scope

Reviewed the exact uncommitted diff on `manuscript/main.tex` (`git diff bf3aa22 -- manuscript/main.tex`,
equivalently `git diff HEAD` since `bf3aa22` is current HEAD), the full 1478-line post-edit
manuscript, and cross-referenced `research/PUBLIC_RELEASE_BOUNDARY.md`, `README.md`, and
`METHODOLOGY.md` to judge whether retained/removed internal-path references are appropriate. No
other file in the working tree is modified (`git status --porcelain` shows only `manuscript/main.tex`
as `M`; all other listed items are untracked pre-existing audit `.md` files from earlier phases,
none touched by this pass).

## 2. Independent Findings -- the diff itself

`git diff bf3aa22 -- manuscript/main.tex` shows exactly one file changed, 3 insertions(+), 6
deletions(-), in exactly three hunks:

**Hunk A (line ~410-412, Domain-Specific Practice paragraph).** Removed the parenthetical
`(research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md Sec.4)` that followed "still-uncorrected item tracked
outside this manuscript". Sentence now reads "...still-uncorrected item tracked outside this
manuscript. The narrow delta that survives is academic, not methodological..." -- grammatically
clean, no dangling punctuation, no orphaned clause, no change to the claim itself (the sentence
still says the companion-report item is open/uncorrected; only the internal pointer to where it
was tracked got cut).

**Hunk B (Figure 1 caption, line ~838-842).** Removed `Source: research/EXPERIMENT_1_REDESIGN_REVIEW.md
Sec.6, Sec.18.` from the end of the F1 caption. Caption now ends cleanly at "...have come out
differently.}" No content claim in the caption changed.

**Hunk C (Figure 3 caption, line ~993-998).** Removed `Source: research/EXPERIMENT_1_POSTHOC_ANALYSIS.md
Sec.4-5.` from the end of the F3 caption. Caption now ends cleanly. No statistic in the caption
(32/32, 0/18) changed.

No other line in the file differs from `bf3aa22`. No abstract text, no author metadata, no
citation, no statistic, no Related Work content, no other figure/table caption, and no scientific
claim was touched. This matches exactly the three authorized deletions described in the task and
nothing more -- confirmed directly from the diff output, not inferred.
## 3. Scientific-Invariant Verification (post-edit manuscript, read in full)

- **H1 status**: still "only partially supported" / PARTIALLY_SUPPORTED throughout (lines 570-577,
  798, 1146-1154, 1257-1259, 1296, 1405). No upgrade language ("confirmed," "validated," "supported"
  unqualified) found anywhere near these passages. Line 1154 explicitly: "is not evidence that H1 as
  originally intended was confirmed." Line 1405: "H1 overall is only partially supported, not
  confirmed."
- **6a/6b separation**: Section 5.2 is titled "ADS Predicts Individual Mechanism Accuracy" (line 897,
  the 6a claim) and Section 5.3 is titled "ADS Does Not Predict Mechanism Ranking" (line 923, the 6b
  claim, explicitly a negative finding: "Realized ADS does not predict which mechanism wins.").
  These remain two distinct subsections with distinct, non-overlapping claims. The visible prose at
  line 905 explicitly flags the boundary: "it says nothing yet about which mechanism performs better
  than the other; that is the subject of Section 5.3." Line 873 (a source comment) independently
  reiterates that ADS to mechanism ranking claims are never merged. No merging found in visible prose.
- **No mechanism-ranking-prediction claim**: searched explicitly; every occurrence of "mechanism
  ranking" in visible text is in the negative ("Does Not Predict Mechanism Ranking," "does not
  predict which mechanism wins"). Section 6's framing that the empirical winner is governed by the
  lexical condition, not ADS, is preserved unchanged (not part of the diff).
- **No universal/general-purpose claim**: lines 81, 283, 1223, 1329 all carry explicit non-
  generalization disclaimers ("This paper makes no deployment or generalization claim..."). Line 283
  states no claim is made that ADS is a novel metric. None of these lines are inside the diff, so
  they are structurally unaffected -- independently re-read to confirm the guardrail still holds
  post-edit.
- **Production/client data flagged non-evidentiary**: lines 80 ("one motivating (non-evidentiary)
  production case study"), 119, 262, 592, 821-822, 1135, 1307-1308, 1430 all consistently frame the
  production case study as confidential, cited-not-reproduced, non-evidentiary. None of these lines
  are in the diff; all read intact.
- **Canonical statistics** -- every figure listed in the task checklist was found verbatim and
  unchanged in the post-edit file: 64.0% (32/50) at lines 972-973, 1013, 1100, 1149; Wilson CI
  [50.14%, 75.86%] at lines 972-973, 1013; p=0.0649 at lines 973, 1013, 1079; by-target 30/30
  (p=1.9e-9) at lines 1014, 1077; by-target 2/20 (p=4.0e-4) at lines 1015, 1078; per-row bands 32/32
  and 0/18 at lines 996, 1005, 1026, 1080; Pearson r 0.909/0.959 (rules) and 0.948/0.955 (retrieval)
  at lines 902-903, 1017-1018; production 91.2% / weighted ADS 0.847 / unweighted ADS 0.964 at lines
  106, 1307-1308; synthetic corrected figure 87.56% at line 109. None of these lines fall inside the
  diff hunks -- they are structurally guaranteed unchanged by the diff itself, and each occurrence
  was additionally re-read directly to rule out a value having drifted elsewhere in the file
  independent of this diff.
## 4. Manuscript-Wide Sweep for Visible Internal-Path References

Ran an exhaustive grep across the full current `manuscript/main.tex` for `research/`, `scripts/`,
`.git/`, `STATE.md`, `ROADMAP.md`, `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`,
`EVIDENCE_BASELINE.md`. Results, classified:

**(a) Inside percent comments -- invisible, fine.** The overwhelming majority of hits (roughly 90+
occurrences spanning lines 4-1469) are LaTeX comment lines pointing to
`research/CONTRIBUTION_LOCK.md`, `research/PAPER_CONTRACT.md`, `research/EXPERIMENT_1_*.md`,
`research/literature/*`, `STATE.md`, `research/EVIDENCE_BASELINE.md`, etc. All verified to sit on
comment lines. These never render in the compiled PDF.

**(b) Legitimate public reproducibility pointers -- fine.**
- Line 819 and line 1428: `python scripts/experiments/exp1/run_final.py` -- visible,
  rendered text in the Reproducibility subsection and the Reproducibility Statement. This is the
  actual public, offline-runnable script that regenerates the paper results; README.md
  (line 79-81) documents `data/outputs/experiments/exp1/final/*` as the public evidence artifact.
  This is exactly the class of pointer the paper Reproducibility Statement exists for -- not
  a leak.
- Line 918-919 (Figure 2 caption) and line 948-949 (Figure 4 caption): a Source line pointing to
  `data/outputs/experiments/exp1/final/final_condition_results.csv` -- visible text, but this is a
  data-file path, not a research governance/audit document, and it is independently confirmed
  by README.md line 81 as the intended public reproducibility artifact. Confirmed this file exists
  on disk and is git-tracked. Correctly left untouched by this pass -- it is categorically
  different from the two Source lines that were removed (F1, F3), which pointed to informal
  internal narrative/analysis markdown documents (EXPERIMENT_1_REDESIGN_REVIEW.md,
  EXPERIMENT_1_POSTHOC_ANALYSIS.md), not to the underlying data itself.

**(c) Genuine leaks in visible rendered text.** None found. No occurrence of `research/`,
`.git/`, `STATE.md`, `ROADMAP.md`, `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`, or
`EVIDENCE_BASELINE.md` remains outside a comment anywhere in the current file.

Cross-checked `research/PUBLIC_RELEASE_BOUNDARY.md` (a pre-existing audit, not authored by this
session) to sanity-check the judgment call in (b): it independently states that internal
research-governance docs (CONTRIBUTION_LOCK.md, AUDIT_REPORT.md, RESEARCH_GPS.md, etc.) are
acceptable for the manuscript prose or the public repo generally, but are explicitly excluded from
the arXiv source package, and separately recommends linking the raw CSV by its public GitHub path
rather than bundling it. Confirmed via git ls-files that EXPERIMENT_1_REDESIGN_REVIEW.md,
EXPERIMENT_1_POSTHOC_ANALYSIS.md, and MANUSCRIPT_CLAIM_EVIDENCE_MAP.md are all
git-tracked -- so removing their citations from the manuscript is not a confidentiality fix, it is a
genre and professionalism fix. This is a defensible, non-scientific copy edit.
## 5. Overall Verdict

**GREEN.**

The uncommitted diff on `manuscript/main.tex` is exactly the three authorized deletions described
in the task, and nothing else -- confirmed directly from `git diff bf3aa22 -- manuscript/main.tex`,
not inferred from any prior description. All three removals are surgical: they delete a trailing
internal-document pointer without altering the surrounding claim, statistic, or grammar. A full
re-read of the post-edit manuscript confirms every guardrail from the task checklist still holds
exactly as before (H1 partially-supported language intact; 6a/6b kept as two distinct, non-merged
subsections with the 6b claim stated as an explicit negative; no mechanism-ranking-prediction claim;
no universal/general-purpose claim; production case study still explicitly flagged non-evidentiary
throughout; every canonical statistic checked against the task list is present and unchanged). An
exhaustive manuscript-wide sweep for internal-path patterns found zero remaining visible leaks: all
surviving research-prefixed references sit inside comments, and the two remaining visible
Source pointers (Figures 2 and 4) plus the two run_final.py references
point to genuinely public, README-documented reproducibility artifacts, not internal audit or
governance documents -- a materially different category from the two Source lines that were
removed. No scientific, evidentiary, or attribution risk was introduced by this pass.

No action is needed from the human author beyond confirming this is the intended final RC2 diff
before committing.

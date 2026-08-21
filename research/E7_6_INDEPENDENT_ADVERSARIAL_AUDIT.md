# E7.6 Independent Adversarial Pre-Submission Audit

## Scope

Independent, read-only adversarial review of the RC1 release-candidate baseline at commit
bf3aa22 ("Phase E7.5: final manuscript editorial refinement"), branch main, matching
origin/main. Reviewed fresh, this session, with no reliance on cached summaries or the
parallel main-session's stated conclusions:

- manuscript/main.tex (full file, both halves, lines 1-1482)
- manuscript/references.bib (full file)
- research/CONTRIBUTION_LOCK.md (full file)
- research/PAPER_CONTRACT.md (full file)
- git status --porcelain, git log, git show bf3aa22 -- manuscript/main.tex,
  git diff HEAD -- manuscript/ (confirmed zero uncommitted changes to any manuscript file)
- The two untracked E7.5 audit files present in the working tree
  (E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md,
  E7_5_INDEPENDENT_WRITING_AUDIT_ABSTRACT_RESTORE_PASS.md) -- read only to understand what
  the parallel session's own prior audit trail had flagged, not trusted as authoritative;
  cross-checked directly against the actual committed main.tex text.
- Two bib entries (jorgensenigel2021, hendrickx2024) spot-verified live against
  publisher/DOI records via web search, as an independent sanity check beyond the repo's own
  internal E7.2.1 correction record for dawidskene1979/rankgpt2023.
- Figure and package dependency check (manuscript/figures/*.pdf, usepackage list).

No file was modified. No git state was changed.

## 1. Scientific guardrails -- GREEN

- H1 status. Verified at every occurrence (lines 571-579, 799-807, 1149-1157, 1163-1169,
  1260-1269, 1406-1408): consistently reported as "PARTIALLY_SUPPORTED," explicitly contrasted
  with "confirmed"/"refuted" (line 1263-1264: "stated here as the honest verdict, not softened
  toward either confirmed or refuted") and with "not confirmed" restated in the Conclusion
  (line 1408: "H1 overall is only partially supported, not confirmed"). No upgrade or downgrade
  found anywhere.
- 6a/6b separation. Verified intact everywhere it matters: Section 3.4 (lines 546-558)
  states the distinction explicitly as two different claims with opposite truth values that
  "this paper never merges"; Results is split into Section 5.2 ("ADS Predicts Individual
  Mechanism Accuracy," lines 899-908) and Section 5.3 ("ADS Does Not Predict Mechanism
  Ranking," lines 925-938) as separate subsections; Discussion, Limitations, Future Work, and
  Conclusion each restate both halves separately rather than collapsing them (e.g. line
  1100-1104, line 1405-1409). No sentence found anywhere that states or implies "ADS predicts
  mechanism suitability" unqualified -- the exact forbidden collapse named in
  PAPER_CONTRACT.md Sec.3 row 13.
- No "ADS predicts ranking" claim. Every instance of "predict(s) which mechanism wins" is
  negated ("does not predict," lines 73, 925, 1099, 1404). The abstract's closing sentence
  (lines 81-86, the only text changed by the E7.5 commit) states "should not be used to predict
  which mechanism will win" and frames the two-feature-signal idea as an explicit, syntactically
  separate "Whether ... would ... is the direct next hypothesis this experiment motivates: no
  such selector was designed, prototyped, or tested here" -- correctly hedged as an untested
  open question, not a claim that such a selector would work.
- No universal-applicability claim. The four-precondition scope-bounding language (repeated
  historical decisions, observable labels, a measurable consistency statistic, sufficient
  historical coverage) recurs at lines 168-175, 456-467, and is never dropped. Line 175 states
  plainly: "where a real system does not [meet the four preconditions], the question this paper
  answers does not directly apply to it." Limitations Sec.7.4 (lines 1324-1334) restates "This
  paper makes no deployment or generalization claim."
- Production/client data never treated as evidence. Checked every production-figure mention
  (lines 103-120, 592-596, 1127-1140, 1308-1322): every single one carries an explicit "cited
  from a confidential engagement, not independently reproducible from this repository" (or
  equivalent) qualifier, and Discussion Sec.6.2 explicitly states "This experiment does not
  confirm the production observation" and "production never ran a lexical-noise sweep." The
  Reproducibility Statement (lines 1424-1442) repeats the same boundary. No sentence uses
  production figures as statistical support for 6a/6b.
- No unearned strength words. Grepped the full manuscript for
  prove/demonstrat/establish/validat/generaliz/robust/superior/optimal/reliab/shows/suggests/
  indicates/confirms. Every hit is either (a) describing what a cited external paper
  establishes/demonstrates (e.g. "citet{jorgensenigel2021} empirically demonstrates," line 399;
  "RankGPT ... establishes that," line 381), (b) explicitly negated ("not a validated selection
  method," line 232; "not a validated method," line 1417; "This experiment does not confirm,"
  line 1134; "Nothing here suggests that literature is wrong," line 1213), or (c) a plain
  description of a figure/table's contents ("Shows the factorial structure," line 839). No
  instance found where the paper asserts an unearned strength claim about its own contribution.
- Numbers verified against PAPER_CONTRACT.md Sec.7's canonical values, exactly:
  32/50=64.0%, Wilson CI [50.14%, 75.86%], p=0.0649 (line 976, Table T4); 32/32 (100%) at
  0.70-0.90, 0/18 (0%) at >=0.90 (lines 962-964, 973-974); Pearson r 0.909/0.959 (rules),
  0.948/0.955 (retrieval) (lines 903-905, Table T4); production 91.2%/0.847/0.964/0.695 (lines
  106, 593, 1310-1311); synthetic deterministic-share 87.56% (line 108) -- correctly the
  canonical post-A5-fix figure, never the superseded 84.12% figure. All match exactly; no
  number drift found.

One observation, not a manuscript defect: PAPER_CONTRACT.md Sec.2 row 9 itself cites
"84.1%" for the synthetic EMBEDDING_PRIMARY figure, which PAPER_CONTRACT.md's own Sec.7 lists
as the superseded pre-A5-fix value (84.12%) -- an internal inconsistency inside
PAPER_CONTRACT.md, not in the manuscript. main.tex correctly uses 87.56% (the canonical
value) throughout, so the manuscript is not the one carrying the stale figure. Flagged for
awareness only; no manuscript action needed.

## 2. Writing quality -- GREEN, one non-blocking note

No grammatical errors, broken terminology, or misleading wording found that would concern a
reviewer on substance. One legitimate formulaic-prose observation (see Sec.3 below) affects
register, not correctness. Sentences are long and heavily qualification-dense throughout (a
deliberate consequence of the paper's own anti-drift contract), which is internally consistent
rather than an authorial-voice defect, but a reviewer could reasonably ask for tighter prose in
places -- this is a taste note, not a correctness issue, and this audit does not recommend
cutting any of the qualifying language, since nearly all of it is scientifically load-bearing
per the guardrails checked in Sec.1.

## 3. AI-writing-pattern concerns -- ORANGE (non-blocking style note)

The Related Work section (Section 2) repeats the identical sentence-opener template "We do not
claim that ..." / "We make no claim that ..." six times within ~85 lines (lines 301, 318, 337,
353, 367, 384), once per cited-literature paragraph, plus two further "does not follow that ..."
instances in Discussion Sec.6.5 (lines 1224, 1226) and one "Nothing here suggests" (line 1213).
Each instance disclaims a different, specific misreading tied to a specific citation, so the
content is not redundant, and the pattern is largely scientifically necessary under this
project's own PAPER_CONTRACT.md negative-claims discipline -- but the literal repetition of
the same four-word opener six times in one section is the kind of templated scaffolding a
careful reviewer could flag as formulaic. This is a genuine, independently-observed pattern
(confirmed by direct grep, not inherited from the parallel session's own prior audit, which
separately flagged the same six sentences). Recommended direction for the human author: vary
the connective phrasing for at least two or three of the six instances (e.g. "This is not
evidence that ...", "None of this implies ...") while keeping every disclaimed proposition
itself unchanged -- a register fix, not a content or hedging change. Not a blocking issue for
submission.

## 4. Originality / source-overlap risk -- GREEN

- The cluster-purity formula restatement (lines 274-286) is a standard mathematical restatement
  of a well-known metric in the paper's own notation ("cluster" mapped to "an item's historical
  booking multiset"), not a copied passage of source prose -- low risk, consistent with how
  formulas are conventionally restated across a field.
- Spot-verified two of the less-common citations directly against live sources:
  - jorgensenigel2021 (Wiley, DOI 10.1002/isaf.1500, ISAFM vol 28(3), pp.159-172, 2021) -- bib
    metadata (author names, journal, volume/number/year/DOI) matches the publisher record
    exactly. The manuscript's characterization ("a global classifier generalizes far worse
    across companies than per-company models") is a reasonable, non-verbatim paraphrase
    consistent with the paper's actual finding.
  - hendrickx2024 (Springer, DOI 10.1007/s10994-024-06534-x, Machine Learning vol 113,
    pp.3073-3110, 2024; arXiv:2107.11277, 2021) -- bib metadata matches exactly, including the
    "arXiv preprint 2021" note.
  - dawidskene1979 and rankgpt2023 were already corrected and re-verified in the prior
    E7.2.1 pass (per the note fields in references.bib lines 64-66, 103-104); not
    re-litigated here beyond confirming the note fields are still present and unchanged.
- No passage in Related Work reads as close paraphrase of a specific source's distinctive
  sentence structure; every citation is used to state what the cited work establishes and then
  immediately, explicitly bound what this paper does/does not claim relative to it -- this is
  citation-then-scoping, not paraphrase-without-attribution.

## 5. references.bib metadata sanity -- GREEN

All 16 entries skimmed for venue/year/DOI plausibility against their citation context. No
mismatches found. Three industry-blog entries (kenfromfinance2025, peakflo2025, ramp2025)
are explicitly and correctly labeled "not peer-reviewed" both in the .bib note fields and in
the citing prose (main.tex line 405-409). frugalgpt2023's bib entry correctly notes the 2023
arXiv preprint / 2024 TMLR publication distinction. No DOI/venue anomaly identified in any entry
that would suggest a fabricated or mismatched reference.

## 6. Package/metadata boundary -- GREEN, one minor packaging-hygiene note

main.tex declares exactly five packages (amsmath, amssymb, graphicx, booktabs, natbib), all
used and all standard -- no unusual or unexplained dependency. All four referenced figures
(f1_design_flow.pdf through f4_ranking_constancy.pdf) exist in manuscript/figures/.
references.bib exists and is the only bibliography target. Minor note: a stray build
artifact, manuscript/figures/__pycache__/generate_figures.cpython-314.pyc, sits inside the
manuscript/ tree; if manuscript/ is packaged as-is for an arXiv source upload, this Python
bytecode cache would be swept in unless explicitly excluded. Not a manuscript-content issue,
but worth cleaning before packaging.

## Overall verdict

GREEN -- ready for RC1 sign-off, with two non-blocking notes for the human author to
optionally action before submission:

1. (Style, optional) Vary at least some of the six repeated "We do not claim that ..." openers
   in Section 2 (Related Work) to reduce template-repetition risk with a reviewer, without
   changing any disclaimed content.
2. (Packaging hygiene, optional) Remove manuscript/figures/__pycache__/ before assembling an
   arXiv source package.

No scientific guardrail violation, no semantic drift, no unresolved source-overlap risk, and no
numerical discrepancy was found anywhere in manuscript/main.tex or manuscript/references.bib
in this independent pass.

# E7.7.2 Independent Bibliography Sanitization Verification Audit

## 1. Scope

Fresh, independent, read-only review of the uncommitted working-tree diff on top of committed HEAD
bf3aa22 ("Phase E7.5: final manuscript editorial refinement"), spanning two modified files:
manuscript/main.tex and manuscript/references.bib. Ground truth was derived directly from
git diff -- manuscript/main.tex, git diff -- manuscript/references.bib, an independent diff
against git show bf3aa22:manuscript/references.bib as a cross-check, and a full read of both
files current contents. No prior audits description was trusted without re-derivation; the
pre-existing research/E7_7_INDEPENDENT_RC2_VERIFICATION_AUDIT.md (which covered only the
main.tex portion of this same diff, before the references.bib changes existed) was consulted only
after independently reproducing its findings, as a cross-check, per the tasks own instructions.

## 2. Independent Findings -- manuscript/main.tex

git diff -- manuscript/main.tex shows exactly three hunks, all deletions of trailing internal
pointer text with no other change to surrounding prose, grammar, or claims:

- Hunk 1 (Domain-Specific Practice paragraph, ~line 410): deletes the parenthetical
  (research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md Sec.4) following "...still-uncorrected item tracked
  outside this manuscript". The sentences claim (that a companion-report item remains open and
  uncorrected) is unchanged; only the internal-doc pointer is removed.
- Hunk 2 (Figure 1 caption, ~line 838-841): deletes "Source: research/EXPERIMENT_1_REDESIGN_REVIEW.md
  Sec.6, Sec.18." The captions substantive content (describing the pre-registration flow figure) is
  untouched.
- Hunk 3 (Figure 3 caption, ~line 993-996): deletes "Source: research/EXPERIMENT_1_POSTHOC_ANALYSIS.md
  Sec.4-5." The captions statistics (100 percent 32/32, 0 percent 0/18) are untouched.

No other line in main.tex differs from HEAD. This is confirmed to be exactly the three hunks
described in the tasks Step 2 scoping, verified directly from the diff, matching character-for-
character what was expected, and independently matching the previously-verified E7_7 audits own
description of this same main.tex diff (that audit reviewed this identical diff before the
references.bib changes were added; both audits derived it independently and agree).

## 3. Independent Findings -- manuscript/references.bib

git diff -- manuscript/references.bib shows exactly four hunks, one each in manning2008,
kenfromfinance2025, peakflo2025, and ramp2025. In every case, only a trailing "Ledger row:
research/literature/....csv, ..." clause was deleted from the note field:

- manning2008 (line 41): note changes from "Chapter 16.3 (cluster purity). Ledger row:
  research/literature/ads_metric_prior_art.csv, G1-01." to "Chapter 16.3 (cluster purity)."
- kenfromfinance2025 (lines 163-164): note drops "Ledger row: research/literature/citation_ledger.csv,
  B8-04.", retaining "Industry source, not peer-reviewed; undated, circa 2025, no DOI."
- peakflo2025 (lines 173-174): same pattern, drops "..., B8-05.", retains the identical
  industry-source-caveat sentence.
- ramp2025 (lines 183-184): same pattern, drops "..., B8-06.", retains "Industry source, not
  peer-reviewed; published 2025-11-03, no DOI."

A second, independently-derived confirmation was run using diff against git show
bf3aa22:manuscript/references.bib (a different tool than git diff, same comparison) and it
reproduces byte-identical output: exactly these four note-field lines differ, nothing else. Every
other field in these four entries (author, title, year, howpublished/publisher, url) is untouched.
No other bib entry in the file (rice1976, smithmiles2009, amigo2009, dawidskene1979, barbudo2023,
idreoskraska2019, frugalgpt2023, rankgpt2023, chow1970, elyaniv2010, hendrickx2024,
mozannarsontag2020, jorgensenigel2021) shows any diff at all. This matches the tasks Step 3
scoping exactly.

Checked research/PAPER_CONTRACT.md and research/CONTRIBUTION_LOCK.md for any rule requiring
ledger-row provenance pointers to remain in the bib note field: no such requirement exists in
either file (grep for "Ledger row"/"ledger row" returns no matches in either). Removing this
bookkeeping trace carries no contractual risk.

## 4. Field-Integrity Spot Check on the Four Touched Entries

Read the four entries surviving fields directly (manuscript/references.bib lines 36-42, 157-182):

- manning2008: Manning, Raghavan, Schutze, Introduction to Information Retrieval, Cambridge
  University Press, 2008, a real, well-known IR textbook; Chapter 16.3 covers cluster evaluation,
  consistent with the retained note "Chapter 16.3 (cluster purity)."
- kenfromfinance2025: author "Ken From Finance", title "Invoice GL Coding Automation: Workflow and
  Controls," howpublished "Practitioner blog, kenfromfinance.com," url
  https://www.kenfromfinance.com/blog/invoice-gl-coding-automation, domain, URL slug, and stated
  venue are internally consistent (a practitioner blog post on the vendors own domain).
- peakflo2025: author "Peakflo", title "How to Automate GL Coding for Non-PO Invoices," howpublished
  "Vendor blog, peakflo.co," url https://peakflo.co/blog/gl-coding-automation-non-po-invoices,
  consistent.
- ramp2025: author "Ramp", title "What Are the Best Practices for Using AI Agents in AP?",
  howpublished "Vendor blog, ramp.com," url https://ramp.com/blog/agentic-ai/best-practices-for-ap-agents,
  consistent.

Because the diff confirms these fields are byte-identical to their state at HEAD (bf3aa22), and
that prior state was itself the product of an earlier verification pass (E5.2 correction work,
per the files own header comment at lines 153-155 referencing "E5.2's correction pass"), no new
bibliographic-accuracy risk is introduced by this note-trimming pass. This spot check is an
internal-consistency check (author/venue/URL/title cohere), not a fresh independent web
verification of each source; live-fetch verification of these four URLs was not performed for this
narrowly-scoped pass and is marked UNVERIFIED rather than assumed correct.

## 5. Citation-Key Resolution Check

Extracted every \citep{}/\citet{} key from main.tex and every @entry{key from references.bib
independently and diffed the two sorted sets: they are identical (17 keys each: amigo2009,
barbudo2023, chow1970, dawidskene1979, elyaniv2010, frugalgpt2023, hendrickx2024, idreoskraska2019,
jorgensenigel2021, kenfromfinance2025, manning2008, mozannarsontag2020, peakflo2025, ramp2025,
rankgpt2023, rice1976, smithmiles2009). Every citation used in the prose resolves to a bib entry;
no broken reference.

## 6. Remaining Visible Internal-Path Sweep

manuscript/main.tex: Grepped the full file for research/, scripts/, .git/, STATE.md, ROADMAP.md,
PAPER_CONTRACT.md, CONTRIBUTION_LOCK.md, EVIDENCE_BASELINE.md. Every hit (roughly 115 occurrences)
sits on a line beginning with percent (a LaTeX comment, invisible in the compiled PDF), checked
line-by-line against the grep output, all confirmed comment lines. The two non-comment hits (lines
819 and 1428) are "python scripts/experiments/exp1/run_final.py" in the Reproducibility subsection
and Reproducibility Statement, the explicitly-permitted, README-documented public reproduction
command, not a leak. Two other visible, non-flagged paths remain in Figure 2 and Figure 4 captions
(lines 918-919, 948-949): "Source: data/outputs/experiments/exp1/final/final_condition_results.csv",
this string contains data/, not any of the eight flagged patterns, and points to a public,
git-tracked CSV artifact (confirmed present on disk under data/outputs/experiments/exp1/final/).
This is outside the scope of both the flagged-pattern list and this passs stated three-hunk edit
(F2/F4 captions were not touched by this diff), so it is not treated as a finding, only noted for
completeness.

manuscript/references.bib: Grepped the full file for the same eight patterns: 4 hits, all on
lines 3, 4, 13, and 154, all inside percent-prefixed BibTeX-level header/section comments (outside
any entry block), never rendered in a compiled bibliography. Zero occurrences remain inside any
author/title/note/url/other field of any entry. This confirms the sanitization pass achieved its
stated goal for this file: all four ledger-row pointers that previously sat inside live note fields
are now gone, and no other in-field leak exists or was ever present elsewhere in this file.

## 7. Scientific Guardrail Verification

Read the full manuscript (all 1478 lines) directly, independent of the diff, to confirm guardrails
hold in the current state (not merely "unaffected by the diff," since none of these lines fall
inside any of the seven changed hunks, but re-verified by direct reading regardless):

- H1 PARTIALLY_SUPPORTED, not upgraded: explicit at lines 570-578 (pre-registration wording),
  798-806 (falsification-table outcome), 1146-1154 ("This result is not without value, but it is
  not evidence that H1 as originally intended was confirmed"), 1257-1266 (Limitations subsection
  titled "H1 Only Partially Supported"), 1405 ("H1 overall is only partially supported, not
  confirmed").
- 6a/6b kept separate: Section 5.2 (line 897, "ADS Predicts Individual Mechanism Accuracy") and
  Section 5.3 (line 923, "ADS Does Not Predict Mechanism Ranking") remain two distinct
  subsections; lines 220-223 state explicitly "These are two different claims, with two different
  (here, opposite) answers, and this paper never merges them into a single statement..."
- No ADS-predicts-ranking claim: every occurrence of "mechanism ranking" in visible prose is
  negative ("does not predict," "Does Not Predict Mechanism Ranking," line 925 "Realized ADS does
  not predict which mechanism wins").
- No universal/general-purpose claim: lines 81, 1223-1230 ("Four inferences this experiment does
  not license..."), 1329 ("This paper makes no deployment or generalization claim") all present
  and intact.
- No novelty inflation: line 283 ("we therefore make no claim that ADS is a novel metric"), lines
  301-302 ("We make no claim that design-time selection from historical evidence is itself new").
- Production data non-evidentiary throughout: lines 116-120, 262, 592-593, 821-827
  (Reproducibility Statement explicitly separates public code from confidential production data),
  1131-1137, 1305-1315, 1430-1434 all consistently frame the production case study as confidential,
  cited-not-reproduced, non-evidentiary.
- Canonical numbers unchanged: spot-checked 64.0% (32/50), Wilson CI [50.14%, 75.86%], p=0.0649,
  by-target 30/30 (p=1.9e-9), 2/20 (p=4.0e-4), per-row bands 32/32 and 0/18, Pearson r 0.909/0.959
  (rules) and 0.948/0.955 (retrieval), production 91.2%/weighted ADS 0.847/unweighted ADS 0.964,
  synthetic corrected 87.56%, all present, all matching research/EVIDENCE_BASELINE.md-class
  canonical values, none inside any changed hunk.

No guardrail violation found. Both diffs are pure metadata/provenance-pointer deletions; neither
touches a scientific claim, a statistic, a hedge, or locked contribution language.

## 8. Regression Check

Compared against research/E7_7_INDEPENDENT_RC2_VERIFICATION_AUDIT.md, the most recent prior audit
covering the main.tex portion of this diff (GREEN verdict, main.tex-only scope, references.bib not
yet modified at that time). Independently re-deriving the main.tex diff here reproduces that
audits findings exactly (same three hunks, same line ranges, same guardrail conclusions), no
regression. The references.bib changes are new since that audit and were not previously reviewed;
this pass is the first independent verification of them. No discrepancy found between this passs
independent findings and the prior passs main.tex findings.

## 9. Verdict

GREEN.

Both diffs are exactly and only what the task described: main.tex's three hunks delete trailing
internal-document pointers (a parenthetical citation and two figure-caption "Source:" sentences)
without altering any surrounding claim, statistic, or grammar; references.bib's four hunks delete
only a trailing "Ledger row: research/literature/....csv, ..." clause from the note field of
manning2008, kenfromfinance2025, peakflo2025, and ramp2025, with every other field in those
entries and every other entry in the file byte-identical to HEAD (confirmed via two independent
diff methods). All citation keys resolve. All scientific guardrails (H1 status, 6a/6b separation,
no ranking-prediction claim, no universality claim, no novelty inflation, production data flagged
non-evidentiary, canonical statistics) are intact and unaffected. An exhaustive sweep of both
files for the eight specified leak patterns found zero remaining visible (non-comment, in-field)
occurrences; all surviving research/-prefixed references sit in LaTeX or BibTeX comments, and the
two legitimate scripts/...run_final.py reproduction-command mentions are explicitly permitted.
This is a clean, narrowly-scoped bibliography/caption sanitization pass with no scientific,
attribution, or leak risk. No human decision is required beyond routine acceptance; the only
unverified (not incorrect, simply not re-checked) item is that this pass did not perform a fresh
live-fetch verification of the four touched bib entries source URLs, since their fields were
already byte-identical to a previously-verified state.

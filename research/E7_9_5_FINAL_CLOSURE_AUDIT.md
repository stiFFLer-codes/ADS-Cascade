# E7.9.5 Final Closure Audit (blocking-defects-only)

## Scope
Final pre-submission scan of manuscript/main.tex and manuscript/references.bib in their
current working-tree state (git diff HEAD reviewed) against research/EVIDENCE_BASELINE.md,
research/CONTRIBUTION_LOCK.md, and research/PAPER_CONTRACT.md. Blocking-defects-only mode:
no stylistic/polish findings recorded.

## Checks performed and results
1. Forbidden claims (PAPER_CONTRACT.md Sec.3): none found. Grep for
   novel|validated|proves|demonstrat*|establish*|robust*|superior|optimal|reliable|generalizab*
   shows every instance is either a citation to prior literature, an explicit negation
   ("no claim that ADS is a novel metric", "not a validated method"), or a scoped/hedged use.
2. Numerical claims vs. EVIDENCE_BASELINE.md / PAPER_CONTRACT.md Sec.7: all canonical values
   (91.2% production deterministic, weighted/unweighted ADS 0.847/0.964, synthetic 87.56%
   deterministic share, cross-company alignment 0.695, Pearson r 0.909-0.959 rules /
   0.948-0.955 retrieval, R3 band agreement 32/32 and 0/18, overall 32/50=64.0%,
   Wilson CI [50.14%,75.86%], p=0.0649, delta=0.02, cutoff=75, R3 thresholds 0.90/0.70)
   match exactly. No number changed via the current diff.
3. H1 status: stated as "only partially supported" (Sec.7.1), matches pre-registered
   PARTIALLY_SUPPORTED row; not upgraded anywhere.
4. 6a/6b distinction: kept separate throughout Sec.3.4, 5.2-5.3, 5.7, 6.1, 6.4; never merged.
5. No claim that ADS predicts mechanism ranking; explicitly and repeatedly negated.
6. No universal/general-purpose selection claim; scope bounded to the four preconditions
   throughout.
7. ADS novelty: explicitly disclaimed (cluster purity / majority-vote-agreement equivalence).
8. Production data: every appearance (Sec.1.1, 6.2, 7.4, Reproducibility Statement) carries
   the "cited from a confidential engagement, not independently reproducible" qualifier;
   never used as Results-section statistical evidence.
9. Citation-key resolution: all 17 \citep/\citet keys in main.tex
   (rice1976, smithmiles2009, manning2008, amigo2009, dawidskene1979, barbudo2023,
   idreoskraska2019, chow1970, elyaniv2010, hendrickx2024, mozannarsontag2020,
   frugalgpt2023, rankgpt2023, jorgensenigel2021, kenfromfinance2025, peakflo2025,
   ramp2025) resolve to entries in references.bib; no orphaned keys either direction.
10. Exposed paths: no local/Windows machine paths in reader-facing prose. The
    Reproducibility Statement's public repo reference (github.com/stiFFLer-codes/ADS-Cascade,
    data/outputs/experiments/exp1/final/) was verified against `git remote -v` and the
    actual committed directory contents -- accurate, intentional, not a confidentiality leak.
11. \ref{} targets: tab:t5 (x2) both resolve to an existing \label; no dangling refs.
    The Sec.4.1 -> Sec.7.3 cross-reference fix in this diff was checked against actual
    section content -- 7.3 ("Domain and Mechanism Scope") is where the LLM-exclusion
    rationale lives; 4.1 ("Research Hypothesis") was the wrong target. This is a
    correction, not a regression.

## Diff-specific review (git diff HEAD)
All changes in the current working tree are: (a) repeated "We do not claim X" ->
"X is not offered as" rephrasings with unchanged negation/semantic force, (b) the
Sec.4.1->7.3 cross-reference fix (correct), (c) one added sentence in Sec.6.4 restating
the widening rules-minus-retrieval gap under VARIED, checked against Table T5's own
values (-0.137 -> -0.168 -> -0.185) -- consistent, not a new/stronger claim, (d) a
\begin{sloppypar} typesetting wrapper around the Reproducibility Statement, (e) an
expanded Reproducibility Statement naming the actual public GitHub repo path (verified
accurate), (f) two added `pages` fields in references.bib (idreoskraska2019,
jorgensenigel2021) and minor note-text simplification, (g) a comment-only title-lock
note (does not render). None of these introduce a numerical, scope, or claim-strength
change.

## Verdict
GREEN -- no submission blockers found.

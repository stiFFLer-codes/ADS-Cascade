# E7.2.1 — Independent Audit: Bibliography Metadata Correction (references.bib)

**Scope:** Narrow, isolated review of a single uncommitted change to
`manuscript/references.bib` (two entries: `dawidskene1979`, `rankgpt2023`). Per the
requesting agent's instruction, this audit does **not** re-cover the rest of the manuscript
or repo — that was covered by the prior `research/E7_2_RELEASE_BOUNDARY_AUDIT.md` pass.

## 1. Repository state

- Branch: `main`. HEAD: `8c214e092f3ffe024fa38044556be1e5edbe8e1d` ("Phase E7.1: manuscript
  author metadata + AI-assistance disclosure") — matches the commit cited in the request.
- Working tree: dirty. Exactly one tracked file modified: `manuscript/references.bib`.
- Untracked files present (`research/E4_*`, `research/E5_*`, `research/E7_2_RELEASE_BOUNDARY_AUDIT.md`,
  etc.) are pre-existing audit-trail artifacts from prior passes, not part of this diff, and
  out of scope per the request.
- Diffed via `git diff -- manuscript/references.bib` and `git diff --stat HEAD` (confirms
  `references.bib` is the only tracked file changed anywhere in the repo since HEAD).

## 2. Changed files

- **Manuscript (bib only):** `manuscript/references.bib` — 11 insertions, 9 deletions, two
  entries touched (`dawidskene1979`, `rankgpt2023`). No `.tex` files changed.
- **Code:** none changed.
- **Experimental artifacts:** none changed.
- **Ledgers:** none changed — verified `research/literature/citation_ledger.csv`,
  `ads_metric_prior_art.csv`, `llm_advisory_prior_art.csv` all show zero diff from HEAD.
- **Other:** none.

## 3. Independent verification of the two corrected entries

### 3.1 `dawidskene1979`

Committed values: `volume=28`, `number=1`, `pages=20--28`, `doi=10.2307/2346806`.

Independently re-derived (not trusting the request's summary) via web search across
Oxford Academic (`academic.oup.com/jrsssc/article/28/1/20/6953573`), JSTOR
(`jstor.org/stable/2346806`), and Wiley Online Library
(`rss.onlinelibrary.wiley.com/doi/abs/10.2307/2346806`), all independently agreeing:
Dawid, A. P. & Skene, A. M. (1979), "Maximum Likelihood Estimation of Observer Error-Rates
Using the EM Algorithm," *Journal of the Royal Statistical Society, Series C (Applied
Statistics)*, Vol. 28, No. 1, pp. 20–28. DOI `10.2307/2346806` resolves (redirects to the
JSTOR record for this exact article), confirming the DOI-to-article binding.

**Result: exact match, fully verified from primary/authoritative sources, not merely
plausible.**

### 3.2 `rankgpt2023`

Committed values: full 8-author list (Sun, Weiwei; Yan, Lingyong; Ma, Xinyu; Wang,
Shuaiqiang; Ren, Pengjie; Chen, Zhumin; Yin, Dawei; Ren, Zhaochun), `pages=14918--14937`.

Independently fetched the ACL Anthology record directly
(`aclanthology.org/2023.emnlp-main.923/`) and pulled its own published BibTeX entry
(`sun-etal-2023-chatgpt`). The author order, all eight names, and the page range
`14918--14937` are byte-for-byte identical to what was committed. `doi =
10.18653/v1/2023.emnlp-main.923` (unchanged by this diff) also matches the Anthology
record.

**Result: exact match, fully verified from the authoritative source (not a mirror or
secondary citation).**

## 4. In-text citation accuracy (did the edit silently repoint a claim)

Grepped `manuscript/main.tex` for both keys — three citation sites, none touched by this
diff (only `references.bib` changed):

- Line 278/484: `\citet{dawidskene1979}` — cited as the origin of "the raw majority-vote
  agreement proportion used throughout the crowdsourcing and truth-inference literature,"
  in the context of the paper's own ADS-is-not-novel argument (explicitly disclaiming
  novelty, citing Dawid & Skene 1979 alongside cluster purity as prior art). This
  correctly represents what the paper is (an EM-based observer-error-rate/truth-inference
  method) and matches the project's settled ADS-rejected-as-novel-metric framing — no drift,
  no resurrection of the rejected claim.
- Line 378: `\citep{rankgpt2023}` — cited for the claim "using a large language model to
  re-rank a pre-fetched candidate list, rather than to classify from a blank input, is [a]
  commodity information-retrieval technique," immediately followed by an explicit disclaimer
  that Experiment 1's mechanism comparison is not itself a cascade contribution. This
  matches RankGPT's actual subject (LLM re-ranking for search) — correctly used.

Both citation sites are semantically correct for what these sources actually are/say.
Since the diff only touched `references.bib` and not `main.tex`, there is no mechanism by
which this edit could have repointed a claim — confirmed by inspection, not merely by
absence of a `main.tex` diff.

## 5. Completeness / no scope creep

- `git diff --stat HEAD`: exactly one file changed, `manuscript/references.bib`
  (11 insertions, 9 deletions) — no manuscript prose, no other bib entries, no ledger CSVs
  touched.
- Entry count unchanged: 17 `@`-entries in the file both before and after (grepped `^@`
  count on current file = 17; diff shows no `@`-line insertions/deletions, only field edits
  inside the two pre-existing entries).
- No leftover `TODO` literals in any entry field (the one remaining `TODO` string in the
  file is the unrelated file-header policy comment at line 7, explaining the original
  convention — not a placeholder in live entry data).
- Both corrected entries carry inline provenance notes (`note = {Verified E7.2.1 against
  ...}`) documenting the source used, consistent with this repo's ledger-verification
  convention.

## 6. Docker build claim (not independently re-run, per instructions)

The request states the manuscript was compiled (bibtex + 2x pdflatex passes) inside the
pinned `texlive/texlive:TL2025-historic` image with a clean exit and no undefined-citation
warnings, and that the corrected entries were visually confirmed in the rendered
bibliography. This was not independently re-run (out of scope per the request — "you don't
need to re-run the Docker build"). Given that (a) the `.bib` syntax in the diff is
well-formed (balanced braces, correct field separators, valid BibTeX entry types), (b) no
`.tex` files changed so no new `\cite` keys could be dangling, and (c) both corrected
entries' new field values are exactly what the primary sources report, the claim is
plausible and consistent with what a clean build would be expected to produce. This is
**unverified by this audit** (not independently re-run) — the plausibility assessment is
inference, not direct verification, and is reported as such.

## 7. Git hygiene

- `git status --porcelain` shows exactly one modified tracked file
  (`manuscript/references.bib`) plus a set of untracked, pre-existing audit `.md` files
  unrelated to this diff (not staged, not touched by this session).
- No secrets, credentials, API keys, or bearer tokens present in the diff (diff is pure
  bibliographic metadata: numbers, author names, a DOI string, and a provenance note).
- No client/production data or real-company names introduced (the two sources are public
  academic papers, consistent with the rest of the public bibliography).
- No local Windows paths or usernames leaked into the diff.
- No `.bak`/`.swp`/`.orig`/`.tmp` files present.
- `README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md` untouched — consistent with a
  bib-only pass.
- Nothing was staged or committed by this audit; only `research/E7_2_1_BIB_CORRECTION_AUDIT.md`
  (this file) was written, per the audit-trail convention and the constraint against
  modifying anything else.
- A safe `git add` for this checkpoint would be: `git add manuscript/references.bib` only
  (plus this audit file, if the project's convention is to check audit files in alongside
  their corresponding change — the requester should confirm that convention rather than
  this audit deciding it).

## 8. Findings

- **REQUIRED NOW:** none.
- **OPTIONAL FUTURE WORK:** none — this is a complete, self-contained, correctly-scoped
  metadata fix with no residual issues identified.

## 9. Required fixes

None. Empty — no REQUIRED NOW findings.

## 10. Verdict

**🟢 PASS**

Both corrected bibliographic entries were independently re-derived from authoritative
primary sources (Oxford Academic/JSTOR/Wiley for Dawid & Skene 1979; the ACL Anthology's
own published BibTeX for RankGPT/Sun et al. 2023) and match the committed values exactly —
volume, issue, pages, and DOI for the first; full 8-author order and page range for the
second. The diff is bib-only, touches no other file (ledgers, prose, and other bib entries
all confirmed unchanged via `git diff --stat`), does not alter any in-text citation
semantics (both citation sites were independently re-read and correctly represent what
these sources are/say, consistent with the project's settled ADS-not-novel framing), and
leaves no leftover placeholder data. Git hygiene is clean: no secrets, no scope creep, no
unrelated files touched. The only unverified element is the Docker build/compile claim,
which was explicitly out of scope for this audit per the request and is assessed as
plausible by inference rather than direct re-run — this does not block the verdict, since
the underlying `.bib` change is independently confirmed correct regardless of build-log
inspection. Safe to commit as its own isolated commit.

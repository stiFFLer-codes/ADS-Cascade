# Manuscript Skeleton Audit (Phase E2)

> Independent audit of `manuscript/main.tex` and `manuscript/references.bib` against
> `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, and
> `research/MANUSCRIPT_ARCHITECTURE.md`. Every check below was re-derived from source documents
> directly (grep, line-count, cross-reads of `EXPERIMENT_1_POSTHOC_ANALYSIS.md`,
> `EXPERIMENT_1_FINAL_RESULTS.md`, `citation_ledger.csv`, `ads_metric_prior_art.csv`), not taken on
> the implementing session's word. No file was modified except this one. No frozen evidence,
> `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`, or any of the four protected audit reports
> (`AUDIT_REPORT.md`, `PAPER_CONTRACT_AUDIT_REPORT.md`, `E0_CHECKPOINT_AUDIT.md`,
> `MANUSCRIPT_ARCHITECTURE_AUDIT.md`) was touched.
>
> **Resolution note (added after this audit ran):** the one REQUIRED NOW finding below (the missing
> Discussion subsection positioning the production case study relative to 6a/6b) and both
> non-blocking notes (the undocumented Results-subsection-count deviation; the over-specified
> `rankgpt2023` author field) were fixed directly in `manuscript/main.tex` and
> `manuscript/references.bib` immediately after this report was written. A separate, independent
> final-checkpoint audit (`research/E2_FINAL_CHECKPOINT_AUDIT.md`) re-verified all three fixes from
> the current file state and returned PASS\_WITH\_NOTES. This report's verdict below (CONDITIONAL)
> reflects the files' state *at the time of this review*, not their current, fixed state.

---

## 1. Section hierarchy vs. `MANUSCRIPT_ARCHITECTURE.md`

Top-level structure: **PASS.** Counted directly from `main.tex`:

| Section | Expected (per task brief) | Counted in `main.tex` |
|---|---:|---:|
| Introduction | 9 | 9 |
| Related Work | 8 | 8 |
| Problem Setting and Signal Definition | 5 | 5 |
| Experimental Design | 14 | 14 |
| Results | 7 | 7 |
| Discussion | 8 | 8 |
| Limitations | 10 | 10 |
| Future Work | 6 | 6 |
| Conclusion | (1, no subsections) | 1 |

The two pre-authorized top-level merges from `MANUSCRIPT_ARCHITECTURE.md` §3.1 (Problem
Setting+Method merged; Results kept as one section, not split into "accuracy" vs. "ranking") are
both correctly implemented — no third top-level section was invented, none renamed beyond the
"classifier→mechanism" swap (which is separately justified in the file header, see §7 below).

**Note (non-blocking) — Results subsection reorganization relative to `MANUSCRIPT_ARCHITECTURE.md`
§4:** the architecture's own detailed Results plan (§4) names exactly six subsections (§5.1
Overview/regime structure, §5.2 A—accuracy, §5.3 CLEAN-vs-VARIED, §5.4 B—ranking, §5.5
mechanism-winner+R3-agreement-by-region, §5.6 uncertainty). `main.tex` instead ships seven: it adds
a new lead-in ("Experimental Completeness and Frozen Design") and a new bridge close ("Summary of
Findings"), folds the architecture's planned §5.3 (CLEAN-vs-VARIED winner-constancy) into the same
subsection as §5.4 (the negative ranking claim itself, using the former as the latter's evidentiary
basis — a reasonable pairing since both are evidence for 6b), and splits the architecture's planned
§5.5 into two: "R3 Threshold Agreement by Realized-ADS Region" and "ADS × Representation-Stability
Interaction." `MANUSCRIPT_ARCHITECTURE.md` §3.1 pre-authorizes only *top-level* section merges, not
this *subsection*-level restructuring, and `main.tex` does not comment anywhere that it is deviating
from the architecture's named subsection list. That said: every substantive requirement survives
the reshuffle — 6a and 6b are never merged into one sentence (verified, §3 below), the band
structure still precedes the flat aggregate, and no evidence source or number changed. This is a
structural-fidelity note, not a content or integrity problem. **OPTIONAL FUTURE WORK.**

---

## 2. `PAPER_CONTRACT.md` §3 forbidden-phrase compliance

**PASS.** Grepped `main.tex` for: `novel metric`, `universally selects`, `enterprise AI`,
`independently validat*`, `proves that`, `consistency alone is sufficient`, `means rules is
better`, `equivalent in general`, `no comparable vendor`, `no vendor`, `typically ship a single`,
`55,394`, `validated as an effective`, `hybrid classification-system composition`. Every hit sits
inside an "OUR NON-CLAIM:" line, a "MUST NOT SAY:" line, or an explicit negated sentence (e.g. "...
production data does **not** independently validate this experiment's finding, and this must never
be implied."). No forbidden claim is asserted as positive content anywhere in the file. The
`~55,394` figure and the vendor-practice sentence (`PAPER_CONTRACT.md` §3 rows 14–15) do not appear
at all.

---

## 3. Accuracy-vs-ranking distinction (6a/6b) preserved

**PASS.** `\subsection{ADS Predicts Individual Mechanism Accuracy}` (Results §5.2, 6a) and
`\subsection{ADS Does Not Predict Mechanism Ranking}` (Results §5.3, 6b) are genuinely separate
subsections with separate draftnotes, evidence anchors, and MUST-NOT-SAY lines. The same split is
repeated in Problem Setting (§3.5, "Mechanism Accuracy vs. Mechanism Ranking" — states the
distinction formally before any result), in Introduction §1.7 ("These two claims are never merged
into one sentence"), and in Discussion (§6.1 states the synthesis; the individual "got right" /
"got wrong" halves are further separated in §6.2/§6.3). No draftnote anywhere collapses the two
into a single "ADS predicts mechanism suitability" sentence — every subsection that touches this
explicitly forbids exactly that phrase (`PAPER_CONTRACT.md` §3 row 13).

---

## 4. Production evidence is motivation-only, never in Results

**PASS (with one placement gap, see below).** Direct grep of `main.tex` for the production numbers
(`91.2%`, `0.847`, `0.964`, `0.695`, `84.1%`, `87.56%`, `76,843`) found them **only** in: the
Abstract's explicit "must stay in body only" exclusion note, Introduction §1.1 (correctly caveated
"likely understated, unverified"), Experimental Design §4.2 (the `0.695` cross-company-alignment
*generator parameter*, not a production citation — a frozen synthetic-design nuisance value, not
Results evidence), and Limitations §7.6/§7.7 (correctly caveated, correctly stating production
"does not independently validate" the finding). **Zero occurrences inside the Results section**
(§5, lines ~1043–1286) — confirmed by direct read, not just grep-absence.

**Finding (CONDITIONAL-level gap):** `MANUSCRIPT_ARCHITECTURE.md` §6 explicitly requires a
*dedicated* Discussion placement: "Discussion (§6.1 or a clearly labeled short subsection): one
paragraph noting that the production observation is *consistent with* 6a ... but was never itself
a controlled test of 6b ... explicitly framed as 'this experiment does not confirm the production
observation, it investigates the more general question the observation raised.'" No Discussion
subsection in `main.tex` carries this content or cites its evidence sources
(`EVIDENCE_BASELINE.md` §1, `r3_threshold_analysis.md`). The closest existing content is §6.7
("What Practitioners Should NOT Infer" — "Do not infer that production data confirms this
finding"), which is a negative disclaimer, not the architecture's requested affirmative
"consistent-with-6a-but-not-a-test-of-6b" positioning paragraph. Since none of the eight Discussion
draftnotes' ALLOWED EVIDENCE lists cite `EVIDENCE_BASELINE.md` or `r3_threshold_analysis.md`, an
E3 drafter following only the skeleton's draftnotes (as the file's own header instructs: "E3
drafting must replace the draftnote content with real prose that satisfies exactly what the block
specifies") would have no scaffolded reason to write this required paragraph. **REQUIRED NOW** —
add either a ninth Discussion subsection or an explicit key point to an existing one (§6.1 is the
architecture's own suggested slot) instructing this exact content before treating the skeleton as
E3-ready.

---

## 5. Numerical spot-checks

**PASS — all independently re-verified against source artifacts, not just against the skeleton's
own internal consistency.**

- **Pearson r ranges:** `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §11 states r(ADS, rules_acc) = 0.96
  (CLEAN) / 0.91 (VARIED); r(ADS, retrieval_acc) = 0.95 (CLEAN) / 0.95 (VARIED) — consistent with
  `CONTRIBUTION_LOCK.md` §4's more precise 0.959/0.909 and 0.955/0.948. `main.tex` §5.2's draftnote
  states "0.909 (VARIED) / 0.959 (CLEAN)" for rules and "0.948 (VARIED) / 0.955 (CLEAN)" for
  retrieval — exact match, both conditions reported side by side as required.
- **32/32 vs. 0/18 (realized-ADS-band split) vs. 30/30 vs. 2/20 (by-nominal-target split):** both
  independently confirmed. `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9 gives the 100% (32/32) / 0% (0/18)
  per-row realized-ADS-band split; `EXPERIMENT_1_FINAL_RESULTS.md` §5 (lines 142–144) gives the
  100% (30/30 across targets 0.50+0.75) / 10% (2/20 at target 1.00) by-nominal-target split.
  `main.tex` §5.4's draftnote correctly labels the 32/32-vs-0/18 framing PRIMARY ("matches R3's own
  actual mechanism — CONTRIBUTION_LOCK.md's locked wording") and the 30/30-vs-2/20 framing
  SECONDARY, and states the exact reason they differ (nominal target and per-row realized ADS
  don't always coincide at the two boundary-straddling targets, §4.4) — matching
  `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §10's own explanation precisely.
- **Six-row ADS-band gap table:** `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5 gives VARIED gaps
  −0.1374 / −0.1678 / −0.1851 (rounds to −0.137/−0.168/−0.185, matching `main.tex` §5.5 exactly)
  and CLEAN gaps +0.0048 / +0.0055 / +0.0063 (rounds to +0.005/+0.005/+0.006, matching `main.tex`'s
  "+0.005 to +0.006" statement).
- **Aggregate 64.0%/32/50/Wilson CI/p:** `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4 and
  `PAPER_CONTRACT.md` §7 both give 32/50 = 64.0%, Wilson CI [50.14%, 75.86%], p=0.0649 — matches
  `main.tex` verbatim everywhere it appears (Abstract exclusion note, §5.4, §5.6).

---

## 6. `references.bib` vs. the literature ledger

**PASS, with one minor drafting overreach.** All 14 entries cross-checked line-by-line against
`research/literature/citation_ledger.csv` and `research/literature/ads_metric_prior_art.csv`
(rows G1-01 through G1-04) for author/title/year/venue/DOI:

- `rice1976`, `smithmiles2009`, `manning2008`, `amigo2009`, `barbudo2023`, `idreoskraska2019`,
  `chow1970`, `elyaniv2010`, `hendrickx2024`, `mozannarsontag2020`, `jorgensenigel2021` — every
  field matches its ledger row exactly (verified individually; DOIs, volumes, page ranges, venue
  names all match).
- `dawidskene1979` — volume/number/pages/DOI correctly left as `TODO` in the `.bib` entry with an
  inline note pointing to ledger row G1-04 ("no DOI independently resolved in this pass") — exactly
  the required behavior (no guess where the ledger itself didn't resolve the field).
- `frugalgpt2023` — matches ledger row B3-02 (year framing, TMLR venue, arXiv URL) exactly.
- `rankgpt2023` — DOI and title match ledger row G2-01 (`research/literature/llm_advisory_prior_art.csv`)
  exactly. **Minor finding:** the `.bib` entry expands the ledger's abbreviated author list ("Sun,
  Yan, Ma, et al.") into full given names ("Sun, Weiwei and Yan, Lingyong and Ma, Xinyu and
  others"). The given names are not independently verified by either ledger row and are supplied
  from outside the verified evidence chain, contrary to the "no field guessed" standard applied
  correctly everywhere else in this file (compare `dawidskene1979`'s TODO treatment). The entry
  does carry a note flagging the list as "abbreviated per the literature ledger ... expand before
  E5," which mitigates but does not fully resolve this — the note describes the abbreviation, it
  does not mark the expanded first names themselves as unverified. **OPTIONAL FUTURE WORK** (low
  severity: the names are in fact correct for this well-known paper, and the note already
  earmarks the field for E5 re-verification), but noted because it is a real, if small, deviation
  from the "TODO, don't guess" rule this file otherwise follows perfectly.

Citation-key resolution: extracted all `\citep{...}` keys from `main.tex` — 14 unique keys, exactly
matching the 14 `@`-entries in `references.bib`. No undefined citation, no orphan bib entry (every
entry is cited at least once; `\nocite{*}` additionally forces the full set to render regardless).

---

## 7. Title terminology

**PASS.** Title uses "Mechanism," not "Classifier" ("Historical Consistency Predicts Mechanism
Accuracy, Not Mechanism Ranking: Evidence from a Controlled Synthetic Study" — candidate #1 from
`MANUSCRIPT_ARCHITECTURE.md` §1, with the classifier→mechanism substitution). The file's opening
comment block (lines 15–26) records the rationale directly and correctly: every locked evidence
document uses "mechanism" exclusively, and "classifier" is flagged as technically loose (the rules
mechanism is exact-match lookup, not a trained classifier). No third framing introduced.

---

## 8. Figure/table placeholders

**PASS.** Every `% FIGURE Fn` / `% TABLE Tn` comment block was checked against
`MANUSCRIPT_ARCHITECTURE.md` §7 (figures) and §8 (tables):

- F1 (design flow, Experimental Design), F2 (ADS-vs-accuracy, after §5.2), F3 (R3 agreement by
  region, after §5.4), F4 (winner-constancy, after §5.3) — all four present, all `REQUIRED`,
  purpose/source-artifact/expected-variables all match the architecture's table row-for-row.
- T1 (production snapshot, optional, Introduction), T2 (literature positioning, required, Related
  Work), T3 (experimental configuration, required, Experimental Design), T4 (main results,
  required, Results), T5 (mechanism-winner-by-region, required, Results), T6 (limitations summary,
  optional, Limitations) — all present with matching purpose/source/required-optional status.
- F5 ("candidate — table preferred") correctly has **no** corresponding figure — only T5 exists,
  matching the architecture's explicit decision to keep this as a table, not a figure.
- F6 ("candidate — rejected") is correctly **absent entirely** — matches the architecture's
  rejection of this figure.
- Confirmed via direct grep: zero occurrences of `\includegraphics`, `\begin{table}`, or
  `\begin{tabular}` anywhere in the file — every figure/table reference is a comment placeholder
  only, no fabricated content.

---

## 9. No frozen artifact modified

**PASS.** `git status --porcelain` shows only untracked additions: `manuscript/` (this pass's new
files) plus a set of pre-existing untracked Phase-E planning docs under `research/`
(`E0_CHECKPOINT_AUDIT.md`, `MANUSCRIPT_ARCHITECTURE.md`, `MANUSCRIPT_ARCHITECTURE_AUDIT.md`,
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_AUDIT_REPORT.md`,
`PHASE_E_PLAN.md`, `PUBLIC_RELEASE_BOUNDARY.md` — none newly created by this pass, all pre-dating
it per the task brief). `git diff HEAD --stat` against every tracked file is **empty** — zero
modifications to any tracked file, including `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`,
everything under `research/`, `data/`, and `scripts/`, and specifically the four protected audit
reports named in the task brief. `manuscript/` contains exactly two files (`main.tex`,
`references.bib`) — no stray files.

---

## 10. No scope expansion

**PASS.** Spot-checked generator/configuration numbers that appear in `main.tex`'s Experimental
Design section against `EXPERIMENT_1_REDESIGN_REVIEW.md` and `EXPERIMENT_1_FINAL_RESULTS.md`: 60
companies (redesign review line 90), 1,200-product vocabulary (line 91), retrieval-cutoff candidate
range `{70,75,80,85,90}` with a 30% coverage floor (lines 380/384), six nominal targets `{0.00,
0.20, 0.30, 0.50, 0.75, 1.00}` (final results line 78), seed range 31001–31020 (final results line
80) — every number traces to an already-existing frozen document; no new experimental claim, no new
literature-search result, and no number introduced that isn't already in `CONTRIBUTION_LOCK.md`,
`EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `EXPERIMENT_1_FINAL_RESULTS.md`, or the citation ledgers.

---

## 11. Compilability substitute (pdflatex/bibtex unavailable)

**PASS, with an explicit confidence caveat.** pdflatex/bibtex confirmed not installed in this
environment; direct inspection was used instead:

- `\begin`/`\end` environment counts balance exactly: `draftnote` 70/70, `itemize` 60/60,
  `equation` 2/2, `abstract` 1/1, `document` 1/1, `cases` 1/1, `enumerate` 1/1, `quote` 1/1 (the
  `quote` pair is inside the `\newenvironment{draftnote}` macro definition itself, not a stray use).
- Global brace count: 518 `{` vs. 518 `}` — balanced.
- No unescaped underscores found in non-comment content (the only bare `_` occurrences are inside
  math mode, e.g. `\mathrm{cluster}_k`, where `_` is the valid subscript operator, not literal
  text). Every underscore in body/comment text referencing code identifiers or file paths
  (`realized\_det\_pct`, `research/EXPERIMENT\_1\_...`) is correctly escaped with `\_`.
- No unescaped `%` found outside comments; the two `%` characters found in non-full-comment lines
  are both the intentional LaTeX line-continuation idiom inside the `\newenvironment{draftnote}`
  macro definition (`{%` / `}{%`), which is correct, standard usage, not a bug.
- `&` appears only twice outside a correctly-escaped `Ali \& Smith`: both are inside the `cases`
  math environment (Equation E3), where `&` is the required column-alignment character — correct
  usage, not a stray ampersand.
- **Caveat:** this is a gross-count/regex-based substitute, not an actual TeX parse. It confirms no
  environment or brace is missing in aggregate and no obvious unescaped special character exists,
  but cannot fully rule out a mis-nested (as opposed to mis-counted) brace or environment pair. It
  is, however, a reasonable substitute given the toolchain is genuinely unavailable, and no
  irregularity was found.

---

## Findings summary

| # | Finding | Tag | Location |
|---|---|---|---|
| 1 | Discussion section is missing the `MANUSCRIPT_ARCHITECTURE.md` §6-mandated dedicated paragraph placing the production case study as "consistent with 6a, not a test of 6b" — no Discussion draftnote cites `EVIDENCE_BASELINE.md` §1 or `r3_threshold_analysis.md`, so an E3 drafter following only the skeleton has no scaffolding to write this required content. | **REQUIRED NOW** | `manuscript/main.tex` §6 (Discussion), esp. §6.1/§6.7 |
| 2 | Results section subsections (7) don't map 1:1 onto `MANUSCRIPT_ARCHITECTURE.md` §4's named 6-subsection plan — content is merged/split/bookended differently, undocumented as a deviation. All numbers and the 6a/6b separation rule survive intact. | OPTIONAL FUTURE WORK | `manuscript/main.tex` §5 (Results) |
| 3 | `references.bib`'s `rankgpt2023` entry supplies full author given names not present in either source ledger row, going slightly beyond the "TODO, don't guess" standard the file otherwise follows perfectly (e.g. `dawidskene1979`). Names are factually correct but not ledger-verified. | OPTIONAL FUTURE WORK | `manuscript/references.bib` (rankgpt2023 entry) |

No BLOCK-level issue was found: no forbidden claim asserted, no frozen evidence touched, no
fabricated citation, no unsupported number, no scope expansion, and git hygiene is clean.

---

## Verdict

## 🟠 CONDITIONAL

The skeleton is faithful to `PAPER_CONTRACT.md` and `CONTRIBUTION_LOCK.md` in every place checked:
no forbidden claim appears as content, the 6a/6b distinction is never collapsed, every number
independently re-traces to its frozen source, every citation matches a verified ledger row (with
appropriate TODOs where the ledger itself didn't resolve a field), the title and figure/table
placeholders are correct and content-free, and no tracked file — including the four protected audit
reports — was touched. The one concrete, fixable gap is Finding #1: `MANUSCRIPT_ARCHITECTURE.md`
§6 specifically requires a Discussion-section paragraph positioning the production case study
relative to 6a/6b, and no Discussion draftnote in `main.tex` currently carries that instruction or
its evidence sources. This is a completeness gap in the scaffolding the E3 drafting session will
rely on, not a research-integrity violation — but it should be added (a key point in an existing
Discussion subsection, or a new one, is sufficient) before this skeleton is treated as the final
word E3 drafts against. Findings #2 and #3 are non-blocking and may be fixed opportunistically.

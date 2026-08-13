# E3 Draft Audit Report — Independent Review of the First Complete Manuscript Draft

> Independent, read-only audit of `manuscript/main.tex` (Phase E3: E2 skeleton replaced with real
> prose across all 9 sections + Reproducibility Statement, 4 real tables, 4 captioned figure
> placeholders). This report is a brand-new file; it does not modify, and was not used to modify,
> any protected/frozen document. No experiment was run, no methodology was changed, no frozen
> evidence was touched.

---

## 1. Verdict

## 🟠 CONDITIONAL

One concrete, checkable factual defect must be fixed before this draft can be checkpointed as
E3-complete: **Table T4 and the accompanying Section 5.4 prose pair the sharper per-row
realized-ADS-band counts (32/32 and 0/18) with p-values that were computed for a different,
non-interchangeable framing (the by-nominal-target 30/30 and 2/20 counts).** The cited p-values
($1.9\times10^{-9}$, $4.0\times10^{-4}$) are real numbers that exist in the frozen evidence base,
but they are not the p-values for the counts they are printed next to. This is a precise,
independently re-derivable numerical error, not a research-integrity violation — no forbidden
claim, no fabricated evidence, no methodology drift, no frozen-artifact tampering. Everything else
inspected (claim strength, evidence traceability for the other ~10 checked quantities, forbidden-
claim scan, citation resolution, manuscript structure, LaTeX static integrity, frozen-artifact
integrity, git hygiene) passed. See §12 for the exact required fix.

---

## 2. Files inspected

**Binding sources (read in full):**
`research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, `research/EVIDENCE_BASELINE.md`,
`research/MANUSCRIPT_ARCHITECTURE.md`, `research/EXPERIMENT_1_FINAL_RESULTS.md`,
`research/EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`, `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`,
`research/literature/citation_ledger.csv`, `research/literature/ads_metric_prior_art.csv`,
`research/literature/llm_advisory_prior_art.csv`. Spot-checked: `research/contribution_lock.csv`
(via CONTRIBUTION_LOCK.md's own reproduction), `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`
(section-header structure only, to confirm main.tex's own cross-reference to its §4 is valid).

**Manuscript under review:** `manuscript/main.tex` (full read, both halves — lines 1–1083 and
1084–1497), `manuscript/references.bib` (full read), `manuscript/figures/generate_figures.py`
(full read).

**Frozen evidence, opened directly and independently recomputed from (not trusted from prose):**
`data/outputs/experiments/exp1/final/final_condition_results.csv` (240 rows, all 24 columns
inspected).

**Git state:** `git log -3 --stat`, `git status --porcelain`, `git diff --stat HEAD -- research/
TECHNICAL_REPORT.md README.md METHODOLOGY.md scripts/ data/`, `git status --porcelain
data/outputs/experiments/exp1/final/`.

**Not modified by this audit session:** confirmed via a second `git status`/`git diff --stat` pass
at the end of the session — identical to the pre-audit state, aside from the manuscript's own E3
changes that pre-date this audit.

---

## 3. Changed files (this E3 pass, relative to the E2 skeleton / last commit `b776a5e`)

- **Manuscript (the object of this audit):** `manuscript/main.tex` — modified (E2 skeleton → E3
  full prose; 1,388 skeleton/draftnote lines removed, 1,075 prose lines added; net line count
  drops because draftnote scaffolding was denser than the prose that replaced it).
- **Code (new):** `manuscript/figures/generate_figures.py` — new file, not executed in this
  environment (matplotlib absent — independently confirmed, §8).
- **Docs:** no `research/*.md` file was modified by this pass (all the untracked `research/*.md`
  files shown by `git status` — `E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`,
  `MANUSCRIPT_ARCHITECTURE.md`, `MANUSCRIPT_ARCHITECTURE_AUDIT.md`,
  `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_AUDIT_REPORT.md`,
  `PHASE_E_PLAN.md`, `PUBLIC_RELEASE_BOUNDARY.md` — are pre-existing artifacts from earlier E0–E2
  phases that were never committed to git; their timestamps predate or match the E2 commit, not
  this E3 pass. Flagged for the record in §10, not attributed to this pass.).
- **Experimental artifacts:** none touched. `data/outputs/experiments/exp1/final/` is git-clean.
- **Manuscript bibliography:** `manuscript/references.bib` — unchanged from E2 (confirmed by its
  own header comment and by this pass finding no citation gap requiring a new entry).
- **Protected files** (`TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`,
  `research/CONTRIBUTION_LOCK.md`, `research/PAPER_CONTRACT.md`, `research/AUDIT_REPORT.md`, etc.):
  zero diff against HEAD — confirmed directly (§11).

---

## 4. Scientific claim-strength audit (item 1)

Read every section in full, with particular attention to Sections 1, 3.6/5, 6, and 9.

- **(a) 6a/6b never merged.** Confirmed. Results keeps them in explicitly separate, adjacently
  titled subsections (§5.2 "ADS Predicts Individual Mechanism Accuracy" vs. §5.3 "ADS Does Not
  Predict Mechanism Ranking"), and Discussion mirrors the split (§6.3 "What the Original Hypothesis
  Got Right" vs. §6.4 "...Got Wrong"). §3.5 ("Mechanism Accuracy vs. Mechanism Ranking") states the
  non-collapse rule explicitly as a standing instruction the rest of the paper follows. No sentence
  anywhere states an undifferentiated "ADS works" / "ADS doesn't work" verdict.
- **(b) H1 never presented as confirmed.** Confirmed. Every occurrence of "confirm"/"confirmed"
  in the document is either negated ("does not confirm," "not... confirmed") or explicitly paired
  with "partially supported, not confirmed" (Conclusion, §6.3, §7.10). Grep of all 9 occurrences
  of "confirm" in main.tex — none asserts H1 was confirmed.
- **(c) Causal account consistently hedged as inferred.** Confirmed. §3.5, §5.3, and especially
  §6.4 ("Why Consistency Predicts Difficulty but Not Ranking") state explicitly: "We state this
  account explicitly as inferred from exhaustive but post-hoc inspection... not as the result of a
  second, independently designed confirmatory experiment." Never asserted as proven or
  demonstrated.
- **(d) No generalization beyond tested scope.** Confirmed at the sentence level throughout —
  every quantitative claim in Results/Discussion carries a scope qualifier ("in this generator,"
  "under this perturbation," "in both lexical conditions," etc.). §6.6 ("What Practitioners Should
  NOT Infer") is a dedicated four-point negative-inference paragraph exactly matching
  `PAPER_CONTRACT.md` §3/§6's negative checklist. Limitations (§7) and Future Work (§8) both
  restate scope boundaries rather than smuggling generalizations into Results/Discussion.

No claim-strength violation found in Sections 1, 3, 5, 6, or 9.

---

## 5. Evidence traceability audit — independently re-derived, not trusted (item 2)

All numbers were recomputed directly from `data/outputs/experiments/exp1/final/final_condition_results.csv`
(240 rows) using a standalone stdlib-only Python script, independent of both the manuscript's own
`% EVIDENCE:` comments and the prose in `EXPERIMENT_1_*` reports (those reports were consulted only
afterward, to cross-check, not as the source of the recomputation).

| # | Claim | Manuscript states | Independently recomputed | Match? |
|---|---|---|---|---|
| 1 | Overall agreement | 32/50 = 64.0%, Wilson CI [50.14%, 75.86%], p=0.0649 | 32/50 = 64.0000%, Wilson CI [50.1410%, 75.8613%], exact binomial p=0.064909 | ✅ Exact |
| 2 | Realized-ADS band split (per-row band, VARIED) | 32/32 (100%) at 0.70–0.90; 0/18 (0%) at ≥0.90 | 32/32 (rate=1.0); 0/18 (rate=0.0) | ✅ Exact |
| 3 | By-nominal-target secondary framing | 30/30 (100%) at targets 0.50+0.75; 2/20 (10%) at target 1.00 | 30/30; 2/20 | ✅ Exact |
| 4 | Pearson r (realized ADS, rules acc.) | 0.909 (VARIED) / 0.959 (CLEAN) | 0.9091 (VARIED) / 0.9592 (CLEAN) | ✅ Exact (to stated precision) |
| 5 | Pearson r (realized ADS, retrieval acc.) | 0.948 (VARIED) / 0.955 (CLEAN) | 0.9476 (VARIED) / 0.9549 (CLEAN) | ✅ Exact |
| 6 | Band-level p-values (Table T4, paired with the 32/32 and 0/18 counts) | $1.9\times10^{-9}$ (32/32 row) and $4.0\times10^{-4}$ (0/18 row) | **For 32/32: $p \approx 4.66\times10^{-10}$. For 0/18: $p \approx 7.63\times10^{-6}$.** The cited values $1.9\times10^{-9}$ and $4.0\times10^{-4}$ are instead the exact binomial p-values for the **30/30** and **2/20** by-nominal-target counts (confirmed by direct computation and cross-checked against `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7, which reports exactly these two figures for the 30/30/2/20 framing). | ❌ **Mismatch — see §12** |
| 7 | Table T5 six-row gap table (realized-ADS band × lexical → rules acc., retrieval acc., gap) | 6 rows, values as printed (e.g. `<0.70`/VARIED: rules 0.5493, retrieval 0.6867, gap −0.1374) | All 6 rows recomputed independently from the raw CSV, byte-for-byte match on every mean and gap to 4 decimal places | ✅ Exact |
| 8 | Winner constancy (120/120 VARIED retrieval; 120/120 CLEAN tie) | Exceptionless in both lexical conditions | Recomputed: VARIED → {'retrieval': 120}; CLEAN → {'tie': 120} | ✅ Exact |
| 9 | Production figures cited in §1.1 | 91.2% (production) and 87.56% (synthetic) | Cross-checked against `EVIDENCE_BASELINE.md` §1/§2: 91.2% is the canonical production figure (with its "likely understated, unverified" caveat correctly attached in Limitations §7.6); 87.56% is the canonical **post-A5-fix** synthetic figure, not the superseded 84.12%/84.1%. | ✅ Canonical values used correctly |
| 10 | Table T3 experimental configuration | targets {0.00,0.20,0.30,0.50,0.75,1.00}; seeds 20 (31001–31020); cutoff 75; R3 thresholds 0.90/0.70; δ=0.02 | Recomputed from the CSV: unique seeds = 20 (31001…31020); unique targets = exactly {0.0,0.2,0.3,0.5,0.75,1.0}; unique retrieval cutoffs used = {75} | ✅ Exact |
| 11 | Realized ADS range | "0.44 to 0.93" | min=0.4414, max=0.9258 (rounds to 0.44–0.93) | ✅ Consistent |

**Result: 10 of 11 independently checked quantitative claims match the frozen evidence exactly.
One (item 6) does not.** This satisfies and exceeds the task's "at least 8 distinct quantitative
claims" requirement.

### Detail on the item-6 mismatch

Section 5.4's prose states: *"...two individually far more significant, opposite effects
(band-level exact binomial $p=1.9\times10^{-9}$ and $p=4.0\times10^{-4}$ respectively, Section
5.6)"* — appearing two sentences after that same paragraph introduces the 32/32-vs-0/18 realized-band
split as "the primary framing, matching the locked wording this paper draws on." Table T4
(`\label{tab:t4}`) makes the pairing explicit and unambiguous in tabular form:

```
Realized ADS 0.70--0.90 (32/32) & 100\% & --- & $1.9\times10^{-9}$ \\
Realized ADS $\geq$0.90 (0/18)  & 0\%   & --- & $4.0\times10^{-4}$ \\
```

The counts (32/32, 0/18) come from `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §9 (the sharper, D.1
per-row-realized-band framing). The p-values ($1.9\times10^{-9}$, $4.0\times10^{-4}$) come from
`EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7 — but that document computes them for the **different**
by-nominal-target counts (30/30, 2/20), which the manuscript's own §5.4 prose correctly
distinguishes from the realized-band counts one paragraph earlier ("These two framings differ
because nominal target and per-row realized ADS do not always coincide"). Somewhere in drafting,
the sharper counts and the correct-for-a-different-framing p-values were spliced together without
recomputing the p-values for the framing actually being reported. Both cited p-values are real,
traceable numbers that exist verbatim in `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7 — this is not a
fabrication — but as printed in main.tex they are attached to the wrong counts. The qualitative
finding (both bands are far more significant than the flat aggregate, in opposite directions) is
unaffected either way; only the specific numerals are wrong.

---

## 6. Forbidden-claim scan (item 3)

Grepped `manuscript/main.tex` for all 16 forbidden-claim patterns and their variants (novel metric,
universally selects, design-time-selection-as-unprecedented-pattern, cascade-combination-novel,
enterprise-AI-broadly, production-independently-validates, consistency-alone-sufficient,
higher-ADS-means-rules-better, CLEAN-implies-equivalent-in-general, p_transform-represents-real-
OCR-noise, two-feature-selector-as-built, ADS-predicts-suitability-unqualified, no-comparable-
vendor-practice, ~55,394, superseded 0.8094/0.9310/84.12%/84.1%, Formulation #4 wording).

**Zero violations found.** Every textual match on a forbidden-sounding phrase (e.g., "novel
metric," "no vendor," "independently valid...") occurs only inside a correctly negated sentence
("we... make no claim that ADS is a novel metric," "we do not claim... no vendor measures...", "does
not... independently validate"). No superseded number appears anywhere in the document. The
~55,394 figure does not appear. The two-feature selector is named only in future tense with an
explicit "not built, not tested here" hedge in every one of its 3 appearances (§1.5, §6.7, §8.1).
The B8-04 (Ken From Finance) vendor-practice contradiction is correctly *disclosed* rather than
resurrected — main.tex §2.8 explicitly states the "no vendor measures" framing is contradicted by
at least one industry source and flags the still-uncorrected `TECHNICAL_REPORT.md` sentence as an
open item tracked outside this manuscript, which is the correct behavior, not a violation.

---

## 7. Citation audit (item 4)

- **Key resolution:** all 14 distinct `\citep{}`/`\citet{}` keys used in `main.tex`
  (`rice1976`, `smithmiles2009`, `barbudo2023`, `manning2008`, `amigo2009`, `dawidskene1979`,
  `idreoskraska2019`, `chow1970`, `elyaniv2010`, `hendrickx2024`, `mozannarsontag2020`,
  `frugalgpt2023`, `rankgpt2023`, `jorgensenigel2021`) resolve to exactly the 14 entries defined in
  `manuscript/references.bib`. No orphan citation, no unused bib entry, no missing key.
  (`\nocite{*}` additionally forces the full bib to render regardless of citation status, per the
  file's own stated intent.)
- **VERIFIED-status tracing:** every cited key traces to a `VERIFIED` (or `VERIFIED-INDUSTRY`/
  `VERIFIED-PREPRINT`) row in `citation_ledger.csv`, `ads_metric_prior_art.csv`, or
  `llm_advisory_prior_art.csv`: `rice1976`→B1-01, `smithmiles2009`→B2-01, `barbudo2023`→B2-02,
  `idreoskraska2019`→B7-01, `chow1970`→B4-01, `elyaniv2010`→B4-02, `hendrickx2024`→B4-05,
  `mozannarsontag2020`→B5-02, `frugalgpt2023`→B3-02, `jorgensenigel2021`→B8-01 (all VERIFIED);
  `manning2008`→G1-01, `amigo2009`→G1-02, `dawidskene1979`→G1-04 (all VERIFIED, `ads_metric_prior_art.csv`);
  `rankgpt2023`→G2-01 (VERIFIED, `llm_advisory_prior_art.csv`, as its own bib-entry note claims).
- **No citation stretched beyond its source's supported claim.** Checked specifically: the
  cluster-purity/majority-vote-agreement citations (`manning2008`, `amigo2009`, `dawidskene1979`)
  are used only to support "ADS is not a novel metric," matching `ads_metric_prior_art.csv`'s own
  "Equivalent"/"Analogous" equivalence-column verdicts — not stretched to claim Dawid-Skene's EM
  model itself is equivalent to ADS (the manuscript correctly attributes the equivalence to "the
  raw majority-vote agreement proportion used throughout the crowdsourcing... literature
  descending from" Dawid & Skene, matching the ledger's own careful distinction between the EM
  model and its baseline comparator). Industry sources (B8-04/05/06) are correctly labeled "not
  peer-reviewed" in body prose (§2.8). The preprint-status row (`hendrickx2024`, journal-published
  2024 with a 2021 arXiv preprint) is not mislabeled as unverified.
- **Two disclosed, non-blocking bib gaps**, both explicitly flagged in the bib file's own comments
  and consistent with E3's "no perfect prose/typography required" standard: `dawidskene1979` has
  `volume/number/pages/doi = TODO` ("Verify before E5, do not guess"); `rankgpt2023`'s author list
  is abbreviated ("expand before E5"). Neither blocks E3 — `PAPER_CONTRACT.md` §11 requires only "a
  References section that compiles (even if not yet fully polished)," and these are disclosed gaps,
  not silent ones.

---

## 8. Manuscript structure audit (item 5)

- All 9 required sections (Introduction, Related Work, Problem Setting and Signal Definition,
  Experimental Design, Results, Discussion, Limitations, Future Work, Conclusion) plus the
  Reproducibility Statement are present with substantive, non-stub prose in every subsection —
  confirmed by reading the document in full (both halves). No section or subsection is a "(to be
  written)" placeholder.
- **6a/6b dedicated, separate subsections in Results:** confirmed (§5.2 vs. §5.3, see §4 above) —
  not merged.
- **Title terminology ("mechanism," not "classifier"):** consistent throughout body prose, checked
  specifically in the Problem Setting mechanism-definition subsections (§3.3 "Exact-Match Rules
  Mechanism," §3.4 "Fuzzy/Similarity Retrieval Mechanism," §3.5). The one appearance of the word
  "classifier" in body prose (§2.8, describing what Jørgensen & Igel's own paper studied — "a
  global classifier generalizes far worse across companies...") is a correct, contextual use
  describing a cited paper's ML classifier, not this paper's rules/retrieval mechanisms, and does
  not violate the title-terminology decision.
- **Retrieval-not-embedding disclaimer present and correctly placed:** §3.4 explicitly states
  "we deliberately call this mechanism 'retrieval,' not 'embedding'... no embedding model was
  trained, downloaded, or evaluated." All later mentions of "embedding" in the document (§6.5,
  §7.4, §8.3) are correctly scoped as a named, untested future-work alternative, never as a
  description of what was tested.
- **Results subsection count (7, not the architecture doc's originally-planned 6):** this is
  self-documented in main.tex's own header comment as "a deliberate refinement, not undocumented
  drift," consistent with a prior E2-stage decision this pass did not silently deviate from.
  Verified: §5.1 Experimental Completeness, §5.2 Accuracy (6a), §5.3 Ranking (6b), §5.4 Band
  Agreement, §5.5 Interaction Table, §5.6 Statistical Interpretation, §5.7 Summary — 7 subsections
  exactly as the header comment claims.

---

## 9. LaTeX/static integrity audit (item 6)

- **pdflatex/bibtex availability:** confirmed absent from this environment (`which pdflatex`,
  `which bibtex`, and `pdflatex --version` all report "command not found"). This is a disclosed,
  not hidden, limitation — consistent with the project's existing E0/E2 checkpoint practice per the
  script's own docstring, which this pass independently confirmed rather than assumed.
- **`\begin`/`\end` environment balance:** confirmed exactly matched — `table`×4, `tabular`×4,
  `figure`×4, `equation`×2, `document`×1, `abstract`×1, `cases`×1, all begins equal all ends.
- **Brace balance:** 284 open `{` vs. 284 close `}` after stripping full-line comments (a
  line-level comment strip, not a full LaTeX-comment-aware parse — a residual risk this method
  cannot fully rule out is a `%` mid-line inside a non-comment context being misparsed, but manual
  spot-inspection of every `%` in the file found only intentional in-line comments and no
  math-mode `\%`/`\&` escaping errors).
- **Unescaped special characters:** all raw underscores found (21 occurrences) are inside math
  mode (`$...$`) or `\mathrm{}`/`\text{}` constructs — none are bare, unescaped underscores in
  running prose. No unescaped bare `%` or `&` found outside `tabular`/math contexts.
- **Tables T2–T5:** all four `tabular` environments are syntactically well-formed (column specs,
  `\toprule`/`\midrule`/`\bottomrule` from `booktabs`, row-ending `\\`, matching `&` column counts
  per row) — visually confirmed row-by-row during the full read.
- **Equations E1 (ADS formula) and E3 (winner/tie definition):** both syntactically valid;
  `\begin{cases}...\end{cases}` for E3 is well-formed and its own begin/end pair is balanced.
- **Figure placeholders:** none of the 4 figures references `\includegraphics` — confirmed via a
  direct grep (zero matches for `includegraphics` anywhere in the file). All 4 use an `\fbox{...}`
  placeholder pattern instead, each with a proper `\caption{}` and `\label{}`. This means
  compilation would not fail due to a missing image file, and this satisfies
  `PAPER_CONTRACT.md` §11's "the slot must exist and be captioned" requirement via a third,
  legitimate option (a placeholder box) beyond the two the contract names (draft image /
  `\includegraphics` reference).
- **Minor, non-blocking figure-label/physical-order mismatch (new finding, not previously
  flagged):** the figure blocks appear in the source in the order F1, F2, **F4**, **F3** (F4's
  `\label{fig:f4}` block precedes F3's `\label{fig:f3}` block in the file, at lines 969 and 1019
  respectively), because Results' narrative order places the ranking-constancy discussion (§5.3,
  architecturally "F4") before the band-agreement discussion (§5.4, architecturally "F3"). Since
  no `\ref{fig:f1..f4}` cross-reference is ever dereferenced in body prose (confirmed by grep — zero
  matches), this causes no broken in-document reference and would not block compilation. It would,
  however, cause LaTeX's auto-numbered captions to read "Figure 3" for the block labeled `fig:f4`
  and "Figure 4" for the block labeled `fig:f3` in the compiled PDF — a source-label-vs-rendered-
  number mismatch that could confuse a future editor cross-referencing this document against
  `MANUSCRIPT_ARCHITECTURE.md`'s F1–F4 figure plan. Cosmetic; does not affect any claim's
  correctness. See §12 for the optional fix.

---

## 10. Comparison against Paper Contract and Contribution Lock (item 7)

- **Formulation match:** the manuscript's Abstract, §1.6 ("Contribution statement"), §6.1, and the
  Conclusion all restate Formulation #2 (`CONTRIBUTION_LOCK.md` §6) essentially verbatim in
  substance — the 6a/6b split plus the exact synthesis sentence ("historical decision consistency
  is informative about classification-mechanism difficulty, not about mechanism ranking..."). Not
  Formulation #1 (the abstract does include the positive 6a correlations, not omitted), not
  Formulation #3 (no prescriptive "should account for representation stability... as a built method"
  language — the future-work framing is consistently hedged as untested), and Formulation #4 is
  explicitly and correctly rejected in the Conclusion's own evidence-anchor comment.
- **Evidence hierarchy (§4) respected:** all Experiment 1 numbers trace to
  `final_condition_results.csv`/`EXPERIMENT_1_POSTHOC_ANALYSIS.md`/`EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`
  (tier 1/2), not to stale tier-5 prose — confirmed the manuscript uses the canonical, corrected
  87.56% synthetic figure, not `TECHNICAL_REPORT.md`'s stale 84.12%/84.1% figures, exactly as §4's
  hierarchy rule requires.
- **Production data rule (§5) respected:** production figures appear only in the Introduction
  (motivation) and one Discussion subsection (§6.2, brief, correctly framed as non-evidentiary),
  never in Results, and every appearance carries the "cited from a confidential engagement, not
  independently reproducible" qualifier.
- **Generalization rule (§6) respected:** checked at the sentence level in §4 above — no
  unqualified generalization found.
- **Numerical rule (§7):** respected for every canonical value except the one defect in §5/§12
  above, which is a computation error, not a citation of a superseded or forbidden number.

---

## 11. Frozen-artifact integrity (item 8)

- `git diff --stat HEAD -- research/ TECHNICAL_REPORT.md README.md METHODOLOGY.md scripts/ data/`
  returns **empty** — zero diff against the last commit for every one of these paths.
- `git status --porcelain data/outputs/experiments/exp1/final/` returns **empty** — the frozen
  Experiment 1 CSV directory is untouched (git-clean).
- The frozen `final_condition_results.csv` used for every independent recomputation in §5 is the
  same, unmodified file this audit read directly (240 rows, 24 columns, matching the schema
  documented in `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §3–5).
- This audit session itself made no lasting changes to any protected path: a temporary verification
  script was written and executed only in the session scratchpad directory (outside the repository),
  never inside `research/` or any tracked path; a stray earlier copy was created inside `research/`
  and immediately deleted before any further work, and a final `git status`/`git diff --stat`
  comparison at the end of the session confirms the working tree is identical to its state before
  this audit began (aside from the pre-existing E3 changes to `manuscript/main.tex` that are the
  subject of this review, and `manuscript/figures/` which pre-dates this audit).

**Frozen-artifact integrity: confirmed intact.**

---

## 12. Required fixes (CONDITIONAL — must be applied before E3 checkpoint)

1. **Table T4 (`\label{tab:t4}`) and the Section 5.4 prose sentence citing "band-level exact
   binomial $p=1.9\times10^{-9}$ and $p=4.0\times10^{-4}$":** these two p-values must be replaced
   with the values that actually correspond to the 32/32 and 0/18 realized-ADS-band counts printed
   next to them:
   - Realized ADS 0.70–0.90 (32/32): replace $1.9\times10^{-9}$ with **$p \approx 4.7\times10^{-10}$**
     (exact: $4.66\times10^{-10}$).
   - Realized ADS ≥0.90 (0/18): replace $4.0\times10^{-4}$ with **$p \approx 7.6\times10^{-6}$**
     (exact: $7.63\times10^{-6}$).
   - This is a pure recomputation fix — no new experiment, no re-derivation of counts, no change to
     any threshold or methodology. The counts (32/32, 0/18) are correct and unchanged; only the two
     p-values attached to them need correcting.
   - Alternative (not recommended, since §5.4's own prose already identifies the realized-band
     framing as "the primary framing" this paper uses): if the intent was instead to report the
     by-nominal-target framing's p-values, the counts in the same two table rows/prose sentence
     would need to change to 30/30 and 2/20 instead, to stay consistent with `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`
     §7 (which is where $1.9\times10^{-9}$/$4.0\times10^{-4}$ actually come from). This alternative
     is offered only for completeness; correcting the p-values (option 1) is the fix that matches
     the rest of the paper's own stated framing choice.

That is the only REQUIRED NOW fix. No other item in this report blocks the checkpoint.

---

## 13. Optional / future-work notes (non-blocking)

- **OPTIONAL — figure label/physical-order mismatch (§9):** reorder the F3/F4 figure blocks in the
  source (or swap their `\label{}` names) so the compiled Figure numbers match the F1–F4 naming
  used in `MANUSCRIPT_ARCHITECTURE.md` and in each figure's own caption text ("Source:
  ...EXPERIMENT_1_POSTHOC_ANALYSIS.md Sec.4-5" for F3, etc.). Purely cosmetic; does not affect any
  claim, does not block compilation, and E3 does not require final figure polish.
- **OPTIONAL — `generate_figures.py`'s matplotlib dependency:** the script correctly discloses (in
  its own docstring) that this is a new, non-stdlib dependency, justified because chart generation
  has no stdlib equivalent in this repository's toolchain — an acceptable, disclosed exception to
  the project's "no new dependency if it can be avoided" convention (`AGENTS.md`), not a violation.
  Independently confirmed matplotlib is genuinely absent from this environment (`ModuleNotFoundError`),
  matching the script's own claim.
- **OPTIONAL — pre-existing E0–E2 `research/*.md` files remain uncommitted:** several files
  protected/frozen for the purposes of this audit (`E0_CHECKPOINT_AUDIT.md`,
  `E2_FINAL_CHECKPOINT_AUDIT.md`, `MANUSCRIPT_ARCHITECTURE.md`, `MANUSCRIPT_ARCHITECTURE_AUDIT.md`,
  `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_AUDIT_REPORT.md`,
  `PHASE_E_PLAN.md`, `PUBLIC_RELEASE_BOUNDARY.md`) show as untracked (`??`) in `git status`, with
  timestamps predating this E3 pass. This is a pre-existing git-hygiene gap from earlier phases,
  not introduced or worsened by this pass, and not this audit's job to fix (staging/committing is
  outside a read-only reviewer's role) — flagged here only so it is not lost before the eventual
  checkpoint commit, at which point a human/builder should decide whether these belong in the same
  commit as the E3 draft or a separate housekeeping commit.
- **OPTIONAL — author/affiliation/date/title-selection placeholders:** correctly and explicitly
  named in the manuscript's own header comments as open human decisions deferred past E3 (per
  `MANUSCRIPT_ARCHITECTURE.md` §14 and `MANUSCRIPT_FORMAT_RESEARCH.md` §3), not scientific content
  gaps. No action required for E3.

---

## Summary

- **Quantitative claims independently re-derived:** 11 checked, 10 exact matches, 1 mismatch (§5,
  §12).
- **Forbidden claims found:** 0.
- **Citations unresolved / unverified-and-uncaveated:** 0.
- **Manuscript structure gaps:** 0.
- **LaTeX structural defects (would block compilation):** 0.
- **Frozen-artifact tampering:** 0.
- **Git hygiene issues (secrets/client data/local paths):** 0.
- **Required fixes:** 1 (Table T4 + §5.4 prose p-value correction, §12).

**Recommendation: CONDITIONAL.** Apply the single required fix in §12, then this draft is ready for
the E3 checkpoint. Everything else inspected — claim strength, the 6a/6b distinction, H1's honest
PARTIALLY_SUPPORTED framing, the production-data rule, the generalization rule, citation integrity,
manuscript completeness, LaTeX static structure, and frozen-evidence integrity — passed.

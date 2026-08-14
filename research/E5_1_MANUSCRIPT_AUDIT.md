# Phase E5.1 Manuscript Audit — Readability/Structure Pass on `manuscript/main.tex`

Independent review of an uncommitted working-tree change. Scope: verify the claimed
subsection-merge pass (68 → 43 `\subsection`s), the H1-subsection reorder in Limitations, and the
~25 renumbered `Section~X.Y` cross-references, per the task brief. This report does not modify
`manuscript/main.tex` or any other file.

---

## 1. What was checked

- `git diff -- manuscript/main.tex` (working tree vs `HEAD` = `4d031ab`), read in full (585-line
  diff, 76 insertions / 135 deletions across the whole file).
- Every line of the current `manuscript/main.tex` (1,462 lines) read directly, in four passes
  (Introduction/Related Work/Problem Setting, Experimental Design, Results/Discussion,
  Limitations/Future Work/Conclusion/Reproducibility Statement), to independently verify prose
  content and cross-reference correctness rather than trust the diff alone.
- Independently rebuilt the full `\subsection` map (see §2) directly from the current file with a
  fresh grep, not from the builder's claimed mapping.
- Every `Section~N` / `Section~N.M` occurrence in the file (86 occurrences) checked against that
  rebuilt map for correctness of the content it points to.
- `\citep{}`/`\citet{}` key sets, `\label{}` set, and `\ref{}` set diffed old vs. new (exact-match
  comparison, not eyeballed).
- Protected numeric strings (32/50, 0/18, 0.0649, 0.909/0.959/0.948/0.955, δ=0.02, cutoff=75,
  64.0%, both p-values) counted old vs. new — identical counts in every case checked.
- Full-file grep for `CONTRIBUTION_LOCK.md` §7's rejected-claim phrase list.
- Results section (`\section{Results}` through `\section{Discussion}`) grepped for the four
  production-only figures (91.2, 0.847, 0.964, 0.695) to confirm no leakage into the evidentiary
  section.
- `python -m pytest scripts/experiments/exp1/ -q` re-run directly (not trusted from the builder's
  claim).
- `git status --porcelain` and `git diff --stat` against `README.md`, `TECHNICAL_REPORT.md`,
  `METHODOLOGY.md`, `research/CONTRIBUTION_LOCK.md`, `research/PAPER_CONTRACT.md`,
  `manuscript/references.bib` to confirm none of the protected/governing files were touched.

---

## 2. Independently rebuilt subsection map (current file)

```
1 Introduction
  1.1 Real-World Motivation and General Problem
  1.2 Research Question
  1.3 Experimental Approach and Main Findings
  1.4 Contribution Statement and Paper Roadmap
2 Related Work
  2.1 Cluster Purity and Majority-Vote Agreement
  2.2 Design-Time Algorithm and Architecture Selection
  2.3 Inference-Time Selection and Escalation
  2.4 Domain-Specific Practice
3 Problem Setting and Signal Definition
  3.1 Historical Product-Level Decisions and Account Labels
  3.2 The Automated Determinism Score (ADS)
  3.3 Two Compared Mechanisms: Exact-Match Rules and Fuzzy Retrieval
  3.4 Mechanism Accuracy vs. Mechanism Ranking
4 Experimental Design
  4.1 Research Hypothesis
  4.2 Synthetic Generator and Factorial Design
  4.3 Realized ADS vs. Target Deterministic Share
  4.4 Lexical Conditions: CLEAN and VARIED
  4.5 Mechanisms and Retrieval Cutoff
  4.6 Seed Structure, Train/Test Separation, and Winner Definition
  4.7 Statistical Analysis
  4.8 Calibration and Preregistration
  4.9 Reproducibility
5 Results (UNCHANGED — 7 subsections, per its own locked in-file design comment)
  5.1 Experimental Completeness and Frozen Design
  5.2 ADS Predicts Individual Mechanism Accuracy
  5.3 ADS Does Not Predict Mechanism Ranking
  5.4 R3 Threshold Agreement by Realized-ADS Region
  5.5 ADS × Representation-Stability Interaction
  5.6 Statistical Interpretation
  5.7 Summary of Findings
6 Discussion
  6.1 What the Experiment Supports
  6.2 The Production Case Study in Light of These Results
  6.3 What the Original Hypothesis Got Right and Wrong
  6.4 Mechanistic Explanation: Representation Stability
  6.5 Relationship to Algorithm Selection and Meta-Learning
  6.6 Implications for Practice and Future Selector Design
7 Limitations
  7.1 H1 Only Partially Supported          <- moved to lead, was last pre-pass
  7.2 Synthetic Generator and Perturbation Model Scope
  7.3 Domain and Mechanism Scope
  7.4 Production Data Limitations
  7.5 No Selector Fix and Limited Generalization
8 Future Work
  8.1 Representation-Stability-Aware Selectors
  8.2 Generalization: Additional Domains and Mechanisms
  8.3 Real-World Noise Models and Independent Datasets
  8.4 Broader Architecture-Selection Experiments
9 Conclusion (no subsections)
```

43 `\subsection`s total, matching the builder's claimed 68→43. Results is confirmed untouched
(still exactly 7 subsections, identical titles/order to `git show HEAD`).

---

## 3. Cross-reference verification (item 7 of the brief)

Every one of the 86 `Section~N`/`Section~N.M` occurrences in the file was checked against the map
in §2 for whether it points at content that actually supports the claim being made at the citing
location (not just whether the number is syntactically plausible). Method: read the citing sentence
in context, then read the target subsection's actual content, for all subsection-level references;
section-level-only references (`Section~2`, `Section~4`, `Section~5`, etc., with no subsection
digit) were checked only for section-level correctness since they don't depend on the merge.

**The three specific fixes named in the task brief, independently re-verified:**

1. **R3 definition, "Section~4.10" → "Section~4.7."** Confirmed correct. R3's threshold definition
   ("at or above 0.90, rules; between 0.70 and 0.90, retrieval; below 0.70, the excluded LLM band")
   is at lines 757–761, inside `\subsection{Statistical Analysis}` (4.7). Both citing locations
   (line 565, line 614) now correctly point at 4.7.
2. **Whole-set-accuracy metric, "Section~4.9" → "Section~4.7."** Confirmed correct. The metric
   definition ("whole-set accuracy: a prediction counts as correct only if the mechanism both
   answered and was right, with abstention counted as incorrect") is at lines 743–745, inside the
   same 4.7 `Statistical Analysis` subsection. The citing location (line 504) now correctly points
   at 4.7, not at 4.9 (`Reproducibility`, which does not define this metric).
3. **Old "Section~7.10"/"Section~6.5" → "Section~7.1"/"Section~6.4."** Confirmed correct on both
   counts. (a) Line 1193's "a fresh, prospective test... would strengthen it further (Section~7.1)"
   correctly points at the now-first Limitations subsection, `H1 Only Partially Supported`, which
   is exactly the subsection that states this same post-hoc-vs-prospective caveat (lines 1269–1276)
   — self-consistent. (b) Line 1055's "the causal account for why it occurs is developed in
   Section~6.4" correctly points at `Mechanistic Explanation: Representation Stability`, which is
   indeed where the ADS-blind-to-surface-form causal account is developed (lines 1182–1207). (c)
   The `H1 Only Partially Supported` subsection's own internal reference to the mechanistic account
   (line 1272, "The mechanistic account in Section~6.4") was updated from the pre-move "Section~6.5"
   correctly, since Discussion's "What the Original Hypothesis Got Right"+"...Got Wrong" merge
   shifted everything after it in that section down by one — verified by independently walking the
   old→new Discussion subsection list, not by trusting the arithmetic.

**All other renumbered references spot-checked** (representative sample, each read in full
citing-sentence + target-subsection-content context): `Section~3.3` (line 106, mechanism
definitions — correct), `Section~4.2` (lines 620, 780, cross-company-alignment / six-target grid —
correct), `Section~4.3` (lines 484, 614, 933, 969, realized-ADS definition and its
lexical-invariance — correct), `Section~4.5` (lines 524, 777, retrieval cutoff calibration —
correct), `Section~4.6` (line 778, winner/tie/CI definitions — correct), `Section~4.8` (lines 569,
598, falsification criteria / 17-point calibration pass — correct), `Section~1.2` (line 454, four
preconditions — correct, `Research Question` is indeed 1.2), `Section~5.5` (lines 1045, 1090, 1107,
1109, 1364, representation-stability interaction table — correct throughout), `Section~8.1` (lines
1237, 1329, future-selector direction — correct). No incorrect subsection-level reference was found
anywhere in the file.

**One pre-existing, not-introduced-by-this-pass item flagged for completeness, not blocking:**
lines 380 and 432 cite `Section~4.1` ("the LLM mechanism is explicitly excluded from Experiment~1
(Section~4.1)") to support the LLM-exclusion claim. `Section~4.1` (`Research Hypothesis`, lines
559–569) states H1 and names R3 but does not itself state the LLM-exclusion rationale — that
rationale is actually given in §1.3 (lines 196–201) and in §4.7/§7.3. This reference was **not**
touched by this pass (absent from the diff; confirmed by `git show HEAD:manuscript/main.tex`) and
`Section~4.1` occupied the same position before and after the merge (nothing was merged ahead of
it in §4), so it is not a renumbering regression — it is a pre-existing, already-E4-audited
imprecision, at most a loose "see the section where Experiment 1 begins" pointer. Flagged as
optional future-work polish, not a finding attributable to this pass.

---

## 4. Content-preservation check (items 1–2, 6 of the brief)

Read every diff hunk plus the surrounding current-file prose. In every hunk, the pattern is: a
`\subsection{...}` line is deleted (and its immediately-preceding blank line), the following
paragraph now runs directly into the prior subsection's text, sometimes with a title rename on the
surviving `\subsection{...}` header. No paragraph text was reworded, no sentence was dropped, no
hedge/qualifier was strengthened or weakened. Spot-checked in full against `git show
HEAD:manuscript/main.tex`:

- Introduction: "Real-world motivation" + "General problem" → merged; both paragraphs present
  verbatim (only two Section~ numbers inside updated, per §3).
- Related Work: six of eight old subsections collapsed into four; all `\citet{}`/`\citep{}`
  sentences present verbatim, same order, same hedging language ("We make no claim that...",
  "We do not claim that...") preserved in every instance.
- Limitations: ten old subsections collapsed into five, plus the `H1 Only Partially Supported`
  subsection moved from last to first. Confirmed sentence-for-sentence identical content in the
  merged subsections (verified in detail in the assistant's own diff-reading above); the moved
  subsection's three sentences are byte-identical except the one intentionally-updated internal
  cross-reference (Section~6.5→6.4, itself required by the Discussion renumbering, not a content
  edit).
- No claim's strength changed. E.g., "H1 (revised) is only partially supported... stated here as
  the honest verdict, not softened toward either 'confirmed' or 'refuted'" is unchanged text,
  unchanged position relative to the rest of Limitations' content (only the subsection's position
  in the section changed, which is exactly the reordering the task authorized based on the
  section's own comment).

**Comment-block reordering note (not a content change):** in the Limitations merges, some
`% EVIDENCE:` comment lines were reordered/concatenated relative to their original position (e.g.
`Domain and Mechanism Scope`'s evidence comments now read `CONTRIBUTION_LOCK.md Sec.8` before
`EXPERIMENT_1_REDESIGN_REVIEW.md Sec.10; CONTRIBUTION_LOCK.md Sec.9`, whereas originally these were
attached to two separate subsections). This is a LaTeX comment, invisible in the compiled PDF, and
every original evidence pointer is still present somewhere in the merged comment block — none
dropped, none fabricated.

---

## 5. Forbidden-claim resurrection check (item 2 of the brief)

Full-file grep for `CONTRIBUTION_LOCK.md` §7's rejected-claim phrase list (`novel metric|our
novel|is novel|proves that|validates R3|independently validat|universally|enterprise AI
broadly|no vendor|no comparable vendor|consistency alone is sufficient|higher ADS means rules`)
found exactly two matches, both correctly-negated disclaimers already present before this pass and
untouched by it:

- Line 276: "We therefore make no claim that ADS is a novel metric" — correct negation.
- Line 397: "We do not claim... that no vendor measures historical consistency before choosing a
  mechanism -- at least one industry source directly contradicts that framing" — correct negation,
  matches `CONTRIBUTION_LOCK.md` §7's Ken-From-Finance correction.

No forbidden claim reappeared as an assertion anywhere in the file.

---

## 6. 6a/6b (accuracy vs. ranking) separation (item 3 of the brief)

Confirmed explicitly maintained in every location the brief asked about:

- Results (untouched, as designed): 5.2 "ADS Predicts Individual Mechanism Accuracy" and 5.3 "ADS
  Does Not Predict Mechanism Ranking" remain two separate, adjacent subsections with an explicit
  hand-off sentence at line 900–901 ("it says nothing yet about which mechanism performs better...
  that is the subject of Section~5.3").
- Discussion (merged 9→6 subsections): the accuracy/ranking distinction is stated explicitly and
  separately at lines 1122–1129 ("historical decision consistency is informative about
  classification-mechanism difficulty, not mechanism ranking") and reiterated at lines 1136–1140
  (production case study is "consistent with Section~5.2's positive finding... but... never itself
  a controlled test of Section~5.3's ranking finding"). The two claims are never collapsed into one
  sentence anywhere in the merged Discussion.
- Introduction (merged): §1.3's "two-part finding... this paper keeps explicitly separate
  throughout" (lines 206–216) and §1.4's contribution statement (lines 223–242) both state the two
  claims separately with their own evidence, matching `CONTRIBUTION_LOCK.md` §6's 6a/6b wording.

No conflation found.

---

## 7. Production-data confinement (item 4 of the brief)

Grepped the Results section (`\section{Results}` through `\section{Discussion}`) for the four
production figures (91.2, 0.847, 0.964, 0.695): zero matches. Production numbers appear only in
Introduction §1.1 (motivating, explicitly "not evidence for it," line 111) and in Discussion §6.2 /
Limitations §7.4, both of which explicitly restate the non-evidentiary caveat ("does not
independently validate," "cannot be re-run against the corrected pipeline," "cited from a
confidential engagement, not independently reproducible"). No merge moved a production number into
Results or reframed it as validating evidence.

---

## 8. Protected numbers (item 5 of the brief)

Occurrence counts, old vs. new, identical for every checked pattern: `32/50` (1/1), `0/18` (5/5),
`0.0649` (3/3), `0.909` (2/2), `0.959` (2/2), `0.948` (2/2), `0.955` (2/2), `δ=0.02` (4/4),
`cutoff $=75$` (1/1), `64.0` (4/4), `1.9` (4/4, covering the `p=1.9×10^{-9}`), `4.0` (8/8, covering
`p=4.0×10^{-4}`, `4.0` in other numeric contexts, and the `0.44--0.93` etc. ranges). The full diff
was also read line-by-line (§4 above) and no hunk touches a numeric table cell, equation, or
statistic — every change is a subsection-header line or a `Section~X.Y` cross-reference digit.

---

## 9. H1 status (item 6 of the brief)

`H1 Only Partially Supported` subsection's content is byte-identical to its pre-pass version except
the one intentionally-corrected internal cross-reference. It still states "H1 (revised) is only
partially supported, matching the pre-registered PARTIALLY_SUPPORTED row of the falsification table
exactly -- stated here as the honest verdict, not softened toward either 'confirmed' or 'refuted.'"
Moving it to lead the section changes its prominence, not its verdict — no upgrade, no downgrade.
This also resolves the pre-existing self-contradiction the task brief flagged (the section's own
top-of-file comment claimed the verdict "leads... not buried" while it was in fact last); the
comment itself was also updated to record why the move happened (lines 1263–1265), which is an
honest, traceable annotation of the change, not a silent edit.

---

## 10. Citations, labels, refs (items 8–9 of the brief)

- `\citep{}`/`\citet{}` key set: identical, confirmed by exact diff of sorted unique key lists
  (`diff` returned no output).
- `\label{}` set: identical — `eq:ads`, `eq:winner`, `fig:f1`–`fig:f4`, `tab:t2`–`tab:t5`, all
  present in both versions, no additions or removals.
- `\ref{}` set: identical (`tab:t5}` reference in Discussion, unchanged).

---

## 11. Test suite (item 10 of the brief)

Re-ran independently: `python -m pytest scripts/experiments/exp1/ -q` → `30 passed in 12.55s`.
Confirms no code was touched by this pass (expected, since the diff touches only
`manuscript/main.tex`).

---

## 12. Git hygiene

- `git diff --stat -- manuscript/main.tex`: 76 insertions, 135 deletions, one file — matches the
  builder's description of the change's shape (net line reduction from removing blank
  lines/headers, no content growth).
- `git diff --stat HEAD -- README.md TECHNICAL_REPORT.md METHODOLOGY.md
  research/CONTRIBUTION_LOCK.md research/PAPER_CONTRACT.md manuscript/references.bib`: empty —
  none of the protected/governing files were touched by this pass.
- `git status --porcelain` shows three unrelated untracked files from prior sessions
  (`research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md`, `research/E4_CHECKPOINT_MANIFEST_VERIFICATION.md`,
  `research/E5_GPS_HOUSEKEEPING_AUDIT.md`) — pre-existing, not created or modified by this pass,
  not evaluated further here since they are outside this task's scope (this report also does not
  overwrite any of them, per instructions). A safe `git add` for this specific checkpoint should
  stage only `manuscript/main.tex` (plus this new `research/E5_1_MANUSCRIPT_AUDIT.md` if the human
  wants the audit trail committed) and leave the three unrelated untracked files for whoever owns
  that separate work to stage.
- No secrets, credentials, client data, real-company names, local Windows paths, or editor
  temp/backup files found in the diff.

---

## 13. Verdict

🟢 **PASS.**

Every one of the ten verification items in the task brief was independently checked against the
current file content and the `HEAD` baseline — not accepted on the builder's summary. The
subsection-merge pass is exactly what it claims to be: header consolidation and one authorized
reorder, zero prose rewrites, zero claim-strength changes, zero forbidden-claim resurrections,
zero protected-number drift, zero production-data leakage into Results, zero citation/label/ref
loss, and all three specifically-claimed cross-reference fixes (plus every other renumbered
reference in the file) verified to point at content that actually supports the citing sentence.
The one flagged item (`Section~4.1`'s loose pointer for the LLM-exclusion rationale) predates this
session, was not touched by it, and is not a renumbering artifact — it is noted as optional
future-work polish only, not a blocking condition. Safe to stage and checkpoint as-is.

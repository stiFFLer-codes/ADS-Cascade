# E3 Final Checkpoint Audit — Independent Pass 5 (V2)

> Read-only, independent, from-scratch verification of the exact staged state described in the
> task brief, performed after four prior independent audits this session (E3_DRAFT_AUDIT_REPORT.md,
> E3_STATISTICAL_RECONCILIATION_AUDIT.md, E3_CHECKPOINT_STAGED_AUDIT.md, E3_FINAL_CHECKPOINT_AUDIT.md)
> and after the three cross-reference fixes + scratch-file cleanup those passes produced. This pass
> wrote its own recomputation script from scratch (not reusing `scripts/experiments/exp1/stats.py`
> or any prior audit script) and kept all working files outside the repository tree, in this
> agent's own temp scratchpad.

## 1. Repository state

- Branch: `main`. HEAD: `b776a5ed334dc9e360c6c30ed6cf51bb3b2dbd81` ("Phase E.2: establish manuscript
  skeleton").
- `git status --porcelain` (tracked changes only): exactly the 6 staged paths below, no unstaged
  modifications to tracked files.
- Untracked `.md` files present in `research/` (E0/E2/E3 audit reports, MANUSCRIPT_ARCHITECTURE*,
  PHASE_E_*, PUBLIC_RELEASE_BOUNDARY.md) are pre-existing artifacts from prior passes, not part of
  this diff, and were left untouched.
- Diffed via `git show :<path>` (staged blob content), confirmed identical to working tree for the
  6 staged files.

## 2. Changed files (staged)

```
A   manuscript/figures/generate_figures.py
M   manuscript/main.tex
A   research/E3_CHECKPOINT_STAGED_AUDIT.md
A   research/E3_DRAFT_AUDIT_REPORT.md
A   research/E3_STATISTICAL_RECONCILIATION.md
A   research/E3_STATISTICAL_RECONCILIATION_AUDIT.md
```
Category: manuscript prose (`main.tex`, largest change — E2 draftnote skeleton replaced with real
E3 prose, ~1382 line-level deletions / equivalent additions within the file, not a deleted file),
one new code file (figure-generation script), four new audit-trail docs. No experimental artifacts
changed. This is a docs+manuscript+one-script pass; no deletions of any file.

## 3. Cross-reference corrections (task item 1)

Independently re-counted every `\subsection` under `\section{Discussion}` (line 1143) in the
staged `main.tex`, from scratch:

| # | Line | Title |
|---|------|-------|
| 6.1 | 1146 | Summary of Findings |
| 6.2 | 1160 | The Production Case Study in Light of These Results |
| 6.3 | 1180 | **What the Original Hypothesis Got Right** |
| 6.4 | 1196 | What the Original Hypothesis Got Wrong |
| 6.5 | 1210 | **Why Consistency Predicts Difficulty but Not Ranking** |
| 6.6 | 1227 | Representation Stability as an Uncaptured Factor |
| 6.7 | 1243 | Relationship to Algorithm Selection and Meta-Learning |
| 6.8 | 1258 | What Practitioners Should NOT Infer |
| 6.9 | 1275 | Implications for Future Selector Design |

Confirms 6.2 = production case study, 6.3 = the PARTIALLY_SUPPORTED discussion, 6.5 = the causal
mechanistic account — matching what the 4th audit determined.

Searched the entire staged `main.tex` for every occurrence of `Section~6.2`, `Section~6.3`,
`Section~6.4`, `Section~6.5` (single regex sweep, all four patterns at once, no filtering that
could hide a stray match). Exactly 3 occurrences exist in the whole document:

- Line 815 → `Section~6.3` (PARTIALLY_SUPPORTED discussion reference) — **correct**.
- Line 1081 → `Section~6.5` (causal-account forward-reference from §5.4) — **correct**.
- Line 1381 → `Section~6.5` (causal-account reference from §7.10) — **correct**.

Zero remaining occurrences of `Section~6.2` or `Section~6.4` anywhere in the document. **Fix is
complete; no other instance of the same error class exists elsewhere.**

(Note, not part of this task's checklist but surfaced while reading `E3_CHECKPOINT_STAGED_AUDIT.md`
§4: that report flags a *separate*, already-resolved, non-blocking citation slip — a prior audit
*report* (`E3_STATISTICAL_RECONCILIATION.md` §7) mis-cited a "governed by" occurrence as being in
"§6.6" when it is actually in §6.7. This pass independently confirms that slip is in the audit
report text, not in `main.tex` itself — verified against my own subsection table above, where §6.6
is "Representation Stability as an Uncaptured Factor" and §6.7 is "Relationship to Algorithm
Selection and Meta-Learning." Not a manuscript defect; recorded here only for completeness.)

## 4. Statistical pairing — independent recomputation, 5th pass (task item 2)

Wrote a fresh stdlib-only Python script (`comb`-based exact two-sided binomial test, closed-form
Wilson interval) against `data/outputs/experiments/exp1/final/final_condition_results.csv` (240
rows, confirmed via `len(rows)==240` assertion). No import of any repo script or prior audit
script.

**Column identification:** the "realized ADS" column that reproduces the claimed per-row band
counts is `realized_det_pct` — confirmed by testing `weighted_ads`, `unweighted_ads`, and
`realized_det_pct` against the VARIED subset (120 rows) and finding only `realized_det_pct`
produces the exact claimed split.

| Quantity | Recomputed | Manuscript states | Match |
|---|---|---|---|
| Realized-ADS band [0.70,0.90), VARIED, agree/total | 32/32 | 32/32 | ✅ |
| Realized-ADS band ≥0.90, VARIED, agree/total | 0/18 | 0/18 | ✅ |
| By-nominal-target {0.50,0.75}, VARIED, agree/total | 30/30 | 30/30 | ✅ |
| By-nominal-target {1.00}, VARIED, agree/total | 2/20 | 2/20 | ✅ |
| Exact two-sided binomial p, 30/30 | 1.862645×10⁻⁹ | $1.9\times10^{-9}$ | ✅ |
| Exact two-sided binomial p, 2/20 | 4.024506×10⁻⁴ | $4.0\times10^{-4}$ | ✅ |
| Aggregate 30+2 / 30+20 | 32/50 = 64.0% | 32/50 (64.0%) | ✅ |
| Wilson 95% CI, 32/50 | (50.14%, 75.86%) | $[50.14\%, 75.86\%]$ | ✅ |
| Exact two-sided binomial p, 32/50 vs 0.5 | 0.064909 | $p=0.0649$ | ✅ |

Per-target breakdown (independent sanity check, not itself claimed in the manuscript as a separate
number): target 0.50 → 10/10 decided (10 rows have `r3_agrees_with_empirical=""`/undecided,
excluded, consistent with a `tie`-vs-mechanism-comparison structure), target 0.75 → 20/20, target
1.00 → 2/20. These sum correctly to the 30/30 and 2/20 groups above.

Confirmed by direct text search of the staged `main.tex` that no p-value is ever attached to the
32/32 or 0/18 counts, and that $1.9\times10^{-9}$/$4.0\times10^{-4}$ are always attached to the
30/30/2/20 counts respectively, in every location checked:

- Table T4 (`\label{tab:t4}`, line 1044; rows at 1049–1051): only "Overall agreement (32/50)" and
  the two by-target rows appear — no row exists for 32/32 or 0/18 at all.
- Figure F3 caption (`\label{fig:f3}`, line 1033; caption at 1029–1032): states "100% (32/32) …
  versus 0% (0/18) …" with no p-value attached.
- §5.4 "R3 Threshold Agreement by Realized-ADS Region" (line 984; explicit statement at
  1041–1042): "no independently frozen $p$-value exists for those exact counts."
- §5.6 "Statistical Interpretation" (line 1110; explicit statement at 1112–1117): pairs
  $p=1.9\times10^{-9}$ with "the 30/30 retrieval-region band" and $p=4.0\times10^{-4}$ with "the
  2/20 rules-region band," then separately notes the 32/32 and 0/18 bands "are not independently
  paired with a frozen $p$-value anywhere in this paper."
- §6.3 "What the Original Hypothesis Got Right" (line 1180; text at 1183): references the 32/32
  band qualitatively ("exceptionless … dominance in every band") without a misattributed p-value.

This is the 5th independent confirmation of these exact numbers this session, all in agreement.

## 5. Claim scope (task item 3)

- H1 status: every occurrence (lines 578, 585, 813, 1182, 1190, 1331, 1376, 1378, 1464) reads
  "PARTIALLY SUPPORTED" / "only partially supported" — never a bare "SUPPORTED." No regression.
- 6a/6b: `% - research/CONTRIBUTION_LOCK.md Sec.4 (6a)` anchors §5.2 "ADS Predicts Individual
  Mechanism Accuracy" (line 918) and `(6b)` anchors §5.3 "ADS Does Not Predict Mechanism Ranking"
  (line 949) — two separate, non-merged Results subsections. Confirmed.
- Formulation #2 substance: header comment (line 6) and contribution statement (§1.8, line 226)
  both anchor to `research/CONTRIBUTION_LOCK.md` (Formulation #2); the "no novel metric" framing
  (line 283, "we therefore make no claim that ADS is a novel metric — this is a closed [cluster
  purity restatement]") is present and correctly hedged, not resurrected as a novelty claim.
- Rejected-claim resurgence check: grepped for "novel metric," "universally selects," "production
  validates," "enterprise AI," "higher ADS means [rules better]," "CLEAN implies equivalent," "no
  comparable vendor," "universal(ly) applicable," "broadly applicable," "selects the right
  mechanism," and the superseded numbers (0.8094, 0.9310, 84.12%, 55,394/55394, "two-feature
  selector"). Findings:
  - "selects the right mechanism" appears twice (lines 246, 1154), both in explicitly *negated*
    form ("not a method we claim selects the right mechanism"; "not a confirmation of that
    hypothesis") — correct framing, not a resurgence.
  - "novel metric" appears once (line 283), explicitly rejecting the claim — correct.
  - None of the other rejected-claim strings, and none of the superseded numeric values, appear
    anywhere in the staged `main.tex`.
- Production numbers (91.2%, 0.847, 0.964, 0.695) inside Results: located all 5 occurrences
  (lines 100, 119, 600, 1340, 1341). All fall in §1.1 "Real-world motivation" (lines 100, 119),
  §4.x "Synthetic Generator" as a calibration input, not a Results claim (line 600), or §7
  "Production Confidentiality"/"Absence of Independent Production Validation" in Limitations
  (lines 1340–1341). `\section{Results}` spans lines 891–1142; **none of the 5 occurrences fall
  inside that range.** Confirmed no production number is presented as Results-section experimental
  evidence.

## 6. Protected artifacts (task item 4)

- `git diff --cached -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md
  research/contribution_lock.csv TECHNICAL_REPORT.md README.md METHODOLOGY.md
  manuscript/references.bib data/outputs/experiments/exp1/final/` → empty. None of these paths are
  staged or modified.
- `git diff 6fb6188 -- data/outputs/experiments/exp1/final/` → empty. The frozen evidence directory
  is byte-identical to the freeze commit.
- `manuscript/references.bib`: `git log --oneline -- manuscript/references.bib` shows only the
  `b776a5e` E2-checkpoint commit touching it, and `git status --porcelain -- manuscript/references.bib`
  is empty (unmodified, not staged) — byte-identical to the E2 checkpoint.
- `git diff --cached --name-status` contains no `D` (deletion) entries — confirmed no deletions in
  the staged diff.

## 7. Manuscript / git safety (task item 5)

Ran a combined grep for PEM headers, `api[_-]?key`, `secret`, `password`, `bearer`, `token`,
AWS-style key patterns, and the operator's local Windows username/path fragments
(`C:\Users\Maitreya`, `MaitreyaSapariya`) across the full staged diff (`git diff --cached`, 4319
lines). Zero matches on any credential/secret pattern. The only `token`-matching lines are prose
about tokenizer/token-reorder text-similarity behavior (lines discussing lexical perturbation), not
credentials. No local paths or usernames leaked into the diff. Consistent with all four prior
passes — clean.

## 8. Exact staged file list (task item 6)

`git diff --cached --name-status` reproduced exactly:
```
A	manuscript/figures/generate_figures.py
M	manuscript/main.tex
A	research/E3_CHECKPOINT_STAGED_AUDIT.md
A	research/E3_DRAFT_AUDIT_REPORT.md
A	research/E3_STATISTICAL_RECONCILIATION.md
A	research/E3_STATISTICAL_RECONCILIATION_AUDIT.md
```
Exactly 6 paths, no more, no fewer, no deletions. Matches the task brief exactly.

## 9. Scratchpad byproducts (task item 7)

`scratchpad/independent_recompute.py`, `scratchpad/staged_generate_figures.py`, and
`scratchpad/staged_main.tex` do not exist anywhere in the working tree (`find . -iname` sweep,
excluding `.git/`, returned nothing) and are not staged.

**New finding (minor, not one of the three named files):** `scratchpad/__pycache__/` contains one
leftover compiled-bytecode file, `staged_generate_figures.cpython-314.pyc` — a runtime byproduct of
having executed the now-deleted `scratchpad/staged_generate_figures.py` in a prior audit pass. It
is covered by `.gitignore`'s `__pycache__/` rule (confirmed: `git status --porcelain scratchpad/`
returns nothing, `git ls-files scratchpad/` returns nothing), so it is untracked and will not be
committed. It is, however, filesystem debris from a prior auditor's session that never got cleaned
up. Not staged, not a research-integrity or git-hygiene risk to the commit itself, but worth a
manual `rm -rf scratchpad/__pycache__` at some point since the source `.py` it was compiled from no
longer exists.

## 10. Test suite (task item 8)

```
python -m pytest scripts/experiments/exp1/ -q
30 passed in 10.46s
```
30/30, matching the expected count.

## 11. Code review — `manuscript/figures/generate_figures.py` (new file)

- Reads only the frozen `final_condition_results.csv`; uses stdlib `csv`, and `matplotlib` only
  inside `main()` (lazy import), consistent with the rest of the script being importable/inspectable
  without matplotlib installed.
- Its `ads_band()` cutoffs (0.70/0.90) and its choice of `realized_det_pct` as the banding column
  (line 42) independently match the manuscript's claimed 32/32 / 0/18 split — cross-checked against
  my own independent recomputation in §4 above (same column, same thresholds, same counts). This is
  a real, if indirect, corroboration: two independently-written pieces of code (this script and my
  fresh audit script) agree on which column and cutoffs reproduce the claimed figures.
  `r3_agrees_with_empirical` values of `""` (undecided/tie rows) are correctly excluded from both
  numerator and denominator (`if flag in ("True", "False")`), matching my own script's handling.
  No leakage, no hardcoded seed dependency, deterministic given the frozen CSV.
- Docstring is honest and falsifiable: explicitly states matplotlib is not installed in this
  environment and the script has *not* been executed, rather than claiming success. Confirmed the
  staged `main.tex` contains no `\includegraphics` calls anywhere (grepped for
  `includegraphics|f1_design_flow|f2_ads_vs_accuracy|f3_r3_agreement|f4_ranking_constancy` — zero
  matches) — all four figure "slots" are `\fbox{...TODO: figure placeholder...}` boxes with
  captions, not embedded images. So the unexecuted script cannot have silently produced a wrong
  image that made it into the PDF; there is no image in the PDF yet. Consistent with the script's
  own docstring claim.
- **Minor finding (non-blocking):** `matplotlib` is a new, undeclared dependency — it does not
  appear in `requirements.txt` (which lists only `pandas`, `requests`, `tqdm`, with `lxml`/
  `openpyxl` commented out for later). This repo is not strictly stdlib-only (pandas/requests are
  already dependencies), so this isn't a hard convention violation, but the script currently cannot
  be run by a fresh clone of the repo without an undocumented `pip install matplotlib` step. Given
  the script is inert placeholder-generation code (never executed, produces no committed output,
  referenced nowhere via `\includegraphics`), this is future-work-grade, not a blocker.
- No test file accompanies this script. Given it produces no numbers (pure plotting from already-
  validated columns) and has no committed output yet, this is consistent with the "docs/pure-glue
  code" exemption in the review guidance, not a required-now gap.

## 12. Experimental integrity

Not applicable — no experimental artifacts changed (confirmed empty diff against `6fb6188` for the
`data/outputs/experiments/exp1/final/` path, §6 above). The 240-row frozen CSV itself was read
read-only for this audit's independent recomputation and was not modified.

## 13. Scope / GPS alignment

`research/RESEARCH_GPS.md`'s "CURRENT LOCATION"/"CURRENT GATE" text still describes "Phase D.1 —
COMPLETE" / "Contribution lock" as the open gate, which is stale relative to the repo's actual state
(Phase E.0/E.1/E.2/E.3 have all since happened per the commit log and the E3 manuscript-draft work
under audit here). This staleness is **not part of the 8-item checklist this task was scoped to**,
and per the standing audit instructions "only the human/builder updates" that file — flagged here
for visibility, not treated as a finding against the staged diff. The staged work itself (replacing
an E2 draftnote skeleton with real E3 manuscript prose, plus a figure-generation script and audit
trail) is squarely on the locked north star (defensible first manuscript draft) and is not a
detour.

## 14. Findings

1. **[OPTIONAL FUTURE WORK]** `scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc` is
   leftover debris from a prior audit session (source `.py` already deleted). Gitignored, untracked,
   not staged, poses no commit risk — but should be manually removed for tree hygiene.
   `scratchpad/__pycache__/staged_generate_figures.cpython-314.pyc`
2. **[OPTIONAL FUTURE WORK]** `matplotlib` is used by the new `manuscript/figures/generate_figures.py`
   but is not declared in `requirements.txt`. The script is unexecuted and produces no committed
   output, so this doesn't affect any claim in the manuscript, but a fresh clone can't run it
   without an undocumented dependency.
   `manuscript/figures/generate_figures.py` (no requirements.txt entry)
3. **[OPTIONAL FUTURE WORK]** `research/RESEARCH_GPS.md`'s CURRENT LOCATION/GATE text is stale
   (still says "Phase D.1 COMPLETE" / "Contribution lock" as the open gate) relative to the repo's
   actual Phase E.0–E.3 progress. Not modified by this task and not part of the 8-item checklist;
   noted for the human/builder to update.
   `research/RESEARCH_GPS.md`

No REQUIRED NOW findings. All 8 checklist items from the task brief verified independently and
found correct, with full agreement to 5+ significant figures on every recomputed statistic.

## 15. Required fixes

None. (Empty — no CONDITIONAL/BLOCK-level findings.)

## 16. Verdict

## 🟢 PASS

Justification: This is the 5th independent, from-scratch verification of the same underlying
numbers and manuscript text this session, and every single one of the 8 checklist items in the
task brief reproduces exactly: the three cross-reference fixes are complete and no residual
instance of the same defect exists anywhere in the document; the statistical pairing (32/32, 0/18,
30/30, 2/20, their p-values, and the 32/50 aggregate with its Wilson CI) independently recomputes
to full precision from the frozen 240-row CSV using a script written from scratch, with no
p-value ever misattached to the exceptionless per-row bands; no rejected claim has resurfaced and
no production number appears inside the Results section; all protected/frozen artifacts are
untouched and the exp1-final directory is confirmed byte-identical to its freeze commit; the
staged file list is exactly the 6 expected paths with no deletions; the three named scratch files
are absent from the tree; the test suite passes 30/30; and the git-hygiene/secrets scan is clean.
The three findings recorded above are all OPTIONAL FUTURE WORK (stray gitignored pycache debris,
an undeclared-but-inert new dependency, and a stale GPS pointer file not in scope for this task) —
none of them touch research integrity, statistical correctness, or the safety of the staged commit.
Safe to checkpoint as staged.

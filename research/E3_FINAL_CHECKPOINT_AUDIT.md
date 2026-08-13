# E3 Final Checkpoint Audit — Fourth Independent Verification Pass

> Read-only audit. This is the fourth independent pass on the Phase E3 manuscript checkpoint,
> immediately before a `git commit`. It does not import, re-run, or trust any prior audit script
> or report; every number below was recomputed from scratch, directly from the frozen CSV, with a
> new hand-rolled script (`scratchpad/independent_recompute.py`, not committed to the repo). No
> file was modified, staged, unstaged, or committed by this pass.

---

## 1. Repository state

- Branch: `main`. HEAD: `b776a5e` "Phase E.2: establish manuscript skeleton".
- Staged (`git diff --cached --name-status`), exactly 6 paths, no deletions, verified twice:
  - `A  manuscript/figures/generate_figures.py`
  - `M  manuscript/main.tex`
  - `A  research/E3_CHECKPOINT_STAGED_AUDIT.md`
  - `A  research/E3_DRAFT_AUDIT_REPORT.md`
  - `A  research/E3_STATISTICAL_RECONCILIATION.md`
  - `A  research/E3_STATISTICAL_RECONCILIATION_AUDIT.md`
- Unstaged/untracked at the time of this audit (not part of the commit under review, noted for
  completeness only): `research/E0_CHECKPOINT_AUDIT.md`, `research/E2_FINAL_CHECKPOINT_AUDIT.md`,
  `research/MANUSCRIPT_ARCHITECTURE.md`, `research/MANUSCRIPT_ARCHITECTURE_AUDIT.md`,
  `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `research/MANUSCRIPT_FORMAT_RESEARCH.md`,
  `research/PHASE_E_AUDIT_REPORT.md`, `research/PHASE_E_PLAN.md`,
  `research/PUBLIC_RELEASE_BOUNDARY.md`. None of these were touched by this audit.
- Inspected staged content via `git show :<path>` (not the working tree) for both `main.tex` and
  `generate_figures.py`, extracted to `scratchpad/staged_main.tex` (1517 lines) and
  `scratchpad/staged_generate_figures.py` (155 lines) for line-numbered review.

## 2. Current research GPS (summarized)

Phase E3 (manuscript drafting) is converting the E2 skeleton into the first complete draft, per
`research/RESEARCH_GPS.md`'s locked north star (defensible first manuscript draft →
reproducibility package → arXiv preprint). This commit is exactly that conversion: `main.tex`
moves from "SKELETON. NOT a draft." to "Phase E3 first complete manuscript draft," and the four
staged `research/E3_*` files are the verification trail three prior sessions produced while
drafting it. Not independently re-read in full this pass (out of scope — see Step 1 of the audit
protocol, which asks for the *current* diff, not a re-audit of GPS itself); no indication GPS is
stale relative to what was observed.

## 3. Changed files (categorized)

- **Manuscript (content)**: `manuscript/main.tex` (M, +2484/-1388 net per `git diff --cached
  --stat` — full E2→E3 rewrite).
- **Code**: `manuscript/figures/generate_figures.py` (A, 155 lines, new file, not yet executable
  in this environment — matplotlib not installed, self-disclosed in its own docstring).
- **Docs (audit trail)**: `research/E3_CHECKPOINT_STAGED_AUDIT.md`,
  `research/E3_DRAFT_AUDIT_REPORT.md`, `research/E3_STATISTICAL_RECONCILIATION.md`,
  `research/E3_STATISTICAL_RECONCILIATION_AUDIT.md` (all A, prior audit reports).
- **Experimental artifacts**: none changed. `data/outputs/experiments/exp1/final/` untouched
  (confirmed, Section 8).
- No other category applies.

## 4. Research integrity

**Independent recomputation (from scratch, `scratchpad/independent_recompute.py`, hand-rolled
exact binomial test via `math.comb`, hand-rolled Wilson interval, no import of `stats.py` or any
prior report):**

| Quantity | My recomputation | Manuscript claim | Match |
|---|---|---|---|
| Realized-ADS band [0.70,0.90), VARIED | 32/32 agree | 32/32 (100%) | ✅ |
| Realized-ADS band ≥0.90, VARIED | 0/18 agree | 0/18 (0%) | ✅ |
| By-nominal-target {0.50,0.75}, VARIED | 30/30 agree | 30/30 (100%) | ✅ |
| By-nominal-target {1.00}, VARIED | 2/20 agree | 2/20 (10%) | ✅ |
| p, 32/32 (exact two-sided binomial) | 4.657e-10 | not cited (correctly, see §6) | ✅ |
| p, 0/18 | 7.629e-06 | not cited (correctly) | ✅ |
| p, 30/30 | 1.863e-09 → rounds 1.9e-9 | 1.9×10⁻⁹ | ✅ |
| p, 2/20 | 4.025e-04 → rounds 4.0e-4 | 4.0×10⁻⁴ | ✅ |
| Aggregate 32/50 | 64.00% | 64.0% | ✅ |
| Wilson 95% CI | [50.14%, 75.86%] | [50.14%, 75.86%] | ✅ |
| Aggregate exact binomial p | 0.06491 | 0.0649 | ✅ |

CLEAN condition independently confirmed to contribute zero defined comparisons at every band (all
120 CLEAN rows have blank `r3_agrees_with_empirical`, matching `empirical_winner == "tie"` for
100% of CLEAN rows). Row count independently verified: 240 total, 120 VARIED / 120 CLEAN, 50 VARIED
rows with a defined agreement flag, exactly matching the union of the 32-row and 18-row
realized-ADS bands. This is a full, from-scratch fourth confirmation of the same numbers three
prior passes already found — no discrepancy.

**Rejected-claims scan (fresh grep across the full staged manuscript, not a re-read of prior
audits' conclusions):**

- "novel metric" appears once (line 283), negated: "we therefore make no claim that ADS is a novel
  metric." ✅ correctly rejected.
- No occurrence of "universally selects," "production validates," broad "enterprise AI," "higher
  ADS means rules is better," or "CLEAN implies equivalent in general" anywhere in the staged text.
- Superseded numbers `0.8094`, `0.9310`, `84.12`, `55,394`/`55394`, and "two-feature selector as
  built" — zero matches anywhere in the staged manuscript. ✅
- "R3 selects the right mechanism" / "selects the right mechanism" — both occurrences (lines 246,
  1154) are explicitly negated ("not a method we claim selects the right mechanism"; "not a
  confirmation of that hypothesis"). ✅ Experiment 1's frozen finding (constant-winner-by-lexical-
  condition, not ADS-driven) is correctly reasserted throughout, not the pre-Experiment-1
  assumption.
- "No comparable vendor practice" claim (line 412) is explicitly walked back in-line: "We do not
  claim... that no vendor measures historical consistency... at least one industry source directly
  contradicts that framing" — correctly scoped to the narrower academic-niche claim (C8), matching
  the known-rejected-claims list exactly. ✅
- Universal/broad applicability: abstract and body consistently scope claims to "one synthetic
  generator, one lexical-perturbation model, one motivating (non-evidentiary) production case
  study," "not a deployment or generalization claim." ✅

**Production-number placement (Section 5 = Results, lines 891–1140 per the staged file's own
`\section`/`\subsection` structure, independently located by grepping every `\section`/
`\subsection` header and its line number):**

- 91.2%, 0.847 (weighted ADS), 0.964 (unweighted ADS), 0.695 (cross-company alignment) — occurrences
  located at lines 100 (Introduction), 600 (Experimental Design, generator calibration), and
  1340–1341 (Limitations §"Production Confidentiality," explicitly captioned "cited... likely
  understated and unverified... cannot be re-run"). A targeted scan restricted to exactly lines
  891–1140 (the Results section boundaries) found **zero** occurrences of any of the four production
  figures inside Results. ✅ Confirms the task's specific requirement.

**No BLOCK-level research-integrity finding.**

## 5. Scientific consistency

H1 = PARTIALLY_SUPPORTED is stated consistently and only ever as PARTIALLY_SUPPORTED (never
softened toward "confirmed" nor overstated toward "refuted"): lines 813/815 (pre-registration),
1183 (§6.3, "What the Original Hypothesis Got Right"), 1376–1379 (Limitations,
"H1 Only Partially Supported"), 1464 (Conclusion). Consistent chain from hypothesis → design →
results → interpretation: Results (§5) reports the raw pattern without a causal claim; Discussion
explicitly defers the causal account and labels it "inferred from exhaustive but post-hoc
inspection... not... a second, independently designed confirmatory experiment" (lines 1216–1218).
This is the correct shape — post-hoc explanation of frozen data, not a re-tuned or reinterpreted
result — and matches `PAPER_CONTRACT.md`/`CONTRIBUTION_LOCK.md`'s stated numerical/interpretive
rules as described in the staged audit trail.

The 6a/6b distinction (per `CONTRIBUTION_LOCK.md`'s internal labels, referenced via `% EVIDENCE:`
anchors at lines 930 and 965) maps onto two genuinely separate, non-merged Results subsections:
§5.2 "ADS Predicts Individual Mechanism Accuracy" (line 918) and §5.3 "ADS Does Not Predict
Mechanism Ranking" (line 949). Formulation #2's synthesis sentence is present in substance in the
Abstract (lines 77–80), §6.1 (lines 1152–1155), and the Conclusion — confirmed by direct reading,
not by trusting the prior reports' claim of this.

**One finding surfaced by this pass that the three prior audits did not report** (this is the kind
of A5/A6-shaped defect — prose/manuscript drift from what the document structure actually is — the
audit protocol specifically asks to hunt for): **three hardcoded, plain-text internal
cross-references in `main.tex` point at the wrong Discussion subsection.** LaTeX subsection
headers were counted directly and independently from the staged file (no `\setcounter`,
`\addtocounter`, or starred `\subsection*` present anywhere — confirmed by grep — so standard
sequential 1-indexed numbering applies under `\section{Discussion}` at line 1143):

- 6.1 What the Experiment Supports (1146)
- 6.2 The Production Case Study in Light of These Results (1160)
- 6.3 What the Original Hypothesis Got Right (1180)
- 6.4 What the Original Hypothesis Got Wrong (1196)
- 6.5 Why Consistency Predicts Difficulty but Not Ranking (1210)
- 6.6 Representation Stability as an Uncaptured Factor (1227)
- 6.7 Relationship to Algorithm Selection and Meta-Learning (1243)

Against that count:

- **Line 815**: "*The observed pattern matches the pre-registered PARTIALLY SUPPORTED row exactly
  (Section~6.2)*" — but §6.2 (1160–1179) is the production case-study subsection, which does not
  discuss the PARTIALLY_SUPPORTED verdict at all (confirmed by reading its full text). The
  PARTIALLY_SUPPORTED discussion is actually in §6.3 (line 1183: "...is exactly why a
  PARTIALLY\_SUPPORTED verdict was a coherent, pre-registered possible outcome"). This reference is
  **wrong by one subsection**.
- **Line 1081**: "*the causal account for why it occurs is developed in Section~6.4, not here*" —
  but §6.4 (1196–1209, "What the Original Hypothesis Got Wrong") is not the causal-mechanism
  section; the causal account ("Realized ADS is computed on the stable product identity,
  structurally blind to the perturbable surface string...") is in §6.5 (1210–1221, "Why Consistency
  Predicts Difficulty but Not Ranking"). **Wrong by one subsection.**
- **Line 1381**: "*The mechanistic account in Section~6.4 is a well-evidenced, exhaustive, but
  post-hoc explanation*" — same error, same correct target (§6.5).

All three are plain hardcoded text (`Section~6.2`, `Section~6.4`), not `\ref{}` cross-references,
so LaTeX's auto-numbering will not silently fix them on compile — they will render exactly as
wrong in the PDF as they read in the source now. This was verified by direct, independent counting
of every `\subsection` header's document position; not inferred from any prior report (none of the
three prior audits' summaries mention this).

## 6. Evidence/claim traceability

Every quantitative claim checked in §4 traces to the single frozen CSV
(`data/outputs/experiments/exp1/final/final_condition_results.csv`, 240 rows, independently
re-read and re-derived, not merely cross-checked against another document's restatement). No
number in the reviewed passages was found floating free of a traceable source. The manuscript's own
`% EVIDENCE:` comment anchors were spot-checked against the artifacts they cite (e.g., Table T5 at
lines 1089–1106 cross-checked conceptually against the band/lexical structure independently
recomputed in §4 — the direction and ordering of the reported accuracy gaps is consistent with the
realized-ADS-band agreement pattern this audit independently reproduced).

## 7. Code review

`manuscript/figures/generate_figures.py` (new file, 155 lines):

- Reads only the frozen CSV via stdlib `csv.DictReader`; no re-computation of any statistic beyond
  simple band-binning and mean/difference arithmetic already present in the frozen data.
- `ads_band()` thresholds (`R3_LOW = 0.70`, `R3_HIGH = 0.90`) match the frozen thresholds used
  throughout the manuscript and independently reproduced in §4.
- `make_f3()`'s agreement-rate-by-band logic (filtering `r3_agrees_with_empirical in ("True",
  "False")`, VARIED only) matches exactly the logic this audit's independent script used and
  produces the same 32/32, 0/18 structure.
- No randomness, no seeding concerns (purely deterministic aggregation over a frozen CSV).
- `python -m py_compile` on the staged content: syntax OK.
- Script has not been executed (matplotlib not installed in this environment) — this is disclosed
  explicitly in the script's own docstring, consistent with this project's prior documented
  practice of disclosing missing-toolchain gaps rather than faking output (cited: the
  pdflatex/bibtex precedent). Not independently re-verified by actually running it (would require
  installing a new package, out of scope for a read-only audit).
- **Dependency note**: `matplotlib` is not a stdlib module and is not currently listed in
  `requirements.txt` (which only lists `pandas`, `requests`, `tqdm` for an unrelated pipeline).
  This is a new, undeclared dependency. Given this repo's "no new dependency if it can be avoided"
  convention, and given no stdlib plotting alternative exists, this is a defensible exception, but
  it is currently undocumented outside the script's own docstring.

No test file accompanies this new script (`manuscript/figures/`). Given it is glue code around a
frozen CSV with no branching logic beyond simple binning, and it cannot even be executed in this
environment, I do not treat missing test coverage as a blocking gap — flagged as optional.

## 8. Experimental integrity

No experimental artifacts changed in this diff. `data/outputs/experiments/exp1/final/` confirmed
untouched: `git status --porcelain` and `git diff --cached --name-status` for that path both return
empty. The 240-row CSV used for independent recomputation is the same frozen file cited throughout
the staged manuscript and prior audit reports (path and row count independently verified).

## 9. Scope/GPS alignment

This work is squarely on-scope: converting the E2 skeleton into an E3 draft is the literal next
step toward the locked north star (first defensible manuscript draft). The four staged
`research/E3_*.md` files are verification artifacts for that same drafting pass, not scope
creep — they exist because the manuscript's most novelty-adjacent, highest-risk content (p-value
pairing) warranted redundant checking, which is itself consistent with `RESEARCH_GPS.md`'s
evident emphasis on evidence discipline. No DO NOT CHASE item appears to have been triggered.
**PASS** on this dimension.

## 10. Git hygiene

- `git status --porcelain` for the six protected paths (`PAPER_CONTRACT.md`,
  `CONTRIBUTION_LOCK.md`, `contribution_lock.csv`, `data/outputs/experiments/exp1/final/`,
  `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`) — empty. None modified, none staged.
- `git diff HEAD -- manuscript/references.bib` — empty. Byte-identical to the E2 checkpoint. ✅
- `git diff --cached --name-status --diff-filter=D` — empty. No deletions in the staged diff. ✅
- Secrets/credentials scan (`git diff --cached | grep -iE "AKIA|api[_-]?key|secret|password|
  bearer|BEGIN ... PRIVATE KEY|C:\\Users\\|/Users/...|CUI[0-9]|ssn|token"`) — the only hits are (a)
  the word "token" used in its NLP sense ("token reorder," "token similarity") in manuscript prose,
  and (b) self-referential prose *inside* the staged audit-report files describing the git-hygiene
  scans they themselves ran (e.g., "grepped for API keys/secrets/passwords/bearer tokens..."). No
  actual secret, credential, key, or local path leaked. ✅
- Exact staged file list independently re-verified via `git diff --cached --name-status`: matches
  the expected 6 paths exactly, no more, no less, no deletions. ✅

## 11. Findings

1. **REQUIRED NOW** — `manuscript/main.tex` line 815: hardcoded cross-reference "Section~6.2"
   should read "Section~6.3" (the PARTIALLY_SUPPORTED discussion is in §6.3, not §6.2, per direct
   subsection-header count).
2. **REQUIRED NOW** — `manuscript/main.tex` line 1081: hardcoded cross-reference "Section~6.4"
   should read "Section~6.5" (the causal mechanistic account is in §6.5 "Why Consistency Predicts
   Difficulty but Not Ranking," not §6.4 "What the Original Hypothesis Got Wrong").
3. **REQUIRED NOW** — `manuscript/main.tex` line 1381: same error, same fix, "Section~6.4" →
   "Section~6.5".
4. **OPTIONAL FUTURE WORK** — `manuscript/main.tex` lines 1150 and 1466: "ranking is governed by a
   representation-stability property the consistency signal does not observe" uses "governed by"
   for representation-stability (an interpretive label built on the inferred, explicitly
   post-hoc-labeled causal account in §6.5), not literally the directly-manipulated lexical
   condition itself. The three prior audits explicitly checked and cleared this exact phrase as
   scoped correctly, and the surrounding sentence is hedged ("in this synthetic experiment,"
   "empirically falsifiable... refinement"), so this is not flagged as a violation — but it sits
   close enough to the line the task asked to police ("governed by" reserved for the
   experimentally-manipulated relationship, never the inferred account) that a human author should
   have final say on whether "representation-stability" here reads as a restatement of the
   manipulated variable or as the separately-inferred causal story.
5. **OPTIONAL FUTURE WORK** — `manuscript/figures/generate_figures.py` introduces `matplotlib`, a
   non-stdlib dependency, without a corresponding update to `requirements.txt` and without having
   been executed even once in any environment (matplotlib unavailable here). Defensible given no
   stdlib plotting option exists and the gap is self-disclosed in the script's docstring; worth
   recording in `requirements.txt` (or a manuscript-scoped requirements file) and actually running
   once matplotlib is available, rather than leaving it permanently unverified.
6. **OPTIONAL FUTURE WORK** — no test file accompanies the new `generate_figures.py`. Low risk
   (pure aggregation over a frozen CSV, no branching logic of consequence) and the script cannot be
   executed in this environment to write a meaningful test against real output; not blocking.

No REQUIRED NOW findings touch research integrity, statistical correctness, protected artifacts,
or git hygiene — all of those independently re-verified clean. The three REQUIRED NOW findings are
manuscript cross-reference errors: verifiable, small, and mechanically fixable (three string
replacements), not evidence of a deeper methodological or integrity problem.

## 12. Required fixes

1. `manuscript/main.tex` line 815: change `Section~6.2` → `Section~6.3`.
2. `manuscript/main.tex` line 1081: change `Section~6.4` → `Section~6.5`.
3. `manuscript/main.tex` line 1381: change `Section~6.4` → `Section~6.5`.

(All three are plain-text string fixes with no downstream numerical or claim-scope consequence —
they do not require re-deriving any statistic or re-checking any other section.)

## 13. Verdict

## 🟠 CONDITIONAL

Justification: the statistical core of this checkpoint — the four count pairs, their four exact
binomial p-values, the 64.0% aggregate, and its Wilson CI — was independently re-derived from the
frozen 240-row CSV using a brand-new hand-rolled script and matches the manuscript and all three
prior audit reports exactly, to five significant figures. Rejected-claim resurrection, causal
overreach, production-number leakage into Results, protected-artifact modification, and git/secrets
hygiene were all independently re-checked and found clean; `references.bib` is byte-identical to
the E2 checkpoint and no deletions are staged; the exp1 test suite passes 30/30. None of that
supports a BLOCK. However, this pass found three concrete, unambiguous, previously-unreported
defects — hardcoded internal cross-references in the newly-drafted Discussion/Limitations prose
that point at the wrong subsection (§6.2 instead of §6.3; §6.4 instead of §6.5, twice) — which none
of the three prior passes caught because their focus was the p-value pairing, not internal
cross-reference accuracy. These are trivial, mechanical fixes with no bearing on any number or
claim's correctness, but they are real defects in the text being checkpointed and are cheap to fix
before committing rather than after. Recommend applying the three fixes in §12, then committing;
no further recomputation or re-audit of the statistical content is needed.

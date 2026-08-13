# E3 Checkpoint — Staged-Content Audit (Third Independent Verification)

> Read-only, independent, from-scratch third-pass verification of exactly what is
> **staged** for the E3 checkpoint commit (`git diff --cached --name-status`), performed
> without reusing `scripts/experiments/exp1/stats.py` or trusting the prior two audit
> reports' numbers — every count, band, and p-value below was recomputed by this session
> directly from the frozen CSV using a fresh, hand-rolled script. This document does not
> modify, and was not used to modify, `manuscript/main.tex`, any frozen evidence, or any
> other file. Nothing was staged, unstaged, or committed by this audit.

---

## 1. Scope confirmation

`git diff --cached --name-status` (re-verified directly, not assumed):

```
A  manuscript/figures/generate_figures.py
M  manuscript/main.tex
A  research/E3_DRAFT_AUDIT_REPORT.md
A  research/E3_STATISTICAL_RECONCILIATION.md
A  research/E3_STATISTICAL_RECONCILIATION_AUDIT.md
```

Exactly 5 paths, matching the task description. No deletions (`git diff --cached
--diff-filter=D --name-only` empty). No protected/frozen file appears in this list:
confirmed absent are `research/CONTRIBUTION_LOCK.md`, `research/PAPER_CONTRACT.md`,
`research/contribution_lock.csv`, `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`,
and anything under `data/outputs/experiments/exp1/final/`.

`diff <(git show :manuscript/main.tex) manuscript/main.tex` returns **no output** — the
staged index content is byte-identical to the working-tree file, so all line numbers
cited below (from `git show :manuscript/main.tex`, 1517 lines) apply equally to both.

Branch `main`, HEAD `b776a5ed334dc9e360c6c30ed6cf51bb3b2dbd81` ("Phase E.2: establish
manuscript skeleton"), working tree otherwise clean aside from the 5 staged paths and a
set of pre-existing untracked `research/*.md` files from earlier E0–E2 phases
(`E0_CHECKPOINT_AUDIT.md`, `E2_FINAL_CHECKPOINT_AUDIT.md`, `MANUSCRIPT_ARCHITECTURE.md`,
`MANUSCRIPT_ARCHITECTURE_AUDIT.md`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`,
`MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_AUDIT_REPORT.md`, `PHASE_E_PLAN.md`,
`PUBLIC_RELEASE_BOUNDARY.md`) — not staged, not part of this review's scope, already
flagged by the prior E3 draft audit as a pre-existing git-hygiene gap not introduced by
this pass.

`references.bib` is staged as unmodified: it is not listed in the staged name-status at
all (confirming it was not touched this pass), and `git diff HEAD --
manuscript/references.bib` returns empty, confirming it is byte-identical to the E2
checkpoint commit.

---

## 2. Independent recomputation (third pass, from the raw 240-row CSV)

Row count and schema confirmed: `data/outputs/experiments/exp1/final/final_condition_results.csv`
has exactly 240 data rows (241 lines including header), all `status == ok`, 24 columns,
120 CLEAN (`lexical_variation == False`) / 120 VARIED (`lexical_variation == True`), 6
nominal targets {0.0, 0.2, 0.3, 0.5, 0.75, 1.0} × 20 seeds × 2 lexical conditions = 240.
Confirmed unmodified by this pass (git-clean; not staged).

Using a fresh stdlib-only script (own `comb`-based exact two-sided binomial test, own
Wilson-interval formula — no import of `stats.py`, no reuse of either prior audit's
script):

**Realized-ADS-band (per-row `realized_det_pct`), VARIED only:**
- `[0.70, 0.90)`: 32 agree / 0 disagree / 32 defined → **32/32 = 100%**
- `>=0.90`: 0 agree / 18 disagree / 18 defined → **0/18 = 0%**
- CLEAN, all three bands: 0 defined comparisons anywhere (all 120 CLEAN rows blank
  `r3_agrees_with_empirical`, `empirical_winner == tie`) — independently confirmed.

**By-nominal-target (`target_deterministic_share`), VARIED only:**
- Targets {0.50, 0.75}: 30 agree / 0 disagree / 30 defined → **30/30 = 100%**
- Target {1.00}: 2 agree / 18 disagree / 20 defined → **2/20 = 10%**

**Exact two-sided binomial p-values (independently computed):**
| Count pair | p (this pass) |
|---|---|
| 32/32 | 4.656612873077393×10⁻¹⁰ |
| 0/18 | 7.62939453125×10⁻⁶ |
| 30/30 | 1.862645149230957×10⁻⁹ (rounds to 1.9×10⁻⁹) |
| 2/20 | 0.0004024505615234375 (rounds to 4.0×10⁻⁴) |

**Overall aggregate:** agree=32, disagree=18, blank=190 (120 tie + 70 N/A `llm_required`),
total=240. **32/50 = 64.0000%**, Wilson 95% CI **[50.1410%, 75.8613%]**, exact binomial
p vs. 0.5 = **0.064909**.

**Result: exact match, to full float precision, with both prior independent passes**
(`E3_STATISTICAL_RECONCILIATION.md` §2/§6 and `E3_STATISTICAL_RECONCILIATION_AUDIT.md`
§2), and with the task's stated expected values. This is the third independent
derivation of the same numbers from the same raw file, using a third distinct script,
and it agrees to the last printed digit. p=1.9×10⁻⁹ mathematically belongs only to
30/30; p=4.0×10⁻⁴ belongs only to 2/20; neither belongs to 32/32 or 0/18.

---

## 3. Staged manuscript pairing check (item 2)

Checked every occurrence of `32/32`, `0/18`, `30/30`, `2/20`, the two p-values, `64.0%`,
and `32/50` in the staged `main.tex` (line numbers from `git show :manuscript/main.tex`):

- **§5.4 "R3 Threshold Agreement by Realized-ADS Region" (lines 984–1013):** states "32 of
  32 ... 0 of 18" (990–991) with no p-value attached to either. The aggregate-explanation
  sentence (1006–1009) restates "32 of 32 and 0 of 18" as exceptionless, then separately
  attaches "$p=1.9\times10^{-9}$ (30 of 30)" and "$p=4.0\times10^{-4}$ (2 of 20)" — each
  p-value is inline-adjacent to its own correct count. Correct.
- **Table T4 (`\label{tab:t4}`, lines 1036–1057):** row `Overall agreement (32/50)` has no
  p-value column value tied to 32/32 or 0/18 (those counts do not appear as table rows at
  all — only the aggregate 32/50 does); `By target, targets 0.50/0.75 (30/30)` row →
  $1.9\times10^{-9}$; `By target, target 1.00 (2/20)` row → $4.0\times10^{-4}$. The
  table's own caption (1038–1043) explicitly states the sharper 32/32/0/18 counts are
  reported in §5.4 and that "no independently frozen $p$-value exists for those exact
  counts, so none is stated here." Correct, and the pairing is unambiguous in tabular
  form.
- **§5.6 "Statistical Interpretation" (lines 1110–1125):** "$p=1.9\times10^{-9}$ for the
  30/30 retrieval-region band and $p=4.0\times10^{-4}$ for the 2/20 rules-region band" —
  explicit named attachment, no ambiguity. Immediately followed by "The sharper per-row
  realized-ADS bands (32/32 and 0/18, Section~5.4) ... are not independently paired with
  a frozen $p$-value anywhere in this paper's evidence base." Correct.
- **§6.3 "What the Original Hypothesis Got Right" (lines 1180–1190):** "perfect,
  exceptionless agreement (32 of 32, Section~5.4), with the corresponding
  by-nominal-target count independently significant at $p=1.9\times10^{-9}$
  (Section~5.6)" — the p-value is explicitly attributed to "the corresponding
  by-nominal-target count," not to 32/32 itself. Correct.
- **Figure F3 caption (lines 1029–1032):** "100\% (32/32) ... versus 0\% (0/18)" — no
  p-value anywhere in the caption. Correct.

**No mismatched pairing found anywhere in the staged file.** A dated correction comment
block immediately after Table T4 (lines 1058–1067) self-documents the original defect and
the fix applied, consistent with both prior reports' account of what changed and why.

---

## 4. Claim-strength / hedging scan (item 3)

Grepped the staged file for "ADS selects"/"ADS chooses" (0 matches), `prove`/`proves`
(0 matches in body prose), `valid*`, `confirm*`, `causal`/`cause*`, `independent*`,
`orthogonal` (0 matches), `govern*`, `classifier`, and inspected every hit connected to
Experiment 1 or this paper's own mechanisms:

- **No unhedged "ADS selects/chooses/proves/validates" language** connected to this
  paper's own claims. The one `validated` occurrence describing this work (line 1473,
  Conclusion) reads "...not a validated method, and not a new metric or architecture" —
  a negation, not an assertion.
- **`confirm`/`confirmed`:** every occurrence connected to H1 or this experiment is
  negated ("does not confirm," "not... confirmed," "not a confirmation of that
  hypothesis"). No occurrence asserts H1, ADS, or the paper's mechanisms were confirmed.
- **`causal`:** both occurrences (line 1080, §5.5; line 1220, §6.5) explicitly hedge —
  "the causal account ... is developed in Section 6.4 ... that account rests on
  additional, explicitly post-hoc reasoning" and "We state this account explicitly as
  inferred from exhaustive but post-hoc inspection ... not as the result of a second,
  independently designed confirmatory experiment." Neither is presented as proven.
- **`governed`/`governs`** (4 body-prose occurrences: line 957 in §5.3, line 1150 in
  §6.1, line 1250 in §6.7 "Relationship to Algorithm Selection and Meta-Learning", line
  1466 in Conclusion): every occurrence attaches "governed by" to the (manipulated
  lexical condition) → (empirical winner) relationship, which the manuscript itself
  explicitly licenses at lines 955–958 ("The lexical condition here is a manipulated,
  controlled experimental factor, not merely an observational correlate, which is what
  licenses describing the empirical winner as *governed by* the lexical condition").
  Lines 1150/1466 phrase this as "governed by a representation-stability property" —
  read in context this is a paraphrase of the same manipulated lexical-condition
  relationship (the paper's own §4.4/§6.6 language treats "representation stability" as
  the conceptual label for what the lexical/surface-form manipulation instantiates in
  this experiment), not the separately-hedged, explicitly-inferred ADS-blindness causal
  account of §6.5 (which never uses "governed"). No occurrence of "governed by" is
  attached to the inferred causal account. **Minor non-blocking note:** the prior
  `E3_STATISTICAL_RECONCILIATION.md` §7 cites this fourth occurrence as being in
  "§6.6" — this pass finds it is actually in §6.7 ("Relationship to Algorithm Selection
  and Meta-Learning"; §6.6 is "Representation Stability as an Uncaptured Factor" and
  contains no "governed" occurrence at all). This is a section-number citation slip in
  a prior *report*, not a defect in the manuscript text itself — the manuscript content
  at that location is correctly hedged either way.
- **`classifier`:** the one body-prose occurrence (line 406, §2.8) describes what a
  *cited paper* (Jørgensen & Igel) studied ("a global classifier generalizes far worse
  across companies than per-company models"), not this paper's own rules/retrieval
  mechanisms. Correct, matches both prior audits' finding.
- **`independent`:** all occurrences are either the standard statistical/methodological
  sense ("independently significant," "independently reproducible," "independent
  variable," "independently designed confirmatory experiment," "Absence of Independent
  Production Validation") or the author-affiliation placeholder — none overclaim.

No claim-strength violation found in the staged content.

---

## 5. H1 / 6a-6b / Formulation #2 integrity (item 4)

- **H1 = PARTIALLY_SUPPORTED:** every occurrence of "partially supported" in the staged
  file (lines 813, 815, 1295 comment, 1376 heading, 1378, 1464) is consistent; no
  occurrence anywhere softens this toward "confirmed" or "supported" unqualified.
- **6a/6b never merged:** confirmed as two separate, adjacently titled Results
  subsections — §5.2 "ADS Predicts Individual Mechanism Accuracy" (line 918) and §5.3
  "ADS Does Not Predict Mechanism Ranking" (line 949) — mirrored in Discussion by §6.3
  "What the Original Hypothesis Got Right" / §6.4 "...Got Wrong". No sentence collapses
  these into a single undifferentiated verdict.
- **Formulation #2's substance** (the 6a/6b split plus the "informative about
  difficulty, not ranking" synthesis) is present verbatim in substance in the Abstract
  (lines 67–74), §6.1 "What the Experiment Supports" (lines 1148–1155), and the
  Conclusion (lines 1464–1467).

All three intact and unaltered, matching the prior two audits' findings.

---

## 6. references.bib (item 5)

`git diff --cached -- manuscript/references.bib` — empty (file not staged, since it was
not modified). `git diff HEAD -- manuscript/references.bib` — empty. Confirmed unchanged
from the E2 checkpoint commit.

---

## 7. Staged-file scope re-check (item 6)

Re-verified directly (not assumed) via `git diff --cached --name-status`: exactly the 5
paths listed in §1 above, no more, no fewer. No deletions. No protected/frozen file
staged. See §1 for the full list of protected paths checked and confirmed absent.

---

## 8. Test suite (item 7)

`python -m pytest scripts/experiments/exp1/ -q` → **30 passed** in 17.06s. No failures,
no errors, no skips.

---

## 9. Additional independent checks performed this pass

- **`generate_figures.py` re-read in full (staged, new file):** confirmed read-only
  (`open(RESULTS_CSV, ...)`, no write-mode file handle on any input path), no hardcoded
  headline numbers (only the frozen `R3_LOW=0.70`/`R3_HIGH=0.90` threshold constants,
  matching the harness), deterministic (no RNG/sampling anywhere in the file), and its
  own `ads_band()` binning logic matches the same 0.70/0.90 thresholds this pass
  independently recomputed against in §2. `savefig()` calls target only
  `manuscript/figures/`, never `data/outputs/`.
- **Git-hygiene scan of the staged diff:** grepped for API keys/secrets/passwords/bearer
  tokens/PEM private-key headers/AWS key patterns — zero matches (only a prose line in
  one of the staged reports discussing "secrets/client data/local paths" as a checklist
  item, not an actual secret). Grepped for local Windows paths (`C:\Users\`) and the
  operator's username — zero matches in the staged diff content. No `.bak`/`.swp`/`.orig`/
  `.tmp` files in the staged file list.

---

## 10. Findings

1. **OPTIONAL FUTURE WORK** — `research/E3_STATISTICAL_RECONCILIATION.md` §7 cites the
   fourth "governed by" occurrence as located in "§6.6," but this pass finds it is
   actually in §6.7 ("Relationship to Algorithm Selection and Meta-Learning"); §6.6
   ("Representation Stability as an Uncaptured Factor") contains no "governed"
   occurrence. This is a citation slip in a prior audit *report*, not a defect in
   `manuscript/main.tex` — the manuscript text at that location is correctly hedged
   regardless of which subsection number is cited for it. No manuscript change needed;
   flagged only for completeness of the audit trail. (File: `research/E3_STATISTICAL_RECONCILIATION.md`, line 216 area / §7; also `manuscript/main.tex` line 1250.)
2. **OPTIONAL FUTURE WORK** — the pre-existing untracked `research/*.md` files from
   earlier E0–E2 phases (listed in §1) remain unstaged/uncommitted. Not introduced or
   worsened by this pass; already flagged by `research/E3_DRAFT_AUDIT_REPORT.md` §13 as
   a housekeeping item for a human decision at checkpoint time, not this audit's call.

No REQUIRED NOW findings. No research-integrity violation, no evidence/prose mismatch,
no frozen-artifact alteration, no unsafe git state, and no code-correctness defect
found in the staged content.

---

## 11. Verdict

## 🟢 PASS

Third independent, from-scratch recomputation of every disputed number (realized-ADS-band
32/32 and 0/18; by-nominal-target 30/30 and 2/20; their four exact binomial p-values;
the 32/50=64.0% aggregate, its Wilson CI, and its exact binomial p) exactly reproduces
both prior independent passes to full float precision, using a third, independently
written script against the same unmodified frozen CSV. Every occurrence of the disputed
values in the staged `manuscript/main.tex` (Table T4, §5.4, §5.6, §6.3, Figure F3
caption) pairs each p-value with its correct count; no mismatch remains anywhere in the
staged file. The claim-strength scan found no unhedged causal-proof language, no
mis-scoped "classifier" usage, and confirmed "governed by" is used only for the
experimentally-manipulated lexical-condition relationship, never for the inferred
ADS-blindness account. H1 = PARTIALLY_SUPPORTED, the 6a/6b separation, and Formulation
#2's substance are all intact and unaltered. `references.bib` is confirmed unchanged from
the E2 checkpoint. The staged file list contains exactly the 5 expected paths, no
protected/frozen file, no deletions. The Experiment 1 test suite passes (30/30). Git
hygiene is clean (no secrets, no local-path leakage, no temp files). The two findings
above are cosmetic/administrative and do not block the checkpoint. This staged content is
ready to commit.

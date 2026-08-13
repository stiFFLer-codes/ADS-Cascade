# E2 Final Checkpoint Audit (Phase E2 — pre-stage gate)

> Independent re-verification of the Phase E2 checkpoint (`manuscript/main.tex`,
> `manuscript/references.bib`, `research/MANUSCRIPT_SKELETON_AUDIT.md`) after the three required/
> non-blocking fixes from the prior `MANUSCRIPT_SKELETON_AUDIT.md` pass were reportedly applied.
> Everything below was re-derived directly from the current file contents, git state, and source
> documents (`CONTRIBUTION_LOCK.md`, `PAPER_CONTRACT.md`, `MANUSCRIPT_ARCHITECTURE.md`,
> `EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `EXPERIMENT_1_FINAL_RESULTS.md`,
> `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`, `research/literature/citation_ledger.csv`,
> `ads_metric_prior_art.csv`, `llm_advisory_prior_art.csv`) — not taken on the prior audit's or the
> implementing pass's word. No file was modified except this one. Nothing was staged, committed, or
> pushed.

---

## 1. The three required/non-blocking fixes — independently re-verified present

**Fix #1 (REQUIRED NOW in the prior audit) — Discussion subsection positioning the production case
study relative to 6a/6b.** CONFIRMED PRESENT. `manuscript/main.tex` lines 1330–1362:
`\subsection{The Production Case Study in Light of These Results}`, inserted directly after
`\subsection{What the Experiment Supports}`. Its draftnote states, verbatim in spirit: "consistent
with 6a ... never itself a controlled test of 6b ... this experiment does not confirm the
production observation, it investigates the more general question the observation raised" — this
is a word-for-word match to `research/MANUSCRIPT_ARCHITECTURE.md` §6's required framing sentence
("this experiment does not confirm the production observation, it investigates the more general
question the observation raised"), independently re-read at `MANUSCRIPT_ARCHITECTURE.md` §6. The
subsection cites `EVIDENCE_BASELINE.md` §1 and `r3_threshold_analysis.md` as ALLOWED EVIDENCE
(previously absent from every Discussion draftnote — this was the exact mechanism of the gap) and
carries an explicit MUST-NOT-SAY guard against implying the production case underwent the same
lexical-noise manipulation. Section 6 header comment (lines 1302–1307) explicitly records that this
subsection was added in response to the flagged gap.

**Fix #2 (OPTIONAL, prior audit) — undocumented Results-subsection-count deviation.** CONFIRMED
FIXED. `manuscript/main.tex` lines 1050–1059 now carry a "NOTE ON SUBSECTION COUNT" comment
explaining the 6-vs-7-subsection difference between `MANUSCRIPT_ARCHITECTURE.md` §4's plan and the
implemented structure, framed as a deliberate E2-brief refinement, not silent drift.

**Fix #3 (OPTIONAL, prior audit) — over-specified `rankgpt2023` author field.** CONFIRMED FIXED.
`manuscript/references.bib` line 97 now reads `author = {Sun and Yan and Ma and others}`, matching
`research/literature/llm_advisory_prior_art.csv` row G2-01's own abbreviated author field ("Sun,
Yan, Ma, et al.") — the previously-flagged fabricated given names ("Weiwei", "Lingyong", "Xinyu")
are gone. No field in this entry now goes beyond what the ledger itself resolved.

All three fixes verified by direct read of the current files, not by trusting the task
description's claim that they were made.

---

## 2. `research/MANUSCRIPT_SKELETON_AUDIT.md` — unchanged, but missing the repo's own resolution-note convention

CONFIRMED: the file's content is identical to what a CONDITIONAL verdict with Finding #1 REQUIRED
NOW / Findings #2–#3 OPTIONAL would read as a live, unresolved gap — it still says (line 106): "add
... before treating the skeleton as E3-ready," with no indication the fix was applied.

**This repo has an established convention for exactly this situation.**
`research/PAPER_CONTRACT_AUDIT_REPORT.md` (one of the five protected historical audit files) carries
a short blockquote **"Resolution note (added after this audit ran):"** inserted right after its
header, stating which REQUIRED NOW findings were fixed, when, and by what verification — without
rewriting the original CONDITIONAL verdict below it. `research/MANUSCRIPT_SKELETON_AUDIT.md`
currently has no equivalent note anywhere in the file.

**Finding (non-blocking, see §11).** This is a documentation-hygiene gap relative to the project's
own established practice, not a research-integrity problem — I independently re-verified in §1
above that the underlying fix is actually present in the current `main.tex`/`references.bib`, so
the substance is not in question, only the historical record's legibility to a future reader who
opens `MANUSCRIPT_SKELETON_AUDIT.md` without also checking `main.tex` directly. Recommend the
builder append a short resolution-note blockquote (matching the `PAPER_CONTRACT_AUDIT_REPORT.md`
pattern) before or shortly after staging — not required to block this checkpoint, since it is a
non-substantive omission in a file explicitly designated as a historical record, and this audit
independently supplies the missing confirmation.

---

## 3. Full checklist re-run (items a–q)

**a. E1 architecture fidelity, including the new Discussion subsection.** PASS. Verified directly
against `MANUSCRIPT_ARCHITECTURE.md` §6 (quoted above) — exact match. Title, section hierarchy
(9 top-level sections + Reproducibility Statement), figure/table placeholders (F1–F4, T1–T6, F5/F6
correctly absent/present) all independently re-checked against `MANUSCRIPT_ARCHITECTURE.md` §1,
§3, §7, §8, §10 — no drift found beyond the two already-documented, non-blocking deviations (§1
Fix #2 above, and the pre-existing classifier→mechanism title substitution, itself explained inline
in the file header).

**b. `PAPER_CONTRACT.md` §3 forbidden phrases.** PASS. Grep for the full phrase list found 4 hits
total (`novel metric` ×2, `means rules is better` ×1, `independently validat` ×1), all four inside
an explicit "OUR NON-CLAIM:"/"MUST NOT SAY:" negation, none asserted as positive content. The
`~55,394` figure and "no comparable vendor" framing do not appear at all.

**c. `CONTRIBUTION_LOCK.md` respected — Formulation #2, §6/§7.** PASS. Read `CONTRIBUTION_LOCK.md`
§6 directly: the locked 6a/6b/Synthesis wording matches `main.tex` §5.2/§5.3/§6.1's draftnotes in
substance (correlation strength, 120/120 vs. 120/120 constancy, the "difficulty not ranking"
synthesis) with no strengthening. §7's rejected-claims list (ADS-as-novel-metric, universal
architecture-selection, "no vendor measures history first," etc.) — none resurface as positive
assertions anywhere in `main.tex` (cross-checked against the rejected-claims list in this audit's
own briefing; every instance found is inside a non-claim/negation).

**d. 6a/6b kept explicitly separate everywhere, including the new Discussion subsection.** PASS.
Separate subsections in Results (§5.2/§5.3), Problem Setting (§3.5), Introduction (§1.7), and
Discussion (§6.1 states the synthesis, §6.3/§6.4 keep "got right"/"got wrong" separate). The new
§6.2 (Production Case Study) explicitly ties the production observation only to 6a ("consistent
with 6a") and explicitly disclaims it as any test of 6b — the distinction is preserved in the new
content, not just the old.

**e. H1 stated as PARTIALLY_SUPPORTED only.** PASS. `main.tex` §7.10 ("H1 Only Partially
Supported") states this as the lead verdict, explicitly "not softened toward either 'confirmed' or
'refuted.'" No other subsection asserts a stronger or weaker verdict; §6.3/§6.4 ("Got Right"/"Got
Wrong") are consistent with a partial verdict, not a full one.

**f. No rejected claim resurfaces as an assertion.** PASS — re-checked against the audit briefing's
explicit rejected-claims list (ADS-as-novel-metric §2.1/§3.2; general design-time-architecture
pattern §1.3/§2.2/§2.3; full combined system as validated §1.8/§8's WEAK framing in Future Work
§8.5; "no comparable vendor practice" §2.8 explicitly cites the Ken From Finance counter-evidence;
universal/enterprise-AI applicability — never appears; "R3 selects the right mechanism" — directly
contradicted in §5.3/§6.4, not reasserted).

**g. Production data is motivation/case-study only, never in Results; new Discussion subsection
explicitly frames it as never a test of 6b.** PASS. Grepped `main.tex` for `91.2`, `0.847`, `0.964`,
`0.695` (also `84.1%`/`87.56%`/`76,843`, none present at all): all hits are at lines 106/107
(Abstract's explicit "must stay body-only" exclusion list), 138 (Introduction §1.1, correctly
caveated), 694 (Experimental Design §4.2's `0.695` cross-company-alignment *generator parameter*,
not a production citation), and 1585 (Limitations §7.6, correctly caveated). **Zero occurrences
inside the Results section** (confirmed both by grep-line-range check against the section's actual
boundaries, lines 1043–1298, and by the direct read performed in this pass). §6.2 explicitly states
the "does not confirm... investigates the more general question" framing required by
`MANUSCRIPT_ARCHITECTURE.md` §6.

**h. Numerical spot-checks (10 independently re-verified, exceeding the required 5).** PASS on all:
- Pearson r 0.909/0.959 (rules), 0.948/0.955 (retrieval) — matches `CONTRIBUTION_LOCK.md` lines
  165–166 exactly.
- 32/32 (100%) at realized ADS 0.70–0.90, 0/18 (0%) at ≥0.90 — matches
  `EXPERIMENT_1_POSTHOC_ANALYSIS.md` line 172–173 exactly.
- 30/30 (100%) / 2/20 (10%) by-nominal-target secondary framing — matches
  `EXPERIMENT_1_FINAL_RESULTS.md` lines 31/33 exactly.
- Six-row gap table: VARIED −0.1374/−0.1678/−0.1851 and CLEAN +0.0048/+0.0055/+0.0063 — matches
  `EXPERIMENT_1_POSTHOC_ANALYSIS.md` lines 67–72 exactly (rounds to the `main.tex` §5.5 statement of
  −0.137/−0.168/−0.185 and +0.005/+0.005/+0.006).
- Aggregate 32/50 = 64.0%, Wilson CI [50.14%, 75.86%], p = 0.0649 — matches
  `EXPERIMENT_1_POSTHOC_ANALYSIS.md` line 52 and `PAPER_CONTRACT.md` line 158 exactly.
- Band-level p-values 1.9×10⁻⁹ and 4.0×10⁻⁴ — matches `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` lines
  86–87 exactly.
No number in `main.tex` was found that isn't traceable to one of these frozen artifacts.

**i. No fabricated bibliographic metadata in `references.bib`.** PASS. All 14 entries independently
cross-checked against `citation_ledger.csv` (rice1976→B1-01, smithmiles2009→B2-01,
barbudo2023→B2-02, idreoskraska2019→B7-01, chow1970→B4-01, elyaniv2010→B4-02, hendrickx2024→B4-05,
mozannarsontag2020→B5-02, jorgensenigel2021→B8-01, frugalgpt2023→B3-02) and
`ads_metric_prior_art.csv`/`llm_advisory_prior_art.csv` (manning2008→G1-01, amigo2009→G1-02,
dawidskene1979→G1-04, rankgpt2023→G2-01) — every author/title/year/venue/DOI field matches its
ledger row. `dawidskene1979`'s volume/number/pages/DOI correctly remain `TODO` (the ledger itself
has no DOI, per row G1-04's own note). `rankgpt2023`'s author field now exactly mirrors the ledger's
abbreviated form (see §1, Fix #3).

**j. Citation key resolution.** PASS. Extracted all `\citep{}` keys from `main.tex` (14 unique) and
all `@`-entries from `references.bib` (14 unique) — identical sets, confirmed by set difference in
both directions (empty both ways). No undefined citation, no orphaned bib entry. `\nocite{*}` is
present, forcing the full set to render.

**k. Unresolved bibliographic fields remain TODO.** PASS — see (i).

**l. Frozen Experiment 1 evidence untouched.** PASS. `git diff 6fb6188 HEAD --
data/outputs/experiments/exp1/final/` is empty.

**m. No Phase A–D artifact or `TECHNICAL_REPORT.md`/`README.md`/`METHODOLOGY.md` modified.** PASS.
`git diff --stat HEAD -- research/ TECHNICAL_REPORT.md README.md METHODOLOGY.md scripts/ data/` is
empty (all changes in this pass are new untracked files, not modifications to any tracked file).

**n. No figures created anywhere.** PASS. `git status --porcelain -uall` shows no new image files
of any kind (checked for `.png/.jpg/.jpeg/.svg/.pdf/.gif`).

**o. No real tables/figures in `main.tex`.** PASS. Zero occurrences of `\includegraphics`,
`\begin{table}`, or `\begin{tabular}` — every figure/table reference is a `%`-comment placeholder.

**p. Secrets/credentials/paths/CUI scan.** PASS. Grepped `main.tex` and `references.bib` for
API-key/secret/password/bearer/AWS/private-key/Windows-path/Unix-home-path/CUI patterns — zero
hits.

**q. Skeleton reads as a skeleton, not finished prose.** PASS. Every subsection body in `main.tex`
is a structured `draftnote` block (PURPOSE/QUESTION/ALLOWED EVIDENCE/KEY POINTS/MUST NOT SAY), not
narrative prose; the Abstract, Title, Author, and Date are all explicit `TODO` placeholders. No
subsection anywhere presents draftnote content as if it were finished scientific writing.

**Structural/compilability substitute** (pdflatex unavailable in this environment, same limitation
noted in the prior audit): `\begin`/`\end` counts balance exactly (`draftnote` 71/71, `itemize`
61/61, `equation` 2/2, `abstract`/`document`/`cases`/`enumerate`/`quote` 1/1 each — one more
draftnote/itemize pair than the prior audit's 70/70 and 60/60, consistent with the one new
Discussion subsection added). Global brace count: 525/525, balanced (up from the prior audit's
518/518, again consistent with the added subsection). This is a gross-count substitute, not an
actual TeX parse, and cannot rule out a mis-nested (vs. mis-counted) pair — same caveat as the prior
audit.

---

## 4. Test suite (item 4)

Ran all five Experiment 1 harness test files directly (`python <file>`), not trusted from a prior
report:

| File | Result |
|---|---|
| `test_generator_rng.py` | 4/4 passed |
| `test_leakage.py` | 2/2 passed |
| `test_mechanisms.py` | 5/5 passed |
| `test_lexical_transform.py` | 8/8 passed |
| `test_stats.py` | 11/11 passed |

**30/30 self-checks passed, 0 failed.** (The "37 tests, 8 files" figure cited inside `main.tex`
§5.1's draftnote is itself explicitly annotated in the same sentence as "now 5 test files per the
current committed tree" — the file correctly flags its own historical/current-count distinction,
not a discrepancy this audit needs to resolve further.)

---

## 5. Git state (item 5)

`git status --porcelain -uall` at the time of this audit:

```
?? manuscript/main.tex
?? manuscript/references.bib
?? research/E0_CHECKPOINT_AUDIT.md
?? research/MANUSCRIPT_ARCHITECTURE.md
?? research/MANUSCRIPT_ARCHITECTURE_AUDIT.md
?? research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md
?? research/MANUSCRIPT_FORMAT_RESEARCH.md
?? research/MANUSCRIPT_SKELETON_AUDIT.md
?? research/PHASE_E_AUDIT_REPORT.md
?? research/PHASE_E_PLAN.md
?? research/PUBLIC_RELEASE_BOUNDARY.md
```

CONFIRMED: all `??` (untracked), nothing staged (no `A ` entries), `manuscript/main.tex`,
`manuscript/references.bib`, and `research/MANUSCRIPT_SKELETON_AUDIT.md` are present alongside the
pre-existing untracked Phase-E planning docs, exactly as expected before this checkpoint's `git add`
is run.

---

## 6. Findings

| # | Finding | Tag | Location |
|---|---|---|---|
| 1 | `research/MANUSCRIPT_SKELETON_AUDIT.md` lacks the short "Resolution note (added after this audit ran)" blockquote that `research/PAPER_CONTRACT_AUDIT_REPORT.md` uses as this project's established convention for a CONDITIONAL verdict whose REQUIRED NOW finding was subsequently fixed. The underlying fix is independently confirmed present in the current `main.tex` (§1/§3a above), so this is a documentation-legibility gap for future readers of the historical record, not a substance problem. | OPTIONAL FUTURE WORK | `research/MANUSCRIPT_SKELETON_AUDIT.md` (whole file — no resolution note present) |
| 2 | No new findings beyond what the prior `MANUSCRIPT_SKELETON_AUDIT.md` pass already surfaced and this pass confirms fixed. | — | — |

No REQUIRED NOW finding survived this pass. No BLOCK-level issue found: no forbidden claim
asserted, no frozen evidence touched, no fabricated citation, no unsupported number, no scope
expansion, no secret/credential/path leak, git hygiene clean, test suite green.

---

## 7. Required fixes before staging

None. Finding #1 is optional and does not need to be resolved before this checkpoint is staged —
it is a nicety for the historical record, not a gate on the checkpoint's actual content, which this
audit has independently re-verified end to end.

---

## 8. Verdict

## 🟢 PASS_WITH_NOTES

All three items reported as fixed after the prior `MANUSCRIPT_SKELETON_AUDIT.md` CONDITIONAL
verdict are independently confirmed present and correct by direct re-read of the current
`manuscript/main.tex` and `manuscript/references.bib` — not taken on the prior report's or the
implementing pass's word. The new Discussion subsection matches `MANUSCRIPT_ARCHITECTURE.md` §6's
required framing verbatim in spirit, including its explicit citation of the previously-missing
evidence sources. The full independent checklist (items a–q) passes on every dimension checked,
including forbidden-phrase compliance, the 6a/6b separation, H1's PARTIALLY_SUPPORTED framing, zero
production data inside Results, ten independently re-verified numbers (twice the required
five), all 14 bibliography entries cross-checked against the literature ledger with no fabricated
field, exact citation-key/bib-entry correspondence, and clean git hygiene (frozen Experiment 1
evidence untouched, no tracked file modified, no new figures, no secrets/paths/credentials, nothing
staged yet). All five Experiment 1 harness test files pass in full (30/30 self-checks).

The verdict is PASS_WITH_NOTES rather than a bare PASS solely because of Finding #1: the historical
audit file being carried into this checkpoint (`MANUSCRIPT_SKELETON_AUDIT.md`) does not carry the
short resolution-note blockquote this project's own prior practice
(`PAPER_CONTRACT_AUDIT_REPORT.md`) uses to mark a CONDITIONAL verdict's REQUIRED NOW finding as
subsequently resolved. This is optional, non-blocking, and does not require another audit pass to
fix — a short blockquote in the same style, added before or shortly after staging, is sufficient.
Safe to stage the checkpoint as specified (exactly `manuscript/main.tex`, `manuscript/references.bib`,
`research/MANUSCRIPT_SKELETON_AUDIT.md`) as-is.

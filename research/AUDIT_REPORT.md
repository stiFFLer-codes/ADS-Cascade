# Audit Report — Phase D.1 Post-hoc Analysis of Experiment 1

> Independent audit. First real audit run of this auditor role. Adversarial re-derivation performed
> against the frozen raw CSV, not trust of the new prose's own numbers.

## 1. Repository state

- Branch: `main`. HEAD: `6fb6188` — "Phase D: freeze Experiment 1 evidence" (this is the parent
  commit the brief names as the frozen checkpoint; no commit has been made on top of it).
- Working tree: dirty with **only untracked additions**, no modifications to any tracked file.
  `git diff --stat` (tracked-file diff) is empty.
- `git diff 6fb618838e47c84234dfad85c89b979e96b6c897 -- data/outputs/experiments/exp1/final/` is
  **empty** — the frozen evidence directory is byte-identical to the frozen commit. Confirmed.
- Diffed: working tree vs. HEAD (`git status --porcelain`), frozen dir vs. freeze commit, and the
  new files' content against `EVIDENCE_BASELINE.md`, `RESEARCH_GPS.md`'s prior state (implicit,
  since the file didn't exist before), `contribution_status.md`, `contribution_stress_test.md`,
  and the raw `final_condition_results.csv`.

## 2. Current research GPS

`research/RESEARCH_GPS.md` (new file, first version) states: North star = defensible manuscript
draft → reproducibility package → arXiv preprint. **CURRENT LOCATION** = Phase D.1 complete.
**CURRENT GATE** = Gate 4 (Contribution Lock) — described correctly as requiring a *human* decision
to adopt the surviving claim, not further analysis. **NEXT GATE** = Gate 5 (Manuscript, Phase E).
Scorecard shows Gates 1-3 fully checked, Gate 4 checkboxes open (correctly, since Gate 4 requires
human sign-off which hasn't happened), Gates 5-6 open. This matches ROADMAP.md's Phase D → Phase E
sequencing. DO NOT CHASE list correctly enumerates: no new experiments, no further novelty search,
no vendor/model experimentation, no manuscript polish pre-lock, the lexical-aware-R3-variant
explicitly deferred to future work, and thresholds/δ/cutoff explicitly frozen. Nothing in the list
looks stale relative to what Phase D.1 actually produced.

## 3. Changed files (all untracked, nothing modified)

- **Docs (new):** `research/EXPERIMENT_1_DATA_DICTIONARY.md`, `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`,
  `research/RESEARCH_GPS.md`
- **Code (new):** `scripts/experiments/exp1/analyze_posthoc.py`
- **Experimental artifacts (new, derived-only):** `data/outputs/experiments/exp1/posthoc/posthoc_analysis_report.json`,
  `data/outputs/experiments/exp1/posthoc/posthoc_rows_with_bands.csv`
- **Manuscript:** none touched (`README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md` all absent
  from `git status`).
- **Frozen evidence:** none touched (`data/outputs/experiments/exp1/final/` diff vs. freeze commit
  is empty).
- This exactly matches the expected D.1 file set named in the audit brief — no extra, no missing
  files. `.claude/` (auditor infra) is correctly gitignored and does not appear in `git status`
  (confirmed via `git check-ignore -v`). `.pytest_cache/` appearing as ignored is a byproduct of
  this audit's own test run, harmless and gitignored.

## 4. Research integrity

All headline numbers independently re-derived from the raw 240-row
`final_condition_results.csv`, using a fresh script written for this audit (not
`analyze_posthoc.py`'s own logic, not its `--demo` output trusted blindly) plus a third
cross-check against the pre-existing, frozen `final_summary.csv` (12-row pre-aggregation,
untouched by D.1):

| Claim | Independently recomputed | Match |
|---|---|---|
| Overall agreement 32/50 = 64.0% | 32/50 = 0.6400 | Exact |
| Wilson 95% CI [50.14%, 75.86%] | [50.14%, 75.86%] (own Wilson implementation) | Exact |
| Binomial p = 0.0649 | 0.0649 (own exact-binomial implementation) | Exact |
| 0.70–0.90 realized-ADS band: 100% (32/32) agreement | 32 agree / 0 disagree / 32 n | Exact |
| ≥0.90 realized-ADS band: 0/18 agreement (sharper than nominal-target 10%) | 0 agree / 18 disagree / 18 n | Exact |
| VARIED: `empirical_winner=="retrieval"` in 120/120, zero exceptions | 120/120, `[]` exceptions | Exact |
| CLEAN: `empirical_winner=="tie"` in 120/120, zero exceptions | 120/120, `[]` exceptions | Exact |
| r(ADS,rules_acc) CLEAN≈0.96 / VARIED≈0.91 | 0.9592 / 0.9091 | Matches to stated precision |
| r(ADS,retrieval_acc) CLEAN≈0.95 / VARIED≈0.95 | 0.9549 / 0.9476 | Matches to stated precision |
| r(lexical, rules−retrieval) pooled ≈ −0.97 | −0.9746 | Matches |
| r(realized ADS, rules−retrieval) CLEAN=+0.230 / VARIED=−0.803 | +0.2300 / −0.8028 | Matches |
| Nominal-target 100%/10% split traces to `EXPERIMENT_1_FINAL_RESULTS.md` | Confirmed: target=0.50/0.75 → 100% (30/30); target=1.00 → 10% (2/20) | Exact |

The "sharper 100%/0% realized-band split supersedes the 100%/10% nominal-target split" claim
is arithmetically consistent: the 3rd-source cross-check (`final_summary.csv`, untouched, frozen)
shows target=1.00/VARIED has n_agree=2/n_disagree=18 (the "10%"), and target=0.50/VARIED has
n_agree=10/n_na=10 (10 of 20 seeds excluded as `llm_required`). The realized-ADS-band regrouping
moves exactly the 2 target=1.00 seeds whose *realized* ADS falls under 0.90 into the 0.70–0.90
band (making it 30+2=32) and leaves 18 in the ≥0.90 band, all disagreeing (0%). 32+18=50,
matching the overall headline. No arithmetic slippage found anywhere in this chain.

**Superseded-value check:** grepped both new prose files for `55,394`/`55394`, `0.7756`,
`0.9746` (the *cross-company* superseded figure — not to be confused with the *unrelated*
Pearson r=−0.9746 computed fresh in this D.1 pass, which is a different quantity that happens to
share digits; verified it is not being used as the superseded cross-company number), `0.7454`,
`96.4%`, `84.12`, `0.8094`, `0.9310`. **Zero matches in either file.** No superseded number was
reintroduced.

**No production/synthetic conflation, no ADS-novelty claim, no "enterprise AI" generalization**:
confirmed by direct read of `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §13 ("Claims we must NOT make"),
which explicitly and correctly disclaims all of: ADS-as-novel-contribution, generalization beyond
the tested setting (naming "enterprise AI" explicitly as out of scope), production-confirms-this
framing, and CLEAN-implies-general-equivalence. Grepped for "novel" and "enterprise AI" across the
whole file — the only hits are inside this disclaimer list, correctly negated ("is a novel
contribution — already settled as out of scope").

**H1 verdict:** the pre-existing, frozen `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §9 states
`PARTIALLY_SUPPORTED` (unmodified — this file is part of the frozen commit, not touched by D.1).
The new `EXPERIMENT_1_POSTHOC_ANALYSIS.md` does not itself repeat an explicit "H1 = X" verdict
line, but nowhere claims or implies `SUPPORTED`; its own §12 minimum-defensible-claim and §13
prohibited-claims list are consistent with, not a strengthening of, PARTIALLY_SUPPORTED. No
upgrade occurred. (Minor observation, not a finding — see §11.)

**"No further experiment needed" (§14):** this is not asserted for convenience. It rests on a
traced, deterministic, seed-by-seed mechanism (§8-11 of the new doc): `realized_det_pct` is
computed train-only, grouped by the stable `product_code`, which the Data Dictionary (§"What
realized ADS is, precisely") and direct inspection of `final_summary.csv` both confirm makes it
byte-identical between CLEAN/VARIED at every target — a structural, not statistical, invariance.
Combined with the exceptionless 120/120 winner-constancy, the explanation is falsifiable-in-
principle (a single counter-example row would have broken it) and was checked exhaustively against
all 240 rows, not sampled. This reasoning is shown, not merely claimed.

## 5. Scientific consistency

Traced RQ → H1 → Experiment 1 design → frozen results → D.1 interpretation → contribution
implications. No break found in the chain. The D.1 document is explicit and correct that it
narrows rather than strengthens the finding: "ADS predicts task difficulty, not mechanism ranking"
is a *more* conservative claim than the pre-Experiment-1 assumption ("higher ADS → rules is
better"), and §13 explicitly lists that exact assumption as a claim that must NOT be made — this
is the correct posture per the known-rejected-claims list in this auditor's brief (the "R3 selects
the right mechanism" claim is not resurrected; it is explicitly and correctly refuted). No A5/A6-
shaped drift (script behavior vs. documented behavior) was found: `analyze_posthoc.py`'s R3
threshold constants (0.90/0.70) are the literal same values imported/hardcoded identically in
`stats.py` (checked side-by-side, §3 below), and the δ=0.02 and cutoff=75 values are read from the
CSV columns (`retrieval_cutoff_used`), not re-derived or re-asserted independently.

## 6. Evidence/claim traceability

Every quantitative claim checked in §4 traces to `final_condition_results.csv` directly (240 raw
rows) and/or `final_summary.csv` (frozen 12-row pre-aggregation) — both under
`data/outputs/experiments/exp1/final/`, confirmed byte-identical to the freeze commit. No claim
was found tracing only to another document's prose restating it once removed. The one place the
document itself flags its own number as *not* independently new (§4: "Exact match to
`EXPERIMENT_1_FINAL_RESULTS.md` §5... not stopping") was independently re-verified by this audit
rather than taken on faith, and matched.

## 7. Code review — `scripts/experiments/exp1/analyze_posthoc.py`

- **Reads only** `data/outputs/experiments/exp1/final/final_condition_results.csv`; **writes
  only** under `data/outputs/experiments/exp1/posthoc/`. Confirmed by direct inspection of the
  `FINAL_CSV`/`OUT` path constants and the two `open(..., "w")` calls — both under `OUT`. No write
  path touches `.../exp1/final/`.
- **No new data generation**: no import of, or call into, any generator module (`gen`,
  `00_generate_synthetic`, etc.) — imports are `csv, json, math, statistics, pathlib` only
  (stdlib-only, confirmed by grep, no new dependency).
- **Thresholds not re-derived**: `R3_RULES_THRESHOLD=0.90`, `R3_RETRIEVAL_THRESHOLD=0.70` are
  literal copies of `stats.py`'s constants (same values, comment says "reused unchanged, never
  re-derived here" in both files). `PRACTICAL_EQUIVALENCE_DELTA`/`RETRIEVAL_CUTOFF` are not
  redefined at all — the script only reads the already-computed `retrieval_cutoff_used` /
  `empirical_winner` columns from the frozen CSV; it does not recompute the winner rule.
- **Blank-string parsing**: `r3_agrees_with_empirical` parses `""` → `None`, `"True"` → `True`,
  `"False"` → `False` (line 49-51) — correct three-way handling, verified by re-deriving the same
  agree/disagree/blank counts independently (32/18/190) and cross-checking they sum to 240.
- **Banding logic**: `ads_band()` is a mechanical function of the same two constants R3 itself
  uses (`>=0.90`, `>=0.70`, else `<0.70`) — not a post-hoc-chosen cut. Confirmed no other banding
  candidates appear anywhere in the script or its output.
- **Math implementations**: Wilson-CI and exact two-sided binomial-p implementations were checked
  against independently-written versions of the same standard formulas (own script, different
  variable names/loop order) — results matched to the reported precision in every case tested.
  Pearson/Spearman are standard-formula stdlib implementations (Spearman uses average-rank tie
  handling); re-derived two Pearson values independently and both matched.
- **Determinism**: no RNG use anywhere in this script (pure aggregation of already-computed
  columns) — determinism is trivially guaranteed.
- **Edge cases**: `agreement_block()` returns `agreement_rate: None` when `n_defined==0` (avoids
  div-by-zero; exercised in practice by the CLEAN slice, which has 0 defined comparisons).
- **`--demo` self-check**: ran `python scripts/experiments/exp1/analyze_posthoc.py --demo` —
  passed: `demo() OK: 32/50 agreement, Wilson CI, and binomial p all reproduce from the frozen
  CSV.` Sufficient test coverage for a read-only analysis script per the brief's own standard.

No correctness issues found in this script.

## 8. Experimental integrity

Not a new experiment — this is a post-hoc analysis of an already-frozen run, so most of dimension
5 (seed manifests, condition counts, train/test separation, no selective reruns) was already
locked at the prior freeze commit and is out of scope for re-verification here *except* to confirm
nothing in this pass altered it. Confirmed: `data/outputs/experiments/exp1/final/` is byte-
identical to the freeze commit (§1); the new posthoc CSV/JSON are pure derived recombinations of
already-frozen columns (no new synthetic generation, §7); write-timestamp check on the two new
posthoc output files shows both at `Aug 12 11:05` (same single run, one timestamp cluster — no
signs of a manually-edited row or partial rerun). Statistical definitions (paired bootstrap δ=0.02
winner rule, whole-set-accuracy-with-abstentions-as-incorrect) are read from the frozen CSV's
columns, not recomputed with a different definition anywhere in the new code.

## 9. Scope/GPS alignment — PASS

Phase D.1 is exactly the currently-open work item per `RESEARCH_GPS.md`'s own "CURRENT LOCATION."
It advances directly toward Gate 4 (Contribution Lock) by producing the evidence a human needs to
adopt or reject the surviving claim — it does not itself lock the contribution (correctly left as
`⬜` in the scorecard, a human decision). No new experimentation was run (confirmed: frozen dir
untouched). The one item flagged as a legitimate future-work idea (lexical-noise-aware R3 variant)
is explicitly *not* built, consistent with the DO NOT CHASE list, and is correctly deferred to a
future-work paragraph (§15) rather than acted on. No detour, no unrequested scope expansion found.

## 10. Git hygiene

- `git status --short`: 5 untracked entries, exactly the expected D.1 set (§3). No unexpected
  files.
- No secrets/API keys/credentials/bearer tokens/private-key material found (grepped all 6 new/
  changed files).
- No client/production data or real-company names found in the new files (all content is derived
  from the already-public-scoped synthetic Experiment 1 CSV).
- No local Windows paths or usernames found in the new files (grepped for `C:\Users\` and the
  account name; zero hits).
- No `.bak`/`.swp`/`.orig`/`.tmp` files present.
- `README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md` — none modified.
- No file under `data/outputs/experiments/exp1/final/` or any other frozen path modified.
- `.claude/agents/research-code-auditor.md` is correctly gitignored, not tracked, does not appear
  as a change to stage.
- A safe `git add` for a checkpoint would be exactly: `research/EXPERIMENT_1_DATA_DICTIONARY.md`,
  `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `research/RESEARCH_GPS.md`,
  `scripts/experiments/exp1/analyze_posthoc.py`, `data/outputs/experiments/exp1/posthoc/` (both
  files). Nothing else. (`.pytest_cache/` created incidentally by this audit's own test run is
  gitignored and should not be staged; it is not part of D.1's output.)

## 11. Findings

1. **OPTIONAL FUTURE WORK** — `EXPERIMENT_1_POSTHOC_ANALYSIS.md` never restates an explicit
   "H1 verdict: PARTIALLY_SUPPORTED" line of its own; it relies on the reader cross-referencing
   `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §9 (frozen, unmodified, correctly says
   `PARTIALLY_SUPPORTED`). No incorrect claim is made anywhere in the new document, so this is not
   a defect — but adding one explicit confirming sentence ("this analysis does not change the
   Evidence Checkpoint's H1 verdict of PARTIALLY_SUPPORTED") would make the non-upgrade
   unambiguous to a future reader who doesn't cross-reference both files. File:
   `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md` (no specific line — an absence, not an error).
2. **OPTIONAL FUTURE WORK** — `STATE.md` (line 6, `Last updated: 2026-08-10`) predates Experiment 1
   and Phase D.1 entirely and does not mention either. This staleness pre-dates this pass (it was
   already stale before D.1 started) and is not something D.1 was responsible for updating, but it
   will need a pass before Phase E starts, since STATE.md is the documented first-read entry point.
   File: `STATE.md:6`.

No REQUIRED NOW findings.

## 12. Required fixes

None. (Empty — no CONDITIONAL or BLOCK-level issues found.)

## 13. Verdict

## 🟢 PASS

Every headline quantitative claim in the new Phase D.1 files was independently re-derived from the
raw, frozen 240-row CSV using code written fresh for this audit (not the builder's own
`analyze_posthoc.py` logic trusted blindly), cross-checked a second time against the separate,
untouched `final_summary.csv`, and matched exactly in every case tested — including the two most
load-bearing and easiest-to-get-wrong claims (the exceptionless 120/120 VARIED-retrieval /
120/120 CLEAN-tie split, and the Pearson correlations underpinning the "predicts difficulty, not
ranking" distinction). No superseded number was reintroduced, no rejected claim (ADS-as-novel,
"higher ADS means rules is better," enterprise-AI generalization) was resurrected, and the H1
verdict was not silently upgraded. The frozen evidence directory is byte-identical to the freeze
commit, the analysis script is read-only against frozen data and stdlib-only, its threshold
constants are literal unmodified copies of the frozen `stats.py` values, and all 30 existing exp1
unit tests plus the script's own `--demo` self-check pass. Git hygiene is clean: exactly the
expected file set is untracked, nothing frozen or manuscript-level was touched, and no secrets,
client data, or local-path leakage was found. The two findings recorded above are both optional,
non-blocking documentation-polish notes, not integrity or correctness issues. Safe to checkpoint
as-is.

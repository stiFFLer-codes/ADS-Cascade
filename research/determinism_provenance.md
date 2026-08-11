# Provenance Investigation — Determinism value conflict (0.7756/0.9746 vs 0.763/0.931)

> Follow-up to Research Audit finding A3. This investigation **executed** the public pipeline
> (`scripts/03_5_dataset_intelligence.py`, `scripts/04_architecture_decision.py`) to determine
> whether the conflicting numbers are current or stale, and wrote one small, standalone, read-only
> verification script (not part of the pipeline, not committed to the repo) to quantify a deeper
> issue this investigation uncovered. No pipeline source file was modified. The one file this
> investigation regenerated (`reports/architecture_decision.md`, which embeds a run timestamp)
> was restored to its committed state afterward via `git checkout --`; a byproduct `data/logs/`
> directory created by running the scripts was deleted. `git status` was
> clean before and after this investigation except for changes already present at its start
> (`STATE.md` modified, `ROADMAP.md`/`research/` untracked).

## The four numbers

| Label (as it appears) | Value | File |
|---|---|---|
| "Global Cross-Company Determinism" | 0.7756 | `data/outputs/intelligence/dataset_intelligence_report.md` |
| "Average Company Determinism" | 0.9746 | `data/outputs/intelligence/dataset_intelligence_report.md` |
| "cross_company_consistency" (R1 row) | 0.7632 | `data/outputs/intelligence/decision_matrix.csv`; `reports/architecture_decision.md` |
| "Dataset ADS (unweighted)" | 0.9310 | `reports/architecture_decision.md`; cited in `TECHNICAL_REPORT.md` §3.2 as "0.931" |

All four are synthetic-branch numbers (60 companies, `random.seed(42)`). This document does not
and cannot check the equivalent production-side conflict (0.7454 vs 0.695) already flagged inside
`data_verification_audit.md`, because the production `dataset_intelligence_report.md` this would
require is confidential and not in this repository — see "Production implications" below for what
can and can't be inferred from the synthetic findings.

## Step 1 — Trace each number to its exact generating code

Both pairs are produced by **the same script**, `scripts/03_5_dataset_intelligence.py`, inside one
function, `module_c_behavioral()` — but through two different downstream consumers of that
function's output:

**Path 1 — `dataset_intelligence_report.md` (0.7756 / 0.9746):** written directly by
`generate_report()` in `03_5_dataset_intelligence.py` (lines 430-458), from the dict returned by
`module_c_behavioral()`:

```python
# lines 349-353 — "Global Cross-Company Determinism"
cross_comp_det_sum += det * total     # det = per-product cross-co determinism; total = product's occurrence count
cross_comp_total += total
global_cross_det = cross_comp_det_sum / cross_comp_total   # ⇐ OCCURRENCE-weighted mean over multi-company products

# lines 373-374 — "Average Company Determinism"
"company_avg_det": statistics.mean([r["avg_determinism"] for r in c2_rows])  # ⇐ simple mean of each COMPANY's own occurrence-weighted avg determinism, one vote per company
```

**Path 2 — `decision_matrix.csv` / `reports/architecture_decision.md` (0.7632 / 0.9310):** written
by `scripts/04_architecture_decision.py`, which re-reads `03_5`'s *per-product* CSV outputs
(`product_ambiguity.csv`, `cross_company_consistency.csv`) — not the `dataset_intelligence_report.md`
prose — and recomputes its own aggregates:

```python
# compute_cross_company_score() — "cross_company_consistency"
multi = [r for r in cross_co if n_companies >= 2]
return sum(r["cross_company_determinism"] for r in multi) / len(multi)   # ⇐ simple (unweighted) mean, one vote per PRODUCT

# compute_dataset_ads() — "Dataset ADS (unweighted)"
unweighted = det_sum / len(products) if products else 0.0   # ⇐ simple mean of per-product determinism_score, one vote per PRODUCT
```

**This alone explains most of the gap: these are two different, legitimate aggregation choices —
occurrence-weighted vs. simple-mean, and company-level-vote vs. product-level-vote — computed from
overlapping but not identical inputs, not a stale-vs-fresh problem.** This mirrors the
weighted-vs-unweighted ADS distinction `TECHNICAL_REPORT.md` §2.2 already discusses openly for the
*production* ADS pair (0.847 vs 0.964) — except nobody has written the equivalent explanation for
*these* two pairs, and the two pairs' names ("Global Cross-Company Determinism" vs "cross-company
consistency"; "Average Company Determinism" vs "unweighted ADS") are similar enough to be
mistaken for the same metric.

## Step 2 — Is either report stale?

Executed both scripts against the currently-committed input data (`invoice_lines_all_companies.csv`,
`product_account_mapping.csv` — neither was regenerated; only the two intelligence-layer scripts
ran):

```
$ python scripts/03_5_dataset_intelligence.py
...Loaded 1234 product mappings. Processed 7523 rows... Script 3.5 finished successfully.

$ python scripts/04_architecture_decision.py
...Dataset ADS: weighted=0.8094, unweighted=0.9310
...Cross-company consistency score: 0.7632
...R3 Complexity: EMBEDDING_PRIMARY
```

`git diff` after both runs showed **zero content changes** to
`data/outputs/intelligence/dataset_intelligence_report.md` and to
`data/outputs/intelligence/decision_matrix.csv` — both are byte-identical to what's already
committed. The only diff anywhere was a one-line run-timestamp in `reports/architecture_decision.md`
("Generated: ..."), which was reverted. **Conclusion: neither 0.7756/0.9746 nor 0.7632/0.9310 is
stale. Both are the live, current, fully-reproducible output of the current script version on the
current committed data.** This rules out "one report is stale" as the explanation the audit task
anticipated — the real explanation is the aggregation-formula difference in Step 1, plus a deeper
issue found in Step 3.

## Step 3 — A deeper finding: `product_ambiguity.csv`'s per-product "dominant account" does not merge same-account rows before comparing

While tracing Path 2's inputs, `product_ambiguity.csv`'s C.1 computation (lines 259-267 of
`03_5_dataset_intelligence.py`) was compared line-by-line against C.3's cross-company computation
(lines 332-339), because both nominally answer the same question — "which account does this
product mainly go to, and how dominant is it?" — from the same underlying per-(company, product,
account) rows in `product_account_mapping.csv`.

**C.3 (`cross_company_consistency.csv`, correct):**
```python
prod_global_accs[prod][account_id] += count      # sums counts PER ACCOUNT across all contributing rows
...
dom_c = accs.most_common(1)[0][1]                  # dominant = largest ACCOUNT TOTAL
```

**C.1 (`product_ambiguity.csv`, the file that feeds ADS and R3):**
```python
acc_list.sort(key=lambda x: x[1], reverse=True)    # sorts the RAW ROWS, never merged by account_id
dominant_account = acc_list[0][0]
dominant_count = acc_list[0][1]                     # dominant = largest SINGLE ROW, not largest account total
```

**Concrete, reproducible example** — product `synth office 00073`, from the raw mapping rows in
`data/outputs/product_account_mapping.csv`:

| Company | Account | Count |
|---|---|---|
| SYNTH COMPANY 016 SRL | 608 | 12 |
| SYNTH COMPANY 032 SRL | 625 | 21 |
| SYNTH COMPANY 043 SRL | 605 | 25 |
| SYNTH COMPANY 055 SRL | 371 | 10 |
| SYNTH COMPANY 056 SRL | 371 | 18 |

Total occurrences = 86. Summed by account: 605→25, 625→21, 608→12, **371→28** (10+18, two
companies). The true dominant account is **371 at 28/86 = 32.56%** — and `cross_company_consistency.csv`
reports exactly this (`0.3256`, dominant `371`). But `product_ambiguity.csv` reports dominant
account **605** (the single largest *row*, 25/86 = **0.2907**) — a different account entirely, and
a lower, wrong determinism score, because it never noticed that account 371's two rows sum to more
than account 605's one row.

**This was quantified across the whole synthetic dataset** with a standalone, read-only script
(not committed to the repository; reads only the already-public `product_account_mapping.csv`):

| Metric | As currently coded (`product_ambiguity.csv`) | If dominant account were correctly summed per account first |
|---|---|---|
| Products affected | — | 74 of 844 (8.8%) have a different determinism score; 6 of those 74 even have a different *dominant account* |
| Unweighted ADS (mean determinism_score) | **0.9310** (matches committed value exactly) | 0.9597 |
| Weighted ADS (occurrence-weighted) | **0.8094** (matches committed value exactly) | 0.9031 |
| Products with determinism > 0.95 (R3's population) | **710 / 844 = 84.12%** (matches committed value exactly) | 739 / 844 = 87.56% |

The verification script's own before-values reproduce the committed 0.9310/0.8094/84.12% exactly,
confirming it faithfully re-implements the current code's logic (not a different formula being
mistaken for a bug). The three affected products shown below illustrate the failure mode most
starkly — each is booked to **one single account by every company that uses it**, i.e. true
determinism = 1.0, but the current code reports them as highly ambiguous because it never merges
duplicate-account rows before picking a "dominant" one:

- `synth maintenance 00545`: 4 companies, **all 4 map to account 609** (rows: 609:1, 609:1, 609:1,
  609:1) → current code reports determinism **0.25**, `n_accounts=4`; true value is **1.0**,
  1 account.
- `synth fuel 00738`: 5 rows, all account 612 → current code reports **0.2963**; true value **1.0**.
- `synth office 01029`: 3 rows, all account 601 → current code reports **0.3333**; true value
  **1.0**.

This is a second bug in the same code path: `n_accounts` (`len(acc_list)`) counts raw *rows*, not
distinct account IDs, so it also over-reports how many accounts a product uses whenever several
companies independently agree on the same account (exactly the case the product-level `ADS`
formula is supposed to be measuring as maximally *deterministic*, not maximally ambiguous).

**Direction of the effect:** merging rows by account before taking the max can only *raise or
leave unchanged* each affected product's determinism score (the true per-account total is always
≥ the largest individual contributing row). The current code therefore systematically
*understates* determinism for every multi-company product — which are disproportionately the
higher-volume products (more companies → more total occurrences), which is why the effect on the
**weighted** ADS (0.8094 → 0.9031, a 0.094 shift) is roughly three times larger than its effect on
the **unweighted** ADS (0.9310 → 0.9597, a 0.029 shift).

## Step 4 — Does this change any of the paper's five architecture decisions?

Recomputed with the corrected (account-summed) determinism scores, on the synthetic dataset only:

- **R3 (model complexity):** 87.56% is still below the 90% `THRESHOLD_DETERMINISTIC_RULES` cutoff
  → **still EMBEDDING_PRIMARY.** The R3 flip discussed in `TECHNICAL_REPORT.md` §3.3 is **not** an
  artifact of this bug — it survives correction, though by a narrower margin (87.56% vs. 90%,
  instead of 84.12% vs. 90%).
- **R1 (retrieval strategy):** the GLOBAL_RETRIEVAL branch additionally requires cross-company
  consistency ≥ 0.85; `cross_company_consistency.csv`/`compute_cross_company_score()` is unaffected
  by this bug (it already sums by account correctly, see Step 1), so cross-co stays at 0.7632 <
  0.85 regardless of the ADS correction → **still HYBRID** either way.
- **R4, R5:** do not depend on `product_ambiguity.csv` at all → unaffected.

**No headline architecture decision changes.** What changes if this is fixed is the *reported
magnitude* of two numbers the paper treats as an important interpretive finding in their own
right: §2.2's "ADS divergence... a gap of 0.117... the products that occur most often are
disproportionately the ambiguous ones" argument would go from a synthetic-branch gap of
`0.9310 − 0.8094 = 0.1216` to a corrected gap of `0.9597 − 0.9031 = 0.0566` — roughly **half** the
current apparent divergence. This document does not know whether the same proportional effect
would hold on the production numbers (91.2%/0.847/0.964) — production has a smaller *share* of
multi-company products (2,696 / 47,306 = 5.7%) than the synthetic run (114 / 844 = 13.5%), which
argues for a smaller effect in absolute percentage-point terms — but production's known
determinism-vs-volume anti-correlation (the paper's own §2.2 narrative) argues the *direction* of
the effect (weighted ADS understated more than unweighted) would likely be the same. **This is
plausible reasoning, not a verified conclusion** — production data is confidential and cannot be
recomputed from this repository.

## Determination — which values are canonical for the current, public, executable pipeline

Per the audit task's instruction to let "the executable pipeline and canonical generated artifacts"
decide, not the paper: the pipeline's own reproducibility instructions
(`TECHNICAL_REPORT.md`'s Reproducibility section and `METHODOLOGY.md`) name exactly six scripts to
run, ending at `04_architecture_decision.py`, and cite numbers from its outputs
(`decision_matrix.csv` / `reports/architecture_decision.md`). `dataset_intelligence_report.md` is
not in that reproduction chain — it's an intermediate, human-readable artifact `03_5` also happens
to emit, consumed by nobody downstream in code (confirmed: `04_architecture_decision.py` reads
`product_ambiguity.csv` and the other Script-3.5 *CSVs* directly, never
`dataset_intelligence_report.md`'s prose).

- **Canonical, currently:** `cross_company_consistency = 0.7632` (≈0.763) and
  `unweighted_ads = 0.9310` (≈0.931) — these are what the designated reproduction chain produces,
  confirmed live-reproducible in Step 2, and what `TECHNICAL_REPORT.md`/`METHODOLOGY.md` already
  cite.
- **Not canonical, but not stale either:** `0.7756` and `0.9746` — correctly computed by the current
  code for the different aggregation they represent, but (a) not part of the reproduction chain the
  paper points readers to, and (b) inherit the Step 3 dominant-account bug in the "0.9746" case's
  upstream inputs to a greater degree than the canonical numbers do (both numbers are somewhat
  affected by the Step 3 bug, since both ultimately derive from the same unmerged per-row data —
  but "Average Company Determinism" is a company-vote average of a *within-company* computation
  that, per Step 3's scope, is not directly implicated by the cross-company row-merging issue in
  the same way `dataset_ads` is; this document did not separately re-derive a corrected value for
  it and does not claim one).
- **The Step 3 bug affects the canonical numbers too.** 0.7632 (cross-company consistency) is
  unaffected by it (C.3's logic is correct). But 0.9310 (unweighted ADS) and 0.8094 (weighted ADS,
  cited as 0.809) — both canonical, both currently cited in the paper — **are** affected, per Step
  3's quantification (true unweighted ≈0.9597, true weighted ≈0.9031 once same-account rows are
  merged before selecting the dominant account).

## Recommendation

1. **Do not silently replace any number.** This document does not change
   `dataset_intelligence_report.md`, `product_ambiguity.csv`, `decision_matrix.csv`, or any script.
2. **Annotate `dataset_intelligence_report.md`** with a one-line note (mirroring
   `data_verification_audit.md`'s existing NOTE for the production 0.7454-vs-0.695 case) explaining
   that "Global Cross-Company Determinism" and "Average Company Determinism" use different
   aggregation weightings than the "cross-company consistency" and "unweighted ADS" figures cited
   elsewhere in this repository, so a reader who opens this file isn't misled. This is a
   documentation-only change to a non-code file; it was **not** made in this pass because the task
   scope was investigation, not editing.
3. **Decide on the Step 3 bug.** This is the more consequential open item: `product_ambiguity.csv`'s
   dominant-account selection (in `module_c_behavioral()`'s C.1 block,
   `scripts/03_5_dataset_intelligence.py` lines ~259-267) should arguably sum counts by
   `account_id` before selecting the dominant account, exactly as its sibling C.3 block already
   does. Fixing it would change the *reported* weighted/unweighted ADS values (upward) on both the
   synthetic branch (verified: 0.8094→~0.9031 weighted, 0.9310→~0.9597 unweighted) and, very
   plausibly but unverifiably from here, the confidential production numbers the paper's headline
   figures (0.847/0.964) come from. **This was not fixed in this pass** — the audit task's
   constraints for A3 authorize regenerating a *stale* report, not altering the underlying
   computation, and this is a computation question, not a staleness question. See Question F-new
   in the updated `RESEARCH_AUDIT.md` and Question 3 in `EVIDENCE_BASELINE.md`'s caveats.
4. **No architecture decision needs to change** — R1/R3/R4/R5 are confirmed robust to this bug on
   the synthetic data (Step 4). This means the fix, if made, changes *reported precision*, not the
   paper's *conclusions* — which lowers the urgency, but the paper's own §2.2 "ADS divergence"
   interpretive claim leans on the exact magnitude of the weighted/unweighted gap, so it is not a
   cosmetic issue either.

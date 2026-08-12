# Experiment 1 — Data Dictionary

> Phase D.1 (post-hoc analysis). Documents every column of the FROZEN
> `data/outputs/experiments/exp1/final/final_condition_results.csv` (240 rows, 24 columns),
> traced to the actual code that produced it — `scripts/experiments/exp1/run_final.py`,
> `consistency.py`, `mechanisms.py`, `stats.py` — not to memory or prose in other reports.
> Nothing in `data/outputs/experiments/exp1/final/` was modified to produce this document.

## Unit of observation

One row = one **condition**: a unique `(seed, target_deterministic_share, lexical_variation)`
triple. 6 targets × 2 lexical conditions × 20 seeds = 240 rows. Within a condition, a fresh
synthetic dataset is generated (`gen.gen_dataset(seed=..., deterministic_share=target,
lexical_variation=lexical, p_transform=p_transform)`), split into train/test, and **both**
mechanisms (rules, retrieval) are evaluated on the same held-out test split — so `rules_*` and
`retrieval_*` columns in the same row are paired observations on identical test lines, not
independent samples (this is why the winner statistic in §Winner below uses a paired bootstrap,
not two independent CIs).

## Columns

| Column | Type | Meaning | Source |
|---|---|---|---|
| `status` | str | `"ok"` for all 240 rows (0 failures) | `run_final.py` try/except wrapper |
| `seed` | int | RNG seed, one of `{31001, ..., 31020}`, identical set for every condition | `run_final.py:45` |
| `target_deterministic_share` | float | The generator's **target** for the share of products that are near-deterministic (one of `{0.00, 0.20, 0.30, 0.50, 0.75, 1.00}`) — an input knob, not the measured outcome | `run_final.py:41`, passed to `gen.gen_dataset(deterministic_share=target)` |
| `lexical_variation` | bool | `False` = CLEAN (no surface-string noise), `True` = VARIED (`p_transform=0.3`) | `run_final.py:42-43` |
| `p_transform` | float | `0.3` if VARIED else `0.0` — probability the generator perturbs a product's surface string (`normalized_product`) at emission time | `run_final.py:92` |
| `realized_det_pct` | float | **The primary independent variable ("realized ADS").** Train-only: share of products (grouped by the stable `product_code`, not the perturbable surface string) whose per-product determinism score (dominant-account share of that product's occurrences) exceeds 0.95. This is what `EXPERIMENT_1_FINAL_RESULTS.md` calls "realized ADS" throughout §4-§9. | `consistency.py: compute_det_pct()["det_pct"]`, called via `realized_ads(lines)` which filters to `split_of(r)=="train"` before aggregating |
| `weighted_ads` | float | Diagnostic/secondary only — occurrence-weighted mean per-product determinism score (not thresholded at 0.95, not used by R3 or any decision) | `consistency.py: compute_det_pct()["weighted_ads"]` |
| `unweighted_ads` | float | Diagnostic/secondary only — unweighted mean per-product determinism score across products | `consistency.py: compute_det_pct()["unweighted_ads"]` |
| `cross_company_consistency` | float | Diagnostic only — for products bought by ≥2 companies, mean share of the cross-company-dominant account; never used by R3 or the winner rule | `consistency.py: compute_cross_company_consistency()` |
| `n_products_train` | int | Distinct `product_code` values with a non-empty `account_id` in the train split of this condition | `consistency.py: compute_det_pct()["n_products"]` |
| `n_train_lines` | int | Row count of the train split (train/test partition via `split_of(row, test_every=5)` — deterministic 4:1 split, not random) | `run_final.py:97` |
| `n_test_lines` | int | Row count of the test split (the held-out set both mechanisms are scored on) | `run_final.py:98` |
| `rules_whole_set_accuracy` | float | Whole-set accuracy of the **rules** mechanism on the test split: exact company-scoped lookup, then exact global lookup, else abstain. Abstentions count as incorrect (the pre-specified primary metric — no partial credit for "would have been right if it hadn't abstained") | `mechanisms.classify_rules` scored by `stats.whole_set_accuracy` |
| `rules_coverage` | float | Fraction of test lines where rules did **not** abstain (found an exact match). Always < 1.0 across all 240 conditions — rules abstains whenever no exact string match exists in the train-built KB | `stats.coverage(rules_preds)` |
| `retrieval_whole_set_accuracy` | float | Whole-set accuracy of the **retrieval** mechanism: rapidfuzz lexical-similarity match (company-scoped, then global), cutoff=75, run as the **primary** classifier on every test item (not a rules-miss fallback). Abstentions count as incorrect | `mechanisms.classify_retrieval` scored by `stats.whole_set_accuracy` |
| `retrieval_coverage` | float | Fraction of test lines where retrieval did not abstain. `1.0` in all 240 conditions — retrieval never abstains at cutoff=75 | `stats.coverage(retrieval_preds)` |
| `retrieval_cutoff_used` | int | `75` in all 240 rows — the single frozen fuzzy-match cutoff (Gate 2 calibration), never varied within this experiment | constant, `run_final.py:44` |
| `paired_diff_point` | float | Point estimate of `rules_accuracy − retrieval_accuracy` on the actual (non-resampled) test split | `stats.paired_bootstrap_diff_ci()["diff_point"]` |
| `paired_diff_ci_low` | float | Lower bound of the 95% **paired** bootstrap CI (2000 resamples, resampling test-line indices, scoring both mechanisms on the same resampled indices — preserves the pairing) on `rules − retrieval` | `stats.paired_bootstrap_diff_ci()` |
| `paired_diff_ci_high` | float | Upper bound of that same paired bootstrap CI | `stats.paired_bootstrap_diff_ci()` |
| `empirical_winner` | str | `"rules"` if the entire paired-diff CI lies above `+δ` (0.02); `"retrieval"` if entirely below `−δ`; otherwise `"tie"` — a difference smaller than the pre-registered practical-equivalence margin is not reported as a winner either way | `stats.paired_bootstrap_winner(delta=0.02)` |
| `r3_selected_mechanism` | str | The pre-existing, unmodified R3 rule applied to this row's `realized_det_pct`: `"rules"` if `≥0.90`, `"retrieval"` if `≥0.70` (and `<0.90`), else `"llm_required"` | `stats.r3_rule_selection(ads["det_pct"])` — thresholds are `stats.R3_RULES_THRESHOLD`/`R3_RETRIEVAL_THRESHOLD`, reused unchanged from `scripts/04_architecture_decision.py` |
| `r3_agrees_with_empirical` | bool / blank | `True`/`False` only when R3 selected a defined, non-excluded mechanism **and** the empirical winner is not a tie; **blank (`None`)** when `r3_selected_mechanism=="llm_required"` (R3 picked the mechanism excluded from this experiment — not comparable) **or** `empirical_winner=="tie"` (no discriminating empirical signal to agree or disagree with) | `run_final.py:128-131` |
| `elapsed_seconds` | float | Wall-clock time for this condition (harness bookkeeping only, not scientific data) | `run_final.py` |

## What "realized ADS" is, precisely

`realized_det_pct` is computed **only from the train split**, and grouped by `product_code` (the
generator's stable ground-truth product identity) rather than `normalized_product` (the surface
string that `lexical_variation`/`p_transform` perturbs). This is a deliberate, documented design
choice (`consistency.py:36-46`): grouping by the surface string would let the lexical-noise
transform fragment one true product into several near-unanimous, low-count surface variants,
artificially inflating `det_pct`. Grouping by `product_code` instead makes `realized_det_pct`
**invariant to the lexical condition** — confirmed directly in the data: `realized_ads_mean` /
`realized_ads_std` in `final_summary.csv` are byte-identical between the CLEAN and VARIED row for
every one of the 6 targets (e.g. target=0.75: `0.7973 ± 0.0105` in both). This invariance is the
mechanical reason ADS and lexical noise are, by construction, two separable axes in this
experiment — see `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §7-8 for what that separability implies about
whether ADS alone can select a mechanism.

## Derived quantities used in the post-hoc analysis (not columns in the frozen CSV)

Computed by `scripts/experiments/exp1/analyze_posthoc.py` from the columns above, written to
`data/outputs/experiments/exp1/posthoc/`:

- `rules_minus_retrieval` = `rules_whole_set_accuracy − retrieval_whole_set_accuracy` (per row)
- `ads_band` = `"<0.70"` / `"0.70-0.90"` / `"≥0.90"`, computed from **per-row** `realized_det_pct`
  against the same R3 thresholds — not from the nominal `target_deterministic_share`. These
  usually but do not always coincide: e.g. at `target=0.50`, individual seeds' realized ADS
  straddles the 0.70 boundary (range 0.659–0.727 across the 20 seeds), so 10/20 seeds land in each
  band even though they share one nominal target. See `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §10.

## Related frozen files (unmodified, read-only inputs to this analysis)

- `final_summary.csv` — pre-aggregated by `(target, lexical)`, 12 rows. Cross-checked, not
  superseded, by the per-row recomputation in this phase.
- `final_bootstrap_results.csv` — a `(seed, target, lexical)`-keyed projection of the bootstrap
  columns only.
- `final_conditions.csv` — the execution manifest (status, realized_det_pct, line counts) without
  the accuracy/winner columns.
- `final_run_metadata.json` — run-level provenance (240/240 succeeded, timing).
- `final_frozen_config.json` — the config block asserted at run start.

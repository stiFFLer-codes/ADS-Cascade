# R3 Threshold Implementation Analysis

> Follow-up to Research Audit finding A4. Read-only inspection of
> `scripts/04_architecture_decision.py`'s `decide_model_complexity()` function and its inputs.
> No implementation changes were made — no bug was found in R3's *decision logic* itself (the
> band structure is internally consistent and correctly implemented). A bug **was** found in
> R3's *input data* (`product_ambiguity.csv`'s determinism_score column) — that is documented in
> `determinism_provenance.md` (Step 3), not here, and is cross-referenced below.

## The metric R3 consumes

`decide_model_complexity(products)` in `scripts/04_architecture_decision.py` (lines 242-289) reads
`products = data["product_ambiguity"]`, i.e. every row of `product_ambiguity.csv` (one row per
normalized product, produced by `03_5_dataset_intelligence.py`'s Module C.1). For each product it
reads the `determinism_score` column and classifies:

```python
deterministic = sum(1 for p in products if determinism_score(p) > 0.95)
ambiguous     = sum(1 for p in products if determinism_score(p) < 0.50)
det_pct = deterministic / n
amb_pct = ambiguous / n
```

`det_pct` (the % of products with `determinism_score > 0.95`) is the sole input to R3's threshold
comparison. **This is the same `product_ambiguity.csv` column shown in `determinism_provenance.md`
to be computed with a dominant-account-selection bug for multi-company products** — R3's headline
percentage (91.2% production / 84.1% synthetic) inherits that issue. This document covers only the
*threshold logic itself*, which is separate from and downstream of that data-quality question.

## All threshold bands, exact boundaries, and the decision each produces

```python
THRESHOLD_DETERMINISTIC_RULES = 0.90   # >= 90% deterministic → rules-first
THRESHOLD_DETERMINISTIC_EMBED = 0.70   # >= 70% → embedding-primary; else LLM
```

```python
if det_pct >= THRESHOLD_DETERMINISTIC_RULES:      # det_pct >= 0.90
    decision = "RULES_FIRST"
elif det_pct >= THRESHOLD_DETERMINISTIC_EMBED:    # 0.70 <= det_pct < 0.90
    decision = "EMBEDDING_PRIMARY"
else:                                              # det_pct < 0.70
    decision = "LLM_REQUIRED"
```

| Band | Exact boundary | Decision | Ever observed in this repo? |
|---|---|---|---|
| Band 1 | `det_pct >= 0.90` | **RULES_FIRST** | Yes — production, 91.2% (`reports/phase1_final_report.md` §8) |
| Band 2 | `0.70 <= det_pct < 0.90` | **EMBEDDING_PRIMARY** | Yes — synthetic, 84.1% (`data/outputs/intelligence/decision_matrix.csv`, confirmed live-reproducible in `determinism_provenance.md` Step 2) |
| Band 3 | `det_pct < 0.70` | **LLM_REQUIRED** | No — neither the production nor the synthetic run has ever produced a `det_pct` below 0.70. This band exists in the code but has zero empirical instances anywhere in this repository. |

The metric is `det_pct = (products with determinism_score > 0.95) / (total distinct normalized
products)` — a **product-count fraction**, not an occurrence-weighted fraction. It uses the
*unweighted* population (each product counts once, regardless of transaction volume) — consistent
with `TECHNICAL_REPORT.md` §2.3's own framing of R3 ("deterministic products 91.2%"), but this is
worth stating explicitly since R1 (the neighboring decision) uses the *weighted* ADS instead — the
two decisions in the same matrix deliberately use differently-weighted versions of "how
deterministic is this dataset," and the report doesn't currently flag that they differ in this way.

## Rationale text the script emits per band (for completeness)

```python
# Band 1
f"{det_pct:.1%} of products are deterministic (>{THRESHOLD_DETERMINISTIC_RULES:.0%}). "
f"Use deterministic lookup for the majority; embedding search only for the "
f"{amb_pct:.1%} ambiguous tail."

# Band 2
f"{det_pct:.1%} deterministic, {amb_pct:.1%} ambiguous. "
f"Significant minority of ambiguous products. "
f"Embedding similarity is the primary classifier."

# Band 3 (never triggered in this repo)
f"Only {det_pct:.1%} deterministic, {amb_pct:.1%} ambiguous. "
f"High ambiguity across the dataset. LLM reasoning needed."
```

## Why `TECHNICAL_REPORT.md` §2.3's current description is incomplete

§2.3's decision-matrix table gives R3 exactly one row:

> "R3 — Model complexity | deterministic products 91.2% | ≥90% → rules-first | **RULES_FIRST**"

This states only the Band-1 boundary and Band-1's outcome. It does not mention:
- That there is a second, named band (`EMBEDDING_PRIMARY`, 70-90%) — which is not a hypothetical:
  it is exactly the band the synthetic run in the very same report (§3.2) falls into and is the
  mechanism behind the R3 "flip" that §3.3 spends an entire subsection discussing. A reader who
  reads §2.3 before §3.2 has no way to know EMBEDDING_PRIMARY is a real, defined, reachable state
  of the same decision rule — they'd have to infer it purely from seeing it appear in the results
  table.
- That there is a third band (`LLM_REQUIRED`, <70%) at all, even though it is never triggered.
  Whether to document a never-triggered band is a judgment call (see Question F5 in
  `RESEARCH_AUDIT.md`), but as written the paper implies R3 is a two-outcome rule
  (RULES_FIRST-or-not) when the code implements a three-outcome rule.
- That R3's metric (`det_pct`) is unweighted/product-count-based, in a report section that, one
  subsection earlier (§2.2), has just finished explaining at length why weighted-vs-unweighted
  matters for ADS. A reader could reasonably assume R3 uses the same weighted ADS R1 uses; it
  doesn't — it recomputes its own unweighted `det_pct` directly from `product_ambiguity.csv`,
  independent of the `dataset_ads_w`/`dataset_ads_u` values `04_architecture_decision.py` computes
  separately in `compute_dataset_ads()`. (Numerically, `det_pct` and `dataset_ads_u` are computed
  from the same `product_ambiguity.csv` rows but are two different statistics — one is "the
  unweighted mean of determinism scores," the other is "the fraction of products above 0.95" — so
  even calling both "unweighted" doesn't make them the same number; they merely share an input.)

## How the synthetic R3 flip mechanically occurs

1. Production: `det_pct = 91.2%` (43,156 / 47,306 products, per `phase1_final_report.md` §7) →
   `91.2% >= 90%` → Band 1 → **RULES_FIRST**.
2. Synthetic: `det_pct = 84.12%` (710 / 844 products, per `data/outputs/intelligence/decision_matrix.csv`,
   confirmed live-reproducible in `determinism_provenance.md`) → `70% <= 84.12% < 90%` → Band 2 →
   **EMBEDDING_PRIMARY**.
3. The flip is entirely a consequence of the synthetic run's `det_pct` landing on the other side of
   the single `0.90` boundary from the production run's `det_pct` — both runs are evaluated by the
   identical, unmodified threshold code; nothing about the *decision logic* differs between runs.
   `TECHNICAL_REPORT.md` §3.3's explanation ("the production figure itself sits only about one
   point above the 90% threshold... sampling noise... is enough to cross it") is an accurate
   description of this mechanism.
4. Per `determinism_provenance.md` Step 4: correcting the Step-3 dominant-account bug moves the
   synthetic `det_pct` from 84.12% to an estimated ~87.56% — still inside Band 2, so **the flip is
   not an artifact of that bug**; it would occur even with corrected input data, just with a
   narrower margin from the boundary (87.56% vs. 90%, instead of 84.12% vs. 90%).

## Is this a bug?

**No bug found in the R3 decision logic itself.** The three-band structure is internally
consistent, deterministic, and correctly implemented — Band 1 and Band 2 boundaries meet exactly
at 0.90 with no gap or overlap, Band 2 and Band 3 meet exactly at 0.70, and every comparison uses
the documented named constants. Per the audit task's instruction ("Do not change the implementation
unless an actual bug is discovered"), **no change was made to `decide_model_complexity()` or its
threshold constants.**

The only bug related to R3 is upstream, in its *input data* (`product_ambiguity.csv`'s
determinism_score computation) — fully documented in `determinism_provenance.md`, not this file —
and, per that document's Step 4, does not change R3's decision on either the production or
synthetic run, only the reported margin.

## Recommendation

Update `TECHNICAL_REPORT.md` §2.3's R3 row (or add a sentence to §3.3) to state the full three-band
structure, not just the ≥90% cutoff — see Recommendation E4 in `RESEARCH_AUDIT.md`. This is a
manuscript-text change and, per this task's scope, is **not** performed here.

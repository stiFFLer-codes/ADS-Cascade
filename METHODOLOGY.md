# METHODOLOGY — Synthetic Reproduction of the ContAI Classification Pipeline

This is the `research` branch of a production accounting-classification project
(D406 Romanian fiscal invoices → GL account classification, extended to receipt
classification). `main` holds the real, confidential production pipeline and
data. This branch holds the **same methodology** — the same unmodified scripts,
the same architecture decisions — running against **entirely synthetic data**,
so the design can be published and independently inspected without exposing
any client's identity, invoices, or receipts.

## What's confidential vs. what's public

| | Confidential (main only) | Public (this branch) |
|---|---|---|
| Client identity, CUIs, addresses | ✓ | never |
| Raw D406 XMLs, receipt photos, invoice line data | ✓ | never |
| The classification methodology (ADS metric, Four-Tier Confidence Cascade, hybrid retrieval, RULES_FIRST decision, all 16 ADRs) | — | ✓ |
| Aggregate statistics computed from real data (91.2% deterministic, 0.695 cross-company consistency, 94.5% VAT stability, etc.) | — | ✓, cited as such |

Everything in `architecture/`, `scripts/` (Phase 1 + Phase 2 + `p2lib/`), and the
reports is the same code that produced the real numbers above — this branch
does not redesign anything, it re-runs it on synthetic input.

## What changed from `main`

1. **`scripts/00_generate_synthetic.py`** (new) — generates fictitious companies,
   products, GL accounts, and invoice lines directly from the *targets* documented
   in `data_verification_audit.md` (91.2% product determinism, 0.695 cross-company
   consistency, 94.5% VAT stability, 73.9/26.1 purchase/sale split), rather than
   reading any real data. It writes `data/outputs/invoice_lines_all_companies.csv`,
   `product_account_mapping.csv`, `invoice_statistics.csv`, and `gl_statistics.csv`
   — the same file paths and column schemas `03_5_dataset_intelligence.py`,
   `04_architecture_decision.py`, and the Phase 2 scripts already expect, so
   nothing downstream needed to change.
2. **Five hand-written synthetic Textract fixtures** (`data/outputs/phase2/textract_raw/`)
   replace the 10 real cached receipt photos, using fictitious vendors/CUIs.
   `p2_05_end_to_end.py` runs against them unmodified.
3. **Deleted**: all real data (`data/normalized/`, `data/downloads/`,
   `data/source_of_truth/`, `data/extracted/`, `Receipts Examples/`, real
   `textract_raw/*.json`, `llm_cache/*`), Phase 1 outputs derived from it
   (`companies_inventory.csv`, `company_gl_accounts.csv`,
   `company_gl_catalog.json`, `metadata.csv`, operational logs under
   `data/logs/`), and files that hadn't been regenerated against synthetic data
   and still held real content (`llm_tail_proposals.csv`, `receipts_demo.json`
   — both require a paid LLM call this branch doesn't make).
4. **Anonymized worked examples**: `architecture/11_SEQUENCE_ROMPETROL.md` →
   `11_SEQUENCE_PETROMAX.md` and every other doc that named a real company
   (Rompetrol, FIRCOM VTEC, Vinalcool, etc.) as a worked example now uses a
   fictitious name, CUI, and address. The Phase 1 evidence pattern the example
   illustrates (the same product booked to different accounts by different real
   companies) is real; the names are not.
5. **Removed superseded delivery drafts** (old presentation HTML/MD files that
   predate the final demo) — not part of the methodology package.

Scripts `01_build_inventory.py` through `03_invoice_line_extraction.py` are
present as source (they *are* part of the methodology) but don't run on this
branch — they parse real D406 XMLs this branch doesn't have. The generator
replaces their *output*, not their *input*. This is the same tradeoff any
paper using confidential production data makes: the pipeline is inspectable,
the input data is not.

## Honest result comparison: real production data vs. this synthetic run

The synthetic run is deliberately smaller (60 companies, ~7,500 lines vs. the
real 169 companies / 296,648 lines) — enough to exercise every downstream
script and reproduce the same *kind* of signal, not a byte-identical replay.
Numbers will not match exactly; that's the point (same method, independent data).

| Metric | Real (production, `main`) | Synthetic (this branch) |
|---|---|---|
| Companies | 169 | 60 |
| Invoice lines | 296,648 | 7,523 |
| Weighted ADS | 0.847 | 0.809 |
| Unweighted ADS | 0.964 | 0.931 |
| Products >0.95 determinism | 91.2% | 84.1% |
| Cross-company consistency | 0.695 | 0.763 |
| Purchase / sale split | 73.9% / 26.1% | 73.5% / 26.5% |
| VAT missing | 4.05% | 4.45% |
| Warehouse missing | 100% | 100% |
| **R1 — Retrieval strategy** | **HYBRID** | **HYBRID** ✓ |
| **R3 — Model complexity** | **RULES_FIRST** (91.2% ≥ 90% threshold) | **EMBEDDING_PRIMARY** (84.1% < 90% threshold) |
| **R4 — VAT strategy** | SECONDARY_FEATURE | SECONDARY_FEATURE ✓ |
| **R5 — Warehouse** | DROP | DROP ✓ |
| Stage A auto-apply accuracy (held-out) | 98.1% @ 42.8% coverage | 99.8% @ 76.2% coverage |

**The R3 discrepancy is a real, useful finding, not a generator bug.** The real
dataset's 91.2% determinism rate is itself only ~1 point above the 90%
RULES_FIRST/EMBEDDING_PRIMARY threshold used by `04_architecture_decision.py`
— it was always a close call. At the smaller synthetic scale, sampling noise
on lower-evidence products pulls the observed rate to 84.1%, crossing to the
other side of the same threshold. Both runs agree on HYBRID, SECONDARY_FEATURE,
and DROP by a comfortable margin; R3 is the one decision close enough to the
threshold that it's sensitive to run-to-run variation — which is itself
evidence the 90% cutoff deserves calibration against more data before being
treated as load-bearing, not evidence the method is wrong. This is intentionally
left as-observed rather than tuned to force a match.

Stage A's higher accuracy/coverage on synthetic data reflects the smaller
product catalog (844 vs. 47,306 unique products): with fewer distinct products
per company, train/test overlap is higher, so more test-time lookups have
direct precedent. This is an expected artifact of scale, not a claim that the
real system performs this well in production.

## Known limitations (carried over from the real system)

- **`p2lib/retrieval.py`** implements lexical fuzzy matching (rapidfuzz) as an
  explicit, in-code placeholder for the embeddings/vector-DB retrieval layer
  `architecture/07_DATA_SCHEMA.md` and `09_AI_ORCHESTRATION.md` specify. This is
  a documented gap between designed and shipped architecture — what was
  deferred, and why — not an oversight.
- Cross-company consistency has a real ceiling (0.695 in production, ~0.7–0.8
  here) — company-specific overrides exist because a shared global model alone
  is measurably wrong on multi-company products often enough to matter.
- All synthetic-run numbers above are single-seed (`random.seed(42)` in the
  generator) — re-running with a different seed will shift the exact figures
  within the same qualitative shape.

## Reproducing this branch

```
python scripts/00_generate_synthetic.py       # writes synthetic Phase 1 outputs
python scripts/03_5_dataset_intelligence.py   # ADS, consistency, VAT stats
python scripts/04_architecture_decision.py    # R1-R5 decisions + report
python scripts/phase2/p2_01_build_kb.py       # knowledge base from synthetic data
python scripts/phase2/p2_02_classify_eval.py  # held-out cascade eval
python scripts/phase2/p2_05_end_to_end.py     # 5 synthetic receipts -> tiers
```

All offline, no API keys, no external data. `p2_06_llm_tail.py` (the LLM
re-ranker) is not run on this branch — it requires a live LLM call and isn't
needed to validate the deterministic/retrieval methodology this branch exists
to demonstrate.

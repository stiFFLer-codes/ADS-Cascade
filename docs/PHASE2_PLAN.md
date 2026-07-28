# Phase 2 — Implementation Plan (Receipt Intelligence, evidence-first demo)

> Working plan for the Phase 2 demo. Status lives in `../STATE.md`; roadmap context in
> `Phases.md`. This implements *demo projections* of `../architecture/07_DATA_SCHEMA.md`
> and `../architecture/08_CONFIDENCE_CASCADE.md` — it does not redesign them.

## Why this shape

Phase 2 adds receipt (bon fiscal) classification. The client spec names Textract (OCR) +
Haiku (reasoning) — that's *one implementation*, not an architecture. We carry forward the
Phase 1 methodology that worked: **each step answers one question and reduces one
uncertainty; AI enters only where evidence demands it.**

Three facts reshape the naive "OCR-first" roadmap:

1. **The uncertainty differs from Phase 1.** Phase 1 already de-risked *classification*
   (91.2% deterministic, RULES_FIRST, hybrid) and that transfers to receipts unchanged
   (same products/companies/KB). The open question now is **extraction** — can a crumpled
   thermal photo become clean structured fields?
2. **Corpus reality.** We have **10 receipt images** (`../Receipts Examples/`), not a
   bucket — enough for a hand-labeled *qualitative* demo, not a statistical benchmark.
   Receipts are **not self-labeling** (no account_id on paper), so ground truth is hand-built.
3. **Tooling.** No paid LLM keys; offline/free preferred. AWS free credits exist but user
   is new to AWS → Textract is an *optional* run, not the spine.

**So we order by dependency, not receipt-flow:** unblocked+free classification first,
then extraction/validation on the 10, then join end-to-end.

Evidence (café receipt): 4 products, VAT brackets A(21%)+B(11%) printed per line, Σ=37.00
reconciles — VAT is deterministic from the bracket letter; the clipped left edge is the
real OCR challenge.

## Guiding principle
One question → one measurable artifact per stage. No AI until a stage's evidence demands
it. Reuse Phase 1 infra (`../utils/`, `../config/settings.py`, the `../prerun_check.py`
pattern). New code in `scripts/phase2/`; outputs in `data/outputs/phase2/`.

---

## Stage 0 — Schema & harness  *(unblocked, ~free)*
**Q:** what contract does every module speak?
Define canonical **receipt JSON** as a flat projection of `07` (`document` +
`document_line` + `extraction_result`): `supplier{name,cui}`, `datetime`, `payment_method`,
`currency`, `totals{grand, vat[]}`, `items[{raw_text, normalized_text, qty, unit_price,
line_amount, vat_bracket_letter, vat_percent, account_id, tax_code, confidence}]`,
`validation{status, checks[]}`. Ship `scripts/phase2/schema/receipt.schema.json` + validator
`scripts/phase2/p2lib/schema.py`.

## Stage A — Classification cascade on Phase 1 data  *(UNBLOCKED, offline, free — DO FIRST)*
**Q:** does the accounting brain work, and how much needs no AI?
- **Inputs:** `data/outputs/product_account_mapping.csv` (76,843 mappings),
  `company_gl_accounts.csv` / `company_gl_catalog.json` (GL screen).
- Build KB (per-company rules + `global_pattern` distributions + product catalog), implement
  the locked **RULES_FIRST cascade** (`08`): P0 alias/normalize → P1 company rule → P1b
  global → P2 lexical fallback → P3 VAT re-rank → P4 GL screen → tiering T1–T4. Hold out a
  slice; measure.
- Shared modules `p2lib/{kb,retrieval,cascade,confidence}.py` (reused by Stage C).
- **P2 fallback = lexical baseline first** (rapidfuzz or sklearn TF-IDF char-ngrams) — free,
  offline. Embeddings (multilingual sentence-transformers) = documented drop-in upgrade
  behind the same `retrieval.py`. 91% is P1 anyway.
- **Scripts:** `p2_01_build_kb.py`, `p2_02_classify_eval.py`.
- **Outputs:** `data/outputs/phase2/kb/*`, `classification_eval.csv`,
  `tier_distribution.csv`, `per_company_accuracy.csv`.
- **Success:** reproduces Phase 1 (~90% Tier-1 auto-apply, high held-out accuracy).

## Stage B — Extraction + validation on the 10 receipts  *(extraction = the real unknown)*
**Q:** can we reliably turn a thermal photo into a valid structured receipt?
- **B1 Gold set:** hand-transcribe all 10 `../Receipts Examples/` into the Stage 0 schema →
  `data/receipts/gold/*.json`. The measuring stick.
- **B2 Extraction:** `p2lib/extract/` adapter (model-agnostic, ADR-011). Optional **AWS
  Textract AnalyzeExpense** via boto3 (free credits; the one AWS-onboarding step, not
  required for the core demo). Vision-LLM noted as a candidate that could collapse
  OCR+structuring, pluggable when a key exists. Score vs gold.
  → `p2_03_extract.py` → `extracted_receipts.json`, `extraction_scores.csv`.
- **B3 Validation (pure logic, offline):** Σ(line_amount)=grand_total ±0.1 RON (hard-fail
  >1); **VAT from bracket letter** with arithmetic reconciliation as fallback only;
  duplicate fingerprint + partial-read join (ADR-014); required-field completeness.
  → `p2_04_validate.py` → `receipt_validation.csv`.
- **Metrics:** field/line extraction accuracy vs gold; validation pass rate; % VAT resolved
  by bracket letter (expected high → little LLM needed).

## Stage C — End-to-end join  *(the demo that turns heads)*
**Q:** photo → ERP-ready entry: how much auto-classifies, how much needs a human?
Feed validated receipts through the Stage A cascade (reuses `p2lib/cascade.py`).
→ `p2_05_end_to_end.py` → `e2e_classification.csv`, `e2e_summary.csv`.
**Metrics:** auto-classify rate (T1/2) vs review rate (T3/4) over the 10. Expected: café
lines resolve high-tier; a precedent-less `rovinieta` lands in T3 with the 628/635/6352
split (matches `08 §6`).

## Deferred — blocked, mark don't build
WhatsApp ingestion (OPEN-Q7), review UI, ERP XML export (OPEN-Q10), monthly etva/ANAF CAEN
refresh. Out of demo scope until manager confirms.

## Reuse (do NOT recreate)
- `utils/{logger,csv_writer,filesystem,manifest}.py`, `config/settings.py`, `prerun_check.py`.
- `data/outputs/product_account_mapping.csv`, `company_gl_accounts.csv`, `company_gl_catalog.json`.
- `architecture/07_DATA_SCHEMA.md`, `architecture/08_CONFIDENCE_CASCADE.md`.
- `Receipts Examples/` (10 images), `image (1).png` (Petromax rovinieta reference, name anonymized).

## New dependencies (minimal; flag before adding)
- `rapidfuzz` **or** `scikit-learn` — P2 lexical similarity (rapidfuzz is lighter).
- `boto3` — only for the optional Textract run.
- `sentence-transformers` — deferred P2 upgrade, not needed for the demo.
- `jsonschema` — optional Stage 0 validator (or hand-roll to stay stdlib).

## Verification
- **A:** `python scripts/phase2/p2_02_classify_eval.py` → accuracy + Tier-1 % near Phase 1;
  `tier_distribution.csv` sums to 100%.
- **B:** `p2_04_validate.py` marks the café receipt VALID (Σ=37.00, A+B VAT from letters)
  and flags a corrupted copy; `extraction_scores.csv` shows per-field accuracy vs gold.
- **C:** `p2_05_end_to_end.py` produces a per-line tier; precedent-less rovinieta → Tier-3.
- Every stage idempotent and re-runnable (`prerun_check` before each), Phase-1 style.

## Open decisions (don't block the demo)
- Run the real Textract benchmark now (AWS onboarding) vs eyeball extraction on 10 and defer.
- Larger receipt corpus + labels — required before any *statistical* OCR benchmark.

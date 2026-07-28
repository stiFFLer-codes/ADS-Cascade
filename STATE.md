# STATE — ContAI Invoice/Receipt Classification

> **Read this first.** Living project state for cheap session handoffs.
> Pointer-based on purpose — it links canonical docs, it does not copy them.
>
> `Last updated: 2026-07-28` · **Current phase: Phase 2 demo COMPLETE; Track A Phase 1 (research branch + synthetic data) COMPLETE on `research` branch**

---

## ▶ Resume in a new session

Paste this into a fresh session to continue with full context:

> I'm continuing the **ContAI Phase 2** project (Romanian receipt/invoice AI classification).
> Read `STATE.md` first, then `docs/INDEX.md`, `docs/PHASE2_PLAN.md`, and `architecture/00_SCOPE.md`
> for full context. Phase 1 (D406 pipeline) and the Phase 2 demo are **complete and committed** —
> code in `scripts/phase2/` (p2_01…p2_06 + p2lib/), interactive demo at `docs/demo/index.html`.
> The AWS Textract + Groq LLM calls are cached so everything reproduces offline at $0
> (`GROQ_API_KEY` goes in a git-ignored `.env`). Don't re-derive what STATE.md already records.
> **What I want to do next: <fill in>.**

---

## Where we are

Phase 1 (data engineering) and Phase 2 (receipt-classification demo) are both **complete and
committed**. The interactive stakeholder demo is built (`docs/demo/index.html`). This folder is
being finalized as the delivery package. No open implementation work — remaining items are optional
(larger OCR benchmark, production pieces awaiting manager decisions).

## Done

- **Phase 1 — Data Engineering pipeline.** 6 scripts (`scripts/`), stdlib-only.
  296,648 invoice lines · 169 companies · weighted ADS 0.847 · 91.2% products
  deterministic · 76,843 product→account mappings. Committed.
  → `reports/phase1_final_report.md`
- **Phase 2 — Solution Architecture.** 17 docs (`architecture/`): scope, requirements,
  NFRs, domain model, services, event workflow, data schema, confidence cascade,
  AI orchestration, API contracts, sequences, security, observability, cost, plus
  16 ADRs and 20 open questions. **Written but untracked in git.**
  → `architecture/00_SCOPE.md`
- **Entry docs** (this file + `docs/`).

## Next (immediate)

**DONE (2026-07-28): Track A Phase 1 — research branch + synthetic data, on `research` branch (commit `456f417`).**
`scripts/00_generate_synthetic.py` generates synthetic companies/products/invoice lines from the
documented target distributions (no real data read). Full pipeline (03_5 → 04 → phase2
p2_01/p2_02/p2_05) re-run end-to-end on synthetic data. All real data, stale real-derived
files, and real-named worked examples in architecture/reports stripped or anonymized — see
`METHODOLOGY.md` for the honest real-vs-synthetic comparison (including a boundary-case R3
architecture-decision flip at the smaller synthetic scale, documented not tuned away).

**Flag for the eventual "publish to public GitHub" step:** the `research` branch's git *history*
still contains every pre-2026-07-28 commit on `main`, including commits with real client data
(before this session's cleanup). Deleting files in new commits does not remove them from history.
Before pushing this branch publicly, it needs either a fresh orphan branch/squashed history
containing only the clean synthetic snapshot, or history-scrubbing (e.g. `git filter-repo`) —
do not `git push` this branch as-is.

**Track A remaining (must-do, ~3 weeks):**
1. Write 4–8 page technical report (problem/method/evaluation/honest limitations, cite as "validated on 296K invoices, synthetic shown for reproducibility")
2. Publish to arXiv/Zenodo preprint (publication credit for Criterion 2 — Previous Relevant Experience)
3. Public GitHub `research` branch (squashed/orphan history, see flag above) with README + `METHODOLOGY.md`
4. Draft CV entry (~150 words) + video talking points (3–4 on rules-first + human feedback)

**Track B (stretch, no deadline):** Once preprint exists, optionally prep for next-year workshop cycles (DocInsights 2027, FinanSE 2027, PAKDD finance 2027). Aug 2, 2026 DocInsights is off the table (only 5 days; too risky to compromise Track A).

**Numbers discipline:** Any metric in the report must trace to `data_verification_audit.md` "Authoritative Value" column (e.g., 91.2% deterministic not 85%, 0.695 consistency not 0.694).

---

### Phase 2 demo (for reference — COMPLETE)

Phase 2 demo plan approved → `docs/PHASE2_PLAN.md`. Already DONE:

- **DONE — Stage B2 (OCR cache):** all 10 `Receipts Examples/` run through AWS Textract
  AnalyzeExpense, cached to `data/outputs/phase2/textract_raw/*.json` via
  `scripts/phase2/p2_03_extract.py` (idempotent, one call ever per receipt). AWS IAM user
  `contai-textract`, region ap-south-1. Finding: AnalyzeExpense returns vendor, CIF
  (TAX_PAYER_ID), date, totals, tax, line items; the VAT bracket letter (A/B) rides in
  each line's `EXPENSE_ROW` — no separate raw-text pass needed. `TOTAL` is ambiguous
  (real total vs "TVA BON") → structuring must disambiguate.

- **DONE — Stage A (classification cascade):** `scripts/phase2/p2lib/*` + `p2_01_build_kb.py`,
  `p2_02_classify_eval.py`, `test_cascade.py`. Held-out eval (63,048 test lines, 80/20 split):
  **Tier-1 deterministic = 98.4% accuracy at 42% coverage**; after calibrating fuzzy/low-evidence
  to review (measured ~45-49% → unsafe to auto-apply), **auto-apply = 42.8% coverage @ 98.1%
  accuracy**, 57% routed to review. Overall 66.7% is pessimistic by construction — a random split
  makes 36% of test lines "cold" (no exact precedent); production seeds the full-history KB so
  cold-start is far smaller. The fuzzy/cold tail (~27% acc) is where embeddings + LLM must earn
  their place. Artifacts: `data/outputs/phase2/{kb/,classification_eval,tier_distribution,per_company_accuracy}.csv`.

- **DONE — Stage B3 + Stage C (structuring + end-to-end):** `p2lib/{structure,normalize}.py`,
  `p2_05_end_to_end.py`. Structured the 10 cached receipts, validated (café Σ=37 PASS, VAT A/B
  from bracket letters; a fuel-retailer receipt's discount lines correctly flagged sum-REVIEW), and routed 22 line
  items through the cascade as a cold-start NEW client (global KB, PURCHASE-strict).
  Result: **0 auto / 8 Tier-3 / 14 Tier-4** — the honest cold-start extreme. KEY FINDING
  (`e2e_classification.csv` nearest_global): most "no precedent" products ARE in the KB at
  fuzzy 90-100 ("rovinieta a autoturisme"→"rovinieta", "4 omv maxxmotion 95"→"omv maxxmotion 95",
  "robineti trecere"→"robinet trecere") — exact lookup missed only on OCR formatting. So the tail
  is mostly a RETRIEVAL-bridge problem, not an LLM problem. Cross-company account signal is weak
  and sometimes wrong (caffee latte→6022 fuel) → confirms everything must go to review.

- **DONE — retrieval bridge in cascade:** `cascade.classify(global_pool=...)` fuzzy-bridges the
  OCR-formatting gap (review only, cutoff 88). Stage C re-run: T4 dropped **14→2**, T3 **8→20** —
  20/22 lines now carry a concrete account candidate; only 2 are genuinely novel.
- **DONE — model-agnostic LLM adapter (Groq):** `p2lib/ai/adapter.py` (uses `requests`, no new dep;
  reads `GROQ_API_KEY` from env; caches to `data/outputs/phase2/llm_cache/`) + `p2_06_llm_tail.py`
  (runs on review tail only, output always REVIEW). No-key path exits cleanly. `.gitignore` added.

- **DONE — LLM tail (Groq live, grounded):** `p2lib/ai/adapter.py` (requests, no python-dotenv;
  `.env` auto-loaded; `parents[4]`; UTF-8; 30 RPM throttle + 429 backoff; caches to `llm_cache/`) +
  `p2_06_llm_tail.py`. Now feeds each product the **cascade's retrieved candidate accounts** (Stage C
  writes them to `e2e_classification.csv:candidate_accounts`); the LLM re-ranks precedent instead of
  guessing. Result flipped from "3717 for everything" to correct accounts (fuel→6022, discount→609,
  cigarettes→371, parking/rovinieta→628). Confirms the architecture: **LLM = re-ranker over retrieval,
  not an autonomous classifier**; output always REVIEW. `llm_tail_proposals.csv`.
- **DONE — committed** Phase 2 + architecture + docs at `a0e013f`. `.env` gitignored; `.claude/`,`.ua/` ignored.

- **DONE — stakeholder demo** (`docs/demo/index.html`): single self-contained HTML (no server, no deps,
  opens by double-click), "Bon Fiscal" design, scroll narrative + animated flowcharts + receipt-scan.
  12 sections: problem → 91% idea → Phase 1 pipeline → 4-tier cascade → live café-receipt trace (with AWS
  & Groq disclosure callouts) → 10 receipts routed → where-AI-belongs funnel → shared-brain loop → CAEN
  cold-start prior → why-it-scales → honest limits. All numbers baked from committed artifacts; verified
  by headless render. Mixed audience (plain-English + "under the hood" expanders).

**Phase 2 demo pipeline is COMPLETE end-to-end** (photo → Textract cache → structure → validate →
cascade → retrieval bridge → grounded LLM tail). Remaining (all optional):

1. **Stage B1/B2:** hand-label the 10 (gold → `data/receipts/gold/`) to put a number on OCR accuracy.
2. Manager-facing write-up of the demo + numbers.
3. Blocked/deferred: WhatsApp ingestion, review UI, ERP export (need manager answers — `OPEN_QUESTIONS.md`).

## How to run / resume (any session or AI)

All offline except two cached API layers. Reproducible without keys (caches committed).
```
python scripts/phase2/p2_01_build_kb.py        # KB from Phase 1 mappings
python scripts/phase2/p2_02_classify_eval.py   # held-out cascade eval (Tier-1 98.4%)
python scripts/phase2/p2_03_extract.py         # Textract OCR (idempotent; 0 new calls if cached)
python scripts/phase2/p2_05_end_to_end.py      # 10 receipts -> per-line tier + candidates
python scripts/phase2/p2_06_llm_tail.py        # LLM re-rank on review tail (needs GROQ_API_KEY)
python scripts/phase2/test_cascade.py          # fast self-checks
```
- **Groq key:** put `GROQ_API_KEY=gsk_...` in `.env` at repo root (gitignored). No key → p2_06 skips cleanly.
- **Groq free-tier limits (llama-3.3-70b-versatile): 30 RPM / 12K TPM.** Adapter throttles to ~27 RPM +
  429 backoff; cached calls don't count. Swap to Claude Haiku = edit `p2lib/ai/adapter.py` + `ANTHROPIC_API_KEY`.
- **AWS:** IAM user `contai-textract`, region ap-south-1; Textract cached → $0 going forward.

## Open decisions / blockers

Headline items (full list → `architecture/OPEN_QUESTIONS.md`):

- **Production stack unconfirmed** — language, DB, hosting, how the live D406
  pipeline is deployed. Design stays tech-agnostic until answered.
- **WhatsApp Business route** — direct Meta vs BSP partner.
- **ERP export format** — target accounting system's import XML schema.
- **Receipt volumes** — per company/month; drives cost model and batching.
- Confidence thresholds (0.95 / 0.85) are Phase 1-derived starting points — pilot must calibrate.

## Where things live

| What | Path |
|---|---|
| Pipeline scripts | `scripts/` |
| Pipeline outputs (ground truth) | `data/outputs/` |
| Source dataset | `data/source_of_truth/Dev-D406-Dataset.json` |
| Phase 2 design (source of truth) | `architecture/` |
| Phase 1 reports | `reports/` |
| Entry / navigation docs | `docs/` (start at `docs/INDEX.md`) |
| Repo map | `README.md` |
| Working rules | `AGENTS.md` |

## Update protocol

At the **end of each session**, edit only *Where we are*, *Next*, *Done*, and the
`Last updated` date. Keep it pointer-based — never copy architecture prose in here.
This is the committed, shared counterpart to Claude's private per-machine memory
(`.claude/.../memory/MEMORY.md`).

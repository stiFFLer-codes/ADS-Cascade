# ADS-Cascade — Score Determinism, Then Choose the Architecture

Most accounting-document classification products start by picking a model. This project starts
by **measuring the data**: for Romanian fiscal documents (D406/SAF-T invoices, extended to
photographed retail receipts), how consistently does a product map to one GL account? That
measurement — the **Automated Determinism Score (ADS)** — is computed first, and it *decides* the
architecture: a rules-first, per-company knowledge base with hybrid retrieval, not a single
learned classifier, with an LLM used only as a re-ranker over retrieved candidates for the
measured minority tail.

**Read the paper:** [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md) — problem, method, evaluation
(real + synthetic), honest limitations. **Read the method in full:** [`METHODOLOGY.md`](METHODOLOGY.md)
— what's public vs. confidential, and the honest real-vs-synthetic comparison this report draws from.

---

## ▶ Start here

1. **Read the technical report:** [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md)
2. **Open the interactive demo:** [`docs/demo/index.html`](docs/demo/index.html) — double-click
   it; a self-contained, animated walkthrough of the whole system (no install, works offline).
   Shows the real (anonymized) production trace — see note below.
3. **Current status & how to run:** [`STATE.md`](STATE.md)
4. **Navigate everything:** [`docs/INDEX.md`](docs/INDEX.md)

---

## What's inside

| Phase | What | Result |
|---|---|---|
| **Phase 1 — Data Engineering** | 6-script pipeline mining D406 (SAF-T) XML filings for per-product determinism | 296,648 invoice lines · 76,843 product→account mappings · 91.2% of products deterministic (cited, production) |
| **Phase 2 — Receipt Intelligence** | photo → OCR → structure/validate → RULES_FIRST four-tier cascade → retrieval → LLM tail | Tier-1 **98.4%** held-out accuracy; auto-apply 42.8% @ 98.1% (cited, production) |

**The idea:** most classification is repetition, not judgment — so a per-company knowledge base
answers the bulk with no AI, retrieval bridges the tail, and an LLM (behind a swappable adapter)
re-ranks only what's genuinely new. Everything is evidence-driven and reproducible.

**Real vs. synthetic, and why both exist here:**

- The interactive demo (`docs/demo/index.html`) walks through the **real production trace** —
  10 actual photographed receipts, OCR'd and classified — with vendor names and CIFs anonymized.
  Its numbers are cited from a confidential engagement, not recomputed in this repo.
- The runnable pipeline (`scripts/`, `data/outputs/`) uses a **from-scratch synthetic generator**
  (`scripts/00_generate_synthetic.py`) so anyone can reproduce the methodology end-to-end offline,
  at $0, with no client data and no API keys. See `METHODOLOGY.md` for the full real-vs-synthetic
  comparison table, including one architecture decision (R3) that flips at the smaller synthetic
  scale — reported as a threshold-sensitivity finding, not tuned away.

---

## Folder map

```
TECHNICAL_REPORT.md ← the paper: problem / method / evaluation / limitations
METHODOLOGY.md      ← what's public vs. confidential + real-vs-synthetic comparison
docs/            ← demo/, INDEX.md, PHASE2_PLAN.md, Context.md, Phases.md
STATE.md         ← living status + how to run + resume prompt
architecture/    ← Phase 2 solution architecture (17 docs, 16 ADRs, open questions)
scripts/         ← Phase 1 pipeline (01–04) + Phase 2 (phase2/: p2_01…p2_06 + p2lib/)
reports/         ← Phase 1 findings & architecture decision
data/            ← source_of_truth manifest + outputs/ (synthetic results, incl. phase2/)
config/ utils/   ← shared settings and helpers
AGENTS.md        ← working conventions
requirements.txt ← Python deps (stdlib-first; rapidfuzz, requests, boto3, pypdf)
```

---

## Honest framing

This is a **validated prototype**, not a shipped product. OCR quality is demonstrated on 10 real
sample receipts in the cited production trace (qualitative validation, not a hand-labeled OCR
benchmark); the AWS Textract and Groq LLM calls in that original run used **test accounts** and
all responses were **cached** so the demo reproduces at **$0** with no keys. This repository's own
runnable pipeline validates the same methodology on synthetic data only. Production pieces
(WhatsApp intake, review UI, ERP export) await business decisions, tracked in
[`architecture/OPEN_QUESTIONS.md`](architecture/OPEN_QUESTIONS.md).

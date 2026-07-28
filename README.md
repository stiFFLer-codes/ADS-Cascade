# ContAI — Accounting Intelligence (D406 + Receipts)

An AI feature that reads Romanian fiscal documents and decides their accounting treatment
— **account, VAT, tax code** — the way each company's own accountant would. Built and
**measured on real data**, in two phases.

---

## ▶ Start here

1. **Open the interactive demo:** [`docs/demo/index.html`](docs/demo/index.html) — double-click
   it; a self-contained, animated walkthrough of the whole system (no install, works offline).
2. **Current status & how to run:** [`STATE.md`](STATE.md)
3. **Navigate everything:** [`docs/INDEX.md`](docs/INDEX.md)

---

## What's inside

| Phase | What | Result |
|---|---|---|
| **Phase 1 — Data Engineering** | 6-script pipeline over 1,290 D406 (SAF-T) XML filings | 296,648 invoice lines · 76,843 product→account mappings · proved 91–95% deterministic |
| **Phase 2 — Receipt Intelligence** | photo → OCR → structure/validate → RULES_FIRST cascade → retrieval → LLM tail | Tier-1 **98.4%** accuracy; auto-apply 42.8% @ 98.1%; demoed on 10 real receipts |

**The idea:** most classification is repetition, not judgment — so a per-company knowledge
base answers the bulk with no AI, retrieval bridges the tail, and an LLM (behind a swappable
adapter) re-ranks only what's genuinely new. Everything is evidence-driven and reproducible.

---

## Folder map

```
docs/            ← START HERE: demo/, INDEX.md, PHASE2_PLAN.md, Context.md, Phases.md
STATE.md         ← living status + how to run + resume prompt
architecture/    ← Phase 2 solution architecture (17 docs, 16 ADRs, open questions)
scripts/         ← Phase 1 pipeline (01–04) + Phase 2 (phase2/: p2_01…p2_06 + p2lib/)
reports/         ← Phase 1 findings & architecture decision
data/            ← source_of_truth manifest + outputs/ (results, incl. phase2/)
config/ utils/   ← shared settings and helpers
AGENTS.md        ← working conventions
requirements.txt ← Python deps (stdlib-first; rapidfuzz, requests, boto3, pypdf)
```

---

## Honest framing

This is a **validated prototype**, not a shipped product. OCR quality is demonstrated on 10
sample receipts (qualitative); the AWS Textract and Groq LLM calls run on **test accounts**
and all responses are **cached** so the demo reproduces at **$0** with no keys. Production
pieces (WhatsApp intake, review UI, ERP export) await business decisions, tracked in
[`architecture/OPEN_QUESTIONS.md`](architecture/OPEN_QUESTIONS.md).

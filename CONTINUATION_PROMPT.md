# Quick Paste for Next Session — EDISS Research Track A Execution

**Copy-paste this into a new session to continue with full context:**

---

I'm continuing the **ContAI** project (Romanian D406 fiscal pipeline → receipt classification). The Phase 1 and Phase 2 demo are complete and committed; now executing a **research publication strategy for EDISS Erasmus Mundus 2027–2029 application** (apply ~Nov 3, 2026).

## What Just Happened (Previous Session, 2026-07-28)

Researched EDISS scoring (Academic Merit 70pts fixed, **Previous Relevant Experience 15pts**, Personal Motivation 10pts, Recommendations 5pts) and identified the real constraint: EDISS doesn't require a research proposal, but does value supporting documentation (publications count under Criterion 2). Created a two-track strategy:

- **Track A (must-do, 3–4 weeks):** Execute existing `synthetic_data_plan.md` (research branch + synthetic data generator + pipeline re-run + preprint publication). This is locked down — plan at `C:\Users\MaitreyaSapariya\.claude\plans\hey-as-you-mentioned-enumerated-wolf.md`.
- **Track B (stretch, no deadline):** Future workshop submissions (not Aug 2 DocInsights — 5 days out, too risky). Next viable cycle is 2027 after EDISS app is in.

**Key insight:** Methodology (ADS, Confidence Cascade, hybrid retrieval, architecture decisions) is publishable. Data (client, CUIs, invoices, images) stays confidential. Existing `synthetic_data_plan.md` and `data_verification_audit.md` already have the roadmap.

## Where to Start

**Read first:**
- `STATE.md` — project state + what's done/next
- `C:\Users\MaitreyaSapariya\.claude\plans\hey-as-you-mentioned-enumerated-wolf.md` — full approved strategy
- `C:\Users\MaitreyaSapariya\.claude\projects\C--Users-MaitreyaSapariya-Desktop-ContAI-Analysis\memory\ediss-application-strategy.md` — key facts (EDISS scoring, timeline, confidential vs. public split)
- `synthetic_data_plan.md` — step-by-step execution plan (this is what I'm about to execute, Steps 1–6)

**What I want to do:** Execute **Track A, Phase 1** (research branch + synthetic data). Start with:
1. Create `research` branch off `main`
2. Write `scripts/00_generate_synthetic.py` (generates synthetic companies/invoices/GL-accounts preserving 91.2% ADS-deterministic, 0.695 cross-company consistency, 73.9/26.1 direction split, etc., without real identity)
3. Hand-write 5–10 synthetic `textract_raw/*.json` files (mimic Textract AnalyzeExpense schema)
4. Strip confidential data from branch
5. Re-run pipeline (`03_5_dataset_intelligence.py` → Phase 2 scripts) on synthetic data
6. Grep-audit for leaked data, write METHODOLOGY.md

## Key Numbers (Authoritative, from `data_verification_audit.md`)

Any metric cited in future reports/CV must trace to these:
- **91.2%** of products deterministic (ADS > 0.95), not 85%
- **0.695** cross-company consistency (not 0.694)
- **94.5%** VAT single-rate stability
- **296,648** total invoice lines (not 297K)
- **169** companies with invoice data (not 201 — 201 in inventory but 169 have data)
- **107,736** total invoices
- **47,306** normalized unique products

## Project Structure

```
ContAI/Analysis/
├── scripts/
│   ├── 01_build_inventory.py, 01_5_xml_normalization.py, 02_gl_account_extraction.py, etc. (Phase 1)
│   └── phase2/
│       ├── p2_01_build_kb.py, p2_02_classify_eval.py, p2_03_extract.py, etc.
│       └── p2lib/
│           ├── cascade.py (Four-Tier Confidence Cascade — core method)
│           ├── retrieval.py (lexical fuzzy matching, documented placeholder for embeddings)
│           ├── structure.py (Textract JSON parsing)
│           ├── normalize.py (product text normalization)
│           ├── data.py (CSV iteration)
│           └── ai/ (model-agnostic LLM adapter, currently Groq)
├── architecture/
│   ├── 00_SCOPE.md, 01_EXECUTIVE_SUMMARY.md, ..., 14 more docs
│   ├── 08_CONFIDENCE_CASCADE.md ← core method, all publishable
│   ├── DECISIONS.md, ADR-001…ADR-016 (16 Architecture Decision Records, all publishable)
│   ├── 12_SECURITY_COMPLIANCE.md ← verify before publishing
│   └── OPEN_QUESTIONS.md
├── reports/
│   ├── phase1_final_report.md ← authoritative numbers source
│   └── architecture_decision.md ← decision matrix
├── data/
│   ├── normalized/ ← real XMLs (DELETE on research branch)
│   ├── source_of_truth/ ← real manifest (DELETE on research branch)
│   ├── outputs/ ← pipeline outputs (regenerate from synthetic data on research branch)
│   └── downloads/ ← (DELETE on research branch)
├── Receipts Examples/ ← real photos (DELETE on research branch)
├── synthetic_data_plan.md ← execution roadmap (THIS is what I execute)
├── data_verification_audit.md ← authoritative metrics
├── STATE.md ← project state (just updated with research track info)
└── CONTINUATION_PROMPT.md ← this file
```

## Timeline (from 2026-07-28, target Nov 3, 2026 EDISS application opens)

| Week | Task |
|---|---|
| 1–2 | Research branch: synthetic generator, strip data, re-run pipeline, leak audit, write METHODOLOGY.md |
| 2–3 | Technical report draft (4–8 pages, problem/method/eval/honest limits) |
| 3–4 | Revise report, publish arXiv/Zenodo, finalize public repo + README |
| 4 | CV entry + video talking points |
| Aug–Oct | Buffer + optional Track B prep |

## Reminders

- **Numbers discipline:** Every metric → `data_verification_audit.md` authoritative column
- **Honest limitations section required:** lexical-vs-embeddings gap in retrieval.py, cold-start 0.695 ceiling, synthetic-only validation
- **Grep audit is non-negotiable** before anything goes public (search for known company names, CUIs, product strings)
- **DocInsights Aug 2, 2026 is OFF the table** — only 5 days, would compromise Track A quality
- The approved plan is non-negotiable — if you hit a blocker, flag it (don't skip to Track B or docinsights)

---

**Ready to start? Next session, paste the above and say: "I'm starting Track A Phase 1 (research branch + synthetic data). Let's go."**

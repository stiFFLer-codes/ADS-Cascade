# Quick Paste for Next Session — EDISS Track A, Report-Writing Phase

**Copy-paste this into a new session to continue with full context:**

---

I'm continuing my **EDISS Erasmus Mundus 2027–2029 application** research
portfolio (application opens ~Nov 3, 2026). This repo — `personal/research`
— is a **standalone public research repo**: the anonymized/synthetic-data
methodology export of a client project (ContAI, Romanian D406 fiscal
pipeline → receipt classification). It has **no relation to any client
repo** — it's a fresh git history (2 commits, started 2026-07-28), safe to
eventually push to GitHub as-is.

Read `STATE.md` and `METHODOLOGY.md` first — don't re-derive what they
already record.

## What's done (Track A Phase 1 — complete)

- `scripts/00_generate_synthetic.py`: generates synthetic companies/products/
  invoice lines targeting the documented real-data distributions (91.2%
  product determinism, 0.695 cross-company consistency, 94.5% VAT stability,
  73.9/26.1 purchase/sale split) — reads no real data.
- Full pipeline re-run end-to-end on synthetic data (`03_5_dataset_intelligence.py`
  → `04_architecture_decision.py` → `phase2/p2_01_build_kb.py` →
  `p2_02_classify_eval.py` → `p2_05_end_to_end.py` on 5 hand-written synthetic
  receipt fixtures).
- All real data, all real-named worked examples (company names, CUIs,
  addresses, receipt vendors), and unaudited binary files (a screenshot that
  leaked a real AWS account ID, a client spec PDF, two internal report PDFs)
  removed or anonymized. Verified with a full scan against the complete
  real company/CUI list — zero hits.
- `docs/demo/index.html` (interactive stakeholder demo) anonymized —
  vendor names/CIFs baked into its JS data array were a second-pass find,
  fixed separately from the main text-doc audit.
- `METHODOLOGY.md` written: what's public vs. confidential, and an honest
  real-vs-synthetic results table (including a boundary-case architecture
  decision that flips at the smaller synthetic scale — documented as a
  finding, not tuned away).

**Audit lesson to carry forward:** the original text-grep audit missed
binary files and a *second* real-name source (receipt vendors, separate
from the D406 invoice-company list). If you add any new content — images,
PDFs, new demo data — audit it explicitly; don't assume the existing clean
state covers new material.

## Key numbers (authoritative — `data_verification_audit.md`)

Real production data (cite as "validated on a confidential production
dataset," never reproduce the raw numbers' source):
- 296,648 invoice lines · 169 companies · 107,736 invoices · 47,306 unique products
- Weighted ADS 0.847 / unweighted 0.964 · 91.2% products deterministic (>0.95 ADS)
- 0.695 cross-company consistency · 94.5% VAT single-rate stability
- 73.9% / 26.1% purchase/sale split

Synthetic reproduction (this repo, `data/outputs/`) — see METHODOLOGY.md's
full comparison table for exact figures and the R3 boundary-case discussion.

## What's next (Track A remaining)

| Week (from 2026-07-28) | Task |
|---|---|
| 2–3 | **← start here.** Write 4–8 page technical report: problem / method (ADS → hybrid retrieval → four-tier cascade) / evaluation (real + synthetic) / honest limitations (retrieval.py lexical-vs-embeddings gap, 0.695 cross-company ceiling, synthetic-only public validation) |
| 3–4 | Revise report, publish to arXiv or Zenodo (Zenodo if arXiv endorsement is a blocker — gives a citable DOI, no gate), finalize this repo's README to lead with architecture not data |
| 4 | Draft CV entry (~150 words, Criterion 2 — Previous Relevant Experience) + 3–4 video talking points (rules-first + human-feedback framing — data-intensive *systems* engineering, not a leaderboard benchmark) |
| Buffer Aug–Oct | Slack, optional Track B (next-cycle workshop: DocInsights/FinanSE/PAKDD-finance 2027, no deadline pressure) |

## Reminders

- **Numbers discipline:** every metric in the report → `data_verification_audit.md`'s authoritative column. Don't cite the exact real-data figures as if measured *in this repo* — this repo's own runs are the synthetic ones; frame real numbers as "validated separately on production data."
- **No git remote yet.** When ready to publish, create a new GitHub repo and push this repo's `main` as-is (its history is already clean — no squashing needed, unlike the client repo it was exported from).
- **Source of truth for methodology questions**: `architecture/` (17 docs, 16 ADRs, all public), `architecture/08_CONFIDENCE_CASCADE.md` (core method), `architecture/DECISIONS.md`.
- If something needs cross-checking against the original client project, that lives at `C:\Users\MaitreyaSapariya\Desktop\ContAI\Analysis` (`research` branch) — but this repo should be self-sufficient for report-writing; you shouldn't need to go back there.

---

**Ready to start? Next session, paste the above and say: "Let's write the technical report draft."**

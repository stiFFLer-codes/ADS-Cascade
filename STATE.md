# STATE — ADS-Cascade Invoice/Receipt Classification

> **Read this first.** Living project state for cheap session handoffs.
> Pointer-based on purpose — it links canonical docs, it does not copy them.
>
> `Last updated: 2026-08-19` · **Current phase: Phase 1 (data engineering) and Phase 2 (receipt
> cascade demo) COMPLETE; repo published + archived on Zenodo (v1.0.0, DOI
> 10.5281/zenodo.21644208); Experiment 1 manuscript FINALIZED as a release candidate
> (`manuscript/main.tex`, through Phase E7.9) — see `research/RESEARCH_GPS.md` for the detailed
> manuscript-phase history. arXiv submission has not yet happened.**

---

## ▶ Resume in a new session

Paste this into a fresh session to continue with full context:

> I'm continuing the **ADS-Cascade** project. Engineering (Phase 1 D406 pipeline, Phase 2 demo,
> public export, GitHub + Zenodo publication) is **complete**. The **Experiment 1 manuscript**
> (`manuscript/main.tex`) is also **complete** — it went through a full audited drafting sequence
> (Phase A research audit → literature verification → contribution lock → experiment →
> manuscript draft → E4 adversarial audit → E5 refinement/citation/reproducibility passes → E6
> final review → E7 release-candidate hardening), finalized at commit `464aa1b` ("Phase E7.9:
> finalize final manuscript release candidate"). Full phase-by-phase detail and the audit trail
> live in `research/` (see `research/RESEARCH_GPS.md` as the entry point; note it was last updated
> mid-sequence and its own "CURRENT GATE" section is stale — trust `git log` and this file over it
> for current status). **The next real step, if resumed, is preparing and submitting the arXiv
> version** (category selection, source-package assembly, cross-linking Zenodo/ORCID/Scholar) —
> not yet started. **What I want to do next: <fill in>.**

---

## Where we are

Phase 1 (data engineering), Phase 2 (receipt-classification demo), and the Experiment 1 manuscript
are all **complete and committed**. The interactive stakeholder demo is built
(`docs/demo/index.html`). No open implementation work remains for any of the three tracks; what's
left is publication logistics (arXiv submission) and optional repository-hygiene polish.

## Done

- **Phase 1 — Data Engineering pipeline.** 6 scripts (`scripts/`), stdlib-only.
  296,648 invoice lines · 169 companies · weighted ADS 0.847 · 91.2% products
  deterministic · 76,843 product→account mappings.
  → `reports/phase1_final_report.md`
- **Phase 2 — Solution Architecture + cascade demo.** 17 docs (`architecture/`): scope,
  requirements, NFRs, domain model, services, event workflow, data schema, confidence cascade,
  AI orchestration, API contracts, sequences, security, observability, cost, plus 16 ADRs and 20
  open questions. Cascade validated end-to-end: Tier-1 held-out accuracy 98.4% @ 42% coverage;
  full-cascade auto-apply 42.8% coverage @ 98.1% accuracy.
  → `architecture/00_SCOPE.md`, `docs/demo/index.html`
- **Public research export + synthetic reproduction (2026-07-28).**
  `scripts/00_generate_synthetic.py` generates synthetic companies/products/invoice lines from
  documented target distributions (no real data read); the full pipeline reproduces the same
  qualitative structure on synthetic data, including one documented architecture-decision flip
  (R3) at smaller scale. Real data, real-derived intermediate files, and real-named worked
  examples were stripped or anonymized. → `METHODOLOGY.md`
- **GitHub + Zenodo publication (2026-07-28).** Repo renamed `stiFFLer-codes/ADS-Cascade`,
  `TECHNICAL_REPORT.md` written, `LICENSE` (MIT) and `CITATION.cff` (ORCID-linked) added,
  GitHub-Zenodo integration connected, `v1.0.0` release published, DOI
  `10.5281/zenodo.21644208` minted.
- **Experiment 1 — controlled mechanism-selection study, through manuscript finalization
  (2026-08-11 → 2026-08-19).** Research audit → literature verification → contribution lock
  (Formulation #2 adopted) → 240-condition frozen experiment
  (`data/outputs/experiments/exp1/final/`) → post-hoc analysis → first complete manuscript draft
  → independent adversarial audit → readability pass → citation/claim audit → public
  reproducibility audit → figure generation → final prose polish → final adversarial review →
  release-candidate hardening (author metadata, AI-assistance disclosure, bibliography
  corrections, release-boundary fixes, editorial refinement). Finalized at `464aa1b`.
  Full audit trail: `research/` (70+ dated audit/evidence documents); phase-by-phase log:
  `research/RESEARCH_GPS.md`.

## Next

**arXiv submission of `manuscript/main.tex`** — not yet started. Per
`research/RESEARCH_GPS.md`'s Gate 6 (public release), remaining items are: pick an arXiv category,
assemble the source package, confirm Google Scholar indexing once live, cross-link the Zenodo
record / GitHub README / ORCID profile to the arXiv identifier. No further scientific or drafting
work is planned — the manuscript is content-frozen at the E7.9 release candidate.

## How to run / resume (any session or AI)

All offline except two cached API layers. Reproducible without keys (caches committed).
```
python scripts/phase2/p2_01_build_kb.py        # KB from Phase 1 mappings
python scripts/phase2/p2_02_classify_eval.py   # held-out cascade eval (Tier-1 98.4%)
python scripts/phase2/p2_03_extract.py         # Textract OCR (idempotent; 0 new calls if cached)
python scripts/phase2/p2_05_end_to_end.py      # 10 receipts -> per-line tier + candidates
python scripts/phase2/p2_06_llm_tail.py        # LLM re-rank on review tail (needs GROQ_API_KEY)
python scripts/phase2/test_cascade.py          # fast self-checks
python scripts/experiments/exp1/run_final.py   # Experiment 1 (single command, no keys)
python scripts/experiments/exp1/analyze_posthoc.py --demo   # fast self-check of Exp. 1 stats
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
- **arXiv category and submission logistics** — not yet decided (see "Next" above).

## Where things live

| What | Path |
|---|---|
| Pipeline scripts | `scripts/` |
| Pipeline outputs (ground truth) | `data/outputs/` |
| Phase 2 design (source of truth) | `architecture/` |
| Phase 1 reports | `reports/` |
| Entry / navigation docs | `docs/` (start at `docs/INDEX.md`) |
| Repo map | `README.md` |
| Working rules | `AGENTS.md` |
| Experiment 1 manuscript | `manuscript/main.tex`, `manuscript/references.bib` |
| Experiment 1 research/audit trail | `research/` (see `research/RESEARCH_GPS.md` for the phase log) |
| Prior arXiv-prep execution plan (historical, superseded by the actual E-phase sequence in `research/`) | `ROADMAP.md` |

## Update protocol

At the **end of each session**, edit only *Where we are*, *Next*, *Done*, and the
`Last updated` date. Update *Resume in a new session* only when the concrete next step changes;
its docs-to-read list is stable scaffolding, not per-session content. Keep it pointer-based, never
copy architecture prose in here.

This is the single committed handoff file. `CLAUDE.md` auto-loads at the start of every session
and points here; nothing else should carry "current status" prose, to avoid the drift a second
status file caused before (`CONTINUATION_PROMPT.md`, removed during the public-cleanup pass). This
file is the committed counterpart to Claude Code's private per-machine memory
(`.claude/.../memory/MEMORY.md`), which is local-only and not portable across machines or clones.
Personal, non-repository planning (application prep, career notes, etc.) does not belong in this
file — it should stay in private, non-tracked notes.

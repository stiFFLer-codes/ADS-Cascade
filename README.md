# ADS-Cascade

A data-driven method for deciding how much of a classification problem actually needs a model.

Most document-classification systems start by picking a model, then scale it up when accuracy
disappoints. This project starts by measuring the data: how consistently does history already
answer the question being asked, before any model is trained? That measurement, the **Automated
Determinism Score (ADS)**, is computed first and it decides the architecture. If most items already
have one dominant, historically consistent answer, the system's job for those items is retrieval,
not inference, and the architecture should reflect that: a rules-first, per-company knowledge base
with hybrid retrieval, not a single learned classifier, with an LLM used only as a re-ranker over
retrieved candidates for the measured minority tail.

The method is validated end to end on Romanian fiscal documents: D406 (SAF-T) invoice filings,
extended to photographed retail receipts. Nothing in the ADS metric or the cascade design is
specific to that domain or that country. Romania is the case study, not the boundary of the idea.

**The paper:** [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md) covers the problem, the method, the
evaluation (real and synthetic), and an honest limitations section, including where the method has
and hasn't been tested.

**The full method:** [`METHODOLOGY.md`](METHODOLOGY.md) explains what is public in this repository
versus what stays confidential, and gives the complete real-versus-synthetic comparison the report
draws its numbers from.

---

## Start here

1. Read the technical report: [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md)
2. Open the interactive demo: [`docs/demo/index.html`](docs/demo/index.html). Double-click the file;
   it is self-contained and works offline, no install required. It walks through the real
   (anonymized) production trace described below.
3. Current status and how to run the pipeline: [`STATE.md`](STATE.md)
4. Full navigation: [`docs/INDEX.md`](docs/INDEX.md)
5. The separate arXiv-track controlled experiment (mechanism selection, not the pipeline above): see
   "Experiment 1" below

---

## What's inside

| Phase | What it does | Result (cited from production) |
|---|---|---|
| **Phase 1, Data Engineering** | Six-script pipeline that mines D406 (SAF-T) XML filings to compute per-product determinism | 296,648 invoice lines, 76,843 product-to-account mappings, 91.2% of products deterministic |
| **Phase 2, Receipt Intelligence** | Photo to OCR to structuring/validation to a rules-first four-tier cascade to retrieval to LLM re-ranking | Tier-1 held-out accuracy 98.4%; full-cascade auto-apply 42.8% coverage at 98.1% accuracy |

The core idea: most classification is repetition, not judgment. A per-company knowledge base
answers the majority of cases with no AI involved, a retrieval layer bridges formatting gaps in the
remaining cases, and an LLM (behind a swappable adapter) is consulted only for what is genuinely
new. Every number above traces to a script and an artifact in this repository; nothing is asserted
without a source.

### Real results versus synthetic reproduction

Two different things live in this repository, for two different reasons:

- The interactive demo (`docs/demo/index.html`) shows the real production trace: ten actual
  photographed receipts, OCR'd and classified, with vendor names and tax IDs anonymized. Its
  numbers are cited from a confidential engagement and are not recomputed here.
- The runnable pipeline (`scripts/`, `data/outputs/`) uses a from-scratch synthetic generator
  (`scripts/00_generate_synthetic.py`), so anyone can reproduce the methodology end to end offline,
  at no cost, with no client data and no API keys. `METHODOLOGY.md` has the full real-versus-synthetic
  comparison table, including one architecture decision (R3) that flips at the smaller synthetic
  scale. That result is reported as a threshold-sensitivity finding, not tuned away to force
  agreement.

---

## Experiment 1 (arXiv-track manuscript)

A separate, controlled synthetic experiment — not the Phase 1/2 engineering pipeline above — tests
whether historical decision consistency predicts which classification mechanism wins, not just how
accurate each one is. It's written up as its own paper: [`manuscript/main.tex`](manuscript/main.tex).

| What | Where |
|---|---|
| Final experiment script (single command, no client data, no API keys) | `python scripts/experiments/exp1/run_final.py` |
| Frozen configuration (targets, seeds, thresholds) | `data/outputs/experiments/exp1/final/final_frozen_config.json` |
| Seed manifest (20 seeds × 6 targets × 2 lexical conditions = 240) | `data/outputs/experiments/exp1/final/final_seed_manifest.csv` |
| Frozen raw results (the manuscript's primary evidence artifact) | `data/outputs/experiments/exp1/final/final_condition_results.csv` |
| Headline statistics (agreement rate, Wilson CI, binomial p-value) regenerated from that CSV | `python scripts/experiments/exp1/analyze_posthoc.py` (or `--demo` for a fast self-check) |
| Figure generation (draft; requires `matplotlib`, see `requirements.txt`) | `manuscript/figures/generate_figures.py` |
| Manuscript source | `manuscript/main.tex`, `manuscript/references.bib` |

Requires Python 3.11+ (the one version floor enforced anywhere in this repository, via
`prerun_check.py`) and `rapidfuzz` (in `requirements.txt`). No client data, no API keys, no cost.

---

## Folder map

```
TECHNICAL_REPORT.md  the paper: problem, method, evaluation, limitations
METHODOLOGY.md        what is public versus confidential, and the real-vs-synthetic comparison
manuscript/            the Experiment 1 paper: main.tex, references.bib, figures/
docs/                  demo/, INDEX.md, PHASE2_PLAN.md, Context.md, Phases.md
STATE.md               living status, how to run, resume prompt
architecture/          Phase 2 solution architecture: 17 docs, 16 ADRs, open questions
scripts/               Phase 1 pipeline (01-04), Phase 2 (phase2/: p2_01...p2_06 plus p2lib/),
                       and Experiment 1 (experiments/exp1/ -- see "Experiment 1" section above)
reports/               Phase 1 findings and architecture decision report
data/                  source-of-truth manifest plus outputs/ (synthetic results, incl. phase2/
                       and experiments/exp1/, the Experiment 1 frozen evidence)
research/              Experiment 1 research/audit trail (evidence review, contribution lock,
                       manuscript drafting checkpoints) -- internal working documents, not needed
                       to reproduce the results, only to see how the manuscript's claims were derived
config/  utils/        shared settings and helpers
AGENTS.md              working conventions
requirements.txt       Python dependencies (standard library first; pandas, requests, tqdm, rapidfuzz)
```

---

## How to cite

This repository is archived on Zenodo with a citable DOI:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21644208.svg)](https://doi.org/10.5281/zenodo.21644208)

See [`CITATION.cff`](CITATION.cff) for structured citation metadata (GitHub renders a "Cite this
repository" button from it automatically). Licensed under [MIT](LICENSE).

---

## Honest framing

This is a validated prototype, not a shipped product. OCR quality is demonstrated on ten real
sample receipts in the cited production trace as qualitative validation, not as a hand-labeled OCR
benchmark. The AWS Textract and Groq LLM calls in that original run used test accounts, and every
response was cached, so the demo reproduces at no cost with no keys required. This repository's own
runnable pipeline validates the same methodology on synthetic data only. Production components not
covered here, such as WhatsApp intake, a review UI, and ERP export, are awaiting business decisions
and are tracked in [`architecture/OPEN_QUESTIONS.md`](architecture/OPEN_QUESTIONS.md).

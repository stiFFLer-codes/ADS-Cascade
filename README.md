# ADS-Cascade

ADS-Cascade is a research project on measuring historical decision-consistency in data before
choosing a classification architecture, developed alongside a production accounting-automation
engineering system for Romanian fiscal-document classification.

This repository contains two related but distinct things:

1. **[Experiment 1](#experiment-1-research-paper)** — a controlled, reproducible research paper
   testing a precise version of that idea (below).
2. **[The broader ADS-Cascade engineering project](#broader-ads-cascade-engineering-project)** —
   the Phase 1/2 data pipeline and receipt-classification cascade that motivated the research
   question.

The engineering project's design rationale — *measure determinism first, then let it decide the
architecture* — is the motivation for Experiment 1's research question. It is a production case
study, not something Experiment 1 itself experimentally establishes; see "Research question and
key finding" below for what the controlled experiment actually found.

---

## Experiment 1 Research Paper

**"Historical Consistency Predicts Mechanism Accuracy, Not Mechanism Ranking: Evidence from a
Controlled Synthetic Study"**
Maitreya Sapariya, Independent Researcher ([ORCID 0009-0003-9346-3775](https://orcid.org/0009-0003-9346-3775))

- **Status:** manuscript finalized (release candidate); not yet submitted to arXiv.
- **Manuscript source:** [`manuscript/main.tex`](manuscript/main.tex), [`manuscript/references.bib`](manuscript/references.bib)
- **Figures:** [`manuscript/figures/`](manuscript/figures/)

This is the paper this repository exists to support — a separate, controlled synthetic
experiment, distinct from the Phase 1/2 engineering pipeline described further down.

---

## Research question and key finding

The paper asks whether historical decision consistency, measured before deployment, can be used
to select between qualitatively different classification mechanisms (exact-match rules vs. fuzzy
retrieval). A 240-condition synthetic factorial experiment (20 seeds × 6 consistency targets × 2
lexical conditions) finds that realized historical consistency is strongly correlated with each
mechanism's own accuracy (Pearson $r>0.9$), but does not reliably predict *which* mechanism wins:
a frozen, pre-specified consistency threshold agrees with the empirically best mechanism in 100%
of comparisons in one consistency band and 0% in another, because the actual winner instead tracks
a separately controlled lexical-noise condition. The paper concludes that a design-time selector
built on historical consistency alone should not be used to predict which mechanism wins — the
manuscript's central hypothesis (H1) is reported as **partially supported**, not confirmed or
rejected outright.

---

## Reproduce Experiment 1

These are the exact artifacts required to reproduce the controlled experiment above, end to end,
offline, with no client data and no API keys:

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

## Broader ADS-Cascade Engineering Project

The research question above is motivated by a two-phase accounting-automation engineering
project, validated end to end on Romanian fiscal documents: D406 (SAF-T) invoice filings,
extended to photographed retail receipts. Nothing in the ADS metric or the cascade design is
specific to that domain or that country — Romania is the case study, not the boundary of the
idea. This engineering work is described in full in [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md)
— the **Phase 1/2 Engineering Report** — a separate, related document from the Experiment 1
Research Paper above: it covers the problem, method, evaluation (real and synthetic), and an
honest limitations section.

[`METHODOLOGY.md`](METHODOLOGY.md) explains what is public in this repository versus what stays
confidential, and gives the complete real-versus-synthetic comparison the report draws its
numbers from.

| Phase | What it does | Result (cited from production) |
|---|---|---|
| **Phase 1, Data Engineering** | Six-script pipeline that mines D406 (SAF-T) XML filings to compute per-product determinism | 296,648 invoice lines, 76,843 product-to-account mappings, 91.2% of products deterministic |
| **Phase 2, Receipt Intelligence** | Photo to OCR to structuring/validation to a rules-first four-tier cascade to retrieval to LLM re-ranking | Tier-1 held-out accuracy 98.4%; full-cascade auto-apply 42.8% coverage at 98.1% accuracy |

The core idea: most classification is repetition, not judgment. A per-company knowledge base
answers the majority of cases with no AI involved, a retrieval layer bridges formatting gaps in
the remaining cases, and an LLM (behind a swappable adapter) is consulted only for what is
genuinely new. Every number above traces to a script and an artifact in this repository; nothing
is asserted without a source.

Interactive demo: [`docs/demo/index.html`](docs/demo/index.html). Double-click the file; it is
self-contained and works offline, no install required. It walks through the real (anonymized)
production trace described below.

Current status and how to run the pipeline: [`STATE.md`](STATE.md). Full navigation:
[`docs/INDEX.md`](docs/INDEX.md).

---

## Real results versus synthetic reproduction

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

## Repository map

```
manuscript/            Experiment 1 Research Paper: main.tex, references.bib, figures/
TECHNICAL_REPORT.md    Phase 1/2 Engineering Report: problem, method, evaluation, limitations
METHODOLOGY.md         what is public versus confidential, and the real-vs-synthetic comparison
docs/                   demo/, INDEX.md, PHASE2_PLAN.md, Context.md, Phases.md
STATE.md               living status, how to run, resume prompt
architecture/          Phase 2 solution architecture: 17 docs, 16 ADRs, open questions
scripts/               Phase 1 pipeline (01-04), Phase 2 (phase2/: p2_01...p2_06 plus p2lib/),
                       and Experiment 1 (experiments/exp1/ -- see "Reproduce Experiment 1" above)
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

## Citation

### Repository / software citation

This repository is archived on Zenodo with a citable DOI, identifying this repository/software
release:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21644208.svg)](https://doi.org/10.5281/zenodo.21644208)

See [`CITATION.cff`](CITATION.cff) for structured citation metadata (GitHub renders a "Cite this
repository" button from it automatically).

### Research paper citation

The Experiment 1 Research Paper does not yet have an independent arXiv identifier or other
citable record separate from this repository — it has not yet been submitted. Until then, cite
the manuscript directly (title, author, and repository URL above); this section will be updated
with an arXiv identifier once one exists.

---

## License

Licensed under [MIT](LICENSE).

---

## Honest framing / scope

This is a validated prototype, not a shipped product. OCR quality is demonstrated on ten real
sample receipts in the cited production trace as qualitative validation, not as a hand-labeled OCR
benchmark. The AWS Textract and Groq LLM calls in that original run used test accounts, and every
response was cached, so the demo reproduces at no cost with no keys required. This repository's own
runnable pipeline validates the same methodology on synthetic data only. Production components not
covered here, such as WhatsApp intake, a review UI, and ERP export, are awaiting business decisions
and are tracked in [`architecture/OPEN_QUESTIONS.md`](architecture/OPEN_QUESTIONS.md).

Experiment 1's own scope note: the mechanism-selection finding above is scoped to one synthetic
generator, one lexical-perturbation model, and one motivating (non-evidentiary) production case
study — it is not a deployment or generalization claim.

# Phase A Closure — Final Evidence Audit Summary

> Output of the Final Phase-A Evidence Closure Audit (2026-08-11), the fourth and final pass of
> Phase A. Read `research/final_numbers_audit.csv` for the full per-claim table (47 rows),
> `research/MANUSCRIPT_UPDATE_QUEUE.md` for the manuscript-facing punch list, and
> `research/EVIDENCE_BASELINE.md` for the canonical-values reference. This document is the summary.

---

## 1. Scope audited

Every percentage, decimal metric, count, dataset size, accuracy, coverage, determinism value, ADS
value, threshold, architecture decision, runtime statistic, and Phase 1/Phase 2 metric appearing in
`TECHNICAL_REPORT.md` (all sections: Abstract, §1–§6, Reproducibility) — an independent, line-by-line
re-extraction, not a re-use of the earlier `claim_evidence_matrix.csv`'s 29 rows (though every item
from that matrix is cross-referenced where it overlaps). Cross-checked against
`research/claim_evidence_matrix.csv`, `research/EVIDENCE_BASELINE.md`, `data_verification_audit.md`,
`reports/phase1_final_report.md`, the currently-committed generated artifacts under
`data/outputs/intelligence/` and `data/outputs/phase2/`, and the generating scripts
(`03_5_dataset_intelligence.py`, `04_architecture_decision.py`, `scripts/phase2/p2lib/confidence.py`,
`scripts/phase2/p2lib/cascade.py`), read live this pass. `TECHNICAL_REPORT.md`, `README.md`, and
`METHODOLOGY.md` were **read only, never modified**.

## 2. Number of quantitative claims checked

**47** distinct claims/claim-clusters (`F01`–`F47` in `research/final_numbers_audit.csv`).

## 3. Matches

**32 of 47** claims MATCH their canonical source artifact exactly (including two — F10, F11 — that
carry the pre-existing "likely understated, unverified" production caveat from Note 1 of
`EVIDENCE_BASELINE.md`, and one — F22 — that is a qualitative/illustrative claim, not a numeric one).

## 4. Rounding-only differences

**3** claims (F17, F25, F40) — all prose restatements ("about 30%," "roughly a third," "about one
point") that round a canonical number in a way a careful reader would accept. None flagged for
correction.

## 5. Definition differences

**2** items:
- **F13** (carried forward from finding A4, not new this pass) — R3's manuscript description states
  only the ≥90% cutoff; the live code implements a three-band decision. Value is correct, framing is
  incomplete.
- **F31** (new this pass) — §3.2's "Purchase / sale split" table row compares a production figure
  computed at the **invoice** level (73.9%/26.1%) against a synthetic figure computed at the
  **line** level (73.5%/26.5%) in the same row. The true line-level production split (73.7%/26.3%)
  is available in the same source document but not the one cited. Low severity (~0.2 point gap) but
  a genuine unit mismatch.

## 6. Stale manuscript values

**6** claim-rows, reducing to **2 distinct root causes**:

- **A5 aftermath (F27, F28, F34, F39)** — §3.2's synthetic ADS/deterministic-share figures
  (0.809/0.931/84.1%) and §3.3's restatement of 84.1% are stale relative to the corrected pipeline
  (canonical: 0.903/0.960/87.6%). Already known and fixed in the code/data (`research/a5_correction_analysis.md`);
  only the manuscript prose hasn't been updated yet. **NUMERIC UPDATE**, queued as N1/N2.
- **New this pass — A6 (F19, F20)** — §2.4's T2 tier description (fuzzy match auto-apply at
  similarity ≥0.85; company-rule floor of 0.80 ADS) no longer matches the shipped
  `scripts/phase2/p2lib/confidence.py`/`cascade.py` (`T2_ADS_LOW=0.90`; `FUZZY_AUTO_APPLY=False`
  makes fuzzy-auto-apply dead code — all fuzzy matches now route to Tier 3). This is a
  **documentation-lag finding, not a code bug** — the code is internally consistent and was
  deliberately tightened after a Stage-A calibration run found the original thresholds unsafe.
  Neither the manuscript nor `architecture/08_CONFIDENCE_CASCADE.md` was updated when the code was.
  **INTERPRETATION UPDATE** (a structural claim about system behavior, not just a digit), queued as
  I2. This is the most consequential finding of this closure pass.

Two further items are also flagged as **UNSUPPORTED** (no traceable generating artifact anywhere in
this repository — new discoveries this pass, not carried forward from A1–A5):

- **F42** (§4): "0.76–0.80 across synthetic seeds" — no multi-seed sweep exists in this repository;
  only a single seed=42 run has ever been executed. Self-contradicts §4's own later "single-seed...
  not swept" bullet.
- **F45** (§6): "under 10% of production volume" (LLM-touch share) — no occurrence-weighted LLM-share
  artifact exists in this repository; the closest real number (8.8%) is a product-count statistic,
  and using it as a "volume" figure repeats exactly the weighted/unweighted conflation §2.2 warns
  against.

## 7. Unresolved items

- **~55,394** (mapping count) — still formally **UNRESOLVED**, unchanged from the prior pass.
  Exhaustive provenance search found no trace anywhere in this repository or its git history. This
  cannot be closed by further audit — it needs the author to check an external source (private
  client repo or session notes), or to approve dropping the framing. Not a blocker: 76,843 stands as
  independently, fully verified canonical regardless.
- **F23** (63,048 test-line count) — minor, new this pass. The stated 80/20 split implies a base
  population (315,240) that doesn't match any total documented in this repository. Not proven wrong,
  just insufficiently documented here; low priority.

## 8. Canonical evidence status

`research/EVIDENCE_BASELINE.md` was reviewed and updated in this pass to close two completeness
gaps found during the audit: (1) a fourth, previously-undocumented "deterministic %" figure
(`kb_summary.json`'s 96.4%, on a company-product-rule basis) was added to the "not canonical" table;
(2) the "Four-tier cascade thresholds" row was completed with the four constants (`T2_ADS_LOW`,
`T2_MIN_EVIDENCE`, `T2_GLOBAL_ADS_LOW`, `FUZZY_AUTO_APPLY`) the original row omitted, with a caveat
explaining the A6 finding. Every metric with more than one legitimate definition — weighted vs.
unweighted ADS, production vs. synthetic, and the now **four** distinct "determinism/cross-company"
figures (0.7632 cited / 0.7756 report-headline / 0.9746 average-company / 96.4% KB-rule-basis) — is
named explicitly, with exactly one value marked canonical per definition. No metric was collapsed
into a single ambiguous number.

## 9. Is Phase A officially CLOSED?

**Yes, with two explicitly-flagged carve-outs.** Every quantitative claim in `TECHNICAL_REPORT.md`
has been traced to a source, classified, and cross-checked; every discrepancy found (old and new)
has been documented rather than silently reconciled; the evidence baseline is internally consistent
and complete. The two items that remain open — `~55,394`'s provenance, and the manuscript-text
updates queued in `research/MANUSCRIPT_UPDATE_QUEUE.md` — are not audit gaps: the first is
permanently unresolvable from this repository alone, and the second is manuscript-editing work
explicitly reserved for Phase E, not further evidence work. No further audit pass is needed before
those get addressed. **Phase A's evidence-integrity objective — CLAIM → EVIDENCE → ARTIFACT →
GENERATING CODE, with no unexplained contradiction — is met.**

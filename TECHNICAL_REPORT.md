# Rules Before Models: A Data-Driven Architecture for Accounting Classification of Fiscal Documents

**Maitreya Sapariya**
Draft technical report — companion to the public repository at [this project's root](.). Methodology,
code, and architecture decision records referenced below are public in this repository; the underlying
client data is not (see *Reproducibility* and `METHODOLOGY.md`).

---

## Abstract

Automatically assigning general-ledger (GL) accounts to invoice and receipt line items is usually
approached as a classification problem to be solved with progressively larger models. We argue the
model choice should be a *consequence* of measured data properties, not a starting assumption, and
present a two-phase pipeline that makes this measurement explicit before any learned component is
built. Phase 1 mines 296,648 invoice lines from 169 companies' Romanian D406 (SAF-T) fiscal filings
and computes an **Automated Determinism Score (ADS)** per product — how consistently a product maps
to one account. The data shows 91.2% of products are deterministic (ADS > 0.95) and cross-company
agreement is only 0.695, which together dictate the architecture: a rules-first, per-company
knowledge base with global fallback (HYBRID retrieval), not a single learned classifier. Phase 2
operationalizes this as a **four-tier confidence cascade** — deterministic lookup, fuzzy/embedding
match, LLM-assisted review, and manual entry that becomes training data — validated end-to-end on
real OCR'd receipts (AWS Textract) with an LLM (Groq/Llama-3.3-70B) used strictly as a re-ranker over
retrieved candidates, never as an autonomous classifier. Tier-1 deterministic lookup reaches 98.4%
held-out accuracy at 42% coverage; the full cascade reaches 98.1% accuracy at 42.8% auto-apply
coverage, routing the rest to human review by design. Because the underlying data is confidential,
we release a synthetic reproduction of the entire pipeline — generator, architecture-decision logic,
and cascade — that independently recovers the same qualitative structure, including a documented
boundary case where one architecture decision flips at smaller scale. We report this discrepancy
rather than tune it away, because it is itself evidence about how close the real system sits to its
own decision threshold.

---

## 1. Introduction

Mid-market accounting automation vendors converge on the same pitch: point a large language model
at a document and ask it to name the account. This works, and it is also the most expensive way to
answer a question that, for the majority of line items, has already been answered — by the same
company, for the same product, dozens of times before. The engineering question this report answers
is not "can an LLM classify this receipt line" (it can) but **"where in the pipeline does an LLM
earn its cost,"** and the answer turns out to be measurable from the data itself, before any model
is trained or any API is called.

The domain is Romanian fiscal compliance: companies file **D406** declarations (the Romanian SAF-T
standard) in XML, and — the extension this project adds — capture retail purchase **receipts**
(paper, photographed) that must be OCR'd, validated, and booked to the same chart of accounts. Both
document types terminate in the same decision: *which GL account, at what VAT rate, does this line
item belong to.* The dataset is real production data from a confidential client engagement; this
report and the accompanying public repository describe the method in full and validate it two ways —
against the real results (cited, not reproduced) and against an independently-generated synthetic
dataset that anyone can run offline with no client data, no API keys, and no cost.

**Contributions:**

1. **ADS**, a determinism metric computed per product (not per model) that turns "is this dataset
   learnable, and by what" into a measured quantity rather than an assumption, and a decision
   procedure (`04_architecture_decision.py`) that maps ADS and three companion statistics onto five
   named architecture decisions with explicit, versioned thresholds.
2. A **four-tier confidence cascade** that keeps OCR-extraction confidence and classification
   confidence as two independent signals (never blended into one score), and that treats an LLM
   call as a *re-ranker over retrieved candidates*, not a free-standing predictor — the LLM never
   sees a blank slate.
3. An **honest two-track evaluation**: production numbers cited from a confidential dataset, plus a
   from-scratch synthetic reproduction released publicly, with the two tracks' agreements and
   disagreements both reported — including one architecture decision (R3) that is close enough to
   its threshold to flip at smaller scale, which we treat as a finding about threshold sensitivity,
   not a bug to be hidden.

---

## 2. Method

### 2.1 Data engineering pipeline (Phase 1)

Six idempotent, stdlib-first Python scripts turn 1,020 raw D406 XML filings across 201 inventoried
companies (169 with usable invoice data) into a clean training table:

| Stage | Script | Job |
|---|---|---|
| 1 | Inventory | Catalog companies, detect duplicate filings |
| 1.5 | Download/extract/validate | Retry-safe, atomic-write, resumable fetch of XMLs (100% validation pass rate on 1,020 files) |
| 2 | GL extraction | Per-company chart of accounts (154,068 records, 201 companies) |
| 3 | Invoice line extraction | Parses 5+ historical schema variants into one row-per-line table: product text, account, direction (purchase/sale), VAT, tax code |
| 3.5 | Dataset intelligence | Computes ADS, cross-company consistency, VAT stability, missingness — see §2.2 |
| 4 | Architecture decision | Thresholds the §3.5 statistics into five named architecture calls — see §2.3 |

The result is 296,648 invoice lines, 47,306 normalized unique products, and 76,843 distinct
`(company, product) → account` mappings — the knowledge base every downstream decision is built on.
Two data-quality facts shape everything downstream: `line_amount` and `warehouse_id` are **100%
absent** from the D406 schema (they are not optional fields the extractor missed — the schema simply
does not carry them), so classification cannot use monetary amount as a feature at all; and `vat_percent`
is missing on 4.05% of lines, which is why VAT is used as a *secondary* re-ranking signal rather than
a required field.

### 2.2 The Automated Determinism Score (ADS)

For a normalized product $p$, let $a_1, \dots, a_k$ be the accounts it has historically been booked
to, with counts $c_1, \dots, c_k$. ADS is the empirical probability that a random occurrence of $p$
was booked to its modal account:

$$\text{ADS}(p) = \frac{\max_i c_i}{\sum_i c_i}$$

Two aggregates matter and are reported separately, deliberately:

- **Unweighted ADS** (mean of $\text{ADS}(p)$ over distinct products) — measures the *catalog's*
  intrinsic learnability.
- **Weighted ADS** (mean weighted by occurrence count) — measures what a random *line item* actually
  experiences.

Production measurement: unweighted 0.964, weighted 0.847 — a 0.117 gap. The gap is itself a finding:
it means the products that occur *most often* are disproportionately the ambiguous ones (e.g. generic
line items like "avans" or "prestari servicii" that map to 50+ accounts depending on context), so a
single scalar accuracy number computed the wrong way silently overstates how solved the problem is.
Reporting only the unweighted number would be a form of survivorship bias toward rare, easy products.

91.2% of products clear the ADS > 0.95 "deterministic" bar; only 1.1% are genuinely ambiguous
(ADS < 0.50). This shapes the entire cascade design in §2.4: if 9 in 10 products already have one
correct answer sitting in history, the system's job for those 9 is *retrieval*, not *inference*.

### 2.3 Evidence-based architecture decisions

`04_architecture_decision.py` takes the Phase 1 statistics and applies **named, versioned
thresholds** — not tuned per dataset, recorded on every run for audit — to five architecture
questions:

| Decision | Statistic | Threshold | Production result |
|---|---|---|---|
| R1 — Retrieval strategy | weighted ADS 0.847, cross-company consistency 0.695 | ≥0.90 global / ≥0.75 hybrid | **HYBRID** |
| R3 — Model complexity | deterministic products 91.2% | ≥90% → rules-first | **RULES_FIRST** |
| R4 — VAT role | single-rate-stable products 94.5% | ≥95% primary / ≥70% secondary | **SECONDARY_FEATURE** |
| R5 — Warehouse feature | missingness 100.0% | ≥90% → drop | **DROP** |

Cross-company consistency (0.695, measured over 2,696 products booked by more than one company)
is the decision that rules out a global-only classifier: the same product is legitimately booked to
different accounts by different companies often enough (about 30% of the time on shared products)
that a model trained across all companies would be measurably wrong on a meaningful slice of
predictions. This is why the knowledge base is **hybrid**: a per-company override layer that always
wins, backed by a global layer for cold-start and cross-company priors (ADR-001).

### 2.4 The four-tier confidence cascade (Phase 2)

The cascade is the runtime consumer of the Phase 1 distribution. Two confidences are computed and
surfaced **independently and never blended**: `extraction_confidence` (did OCR read the paper
correctly — line-sum reconciliation against the printed total, field-level confidence from the OCR
provider) gates entry to the cascade; `classification_confidence` (do we know which account this
product belongs to) determines the tier. A crisp photo of an ambiguous product and a blurry photo of
a deterministic product are opposite failure modes needing opposite remediation, so collapsing them
into one score was explicitly rejected (ADR-007).

Classification order is fixed (RULES_FIRST, ADR-002): alias resolution → per-company deterministic
lookup → global deterministic lookup (strict, near-unanimous only) → embedding/fuzzy fallback → VAT
re-ranking (secondary signal, never elimination) → chart-of-accounts sanity screen → LLM inference,
consulted **only** when the first five stages produce no confident candidate.

| Tier | Trigger | Action |
|---|---|---|
| **T1** | Company rule ADS ≥ 0.95, evidence ≥ 3 (or a fresh human correction, or a near-unanimous global pattern with ≥5 companies agreeing) | Auto-apply, no flag |
| **T2** | Fuzzy/embedding match (similarity ≥ 0.85) or a weaker company rule (0.80–0.95 ADS) corroborated by VAT | Auto-apply, flagged for a sampled spot-check |
| **T3** | Similarity < 0.85, candidates disagree, or an LLM was consulted | Routed to human review; LLM proposals are **never** auto-applied |
| **T4** | No candidate above the review floor (0.50) | Manual entry — and this is the knowledge base's growth mechanism, not a failure state: every T4 resolution permanently promotes that product to T1 for that company |

The critical architectural choice is in T3: an LLM call, when it happens, is fed the cascade's
already-retrieved candidate accounts and asked to **re-rank precedent**, never asked to classify from
a blank product string. In the end-to-end trace on 10 real OCR'd receipts (§3.1), this changed the
LLM's behavior from defaulting to one generic account for everything to correctly distinguishing
fuel (→6022), discounts (→609), tobacco (→371), and road tax (→628) — because it was ranking real
candidates instead of guessing from a product name alone.

### 2.5 Retrieval and OCR extraction

The company-scoped fuzzy fallback (`p2lib/retrieval.py`) is a deliberate placeholder: lexical
similarity (`rapidfuzz`, `WRatio`) over each company's own product catalog first, global catalog
second — chosen because it is fast, dependency-light, and sufficient to demonstrate that most
"no exact precedent" cases in the cold-start trace were OCR-formatting variants of already-known
products ("rovinieta a autoturisme" → "rovinieta", 90+ fuzzy score), not genuinely new products. The
architecture document (`09_AI_ORCHESTRATION.md`) specifies this slot as replaceable by a proper
embedding/vector-DB layer; the code marks the gap explicitly (`# ponytail:` comment naming the
ceiling) rather than silently shipping a stopgap as if it were the final design. Receipt OCR uses AWS
Textract's `AnalyzeExpense`, cached per-receipt so the pipeline reproduces at $0 after the first call;
VAT bracket letters (A/B) printed per line by Romanian fiscal-device firmware are read directly from
the OCR output rather than inferred, per ADR-010.

---

## 3. Evaluation

### 3.1 Production results (cited, not reproduced in this repository)

Measured on the confidential production dataset (296,648 invoice lines, 169 companies) and on a
held-out 80/20 split of the classification cascade over 63,048 test lines:

- **Tier-1 deterministic lookup:** 98.4% accuracy at 42% coverage.
- **Full cascade auto-apply (T1+T2):** 42.8% coverage at 98.1% accuracy; the remaining 57.2% is
  routed to human review by design, not treated as a system failure.
- **End-to-end receipt trace (10 real photographed receipts, cold-start "new client" simulation):**
  before the retrieval bridge, 0 lines auto-applied, 8 landed in Tier 3, 14 in Tier 4. Adding the
  fuzzy retrieval bridge (§2.5) moved 14 of those 22 lines to Tier 3 with a concrete candidate account
  (only 2 lines remained genuinely novel) — confirming that most of the apparent cold-start problem
  was a retrieval/formatting gap, not a knowledge gap.

The overall 66.7% raw held-out accuracy figure (not restated as a headline number above) is
*pessimistic by construction*: a random train/test split makes roughly a third of test lines "cold"
(no exact precedent seen in training), which does not represent production, where the knowledge base
is seeded with full history before go-live.

### 3.2 Synthetic reproduction (this repository's own runs)

Because the production data cannot be published, this repository ships a generator
(`scripts/00_generate_synthetic.py`) that produces synthetic companies, products, and invoice lines
targeting the same documented distributions — without reading any real data — and re-runs the
identical, unmodified pipeline and cascade code end-to-end. This is the only evaluation actually
computed *in this repository*; the following table separates cited production numbers from measured
synthetic numbers:

| Metric | Production (cited, confidential) | Synthetic (this repo, `random.seed(42)`) |
|---|---|---|
| Companies / invoice lines | 169 / 296,648 | 60 / 7,523 |
| Weighted / unweighted ADS | 0.847 / 0.964 | 0.809 / 0.931 |
| Products >0.95 deterministic | 91.2% | 84.1% |
| Cross-company consistency | 0.695 | 0.763 |
| Purchase / sale split | 73.9% / 26.1% | 73.5% / 26.5% |
| VAT missing | 4.05% | 4.45% |
| R1 — Retrieval strategy | HYBRID | HYBRID ✓ |
| **R3 — Model complexity** | **RULES_FIRST** (91.2% ≥ 90%) | **EMBEDDING_PRIMARY** (84.1% < 90%) |
| R4 — VAT strategy | SECONDARY_FEATURE | SECONDARY_FEATURE ✓ |
| R5 — Warehouse | DROP | DROP ✓ |
| Cascade auto-apply (held-out) | 98.1% @ 42.8% coverage | 99.8% @ 76.2% coverage |

Four of five decisions and the qualitative shape of the ADS distribution reproduce independently on
data the generator never saw. The synthetic run's higher cascade coverage/accuracy is explained, not
celebrated: a smaller catalog (844 vs. 47,306 unique products) gives higher train/test overlap, so
more held-out lookups have direct precedent — an expected artifact of scale, not evidence the method
performs this well in production.

### 3.3 The R3 boundary case: a scale-sensitivity finding, not a bug

R3 flips between runs (RULES_FIRST at 91.2%, EMBEDDING_PRIMARY at 84.1%) because the production
figure itself sits only about one point above the 90% threshold used to make the call — it was
always a close decision, and sampling noise on lower-evidence products at the smaller synthetic scale
is enough to cross it. We report this as-observed rather than adjust the generator or the threshold
to force agreement, for two reasons: first, silently forcing agreement would defeat the purpose of an
independent reproduction; second, the flip is itself useful evidence that the 90% RULES_FIRST cutoff
is close enough to load-bearing production data that it deserves calibration against more evidence
before being treated as fixed, rather than evidence that either run is wrong.

---

## 4. Limitations

- **Validated on a single domain.** Every empirical result in this report, real and synthetic,
  comes from Romanian fiscal-document classification (D406 invoices and retail receipts). Neither
  the ADS metric nor the four-tier cascade references anything specific to Romania or to fiscal
  documents: both operate on any historical record of `(item, label)` assignments with counts.
  We expect the method to transfer to adjacent problems (expense categorization under other tax
  regimes, retail SKU-to-category mapping, medical billing code assignment) wherever a large,
  imperfectly-consistent, human-labeled history exists. That transfer is argued from the method's
  design, not measured: the pipeline has not been run against a second domain's data, and the
  specific threshold values in §2.3 (90% for RULES_FIRST, 0.75/0.90 for retrieval strategy) were
  calibrated against this domain's statistics and would need re-validation elsewhere.
- **Lexical retrieval, not embeddings.** The fuzzy fallback (§2.5) is an explicit, documented
  placeholder for the embedding/vector-DB layer specified in the architecture but not built in this
  phase. It resolves OCR-formatting variance well; it has not been evaluated against genuine semantic
  gaps (a product described in unfamiliar words with no lexical overlap to any known product).
- **Cross-company consistency has a real, measured ceiling** (0.695 in production; 0.76–0.80 across
  synthetic seeds) — this is not a data-cleaning problem to be solved away. It reflects that different
  companies' accountants make legitimately different, defensible choices for the same product, which
  is why the architecture is hybrid rather than aiming for a single global classifier that would
  "fix" the inconsistency.
- **Public validation is synthetic-only.** All accuracy numbers publicly *reproducible from this
  repository* come from generated data; the real-world numbers in §3.1 are cited from a confidential
  engagement and cannot be independently re-verified by a third party without access to that data.
  This is the same tradeoff any report built on confidential production data makes — the method is
  fully inspectable, the input data is not.
- **Single-seed synthetic run.** The synthetic table in §3.2 is one `random.seed(42)` run; a different
  seed shifts exact figures within the same qualitative shape but was not swept to produce confidence
  intervals.
- **Cascade thresholds are Phase-1-derived starting points**, not pilot-calibrated. ADR-016 records
  them as named, versioned configuration precisely so they can be recalibrated against live
  precision/recall data once a pilot runs — they are not claimed to be optimal as shipped.
- **OCR extraction quality is demonstrated qualitatively** on a small set of real receipts (structural
  validation: line-sum reconciliation against the printed total), not benchmarked against a
  hand-labeled gold set with a numeric OCR accuracy figure.

---

## 5. Related work and positioning

Commercial expense/invoice categorization (e.g., accounting-software auto-categorization features,
generic document-AI vendors) typically ships a single learned classifier — rule-based, ML, or
LLM-based — chosen up front rather than derived from a measured determinism distribution of the
target data. Retrieval-augmented LLM pipelines are common in adjacent document-processing products,
but usually treat retrieval as a prompt-construction step for the LLM rather than as the terminal
answer for the majority of cases with the LLM held in reserve for a measured minority tail. The
contribution here is not a novel model or algorithm — the fuzzy matcher, the OCR provider, and the
LLM are all off-the-shelf — but the **decision procedure that determines how much of each is needed**,
made auditable via a named-threshold decision matrix and validated by an ADS-style determinism metric
computed directly on the target dataset before any model is chosen.

---

## 6. Conclusion

Measuring a dataset's determinism before choosing an architecture turned what could have been a
model-selection debate into an evidence-based decision: 91.2% of products in this dataset already
have one dominant, historically-consistent answer, so the majority of the classification problem is
retrieval, and the LLM's job shrinks to re-ranking retrieved candidates for a measured minority tail
(under 10% of production volume) rather than classifying every line from scratch. The same pipeline,
re-run on synthetic data with the identical unmodified code, independently recovers four of five
architecture decisions and the qualitative shape of the underlying distribution — with the one
decision that doesn't reproduce identified as a genuine threshold-sensitivity finding rather than
smoothed over. We believe this evidence-first discipline — compute the determinism, let it choose
the architecture, keep the expensive component behind a measured gate, and report disagreements
instead of hiding them — generalizes beyond Romanian fiscal documents to any classification problem
with a large, imperfectly-consistent, human-labeled history to learn from.

---

## Reproducibility

Everything needed to re-run the synthetic reproduction in §3.2 is in this repository and requires no
API keys, no client data, and no cost:

```
python scripts/00_generate_synthetic.py       # synthetic Phase 1 data
python scripts/03_5_dataset_intelligence.py   # ADS, consistency, VAT stats
python scripts/04_architecture_decision.py    # R1-R5 decisions + report
python scripts/phase2/p2_01_build_kb.py       # knowledge base
python scripts/phase2/p2_02_classify_eval.py  # held-out cascade eval
python scripts/phase2/p2_05_end_to_end.py     # 5 synthetic receipts -> tiers
```

Full method detail, all 16 architecture decision records, the confidence-cascade specification, and
the real-vs-synthetic comparison this report draws from are in `architecture/` and `METHODOLOGY.md`
in the same repository. Production numbers throughout this report are cited from a confidential
client engagement and are not independently reproducible from this repository; they are stated as
measured facts from that engagement, not as results computed here.

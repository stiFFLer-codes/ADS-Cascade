# 03 — Non-Functional Requirements

> **Status:** Solution Architecture — governing document
> **Date:** 2026-07-06
> **Depends on:** `00_SCOPE.md` (scope, locked Phase 1 decisions), `08_CONFIDENCE_CASCADE.md` (tier definitions), `13_OBSERVABILITY.md` (measurement plumbing), `14_COST_MODEL.md` (cost math)

Every NFR below states a **target**, a **measurement method**, and a **rationale citing the specific Phase 1 metric** that justifies it. Targets marked *(pilot-calibrate)* are Phase 1-derived starting points that the pilot must confirm or adjust (open question #12 in `00_SCOPE.md`). Nothing here prescribes a vendor or product; where a candidate technology is named it is a candidate, with the decision deferred to `DECISIONS.md` / `OPEN_QUESTIONS.md`.

Tier vocabulary (from `08_CONFIDENCE_CASCADE.md`): **T1** auto-apply, **T2** auto-apply + spot-check, **T3** human review (LLM-assisted suggestion), **T4** manual entry that becomes training data.

---

## 1. Accuracy

### NFR-1 — Overall auto-applied correctness
- **Target:** ≥ 85% of auto-applied classifications (T1 + T2 combined, across all four output fields AccountID / VAT% / TaxCode / WarehouseID) correct at pilot exit; ≥ 90% at steady state (3 months post-pilot).
- **Measurement:** Correction rate against accountant behaviour. A classification counts as *correct* if it is exported without correction, or explicitly confirmed in review. Computed as a rolling 30-day window per field and combined. Accountant corrections are the ground truth — there is no separate labelling effort.
- **Rationale:** Phase 1 success target is 85–90% accuracy. The deterministic base rate supports this: 91.2% of products classify deterministically (ADS > 0.95), so the auto-applied population is dominated by cases the historical data already answers.

### NFR-2 — Per-tier accuracy floors
- **Target:** T1 ≥ 98% correct; T2 ≥ 92% correct. T3 carries no auto-apply accuracy target (nothing is applied without a human), but suggestion acceptance rate is tracked as a model-quality signal, target ≥ 70% *(pilot-calibrate)*. T4 has no accuracy target — it is the training-data intake.
- **Measurement:** T1 and T2 measured against accountant corrections as in NFR-1, segmented by the tier recorded at classification time. T2 additionally receives a mandatory random spot-check sample (≥ 5% of T2 volume routed to review regardless of confidence) so T2 accuracy is measured on an unbiased sample, not only on documents accountants happened to open.
- **Rationale:** The tier thresholds (0.95 / 0.85) are only meaningful if each tier has an accuracy floor to be calibrated against. If T1 falls below 98%, the T1 threshold must rise (fewer auto-applies); if T2 sits far above 92%, the threshold can drop (more automation). This is the control loop that turns the Phase 1 thresholds from guesses into managed quantities.

### NFR-3 — Reporting granularity: per-company AND per-product
- **Target:** Accuracy is reported (a) aggregate, (b) per company, (c) per normalized product, in every accuracy dashboard and pilot report. An aggregate-only number is non-compliant with this NFR.
- **Measurement:** The correction-rate computation of NFR-1 grouped by `company_id` and by `normalized_product_id`; worst-decile companies and products surfaced explicitly (see `13_OBSERVABILITY.md`).
- **Rationale:** Weighted ADS is 0.847 while unweighted is 0.964. That 0.117 gap means high-volume products are disproportionately the ambiguous ones: an aggregate accuracy number will look healthy while specific companies or specific frequent products fail persistently. Cross-company consistency of 0.695 further guarantees that errors cluster by company. Aggregate accuracy hides exactly the tail this system must manage.

### NFR-4 — Confidence calibration
- **Target:** Within each confidence decile, empirical accuracy deviates from predicted confidence by ≤ 3 percentage points *(pilot-calibrate)*. Thresholds (0.95 for T1, 0.85 for T2) are reviewed at pilot midpoint and exit.
- **Measurement:** Reliability diagram (predicted confidence vs observed correction rate) computed monthly per company and globally.
- **Rationale:** The four-tier cascade is only as good as the score that routes into it. Phase 1 derived 0.95/0.85 from invoice-line ADS distributions; receipts add OCR noise the invoice data never had, so calibration must be re-established on receipt traffic before the thresholds are trusted.

---

## 2. Latency

### NFR-5 — Synchronous classify API latency
- **Target:** p95 < 100 ms per line for the synchronous classify call (T1/T2 path). Internal budget: deterministic lookup p95 < 10 ms; embedding fallback search p95 < 50 ms; VAT re-ranking and tier assignment within the remainder. The LLM is **never** on the synchronous path.
- **Measurement:** Server-side latency histograms per stage (lookup / embedding / re-rank), exported per `13_OBSERVABILITY.md`; measured at expected concurrent load, not idle.
- **Rationale:** Phase 1 target: < 100 ms per classification, lookup < 10 ms, embedding < 50 ms. The budget is achievable precisely because 91.2% of lines terminate in the deterministic lookup and never reach the embedding stage.

### NFR-6 — End-to-end asynchronous receipt pipeline
- **Target:** WhatsApp message received → all lines classified (or routed to T3/T4): **p95 ≤ 5 minutes in normal mode**. A **batch mode** grouping work into windows (client spec suggests 15-minute batches, primarily to exploit LLM Batch-API pricing) is a per-deployment configuration switch. Which mode is the default is **pending business confirmation** — the trade is ~€0.0004/line saved (see `14_COST_MODEL.md` §4) against up to ~15 minutes of added wall-clock latency.
- **Measurement:** Timestamp delta from durable intake (webhook ack) to final classification event, per receipt; histograms split by mode and by stage (queue wait / OCR / extraction validation / classification / LLM batch wait).
- **Rationale:** This budget is dominated by components outside the classify API: OCR is seconds per document, and optional LLM batching is minutes by design. Mixing it into NFR-5 would make both targets meaningless — they are separate budgets on purpose. Receipts are not an interactive workload (the accountant sees results in a review queue, not a spinner), so minutes-scale p95 is a business choice, not a technical ceiling.

### NFR-7 — Tier 3 turnaround
- **Target:** A line entering T3 has an LLM suggestion attached and is visible in the review queue within p95 ≤ 5 min (normal mode) / ≤ batch window + 5 min (batch mode). Human review time itself is a workflow SLA (business-owned), not a system NFR, but queue age is monitored with an alert at > 24 h *(pilot-calibrate)*.
- **Measurement:** Queue-entry to suggestion-attached delta; review-queue age distribution.
- **Rationale:** T3 is ~5–9% of lines (the non-deterministic tail net of embedding matches; ADS evidence: 8.8% of products are non-deterministic, 1.1% genuinely ambiguous). The tier only works economically if the human sees a pre-formed suggestion rather than a blank field.

---

## 3. Cost

### NFR-8 — Per-line classification cost
- **Target:** Blended classification cost < €0.001 per line, measured monthly. Composition: T1/T2 lines cost amortized infrastructure only (order €5–50 per million lines); the LLM is invoked only for the T3 tail.
- **Measurement:** (LLM spend attributable to classification + classification-attributable infra) ÷ lines classified, per month, per company and fleet-wide. LLM spend is metered per call with company attribution (see NFR guardrails in `14_COST_MODEL.md` §8).
- **Rationale:** Phase 1 target: < €0.001/line. The math holds *because* 91.2% of lines never touch the LLM: even at worst-case Haiku-class pricing with no batch discount, a 9% T3 share yields ≈ €0.00017/line blended (`14_COST_MODEL.md` §4, with sensitivity analysis). The target is broken only if the deterministic core collapses — which is a KB-health incident, not a pricing problem.

### NFR-9 — OCR cost is a per-document budget, stated separately
- **Target:** OCR/extraction cost budgeted per **document** at €0.002–€0.011 per receipt depending on provider class (`14_COST_MODEL.md` §3), including a 5% retry allowance *(assumed, pending confirmation)*. OCR cost is **never** folded into the €0.001/line metric.
- **Measurement:** Provider invoices reconciled against per-document call metering, monthly.
- **Rationale:** Honesty requirement. A receipt with one line would "cost" €0.01+ per line if OCR were counted, falsely failing NFR-8; a 10-line receipt would dilute it, falsely passing. Ingestion cost scales with documents, classification cost scales with lines — they are different unit economics and are reported as such. D406 XML had zero extraction cost; receipts introduce this as a genuinely new budget line.

---

## 4. Throughput & Scale

### NFR-10 — Sizing baseline
- **Target:** The system is sized from Phase 1 evidence: 169 companies, 296,648 invoice lines historical, median company ~68 documents/month, average ~623 (skewed distribution — sizing must use the distribution, not the mean). Receipt volume per company is **unknown** (open question #6); capacity planning uses the three scenarios of `14_COST_MODEL.md` §2 (100 / 500 / 2,000 receipts/company/month). Design point: sustain the mid scenario across all onboarded companies with ≤ 50% steady-state utilization.
- **Measurement:** Load test at 2× mid-scenario volume before pilot exit; sustained-throughput and queue-depth dashboards in production.
- **Rationale:** Every sizing number here is traceable to Phase 1 data or explicitly flagged as a scenario. Guessing receipt volume silently would contaminate the cost model and the capacity plan with the same unverified number.

### NFR-11 — Burst handling (month-end close)
- **Target:** Absorb bursts of 10× median daily volume (fiscal month-end and VAT-deadline clustering) with **no document loss and no ingestion backpressure to WhatsApp**; during burst, end-to-end p95 (NFR-6) may degrade up to 3× but ingestion acknowledgement latency must not.
- **Measurement:** Synthetic burst test (10× for 2 hours) in staging per release; queue-depth and ack-latency alerts in production.
- **Rationale:** Romanian accounting workloads are deadline-driven; the receipt stream will spike exactly when accountants are busiest and least tolerant of loss. The durable-queue architecture (NFR-12) makes latency the degradation axis instead of availability.

---

## 5. Availability & Degradation

### NFR-12 — Ingestion durability: never lose a document
- **Target:** A WhatsApp webhook delivery is acknowledged only after the message reference and payload are durably persisted (intake queue + object storage for media). Zero document loss under any single downstream failure (OCR provider down, DB degraded, LLM down). Webhook endpoint availability ≥ 99.9% monthly.
- **Measurement:** End-to-end reconciliation: WhatsApp delivery receipts vs intake records, daily; chaos test — kill each downstream dependency and verify intake continues and replays.
- **Rationale:** A lost receipt is a fiscal-compliance failure for the client's client and is unrecoverable (the paper may be gone; the 7-day WhatsApp hold in the client spec is a mitigation, not a substitute). Everything downstream of intake is retryable; intake itself must therefore be the most available component in the system.

### NFR-13 — Classify API availability
- **Target:** ≥ 99.5% monthly for the synchronous classify API *(pending hosting/stack confirmation — open question #1; a hard SLO cannot be committed before the deployment topology is known)*.
- **Measurement:** Success-rate SLI (non-5xx, within NFR-5 latency) from the load balancer / gateway, monthly.
- **Rationale:** The classify API also serves the existing D406 pipeline (shared knowledge base, `05_SERVICE_ARCHITECTURE.md`); its availability now carries two workloads.

### NFR-14 — Graceful degradation ladder
- **Target:** Explicit, tested degraded modes — never a hard stop:
  1. **LLM provider down/over budget:** T1/T2 continue unaffected; T3 lines queue for human review without a suggestion (flagged "no AI suggestion"). No retry storm — circuit breaker with exponential backoff.
  2. **Embedding store down:** deterministic-lookup-only mode; lines that would have matched via embeddings route to review. T1 volume drops, nothing is misclassified silently.
  3. **Knowledge base DB degraded:** ingestion continues (NFR-12); classification pauses and drains on recovery.
  4. **OCR provider down:** documents held in intake; retry with backoff; alert at 15 min *(pilot-calibrate)*.
- **Measurement:** Each rung exercised in a quarterly game-day; mode transitions are events, alerted per `13_OBSERVABILITY.md`.
- **Rationale:** The cascade's ordering (deterministic → embedding → VAT re-rank, LLM only at T3) is what makes degradation graceful: each dependency loss removes a refinement, not the service. 91.2% of value survives the loss of every AI component simultaneously.

---

## 6. Data Quality

### NFR-15 — Extraction validation rate
- **Target:** ≥ 98% of ingested receipts either pass arithmetic validation or are explicitly flagged to review — silent acceptance of non-reconciling extractions is prohibited. Validation = per-line amounts sum to receipt total ± rounding tolerance, and per-line VAT bracket letters reconcile against the printed per-bracket VAT totals (e.g. `30.57 A` ↔ `TOTAL TVA A – 21%`).
- **Measurement:** Validation outcome recorded per receipt (pass / auto-repaired / flagged); rate dashboarded per OCR provider and per company.
- **Rationale:** The VAT bracket letter is a deterministic per-line signal the client spec ignored (`00_SCOPE.md` §3); arithmetic reconciliation is the cheap validator that catches most OCR damage before it can poison classification or the learning loop.

### NFR-16 — Duplicate detection
- **Target:** Duplicate-receipt detection precision ≥ 99%, recall ≥ 95% *(pilot-calibrate)*. Precision is prioritized: falsely merging two distinct receipts corrupts the books; a missed duplicate is caught by the accountant.
- **Measurement:** Precision from review-queue overturns of duplicate flags; recall from periodic sampled audit (same vendor/total/date-window candidates).
- **Rationale:** Users re-send photos (blur, "did it go through?"). Receipts, unlike D406 XML, have no unique document identifier — duplication is an inherent property of the channel and needs an explicit quality bar.

### NFR-17 — Confidence-signal independence (hard rule)
- **Target:** OCR extraction confidence and classification confidence are **never collapsed into a single score** — not in storage, not in APIs, not in the review UI, not in tier routing. Tier routing may *consume* both, but each must remain independently inspectable end-to-end.
- **Measurement:** Schema review (`07_DATA_SCHEMA.md` carries both fields separately); API contract check (`10_API_CONTRACTS.md`); UI audit at pilot.
- **Rationale:** Locked decision in `00_SCOPE.md` §2. A blurry photo of an unambiguous product and a crisp photo of an ambiguous product need opposite remediations (re-photo vs human classification). One blended number makes the two failure modes indistinguishable and both dashboards (NFR-15, NFR-1) unactionable.

---

## 7. Auditability

### NFR-18 — Reproducibility of every auto-applied classification
- **Target:** Every auto-applied (T1/T2) classification stores: rule/lookup version, knowledge-base snapshot reference, embedding model + index version, VAT rate-table version (Legea 141/2025 effective-date ranges), and — where an LLM contributed a T3 suggestion — model identifier, prompt template version, and request ID. Replaying the stored inputs against the referenced versions must yield the same output.
- **Measurement:** Automated replay audit: monthly sample of ≥ 500 auto-applied lines re-executed against pinned versions; 100% match required (mismatch = incident).
- **Rationale:** These are fiscal bookings for third parties. When ANAF or a client disputes a booking, "the model said so" is not an answer; "rule R-1043 v7 over KB snapshot S-2026-06-30 produced account 6352" is. VAT-as-dated-attribute (the August 2025 rate change, 19→21% / 9→11%) makes version-pinned rate tables mandatory — a receipt reprocessed today must classify under the rates in force on its issue date.

### NFR-19 — Correction traceability
- **Target:** Every accountant correction records: prior value, new value, actor, timestamp, the classification record it overrides (with its NFR-18 provenance), and the identifier of any company rule or KB event the correction generated. The chain correction → rule → subsequent classifications is queryable in both directions.
- **Measurement:** Referential-integrity checks in the audit store; spot audit at pilot: pick 20 corrections, walk the chain both ways.
- **Rationale:** Corrections are simultaneously audit events and training data (T4 → training data by design). If the lineage from a correction to the rule it spawned is lost, a bad correction cannot be recalled — and cross-company consistency 0.695 means company rules carry real semantic weight per company; they must be attributable.

---

## 8. Learning Loop

### NFR-20 — Correction-to-rule propagation latency
- **Target:** An accepted correction becomes a company rule **visible to subsequent classifications** within p95 ≤ 60 seconds (hard ceiling: minutes, not hours). Propagation is event-driven (`06_EVENT_DRIVEN_WORKFLOW.md`), not poll- or batch-based.
- **Measurement:** Event timestamp delta: `CorrectionAccepted` → rule active in the serving lookup path; verified continuously by a canary (write synthetic correction, classify probe line, measure).
- **Rationale:** The 8.8% non-deterministic tail converts to deterministic company rules *only* through corrections (cross-company 0.695 proves rules must be learned per company). An accountant working through a stack of receipts from the same merchant should correct once and see the fix on the very next document — that experience is what makes the review tier a training channel rather than a grievance channel.

### NFR-21 — No synchronous mass reprocessing (prohibited pattern)
- **Target:** A rule or monography change must **never** trigger synchronous reprocessing of the document corpus. Re-scoring is lazy and applies to **unexported documents only**; exported documents are immutable (correctable only through the accounting system's own workflow). Background re-scoring, where used, is rate-limited so that classification and ingestion SLOs (NFR-5, NFR-6) are unaffected — verified by the burst test of NFR-11 running concurrently with a re-score.
- **Measurement:** Architectural conformance (no code path from rule-change to bulk reprocess); load test with concurrent re-scoring; alert on re-score queue starving the classify path.
- **Rationale:** The client spec's "reprocess all documents on monography change" is a scale trap explicitly designed out (`00_SCOPE.md` §2): at 169 companies × 296k+ historical lines and growing, each rule change would trigger unbounded work with no fiscal effect on already-exported bookings.

---

## 9. Security & Compliance

### NFR-22 — Security, GDPR, and fiscal-data compliance
- **Target/Measurement/Rationale:** Governed in full by `12_SECURITY_COMPLIANCE.md` (tenant isolation of per-company knowledge bases, receipt-image PII handling, data residency and retention — open question #11, WhatsApp channel security, LLM-provider data-processing terms). Stated here once, by reference, to avoid duplication; those requirements bind this document's NFRs wherever they intersect (notably NFR-12 storage and NFR-18 audit retention).

---

## 10. Localization

### NFR-23 — Romanian-capable embedding model
- **Target:** The embedding model used for the fallback search must be multilingual with **verified** Romanian performance: benchmarked on a held-out Romanian product-description corpus drawn from the 47,306 normalized Phase 1 products, with retrieval quality (recall@5 of the correct product cluster) ≥ 90% *(pilot-calibrate)* before the model is accepted. Candidates (API-hosted multilingual embedding models vs self-hosted multilingual encoders) are compared in `09_AI_ORCHESTRATION.md`; the model choice sits behind the provider-agnostic interface and its version is pinned per NFR-18.
- **Measurement:** The benchmark above, re-run on every model or version change; per-language retrieval-quality monitoring in production.
- **Rationale:** All product text is Romanian (`MOTORINA`, `ROVINIETA`, abbreviated till-receipt vocabulary — uppercase, truncated, no diacritics on many fiscal printers). An English-centric embedding model silently degrades exactly the 8.8% tail the embedding stage exists to catch.

### NFR-24 — Diacritics and text normalization
- **Target:** A single deterministic normalization pipeline applied identically at KB build time, at query time, and in the learning loop. It must handle: Romanian diacritics including the cedilla vs comma-below variants (ș/ş, ț/ţ — both encodings appear in the wild), diacritic-stripped receipt text matching diacritic-full KB entries, case folding, and till-receipt abbreviation patterns. Normalization version is part of the NFR-18 provenance.
- **Measurement:** Property-based tests over the variant pairs; audit that KB-side and query-side normalization are the same code artifact (not two implementations).
- **Rationale:** Fiscal printers emit `TIGARI`; the knowledge base may hold `țigări`. If lookup-side and KB-side normalization ever diverge, the deterministic tier — the component carrying 91.2% of traffic — silently loses matches, and the failure surfaces as unexplained T3 inflation and cost drift rather than as an error.

---

## Open questions surfaced by this document

1. **Receipt volume per company per month** (open question #6) — blocks final capacity sizing (NFR-10) and the cost scenarios; the three-scenario model in `14_COST_MODEL.md` is the interim.
2. **Normal mode vs 15-minute batch mode default** (NFR-6) — a latency-vs-cost business decision, pending confirmation from the firm.
3. **Confidence thresholds 0.95/0.85 and all *(pilot-calibrate)* targets** — Phase 1-derived starting points; the pilot must produce the calibrated values (NFR-2, NFR-4, NFR-7, NFR-14, NFR-16, NFR-23).
4. **Hosting and stack** (open question #1) — NFR-13's availability SLO and NFR-10's utilization design point cannot be committed until deployment topology is known.
5. **T2 spot-check sampling rate** — 5% is an assumption; the correct rate depends on T2 volume and observed T2 error rate (NFR-2).
6. **OCR retry-rate assumption (5%)** — used in NFR-9 and the cost model; needs measurement on real receipt photo quality during pilot.
7. **Review-queue workflow SLA** (NFR-7) — who owns the > 24 h queue-age escalation, the firm or the platform team?
8. **Retention period for provenance and audit records** (NFR-18, NFR-19) — Romanian fiscal retention obligations vs GDPR minimization; resolved in `12_SECURITY_COMPLIANCE.md` (open question #11).
9. **Whether the D406 pipeline adopts these same NFRs** — the shared classify API (NFR-13) now serves both workloads; the D406 side's existing expectations are undocumented (open question #2).

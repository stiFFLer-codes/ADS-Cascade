# 13 — Observability: Monitoring, Metrics, Alerting & Model-Quality

> **Status:** Solution Architecture (governing document)
> **Date:** 2026-07-06
> **Scope:** What the system measures, how it alerts, and how it proves the classification engine stays trustworthy over time. Instrumentation standard: OpenTelemetry (traces, metrics, logs). Backends are candidates pending stack confirmation: a managed cloud-native suite, a Prometheus/Grafana/Loki/Tempo-class open stack, or a commercial APM — chosen with the hosting decision (`OPEN_QUESTIONS.md` #1).

---

## 1. Three Observability Planes

A classification platform can be "up" while silently going wrong. We therefore monitor three distinct planes, each with its own signals, owners, and dashboards:

| Plane | Question it answers | Typical signals | Failure looks like |
|---|---|---|---|
| **P1 — System health** | Are the services alive and fast? | Standard RED (rate, errors, duration) per service; USE (utilization, saturation, errors) per resource; queue/broker health | 5xx spikes, latency, broker lag |
| **P2 — Pipeline health** | Is every document moving through the funnel? | Document-level funnel counters, stage latencies, stuck-document detection, DLQ depth | Documents received but never exported; silent stalls |
| **P3 — Model & knowledge quality** | Are the *answers* still right? | Tier shares, correction rates, confidence distributions, KB coverage, cost per line | Everything green on P1/P2 while accountants quietly correct more and more lines |

P3 is the differentiator. P1 and P2 use industry-standard patterns and are summarized; P3 is specified in detail (§3–§7) because it encodes the Phase 1 evidence into runtime guardrails.

**P1 summary:** every service exports RED metrics with `service`, `endpoint`, `company_id` (as a low-cardinality dimension only where per-company breakdown is needed — see §10 on cardinality), plus resource USE metrics from the platform. External dependencies (OCR vendor, LLM vendor, embedding vendor, WhatsApp API, ANAF/e-Factura) each get a synthetic health probe and an error-rate/latency panel, so vendor regressions are distinguishable from our own.

---

## 2. Pipeline Funnel (P2)

Every document advances through named stages; each transition emits a counted, timestamped event:

```
received → extracted → validated → classified(T1|T2|T3) → [review(T4)] → exported
```

- **Funnel counters** per stage, per company and global, windowed (hour/day/month). The invariant is conservation: everything `received` must eventually reach `exported`, `rejected` (with a reason code), or `quarantined`. A daily reconciliation job checks conservation and reports discrepancies as a P2 alert — this catches "silently dropped" documents that no error metric sees.
- **Stage latency histograms** for each transition, per company and global.
- **Stuck-document detection:** a scheduled sweep finds documents whose current stage age exceeds a per-stage threshold (e.g., extraction > 15 min, review queue > 24 h, validated-but-unclassified > 5 min — thresholds configurable, initial values pending pilot). Stuck documents raise an alert with the document IDs and stage, and appear on the ops dashboard as an actionable list, not just a count.
- **Review-queue metrics:** queue depth per company, age of oldest item, review throughput per operator-hour. Queue depth trending up while correction rate is flat means a staffing problem, not a model problem — the split matters for the runbook.
- **Ingestion-edge metrics:** webhook signature failures, allowlist rejections, quarantine additions/purges, media validation rejections (ties to `12_SECURITY_COMPLIANCE.md` §4 — a spike in signature failures is a security signal, not an ops nuisance).

Rejected documents carry machine-readable reason codes (unreadable image, not a fiscal receipt, duplicate, validation-total mismatch, …) so the rejection mix is itself a monitored distribution.

---

## 3. Classification Quality Metrics (P3)

The cascade's health is defined by *where* traffic lands and *how often humans overturn it*.

### 3.1 Tier volume share

Phase 1 measured **91.2% of products as deterministic** (ADS > 0.95). At steady state, therefore, **Tier 1 should carry roughly ≥90% of line volume**, Tier 2 most of the remainder, Tier 3 a few percent, Tier 4 (human) the residue.

- Metric: `lines_classified_total{tier, company_id}` → tier share per company and global, daily and 7-day rolling.
- **Alert: T1 share drops materially below its baseline** (global default: below ~85% for a sustained window; per-company baselines learned during pilot, since a young company legitimately runs lower until its KB warms up). A falling T1 share means one of two things, and the dashboard must make them distinguishable: **KB drift** (new products/suppliers the rules don't cover — check KB coverage §6) or **extraction degradation** (product text arriving mangled, so rules stop matching — check OCR confidence §4). Cold-start companies are annotated so they don't pollute the global alert.
- T3 (LLM) share is also cost-bounded: rising T3 share is simultaneously a quality and a spend signal (§5).

### 3.2 Correction rate per tier

The single most important quality number: of lines auto-classified at tier X, what fraction did a human later correct?

- Metric: `corrections_total{tier_of_original, company_id, field}` / lines classified at that tier, computed over export-complete windows (a line can only be counted "uncorrected" once its document is exported).
- **Thresholds:**
  - **T1 correction rate ≥ 2% = threshold breach.** Deterministic rules being overturned at 2%+ means rules are stale or mis-scoped — this triggers cascade tuning: review the offending rules, check ADS recomputation (§6), consider raising the T1 confidence bar. T1 is supposed to be near-perfect; its error budget is the tightest.
  - T2 correction rate baseline set in pilot (expected low single digits); sustained doubling vs baseline alerts.
  - T3 correction rate is expected to be the highest (it handles the ambiguous ~1.1% tail plus KB gaps); it is *tracked* for model comparison and prompt-version regression (a step change after a model or prompt-version rollout is a rollback signal — versions are dimensions on the metric, from the audit record).
- Corrections are broken out **per field** (AccountID vs VAT% vs TaxCode vs WarehouseID). VAT corrections have their own watch: Phase 1 showed 94.5% single-rate, and the Legea 141/2025 rate change demonstrated that VAT errors arrive *in bursts around law changes* — a VAT-correction burst is a "dated-rate configuration" runbook, not a model runbook.

### 3.3 Per-company accuracy trend

Per company: correction rate over time (all tiers), plotted monthly. Cross-company consistency of 0.695 means companies genuinely differ — **quality is managed per company**, and a single global accuracy number can hide one client's degradation behind another's improvement. The monthly review pack (§9) leads with this chart.

### 3.4 Repeat-correction detector

A dedicated detector watches correction events per `(company_id, normalized_product)`:

- **Same product corrected twice** (same target) → **rule candidate**: the learning loop should have proposed a rule; if none exists, flag for rule creation.
- **Same product corrected to different targets** → **conflict**: either two valid contexts (needs a discriminating attribute) or operator disagreement (needs the firm's methodological call). Conflicts go to a human-curation queue, never auto-resolved.

This detector is the operational teeth of the learning loop: its backlog should trend toward zero in a healthy system, and its output feeds `06_EVENT_DRIVEN_WORKFLOW.md`'s rule-proposal flow.

---

## 4. Two Confidence Signals — Monitored Separately, Never Merged

Locked architectural rule (`00_SCOPE.md` vision-notes disposition): **OCR extraction confidence and classification confidence are independent signals and are never collapsed into one number** — not in the cascade, not in the UI, and not in monitoring.

| Signal | Distribution monitored | Drift alarm means |
|---|---|---|
| **Extraction confidence** (per field and per document, from the OCR/extraction layer) | Daily distribution per company and global; percentile bands (p10/p50/p90) | Drop ⇒ *input-side* problem: camera/receipt-photo quality decline at a client (per-company drop), thermal-paper fading seasonality, or an **OCR vendor regression** (global drop, check vendor version/status). Runbook starts at the image, not the KB. |
| **Classification confidence** (per line, from the cascade tier that decided) | Daily distribution per tier, per company and global | Drop ⇒ *knowledge-side* problem: **KB coverage gap** (new product mix, new supplier), ADS drift, embedding index staleness. Runbook starts at the KB, not the images. |

- Drift detection on each: compare the rolling window distribution against a baseline window (simple percentile-shift or population-stability checks are sufficient; exotic drift statistics are not required). Alarm on sustained shift, per company and global.
- **The joint view is a 2×2 diagnostic, not a merged score:** low extraction + low classification = garbage in; high extraction + low classification = knowledge gap; low extraction + high classification = suspicious (rules matching on mangled text — investigate false T1 hits); high/high = healthy. The ops dashboard shows this quadrant explicitly.
- The accountant-facing green/amber colours in the frontend derive from these same two signals separately (amber-extraction vs amber-classification are different visual cues), so what operators see and what monitoring sees never disagree.

---

## 5. Cost Observability

Cost is a first-class metric because the architecture's economics depend on the tail staying a tail (`14_COST_MODEL.md`).

- **LLM spend:** per company per day, tokens and € — derived from per-call usage metadata tagged with `company_id`, `model`, `prompt_version`. Also €/T3-line.
- **€/line trend (all-in)** vs the **<€0.001/line target**: OCR cost + embedding cost + LLM cost, divided by lines processed, per company and global, weekly trend on the ops dashboard and in the monthly pack.
- **OCR spend per document** per vendor (the every-document cost, hence the biggest lever).
- **Budget alerts:** soft alert at a configurable % of a per-company daily budget; hard alert at the budget. Budgets are per company because a single compromised or misbehaving sender flooding one company must not be discoverable only in the aggregate bill (ties to rate limits, `12_SECURITY_COMPLIANCE.md` §4.5).
- **Deterministic-only kill switch:** an operational control (per company or global) that, when tripped — manually or automatically on hard budget breach or vendor incident — disables Tier 2/Tier 3 calls; lines that T1 cannot answer route directly to the review queue. The pipeline degrades to slower-but-safe instead of expensive-or-down. Kill-switch state is itself a monitored, alerting metric (it should never be silently left on), and every trip is audited.

---

## 6. Knowledge-Base Health

The KB is the product; it gets its own vital signs.

- **Rule coverage per company:** % of the company's incoming lines that hit a company rule (T1-company). Complement: % answered only by the global layer, % reaching T2/T3. A company whose coverage plateaus low is a candidate for a rule-curation session; coverage should climb over a company's first months (cold-start curve tracked per company).
- **Global-vs-override hit ratio:** of T1 hits, how many resolved from the company override layer vs the global de-identified layer. Given cross-company consistency of 0.695, a company running mostly on global-layer answers is *at risk* — its corrections haven't yet localized the ~30% of products where companies diverge. This ratio maturing toward override-dominant is the KB "warming up" signal.
- **ADS recomputation drift:** ADS (weighted 0.847 / unweighted 0.964 at Phase 1) is recomputed on schedule as new data lands. Monitor the per-company and global ADS trend; a *falling* ADS means the product population is getting genuinely more ambiguous (new business lines, supplier changes) and predicts a falling T1 share before it happens — this is the leading indicator, tier share is the lagging one. Products whose individual determinism score crosses below the T1 threshold on recomputation are listed for review.
- **Embedding index freshness:** lag between a rule/product/correction becoming active and its embedding being present in the index (staleness histogram); count of KB entries missing embeddings; index size per company. Stale indexes silently degrade T2 into wrong-neighbour retrieval — freshness breach is an alert, not a log line.
- **Rule lifecycle counters:** rules proposed / activated / retired per week per company — a stalled learning loop shows up here as zeros.

---

## 7. Learning-Loop Health

The event-driven correction loop (`06_EVENT_DRIVEN_WORKFLOW.md`) is asynchronous, so its health is measured in lag and backlog:

- **Correction → active-rule propagation lag:** time from a human correction event to the resulting rule/mapping being live for subsequent classifications. **Target: minutes.** Measured end-to-end via the correlation ID on the correction event; p50/p95 tracked; p95 above target for a sustained window alerts (an accountant correcting the same product all afternoon because propagation stalled is the exact failure this catches).
- **Event backlog depth** per topic/consumer group (broker-native lag metrics), with per-topic thresholds; the corrections topic has the tightest threshold.
- **Dead-letter queue monitoring:** DLQ depth > 0 on any pipeline topic pages at warning within business hours; DLQ items carry the original event, error, and correlation ID; a redrive runbook exists per topic. DLQ age (oldest item) is monitored separately from depth.
- **Lazy re-scoring debt:** count of unexported documents flagged for re-scoring after a rule change, and the drain rate. Growing debt with a flat drain rate means re-scoring capacity is undersized.

---

## 8. Latency SLOs & Tracing

### 8.1 SLOs

| Path | SLO | Budget breakdown |
|---|---|---|
| Synchronous classify API | **<100 ms p95** per line/document call | T1 rule/catalog lookup **<10 ms**; embedding + T2 retrieval **<50 ms**; overhead/validation the remainder. T3 (LLM) calls are excluded from this SLO — Tier 3 escalation returns asynchronously or with an explicit degraded-latency contract (per `10_API_CONTRACTS.md`). |
| End-to-end async pipeline (WhatsApp receipt → ready-for-review/auto-classified) | Budget allocated per stage: media fetch, OCR, validation, classification, persistence — initial end-to-end target minutes-scale, **exact figure pending volume confirmation** (open question #6). OCR vendor latency dominates and is tracked as its own SLI. | |
| Review action → learning propagation | Minutes (see §7) | |

SLO compliance is computed from real traffic (not synthetic only) and reported monthly with error-budget burn.

### 8.2 Tracing

- OpenTelemetry tracing across every service and every vendor call.
- **Correlation ID from the WhatsApp message ID (or frontend upload ID) through to export:** assigned at ingestion, propagated on every event, every service call, every vendor request (as metadata where the vendor supports it), stored on the document record, and stamped into the audit trail. One ID answers "what happened to this receipt?" across P1, P2, and P3.
- Spans carry `company_id`, `document_id`, `tier`, `rule_version`/`model`/`prompt_version` as attributes — the same identifiers the audit trail records, so a trace and an audit record are always joinable.
- Span attributes never contain receipt text, image bytes, or phone numbers (§10).

---

## 9. Dashboards & Review Cadence

1. **Ops dashboard (P1+P2):** service RED panels, vendor health, funnel with conservation check, stuck-document list, queue depths, DLQ, kill-switch state, cost-today vs budget. Audience: whoever is on call.
2. **Accountant-facing quality view:** per-company — review-queue state, today's tier mix, extraction-vs-classification confidence quadrant in the same green/amber vocabulary as the frontend's per-line colours, repeat-correction list awaiting a rule decision. Audience: firm operators/admin; this is a product surface, read-only, per-company scoped under the same authorization as the app (`12_SECURITY_COMPLIANCE.md` §5).
3. **Monthly model-quality review pack (P3):** per-company accuracy trend, tier shares vs baseline, T1 correction rate vs the 2% bar, ADS drift, KB coverage curves, €/line vs target, incidents and threshold changes. Audience: firm leadership + engineering; this pack is where cascade thresholds (0.95/0.85 starting points, open question #12) get recalibrated with evidence.

---

## 10. Structured Logging, Event Versioning & PII

- **Structured logs only** (JSON-class), with mandatory fields: timestamp, service, severity, correlation ID, `company_id` where applicable, event/log type. Free-text messages are for humans; fields are for queries.
- **PII rules in telemetry:** logs, metrics, traces, and alert payloads contain **no receipt images, no raw OCR text, no phone numbers, no cashier names**. Documents are referenced by ID; senders by an opaque ingestion ID. Product text may appear only in the dedicated KB/correction data stores — not in general-purpose logs; where a log line genuinely needs product context (e.g., conflict detector output), it logs the normalized-product hash/ID and the reader joins in the application. Log pipelines get a redaction filter as a backstop (pattern-based phone/CUI scrubbing), but the primary control is never emitting PII in the first place.
- **Cardinality discipline:** `company_id` is an acceptable metric dimension at this tenancy scale (one firm, tens of companies); `document_id`, `product`, and `user` are trace/log fields, never metric labels.
- **Event schema versioning:** every event on the backbone carries `schema_version`; consumers tolerate additive change and reject unknown-major versions to the DLQ (which is monitored, §7). Metric names and label sets are versioned in an instrumentation registry doc so dashboards don't silently break on rename; alert rules live in version control alongside the runbooks they point to.
- **Retention of telemetry:** logs/traces are short-retention operational data (e.g., 30–90 days, pending confirmation), distinct from the audit trail (`12_SECURITY_COMPLIANCE.md` §7), which is the long-retention record of decisions. Telemetry is never the system of record for who-changed-what.

---

## 11. Alerting Matrix

Severity: **P1-page** (immediate), **P2-hours** (business hours), **P3-review** (weekly/monthly review).

| Symptom | Probable cause | Severity | Runbook pointer |
|---|---|---|---|
| Webhook signature failures spike | Misconfigured secret rotation, or probing/attack | P1-page | RB-SEC-01 (rotate/verify secret; if valid secret, treat as attack) |
| Funnel conservation mismatch (daily job) | Dropped documents, consumer crash without DLQ | P1-page | RB-PIPE-01 (locate stage via correlation IDs) |
| DLQ depth > 0 (pipeline topics) | Poison event, schema-version rejection, consumer bug | P2-hours | RB-PIPE-02 (inspect, fix, redrive) |
| Stuck documents > threshold in a stage | Stage worker down, vendor outage, review understaffing | P2-hours | RB-PIPE-03 (per-stage triage table) |
| Extraction confidence distribution drops (global) | OCR vendor regression/model change | P2-hours | RB-OCR-01 (vendor status, canary set, consider vendor failover) |
| Extraction confidence drops (one company) | Client photo/camera/receipt-quality issue | P3-review | RB-OCR-02 (contact client with photo guidance) |
| Classification confidence drops, extraction stable | KB coverage gap, embedding staleness, ADS drift | P2-hours | RB-KB-01 (coverage + freshness + ADS panels) |
| T1 share < baseline (sustained) | KB drift or extraction degradation | P2-hours | RB-KB-02 (use §4 quadrant to branch) |
| T1 correction rate ≥ 2% | Stale/mis-scoped rules; threshold miscalibration | P2-hours | RB-KB-03 (audit offending rules; cascade tuning) |
| VAT-correction burst across companies | Rate-law change / dated-rate config gap (cf. Legea 141/2025) | P1-page | RB-VAT-01 (verify dated rate table, freeze exports if wrong) |
| Same product corrected to different targets | Rule conflict or operator disagreement | P3-review | RB-KB-04 (conflict curation queue) |
| Correction→rule propagation p95 > minutes target | Consumer lag, broker backlog | P2-hours | RB-LOOP-01 (backlog + consumer health) |
| LLM spend > per-company daily budget | T3 share creep, sender flooding, retry storm | P1-page | RB-COST-01 (identify driver; kill switch if hard breach) |
| €/line trend approaching €0.001 | OCR cost drift, falling T1 share diluting economics | P3-review | RB-COST-02 (monthly pack; vendor/tier levers) |
| Kill switch active > agreed window | Left on after incident | P2-hours | RB-COST-03 (review, restore tiers) |
| Embedding index freshness breach | Indexer down/backlogged | P2-hours | RB-KB-05 (indexer health, rebuild) |
| Classify API p95 > 100 ms | Hot path regression, DB/index degradation | P2-hours | RB-PERF-01 (per-span budget breakdown) |

Every alert links its runbook; every runbook names the dashboard panels it uses; runbooks and alert rules are versioned together.

---

## 12. Open Questions Surfaced by This Document

1. **Observability backend** (managed cloud suite vs Prometheus/Grafana-class stack vs commercial APM) — follows the hosting decision; OpenTelemetry instrumentation is backend-neutral either way.
2. **On-call model:** who receives P1 pages — the firm has no 24/7 ops today; is business-hours-only paging acceptable given the async pipeline tolerates hours of delay?
3. **End-to-end async latency target** (receipt → reviewable): needs volume and workflow expectations from the firm (open question #6) before a number is committed.
4. **Baseline windows and exact alert thresholds** (T1 share floor per company, correction-rate baselines for T2/T3, drift sensitivity): pilot-calibrated; the values in this document are starting points tied to Phase 1 evidence, not final.
5. **Per-company daily LLM/OCR budgets** for the cost alerts and kill switch — needs the cost model (`14_COST_MODEL.md`) plus confirmed volumes.
6. **Telemetry retention** (30–90 days proposed) and whether traces may leave the EU if a SaaS backend is chosen — intersects with `12_SECURITY_COMPLIANCE.md` residency question.
7. **Accountant-facing quality view scope:** is it a page in the existing frontend or a separate dashboard product? Affects authorization plumbing.
8. **Vendor usage-metadata completeness:** do the candidate OCR/LLM vendors expose per-call cost/usage adequate for per-company attribution, or must we meter by our own token counts?
9. **ADS recomputation cadence** (nightly vs weekly) — tradeoff between drift-detection latency and compute cost; to be set in pilot.

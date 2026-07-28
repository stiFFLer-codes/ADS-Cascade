# Phase 2 Architecture Package — Scope & Table of Contents

> **Status:** Solution Architecture (governing document set for implementation)
> **Date:** 2026-07-06
> **Scope:** Automated classification (AccountID, VAT%, TaxCode, WarehouseID) for fiscal receipts (bonuri fiscale), sharing intelligence with the solved D406 invoice classification problem.

---

## 1. Package Contents

| # | File | Contents |
|---|------|----------|
| 00 | `00_SCOPE.md` | This document — scope, vision-notes disposition, open-questions index |
| 01 | `01_EXECUTIVE_SUMMARY.md` | Non-technical summary for manager/client audience |
| 02 | `02_REQUIREMENTS.md` | Business & functional requirements derived from the client spec, with divergences marked |
| 03 | `03_NON_FUNCTIONAL_REQUIREMENTS.md` | Accuracy, latency, cost, ROI, availability, data-quality NFRs |
| 04 | `04_DOMAIN_MODEL.md` | Entities (Receipt, Product, Category, Company, Supplier, KnowledgeBase, …) and relationships |
| 05 | `05_SERVICE_ARCHITECTURE.md` | Service breakdown, boundaries, ownership of data, integration contracts |
| 06 | `06_EVENT_DRIVEN_WORKFLOW.md` | Event catalog; correction propagation without synchronous mass reprocessing |
| 07 | `07_DATA_SCHEMA.md` | Knowledge base + product catalog schema (logical DDL, technology-agnostic) |
| 08 | `08_CONFIDENCE_CASCADE.md` | Four-tier confidence cascade — full technical specification |
| 09 | `09_AI_ORCHESTRATION.md` | Model-agnostic LLM/embedding orchestration layer |
| 10 | `10_API_CONTRACTS.md` | Core classification + ingestion + review + export API contracts |
| 11 | `11_SEQUENCE_PETROMAX.md` | End-to-end sequence diagrams tracing the Petromax rovinieta receipt |
| 12 | `12_SECURITY_COMPLIANCE.md` | Security, GDPR, fiscal-data compliance |
| 13 | `13_OBSERVABILITY.md` | Monitoring, metrics, alerting, model-quality observability |
| 14 | `14_COST_MODEL.md` | Per-line and per-document cost model against the <€0.001/line target |
| — | `DECISIONS.md` | Architecture Decision Records — every significant call, alternatives, and evidence |
| — | `OPEN_QUESTIONS.md` | All unconfirmed assumptions and items needing engineering/business confirmation |

---

## 2. Disposition of the Prior Vision Notes ("ContAI Accounting Intelligence Platform")

Each element of the prior vision is kept, changed, or dropped based on a specific Phase 1 metric.

| Vision element | Disposition | Evidence |
|----------------|-------------|----------|
| **Product Catalog as the system's center of gravity (not the LLM)** | **KEEP** | 91.2% of products are deterministic (ADS > 0.95); only 1.1% genuinely ambiguous (ADS < 0.50). The catalog + rules answer the overwhelming majority of classifications; the LLM is a tail worker. RULES_FIRST decision is locked (decision matrix R3, 91.2% ≥ 90% threshold). |
| **Service-oriented design** | **KEEP (with hard boundaries defined)** | The receipts pipeline and D406 pipeline must share one per-company knowledge base without coupling ingestion formats. Service boundaries in `05_SERVICE_ARCHITECTURE.md` are drawn around data ownership, not deployment units — deployment topology is an open question (production stack unknown). |
| **Confidence Engine as a first-class component** | **KEEP (extended)** | ADS divergence (weighted 0.847 vs unweighted 0.964) means confidence must be computed per product, not per model. Extended with a hard rule: OCR extraction confidence and classification confidence are **independent signals, never collapsed** — receipts add an extraction-quality dimension D406 XML never had. |
| **Knowledge Lifecycle feedback loop** | **KEEP (redesigned as event-driven)** | Corrections are the only mechanism that converts the 8.8% non-deterministic tail into deterministic company rules (cross-company consistency 0.695 proves rules must be learned per company). Changed: propagation is event-driven with lazy re-scoring of *unexported* documents only — the client spec's "reprocess all documents on monography change" is a scale trap and is explicitly designed out (`06_EVENT_DRIVEN_WORKFLOW.md`). |
| **Model-agnostic reasoning layer** | **KEEP** | Client spec hard-wires Textract + Haiku. Both are kept as *candidates* behind provider-agnostic interfaces (`09_AI_ORCHESTRATION.md`), because (a) the production stack is unconfirmed, and (b) the LLM handles only Tier 3 traffic (~a few % of lines), so vendor choice is a cost/quality knob, not an architectural commitment. |
| **Single global classifier / global category intelligence** | **CHANGE → hybrid, per-company overrides win** | Cross-company consistency is 0.695 — a global-only classifier is wrong ~30% of the time on multi-company products. Locked Phase 1 decision: HYBRID retrieval (global KB + company overrides), RULES_FIRST order. The rovinieta worked example shows this concretely: the same product legitimately maps to 628, 635, or 6352 depending on the company. |
| **VAT as a primary discriminator** | **CHANGE → secondary/tie-breaking signal** | 94.5% single-rate — below the 95% primary-discriminator threshold (decision matrix R4). Also: Legea 141/2025 changed rates (19→21%, 9→11%) in August 2025; any VAT-partitioned structure fractures across a law change. VAT is an attribute with effective-date ranges, never a partitioning key. |
| **Warehouse as a learned classification output** | **DROP → configuration-resolved, not learned** | warehouse_id is 100% missing in D406 (decision matrix R5: DROP). There is no historical signal to learn from. WarehouseID is resolved by per-company configuration rules; where warehouse master data lives is an open question for engineering. |

## 3. Disposition of the Client Receipts Spec — headline divergences

Full requirement-by-requirement treatment is in `02_REQUIREMENTS.md`; every divergence has an ADR in `DECISIONS.md`.

| Client spec proposal | Disposition |
|---|---|
| WhatsApp Business ingestion, number allowlist, 7-day hold, reply templates | **KEEP** — sound workflow design, adopted as functional requirements |
| Arithmetic VAT allocation across receipt lines (1-product, 1-rate, 2×2, N×2 cases) | **KEEP + STRENGTHEN** — Romanian fiscal receipts print a per-line VAT bracket letter (the sample receipt shows `30.57 A` ↔ `TOTAL TVA A – 21%`). The bracket letter is a deterministic per-line signal the spec ignores; arithmetic reconciliation becomes the validator, LLM the last resort |
| Textract OCR + "NPL" structuring | **KEEP AS CANDIDATE** behind a provider-agnostic Extraction interface (2–3 candidates, pending stack confirmation) |
| Haiku for categorization / VAT assumption | **KEEP AS CANDIDATE** behind the model-agnostic reasoning layer; invoked only at Tier 3 |
| AI-generated categories with "all products in a category share one VAT value" | **CHANGE** — VAT-homogeneous categories fracture across the 2025 rate change and conflict with the 5.5% multi-rate products; categories are semantic groupings, VAT is a dated attribute |
| Category-level AccountID as the primary mapping | **CHANGE** — mappings are per-company at product level first (ADS 0.847/0.964), category level is the cold-start fallback (cross-company 0.695 forbids category-global accounts) |
| Receipts category catalog built separately, seeded from D406 | **CHANGE** — one shared per-company knowledge base feeds both pipelines; no parallel catalogs that can drift |
| Monography change ⇒ "all documents reprocessed" | **CHANGE** — event-driven propagation, lazy re-scoring of unexported documents only |
| Supplier as a primary categorization attribute | **CHANGE** — supplier is a weak signal, product description dominates (Petromax receipt: fuel company, non-fuel line; one company in the data misbooked rovinieta to 6022 Fuel — the exact supplier-prior error) |

---

## 4. Open Questions — running index

Collected in full, with impact and default assumptions, in `OPEN_QUESTIONS.md`. Headline items:

1. Production stack: language/framework, database engine, hosting, deployment pipeline — all unconfirmed.
2. How the existing D406 pipeline is deployed and where its outputs live today.
3. Vector store choice (candidates named with tradeoffs, pending stack confirmation).
4. Message broker / event backbone choice (same).
5. Where warehouse master data lives (ERP?) and whether the client actually uses warehouses for receipt bookings.
6. Expected receipt volume per company per month (drives cost model and batching).
7. WhatsApp Business API route: direct Meta vs BSP partner.
8. e-Factura lookup mechanism for the "<500 RON and not in e-Factura" rule.
9. etva/ANAF API access, rate limits, and terms for CUI→company resolution and CAEN codes.
10. The accounting-system XML export format (target ERP and schema).
11. Data residency and retention obligations for receipt images (GDPR + Romanian fiscal law).
12. Confidence thresholds (0.95/0.85) are Phase 1-derived starting points — pilot must calibrate them.

---

*Phase A complete. Phase B documents follow in this folder.*

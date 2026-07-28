# Architecture Decision Records — Receipts Classification (Phase 2)

Format: one record per significant decision. Status `ACCEPTED` means the package is designed around it. Decisions locked by Phase 1 are recorded here for completeness and marked `INHERITED (Phase 1)`.

---

## ADR-001 — Hybrid retrieval: global knowledge base + per-company overrides

**Status:** INHERITED (Phase 1) — locked, not re-litigated.
**Decision:** Classification knowledge is stored in one global product→account knowledge layer plus per-company override layers. Company layer always wins.
**Evidence:** Cross-company consistency = 0.695 (2,696 multi-company products); within-company weighted ADS = 0.847. Same product, different legitimate account per company (rovinieta: 628 at AGROVIN SUD/VERDEFERM, 635 at NORDLINE TRANS ×55, 6352 at BRIGHT VENDING; company names anonymized for public docs).
**Alternatives rejected:** Global-only classifier (~30% wrong on multi-company products); per-company-only (no cold start for new companies, wastes the 69.5% that *is* shared).

## ADR-002 — RULES_FIRST classification order

**Status:** INHERITED (Phase 1) — locked.
**Decision:** Deterministic lookup → embedding similarity fallback → VAT re-ranking. LLM sits behind all three, Tier 3 only.
**Evidence:** 91.2% of products deterministic (ADS > 0.95); only 1.1% genuinely ambiguous (< 0.50). Decision matrix R3 (≥90% threshold). LLM-per-line would be ~30× cost, 20–50× latency, for no accuracy gain on the deterministic majority.

## ADR-003 — One shared per-company knowledge base for receipts AND D406 invoices

**Status:** ACCEPTED — deliberate divergence from the client spec.
**Decision:** Both pipelines read from and write to the same per-company knowledge base (product catalog + account rules). Ingestion channels differ; intelligence does not. Source provenance (`D406` / `RECEIPT` / `MANUAL`) is an attribute on evidence, not a separate store.
**Alternatives:** Client spec implies a receipts category catalog seeded from D406 — a second categorization system. Rejected: two stores drift; a correction made in the receipts flow would not benefit invoice classification and vice versa. The D406 corpus (76,843 (company, product, account) mappings) is the only training data that exists on day one — receipts must inherit it directly, and receipt corrections must enrich the same store.
**Consequence:** The KB schema must be document-type-agnostic (07_DATA_SCHEMA.md); the D406 pipeline becomes a *feeder* of the shared KB, requiring one integration contract (05, §D406 Sync).

## ADR-004 — Product-level per-company rules primary; category-level fallback; categories are semantic, not VAT-partitioned

**Status:** ACCEPTED — diverges from the client spec.
**Decision:** The primary mapping unit is `(company, canonical product) → (account_id, tax_code)`. Categories exist as a global semantic taxonomy used for cold start and for the associated-products inference the client spec describes — but a category never carries a global account, and category membership is not constrained by VAT rate. Expected VAT per product/category is a *dated attribute* (`effective_from`/`effective_to`).
**Evidence:**
- Cross-company consistency 0.695 forbids category-global accounts (a category→account table shared across companies is just a global classifier wearing a costume).
- VAT-homogeneous categories (client spec: "all products in a category have the same VAT value") fracture on rate changes: Legea 141/2025 moved 19%→21% and 9%→11% in Aug 2025; Phase 1 data contains both 19% (5,577 lines) and 21% (167,659 lines) for the same economic goods. A VAT-partitioned catalog would split every category at the law boundary.
- 5.5% of products legitimately carry 2+ VAT rates — they'd be unrepresentable.
**Alternatives:** Client spec's VAT-partitioned AI categories. Rejected per above.

## ADR-005 — Supplier is a context feature, never a primary classifier

**Status:** ACCEPTED — diverges from the client spec's attribute ordering.
**Decision:** Product description text dominates retrieval and matching. Supplier identity is stored, used for duplicate detection, supplier-specific alias resolution (same chain prints the same abbreviations), and as a weak re-ranking feature — never as the lookup key.
**Evidence:** The worked example itself: Petromax (fuel company, name anonymized) selling a road vignette. In Phase 1 data, one company booked "rovinieta" to 6022 (fuel expense) — the exact error a supplier prior produces. Product-text lookup lands 628/635 correctly.

## ADR-006 — Four-tier confidence cascade governs how predictions surface

**Status:** ACCEPTED (target shape given; this package specifies it).
**Decision:** T1 deterministic/high-ADS → auto-apply; T2 fuzzy/embedding → auto-apply + spot-check flag; T3 LLM/unconfirmed → human review queue; T4 no precedent → manual entry becomes training data. Full spec: 08_CONFIDENCE_CASCADE.md.
**Evidence:** ADS distribution (91.2% / 7.7% / 1.1%) maps directly onto expected tier volumes; the weighted-vs-unweighted gap (0.847 vs 0.964) proves per-product confidence is mandatory — a single model-level confidence would over-trust high-volume ambiguous products.

## ADR-007 — OCR extraction confidence and classification confidence are independent, never collapsed

**Status:** ACCEPTED (hard rule from ground truth).
**Decision:** Every line carries `extraction` confidence (did we read the paper correctly?) and `classification` confidence (do we know where this product goes?) as separate signals with separate thresholds, separate UI indicators, separate alarms. A gate on extraction quality runs *before* classification tiering; low extraction confidence routes to extraction-repair, not to the classification review queue.
**Alternatives:** Single blended score (client spec's ">95% is green"). Rejected: a perfectly-read receipt of an ambiguous product and a badly-read receipt of a deterministic product would get the same score and the same (wrong) remediation.

## ADR-008 — Event-driven correction propagation; no synchronous mass reprocessing

**Status:** ACCEPTED — diverges from the client spec ("all documents would be reprocessed with that change").
**Decision:** A monography/correction change creates a new immutable rule version and emits `knowledge.rule_changed`. An impact worker re-scores only *unexported* documents affected by the rule, asynchronously and rate-limited. Exported/booked documents are never mutated; the new rule applies forward. Full design: 06_EVENT_DRIVEN_WORKFLOW.md.
**Evidence:** Synchronous reprocessing is O(history) on every edit — at Phase 1 scale (296,648 lines historical; growing monthly) a single category edit would trigger six-figure reprocessing, and concurrent edits race. Also an audit problem: booked fiscal records must not silently change.

## ADR-009 — WarehouseID is resolved by per-company configuration, not learned

**Status:** ACCEPTED.
**Decision:** WarehouseID is assigned by a deterministic per-company configuration rule (default warehouse; optional overrides by document type or account class). It is part of the classification *response* but not of the learned knowledge base.
**Evidence:** warehouse_id is 100% missing in all 296,648 D406 lines (decision matrix R5: DROP). There is nothing to learn from. Receipts don't print warehouses either. Where warehouse master data lives (target ERP?) is OPEN-Q5.

## ADR-010 — Per-line VAT bracket letter is the primary VAT allocation signal

**Status:** ACCEPTED — strengthens the client spec.
**Decision:** VAT% per line resolves in order: (1) per-line bracket letter (A/B/…) printed on the receipt, joined to the receipt's `TOTAL TVA <letter> – <rate>%` footer; (2) arithmetic allocation for the spec's enumerated cases (single product; one rate; 2×2 solvable); (3) expected-VAT lookup from the KB; (4) LLM assumption (Tier 3). Arithmetic reconciliation (Σ lines = total ±0.1 RON) always runs as a validator regardless of path.
**Evidence:** The sample Petromax receipt (name anonymized) prints `30.57 A` on the line and `TOTAL TVA A – 21%` in the footer — a deterministic per-line link the client spec ignores. Romanian fiscal printers (Ordinance 28/1999 fiscal device regime) print bracket letters per line as standard. VAT itself remains a secondary *classification* signal (94.5% single-rate, R4) — this ADR is about *extracting* the line's VAT, not about using VAT to pick accounts.

## ADR-011 — Model-agnostic AI orchestration layer; Textract and Haiku are candidates, not commitments

**Status:** ACCEPTED — keeps the vision-notes direction; softens the client spec's vendor picks.
**Decision:** OCR/extraction, embeddings, and LLM reasoning sit behind provider-agnostic interfaces with capability contracts, per-provider adapters, and configuration-driven routing (09_AI_ORCHESTRATION.md). AWS Textract and Claude Haiku are strong first candidates and may well be the pilot choice — but no service may import a vendor SDK outside its adapter.
**Evidence:** Production stack unconfirmed (OPEN-Q1); LLM traffic is only the Tier 3 tail (~5–9% of lines by ADS distribution), so vendor choice is a cost knob; Romanian-language quality across OCR/embedding vendors is unbenchmarked (OPEN-Q13).

## ADR-012 — Receipts capture line amounts and enrich the KB with them; D406-derived rules function without them

**Status:** ACCEPTED.
**Decision:** Receipt lines carry quantity, unit price, and amounts (they exist on paper), and are stored as evidence attributes. No classification rule may *require* an amount, because the D406-derived majority of the KB has none (line_amount 100% missing in D406). Amounts are used for validation (Σ = total) and available as future re-ranking features once receipt-sourced evidence accumulates.

## ADR-013 — Synchronous classify API + asynchronous document pipeline, one shared engine

**Status:** ACCEPTED.
**Decision:** The classification engine is exposed twice: a synchronous `POST /classifications` API (<100ms p95, no LLM in-path — Tier 3 candidates return `PENDING_REVIEW`/`PENDING_LLM` immediately) used by the D406/invoice flow and interactive UI; and the async receipts pipeline where the same engine runs inside workers and LLM batching is allowed. One engine, two invocation modes — prevents the two-pipelines drift the shared-KB mandate exists to stop.
**Evidence:** <100ms latency target is incompatible with LLM calls (seconds); 91.2% deterministic majority makes the sync path viable for nearly all lines.

## ADR-014 — Duplicate detection by document fingerprint with partial-read joining

**Status:** ACCEPTED (adopted from client spec, formalized).
**Decision:** Fingerprint = (issuer CUI, document date+time to the minute, total). Two partial extractions matching on fingerprint merge into one document (client spec's joining rule). Confirmed duplicates are suppressed from review UI. Fingerprint collisions (two genuinely distinct receipts, same minute, same total, same supplier) are flagged, not silently merged, when receipt numbers differ.

## ADR-015 — Global KB layer contains only de-identified pattern data

**Status:** ACCEPTED.
**Decision:** The global layer stores normalized product text, account/tax-code distributions, counts, and ADS — never amounts, supplier-customer relationships, or company identities in retrievable form. Cross-tenant leakage is both a confidentiality and a correctness hazard (0.695 cross-company consistency means another tenant's rule is wrong ~30% of the time anyway).

## ADR-016 — Thresholds are named, versioned configuration

**Status:** ACCEPTED (continues the Phase 1 practice).
**Decision:** All cascade thresholds (T1 ADS ≥ 0.95, evidence ≥ 3, similarity ≥ 0.85, etc.) are named configuration values, versioned, recorded on every classification result, and calibrated during pilot. Phase 1's threshold discipline (decision-matrix named constants) carries into runtime.

---

## Cross-reference: where each divergence from source material is specified

| Divergence | ADR | Specified in |
|---|---|---|
| Shared KB, not parallel catalogs | ADR-003 | 05, 07 |
| Categories semantic, not VAT-partitioned; product-level company rules | ADR-004 | 04, 07 |
| Supplier demoted to context feature | ADR-005 | 08 |
| No mass reprocessing on monography change | ADR-008 | 06 |
| Warehouse from config | ADR-009 | 07, 10 |
| Bracket-letter VAT allocation | ADR-010 | 02, 11 |
| Vendor-agnostic AI layer | ADR-011 | 09 |
| Split sync/async invocation | ADR-013 | 05, 10 |
| Separate OCR vs classification confidence | ADR-007 | 08, 13 |

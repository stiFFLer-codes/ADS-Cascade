# 02 — Business & Functional Requirements: Receipts Classification

> **Status:** Solution Architecture — governing requirements for the Phase 2 receipts pipeline
> **Date:** 2026-07-06
> **Derived from:** Client receipts specification ("Receipts AI"), reconciled against Phase 1 evidence per `00_SCOPE.md` §3. Every divergence from the client spec is marked inline and consolidated in §13.
> **Conventions:** "SHALL" = mandatory, testable. "SHOULD" = strong default, deviation requires an ADR. Technology names appear only as *candidates, pending confirmation* — this document commits to capabilities, not products.

---

## 1. Business Context & Goals

ADS-Cascade serves a Romanian accounting firm that processes documents for a portfolio of client companies. Phase 1 solved automated classification (AccountID, VAT%, TaxCode) for D406 invoices. Phase 2 extends the same intelligence to **fiscal receipts (bonuri fiscale)** — thermal-paper documents issued at point of sale, which in accounting terms are the invoices **under 500 RON that do not appear in e-Factura**.

Today these receipts are keyed into the accounting system by hand. They are numerous, low-value individually, and expensive in aggregate: an accountant re-types supplier, date, totals, and line items, then decides the account, tax code, and (where applicable) warehouse for every line. The goal of this feature is to **automate receipt entry end-to-end**: receive the receipt image, extract its structured content, validate it, classify every product line, and produce an import file for the target accounting system — with the accountant reviewing only what the system is not confident about.

**Business goals (success is measured against `03_NON_FUNCTIONAL_REQUIREMENTS.md`):**

- **G-1** Eliminate manual data entry for the large majority of receipts; the accountant's role shifts from typist to reviewer of flagged exceptions.
- **G-2** Reuse Phase 1 intelligence: one **shared per-company knowledge base** serves both the D406 pipeline and the receipts pipeline. No second catalog is built (divergence D-6, §13).
- **G-3** Make it trivial for client-company employees to submit receipts (WhatsApp photo from the shop counter) while keeping the accountant in control of who may submit for which company.
- **G-4** Keep per-line processing cost within the Phase 1 cost target by answering deterministically wherever possible — Phase 1 showed 91.2% of products classify deterministically; the LLM is a tail worker, not the engine.

**Out of scope for this document:** accuracy/latency/cost targets (`03`), data model (`04`, `07`), service decomposition (`05`), the confidence cascade internals (`08`), and security/GDPR obligations (`12`).

---

## 2. Actors

| Actor | Description | Interactions |
|---|---|---|
| **Accountant / operator** | Employee of the accounting firm. Manages the per-company phone allowlists, imports documents via the frontend, reviews flagged receipts, edits classifications, manages the monography, triggers XML export. | Frontend (all screens), correction feedback loop |
| **Client-company employee** | Employee of one of the firm's client companies (e.g. a driver, a site manager). Photographs receipts and sends them over WhatsApp. Has **no** ADS-Cascade account or UI access. | WhatsApp only (send image, receive Romanian-language replies) |
| **The system (ADS-Cascade receipts pipeline)** | Ingests, extracts, validates, allocates VAT, classifies, and queues receipts; sends WhatsApp replies; learns from corrections via the shared knowledge base. | All of the above, plus external registries |
| **Target accounting / ERP system** | The firm's bookkeeping software. Consumes the generated XML import file. Not integrated bidirectionally in this phase — export is file-based. | XML import (format pending confirmation — see §14) |
| **External registries (ANAF / etva)** | Authoritative source for company VAT status, active status, and CAEN code by CUI. | Monthly refresh (FR-40..FR-42) |

---

## 3. Functional Requirements — Ingestion

### 3.1 WhatsApp Business channel

- **FR-1** The system SHALL receive receipt images via the WhatsApp Business API. The integration route (direct Meta vs. Business Solution Provider partner) is *pending confirmation* (§14).
- **FR-2** The accountant SHALL be able to register, per client company, one or more mobile phone numbers authorized to submit receipts for that company (**allowlist**).
- **FR-3** The same phone number SHALL be permitted on the allowlists of multiple companies simultaneously, with no restriction. When a number is allocated to more than one company, the system SHALL determine the target company for each inbound document; if the target cannot be determined automatically, the document SHALL be queued for the accountant to assign a company before processing continues.
- **FR-4** A message from a number on exactly one company's allowlist SHALL be recorded against that company and enter the extraction pipeline automatically.
- **FR-5** A message from a number **not on any allowlist** SHALL be retained, unprocessed, for **7 days**. If the accountant adds that number to a company's allowlist within the 7-day window, the held messages SHALL be processed for that company as if newly received. After 7 days, held messages SHALL be deleted (retention interplay with GDPR: see `12_SECURITY_COMPLIANCE.md`).
- **FR-6** When a message arrives from an unallocated number, the system SHALL reply with exactly the following Romanian template (client-spec text, adopted verbatim):

  > „Bună ziua!
  > Ați contactat ContAi, asistentul dvs. contabil digital.
  > Numărul dvs. de telefon nu este înregistrat în aplicație și documentele trimise nu pot fi procesate în acest moment.
  > Pentru a obține acces, vă rugăm să contactați contabilul dvs. care vă va înrola în sistem în câteva minute.
  > Vă mulțumim pentru înțelegere!"

- **FR-7** When a submitted receipt is processed and validated successfully, the system SHALL send the sender a Romanian-language confirmation that the receipt was registered, including at minimum supplier name, total, and date. Template text SHALL be configurable per the firm's wording.
- **FR-8** All system-initiated WhatsApp replies SHALL use pre-approved Romanian message templates and SHALL be sent within the messaging window that avoids per-message conversation charges where the platform's pricing rules allow (the client spec targets reply-within-1-hour for the free service window).

### 3.2 Frontend import

- **FR-9** The accountant SHALL be able to import receipt documents through the frontend: select the client company from a dropdown, then add files by drag-and-drop, file picker, or paste.
- **FR-10** Frontend-imported documents SHALL follow the identical processing path as WhatsApp documents (extraction → validation → VAT allocation → classification), differing only in the failure channel: failures surface in the report for user fill-in (FR-22) instead of a WhatsApp resend request.

### 3.3 Local folder ingestion

- **FR-11** The system SHALL support ingesting receipt files deposited in a designated local/network folder per company, entering the same pipeline as FR-10. Folder location, polling mechanism, and company-mapping convention are deployment configuration (*pending stack confirmation*).

---

## 4. Functional Requirements — Extraction

- **FR-12** For every ingested receipt image, the system SHALL extract the following fields. "Required" means extraction failure for that field makes the document invalid (§5); "Optional" fields are extracted when present.

| # | Field | Requirement | Notes |
|---|---|---|---|
| 1 | Supplier name | Required | |
| 2 | Issuer CUI | Required | Format "RO" + number; the numeric part alone SHALL also be accepted and normalized |
| 3 | Receiver CUI | Optional | Same format |
| 4 | Total | Required | Numeric |
| 5 | VAT value per rate | Required | One amount per VAT percentage printed on the receipt |
| 6 | Payment method | Required | Recognize Romanian variants: *cash*, *numerar*, *card*, *carte credit*, *card bancar*; capture sub-details when printed (contactless, Mastercard, Visa) |
| 7 | Product lines | Required | Description, line value |
| 8 | Price per unit of measure | Required | Per line |
| 9 | Quantity | Required | Per line |
| 10 | Unit of measure | Required | Per line |
| 11 | Document date | **Month required**; day/time optional, extracted when present | |
| 12 | Receipt number | Required when printed | Used for duplicate joining (FR-19) |
| 13 | **Per-line VAT bracket letter (A/B/…)** | Required **when printed** | **Divergence D-1** — see below |
| 14 | Other printed data | Optional | Retained as raw text for audit |

- **FR-13 (Divergence D-1 — addition to the client spec).** Romanian fiscal receipts print a **VAT bracket letter per product line** (e.g. `30,57 A`) and a matching totals block (`TOTAL TVA A – 21%`). The system SHALL extract the bracket letter for each line when present and SHALL extract the bracket-letter→rate legend from the totals block. This letter **deterministically** links a line to a VAT rate and is the primary VAT-allocation signal (FR-25). Evidence: the sample Petromax receipt (name anonymized) shows exactly this structure; the client spec omits it and jumps to arithmetic/LLM inference.
- **FR-14** The extraction component SHALL be provider-agnostic. OCR/structuring candidates: **AWS Textract + LLM structuring** (client proposal), **a document-AI service**, or **a multimodal LLM reading the image directly** — 2–3 candidates behind one interface, *pending stack confirmation* (`09_AI_ORCHESTRATION.md`).
- **FR-15** Every extracted field SHALL carry a per-field **extraction confidence** score, aggregated to a document-level extraction confidence. This score is reported separately from classification confidence and is never merged with it (FR-36, hard rule).

---

## 5. Functional Requirements — Validation

- **FR-16** A receipt SHALL be marked **valid** only if (a) all required fields in FR-12 were extracted, and (b) the arithmetic check FR-17 passes.
- **FR-17** The system SHALL verify that the sum of extracted product-line values equals the extracted receipt total within **±0.1 RON**; a discrepancy up to 1 RON MAY be accepted with a flag (needs-verification), and a discrepancy **greater than 1 RON SHALL never validate**.
- **FR-18** A receipt that fails validation SHALL first be checked against already-received documents for the same company: a successfully processed document with the same date, hour:minute(:second where available), same total, and same supplier SHALL cause the failing document to be treated as a duplicate (not surfaced; FR-38). If similar documents are still in the queue, the system SHALL wait until they finish processing before deciding.
- **FR-19 (Duplicate-document joining).** When two partial reads of the same physical receipt each fail validation but together cover the required fields, the system SHALL merge them into one validated document, provided **all** of the following match across both reads: receipt number, date, hour:minute, and total value.
- **FR-20** For a WhatsApp-sourced receipt that fails validation and cannot be joined or matched to a validated duplicate, the system SHALL send the sender a Romanian-language resend request naming the supplier, value, and date (as far as extracted) and stating that the document was unreadable.
- **FR-21** Resend requests SHALL be sent only after in-queue processing settles (FR-18), and within the timing constraint of FR-8.
- **FR-22** For a frontend-imported receipt that fails validation, the system SHALL display the extracted data alongside the document image and allow the accountant to fill in missing/incorrect fields or re-import the file. Bad frontend imports SHALL appear in the report immediately (validation-issue status), ahead of silent retry.

---

## 6. Functional Requirements — VAT Allocation (per line)

Once a receipt is validated, every product line must be assigned its VAT rate. **The order below is a divergence (D-2) from the client spec:** the spec starts at arithmetic cases and ends at the LLM; this document inserts the printed bracket letter as step one, because it is deterministic where every later step is inferential.

- **FR-23** The system SHALL resolve per-line VAT in the following strict order, stopping at the first step that yields an answer:
  1. **Bracket letter (deterministic).** If the line carries a VAT bracket letter and the totals block defines that letter's rate (FR-13), the line's VAT rate is that rate. No inference.
  2. **Arithmetic reconciliation.** The client spec's case logic, used as solver and as validator of step 1:
     - single product → the receipt's single VAT rate applies;
     - multiple products, one VAT rate in totals → that rate applies to all lines;
     - two products, two VAT rates → solve the 2×2 system arithmetically (which line at which rate makes the per-rate VAT totals balance);
     - N products, two rates → proceed to step 3 for the lines arithmetic cannot pin down.
  3. **Catalog elimination.** Look up each unresolved line in the shared per-company knowledge base; lines with a known VAT attribute are eliminated, and the arithmetic of step 2 is re-run on the remainder.
  4. **LLM inference (Tier 3, last resort).** Only lines still unresolved are sent to the reasoning layer for VAT assumption, batched per `09_AI_ORCHESTRATION.md`. LLM-assigned VAT SHALL be marked as inferred and priced against the arithmetic residual as a sanity check.
- **FR-24** Per-rate VAT amounts computed from allocated lines SHALL reconcile with the receipt's printed per-rate VAT totals within the FR-17 tolerance; failure demotes the document to needs-verification.
- **FR-25** VAT rates SHALL be validated against the rate set legally in force at the **document date**: currently **21% standard and 11% reduced (Legea 141/2025, effective August 2025)**; 19%/9%/5% SHALL be accepted only for documents dated before the transition. VAT is stored as a **dated attribute with effective ranges**, never as a partitioning key of the catalog (divergence D-4).

---

## 7. Functional Requirements — Classification

- **FR-26** For every validated product line, the system SHALL produce four outputs: **AccountID**, **VAT%**, **TaxCode**, and **WarehouseID**.
- **FR-27** AccountID, VAT%, and TaxCode SHALL be resolved through the **shared per-company knowledge base** using the **four-tier confidence cascade specified in `08_CONFIDENCE_CASCADE.md`** (company rule → global catalog → similarity retrieval → LLM). This document does not re-specify the cascade; the binding requirement is that receipts lines and D406 lines traverse the *same* cascade against the *same* knowledge base.
- **FR-28** Per-company mappings SHALL take precedence over global mappings (Phase 1 evidence: cross-company consistency 0.695 — the same product legitimately books to different accounts in ~30% of multi-company cases).
- **FR-29 (Divergence D-7).** **WarehouseID SHALL be resolved from per-company configuration rules, not learned from history** — warehouse_id is 100% missing in the D406 corpus, so there is no signal to learn from. Companies with no warehouse configuration SHALL receive a configured default or an empty value per the export schema (*pending confirmation*, §14).
- **FR-30** Every classified line SHALL carry a **classification confidence** score computed per line (Phase 1: ADS weighted 0.847 vs unweighted 0.964 proves confidence varies by product, not by model), driving the review workflow and the colour coding of FR-36.
- **FR-31** Accountant corrections to any line's classification SHALL be written back to the per-company knowledge base as feedback events (`06_EVENT_DRIVEN_WORKFLOW.md`); a correction SHALL affect future classifications and lazy re-scoring of **unexported** documents only — never a synchronous reprocessing of all documents (divergence D-8).

---

## 8. Functional Requirements — Knowledge Base Seeding

- **FR-32** Before receipt processing goes live for a company, the system SHALL bootstrap that company's knowledge base from its existing D406 data: all invoice lines from documents **< 500 RON and not present in e-Factura** (the population that corresponds to receipts), carrying product description, VAT (from tax code), supplier, unit of measure, unit price, AccountID, and TaxCode.
- **FR-33 (Divergence D-6).** There SHALL be **one shared per-company knowledge base** used by both the D406 pipeline and the receipts pipeline. The client spec's separately built receipts category catalog (seeded from, but parallel to, D406 data) is rejected: two catalogs answering the same question drift apart, and Phase 1 located the system's intelligence in a single catalog (91.2% deterministic).
- **FR-34 (Divergence D-5).** Categories in the knowledge base are **semantic groupings**; they SHALL NOT be constrained to a single VAT value ("all products in a category share one VAT" per the client spec). Rationale: VAT-homogeneous categories fracture whenever rates change by law (Legea 141/2025 moved 19→21% and 9→11% in one month) and cannot host legitimately multi-rate products. Account mappings attach **per company at product level first**, with category-level mappings only as the cold-start fallback (ADS 0.847/0.964; cross-company 0.695 forbids category-global accounts).
- **FR-35** The e-Factura membership check needed by FR-32 ("not present in e-Factura") SHALL be performed against the firm's e-Factura data source; the lookup mechanism is *pending confirmation* (§14).

---

## 9. Functional Requirements — Frontend & Reporting

- **FR-36** The frontend SHALL provide a report under **"Procesare documente" → "Receipts"** with:
  - **Filters:** Month, Client.
  - **Columns:** client name, document number, supplier name, document date, total value (incl. VAT), currency, **recognition status** (extraction quality), **processing status** — one of *processed*, *in queue*, *validation issue*, *needs verification* — and Actions.
  - **Actions:** *see/edit* (opens the document detail: all product lines with quantity, unit of measure, unit value, line total, document total; editable values, AccountID, TaxCode; option to create a per-company context for an alternative registration) and *delete document*.
  - **Confidence colour coding:** confidence above 95% renders green, with graduated colours below (exact bands per `08_CONFIDENCE_CASCADE.md` thresholds; 0.95/0.85 are Phase 1-derived starting points, pilot-calibrated).
  - **Hard rule (Divergence D-9):** the report and detail views SHALL display **extraction confidence and classification confidence as two separate indicators, never one collapsed score.** A perfectly-read receipt with an uncertain account and a barely-legible receipt with an obvious account are different problems requiring different operator actions.
- **FR-37** The frontend SHALL provide, from the same report: (a) an **Import** button implementing FR-9; (b) a **Monography** view showing, per client, how receipts are being recorded per category with AccountID and TaxCode, where each category offers a dropdown of **recommended code / follow historic way / new method** — applying a change emits a correction/configuration event per FR-31 (no mass reprocessing); (c) an **XML export** control listing all clients that have receipts, allowing selection of one, a custom set, or all, and a Generate action producing the accounting-system import XML for the selected clients' processed receipts.
- **FR-38 (Duplicates & filtering).** The frontend SHALL NOT surface for approval: (a) **duplicates** — a document on the same date with the same value as an already-validated document, whether the second copy validated or errored; and (b) documents originating from **unauthorized sources** (numbers outside all allowlists, FR-5–FR-6). Both remain queryable in an audit view but never enter the review queue.
- **FR-39** Exported documents SHALL be marked as exported and excluded from lazy re-scoring (FR-31); re-export of a corrected document SHALL be an explicit accountant action.

---

## 10. Functional Requirements — CAEN Recognition

- **FR-40** For every client company in the accountant's portfolio, the system SHALL query the etva/ANAF service to retrieve and store: **VAT-payer status**, **active status**, and **CAEN code**.
- **FR-41** These attributes SHALL be refreshed **monthly** per company, with the retrieval date stored; stale data (missed refresh) SHALL be flagged to the operator.
- **FR-42** CAEN code and VAT status SHALL be available to the classification context (a company's line of business is a classification prior — e.g. fuel is stock for a transport company and expense for an office), and issuer-CUI lookups SHALL use the same service to resolve supplier names (FR-12 field 1 cross-check). API access, rate limits, and terms are *pending confirmation* (§14).

---

## 11. Traceability note

Every FR above maps to a client-spec paragraph or to a divergence in §13; `DECISIONS.md` carries one ADR per divergence. NFR counterparts (accuracy floors per tier, latency of the WhatsApp reply loop, cost per line, availability) live in `03_NON_FUNCTIONAL_REQUIREMENTS.md`.

---

## 12. Explicitly out of scope (this feature)

- Bidirectional ERP integration (export is file-based XML in this phase).
- Receipts ≥ 500 RON or documents present in e-Factura (they remain D406/e-Factura pipeline territory).
- End-user (client-company employee) UI beyond WhatsApp conversations.
- Multi-currency conversion — currency is captured and reported (FR-36) but receipts are expected in RON; non-RON handling is an open question (§14).

---

## 13. Divergences from the client spec

| # | Client spec says | This document says | Evidence (one line) |
|---|---|---|---|
| **D-1** | Extract totals-level VAT only; per-line rate is inferred | Extract the **per-line VAT bracket letter (A/B)** and its legend whenever printed (FR-13) | Sample receipt prints `30,57 A` ↔ `TOTAL TVA A – 21%` — a deterministic per-line link the spec ignores |
| **D-2** | VAT allocation: arithmetic cases, then catalog, then Haiku | Order: **bracket letter first**, arithmetic second, catalog third, LLM last (FR-23) | 91.2% of products are deterministic — exhaust deterministic signals before any inference |
| **D-3** | Supplier is a primary categorization attribute | Supplier is a **weak, secondary** signal; product description dominates | Petromax receipt (name anonymized): fuel supplier, non-fuel line — one company misbooked rovinieta to 6022 Fuel, the exact supplier-prior error |
| **D-4** | VAT value is a defining attribute of categories | VAT is a **dated attribute with effective ranges**, never a partitioning key (FR-25) | Legea 141/2025 changed 19→21% and 9→11% in Aug 2025; any VAT-partitioned structure fractures at a law change |
| **D-5** | All products in a category share one VAT; category carries the AccountID | Categories are semantic; **mappings are per-company at product level first**, category as cold-start fallback (FR-34) | Cross-company consistency 0.695 — category-global accounts are wrong ~30% of the time; ADS weighted 0.847 vs unweighted 0.964 shows confidence lives at product level |
| **D-6** | Build a receipts category catalog, seeded from D406 | **One shared per-company knowledge base** for both pipelines; no parallel catalog (FR-32–FR-33) | Two catalogs answering one question drift; the single catalog is the system's center of gravity (91.2% deterministic) |
| **D-7** | (Implied) all four outputs learned from data | **WarehouseID is configuration-resolved, not learned** (FR-29) | warehouse_id is 100% missing in D406 — no historical signal exists to learn from |
| **D-8** | Monography change ⇒ "all documents would be reprocessed" | **Event-driven propagation; lazy re-scoring of unexported documents only** (FR-31, FR-37b) | "Reprocess all documents" is a scale trap — cost and latency grow with corpus size; events decouple correction from corpus |
| **D-9** | One quality indicator ("nivel de încredere peste 95% este verde") | **Extraction confidence and classification confidence are separate indicators, never collapsed** (FR-15, FR-36) | ADS divergence (0.847 weighted / 0.964 unweighted) proves confidence must be computed per signal; receipts add an extraction dimension D406 XML never had |
| **D-10** | Textract + "NPL", Haiku — named as the technology | Both kept only as **candidates behind provider-agnostic interfaces**, LLM invoked at Tier 3 only | VAT 94.5% single-rate and 91.2% deterministic mean the LLM sees a few % of lines — vendor choice is a cost knob, not an architectural commitment |

---

## 14. Open questions surfaced by this document

(Consolidated with impact and defaults in `OPEN_QUESTIONS.md`; listed here as raised by these requirements.)

1. **WhatsApp route** — direct Meta vs. BSP partner; affects FR-1, FR-8 template approval flow and pricing window.
2. **Multi-company numbers (FR-3)** — what disambiguation does the firm want when one number serves several companies: sender chooses via reply, accountant assigns, or per-conversation default?
3. **7-day hold vs. GDPR (FR-5)** — is 7-day retention of images from unknown senders acceptable under the firm's GDPR posture, and is deletion-after-7-days sufficient?
4. **e-Factura lookup (FR-35)** — what is the authoritative mechanism for "< 500 RON and not in e-Factura" during KB seeding and ongoing operation?
5. **etva/ANAF access (FR-40–FR-42)** — API availability, rate limits, and contractual terms for monthly portfolio-wide refresh and per-receipt CUI resolution.
6. **XML export schema (FR-37c)** — which accounting system(s), which import schema, and does it require a WarehouseID for receipt bookings at all (bears directly on FR-29)?
7. **Warehouse usage (FR-29)** — do any portfolio companies actually book receipts against warehouses, and where does warehouse master data live?
8. **Non-RON receipts (§12)** — do employees ever submit foreign receipts, and if so are they in scope or explicitly rejected?
9. **Volume (FR-8, cost model)** — expected receipts per company per month; drives batching, the WhatsApp reply-timing design, and `14_COST_MODEL.md`.
10. **Confidence thresholds (FR-36)** — 0.95/0.85 are Phase 1-derived starting points; the pilot must calibrate green/amber/red bands on real receipt traffic.
11. **Confirmation template wording (FR-7)** — the success-reply text is "custom text" in the client spec; final Romanian wording needs the firm's sign-off (the rejection template FR-6 is already fixed verbatim).
12. **Local folder ingestion (FR-11)** — folder topology, company mapping convention, and polling vs. event-driven pickup, pending production stack confirmation.

---

*Requirements complete. Non-functional counterparts follow in `03_NON_FUNCTIONAL_REQUIREMENTS.md`.*

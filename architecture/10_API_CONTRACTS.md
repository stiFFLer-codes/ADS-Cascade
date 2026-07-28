# 10 — API Contracts

Contract stubs for the core surfaces. Style: REST/JSON for illustration; the shapes are the contract, transport is stack-dependent (OPEN-Q1). All endpoints: authenticated, authorized per `company` scope (12), idempotency keys on mutating calls, `correlation_id` propagated.

Errors follow one envelope: `{error: {code, message, details[]}}` with stable machine codes (`COMPANY_NOT_FOUND`, `ACCOUNT_NOT_IN_CHART`, `VALIDATION_SUM_MISMATCH`, …).

---

## 1. Classification API (the core endpoint — ADR-013 sync mode)

### `POST /v1/companies/{cui}/classifications`

Classify one or more lines synchronously. **p95 < 100ms; never invokes an LLM.** Used by interactive UI, the D406/invoice flow, and re-scoring.

**Request**

```json
{
  "options": { "include_alternatives": true, "max_alternatives": 3 },
  "lines": [
    {
      "line_ref": "doc-7f3a/line-1",
      "text": "ROVINIETA - A - AUTOTURISME",
      "direction": "PURCHASE",
      "vat_percent": 21.0,
      "vat_bracket_letter": "A",
      "supplier_cui": "RO90012345",
      "quantity": 1,
      "unit_price": 30.57,
      "line_amount": 30.57,
      "document_context": {
        "doc_type": "RECEIPT",
        "document_date": "2026-03-16",
        "payment_method": "NUMERAR"
      }
    }
  ]
}
```

`text` is required; everything else optional (D406-sourced callers have no amounts — ADR-012; 4.05% of lines lack VAT and must still classify).

**Response — Tier 1 (company with rovinieta precedent)**

```json
{
  "results": [
    {
      "line_ref": "doc-7f3a/line-1",
      "status": "CLASSIFIED",
      "classification": {
        "account_id": "635",
        "tax_code": "301104",
        "vat_percent": 21.0,
        "warehouse_id": null
      },
      "tier": 1,
      "method": "COMPANY_RULE",
      "classification_confidence": 1.0,
      "flags": [],
      "evidence": {
        "product": { "product_id": "prd_rovinieta", "canonical_text": "rovinieta", "matched_via": "ALIAS" },
        "rule": { "rule_id": "rul_9c21", "version": 4, "ads": 1.0, "evidence_count": 55,
                   "origin": "D406_HISTORY", "last_seen": "2026-04-28" },
        "vat_source": "BRACKET_LETTER",
        "warehouse_source": "COMPANY_CONFIG_DEFAULT"
      },
      "alternatives": [
        { "account_id": "628", "tax_code": "301104", "basis": "GLOBAL_PATTERN", "support": 0.41 }
      ],
      "config_versions": { "thresholds": "v1", "embedding_model": "emb-2026-01", "engine": "cls-1.3" }
    }
  ]
}
```

**Response — Tier 3 (no precedent; async proposal to follow)**

```json
{
  "results": [
    {
      "line_ref": "doc-7f3a/line-1",
      "status": "PENDING_REVIEW",
      "tier": 3,
      "reason": "GLOBAL_PATTERN_SPLIT",
      "candidates": [
        { "account_id": "635", "description": "CHELT. CU ALTE IMPOZITE, TAXE...", "basis": "GLOBAL_PATTERN", "support": 0.45, "company_count": 9 },
        { "account_id": "628", "description": "ALTE CHELT. CU SERVICIILE...",    "basis": "GLOBAL_PATTERN", "support": 0.41, "company_count": 11 },
        { "account_id": "6352", "description": "IMPOZITE, TAXE SI VARSAMINTE DIVERSE", "basis": "GLOBAL_PATTERN", "support": 0.12, "company_count": 1 }
      ],
      "resolved_fields": { "vat_percent": 21.0, "warehouse_id": null },
      "review_item_id": "rev_5510"
    }
  ]
}
```

Contract invariants:
- Response always carries `tier`, `method`, `classification_confidence`, full `evidence` — auditability is part of the contract, not a log.
- `classification_confidence` never reflects extraction quality; extraction confidence travels on document endpoints only (ADR-007).
- Proposed `account_id` is guaranteed to exist in the company's GL chart.
- `vat_percent` and `warehouse_id` are always resolved (VAT via bracket → arithmetic → KB expectation; warehouse via config), even when the account is `PENDING_REVIEW` — partial answers are explicit, never silently defaulted.

---

## 2. Document ingestion & lifecycle

```
POST /v1/companies/{cui}/documents            multipart image or {image_ref}; channel; idempotency-key
  → 202 { document_id, status: "RECEIVED", correlation_id }

GET  /v1/companies/{cui}/documents?month=&status=&supplier=   — the frontend report (client spec fields)
GET  /v1/companies/{cui}/documents/{id}
  → { document, extraction: { version, extraction_confidence, fields, validation },
      lines: [ { line, classification (current version), both confidences SEPARATE } ] }

POST /v1/companies/{cui}/documents/{id}/fields     — frontend fill-in for failed extraction
DELETE /v1/companies/{cui}/documents/{id}          — spec's delete action (blocked once EXPORTED)
```

WhatsApp webhook is internal to Ingestion (signature-verified; not a public contract here).

## 3. Review & corrections

```
GET  /v1/companies/{cui}/review-items?status=OPEN&tier=
  → items with candidates, evidence, extraction_confidence AND classification_confidence

POST /v1/review-items/{id}/resolve
  { "action": "ACCEPT" | "OVERRIDE",
    "classification": { "account_id": "635", "tax_code": "301104", "vat_percent": 21.0, "warehouse_id": null },
    "reason_code": "COMPANY_POLICY" }
  → 200; emits classification.confirmed or correction.submitted (learning loop, 06)
```

## 4. Knowledge base & monography

```
GET  /v1/companies/{cui}/monography
  → per category/product: current rule (account, tax_code), origin, ads, evidence_count,
    options: RECOMMENDED | FOLLOW_HISTORIC | NEW_METHOD (client spec)

PUT  /v1/companies/{cui}/rules
  { "scope": "PRODUCT", "product_id": "prd_rovinieta", "direction": "PURCHASE",
    "account_id": "635", "tax_code": "301104" }
  → 200 { rule_id, version }   — creates a NEW VERSION; emits knowledge.rule_changed;
                                  propagation is async & scoped (ADR-008). Response includes
                                  { "impact": { "unexported_lines_to_rescore": 12, "exported_untouched": true } }

GET  /v1/companies/{cui}/rules?product=&status=
GET  /v1/global/patterns?product=rovinieta          — de-identified distribution only (ADR-015)
PUT  /v1/companies/{cui}/warehouse-config           — ADR-009
```

## 5. KB evidence sync (D406 pipeline feeder — ADR-003)

```
PUT /v1/kb/companies/{cui}/evidence:batch           — idempotent bulk upsert
  { "source_type": "D406_SYNC", "batch_id": "d406-2026-06",
    "records": [ { "normalized_product": "rovinieta", "direction": "PURCHASE",
                   "account_id": "635", "tax_code": "301104", "count": 55,
                   "first_seen": "2025-09-22", "last_seen": "2026-04-28" } ] }
  → 200 { accepted, products_created, rules_recomputed }
```

Same contract seeds day one (76,843 mappings) and runs on every future D406 filing cycle — the invoice pipeline and receipts pipeline stay coupled to one KB by construction.

## 6. Exports

```
POST /v1/export-batches   { "company_ids": ["..."] | "ALL", "period": "2026-03" }
  → 202 { batch_id }      — freezes included documents (ADR-008)
GET  /v1/export-batches/{id}          → status + xml_ref download URL
```

Target XML schema: OPEN-Q10.

---

## 7. Versioning & compatibility

URL-versioned (`/v1`); additive changes only within a version; response fields never repurposed. `config_versions` in every classification response ties results to threshold/model/prompt versions for reproducibility (ADR-016).

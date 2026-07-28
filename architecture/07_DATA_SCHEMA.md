# 07 — Data & Schema Design: Knowledge Base and Product Catalog

Logical schema in ANSI-ish DDL — an architecture artifact, engine-agnostic (candidates: PostgreSQL / MySQL / SQL Server, pending OPEN-Q1). `VECTOR` columns denote the embedding index, which may live in-database (pgvector) or in a dedicated store (Qdrant, OpenSearch k-NN) behind the KB service — the *contract* is identical (OPEN-Q3).

Conventions: `id` columns are surrogate keys (UUID or bigint per stack); `TIMESTAMPTZ` everywhere; soft history via append-only versions, never in-place mutation of rules or results.

---

## 1. Tenant & configuration

```sql
CREATE TABLE company (
    company_id        PK,
    cui               TEXT NOT NULL UNIQUE,          -- 'RO12345678'
    name              TEXT NOT NULL,
    caen_code         TEXT,                          -- refreshed monthly (etva/ANAF)
    vat_payer_status  TEXT,                          -- refreshed monthly
    active_status     TEXT,
    settings          JSONB NOT NULL DEFAULT '{}',   -- batching mode, threshold overrides
    created_at        TIMESTAMPTZ NOT NULL
);

CREATE TABLE authorized_sender (
    sender_id      PK,
    company_id     FK -> company NOT NULL,
    phone_e164     TEXT NOT NULL,
    added_by       TEXT NOT NULL,
    active         BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (company_id, phone_e164)                  -- same phone OK across companies
);

CREATE TABLE gl_account (                            -- mirror of company chart of accounts
    company_id    FK -> company NOT NULL,
    account_id    TEXT NOT NULL,                     -- '635', '6022', '4093...'
    description   TEXT,
    account_type  TEXT,                              -- 'Activ' / 'Pasiv' (validation layer)
    source        TEXT NOT NULL,                     -- 'D406_GL' | 'MANUAL'
    PRIMARY KEY (company_id, account_id)
);

CREATE TABLE warehouse_config (                      -- ADR-009: config, never learned
    company_id            FK -> company NOT NULL,
    default_warehouse_id  TEXT,                      -- may be NULL: company doesn't use warehouses
    overrides             JSONB NOT NULL DEFAULT '[]',
      -- [{"match": {"doc_type": "RECEIPT"}, "warehouse_id": "..."},
      --  {"match": {"account_class": "3xx"}, "warehouse_id": "..."}]
    PRIMARY KEY (company_id)
);
```

## 2. Product catalog (global) — the center of gravity

```sql
CREATE TABLE product (
    product_id      PK,
    canonical_text  TEXT NOT NULL UNIQUE,            -- 'rovinieta' (normalized form)
    display_name    TEXT,                            -- generic description (LLM-suggested, human-editable)
    category_id     FK -> category NULL,
    global_ads      NUMERIC(5,4),                    -- recomputed batch job
    company_count   INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL,
    origin          TEXT NOT NULL                    -- 'D406_SEED' | 'RECEIPT' | 'MANUAL'
);

CREATE TABLE product_alias (
    alias_id         PK,
    product_id       FK -> product NOT NULL,
    alias_text       TEXT NOT NULL,                  -- 'rovigneta', 'rovinieta conform anexa'
    supplier_cui     TEXT NULL,                      -- scoped alias: this supplier prints this form
    confidence       NUMERIC(5,4) NOT NULL,          -- 1.0 = human-confirmed
    origin           TEXT NOT NULL,                  -- 'NORMALIZATION' | 'EMBEDDING_PROMOTED' | 'MANUAL'
    UNIQUE (alias_text, COALESCE(supplier_cui, ''))
);
-- Alias resolution turns yesterday's fuzzy match into today's deterministic hit:
-- an embedding match confirmed by a human is promoted to an alias row.

CREATE TABLE category (                              -- semantic taxonomy, ADR-004:
    category_id   PK,                                -- no account, no VAT partition
    name          TEXT NOT NULL,                     -- 'Taxe de drum'
    parent_id     FK -> category NULL,
    origin        TEXT NOT NULL                      -- 'SEED_TAXONOMY' | 'LLM_PROPOSED' | 'MANUAL'
);

CREATE TABLE product_expected_vat (                  -- dated attribute, ADR-004
    product_id     FK -> product NOT NULL,
    vat_percent    NUMERIC(5,2) NOT NULL,            -- 21.00 (19.00 rows closed at 2025-08)
    effective_from DATE NOT NULL,
    effective_to   DATE NULL,
    share          NUMERIC(5,4),                     -- for the 5.5% multi-rate products
    PRIMARY KEY (product_id, vat_percent, effective_from)
);

CREATE TABLE product_embedding (                     -- or external vector store, same contract
    product_id     FK -> product NOT NULL,
    model_id       TEXT NOT NULL,                    -- embeddings are model-versioned (09)
    embedding      VECTOR NOT NULL,
    updated_at     TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (product_id, model_id)
);
```

## 3. Knowledge base — per-company rules, evidence, global patterns

```sql
CREATE TABLE company_account_rule (
    rule_id        PK,
    company_id     FK -> company NOT NULL,
    version        INT NOT NULL,
    scope          TEXT NOT NULL,                    -- 'PRODUCT' (primary) | 'CATEGORY' (fallback)
    product_id     FK -> product NULL,
    category_id    FK -> category NULL,              -- exactly one of the two, per scope
    direction      TEXT NOT NULL,                    -- 'PURCHASE' | 'SALE' | 'ANY'
    account_id     TEXT NOT NULL,                    -- FK (company_id, account_id) -> gl_account
    tax_code       TEXT NOT NULL,                    -- '301104'
    ads            NUMERIC(5,4) NOT NULL,            -- within-company determinism (derived)
    evidence_count INT NOT NULL,
    last_seen      TIMESTAMPTZ,
    origin         TEXT NOT NULL,                    -- 'D406_HISTORY'|'CORRECTION'|'MANUAL_MONOGRAPHY'|'COLD_START_GLOBAL'
    status         TEXT NOT NULL,                    -- 'ACTIVE'|'SUPERSEDED'|'CONFLICTED'
    created_at     TIMESTAMPTZ NOT NULL,
    created_by     TEXT NOT NULL                     -- user or 'knowledge-lifecycle'
);
-- Invariants (enforced by Knowledge Lifecycle service, single writer):
--   * at most one ACTIVE row per (company_id, product_id, direction) for scope=PRODUCT
--   * versions are append-only; supersede, never UPDATE mapping fields
CREATE UNIQUE INDEX uq_active_product_rule
    ON company_account_rule (company_id, product_id, direction)
    WHERE status = 'ACTIVE' AND scope = 'PRODUCT';
CREATE INDEX ix_rule_lookup                          -- the <10ms deterministic path
    ON company_account_rule (company_id, product_id, direction, status);

CREATE TABLE kb_evidence (                           -- append-only observations
    evidence_id    PK,
    company_id     FK -> company NOT NULL,
    product_id     FK -> product NOT NULL,
    direction      TEXT NOT NULL,
    account_id     TEXT NOT NULL,
    tax_code       TEXT,
    vat_percent    NUMERIC(5,2),
    source_type    TEXT NOT NULL,                    -- 'D406_SYNC'|'RECEIPT_CONFIRMED'|'CORRECTION'|'MANUAL'
    source_ref     TEXT,                             -- document/line id or D406 batch id
    observed_at    TIMESTAMPTZ NOT NULL,
    weight         NUMERIC(6,2) NOT NULL DEFAULT 1   -- D406 bulk rows carry count as weight
);
CREATE INDEX ix_evidence_agg ON kb_evidence (company_id, product_id, direction);
-- ADS per (company, product, direction) = max(account share) over weighted evidence;
-- recomputed incrementally on append, exactly the Phase 1 ADS definition.

CREATE TABLE global_pattern (                        -- de-identified, ADR-015
    product_id       FK -> product NOT NULL,
    direction        TEXT NOT NULL,
    account_distribution JSONB NOT NULL,             -- {"628": 41, "635": 62, "6352": 18, "471": 2}
    global_ads       NUMERIC(5,4) NOT NULL,          -- rovinieta/PURCHASE: ~0.45 → never auto-applies
    company_count    INT NOT NULL,
    recomputed_at    TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (product_id, direction)
    -- NO amounts, NO company ids, NO supplier links. Enforced by build job, audited.
);
```

## 4. Documents, extraction, classification

```sql
CREATE TABLE document (
    document_id     PK,
    company_id      FK -> company NOT NULL,
    doc_type        TEXT NOT NULL,                   -- 'RECEIPT'|'D406_SOURCE'|'MANUAL'
    channel         TEXT NOT NULL,                   -- 'WHATSAPP'|'FRONTEND_IMPORT'|'FOLDER'|'D406_SYNC'
    supplier_cui    TEXT,
    supplier_name   TEXT,
    receipt_number  TEXT,
    document_datetime TIMESTAMPTZ,
    total_amount    NUMERIC(14,2),
    currency        TEXT DEFAULT 'RON',
    payment_method  TEXT,                            -- 'NUMERAR'|'CARD'|...
    vat_totals      JSONB,                           -- [{"bracket":"A","rate":21.00,"vat":5.31}]
    fingerprint     TEXT,                            -- hash(supplier_cui|datetime_minute|total)  ADR-014
    status          TEXT NOT NULL,                   -- lifecycle in 04 §3
    image_ref       TEXT,                            -- object storage key; never bytes in DB
    sender_ref      TEXT,                            -- pseudonymized sender (12_SECURITY)
    created_at      TIMESTAMPTZ NOT NULL
);
CREATE INDEX ix_doc_fingerprint ON document (company_id, fingerprint);
CREATE INDEX ix_doc_status ON document (company_id, status, document_datetime);

CREATE TABLE extraction_result (
    extraction_id   PK,
    document_id     FK -> document NOT NULL,
    version         INT NOT NULL,
    provider        TEXT NOT NULL,                   -- adapter id (09)
    provider_model  TEXT,
    fields          JSONB NOT NULL,                  -- per-field values + per-field confidence
    extraction_confidence NUMERIC(5,4) NOT NULL,     -- independent signal (ADR-007)
    validation      JSONB,                           -- {"sum_check": "PASS", "delta": 0.00, ...}
    created_at      TIMESTAMPTZ NOT NULL,
    UNIQUE (document_id, version)
);

CREATE TABLE document_line (
    line_id         PK,
    document_id     FK -> document NOT NULL,
    line_no         INT NOT NULL,
    raw_text        TEXT NOT NULL,                   -- 'ROVINIETA - A - AUTOTURISME'
    normalized_text TEXT NOT NULL,                   -- 'rovinieta a autoturisme'
    product_id      FK -> product NULL,              -- resolved canonical product
    quantity        NUMERIC(14,3),
    unit_of_measure TEXT,
    unit_price      NUMERIC(14,4),
    line_amount     NUMERIC(14,2),                   -- receipts have amounts (ADR-012); D406 rows NULL
    vat_bracket_letter TEXT,                         -- 'A'  (ADR-010)
    vat_percent     NUMERIC(5,2),
    direction       TEXT NOT NULL DEFAULT 'PURCHASE',
    UNIQUE (document_id, line_no)
);

CREATE TABLE classification_result (                 -- append-only versions
    result_id       PK,
    line_id         FK -> document_line NOT NULL,
    result_version  INT NOT NULL,
    account_id      TEXT NOT NULL,
    tax_code        TEXT NOT NULL,
    vat_percent     NUMERIC(5,2) NOT NULL,
    warehouse_id    TEXT NULL,                       -- from warehouse_config (ADR-009)
    tier            SMALLINT NOT NULL,               -- 1..4
    method          TEXT NOT NULL,                   -- 'COMPANY_RULE'|'ALIAS'|'GLOBAL_RULE'|'EMBEDDING'|'LLM'|'MANUAL'
    classification_confidence NUMERIC(5,4) NOT NULL, -- never blended with extraction (ADR-007)
    evidence        JSONB NOT NULL,                  -- rule_id+version | topK similarities | LLM rationale ref
    config_versions JSONB NOT NULL,                  -- {"thresholds":"v3","embed_model":"...","llm":"..."}  ADR-016
    stale           BOOLEAN NOT NULL DEFAULT FALSE,  -- set by impact worker (06); never on EXPORTED docs
    created_at      TIMESTAMPTZ NOT NULL,
    UNIQUE (line_id, result_version)
);

CREATE TABLE correction (
    correction_id   PK,
    line_id         FK -> document_line NOT NULL,
    result_version  INT NOT NULL,                    -- what was corrected
    field           TEXT NOT NULL,                   -- 'account_id'|'tax_code'|'vat_percent'|'warehouse_id'
    old_value       TEXT, new_value TEXT NOT NULL,
    reviewer        TEXT NOT NULL,
    reason_code     TEXT,
    created_at      TIMESTAMPTZ NOT NULL
);

CREATE TABLE review_item (
    review_item_id  PK,
    line_id         FK -> document_line NOT NULL,
    tier            SMALLINT NOT NULL,               -- 3, 4, or 2 (spot-check sample)
    reason          TEXT NOT NULL,                   -- 'LLM_INFERENCE'|'NO_PRECEDENT'|'SPOT_CHECK'|'CONFLICT'
    payload         JSONB NOT NULL,                  -- candidates + evidence + both confidences
    status          TEXT NOT NULL,                   -- 'OPEN'|'RESOLVED'|'EXPIRED'
    created_at      TIMESTAMPTZ NOT NULL,
    resolved_at     TIMESTAMPTZ, resolved_by TEXT
);

CREATE TABLE export_batch (
    batch_id        PK,
    company_id      FK -> company NOT NULL,
    document_ids    JSONB NOT NULL,
    xml_ref         TEXT NOT NULL,                   -- object storage
    generated_by    TEXT NOT NULL,
    generated_at    TIMESTAMPTZ NOT NULL
);

CREATE TABLE event_outbox (                          -- transactional outbox (06)
    outbox_id       PK,
    event_type      TEXT NOT NULL,
    event_version   INT NOT NULL,
    company_id      TEXT,
    correlation_id  TEXT NOT NULL,
    payload         JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL,
    published_at    TIMESTAMPTZ NULL
);
```

---

## 5. Read-path design against the latency NFR

| Path | Access pattern | Budget |
|---|---|---|
| Tier 1 lookup | `ix_rule_lookup` point read + alias hash lookup; per-company rule cache in front (invalidated by `knowledge.rule_changed`) | <10ms |
| Tier 2 retrieval | vector top-K (company-scoped evidence join, then global patterns) | <50ms |
| VAT resolution | in-payload bracket letter, else `product_expected_vat` point read | ~0ms |
| Warehouse | `warehouse_config` point read (cacheable, tiny) | ~0ms |

Effective per-company rule sets are small (Phase 1: only 579 accounts used across all invoice lines vs 15,168 defined; single-company example 18 of 332), so the whole hot path fits comfortably in cache.

## 6. Sizing

Day-one seed: 47,306 products, 76,843 rules-worth of evidence, 169 companies — trivially small for any relational engine. Growth is receipt-driven: at even 2,000 receipts/company/month × 200 companies × ~5 lines, ~2M lines/month — well within a single-node relational store for years; partitioning by `company_id` is the natural scale-out seam if needed (OPEN-Q6 volumes).

## 7. Retention & PII pointers

Images, sender phone numbers, quarantine purge (7 days), and fiscal retention periods are specified in `12_SECURITY_COMPLIANCE.md`; the schema supports them via `image_ref` (deletable object), `sender_ref` (pseudonymized), and append-only audit tables.

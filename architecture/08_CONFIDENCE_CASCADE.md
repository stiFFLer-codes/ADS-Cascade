# 08 — The Four-Tier Confidence Cascade (Full Specification)

The cascade decides how every prediction surfaces: applied silently, applied with a flag, queued for a human, or requested from a human. It is the runtime embodiment of the Phase 1 ADS distribution — 91.2% of products deterministic (>0.95), 7.7% in the 0.50–0.95 band, 1.1% genuinely ambiguous (<0.50).

---

## 1. Two independent signals, one gate, one cascade

```
extraction_confidence  ──►  EXTRACTION GATE  ──fail──►  extraction-repair loop
        (OCR)                     │                     (resend / UI fill-in)
                                  pass
                                  ▼
match evidence  ──►  CONFIDENCE ENGINE  ──►  tier 1–4  ──►  surface behavior
 (KB lookups,          classification
  similarities)          confidence
```

**Hard rule (ADR-007):** `extraction_confidence` and `classification_confidence` are computed, stored, displayed, thresholded, and alarmed **separately**. They never multiply, average, or blend. Rationale: a crisp photo of an ambiguous product and a blurry photo of a deterministic product are opposite problems with opposite remediations — a blended score makes both look identical.

**Extraction gate (runs before tiering):**

| Condition | Action |
|---|---|
| All required fields extracted AND Σ lines = total within ±0.10 RON AND field confidences ≥ `X_FIELD_MIN` (start: 0.90) | Pass to cascade |
| Sum delta ≤ 1.00 RON but > 0.10 | Pass, document flagged `SUM_TOLERANCE` for spot-check |
| Missing required field / sum delta > 1.00 / field below floor | Fail → duplicate-join attempt (ADR-014), then WhatsApp resend request or frontend fill-in. **Never enters the classification review queue** |

---

## 2. Classification pipeline order (locked: RULES_FIRST)

For a line with `(company_id, normalized_text, direction, vat_percent?, supplier_cui?)`:

1. **P0 — Alias/canonical resolution.** normalized_text → `product_id` via exact + alias table (supplier-scoped aliases first). No product resolved → skip to P2 with raw text embedding.
2. **P1 — Deterministic lookup.** ACTIVE `company_account_rule` for (company, product, direction), else (company, product, ANY). Hit → evaluate Tier 1 conditions.
3. **P1b — Global deterministic.** No company rule → `global_pattern` for (product, direction). Only eligible for auto-apply under the strict global conditions below.
4. **P2 — Embedding fallback.** Top-K similarity (K=10) over company-evidenced products first, then global catalog. Candidate accounts inherited from the matched products' rules.
5. **P3 — VAT re-ranking (secondary signal, R4: 94.5% single-rate).** Candidates whose expected VAT (dated attribute) matches the line's extracted VAT get a bounded boost; mismatch is a demotion, never an elimination (the 5.5% multi-rate tail and the 4.05% missing-VAT lines must survive).
6. **P4 — GL sanity screen.** Drop candidates not present in the company's chart of accounts; flag Activ/Pasiv implausibility (receipt purchase → expense/asset accounts expected).
7. **P5 — LLM inference (async only, ADR-013).** Only when P1–P4 produce no candidate above Tier 3 floor, or for new-product category allocation. Constrained: choose from the company's account list + candidate set; never invent accounts (12_SECURITY).

---

## 3. Tier definitions

All thresholds are named, versioned configuration (ADR-016), recorded on every result. Values below are **pilot starting points derived from Phase 1 distributions — calibration is a pilot exit criterion** (OPEN-Q12).

### Tier 1 — Deterministic → auto-apply, no flag

Any of:
- **T1-a (company rule):** `ads ≥ T1_ADS (0.95)` AND `evidence_count ≥ T1_MIN_EVIDENCE (3)` AND rule ACTIVE (not CONFLICTED).
- **T1-b (fresh correction rule):** origin ∈ {CORRECTION, MANUAL_MONOGRAPHY} — a human just told us the answer; evidence floor waived, `evidence_count ≥ 1`.
- **T1-c (global unanimous):** no company evidence, but `global_ads ≥ T1_GLOBAL_ADS (0.98)` AND `company_count ≥ 5` AND direction match. (Strict on purpose: cross-company consistency is 0.695 on multi-company products — the global layer auto-applies only near-unanimous patterns.)

`classification_confidence = ads` (company) or `global_ads` (global). Expected volume: ~90% of lines once the KB is warm (91.2% deterministic products; high-volume ambiguous products pull the line-weighted share down toward the weighted ADS 0.847 — hence not 96%).

**Accuracy target:** ≥98% (13_OBSERVABILITY alarms at T1 correction rate ≥2%).

### Tier 2 — Fuzzy/embedding match → auto-apply + spot-check flag

Any of:
- **T2-a:** company rule with `0.80 ≤ ads < 0.95` AND `evidence_count ≥ 3` AND VAT corroboration (P3 match or VAT missing).
- **T2-b:** embedding match `similarity ≥ T2_SIM (0.85)` to a product whose company rule qualifies for T1-a, AND top-3 candidates agree on the same account.
- **T2-c:** global pattern `0.85 ≤ global_ads < 0.98` with `company_count ≥ 5` AND VAT corroboration.

Auto-applied, flagged `SPOT_CHECK`; a sampled fraction (start: 20%, decaying with observed precision) is routed into the review queue as audit items. A confirmed T2-b spot-check **promotes the alias** (07 §2) — the fuzzy match becomes deterministic forever after.

**Accuracy target:** ≥92%.

### Tier 3 — LLM inference / unconfirmed pattern → human review queue

Triggers:
- Best similarity < 0.85, or top candidates disagree (e.g. global rovinieta split 628/635/6352 — the worked example for a precedent-less company).
- Company rule CONFLICTED, or ads < 0.80, or evidence_count < 3 (unconfirmed pattern).
- VAT contradiction on an otherwise-strong match (expected 11%, extracted 21%).
- LLM was consulted (P5): its proposal **always** lands in review — LLM output is never auto-applied in this phase. Revisit after pilot precision data.

Review item carries: candidates with per-candidate evidence (rule versions, similarities, global distribution), both confidences, LLM rationale if any. Sync API callers receive `status: PENDING_REVIEW` immediately (ADR-013).

Expected volume: ~5–9% of lines (the 7.7% mid-band plus new products), shrinking as corrections convert the tail.

### Tier 4 — No precedent → manual entry becomes training data

Triggers: no product resolution, no candidate above `T3_FLOOR (0.50)`, or a brand-new product with an empty category candidate set.

The accountant classifies from scratch (UI offers the company's most-used accounts + category suggestions). The entry writes: `kb_evidence` (source CORRECTION), a new T1-b rule, alias rows for the raw text, embedding upsert for the new product. **Tier 4 is the KB's growth mechanism, not a failure state** — every T4 resolution permanently moves that product to T1 for that company.

---

## 4. Decision table (normative)

| # | Company rule | Global pattern | Embedding | Outcome |
|---|---|---|---|---|
| 1 | ads ≥.95, ev ≥3 | — | — | **T1-a** auto-apply |
| 2 | correction-origin, ev ≥1 | — | — | **T1-b** auto-apply |
| 3 | none | gads ≥.98, cos ≥5 | — | **T1-c** auto-apply |
| 4 | .80–.95, ev ≥3, VAT ok | — | — | **T2-a** apply+flag |
| 5 | none | — | sim ≥.85 → T1-grade rule, top-3 agree | **T2-b** apply+flag |
| 6 | none | .85–.98, cos ≥5, VAT ok | — | **T2-c** apply+flag |
| 7 | conflicted / ads <.80 / ev <3 | any | any | **T3** review |
| 8 | none | gads <.85 (split, e.g. rovinieta 628/635) | sim <.85 or disagreement | **T3** review (LLM may pre-propose) |
| 9 | none | none | no candidate ≥.50 | **T4** manual |

Precedence: company evidence always outranks global (ADR-001); a row-7 condition overrides any global row.

---

## 5. Confidence computation notes

- `classification_confidence` is the *decisive signal's* strength (ADS, global_ads, or calibrated similarity), not a product of all signals — multiplying independent weak signals manufactures false precision.
- Similarity scores are calibrated to empirical precision during pilot (isotonic/binned mapping), so "0.85" means "~85% of matches at this score were correct", not raw cosine.
- Supplier identity contributes only through supplier-scoped aliases and duplicate detection — never a confidence term (ADR-005; the 6022-misbooking in Phase 1 data is the cautionary tale).
- Recency: evidence older than the VAT law boundary (2025-08) keeps account weight but its VAT attribute is remapped through the rate-transition table (19→21, 9→11), so pre-change history doesn't poison VAT corroboration.

---

## 6. Worked example through the cascade

**Company WITH precedent (Nordline-like: rovinieta→635 ×55, ads 1.0):** P0 alias `rovinieta a autoturisme`→`rovinieta` → P1 hit (PURCHASE, ACTIVE, ads 1.0, ev 55) → row 1 → **T1-a**: account 635, tax_code 301104, VAT 21% (bracket letter A), warehouse from config. Confidence 1.0. No LLM, no review, <10ms.

**Company WITHOUT precedent:** P1 miss → P1b: global rovinieta/PURCHASE distribution {628, 635, 6352, 471} → global_ads ~0.45 < 0.85 → P2 embeddings return the same split family → row 8 → **T3**: review item with candidates 635 (CHELT. CU ALTE IMPOZITE, dominant), 628 (SERVICII TERTI), 6352 — each with company counts. Accountant picks 635 → `correction.submitted` → T1-b rule created → the company's next rovinieta is row 2, **T1-b**, auto-applied. Two receipts: that's the full Knowledge Lifecycle in one product.

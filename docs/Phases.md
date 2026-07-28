# Phases — roadmap

*Where the project has been and the proposed path forward. Current status always
lives in `../STATE.md`.*

---

## Phase 1 — Data Engineering · **DONE**

Built the evidence base from D406 SAF-T XML.

- 296,648 invoice lines · 169 companies · 1,020 XML files
- Weighted ADS **0.847** / unweighted 0.964 · **91.2%** products deterministic (>0.95)
- Cross-company consistency **0.695** · VAT single-rate 94.5%
- **76,843** product→account mappings (`data/outputs/product_account_mapping.csv`)

→ Full report: `../reports/phase1_final_report.md`

## Phase 2 — Solution Architecture · **DONE (design)**

Technology-agnostic architecture for receipt classification, sharing intelligence
with D406. 17 docs, 16 ADRs, 20 open questions.

→ Index: `../architecture/00_SCOPE.md`

## Phase 2 — Implementation · **PLAN APPROVED — detail in `PHASE2_PLAN.md`**

Ordered by **dependency, not receipt-flow**: classification (unblocked/free) first,
extraction on the 10 receipts second, end-to-end join third. Full stage breakdown,
contracts, outputs and metrics → `PHASE2_PLAN.md`. Summary below.

| # | Slice | Depends on / blocked by |
|---|---|---|
| 1 | **Prototype the core thesis** — deterministic lookup + embedding fallback over `product_account_mapping.csv`. Proves the 91% with real numbers. | Nothing — runs on Phase 1 outputs, no production access. **Do this first.** |
| 2 | **Knowledge Base service** + D406 seed contract (the 76,843 mappings) | Stack/DB confirmation (OPEN-Q1/3) for the *real* build; prototype can stub it |
| 3 | **Classification service** (RULES_FIRST cascade) + **Confidence Engine** | KB (#2); cascade spec is `../architecture/08_CONFIDENCE_CASCADE.md` |
| 4 | **Extraction + Validation** — OCR, per-line VAT bracket letter, arithmetic reconciliation (Σ lines = total), duplicate-join | OCR provider choice (OPEN-Q); Textract is a candidate, behind an adapter |
| 5 | **Ingestion + Review + Export** — WhatsApp/upload intake, human review queue, ERP XML export | WhatsApp route (OPEN-Q7), ERP export schema (OPEN-Q10) |

**Guiding rule:** don't build a slice that's blocked on an unconfirmed fact when an
earlier, unblocked slice still delivers evidence. Slice 1 is unblocked today.

# Context — plain English

*What this project is and its constraints. The client-facing version is
`architecture/01_EXECUTIVE_SUMMARY.md`.*

---

## The situation

This project was carried out for a **Romanian accounting client** — a firm whose product is
**live in production with daily users**. Access to the client's environment was limited to a data
role (able to see the client's data, but not the deployed application's internals). The brief was
open-ended: **research how to integrate an AI feature** into the existing product. Without full
visibility into the live system, everything here is designed to *not depend* on facts that
couldn't be confirmed.

## What the product does

Accountants manually type small purchases into the accounting system. For every
receipt/invoice line they decide four things by hand:

- **AccountID** — which expense/asset account it books to
- **VAT %** — the tax rate
- **TaxCode** — the fiscal code
- **WarehouseID** — where applicable

The AI feature's job: **learn each company's past decisions and auto-fill these**,
sending only the genuinely uncertain cases to a human.

## Two data sources

- **D406 invoices (SAF-T XML)** — analyzed in Phase 1. This is the *evidence base*:
  it proved the approach works and produced 76,843 real product→account mappings.
- **Receipts / bonuri fiscale** — the new Phase 2 *feature*. Thermal-paper receipts
  (invoices < 500 RON not in e-Factura), arriving via WhatsApp or file upload.

Both feed **one shared per-company knowledge base** — not two catalogs that drift.

## The hard constraint

The **production stack is unknown** (language, DB, hosting, deployment). So the
architecture is deliberately **technology-agnostic**: decisions are drawn around
data ownership and contracts, not specific vendors or deployment units. See
`architecture/OPEN_QUESTIONS.md`.

## Working philosophy

- **Evidence-driven** — decisions come from Phase 1 measurements, not guesses.
- **Catalog-centric, not LLM-centric** — 91.2% of products are deterministic; the
  product catalog answers most lines with no AI call. The AI *builds* the catalog
  and handles only the ambiguous tail.
- **Model-agnostic** — OCR/LLM providers sit behind swappable interfaces.

# 01 — Executive Summary

*For management and client stakeholders. Technical depth lives in documents 02–14.*

---

## What we are building

Today, when a client company buys something small — fuel, office supplies, a road vignette — the paper receipt (bon fiscal) has to be typed into the accounting system by hand: what was bought, which expense account it belongs to, which VAT rate and tax code apply. This is slow, repetitive work, and it doesn't scale with the firm's client portfolio.

Phase 2 automates it. A client employee photographs the receipt and sends it on WhatsApp (or the accountant uploads it). The system reads the receipt, works out the correct accounting treatment — **account, VAT rate, tax code, and warehouse** — for every line, and prepares the entries for import into the accounting system. Accountants review only the genuinely uncertain cases instead of typing everything.

## Why we're confident it works: the Phase 1 evidence

This design is not a guess. Phase 1 analyzed **296,648 real invoice lines from 169 Romanian companies** and established, with measurements:

- **Most classification decisions are repetition, not judgment.** 91.2% of products are booked the same way virtually every time within a company. A system that *remembers* each company's past decisions answers the vast majority of lines instantly, with no AI cost at all.
- **But companies differ from each other.** The same product is booked to different accounts by different firms often enough (consistency across companies is only ~70%) that a one-size-fits-all model would be wrong roughly 3 times in 10 on shared products. So the system keeps **one knowledge base per client company**, backed by a shared global layer for common patterns.
- **The hard cases are a small, known tail.** Only ~1% of products are genuinely ambiguous. That tail — and only that tail — goes to an AI model and, when still uncertain, to a human. Every human answer is remembered, so the tail shrinks over time.

A real example runs through the entire package: a Petromax receipt for a **road vignette (rovinieta)** (company name anonymized; the receipt and Phase 1 evidence are real). Petromax is a fuel company, but this purchase isn't fuel — and in the Phase 1 data, real companies book this exact product to different accounts (628, 635, 6352), each consistently. The system gets it right because it reads *what was bought*, not *who sold it*, and because it applies *this company's* precedent. Where no precedent exists, it asks the accountant once — and never asks again for that product.

## How it decides: four levels of confidence

1. **Known answer** → applied automatically (expected: ~90% of lines once warmed up).
2. **Very close match** → applied automatically, flagged for occasional spot-checks.
3. **AI suggestion, unconfirmed** → routed to the accountant's review queue with the evidence attached.
4. **Never seen before** → the accountant classifies it once; the answer becomes permanent knowledge.

Two safety properties are built in: the system distinguishes "we couldn't read the photo" from "we don't know the account" (they get different fixes — a resend request vs a review), and it **never invents accounts** — it can only propose accounts that exist in the client's own chart of accounts.

## One brain, not two

The receipts feature and the existing D406 invoice analysis feed **the same knowledge base per company**. The 76,843 product-to-account mappings already extracted in Phase 1 are the starting knowledge on day one — the system is born experienced, not blank. A correction made on a receipt improves invoice classification, and vice versa. (This is a deliberate improvement over the original proposal, which would have grown two separate catalogs that drift apart.)

Another deliberate improvement: when an accountant changes a booking policy, the change applies **going forward** and quietly updates only the still-open documents. Already-booked records are never silently rewritten — an audit and stability requirement — and the system never grinds through the whole archive on every edit.

## The targets (from Phase 1, unchanged)

| Measure | Target |
|---|---|
| Accuracy of automatic classifications | 85–90% at pilot, higher as knowledge accumulates |
| Speed per classification | under 100 milliseconds |
| Cost per line classified | under €0.001 (modelled: ~15× under budget, because 91%+ of lines need no AI call) |
| Return on investment | manual ≈ €2,490/company/month vs automated ≈ €282 — break-even in **under 2 months** at pilot scale |

## What we need from you (decisions, not designs)

The architecture is complete and technology-agnostic; a short list of business/engineering confirmations remains before build starts — chiefly: the production technology stack, the WhatsApp Business route, the target accounting system's import format, and expected receipt volumes. The full list, with defaults already assumed so nothing is blocked, is in `OPEN_QUESTIONS.md`.

## Risks, honestly stated

- **Photo quality** is the biggest operational unknown — mitigated by automatic resend requests and by measuring extraction quality separately from classification quality.
- **Cold start for new client companies**: the global knowledge layer covers common patterns; the first weeks involve more review-queue work until company precedents accumulate. This is by design — the alternative (guessing) produces silent errors in the books.
- **Vendor dependence** is engineered out: OCR and AI providers sit behind swappable interfaces, and if every AI vendor vanished tomorrow, ~90% of classification volume would continue unaffected.

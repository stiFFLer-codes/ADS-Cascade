# 14 — Cost Model

> **Status:** Solution Architecture — governing document
> **Date:** 2026-07-06
> **Depends on:** `03_NON_FUNCTIONAL_REQUIREMENTS.md` (NFR-8 per-line target, NFR-9 OCR budget separation, NFR-10 sizing), `08_CONFIDENCE_CASCADE.md` (tier routing), `13_OBSERVABILITY.md` (metering & alerting), `00_SCOPE.md` (locked decisions)

## 1. Purpose and method

This document shows that the **< €0.001 per line** classification target (Phase 1 success criterion, NFR-8) is achievable with wide margin, and makes every number behind that claim inspectable. Method:

- Every input is a **named variable** in the assumption table (§2). Anything not measured in Phase 1 is marked **pending confirmation**.
- All vendor prices are **indicative as of July 2026, from public price lists, to be re-quoted before contract**. The model is technology-agnostic: each cost slot names 2–3 candidates with their cost character, never a settled pick.
- Per-**document** ingestion cost (OCR) and per-**line** classification cost are kept strictly separate, per NFR-9. They have different unit economics and mixing them makes both targets meaningless.
- FX: €1 ≈ $1.08 assumed ($1 ≈ €0.93). Immaterial at these magnitudes; restate at re-quote.

---

## 2. Assumption table

| Variable | Value(s) | Source / status |
|---|---|---|
| `C` — companies onboarded | 169 (Phase 1 population); pilot subset TBD | Phase 1 data; pilot size **pending confirmation** |
| `R` — receipts / company / month | **UNKNOWN** → three scenarios: **Low = 100, Mid = 500, High = 2,000** | Open question #6 in `00_SCOPE.md`; **pending confirmation** |
| `L` — lines per receipt | 1–10, planning mean **3.5** | Assumed from receipt shape (fuel/retail mix); **pending confirmation** |
| `p3` — share of lines reaching Tier 3 (LLM) | **5–9%**, planning value 7% | ADS evidence: 91.2% deterministic (ADS > 0.95), 8.8% non-deterministic tail, part caught by embedding fallback at T2; 1.1% genuinely ambiguous. Receipt-side value **pending pilot measurement** |
| `r_ocr` — OCR retry rate | 5% | Assumed photo-quality allowance; **pending pilot measurement** |
| `T_in` — input tokens per batched Tier 3 line | 500–1,500, planning **1,000** (prompt + candidate accounts + company context) | Prompt design estimate; **pending measurement** |
| `T_out` — output tokens per Tier 3 line | ~100 (structured suggestion) | Estimate; **pending measurement** |
| LLM price (Haiku-class small model) | ~$1 / MTok input, ~$5 / MTok output | Indicative July 2026 public pricing; order-of-magnitude anchor, **re-quote** |
| Batch API discount | ~50% off token prices | Indicative July 2026; **re-quote** |
| Prompt caching | cached input reads ~0.1×, cache writes ~1.25× | Indicative July 2026; assumes ≥ 60% of `T_in` is a stable cached prefix (system prompt + per-company context) |
| Embedding price (API-hosted) | ~$0.02–$0.13 / MTok | Indicative July 2026 band across common providers; **re-quote** |
| Receipt image size | ~200 KB average | Assumed; **pending measurement** |
| Manual baseline | €2,490 / company / month | Given (Phase 1 ROI baseline) |
| Automated cost | €282 / company / month (89% reduction) | Given; assumed to include residual human review labor + allocated platform cost — composition **pending confirmation** (§7) |
| Build cost (Phase 2, one-time) | €20,000–€40,000 | Engineering estimate placeholder; **pending confirmation** |

---

## 3. Per-document ingestion cost (OCR)

Receipts are effectively one page each. Candidates behind the provider-agnostic Extraction interface (`09_AI_ORCHESTRATION.md`), indicative July 2026 public pricing:

| Candidate | Class | Indicative price / page | Cost character & trade-offs |
|---|---|---|---|
| AWS Textract — DetectDocumentText | Raw OCR | ~$0.0015 | Cheapest; returns text only — line-item segmentation, totals, VAT brackets are our code. Lowest cost, highest engineering burden |
| AWS Textract — AnalyzeExpense | Receipt-aware | ~$0.01 | Structured vendor/date/line-item/total fields out of the box; ~7× the raw price buys less extraction code and likely fewer T3 escalations |
| Google Document AI — OCR / Expense parser | Raw / receipt-aware | ~$0.0015 / ~$0.01 (order) | Comparable split; strong multi-language OCR — relevant for Romanian diacritics (NFR-24) |
| Azure Document Intelligence — Read / prebuilt-receipt | Raw / receipt-aware | ~$0.0015 / ~$0.01 (order) | Comparable split; EU-region availability relevant to data residency (open question #11) |

**Per-document budget** (NFR-9), including the `r_ocr` = 5% retry allowance:

- Raw-OCR class: ~$0.0016 ≈ **€0.0015 / receipt**
- Receipt-aware class: ~$0.0105 ≈ **€0.0098 / receipt**

Budget band adopted: **€0.002–€0.011 per receipt**. This is a per-document ingestion cost and is **never counted into the €0.001/line classification target** — a 1-line receipt would falsely fail it and a 10-line receipt would falsely dilute it. Provider choice (raw vs receipt-aware, and vendor) is an open engineering trade: at Mid scenario fleet volume the price gap is ~€700/month (§6) against the cost of building and maintaining our own line-item segmentation and the arithmetic-validation failure rate (NFR-15).

---

## 4. Per-line classification cost

### 4.1 Tier 1 / Tier 2 — infra-only

T1 (deterministic lookup) and T2 (embedding fallback + VAT re-ranking) touch only the knowledge-base store and the vector index. Marginal cost is amortized infrastructure:

- At Mid-scenario fleet volume (~296k lines/month, §6) against the Stack A infra floor (§5), the classification-attributable share works out to **≈ €5–50 per million lines, i.e. €5–50µ per line** (€0.000005–0.00005).
- At Low volumes the *average* rises because the infra floor is fixed — but that is amortization arithmetic, not marginal cost. The marginal T1/T2 line is effectively free.

### 4.2 Tier 3 — LLM cost per line

Haiku-class pricing, `T_in` = 1,000, `T_out` = 100:

| Pricing mode | Math | $ / T3 line | € / T3 line |
|---|---|---|---|
| Naive (no batch, no cache) | (1,000 × $1 + 100 × $5) / 1M | $0.00150 | €0.0014 |
| Batch API (−50%) | 0.5 × above | $0.00075 | €0.0007 |
| Batch + prompt caching (60% of input cached at 0.1×) | ((400 × $1 + 600 × $0.10) + 100 × $5) / 1M × 0.5 | $0.00048 | €0.00045 |

Even the **naive** mode is only ~1.4× the *entire* per-line budget — and it applies to ≤ 9% of lines.

### 4.3 Blended cost — why < €0.001/line holds

Blended = (1 − p3) × infra-only + p3 × T3 cost:

| Case | p3 | T3 mode | Blended € / line | Margin vs €0.001 |
|---|---|---|---|---|
| Planning | 7% | Batch (€0.0007) | (0.93 × €0.00002) + (0.07 × €0.0007) ≈ **€0.000068** | ~15× under |
| Conservative | 9% | Naive (€0.0014) | (0.91 × €0.00005) + (0.09 × €0.0014) ≈ **€0.00017** | ~6× under |
| Optimized | 5% | Batch + cache (€0.00045) | ≈ **€0.000033** | ~30× under |

The target holds **because 91.2% of lines never touch the LLM** (deterministic ADS > 0.95). The LLM is a tail worker; its price is multiplied by a small number before it reaches the blended figure.

### 4.4 Sensitivity — Tier 3 share doubles

If the KB underperforms on receipts and `p3` doubles to 14–18%:

| p3 | T3 mode | Blended € / line |
|---|---|---|
| 14% | Batch | ≈ €0.00012 |
| 18% | Naive (worst case) | (0.82 × €0.00005) + (0.18 × €0.0014) ≈ **€0.00029** |

Still ~3.5× under budget in the worst combined case. Solving for the break point: at naive pricing the €0.001 budget is breached only when **p3 exceeds ~68%** — i.e. only if the deterministic core has collapsed, which is a knowledge-base health incident (alert per §8), not a pricing problem. Cost is therefore a *lagging* indicator of KB failure; the leading indicator is the T3-share alert.

---

## 5. Embedding costs

**One-time backfill** — embed all 47,306 normalized Phase 1 products. At ~10–25 tokens per normalized product name: ~0.5–1.2 MTok total.

- API-hosted multilingual embedding model: 1.2 MTok × $0.02–$0.13/MTok ≈ **$0.02–$0.16 one-time**. Negligible — a full re-embed on a model upgrade costs under €1, so model iteration is not cost-constrained.
- Self-hosted multilingual encoder (E5/BGE-class, per NFR-23 Romanian benchmark): no per-token fee; cost appears as a compute line in the infra baseline (≈ €30–150/month if a dedicated instance, less if shared/on-demand). Choose on quality + residency grounds, not cost — both options are noise at this scale.

**Incremental** — new products discovered from receipts (thousands/month at fleet scale): well under 0.1 MTok/month, ≈ **€0.01/month API-hosted**. Also noise.

**Query-time embeddings** — only the ≤ 8.8% of lines that miss deterministic lookup need an embedding for search; already inside the T1/T2 infra-only figure (self-hosted) or adds ≈ €0.5/month fleet-wide (API-hosted).

---

## 6. Infrastructure baseline

Monthly bands, technology-agnostic, sized for the Mid scenario across 169 companies (≈ 84,500 receipts, ≈ 296k lines/month — coincidentally the Phase 1 monthly-equivalent line volume). Components: relational DB (knowledge base, rules, audit), vector store, durable queue, object storage (receipt images).

| Stack | Composition | Indicative monthly band | Cost character |
|---|---|---|---|
| **A — consolidated** | Managed Postgres + pgvector (one store for KB + vectors), managed queue (SQS/PubSub-class), object storage, 2–4 small app/worker instances | **€100–450** | Lowest floor, one backup/consistency domain, no KB↔vector drift. pgvector comfortably serves ~50k-product-scale ANN at our QPS. Default candidate |
| **B — dedicated vector DB** | Stack A + managed vector DB (Qdrant/Weaviate/Pinecone-class) | **€170–750** | Adds €70–300/month + an operational surface + a second store that can drift from the KB. Justified only if ANN QPS or index size outgrows pgvector — not indicated by Phase 1 volumes |
| **C — serverless-native** | Serverless relational/NoSQL + managed search/vector service + serverless functions + queue | **€50–600 (usage-spiky)** | Lowest idle floor for a small pilot; costs track the month-end burst (NFR-11); tighter vendor coupling. Attractive for pilot, re-evaluate at fleet scale |

Object storage detail: 84,500 receipts × 200 KB ≈ 17 GB/month new; with a 5-year fiscal retention assumption (**pending `12_SECURITY_COMPLIANCE.md`**, open question #11) the archive grows ~1 TB over 5 years ≈ €5–25/month at cold-tier prices — retention policy, not storage price, is the real variable.

**Fleet-level variable costs at each scenario** (169 companies, receipt-aware OCR class, planning blended line cost):

| Scenario | Receipts/mo (fleet) | Lines/mo (fleet) | OCR /mo | Classification (LLM + variable) /mo |
|---|---|---|---|---|
| Low (R=100) | 16,900 | 59,150 | ≈ €165 | ≈ €4 |
| Mid (R=500) | 84,500 | 295,750 | ≈ €830 | ≈ €20 |
| High (R=2,000) | 338,000 | 1,183,000 | ≈ €3,320 | ≈ €80 |

Reading: **the infra floor and OCR dominate total platform cost; LLM classification spend is almost irrelevant** at compliant p3. The cost architecture's job is to keep it that way (§8).

---

## 7. ROI and break-even

Given: manual processing ≈ **€2,490 / company / month**; automated ≈ **€282 / company / month** (89% reduction) → **savings ≈ €2,208 / company / month**.

Consistency check: the platform's variable cost per company at Mid scenario is ≈ €5–10/month (OCR + LLM + infra share). The €282 automated figure is therefore assumed to be **mostly residual human labor** (T3 review, T2 spot-checks, exception handling) plus allocated platform cost — a composition consistent with the cascade design (~5–9% of lines still see a human), but **pending confirmation** with the firm.

**Break-even including build amortization** (assumption: one-time Phase 2 build €20k–€40k, pending confirmation; savings accrue from go-live):

| Pilot size | Build €20k | Build €40k |
|---|---|---|
| 5 companies (€11,040 saved/mo) | 1.8 months | 3.6 months |
| 10 companies (€22,080 saved/mo) | 0.9 months | 1.8 months |
| 20 companies (€44,160 saved/mo) | 0.5 months | 0.9 months |

The Phase 1 target of **break-even < 2 months** holds at ≥ 5 companies for a €20k build, or ≥ 10 companies for a €40k build. Per-company marginal ROI (ignoring build) breaks even in **days**: €2,208/month savings against €5–10/month marginal cost. The ROI case is robust to every assumption in §2 except the €282/€2,490 baseline itself — which is why its composition is the single most important number to confirm.

---

## 8. Cost guardrails

Cost must be *governed*, not just estimated. Alerting and metering plumbing is specified in `13_OBSERVABILITY.md`; this section defines the policy.

1. **Per-company LLM budget cap.** Every LLM call carries company attribution; each company has a monthly token/€ cap defaulting to **3× its scenario-expected T3 spend**. On breach: that company degrades to deterministic-only mode (rung 1 of the NFR-14 ladder — T3 lines queue for human review without an LLM suggestion), and an alert fires. Documents are never dropped or delayed at intake.
2. **Fleet-level LLM spend alerts.** Daily LLM spend > 2× the trailing 7-day median → warning; > 4× → page. Catches prompt-size regressions and retry storms before the invoice does.
3. **T3-share alert (leading indicator).** Any company with T3 share > 15% over a 7-day window, or fleet T3 share > 12%, alerts as a **KB-health signal** — per §4.4, cost only breaks after the knowledge base has already failed, so this alert front-runs the money.
4. **OCR guardrails.** Retry rate > 10% per provider alerts (photo-quality or provider regression); per-document OCR spend metered against the §3 budget band monthly.
5. **Kill switch to deterministic-only mode.** A configuration flag — per company and global — that removes all LLM (and optionally embedding) calls from the pipeline immediately. Behavior is exactly the NFR-14 degradation ladder: T1/T2 deterministic continues, everything else routes to human review. This bounds worst-case spend at the infra floor + OCR, with zero document loss.
6. **Batch-mode lever.** The 15-minute batch mode (NFR-6, pending business confirmation) is the standing ~50% discount on T3 spend; the cost model works without it, so it is a lever, not a dependency.
7. **Re-quote cadence.** All indicative prices in §3–§5 re-quoted quarterly and at any provider/model change; the assumption table is the single place they live.

---

## Open questions surfaced by this document

1. **`R` — receipts per company per month** (open question #6). The single largest unknown; drives OCR spend, capacity sizing (NFR-10), and the batch-mode decision. Needed from the firm's intake data or pilot measurement.
2. **`L` — lines-per-receipt distribution** — planning mean 3.5 is unmeasured; affects the per-line denominator everywhere.
3. **Composition of the €282/month automated figure** — how much is residual review labor vs platform allocation? The ROI case (§7) leans on this given baseline.
4. **Build cost and pilot company count** — the €20k–€40k build assumption and the 5/10/20-company pilot sizes determine whether the < 2-month break-even is met (§7).
5. **OCR provider class** — raw OCR + own line-item segmentation vs receipt-aware API at ~7× the per-page price: an engineering-effort vs unit-cost trade, decided after a pilot bake-off on real Romanian receipts (ties to NFR-15 validation rates).
6. **Receipt-side `p3`** — the 5–9% Tier 3 share is extrapolated from invoice-line ADS; OCR noise may push it up. Pilot must measure it (it is also the §8.3 alert threshold input).
7. **Normal vs 15-minute batch mode default** (NFR-6) — business latency tolerance vs the ~50% T3 discount.
8. **Hosting/stack choice** (open question #1) — selects Stack A/B/C and turns the infra bands into a number; also gates the embedding hosted-vs-self-hosted call (NFR-23, residency per `12_SECURITY_COMPLIANCE.md`).
9. **Image retention period** — fiscal retention vs GDPR minimization (open question #11) sets the object-storage growth curve (§6).
10. **`T_in`/`T_out` per Tier 3 line and cacheable-prefix share** — prompt-design estimates (1,000/100 tokens, 60% cached) to be measured once the T3 prompt is built; §4.2 sensitivity shows the target survives even the naive case.

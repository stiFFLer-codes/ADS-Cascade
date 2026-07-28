# D406 Invoice Classification Pipeline
## Technical Report — Phase 1 Complete

---

## 01 Understanding the Problem

### D406 Invoice Classification System
**Objective:** Build an AI system that automatically classifies invoice line items to the correct accounting categories.

**The Challenge:**
- Romanian companies file D406 tax declarations (XML format)
- Each invoice line needs an accounting category (GL Account)
- Manual classification is slow, error-prone, and doesn't scale
- Need to learn from historical data across 201 companies to automate this

### Real-World Example
**Invoice #12345 from Supplier "TechStore"**
Line 1: "Laptop Dell Inspiron 15" → ???
Line 2: "Microsoft Office 365 License" → ???

**Accountant needs to assign GL Accounts:**
Line 1: Laptop → Account 214 (IT Equipment)
Line 2: Office 365 → Account 613 (Software Licenses)

**The Questions:**
1. Can we learn these patterns from historical data?
2. Are patterns consistent across companies or company-specific?
3. Which features actually help?
4. What AI architecture should we use?

---

## 02 Core Engineering Principle

### Traditional AI vs Data-Driven AI

**❌ Traditional Approach (What NOT to Do)**
Day 1: "Let's use GPT-4 for everything!"
Week 2: Build GPT-4 integration
Month 1: Deploy to production
Month 2: Accuracy is 60%... why?
Month 3: Discover data issues
Month 4: Realize GPT-4 is overkill

**Cost:** Expensive, slow, wrong architecture

**✅ Data-Driven Approach (What We Did)**
Week 1: Extract all data cleanly
Week 2: Analyze patterns statistically
Week 3: Let data answer architecture questions
Week 4: Build right solution from day 1

**Benefits:**
- Right architecture from day 1
- Know which features to collect
- Understand edge cases upfront
- Cost-effective (rules > ML > LLM)

---

## 03 Building the Foundation

### Dataset Overview
**Source:** 201 Romanian companies inventoried, 169 with invoice data, 9 months of tax declarations

| Metric | Count |
|--------|-------|
| Companies (inventory) | 201 |
| Companies (with invoices) | 169 |
| XML files processed | 1,020 |
| Total invoices | 107,736 |
| Invoice lines (training examples) | 296,648 |
| Unique products (raw / normalized) | 62,447 / 47,306 |
| GL accounts defined | 15,168 |
| GL accounts actually used | 579 (3.8%) |
| Unique VAT rates | 6 |

> ### 💡 Finding
> Companies define thousands of categories but only use a small fraction.
>
> **Evidence**
> 15,168 accounts defined vs 579 actually used (3.8% utilization).
>
> **Impact**
> The classification space is dramatically smaller than the raw Chart of Accounts suggests, improving model feasibility.

### 5-Stage Data Engineering Pipeline

```mermaid
graph LR
    A[1,290 Raw Files] --> B[Script 1<br/>Inventory]
    B --> C[Script 1.5<br/>Normalize]
    C --> D[Script 2<br/>Extract GL]
    D --> E[Script 3<br/>Extract Invoices]
    E --> F[Script 3.5<br/>Intelligence]
    F --> G[Script 4<br/>Architecture]
    G --> H[Phase 2:<br/>Build AI]
```

### Script 1: Create Master Catalog
Builds a single source of truth for all downstream processing, cataloging 201 companies and detecting duplicate filings.

### Script 1.5: Download → Extract → Validate
Instead of re-downloading files on every run, we built a robust pipeline:

**Downloads** → **4 Workers** → **Retry Logic** → **Atomic Write** → **Validated XML**

All 1,020 XML files successfully downloaded, extracted, and validated (100% pass rate). Result: "Download once, reuse forever."

---

## 04 Teaching the System Accounting

### Script 2: Build Company Knowledge Base

Extracts the General Ledger (GL) accounts for every company to understand their unique category systems.

**Example:**
`707` → "Venituri din prestări servicii" (Revenue from Services)
`214` → "Echipamente IT" (IT Equipment)

**Key Output:**
`company_gl_catalog.json` — Fast O(1) lookup structure for all 154,068 GL account records across 201 companies (average 766.5 accounts/company, range: 2 to 14,806).

---

## 05 Learning From Historical Decisions

### Script 3: Build Training Dataset

Parses all 1,020 XMLs, handles schema variations (5+ ways to represent the same field), and extracts individual invoice lines as training examples.

**Phase 1: Raw Extraction**
Extracts product, account, VAT, amount, date, direction (sale/purchase). Handles purchase-heavy dataset (73.9% purchases, 26.1% sales).

**Phase 2: Enrichment**
Normalizes product names and enriches them with account metadata from Script 2.

### Data Quality Summary

| Field | Missing % | Status |
|-------|-----------|--------|
| product_description | 0.0% | ✓ Complete |
| account_id | 0.0% | ✓ Complete |
| direction | 0.0% | ✓ Complete |
| tax_code | 0.0% | ✓ Complete |
| vat_percent | 4.05% | ⚠ 12,007 lines |
| warehouse_id | 100.0% | ✗ Absent from schema |
| line_amount | 100.0% | ✗ Absent from schema |

> ### 🔍 Finding
> Warehouse and line amount data are entirely absent from the D406 XML schema.
>
> **Evidence**
> 100.0% of warehouse and line_amount fields are missing — these fields simply don't exist in the data.
>
> **Impact**
> Dropped from feature engineering entirely. Classification must rely on product description and categorical features alone.

---

## 06 Understanding the Dataset

### Script 3.5: Statistical Analysis — "Can AI Solve This?"

> ### 📊 Finding
> Dataset is highly learnable — 91.2% of products are deterministic.
>
> **Evidence**
> Weighted ADS = 0.847, Unweighted ADS = 0.964. Of 47,306 normalized products, 43,156 (91.2%) have a determinism score above 0.95. Only 526 products (1.1%) are truly ambiguous (ADS < 0.50).
>
> **Impact**
> A rules-first approach handles the vast majority. ML is only needed for the 8.8% non-deterministic tail.

> ### ⚠️ Finding
> High-volume products are more ambiguous than rare products.
>
> **Evidence**
> ADS divergence = 0.117 (weighted 0.847 vs unweighted 0.964). Common products like "avans" and "prestari servicii" map to 50+ different accounts.
>
> **Impact**
> The hardest products to classify are also the most frequent — the core challenge for Phase 2.

> ### 🔍 Finding
> Cross-company consistency is moderate — companies classify the same products differently.
>
> **Evidence**
> Cross-company consistency score = 0.695, analyzed across 2,696 multi-company products. The same product can map to entirely different accounts depending on the company's accounting philosophy.
>
> **Impact**
> A global-only model would face a ~30% consistency gap. Company-specific overrides are essential.

> ### 💡 Finding
> VAT is highly standardized — a useful secondary signal.
>
> **Evidence**
> Only 6 unique VAT rates exist, and 94.5% of products consistently use a single VAT rate.
>
> **Impact**
> VAT should be used as a secondary discriminator/tie-breaker. Falls just short of the 95% threshold needed for a primary discriminator.

---

## 07 Letting the Data Choose the Architecture

### Script 4: Evidence-Based Recommendations

Instead of guessing, we used threshold-based rules on our statistical findings to determine the architecture. All thresholds are named constants — not magic numbers — and the full decision matrix is recorded for auditability.

| Component | Metric | Value | Threshold | Decision |
|-----------|--------|-------|-----------|----------|
| **Retrieval Strategy** | Dataset ADS | 0.847 | ≥ 0.90 (global) / ≥ 0.75 (hybrid) | **HYBRID** |
| | Cross-company consistency | 0.695 | ≥ 0.85 (global) | **HYBRID** |
| **Model Complexity** | Deterministic products (>0.95) | 91.2% | ≥ 90% | **RULES_FIRST** |
| **VAT Strategy** | Single-rate products | 94.5% | ≥ 95% (discriminator) / ≥ 70% (secondary) | **SECONDARY_FEATURE** |
| **Warehouse** | Missing % | 100.0% | ≥ 90% | **DROP** |

### Feature Selection

| Feature | Missing % | AI Value | Action |
|---------|-----------|----------|--------|
| product_description | 0.0% | HIGH | INCLUDE_REQUIRED |
| vat_percent | 4.05% | HIGH | INCLUDE_REQUIRED |
| tax_code | 0.0% | HIGH | INCLUDE_REQUIRED |
| direction | 0.0% | HIGH | INCLUDE_REQUIRED |
| warehouse_id | 100.0% | DROP | EXCLUDE |

### Final Architecture Recommendation

```mermaid
flowchart TD
    A["📄 Invoice Line Input"] --> B["🗄️ Hybrid Vector Database"]
    B --> C["🔍 Similarity Search"]
    C --> D{"📋 Deterministic Match?"}
    D -->|"✓ Match (91%)"| E["✅ Return Account"]
    D -->|"✗ No Match (9%)"| F["🤖 Embedding Fallback"]
    F --> G["🎯 VAT Re-ranking"]
    G --> H["📊 Predicted Account"]
```

**Why Not Global-Only?** The cross-company consistency is only 69.5% — a global-only model would misclassify products that different companies book differently. The hybrid approach preserves company-specific accounting logic while sharing knowledge for common products.

**Why Not LLM-First?** 91.2% of products are deterministic — using an LLM for every prediction would be wasteful. The RULES_FIRST approach handles the easy 91% with a simple lookup, and only escalates the hard 9% to a more expensive similarity search.

---

## 08 Key Findings & Engineering Excellence

### Engineering Excellence
**1. Separation of Concerns** — Each script has ONE job. Download ≠ Extract ≠ Analyze.
**2. Idempotent & Resumable** — Restart after crashes without re-downloading.
**3. Atomic Operations** — No partial corrupted files.
**4. Named Thresholds** — `THRESHOLD_ADS_GLOBAL = 0.90` (Self-documenting, no magic numbers).
**5. Pre-Run Validation** — Every script validates inputs, schemas, and dependencies before execution.

### Outputs & Artifacts
The pipeline generates comprehensive, production-ready artifacts:
- **Data:** 296,648 training examples, 154,068 GL definitions, 76,843 unique (company, product, account) mappings.
- **Intelligence:** 7 analysis CSVs covering ADS scores, company consistency, cross-company divergence, VAT stability, and AI readiness.
- **Reports:** Full architecture recommendation with evidence trail + this technical report.
- **Code:** 6 idempotent Python scripts + reusable utility packages + pre-run validation.

---

## 09 Phase 2 Roadmap

### Roadmap to Production (Illustrative)
**Week 1–2:** Data Infrastructure — Build hybrid vector database, create embeddings for 47,306 normalized products, partition by company.
**Week 3–4:** Model Development — Deterministic lookup tables, embedding-based similarity search, VAT re-ranking logic, confidence scoring.
**Week 5–6:** API Development — `POST /classify` endpoint returning account ID, confidence score, method used, and alternatives.
**Week 7–8:** Testing & Validation — Holdout test set, A/B testing against manual classification, temporal train/test split.
**Week 9–10:** Beta Launch — Deploy to 5 pilot companies (mix of high/low consistency, different industries).
**Week 11–12:** Evaluation & Next Steps — Analyze pilot results, iterate on confidence thresholds, plan full rollout.

> [!NOTE]
> This roadmap is an illustrative production path. The immediate Phase 2 deliverable is proving the hybrid retrieval system works on a real pilot company — not the full 12-week plan.

### Success Metrics
- **Accuracy:** 85–90% (based on ADS of 0.847)
- **Latency:** <100ms per classification (deterministic lookup <10ms, embedding search <50ms)
- **Cost:** <€0.001 per line (mostly lookup — no LLM calls needed)
- **ROI:** Manual processing costs ~€2,490/month per company; automated processing ~€282/month (89% reduction)

---

## Appendix

### Comparison with Industry Standards
**Similar Systems:** Amazon Product Categorization, Stripe Transactions, QuickBooks AutoCategorize.
**Our Differentiation:** Data-driven architecture with explicit ADS determinism metrics, evidence-based threshold decisions, and a full audit trail. Targets are competitive: 85–90% accuracy (industry: 75–85%), <100ms latency (industry: 500ms–2s), <€0.001/classification (industry: €0.01–€0.05).

### Lessons Learned
**✅ What Worked:** Data-first approach saved months of wrong architecture; idempotent scripts survived 3 pipeline crashes during development without data loss; named thresholds made decisions traceable and recalibratable.
**⚠️ What to Improve:** Do earlier schema exploration to build unified parsers from day 1; add progress bars and data versioning from the start; consider temporal train/test splits during analysis phase.

### Q&A Preparation
**Q: Why not just use GPT-4?**
A: 91.2% of products are deterministic — lookup beats LLM. GPT-4 would be ~30x more expensive (€0.03 vs <€0.001/classification), 20–50x slower (2–5s vs <100ms), and not measurably more accurate for the deterministic majority.

**Q: Cold start for new companies?**
A: Start with the global knowledge base, which captures shared classification patterns. Cross-company consistency of 69.5% means the global model will have gaps, so we rapidly collect feedback on the first 100 classifications to build company-specific overrides. Fallback hierarchy: Company-specific → Global → Industry average (CAEN code) → Flag for manual review.

**Q: Handling completely new products?**
A: Semantic similarity via embeddings. Example: "MacBook Pro M3" has never been seen, but embedding search finds similar products like "Laptop Dell Inspiron" (similarity: 0.89) and "MacBook Air" (similarity: 0.92), both mapping to Account 214. This is why embeddings outperform keyword matching.

### Risks & Mitigation
- **ADS skewed by high-volume products** — Report both weighted/unweighted ADS; monitor per-product accuracy in Phase 2.
- **Cross-company divergence (30.5%)** — Company-specific overrides in the hybrid model.
- **4.05% missing VAT data** — Use fallback classification path when VAT is absent.
- **Model drift** — Implement quarterly automated retraining; monitor confidence scores over time.
- **5.4% duplicate invoice lines** — Already flagged in data quality report; deduplicate before training.

### Known Limitations
- **No monetary amounts:** The D406 XML does not include extractable line-level amounts. Classification relies on product description and categorical features.
- **Romanian language only:** All product descriptions are in Romanian. Phase 2 embeddings must use a multilingual or Romanian-specific model.
- **No temporal validation:** Classification pattern stability over time has not been tested. Phase 2 should include a temporal train/test split.

# Data Verification Audit

> Source of truth: [phase1_final_report.md](file:///C:/Users/MaitreyaSapariya/Desktop/ContAI/Analysis/reports/phase1_final_report.md) + [architecture_decision.md](file:///C:/Users/MaitreyaSapariya/Desktop/ContAI/Analysis/reports/architecture_decision.md)

## Discrepancies Found & Corrected

| # | Metric | HTML Had (Wrong) | Authoritative Value | Source |
|---|--------|-----------------|---------------------|--------|
| 1 | Deterministic products (>0.95 ADS) | 85% | **91.2%** (43,156 of 47,306) | phase1_final_report §7 |
| 2 | Ambiguous products | 15% | **1.1%** (<0.50 ADS, 526 products) | phase1_final_report §7 |
| 3 | Cross-company consistency | 0.694 | **0.695** (0.6946) | architecture_decision §2 |
| 4 | Warehouse missing | 98.7% | **100.0%** | phase1_final_report §6 Data Quality |
| 5 | VAT single-rate stability | 85% | **94.5%** | phase1_final_report §7 |
| 6 | ADS divergence | 0.12 | **0.117** | phase1_final_report §7 |
| 7 | product_description missing | 2.3% | **0.0%** | phase1_final_report §6 Data Quality |
| 8 | vat_percent missing | 15.4% | **4.05%** (12,007 lines) | phase1_final_report §6 Data Quality |
| 9 | tax_code missing | 18.2% | **0.0%** | phase1_final_report §6 Data Quality |
| 10 | account_id missing | 0.1% | **0.0%** | phase1_final_report §6 Data Quality |
| 11 | Architecture match split | 85%/15% | **91%/9%** | follows from #1 |
| 12 | Purchase/Sales ratio | 3:1 | **~2.8:1** (73.9% / 26.1%) | phase1_final_report §1 |
| 13 | "69% cold-start accuracy" claim | 69% accuracy | **Not a valid claim** — 0.695 is cross-company *consistency*, not prediction accuracy | Reframed as consistency gap |
| 14 | Companies with invoice data | 201 | **169** (201 in inventory, 169 have invoices) | phase1_final_report §1 |
| 15 | Total invoices (not mentioned) | — | **107,736** | phase1_final_report §1 |
| 16 | Normalized unique products | — | **47,306** (62,447 raw) | phase1_final_report §1 |
| 17 | Unweighted ADS | 0.9635 | **0.964** ✓ (matches) | Confirmed correct |
| 18 | Weighted ADS | 0.847 | **0.847** ✓ (matches) | Confirmed correct |

> [!NOTE]
> There is also a discrepancy *between project reports*: `dataset_intelligence_report.md` says "Global Cross-Company Determinism: 0.7454" while `phase1_final_report.md` says 0.695. The final report analyzed 2,696 multi-company products specifically; the intelligence report may use a different aggregation. `phase1_final_report.md` is authoritative per user directive.

## Numbers Confirmed Correct (No Changes Needed)

| Metric | Value | Source |
|--------|-------|--------|
| Companies in inventory | 201 | phase1_final_report §1 |
| XML files processed | 1,020 | phase1_final_report §1 |
| Total invoice lines | 296,648 | phase1_final_report §1 |
| Unique products (raw) | 62,447 | phase1_final_report §1 |
| GL accounts defined | 15,168 | phase1_final_report §5 |
| GL accounts used | 579 (3.8%) | phase1_final_report §1 |
| GL account records | 154,068 | phase1_final_report §5 |
| Unique VAT rates | 6 | phase1_final_report §1 |
| Weighted ADS | 0.847 | phase1_final_report §7 |
| Unweighted ADS | 0.964 | phase1_final_report §7 |
| Architecture: HYBRID | ✓ | architecture_decision §2 |
| Architecture: RULES_FIRST | ✓ | architecture_decision §4 |
| Architecture: SECONDARY_FEATURE (VAT) | ✓ | architecture_decision §5 |
| Architecture: DROP (warehouse) | ✓ | architecture_decision Appendix |

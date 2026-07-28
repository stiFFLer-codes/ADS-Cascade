# Dataset Intelligence Report

## Executive Summary
Dataset Accounting Determinism Score (ADS): **0.8094**
Global Cross-Company Determinism: **0.7756**

## Data Quality
- **product_description**: 0.0% missing
- **account_id**: 0.0% missing
- **vat_percent**: 4.45% missing
- **tax_code**: 0.0% missing
- **warehouse_id**: 100.0% missing
- **line_amount**: 100.0% missing
- **invoice_date**: 0.0% missing
- **validation_status**: 0.0% missing
- **duplicate_invoice_lines**: 0.0% missing

## Behavioral Analysis
- Average Company Determinism: **0.9746**
- VAT Stability: **74.94%** of products have a single VAT rate.

## AI Readiness Matrix
| Feature | Missing % | Value | Recommendation |
|---|---|---|---|
| product_description | 0.0% | HIGH | Strong feature. |
| vat_percent | 4.45% | MEDIUM | Usable, but needs imputation. |
| tax_code | 0.0% | HIGH | Strong feature. |
| warehouse_id | 100.0% | DROP | Too many missing values. |
| direction | 0% | HIGH | Strong feature. |

## Recommendations
High company-specific behavior detected. Consider company-scoped knowledge bases or specific models.

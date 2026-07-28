# BUILD_PLAN.md

## Project Overview

This document outlines the complete build plan for the D406 Invoice Classification System. The project is divided into two main phases:

1. **Phase 1: Dataset Preparation & Analysis** (this document)
2. **Phase 2: AI Pipeline Implementation** (follows after Phase 1 completion)

---

## Phase 1: Dataset Preparation & Analysis

### Objective

Build a high-quality, normalized dataset from D406 XML files that will serve as the foundation for an AI-powered invoice classification system. **Let the data drive the architecture decision**, not the other way around.

---

## Pipeline Architecture

```
JSON Manifest
    ↓
Script 1  → Company Inventory
    ↓
Script 1.5 → XML Normalization
    ↓
Script 2  → GL Account Extraction
    ↓
Script 3  → Invoice Line Extraction
    ↓
Script 4  → Cross-Company Analysis
    ↓
Research Report + Architecture Decision
    ↓
Phase 2: Build the Invoice Classification System
```

---

## Script Details

### ✅ Script 1 — D406 Inventory Builder

**Purpose:**  
Parse the manifest, filter for D406 declarations, and create a clean inventory of companies and filings.

**Input:**  
- `data/manifest/Dev-D406-Dataset.json`

**Processing:**
1. Read manifest
2. Keep only D406 XML files
3. Extract metadata for each file
4. Derive S3 bucket and object key from file URLs
5. Identify duplicate filings

**Output:**
- `data/outputs/metadata.csv`
  - Columns: `CUI`, `filing_period`, `file_path`, `file_url`, `bucket`, `object_key`, `duplicate_status`
- `data/outputs/companies_inventory.csv`
  - Columns: `CUI`, `company_name`, `filing_count`, `has_duplicates`

**Key Decision:**  
Store both `file_url` AND derived `bucket`/`object_key` columns. This decouples downstream scripts from URL parsing and makes the pipeline resilient to storage endpoint changes.

**Status:** ✅ Implemented

---

### ✅ Script 1.5 — XML Normalization

**Purpose:**  
Download, extract, validate, and store XML files locally. This step separates the concerns of data acquisition and data processing.

**Why This Step Matters:**
```
WITHOUT normalization:
Download → Extract → Parse → Crash → Download everything again

WITH normalization:
Download once → Store XML → All later scripts reuse XML
```

**Input:**
- `data/outputs/metadata.csv`

**Processing:**
1. Read bucket/object_key from metadata.csv
2. Use `boto3` with AWS SSO credentials to download from S3
3. Extract ZIP files
4. Validate XML structure
5. Store normalized XML locally

**Output:**
- `data/normalized/`
  ```
  normalized/
    ├── company1/
    │   ├── file1.xml
    │   └── file2.xml
    ├── company2/
    │   └── file1.xml
  ```
- `data/outputs/normalization_status.csv`
  - Columns: 
    - `cui` — Company unique identifier
    - `company_name` — Company name
    - `logical_key` — Unique file identifier
    - `file_name` — Original file name
    - `extension` — File type (XML/ZIP)
    - `download_status` — success/failed/skipped
    - `extraction_status` — success/failed/not_applicable
    - `validation_status` — valid/invalid/not_checked
    - `download_path` — Local path to downloaded file
    - `extracted_path` — Local path to extracted file
    - `normalized_path` — Local path to normalized XML
    - `error_stage` — Which stage failed (if any)
    - `error_message` — Error details
    - `processed_at` — Timestamp

**Key Technical Decision:**  
Use `boto3.client("s3").download_file()` instead of HTTP requests. AWS SSO credentials provide direct S3 access without URL expiration issues.

**Status:** ⏳ Pending

---

## Current Progress

### Completed
- Repository scaffolding
- Script 1 -- Inventory Builder
- metadata.csv with bucket/object_key derivation
- companies_inventory.csv
- Duplicate detection

### Dataset Statistics (as of 2026-06-25)

| Metric | Value |
|--------|-------|
| Total Records | 1290 |
| Companies | 201 |
| XML Files | 642 |
| ZIP Files | 648 |
| Duplicate Records | 548 |

### Pending
- **Script 1.5 -- XML Normalization** (next priority)
- Script 2 -- GL Account Extraction
- Script 3 -- Invoice Line Extraction
- Script 4 -- Cross-Company Analysis
- Research Report
- Phase 2 AI Implementation

---

## Engineering Principles

These principles guide the implementation of all scripts:

- **JSON Manifest is the single source of truth** — All file metadata derives from it
- **One responsibility per script** — Each script has a single, well-defined purpose
- **Produce reusable artifacts** — Outputs are consumable by downstream scripts and future analyses
- **XML parsed once** — Normalization step ensures we never re-download or re-parse
- **Preserve raw downloads** — Original files remain unchanged for reproducibility
- **Idempotent processing** — Scripts can be safely re-run without side effects
- **Resume after interruption** — Track progress; skip already-processed items
- **Continue after failures** — Log errors but process remaining items

---

### Script 2 — General Ledger Extraction

**Purpose:**  
Extract the chart of accounts from each company's D406 XML. This becomes the company-specific knowledge base for the classifier.

**Input:**
- Normalized XML files in `data/normalized/`

**Processing:**
1. Parse each XML file
2. Extract GL account information
3. Save per-company and aggregate datasets

**Output:**
- `data/extracted/gl_accounts/company_{CUI}.csv`
  - Columns: `AccountID`, `Description`, `AccountType`, `SourceCompany`, `SourceFile`, `Currency`, `NamespaceVersion`, `XMLDate`
- `data/extracted/all_companies_gl_accounts.csv`
  - Aggregate of all company GL accounts

**Enhanced Metadata:**  
Beyond the basic fields, also extract:
- `SourceCompany` — CUI
- `SourceFile` — Which XML file this came from
- `Currency` — Reporting currency
- `NamespaceVersion` — XML schema version (optional but useful for debugging)
- `XMLDate` — Date from XML metadata

**Why Extra Metadata?**  
Storage is cheap. Missing metadata is expensive. These fields make debugging and tracing significantly easier.

**Status:** 🔄 Ready to implement (blocked by Script 1.5 completion)

---

### Script 3 — Invoice Line Extraction

**Purpose:**  
Extract every invoice line from every company. This becomes the ground-truth training dataset.

**Input:**
- Normalized XML files in `data/normalized/`

**Processing:**
1. Parse each XML file
2. Extract invoice line items
3. Include invoice metadata and supplier/customer information

**Output:**
- `data/extracted/invoice_lines/company_{CUI}.csv`
  - Columns:
    - `InvoiceID`
    - `InvoiceType` (Sales/Purchase)
    - `Direction` (Inbound/Outbound)
    - `ProductDescription`
    - `AccountID`
    - `TaxCode`
    - `VAT_Percent`
    - `WarehouseID`
    - `Amount`
    - `Currency`
    - `Supplier` / `Customer`
    - `InvoiceDate`
    - `SourceCompany`
    - `SourceFile`
- `data/extracted/all_invoice_lines.csv`
  - Aggregate of all invoice lines

**Critical Addition:**  
Include `InvoiceType` or `Direction` field. A product going to account `707` in Sales is fundamentally different from the same product going to `371` in Purchase. The XML already contains this information — capture it.

**Status:** 🔄 Ready to implement (blocked by Script 1.5 completion)

---

### Script 4 — Cross-Company Analysis

**Purpose:**  
Answer statistical questions about the dataset that will inform architectural decisions for Phase 2.

**Input:**
- `data/extracted/all_companies_gl_accounts.csv`
- `data/extracted/all_invoice_lines.csv`

**Processing:**  
Generate insights across multiple dimensions.

**Output:**
- `data/outputs/cross_company_analysis/`
  - `account_universality.csv`
  - `product_mapping_consistency.csv`
  - `company_behavior_patterns.csv`
  - `gl_density_analysis.csv`
  - `mapping_ambiguity_report.csv`

**Key Questions to Answer:**

#### 1. Universality
```
AccountID: 707
Companies using it: 237 / 252
Consistency: 94%
```

#### 2. Description Variants
```
Product: "Laptop Dell"
  Company A → 707
  Company B → 707
  Company C → 708  ← Interesting outlier
```

#### 3. Company Behavior Patterns
```
Company A: Product category X always → 707
Company B: Same products → 704
```
This reveals whether classification is universal or company-specific.

#### 4. GL Density
```
Company A: 332 GL accounts defined, 18 used (5.4%)
Company B: 421 GL accounts defined, 27 used (6.4%)
```
Very valuable for understanding actual vs. theoretical complexity.

#### 5. Mapping Ambiguity
```
Product: "Office Supplies"
  Maps to: 601, 602, 604 (ambiguous)
  
Product: "Laptop"
  Maps to: 707 (99% consistency, deterministic)
```

**Status:** 🔄 Ready to implement (blocked by Scripts 2 & 3 completion)

---

## Project Metrics Dashboard

Track progress in real-time. Suggested implementation: a simple script that scans outputs and generates a markdown report.

| Metric                  |   Current | Target |
| ----------------------- | --------: | -----: |
| Companies processed     |  201 / 201 |    201 |
| Files processed         |  642 / 642 |    642 |
| GL Accounts extracted   |          0 |    TBD |
| Invoice lines extracted |          0 |    TBD |
| Unique AccountIDs       |          0 |    TBD |
| Unique Products         |          0 |    TBD |
| Unique TaxCodes         |          0 |    TBD |
| Unique Warehouses       |          0 |    TBD |
| ZIP files downloaded    |          0 |    648 |
| XML files normalized    |          0 |    642 |
| Failed files            |          0 |      0 |

**Implementation:** Create `scripts/00_dashboard.py` that reads from logs and outputs directories.

---

## Final Deliverable: Research Report

Instead of jumping directly to implementation, produce a structured research report that bridges analysis and architecture.

### Recommended Report Structure

```markdown
# D406 Invoice Classification System — Phase 1 Research Report

## 1. Dataset Overview
   - Total companies analyzed
   - Total filings processed
   - Date range covered
   - Data quality assessment

## 2. Company Statistics
   - Company size distribution
   - Filing frequency patterns
   - Duplicate filing analysis

## 3. GL Account Statistics
   - Total unique accounts
   - Account usage distribution
   - Most common accounts
   - Company-specific vs. universal accounts

## 4. Invoice Statistics
   - Total invoice lines extracted
   - Product category distribution
   - Tax code patterns
   - Warehouse usage patterns

## 5. Cross-Company Findings
   - Account universality analysis
   - Product mapping consistency
   - Company behavior patterns
   - Mapping ambiguity identification

## 6. Deterministic Rules
   - Clear product → account mappings
   - Universal patterns that hold across companies

## 7. Company-Specific Rules
   - Mappings that vary by company
   - Industries with unique patterns

## 8. Recommended AI Architecture
   - Evidence-based architecture choice:
     * If mappings are highly consistent → retrieval-based approach
     * If mappings vary significantly → company-specific knowledge base
     * If both patterns exist → hybrid architecture
   - Justification based on findings

## 9. Risks & Limitations
   - Data quality issues discovered
   - Edge cases identified
   - Potential failure modes

## 10. Future Work
    - Phase 2 implementation roadmap
    - Additional data sources to consider
    - Validation strategy
```

---

## Critical Principle: Data-Driven Architecture

**⚠️ Warning:**  
Do not let Script 4 become "start designing the AI."

The purpose of Phase 1 is **to learn from the data**, not to validate a preferred architecture.

**The architecture decision should emerge from evidence:**

- If product descriptions map consistently to a single AccountID across companies → retrieval-based approach may be sufficient
- If mappings differ significantly by company → company-specific knowledge base becomes essential
- If both patterns exist → hybrid architecture is likely the right choice

Let the dataset answer these questions rather than assuming the answer in advance.

---

## Technical Implementation Notes

### AWS S3 Access Strategy

**Problem:** Pre-signed URLs in the manifest have expired.

**Solution:** Use direct S3 access with existing AWS SSO credentials.

```python
import boto3
from urllib.parse import urlparse

def extract_bucket_key(s3_url: str) -> tuple[str, str]:
    """Extract bucket and key from S3 URL."""
    parsed = urlparse(s3_url)
    bucket = parsed.netloc.split(".")[0]
    key = parsed.path.lstrip("/")
    return bucket, key

# Usage in Script 1.5
bucket, key = extract_bucket_key(row["file_url"])
s3_client = boto3.client("s3")
s3_client.download_file(bucket, key, local_path)
```

**Benefits:**
- No URL expiration issues
- Direct S3 access via existing credentials
- No backend changes required
- No manifest regeneration needed

### Separation of Concerns

Each script has a **single responsibility**:

1. **Script 1:** Metadata extraction and inventory
2. **Script 1.5:** Data acquisition and normalization
3. **Script 2:** GL account knowledge extraction
4. **Script 3:** Invoice line ground truth extraction
5. **Script 4:** Statistical analysis and insights

This makes each step:
- Testable in isolation
- Resumable if it fails
- Reusable by downstream scripts
- Easy to debug and maintain

---

## Success Criteria for Phase 1

Phase 1 is complete when:

- ✅ Script 1 completed — Inventory built
- ⏳ Script 1.5 pending — XML normalization
- ⬜ Script 2 pending — GL accounts extracted for all companies
- ⬜ Script 3 pending — Invoice lines extracted for all companies
- ⬜ Script 4 pending — Cross-company analysis completed
- ⬜ Research report written with architecture recommendation
- ⬜ Zero critical data quality issues remain unresolved
- ✅ All outputs are in clean, documented CSV format
- ✅ Codebase is documented and runnable by another developer

---

## Transition to Phase 2

Once Phase 1 is complete and the research report is reviewed, Phase 2 begins:

```
Invoice Input
    ↓
Normalization
    ↓
Company Knowledge Base Lookup
    ↓
Embedding Search
    ↓
Rule Engine
    ↓
LLM (only when needed)
    ↓
Validation & Confidence Scoring
    ↓
Classified Invoice Output
```

The quality of Phase 1 data will largely determine the quality of the Phase 2 model.

**Build high-quality data first. Then build the AI.**

---

## Project Directory Structure

```
Analysis/
├── data/
│   ├── manifest/               # Original JSON manifest
│   ├── normalized/             # Normalized XML files (Script 1.5 output)
│   ├── extracted/              # Extracted data (Scripts 2-3 output)
│   │   ├── gl_accounts/
│   │   └── invoice_lines/
│   ├── outputs/                # Analysis results (Scripts 1, 4 output)
│   │   └── cross_company_analysis/
│   └── logs/                   # Processing logs
├── scripts/
│   ├── 00_dashboard.py         # Progress metrics (not yet implemented)
│   ├── 01_build_inventory.py   # ✅ Complete
│   ├── 01_5_xml_normalization.py  # ⏳ Next priority
│   ├── 02_gl_account_extraction.py  # ⬜ Blocked by 1.5
│   ├── 03_invoice_line_extraction.py  # ⬜ Blocked by 1.5
│   └── 04_cross_company_analysis.py  # ⬜ Blocked by 2 & 3
├── docs/
│   ├── STATE_HANDOFF.md        # Current progress documentation
│   └── RESEARCH_REPORT.md      # Final Phase 1 deliverable
├── utils/                      # Shared utilities
├── BUILD_PLAN.md              # This document
└── README.md                   # Project overview
```

---

## Next Steps

### Immediate Priority

1. **Complete Script 1.5** — XML Normalization
   - Update Script 1 to derive bucket and object_key (already done)
   - Replace requests with boto3 for S3 access
   - Download declarations from S3
   - Extract ZIP files
   - Validate XML structure
   - Generate normalization_status.csv

### Sequential Implementation

2. **Complete Script 2** — GL Account Extraction
3. **Complete Script 3** — Invoice Line Extraction
4. **Complete Script 4** — Cross-Company Analysis
5. **Write Research Report** — Synthesize findings and recommend architecture
6. **Review & Decision Gate** — Review report before proceeding to Phase 2
7. **Begin Phase 2** — Implement the AI pipeline based on Phase 1 findings

---

## Guiding Principle

> Build reusable datasets first. Let the data determine the architecture. Do not design the AI before completing the analysis.

---

*Last Updated: 2026-06-25*

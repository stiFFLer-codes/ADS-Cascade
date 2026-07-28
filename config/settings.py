"""
config/settings.py
------------------
Central configuration for the contai-analysis pipeline.
All paths and tuneable constants live here — scripts import from this module
instead of hard-coding values.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Root directories
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent   # contai-analysis/

DATA_DIR       = BASE_DIR / "data"
DOWNLOADS_DIR  = DATA_DIR / "downloads"   # original ZIP/XML exactly as downloaded
EXTRACTED_DIR  = DATA_DIR / "extracted"   # XML extracted from ZIPs
NORMALIZED_DIR = DATA_DIR / "normalized"  # validated XML ready for parsing
OUTPUTS_DIR    = DATA_DIR / "outputs"
MANIFEST_DIR   = DATA_DIR / "manifest"
LOGS_DIR       = DATA_DIR / "logs"
REPORTS_DIR    = BASE_DIR / "reports"

# ---------------------------------------------------------------------------
# Key files
# ---------------------------------------------------------------------------

DATASET_FILE = MANIFEST_DIR / "Dev-D406-Dataset.json"

# Expected output CSVs
COMPANIES_CSV     = OUTPUTS_DIR / "companies_inventory.csv"
GL_ACCOUNTS_CSV   = OUTPUTS_DIR / "company_gl_accounts.csv"
GL_CATALOG_JSON   = OUTPUTS_DIR / "company_gl_catalog.json"
GL_STATISTICS_CSV = OUTPUTS_DIR / "gl_statistics.csv"
INVOICE_LINES_CSV = OUTPUTS_DIR / "invoice_lines_all_companies.csv"
INVOICE_LINES_RAW_CSV = OUTPUTS_DIR / "invoice_lines_raw.csv"
PRODUCT_ACCOUNT_MAPPING_CSV = OUTPUTS_DIR / "product_account_mapping.csv"
INVOICE_STATISTICS_CSV = OUTPUTS_DIR / "invoice_statistics.csv"
INVOICE_EXTRACTION_ERRORS_CSV = OUTPUTS_DIR / "invoice_extraction_errors.csv"
CROSS_COMPANY_CSV = OUTPUTS_DIR / "cross_company_account_analysis.csv"
INTELLIGENCE_DIR = OUTPUTS_DIR / "intelligence"

# ---------------------------------------------------------------------------
# Pipeline settings
# ---------------------------------------------------------------------------

# Encoding used for all CSV / text output
CSV_ENCODING = "utf-8-sig"   # BOM variant — opens cleanly in Excel

# Set to True to re-process files that already appear in the manifest
FORCE_REPROCESS = False

# Logging level for file handlers ("DEBUG", "INFO", "WARNING", "ERROR")
LOG_LEVEL_FILE    = "DEBUG"
LOG_LEVEL_CONSOLE = "INFO"

# ---------------------------------------------------------------------------
# 01_5 download settings
# ---------------------------------------------------------------------------

# Number of parallel download threads
DOWNLOAD_WORKERS = 8

# Per-request timeout in seconds
DOWNLOAD_TIMEOUT = 60

# Exponential backoff: wait = min(BACKOFF_BASE * 2^(attempt-1), BACKOFF_MAX)
BACKOFF_BASE         = 1    # seconds — first retry waits 1s, then 2s, 4s …
BACKOFF_MAX          = 30   # seconds — ceiling on any single wait
BACKOFF_MAX_ATTEMPTS = 4    # total attempts before giving up

# AWS profile to use for S3 CLI downloads
AWS_PROFILE = "development"


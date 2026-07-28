"""
01_build_inventory.py
---------------------
Step 1 of the contai-analysis pipeline.

Reads Dev-D406-Dataset.json from data/manifest/ and produces two CSVs:

  data/outputs/metadata.csv              — one row per source file record
  data/outputs/companies_inventory.csv   — one row per unique company (CUI)

Schema fields used
------------------
  cui             : company tax ID
  company_name    : legal name
  caen_code       : industry classification code
  xml_file_name   : source filename  (used to derive extension & reporting period)
  xml_file_size   : file size in KB
  xml_file_url    : S3 download URL
  created_at      : record creation timestamp
  _id             : MongoDB document ID
"""

import json
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Make project-root packages (config/, utils/) importable when the script is
# run directly:  python scripts/01_build_inventory.py
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import OUTPUTS_DIR, LOGS_DIR
from utils.logger import get_logger

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
INPUT_JSON      = PROJECT_ROOT / "data" / "manifest" / "Dev-D406-Dataset.json"
OUTPUT_METADATA  = OUTPUTS_DIR / "metadata.csv"
OUTPUT_COMPANIES = OUTPUTS_DIR / "companies_inventory.csv"

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logger = get_logger("01_build_inventory", log_file="01_build_inventory.log")


# ===========================================================================
# Load JSON
# ===========================================================================

def load_dataset(path: Path) -> list[dict]:
    logger.info("Loading dataset from %s", path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info("Loaded %d records", len(data))
    return data


# ===========================================================================
# Build metadata table
# ===========================================================================

def build_metadata(records: list[dict]) -> pd.DataFrame:
    logger.info("Building metadata table …")

    rows = []
    for record in records:
        file_name = record.get("xml_file_name", "")
        extension = Path(file_name).suffix.lower().lstrip(".")

        rows.append({
            "cui":          record.get("cui"),
            "company_name": record.get("company_name"),
            "caen_code":    record.get("caen_code"),
            "file_name":    file_name,
            "extension":    extension,
            "file_size_kb": record.get("xml_file_size"),
            "file_url":     record.get("xml_file_url"),
            "created_at":   record.get("created_at"),
            "mongo_id":     record.get("_id"),
        })

    df = pd.DataFrame(rows)

    # --- Reporting period from filename  e.g. D406_12345678_31-05-2026_Inf.xml
    df["reporting_period"] = (
        df["file_name"]
        .str.extract(r"(\d{2}-\d{2}-\d{4})", expand=False)
    )

    # --- File-type flags
    df["is_zip"] = df["extension"] == "zip"
    df["is_xml"] = df["extension"] == "xml"

    # --- Logical key: one declaration per company per period
    df["logical_key"] = (
        df["cui"].astype(str)
        + "_"
        + df["reporting_period"].fillna("")
    )

    # --- Duplicate detection
    df["duplicate_count"] = (
        df.groupby("logical_key")["logical_key"]
        .transform("count")
    )
    df["is_duplicate"] = df["duplicate_count"] > 1

    df.sort_values(["company_name", "reporting_period"], inplace=True)

    logger.info(
        "Metadata built: %d records | %d ZIP | %d XML | %d duplicates",
        len(df),
        df["is_zip"].sum(),
        df["is_xml"].sum(),
        df["is_duplicate"].sum(),
    )
    return df


# ===========================================================================
# Build company inventory
# ===========================================================================

def build_company_inventory(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Aggregating company inventory …")

    companies = (
        df.groupby(["cui", "company_name", "caen_code"], dropna=False)
        .agg(
            total_files    = ("file_name",         "count"),
            xml_files      = ("is_xml",            "sum"),
            zip_files      = ("is_zip",            "sum"),
            first_period   = ("reporting_period",  "min"),
            last_period    = ("reporting_period",  "max"),
            duplicate_files= ("is_duplicate",      "sum"),
        )
        .reset_index()
        .sort_values("company_name")
    )

    logger.info("Company inventory: %d unique companies", len(companies))
    return companies


# ===========================================================================
# Save outputs
# ===========================================================================

def save_outputs(metadata: pd.DataFrame, companies: pd.DataFrame) -> None:
    metadata.to_csv(OUTPUT_METADATA, index=False, encoding="utf-8-sig")
    logger.info("Saved metadata   → %s", OUTPUT_METADATA)

    companies.to_csv(OUTPUT_COMPANIES, index=False, encoding="utf-8-sig")
    logger.info("Saved inventory  → %s", OUTPUT_COMPANIES)


# ===========================================================================
# Summary
# ===========================================================================

def print_summary(metadata: pd.DataFrame, companies: pd.DataFrame) -> None:
    sep = "=" * 60
    print(sep)
    print("  Inventory Successfully Created")
    print(sep)
    print(f"  Total Records      : {len(metadata)}")
    print(f"  Companies          : {len(companies)}")
    print(f"  XML Files          : {int(metadata['is_xml'].sum())}")
    print(f"  ZIP Files          : {int(metadata['is_zip'].sum())}")
    print(f"  Duplicate Records  : {int(metadata['is_duplicate'].sum())}")
    print(sep)
    print("  Generated Files")
    print(sep)
    print(f"  {OUTPUT_METADATA}")
    print(f"  {OUTPUT_COMPANIES}")
    print(sep)


# ===========================================================================
# Entry point
# ===========================================================================

def main() -> None:
    records  = load_dataset(INPUT_JSON)
    metadata = build_metadata(records)
    companies = build_company_inventory(metadata)
    save_outputs(metadata, companies)
    print_summary(metadata, companies)


if __name__ == "__main__":
    main()

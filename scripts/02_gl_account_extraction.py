"""
02_gl_account_extraction.py
----------------------------
Extract the complete General Ledger master from every normalized D406 XML.

Input:  data/normalized/<CUI>/*.xml
        data/outputs/metadata.csv
Output: data/outputs/company_gl_accounts.csv
        data/outputs/company_gl_catalog.json
        data/outputs/gl_statistics.csv
"""

import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import (
    CSV_ENCODING,
    GL_ACCOUNTS_CSV,
    GL_CATALOG_JSON,
    GL_STATISTICS_CSV,
    NORMALIZED_DIR,
    OUTPUTS_DIR,
)
from utils.csv_writer import write_csv
from utils.filesystem import save_json
from utils.logger import get_logger

logger = get_logger("02_gl_account_extraction", log_file="02_gl_account_extraction.log")

GL_FIELDNAMES = [
    "cui",
    "company_name",
    "reporting_period",
    "source_file",
    "account_id",
    "account_description",
    "standard_account_id",
    "account_type",
    "opening_debit",
    "opening_credit",
    "closing_debit",
    "closing_credit",
    "currency_code",
    "namespace",
]

STATS_FIELDNAMES = ["metric", "value"]

_DATE_PATTERN = re.compile(r"(\d{2}-\d{2}-\d{4})")


def _extract_namespace(root: ET.Element) -> dict[str, str]:
    """Build an ``{prefix: uri}`` map from the root element's namespace.

    Works with any schema version — no hardcoded URIs.
    """
    tag = root.tag
    if "}" in tag:
        ns_uri = tag.split("}")[0].lstrip("{")
        return {"ns": ns_uri}
    return {}


def load_metadata(metadata_path: Path) -> dict[str, dict]:
    """Return ``{cui: {company_name, caen_code}}`` from *metadata_path*.

    The CSV produced by Script 1 is the single source of truth for
    company-level attributes.
    """
    meta: dict[str, dict] = {}
    try:
        with open(metadata_path, "r", encoding=CSV_ENCODING) as f:
            reader = csv.DictReader(f)
            for row in reader:
                cui = row["cui"]
                if cui not in meta:
                    meta[cui] = {
                        "company_name": row["company_name"],
                        "caen_code": row["caen_code"],
                    }
    except FileNotFoundError:
        logger.warning("Metadata not found — output will lack enrichment: %s", metadata_path)
    return meta


def _extract_reporting_period(source: Path) -> str:
    """Derive ``DD-MM-YYYY`` reporting period from the XML filename."""
    m = _DATE_PATTERN.search(source.name)
    return m.group(1) if m else ""


def extract_gl_from_xml(
    xml_path: Path,
    cui: str,
    company_name: str,
    metadata: dict[str, dict],
) -> list[dict]:
    """Parse a single normalized XML and return its GL account records.

    Parameters
    ----------
    xml_path:     Path to the normalized XML.
    cui:          Company identifier (from the parent directory name).
    company_name: Company name from metadata.
    metadata:     Full metadata dict (unused here but reserved for future
                  enrichment without changing the signature).

    Returns
    -------
    list[dict]  One dict per ``<Account>`` element.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = _extract_namespace(root)

    # DefaultCurrencyCode from Header
    currency_code = ""
    header = root.find("ns:Header", ns)
    if header is not None:
        cur_el = header.find("ns:DefaultCurrencyCode", ns)
        if cur_el is not None and cur_el.text:
            currency_code = cur_el.text.strip()

    # MasterFiles → GeneralLedgerAccounts
    mf = root.find("ns:MasterFiles", ns)
    if mf is None:
        logger.warning("MISSING_MASTER_FILES | %s | %s", xml_path.name, cui)
        return []

    gla = mf.find("ns:GeneralLedgerAccounts", ns)
    if gla is None:
        logger.warning("MISSING_GL_SECTION | %s | %s", xml_path.name, cui)
        return []

    accounts = gla.findall("ns:Account", ns)
    if not accounts:
        logger.warning("MISSING_GL_ACCOUNTS | %s | %s", xml_path.name, cui)
        return []

    reporting_period = _extract_reporting_period(xml_path)

    namespace_uri = ns.get("ns", "")
    records = []
    for acc in accounts:
        records.append(
            {
                "cui": cui,
                "company_name": company_name,
                "reporting_period": reporting_period,
                "source_file": xml_path.name,
                "account_id": _safe_findtext(acc, "ns:AccountID", ns),
                "account_description": _safe_findtext(acc, "ns:AccountDescription", ns),
                "standard_account_id": _safe_findtext(acc, "ns:StandardAccountID", ns),
                "account_type": _safe_findtext(acc, "ns:AccountType", ns),
                "opening_debit": _safe_findtext(acc, "ns:OpeningDebitBalance", ns),
                "opening_credit": _safe_findtext(acc, "ns:OpeningCreditBalance", ns),
                "closing_debit": _safe_findtext(acc, "ns:ClosingDebitBalance", ns),
                "closing_credit": _safe_findtext(acc, "ns:ClosingCreditBalance", ns),
                "currency_code": currency_code,
                "namespace": namespace_uri,
            }
        )

    return records


def _safe_findtext(element: ET.Element, xpath: str, ns: dict[str, str]) -> str:
    """Return stripped text or ``""`` on missing element."""
    child = element.find(xpath, ns)
    if child is not None and child.text:
        return child.text.strip()
    return ""


def build_gl_catalog(all_rows: list[dict]) -> dict[str, dict[str, dict]]:
    """Build ``{cui: {account_id: {description, type}}}`` for O(1) lookups."""
    catalog: dict[str, dict[str, dict]] = {}
    for row in all_rows:
        cui = row["cui"]
        catalog.setdefault(cui, {})[row["account_id"]] = {
            "description": row["account_description"],
            "type": row["account_type"],
        }
    return catalog


def compute_statistics(
    all_rows: list[dict],
    total_xmls: int,
    failed_xmls: int,
) -> list[dict[str, str | int]]:
    """Return a list of metric → value rows for ``gl_statistics.csv``."""
    companies = set(r["cui"] for r in all_rows)
    total_companies = len(companies)

    per_company = Counter(r["cui"] for r in all_rows)
    counts = list(per_company.values())

    return [
        {"metric": "Total Companies", "value": total_companies},
        {"metric": "Total XML Parsed", "value": total_xmls},
        {"metric": "Total GL Accounts", "value": len(all_rows)},
        {"metric": "Unique AccountIDs", "value": len({r["account_id"] for r in all_rows})},
        {"metric": "Avg Accounts / Company", "value": round(len(all_rows) / total_companies, 1) if total_companies else 0},
        {"metric": "Min Accounts", "value": min(counts) if counts else 0},
        {"metric": "Max Accounts", "value": max(counts) if counts else 0},
        {"metric": "Failed XMLs", "value": failed_xmls},
    ]


def main() -> None:
    logger.info("=" * 60)
    logger.info("Script 2 — GL Account Extraction — start")
    logger.info("=" * 60)

    # ---- metadata ----
    metadata_path = OUTPUTS_DIR / "metadata.csv"
    metadata = load_metadata(metadata_path)
    logger.info("Metadata loaded: %d companies", len(metadata))

    # ---- discover XMLs ----
    xml_files = sorted(NORMALIZED_DIR.rglob("*.xml"))
    logger.info("Discovered %d normalized XML files", len(xml_files))

    if not xml_files:
        logger.warning("No XML files found under %s — nothing to do.", NORMALIZED_DIR)
        return

    # ---- process ----
    all_rows: list[dict] = []
    failed_xmls = 0

    for xml_path in xml_files:
        # CUI is the immediate parent directory name
        cui = xml_path.parent.name
        company_info = metadata.get(cui, {})
        company_name = company_info.get("company_name", "")

        error_stage = ""
        try:
            error_stage = "extract_gl"
            records = extract_gl_from_xml(xml_path, cui, company_name, metadata)
            all_rows.extend(records)
            logger.debug("OK | %s | %s | %d accounts", xml_path.name, cui, len(records))
        except ET.ParseError as e:
            failed_xmls += 1
            logger.error("PARSE_ERROR | %s | %s | %s", xml_path.name, cui, e)
        except Exception as e:
            failed_xmls += 1
            logger.error("EXCEPTION | %s | %s | %s | %s", xml_path.name, cui, e, error_stage)

    # ---- write outputs ----
    logger.info("Total accounts extracted: %d", len(all_rows))
    logger.info("Failed XMLs: %d", failed_xmls)

    # 1. Flat CSV
    rows_written = write_csv(all_rows, GL_ACCOUNTS_CSV, fieldnames=GL_FIELDNAMES)
    logger.info("Wrote %d rows to %s", rows_written, GL_ACCOUNTS_CSV)

    # 2. JSON catalog
    catalog = build_gl_catalog(all_rows)
    save_json(catalog, GL_CATALOG_JSON)
    logger.info("Wrote catalog (%d companies) to %s", len(catalog), GL_CATALOG_JSON)

    # 3. Statistics CSV
    stats = compute_statistics(all_rows, len(xml_files), failed_xmls)
    write_csv(stats, GL_STATISTICS_CSV, fieldnames=STATS_FIELDNAMES)
    for s in stats:
        logger.info("Stat | %s: %s", s["metric"], s["value"])

    logger.info("Script 2 — GL Account Extraction — done")


if __name__ == "__main__":
    main()

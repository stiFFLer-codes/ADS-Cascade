"""
03_invoice_line_extraction.py
------------------------------
Step 3 of the analysis pipeline.

Extracts invoice line items from normalized XML files.
Phase 1: Raw extraction to invoice_lines_raw.csv.
Phase 2: Enrichment with GL catalog & metadata, validation, mapping generation.

Input:  data/normalized/*.xml
        data/outputs/company_gl_catalog.json
        data/outputs/metadata.csv
Output: data/outputs/invoice_lines_raw.csv
        data/outputs/invoice_lines_all_companies.csv
        data/outputs/product_account_mapping.csv
        data/outputs/invoice_statistics.csv
        data/outputs/invoice_extraction_errors.csv
"""

import csv
import json
import re
import sys
import hashlib
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    from tqdm import tqdm
except ImportError:
    # Fallback if tqdm not installed
    def tqdm(iterable, *args, **kwargs):
        return iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import (
    NORMALIZED_DIR,
    GL_CATALOG_JSON,
    OUTPUTS_DIR,
    CSV_ENCODING,
    INVOICE_LINES_RAW_CSV,
    INVOICE_LINES_CSV,
    PRODUCT_ACCOUNT_MAPPING_CSV,
    INVOICE_STATISTICS_CSV,
    INVOICE_EXTRACTION_ERRORS_CSV,
)
from utils.logger import get_logger

logger = get_logger("03_invoice_line_extraction", log_file="03_invoice_line_extraction.log")

RAW_FIELDNAMES = [
    "logical_key", "source_file", "sha256", "schema_version",
    "invoice_number", "invoice_date", "invoice_type", "direction",
    "line_number", "product_code", "product_description",
    "quantity", "unit_of_measure", "unit_price", "line_amount",
    "vat_percent", "tax_code", "tax_type", "tax_amount",
    "account_id"
]

ENRICHED_FIELDNAMES = [
    "logical_key", "cui", "company_name", "reporting_period", "source_file",
    "sha256", "schema_version",
    "invoice_number", "invoice_date", "invoice_type", "direction",
    "line_number", "product_code", "product_description", "normalized_product",
    "quantity", "unit_of_measure", "unit_price", "line_amount",
    "vat_percent", "tax_code", "tax_type", "tax_amount",
    "account_id", "account_description", "account_type",
    "warehouse_id", "warehouse_exists",
    "validation_status"
]

MAPPING_FIELDNAMES = [
    "Company", "Product", "Normalized Product",
    "AccountID", "AccountDescription", "AccountType",
    "Count", "First Seen", "Last Seen"
]

ERROR_FIELDNAMES = [
    "source_file", "logical_key", "invoice_number", "error_type", "error_message"
]


def _extract_namespace(root: ET.Element) -> dict[str, str]:
    tag = root.tag
    if "}" in tag:
        ns_uri = tag.split("}")[0].lstrip("{")
        return {"ns": ns_uri}
    return {}

def extract_logical_key(filename: str) -> str:
    m = re.search(r'_(\d+)_(\d{2}-\d{2}-\d{4})_', filename)
    if m:
         return f"{m.group(1)}_{m.group(2)}"
    return ""

def file_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def normalize_product(product: str) -> str:
    if not product: return ""
    p = product.lower()
    p = re.sub(r'\s+', ' ', p)
    return p.strip()


class InvoiceSchema:
    def __init__(self, ns: dict[str, str]):
        self.ns = ns

    def get(self, el, tags, default=""):
        if el is None: return default
        for tag in tags:
            val = el.find(f"ns:{tag}", self.ns)
            if val is not None and val.text:
                return val.text.strip()
        return default

    def find_lines(self, inv):
        lines = inv.findall("ns:Line", self.ns)
        if not lines:
            lines = inv.findall("ns:InvoiceLine", self.ns)
        return lines

    def get_description(self, el):
        return self.get(el, ["Description", "ItemDescription", "ProductDescription", "Product"])

    def get_account_id(self, el):
        return self.get(el, ["AccountID", "AccountNumber", "GLAccount"])

    def get_vat_percent(self, el):
        tax_inf = el.find("ns:TaxInformation", self.ns)
        if tax_inf is not None:
            res = self.get(tax_inf, ["TaxPercentage", "TaxRate"])
            if res: return res
        return self.get(el, ["TaxPercentage", "VATPercent", "TaxRate", "VATRate"])
        
    def get_tax_code(self, el):
        tax_inf = el.find("ns:TaxInformation", self.ns)
        if tax_inf is not None:
            res = self.get(tax_inf, ["TaxCode"])
            if res: return res
        return self.get(el, ["TaxCode"])
        
    def get_tax_type(self, el):
        tax_inf = el.find("ns:TaxInformation", self.ns)
        if tax_inf is not None:
            res = self.get(tax_inf, ["TaxType"])
            if res: return res
        return self.get(el, ["TaxType"])
        
    def get_tax_amount(self, el):
        tax_inf = el.find("ns:TaxInformation", self.ns)
        if tax_inf is not None:
            res = self.get(tax_inf, ["TaxAmount", "Amount"])
            if res: return res
        return self.get(el, ["TaxAmount"])

    def get_product_code(self, el):
        return self.get(el, ["ProductCode", "ItemCode"])

    def get_quantity(self, el):
        return self.get(el, ["Quantity"])

    def get_uom(self, el):
        return self.get(el, ["UnitOfMeasure", "UOM"])

    def get_unit_price(self, el):
        return self.get(el, ["UnitPrice", "Price"])

    def get_line_amount(self, el):
        return self.get(el, ["LineAmount", "InvoiceLineAmount", "Amount", "NetTotal", "CreditAmount", "DebitAmount"])

    def get_line_number(self, el):
        return self.get(el, ["LineNumber"])


def _write_csv_headers():
    for p, fields in [
        (INVOICE_LINES_RAW_CSV, RAW_FIELDNAMES),
        (INVOICE_LINES_CSV, ENRICHED_FIELDNAMES),
        (PRODUCT_ACCOUNT_MAPPING_CSV, MAPPING_FIELDNAMES),
        (INVOICE_EXTRACTION_ERRORS_CSV, ERROR_FIELDNAMES),
    ]:
        with open(p, "w", encoding=CSV_ENCODING, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

def load_gl_catalog() -> dict:
    if not GL_CATALOG_JSON.exists():
        logger.warning("company_gl_catalog.json not found!")
        return {}
    with open(GL_CATALOG_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def load_metadata() -> dict:
    meta = {}
    path = OUTPUTS_DIR / "metadata.csv"
    if not path.exists():
        logger.warning("metadata.csv not found!")
        return meta
    with open(path, "r", encoding=CSV_ENCODING) as f:
        for row in csv.DictReader(f):
            if row.get("is_duplicate", "").lower() == "true":
                continue
            lk = row.get("logical_key")
            if lk:
                meta[lk] = {
                    "cui": row.get("cui", ""),
                    "company_name": row.get("company_name", ""),
                    "reporting_period": row.get("reporting_period", "")
                }
    return meta


def phase_1_raw_extraction(xml_files: list[Path]):
    logger.info("Starting Phase 1: Raw Extraction")
    
    with open(INVOICE_LINES_RAW_CSV, "a", encoding=CSV_ENCODING, newline="") as f_raw, \
         open(INVOICE_EXTRACTION_ERRORS_CSV, "a", encoding=CSV_ENCODING, newline="") as f_err:
         
        raw_writer = csv.DictWriter(f_raw, fieldnames=RAW_FIELDNAMES)
        err_writer = csv.DictWriter(f_err, fieldnames=ERROR_FIELDNAMES)
        
        buffer = []
        errors = []
        
        def flush():
            if buffer:
                raw_writer.writerows(buffer)
                buffer.clear()
            if errors:
                err_writer.writerows(errors)
                errors.clear()

        for xml_path in tqdm(xml_files, desc="Phase 1", unit="file"):
            lk = extract_logical_key(xml_path.name)
            try:
                h = file_sha256(xml_path)
                tree = ET.parse(xml_path)
                root = tree.getroot()
                ns = _extract_namespace(root)
                
                sv = root.attrib.get("AuditFileVersion") or root.attrib.get("version", "")
                if not sv:
                    header = root.find("ns:Header", ns)
                    if header is not None:
                        av = header.find("ns:AuditFileVersion", ns)
                        if av is not None and av.text:
                            sv = av.text.strip()
                
                schema = InvoiceSchema(ns)
                sd = root.find("ns:SourceDocuments", ns)
                if sd is None:
                    continue
                
                for section, direction in [("ns:SalesInvoices", "SALE"), ("ns:PurchaseInvoices", "PURCHASE")]:
                    doc_section = sd.find(section, ns)
                    if doc_section is not None:
                        for inv in doc_section.findall("ns:Invoice", ns):
                            inv_no = schema.get(inv, ["InvoiceNo", "InvoiceNumber"])
                            inv_date = schema.get(inv, ["InvoiceDate"])
                            inv_type = schema.get(inv, ["InvoiceType"])
                            
                            for line in schema.find_lines(inv):
                                buffer.append({
                                    "logical_key": lk,
                                    "source_file": xml_path.name,
                                    "sha256": h,
                                    "schema_version": sv,
                                    "invoice_number": inv_no,
                                    "invoice_date": inv_date,
                                    "invoice_type": inv_type,
                                    "direction": direction,
                                    "line_number": schema.get_line_number(line),
                                    "product_code": schema.get_product_code(line),
                                    "product_description": schema.get_description(line),
                                    "quantity": schema.get_quantity(line),
                                    "unit_of_measure": schema.get_uom(line),
                                    "unit_price": schema.get_unit_price(line),
                                    "line_amount": schema.get_line_amount(line),
                                    "vat_percent": schema.get_vat_percent(line),
                                    "tax_code": schema.get_tax_code(line),
                                    "tax_type": schema.get_tax_type(line),
                                    "tax_amount": schema.get_tax_amount(line),
                                    "account_id": schema.get_account_id(line)
                                })
            except Exception as e:
                errors.append({
                    "source_file": xml_path.name,
                    "logical_key": lk,
                    "invoice_number": "",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })
            
            if len(buffer) >= 50000:
                flush()
                
        flush()
    logger.info("Phase 1 Complete.")


def phase_2_enrichment():
    logger.info("Starting Phase 2: Enrichment")
    meta = load_metadata()
    gl_catalog = load_gl_catalog()
    
    product_mappings = {}
    
    # metrics
    stat_invoices = set()
    stat_sales = set()
    stat_purchases = set()
    stat_lines = 0
    stat_products = set()
    stat_accounts = set()
    stat_vats = set()
    stat_taxcodes = set()
    stat_warehouses = set()

    with open(INVOICE_LINES_RAW_CSV, "r", encoding=CSV_ENCODING) as f_in, \
         open(INVOICE_LINES_CSV, "a", encoding=CSV_ENCODING, newline="") as f_out:
         
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=ENRICHED_FIELDNAMES)
        
        buffer = []
        for row in tqdm(reader, desc="Phase 2", unit="rows"):
            lk = row["logical_key"]
            m = meta.get(lk, {})
            cui = m.get("cui", "")
            comp_name = m.get("company_name", "")
            
            prod_desc = row["product_description"]
            acc_id = row["account_id"]
            vat = row["vat_percent"]
            
            norm_prod = normalize_product(prod_desc)
            
            # gl lookup
            gl_info = gl_catalog.get(cui, {}).get(acc_id, {})
            acc_desc = gl_info.get("description", "")
            acc_type = gl_info.get("type", "")
            wh_id = gl_info.get("warehouse_id", "")  # placeholder if it existed in catalog, otherwise blank
            
            val_status = "VALID"
            if not prod_desc or not acc_id or not vat:
                val_status = "INCOMPLETE"
                
            out_row = {**row} # copy raw
            out_row.update({
                "cui": cui,
                "company_name": comp_name,
                "reporting_period": m.get("reporting_period", ""),
                "normalized_product": norm_prod,
                "account_description": acc_desc,
                "account_type": acc_type,
                "warehouse_id": wh_id,
                "warehouse_exists": str(bool(wh_id)),
                "validation_status": val_status
            })
            buffer.append(out_row)
            
            # mappings
            if comp_name and prod_desc and acc_id:
                m_key = (comp_name, prod_desc, norm_prod, acc_id)
                if m_key not in product_mappings:
                    product_mappings[m_key] = {
                        "AccountDescription": acc_desc,
                        "AccountType": acc_type,
                        "Count": 0,
                        "First Seen": row["invoice_date"],
                        "Last Seen": row["invoice_date"]
                    }
                pm = product_mappings[m_key]
                pm["Count"] += 1
                inv_date = row["invoice_date"]
                if inv_date:
                    if not pm["First Seen"] or inv_date < pm["First Seen"]: pm["First Seen"] = inv_date
                    if not pm["Last Seen"] or inv_date > pm["Last Seen"]: pm["Last Seen"] = inv_date
                    
            # stats
            inv_id = (lk, row["invoice_number"])
            stat_invoices.add(inv_id)
            if row["direction"] == "SALE": stat_sales.add(inv_id)
            else: stat_purchases.add(inv_id)
            stat_lines += 1
            if norm_prod: stat_products.add(norm_prod)
            if acc_id: stat_accounts.add(acc_id)
            if vat: stat_vats.add(vat)
            if row["tax_code"]: stat_taxcodes.add(row["tax_code"])
            if wh_id: stat_warehouses.add(wh_id)
            
            if len(buffer) >= 50000:
                writer.writerows(buffer)
                buffer.clear()
                
        if buffer:
            writer.writerows(buffer)
            
    logger.info("Phase 2 Complete. Writing mappings and stats.")
    
    with open(PRODUCT_ACCOUNT_MAPPING_CSV, "a", encoding=CSV_ENCODING, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MAPPING_FIELDNAMES)
        for (c_name, p_desc, n_prod, a_id), vals in product_mappings.items():
            writer.writerow({
                "Company": c_name,
                "Product": p_desc,
                "Normalized Product": n_prod,
                "AccountID": a_id,
                "AccountDescription": vals["AccountDescription"],
                "AccountType": vals["AccountType"],
                "Count": vals["Count"],
                "First Seen": vals["First Seen"],
                "Last Seen": vals["Last Seen"]
            })

    with open(INVOICE_STATISTICS_CSV, "w", encoding=CSV_ENCODING, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerows([
            ["Sales invoices", len(stat_sales)],
            ["Purchase invoices", len(stat_purchases)],
            ["Total invoices", len(stat_invoices)],
            ["Total invoice lines", stat_lines],
            ["Unique products", len(stat_products)],
            ["Unique AccountIDs", len(stat_accounts)],
            ["Unique VAT rates", len(stat_vats)],
            ["Unique TaxCodes", len(stat_taxcodes)],
            ["Unique Warehouses", len(stat_warehouses)],
        ])

def main() -> None:
    logger.info("=" * 60)
    logger.info("Script 3 — Invoice Line Extraction — start")
    logger.info("=" * 60)

    if not NORMALIZED_DIR.exists():
        logger.error("Normalized XML directory %s does not exist.", NORMALIZED_DIR)
        return

    xml_files = sorted(NORMALIZED_DIR.rglob("*.xml"))
    if not xml_files:
        logger.warning("No normalised XML files found in %s.", NORMALIZED_DIR)
        return

    logger.info("Discovered %d normalized XML files", len(xml_files))

    _write_csv_headers()

    phase_1_raw_extraction(xml_files)
    phase_2_enrichment()

    logger.info("Script 3 — Invoice Line Extraction — done")


if __name__ == "__main__":
    main()

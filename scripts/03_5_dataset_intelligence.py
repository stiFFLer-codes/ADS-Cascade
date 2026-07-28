"""
scripts/03_5_dataset_intelligence.py
------------------------------------
Profiles the entire extracted dataset and produces quantitative intelligence
to drive architectural decisions in Phase 2.
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path
import statistics

# Add root to sys.path to import from config and utils
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config.settings import (
    INVOICE_LINES_CSV, PRODUCT_ACCOUNT_MAPPING_CSV, INTELLIGENCE_DIR,
    CSV_ENCODING
)
from utils.logger import get_logger
from utils.filesystem import ensure_dir
from utils.csv_writer import write_csv

logger = get_logger("dataset_intelligence")

def pass_1_stream(invoice_lines_csv: Path):
    """
    Streams invoice_lines_all_companies.csv once.
    Accumulates counters for Module A, Module B, and Module C.4.
    """
    # Module A: Data Quality
    a_total_rows = 0
    a_missing = Counter()
    a_incomplete = 0
    a_line_seen = Counter()  # (cui, invoice_number, line_number, account_id) -> count
    a_invoice_lines = Counter() # (cui, invoice_number) -> count of lines

    # Module B: Statistics
    b_companies = set()
    b_cui_invoices = defaultdict(set) # cui -> set of invoice_numbers
    b_cui_products = defaultdict(set)
    b_cui_accounts = defaultdict(set)
    b_vat_freq = Counter()
    b_product_freq = Counter()
    b_account_freq = Counter()
    b_direction = Counter()
    b_period = Counter()

    # Module C.4: VAT Consistency
    c4_vat_by_product = defaultdict(Counter)

    logger.info(f"Streaming {invoice_lines_csv.name}...")
    with open(invoice_lines_csv, "r", encoding=CSV_ENCODING) as f:
        reader = csv.DictReader(f)
        for row in reader:
            a_total_rows += 1
            
            cui = row.get("cui", "")
            inv_num = row.get("invoice_number", "")
            line_num = row.get("line_number", "")
            acc_id = row.get("account_id", "")
            prod_desc = row.get("product_description", "")
            norm_prod = row.get("normalized_product", "")
            vat = row.get("vat_percent", "")
            tax = row.get("tax_code", "")
            wh = row.get("warehouse_id", "")
            amt = row.get("line_amount", "")
            date = row.get("invoice_date", "")
            status = row.get("validation_status", "")
            direction = row.get("direction", "")
            period = row.get("reporting_period", "")

            # Module A
            if not prod_desc: a_missing["product_description"] += 1
            if not acc_id: a_missing["account_id"] += 1
            if not vat: a_missing["vat_percent"] += 1
            if not tax: a_missing["tax_code"] += 1
            if not wh: a_missing["warehouse_id"] += 1
            if not amt: a_missing["line_amount"] += 1
            if not date: a_missing["invoice_date"] += 1
            if status == "INCOMPLETE": a_incomplete += 1

            line_key = (cui, inv_num, line_num, acc_id)
            a_line_seen[line_key] += 1
            
            inv_key = (cui, inv_num)
            a_invoice_lines[inv_key] += 1

            # Module B
            b_companies.add(cui)
            b_cui_invoices[cui].add(inv_num)
            if norm_prod: b_cui_products[cui].add(norm_prod)
            if acc_id: b_cui_accounts[cui].add(acc_id)
            if vat: b_vat_freq[vat] += 1
            if norm_prod: b_product_freq[norm_prod] += 1
            if acc_id: b_account_freq[acc_id] += 1
            if direction: b_direction[direction] += 1
            if period: b_period[period] += 1

            # Module C.4
            if norm_prod and vat:
                c4_vat_by_product[norm_prod][vat] += 1

    logger.info(f"Processed {a_total_rows} rows from invoice lines.")

    return {
        "A": {
            "total_rows": a_total_rows,
            "missing": a_missing,
            "incomplete": a_incomplete,
            "line_seen": a_line_seen,
            "invoice_lines": a_invoice_lines,
        },
        "B": {
            "companies": b_companies,
            "cui_invoices": b_cui_invoices,
            "cui_products": b_cui_products,
            "cui_accounts": b_cui_accounts,
            "vat_freq": b_vat_freq,
            "product_freq": b_product_freq,
            "account_freq": b_account_freq,
            "direction": b_direction,
            "period": b_period,
        },
        "C4": {
            "vat_by_product": c4_vat_by_product
        }
    }


def load_mapping_data(mapping_csv: Path):
    """Loads product_account_mapping.csv entirely into memory."""
    logger.info(f"Loading {mapping_csv.name}...")
    mappings = []
    with open(mapping_csv, "r", encoding=CSV_ENCODING) as f:
        reader = csv.DictReader(f)
        for row in reader:
            mappings.append({
                "company": row.get("Company", ""),
                "normalized_product": row.get("Normalized Product", ""),
                "account_id": row.get("AccountID", ""),
                "count": int(row.get("Count", 0))
            })
    logger.info(f"Loaded {len(mappings)} product mappings.")
    return mappings


def module_a_data_quality(a_data):
    """Produces data_quality_report.csv data."""
    logger.info("Running Module A: Data Quality...")
    total = a_data["total_rows"]
    missing = a_data["missing"]
    
    fields = [
        "product_description", "account_id", "vat_percent", "tax_code",
        "warehouse_id", "line_amount", "invoice_date"
    ]
    
    rows = []
    for f in fields:
        m_count = missing[f]
        rows.append({
            "field": f,
            "total_rows": total,
            "non_empty": total - m_count,
            "empty": m_count,
            "missing_pct": round((m_count / total) * 100, 2) if total else 0,
            "notes": ""
        })
    
    rows.append({
        "field": "validation_status",
        "total_rows": total,
        "non_empty": total - a_data["incomplete"],
        "empty": a_data["incomplete"],
        "missing_pct": round((a_data["incomplete"] / total) * 100, 2) if total else 0,
        "notes": "INCOMPLETE status count"
    })

    # Duplicates
    dup_lines = sum(1 for v in a_data["line_seen"].values() if v > 1)
    
    rows.append({
        "field": "duplicate_invoice_lines",
        "total_rows": total,
        "non_empty": total - dup_lines,
        "empty": dup_lines,
        "missing_pct": round((dup_lines / total) * 100, 2) if total else 0,
        "notes": "Exact line duplicates"
    })

    write_csv(rows, INTELLIGENCE_DIR / "data_quality_report.csv", list(rows[0].keys()))
    return rows


def module_b_statistics(a_data, b_data):
    """Produces dataset_statistics.csv data."""
    logger.info("Running Module B: Statistics...")
    
    rows = []
    
    companies_count = len(b_data["companies"])
    rows.append({"category": "General", "metric": "Companies count", "value": companies_count})
    
    # Invoices per company
    inv_counts = [len(invs) for invs in b_data["cui_invoices"].values()]
    if inv_counts:
        inv_counts.sort()
        rows.append({"category": "Invoices per company", "metric": "min", "value": min(inv_counts)})
        rows.append({"category": "Invoices per company", "metric": "max", "value": max(inv_counts)})
        rows.append({"category": "Invoices per company", "metric": "avg", "value": round(statistics.mean(inv_counts), 2)})
        rows.append({"category": "Invoices per company", "metric": "median", "value": round(statistics.median(inv_counts), 2)})
    
    # Products per company
    prod_counts = [len(ps) for ps in b_data["cui_products"].values()]
    if prod_counts:
        rows.append({"category": "Products per company", "metric": "min", "value": min(prod_counts)})
        rows.append({"category": "Products per company", "metric": "max", "value": max(prod_counts)})
        rows.append({"category": "Products per company", "metric": "avg", "value": round(statistics.mean(prod_counts), 2)})

    # Accounts per company
    acc_counts = [len(ac) for ac in b_data["cui_accounts"].values()]
    if acc_counts:
        rows.append({"category": "AccountIDs per company", "metric": "min", "value": min(acc_counts)})
        rows.append({"category": "AccountIDs per company", "metric": "max", "value": max(acc_counts)})
        rows.append({"category": "AccountIDs per company", "metric": "avg", "value": round(statistics.mean(acc_counts), 2)})

    # Top VAT rates
    for v, c in b_data["vat_freq"].most_common(5):
        rows.append({"category": "VAT Rates", "metric": f"Rate {v}", "value": c})

    # Direction
    for d, c in b_data["direction"].most_common():
        rows.append({"category": "Direction", "metric": d, "value": c})

    # Top 50 products -> 10 for CSV
    for p, c in b_data["product_freq"].most_common(10):
        rows.append({"category": "Top Products", "metric": p, "value": c})

    write_csv(rows, INTELLIGENCE_DIR / "dataset_statistics.csv", ["category", "metric", "value"])
    return b_data


def module_c_behavioral(mappings, c4_data):
    """Produces C.1, C.2, C.3, C.4 csvs."""
    logger.info("Running Module C: Behavioral Analysis...")
    
    # C.1 Product Ambiguity
    prod_accs = defaultdict(list)
    for m in mappings:
        prod_accs[m["normalized_product"]].append((m["account_id"], m["count"]))

    c1_rows = []
    total_det_sum = 0
    total_count_sum = 0
    
    for prod, acc_list in prod_accs.items():
        total = sum(c for _, c in acc_list)
        if total == 0: continue
        
        acc_list.sort(key=lambda x: x[1], reverse=True)
        dominant_account = acc_list[0][0]
        dominant_count = acc_list[0][1]
        
        determinism = dominant_count / total
        
        c1_rows.append({
            "normalized_product": prod,
            "total_occurrences": total,
            "n_accounts": len(acc_list),
            "dominant_account_id": dominant_account,
            "dominant_account_desc": "",
            "dominant_pct": round(determinism * 100, 2),
            "determinism_score": round(determinism, 4),
            "ambiguity_score": round(1.0 - determinism, 4),
            "all_accounts": ";".join([f"{a}:{c}" for a, c in acc_list])
        })
        
        total_det_sum += (determinism * total)
        total_count_sum += total
        
    write_csv(c1_rows, INTELLIGENCE_DIR / "product_ambiguity.csv", list(c1_rows[0].keys()) if c1_rows else [])
    
    dataset_ads = (total_det_sum / total_count_sum) if total_count_sum else 0

    # C.2 Company Consistency
    comp_prod_accs = defaultdict(lambda: defaultdict(list))
    for m in mappings:
        comp_prod_accs[m["company"]][m["normalized_product"]].append((m["account_id"], m["count"]))

    c2_rows = []
    for comp, prods in comp_prod_accs.items():
        consistent = 0
        inconsistent = 0
        comp_det_sum = 0
        comp_total = 0
        for prod, acc_list in prods.items():
            total = sum(c for _, c in acc_list)
            if not total: continue
            dom_c = max(c for _, c in acc_list)
            det = dom_c / total
            if len(acc_list) == 1:
                consistent += 1
            else:
                inconsistent += 1
            comp_det_sum += det * total
            comp_total += total
        
        c2_rows.append({
            "company": comp,
            "total_products": len(prods),
            "consistent_products": consistent,
            "inconsistent_products": inconsistent,
            "consistency_pct": round((consistent / len(prods)) * 100, 2) if prods else 0,
            "avg_determinism": round(comp_det_sum / comp_total, 4) if comp_total else 0
        })
    write_csv(c2_rows, INTELLIGENCE_DIR / "company_consistency.csv", list(c2_rows[0].keys()) if c2_rows else [])

    # C.3 Cross-Company Consistency
    prod_comps = defaultdict(set)
    prod_global_accs = defaultdict(Counter)
    for m in mappings:
        prod = m["normalized_product"]
        prod_comps[prod].add(m["company"])
        prod_global_accs[prod][m["account_id"]] += m["count"]

    c3_rows = []
    cross_comp_det_sum = 0
    cross_comp_total = 0
    for prod, comps in prod_comps.items():
        if len(comps) < 2: continue
        
        accs = prod_global_accs[prod]
        total = sum(accs.values())
        dom_acc = accs.most_common(1)[0][0]
        dom_c = accs.most_common(1)[0][1]
        det = dom_c / total
        
        c3_rows.append({
            "normalized_product": prod,
            "n_companies": len(comps),
            "n_accounts_global": len(accs),
            "dominant_account_id": dom_acc,
            "cross_company_determinism": round(det, 4),
            "accounts_by_company": ""
        })
        cross_comp_det_sum += det * total
        cross_comp_total += total

    write_csv(c3_rows, INTELLIGENCE_DIR / "cross_company_consistency.csv", list(c3_rows[0].keys()) if c3_rows else [])
    global_cross_det = (cross_comp_det_sum / cross_comp_total) if cross_comp_total else 0

    # C.4 VAT Consistency
    c4_rows = []
    for prod, vat_counts in c4_data["vat_by_product"].items():
        total = sum(vat_counts.values())
        if total == 0: continue
        dom_vat, dom_c = vat_counts.most_common(1)[0]
        
        c4_rows.append({
            "normalized_product": prod,
            "total_lines": total,
            "n_vat_rates": len(vat_counts),
            "dominant_vat": dom_vat,
            "dominant_vat_pct": round((dom_c / total) * 100, 2),
            "vat_rates": ";".join([f"{v}:{c}" for v, c in vat_counts.items()])
        })
    write_csv(c4_rows, INTELLIGENCE_DIR / "vat_consistency.csv", list(c4_rows[0].keys()) if c4_rows else [])

    return {
        "dataset_ads": dataset_ads,
        "company_avg_det": statistics.mean([r["avg_determinism"] for r in c2_rows]) if c2_rows else 0,
        "global_cross_det": global_cross_det,
        "vat_consistency_pct": (sum(1 for r in c4_rows if r["n_vat_rates"] == 1) / len(c4_rows) * 100) if c4_rows else 0
    }


def module_d_ai_readiness(a_rows, c_metrics):
    """Produces ai_readiness.csv based on results."""
    logger.info("Running Module D: AI Readiness...")
    
    missing_dict = {r["field"]: r["missing_pct"] for r in a_rows}
    
    features = [
        {"feature": "product_description", "missing": missing_dict.get("product_description", 100), "cons_metric": "ADS", "cons_val": c_metrics["dataset_ads"]},
        {"feature": "vat_percent", "missing": missing_dict.get("vat_percent", 100), "cons_metric": "VAT Stable", "cons_val": c_metrics["vat_consistency_pct"]/100},
        {"feature": "tax_code", "missing": missing_dict.get("tax_code", 100), "cons_metric": "-", "cons_val": 0},
        {"feature": "warehouse_id", "missing": missing_dict.get("warehouse_id", 100), "cons_metric": "-", "cons_val": 0},
        {"feature": "direction", "missing": 0, "cons_metric": "-", "cons_val": 1.0},
    ]
    
    d_rows = []
    for f in features:
        miss = f["missing"]
        cons = f["cons_val"]
        
        if miss > 90:
            val = "DROP"
            rec = "Too many missing values."
        elif miss < 5 and (f["cons_metric"] == "-" or cons > 0.8):
            val = "HIGH"
            rec = "Strong feature."
        elif miss < 20 or (f["cons_metric"] != "-" and cons >= 0.5):
            val = "MEDIUM"
            rec = "Usable, but needs imputation."
        else:
            val = "LOW"
            rec = "Weak feature."
            
        d_rows.append({
            "feature": f["feature"],
            "total_rows": a_rows[0]["total_rows"],
            "non_empty": 0,
            "missing_pct": miss,
            "consistency_metric": f["cons_metric"],
            "consistency_value": round(cons, 4),
            "ai_value": val,
            "recommendation": rec
        })
    write_csv(d_rows, INTELLIGENCE_DIR / "ai_readiness.csv", list(d_rows[0].keys()))
    return d_rows


def generate_report(a_rows, b_data, c_metrics, d_rows):
    """Writes dataset_intelligence_report.md."""
    logger.info("Generating final report...")
    
    report = f"""# Dataset Intelligence Report

## Executive Summary
Dataset Accounting Determinism Score (ADS): **{c_metrics['dataset_ads']:.4f}**
Global Cross-Company Determinism: **{c_metrics['global_cross_det']:.4f}**

## Data Quality
"""
    for r in a_rows:
        report += f"- **{r['field']}**: {r['missing_pct']}% missing\n"

    report += "\n## Behavioral Analysis\n"
    report += f"- Average Company Determinism: **{c_metrics['company_avg_det']:.4f}**\n"
    report += f"- VAT Stability: **{c_metrics['vat_consistency_pct']:.2f}%** of products have a single VAT rate.\n"

    report += "\n## AI Readiness Matrix\n"
    report += "| Feature | Missing % | Value | Recommendation |\n|---|---|---|---|\n"
    for r in d_rows:
        report += f"| {r['feature']} | {r['missing_pct']}% | {r['ai_value']} | {r['recommendation']} |\n"

    report += "\n## Recommendations\n"
    if c_metrics['global_cross_det'] > 0.90:
        report += "A global retrieval model will likely succeed due to high cross-company determinism.\n"
    else:
        report += "High company-specific behavior detected. Consider company-scoped knowledge bases or specific models.\n"

    report_path = INTELLIGENCE_DIR / "dataset_intelligence_report.md"
    report_path.write_text(report, encoding="utf-8")
    logger.info(f"Report written to {report_path}")


def main():
    logger.info("Starting Script 3.5: Dataset Intelligence")
    ensure_dir(INTELLIGENCE_DIR)

    # Load mapping data
    mappings = load_mapping_data(PRODUCT_ACCOUNT_MAPPING_CSV)

    # Pass 1 stream
    pass_1_res = pass_1_stream(INVOICE_LINES_CSV)

    # Module A
    a_rows = module_a_data_quality(pass_1_res["A"])

    # Module B
    b_data = module_b_statistics(pass_1_res["A"], pass_1_res["B"])

    # Module C
    c_metrics = module_c_behavioral(mappings, pass_1_res["C4"])

    # Module D
    d_rows = module_d_ai_readiness(a_rows, c_metrics)

    # Report
    generate_report(a_rows, b_data, c_metrics, d_rows)

    logger.info("Script 3.5 finished successfully.")

if __name__ == "__main__":
    main()

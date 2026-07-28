"""
scripts/00_generate_synthetic.py
---------------------------------
Generates statistically-equivalent synthetic Phase 1 outputs for the public
`research` branch. Targets the aggregate distributions documented in
data_verification_audit.md (91.2% product determinism, 0.695 cross-company
consistency, 94.5% VAT stability, 73.9/26.1 purchase/sale split) without
reading or containing any real company name, CUI, or product string --
every value here is generated from scratch.

Output is a smaller synthetic run (not a 296K-line clone): the point is that
the unmodified downstream scripts (03_5, 04, phase2/p2_01, p2_02) reproduce
the same *shape* of results on it, which is the actual research claim.

Usage: python scripts/00_generate_synthetic.py
Writes: data/outputs/invoice_lines_all_companies.csv
        data/outputs/product_account_mapping.csv
        data/outputs/invoice_statistics.csv
        data/outputs/gl_statistics.csv
"""
import csv
import hashlib
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "outputs"

random.seed(42)  # reproducible synthetic run

N_COMPANIES = 60
N_PRODUCTS = 1200               # kept low relative to line volume so each product gets enough
                                 # evidence for its determinism score to be a stable estimate
                                 # (a handful of occurrences is too noisy to reflect the
                                 # underlying per-product probability)

# Targets from data_verification_audit.md's "Authoritative Value" column
DETERMINISTIC_SHARE = 0.95      # products with dominant-account share > 0.95 (set above the
                                 # 91.2% real target: small per-product sample sizes in this
                                 # scaled-down run add noise that pulls the realized rate down)
CROSS_COMPANY_ALIGN = 0.695     # P(companies sharing a product agree on its dominant account)
VAT_STABILITY = 0.945           # P(a line uses its product's dominant VAT rate)
VAT_MISSING = 0.0405            # P(vat_percent blank on a line)
PURCHASE_SHARE = 0.739          # direction split

VAT_RATES = ["0.00", "5.00", "9.00", "11.00", "19.00", "21.00"]

# Standard Romanian chart-of-accounts codes (public accounting standard, not
# client-specific) split by the direction they'd realistically appear under.
PURCHASE_ACCOUNTS = [
    ("371", "MARFURI", "Activ"), ("401", "FURNIZORI", "Pasiv"),
    ("4426", "TVA DEDUCTIBILA", "Activ"), ("601", "CHELT. CU MATERIILE PRIME", "Cheltuieli"),
    ("602", "CHELT. CU MATERIALELE CONSUMABILE", "Cheltuieli"),
    ("605", "CHELT. CU ENERGIA SI APA", "Cheltuieli"), ("607", "CHELT. PRIVIND MARFURILE", "Cheltuieli"),
    ("608", "CHELT. PRIVIND AMBALAJELE", "Cheltuieli"), ("609", "REDUCERI COMERCIALE PRIMITE", "Cheltuieli"),
    ("612", "CHELT. CU REDEVENTELE, LOCATIILE DE GESTIUNE", "Cheltuieli"),
    ("613", "CHELT. CU PRIMELE DE ASIGURARE", "Cheltuieli"),
    ("622", "CHELT. CU COMISIOANELE SI ONORARIILE", "Cheltuieli"),
    ("625", "CHELT. CU DEPLASARI, DETASARI", "Cheltuieli"),
    ("628", "ALTE CHELT. CU SERVICIILE EXECUTATE DE TERTI", "Cheltuieli"),
    ("6022", "CHELT. PRIVIND COMBUSTIBILUL", "Cheltuieli"),
    ("635", "CHELT. CU ALTE IMPOZITE, TAXE", "Cheltuieli"),
]
SALE_ACCOUNTS = [
    ("411", "CLIENTI", "Activ"), ("4427", "TVA COLECTATA", "Pasiv"),
    ("701", "VEN. DIN VANZAREA PROD. FINITE", "Pasiv"),
    ("704", "VEN. DIN SERVICII PRESTATE", "Pasiv"),
    ("707", "VEN. DIN VANZAREA MARFURILOR", "Pasiv"),
]
CATEGORIES = ["FUEL", "OFFICE", "RAW MATERIAL", "SERVICE", "RETAIL",
              "TRANSPORT", "UTILITY", "MAINTENANCE", "PACKAGING", "MISC"]

ACCT_DESC = {a: (d, t) for a, d, t in PURCHASE_ACCOUNTS + SALE_ACCOUNTS}


def gen_companies():
    return [{"cui": f"9{900000 + i}", "name": f"SYNTH COMPANY {i:03d} SRL"} for i in range(1, N_COMPANIES + 1)]


def gen_products():
    """Each product gets a fixed direction, an account pool for that direction, a
    'true' dominant account, and a target dominant-share (the per-product ADS)."""
    products = []
    for i in range(1, N_PRODUCTS + 1):
        direction = "PURCHASE" if random.random() < PURCHASE_SHARE else "SALE"
        pool = PURCHASE_ACCOUNTS if direction == "PURCHASE" else SALE_ACCOUNTS
        deterministic = random.random() < DETERMINISTIC_SHARE
        # at ~9 occurrences/product, even one deviation drops the *observed* determinism
        # below the 0.95 cutoff -- push the floor high enough that P(zero misses) is high
        dominant_frac = random.uniform(0.99, 1.0) if deterministic else random.uniform(0.55, 0.94)
        n_accts = 1 if (deterministic and random.random() < 0.7) else random.randint(2, 3)
        accounts = random.sample(pool, k=min(n_accts, len(pool)))
        cat = random.choice(CATEGORIES)
        name = f"SYNTH {cat} {i:05d}"
        products.append({
            "idx": i, "name": name, "normalized": name.lower(), "direction": direction,
            "accounts": [a for a, _, _ in accounts], "dominant_frac": dominant_frac,
            "vat_rate": random.choice(VAT_RATES), "weight": random.lognormvariate(0, 1.1),
        })
    return products


def assign_companies(products, companies):
    """~88% of products belong to one company; ~12% are shared by 2-10 companies.
    Sharing companies agree on the same 'true' dominant account with probability
    CROSS_COMPANY_ALIGN -- this is what 03_5 later measures back out as
    cross_company_determinism."""
    for p in products:
        if random.random() < 0.12 and N_COMPANIES >= 2:
            k = min(N_COMPANIES, random.choice([2, 2, 3, 3, 4, 5, 6, 8, 10]))
            comps = random.sample(companies, k)
        else:
            comps = [random.choice(companies)]
        p["companies"] = comps
        base = p["accounts"][0]
        full_pool = PURCHASE_ACCOUNTS if p["direction"] == "PURCHASE" else SALE_ACCOUNTS
        full_ids = [a for a, _, _ in full_pool]
        p["dominant_by_cui"] = {}
        for c in comps:
            agree = len(comps) == 1 or random.random() < CROSS_COMPANY_ALIGN
            if agree:
                acct = base
            else:
                # genuinely different account (not just another pick from the same
                # small product-level pool, or "disagreement" mostly re-lands on
                # base by chance and cross-company consistency never actually drops)
                acct = random.choice([a for a in full_ids if a != base] or [base])
                if acct not in p["accounts"]:
                    p["accounts"].append(acct)
            p["dominant_by_cui"][c["cui"]] = acct
    return products


def pick_account(product, cui):
    dominant = product["dominant_by_cui"][cui]
    if random.random() < product["dominant_frac"] or len(product["accounts"]) == 1:
        return dominant
    others = [a for a in product["accounts"] if a != dominant] or [dominant]
    return random.choice(others)


def pick_vat(product):
    if random.random() < VAT_MISSING:
        return ""
    if random.random() < VAT_STABILITY:
        return product["vat_rate"]
    return random.choice([r for r in VAT_RATES if r != product["vat_rate"]] or VAT_RATES)


def gen_dataset():
    companies = gen_companies()
    products = assign_companies(gen_products(), companies)
    by_company = defaultdict(list)
    for p in products:
        for c in p["companies"]:
            by_company[c["cui"]].append(p)

    start = date(2024, 6, 1)
    lines = []
    for c in companies:
        pool = by_company[c["cui"]]
        if not pool:
            continue
        by_dir = {
            "PURCHASE": [p for p in pool if p["direction"] == "PURCHASE"],
            "SALE": [p for p in pool if p["direction"] == "SALE"],
        }
        n_invoices = max(1, int(random.lognormvariate(3.3, 1.1)))
        for inv_i in range(n_invoices):
            # pick a direction this company actually has products for
            available = [d for d in ("PURCHASE", "SALE") if by_dir[d]]
            if not available:
                continue
            direction = "PURCHASE" if ("PURCHASE" in available and
                                        (random.random() < PURCHASE_SHARE or "SALE" not in available)) else "SALE"
            dir_pool = by_dir[direction]
            weights = [p["weight"] for p in dir_pool]
            inv_date = start + timedelta(days=random.randint(0, 760))
            period_end = date(inv_date.year + (inv_date.month == 12), inv_date.month % 12 + 1, 1) - timedelta(days=1)
            reporting_period = period_end.strftime("%d-%m-%Y")
            invoice_number = f"SYN{c['cui']}-{inv_i:06d}"
            logical_key = f"{c['cui']}_{reporting_period}"
            source_file = f"SYNTH_{c['cui']}_{reporting_period}_Inf.xml"
            sha = hashlib.sha256(f"{c['cui']}{invoice_number}".encode()).hexdigest()
            n_lines = random.choices([1, 2, 3, 4, 5, 6, 7, 8],
                                      weights=[30, 25, 15, 10, 8, 6, 4, 2])[0]
            picks = random.choices(dir_pool, weights=weights, k=n_lines)
            for ln, prod in enumerate(picks, start=1):
                account = pick_account(prod, c["cui"])
                vat = pick_vat(prod)
                desc, acct_type = ACCT_DESC[account]
                vat_int = int(float(vat)) if vat else 0
                tax_code = f"3{vat_int:02d}{prod['idx'] % 1000:03d}"
                lines.append({
                    "logical_key": logical_key, "cui": c["cui"], "company_name": c["name"],
                    "reporting_period": reporting_period, "source_file": source_file,
                    "sha256": sha, "schema_version": "2.0", "invoice_number": invoice_number,
                    "invoice_date": inv_date.isoformat(), "invoice_type": "380",
                    "direction": direction, "line_number": ln,
                    "product_code": f"{prod['idx']:08d}", "product_description": prod["name"],
                    "normalized_product": prod["normalized"],
                    "quantity": f"{random.uniform(1, 500):.3f}",
                    "unit_of_measure": random.choice(["BUC", "KG", "L", "", ""]),
                    "unit_price": f"{random.uniform(1, 500):.2f}",
                    "line_amount": "", "vat_percent": vat, "tax_code": tax_code,
                    "tax_type": "300", "tax_amount": "", "account_id": account,
                    "account_description": desc, "account_type": acct_type,
                    "warehouse_id": "", "warehouse_exists": "False", "validation_status": "VALID",
                })
    return companies, lines


LINES_HEADER = [
    "logical_key", "cui", "company_name", "reporting_period", "source_file", "sha256",
    "schema_version", "invoice_number", "invoice_date", "invoice_type", "direction",
    "line_number", "product_code", "product_description", "normalized_product",
    "quantity", "unit_of_measure", "unit_price", "line_amount", "vat_percent",
    "tax_code", "tax_type", "tax_amount", "account_id", "account_description",
    "account_type", "warehouse_id", "warehouse_exists", "validation_status",
]


def write_invoice_lines(lines):
    path = OUT / "invoice_lines_all_companies.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LINES_HEADER)
        w.writeheader()
        w.writerows(lines)
    return path


def write_product_account_mapping(lines):
    agg = defaultdict(lambda: {"count": 0, "first": None, "last": None,
                                "desc": "", "type": ""})
    for r in lines:
        key = (r["company_name"], r["product_description"], r["normalized_product"], r["account_id"])
        a = agg[key]
        a["count"] += 1
        d = r["invoice_date"]
        a["first"] = d if a["first"] is None else min(a["first"], d)
        a["last"] = d if a["last"] is None else max(a["last"], d)
        a["desc"] = r["account_description"]
        a["type"] = r["account_type"]

    path = OUT / "product_account_mapping.csv"
    header = ["Company", "Product", "Normalized Product", "AccountID", "AccountDescription",
              "AccountType", "Count", "First Seen", "Last Seen"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for (company, product, norm, account), a in agg.items():
            w.writerow([company, product, norm, account, a["desc"], a["type"],
                        a["count"], a["first"], a["last"]])
    return path


def write_headline_stats(companies, lines):
    sales = sum(1 for r in lines if r["direction"] == "SALE")
    purchases = len(lines) - sales
    n_invoices = len({(r["cui"], r["invoice_number"]) for r in lines})
    n_sale_inv = len({(r["cui"], r["invoice_number"]) for r in lines if r["direction"] == "SALE"})
    n_purchase_inv = n_invoices - n_sale_inv

    with open(OUT / "invoice_statistics.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Value"])
        w.writerow(["Sales invoices", n_sale_inv])
        w.writerow(["Purchase invoices", n_purchase_inv])
        w.writerow(["Total invoices", n_invoices])
        w.writerow(["Total invoice lines", len(lines)])

    n_accounts = len({r["account_id"] for r in lines})
    with open(OUT / "gl_statistics.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["Total Companies", len(companies)])
        w.writerow(["Total XML Parsed", "N/A (synthetic run, no source XMLs)"])
        w.writerow(["Total GL Accounts", len(lines)])
        w.writerow(["Unique AccountIDs", n_accounts])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    companies, lines = gen_dataset()
    lp = write_invoice_lines(lines)
    mp = write_product_account_mapping(lines)
    write_headline_stats(companies, lines)
    print(f"Synthetic dataset: {len(companies)} companies, {len(lines):,} invoice lines")
    print(f"  -> {lp}")
    print(f"  -> {mp}")
    print(f"  -> {OUT / 'invoice_statistics.csv'}")
    print(f"  -> {OUT / 'gl_statistics.csv'}")


if __name__ == "__main__":
    main()

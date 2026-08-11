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

Experiment 1 (research/EXPERIMENT_1_REDESIGN_REVIEW.md) reuses gen_dataset()
directly, in-memory, with a swept seed/deterministic_share/lexical_variation
-- it does not go through main()/the file-writing functions below, so it
never touches these committed output paths.
"""
import csv
import hashlib
import random
import zlib
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "outputs"

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


def gen_products(rng, deterministic_share):
    """Each product gets a fixed direction, an account pool for that direction, a
    'true' dominant account, and a target dominant-share (the per-product ADS)."""
    products = []
    for i in range(1, N_PRODUCTS + 1):
        direction = "PURCHASE" if rng.random() < PURCHASE_SHARE else "SALE"
        pool = PURCHASE_ACCOUNTS if direction == "PURCHASE" else SALE_ACCOUNTS
        deterministic = rng.random() < deterministic_share
        # at ~9 occurrences/product, even one deviation drops the *observed* determinism
        # below the 0.95 cutoff -- push the floor high enough that P(zero misses) is high
        dominant_frac = rng.uniform(0.99, 1.0) if deterministic else rng.uniform(0.55, 0.94)
        n_accts = 1 if (deterministic and rng.random() < 0.7) else rng.randint(2, 3)
        accounts = rng.sample(pool, k=min(n_accts, len(pool)))
        cat = rng.choice(CATEGORIES)
        name = f"SYNTH {cat} {i:05d}"
        products.append({
            "idx": i, "name": name, "normalized": name.lower(), "direction": direction,
            "accounts": [a for a, _, _ in accounts], "dominant_frac": dominant_frac,
            "vat_rate": rng.choice(VAT_RATES), "weight": rng.lognormvariate(0, 1.1),
        })
    return products


def assign_companies(products, companies, rng, cross_company_align):
    """~88% of products belong to one company; ~12% are shared by 2-10 companies.
    Sharing companies agree on the same 'true' dominant account with probability
    cross_company_align -- this is what 03_5 later measures back out as
    cross_company_determinism."""
    for p in products:
        if rng.random() < 0.12 and N_COMPANIES >= 2:
            k = min(N_COMPANIES, rng.choice([2, 2, 3, 3, 4, 5, 6, 8, 10]))
            comps = rng.sample(companies, k)
        else:
            comps = [rng.choice(companies)]
        p["companies"] = comps
        base = p["accounts"][0]
        full_pool = PURCHASE_ACCOUNTS if p["direction"] == "PURCHASE" else SALE_ACCOUNTS
        full_ids = [a for a, _, _ in full_pool]
        p["dominant_by_cui"] = {}
        for c in comps:
            agree = len(comps) == 1 or rng.random() < cross_company_align
            if agree:
                acct = base
            else:
                # genuinely different account (not just another pick from the same
                # small product-level pool, or "disagreement" mostly re-lands on
                # base by chance and cross-company consistency never actually drops)
                acct = rng.choice([a for a in full_ids if a != base] or [base])
                if acct not in p["accounts"]:
                    p["accounts"].append(acct)
            p["dominant_by_cui"][c["cui"]] = acct
    return products


def pick_account(product, cui, rng):
    dominant = product["dominant_by_cui"][cui]
    if rng.random() < product["dominant_frac"] or len(product["accounts"]) == 1:
        return dominant
    others = [a for a in product["accounts"] if a != dominant] or [dominant]
    return rng.choice(others)


def pick_vat(product, rng):
    if rng.random() < VAT_MISSING:
        return ""
    if rng.random() < VAT_STABILITY:
        return product["vat_rate"]
    return rng.choice([r for r in VAT_RATES if r != product["vat_rate"]] or VAT_RATES)


# ---------------------------------------------------------------------------
# Lexical variation (Experiment 1, research/EXPERIMENT_1_REDESIGN_REVIEW.md §8).
# Off by default (lexical_variation=False draws zero extra randomness and
# leaves every line's surface string exactly as before -- required for the
# default-output regression test in scripts/test_00_generate_synthetic.py).
# ---------------------------------------------------------------------------

TRANSFORM_TYPES = ("case", "punct", "reorder", "abbrev", "whitespace")


def _line_rng(seed, logical_key, line_number):
    """Stable, reproducible per-line sub-seed -- same crc32-hash convention as
    scripts/phase2/p2lib/data.py::split_of(), so a given (seed, logical_key,
    line_number) always yields the same transform decision, independent of
    generation order or of any other line's draws."""
    key = f"{seed}|{logical_key}|{line_number}".encode()
    return random.Random(zlib.crc32(key))


def _apply_token_transform(name, tokens, rng):
    if name == "case":
        return [t.upper() if rng.random() < 0.5 else t.lower() for t in tokens]
    if name == "punct" and len(tokens) >= 2:
        tokens = tokens[:]
        i = rng.randrange(len(tokens) - 1)
        tokens[i] = tokens[i] + rng.choice(["-", "."])
        return tokens
    if name == "reorder" and len(tokens) >= 2:
        tokens = tokens[:]
        tokens[0], tokens[1] = tokens[1], tokens[0]
        return tokens
    if name == "abbrev" and len(tokens) >= 2:
        tokens = tokens[:]
        tokens[1] = tokens[1][:3] + "."
        return tokens
    return tokens


def _apply_whitespace(joined, rng):
    positions = [i for i, ch in enumerate(joined) if ch == " "]
    if not positions:
        return joined
    i = rng.choice(positions)
    sep = rng.choice(["  ", "\t"])
    return joined[:i] + sep + joined[i + 1:]


def lexical_variant(name, seed, logical_key, line_number, p_transform):
    """Semantic-preserving surface-form variant of a product name string, for
    Experiment 1's retrieval-stress condition. Deterministic given
    (seed, logical_key, line_number). Never touches the ground-truth key
    (product_code / product idx) -- callers must keep grading on that, not on
    this string. Returns (surface_string, was_transformed, transform_types_applied)."""
    rng = _line_rng(seed, logical_key, line_number)
    if rng.random() >= p_transform:
        return name, False, []
    tokens = name.split(" ")
    n = rng.choice([1, 2])
    chosen = rng.sample(list(TRANSFORM_TYPES), k=min(n, len(TRANSFORM_TYPES)))
    for t in chosen:
        if t == "whitespace":
            continue  # applied after join, below
        tokens = _apply_token_transform(t, tokens, rng)
    joined = " ".join(tokens)
    if "whitespace" in chosen:
        joined = _apply_whitespace(joined, rng)
    return joined, True, chosen


def gen_dataset(seed=42, deterministic_share=DETERMINISTIC_SHARE,
                cross_company_align=CROSS_COMPANY_ALIGN,
                lexical_variation=False, p_transform=0.5):
    """Generate (companies, lines) in memory. `seed` drives an isolated
    random.Random instance -- no global random state is mutated, so calls
    with different seeds (in any order) are independent and reproducible.

    lexical_variation/p_transform are Experiment 1 additions (default off);
    with lexical_variation=False this reproduces the original, single-seed
    generator's output exactly (same call order, same rng draws -- see
    scripts/test_00_generate_synthetic.py)."""
    rng = random.Random(seed)
    companies = gen_companies()
    products = assign_companies(gen_products(rng, deterministic_share), companies,
                                 rng, cross_company_align)
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
        n_invoices = max(1, int(rng.lognormvariate(3.3, 1.1)))
        for inv_i in range(n_invoices):
            # pick a direction this company actually has products for
            available = [d for d in ("PURCHASE", "SALE") if by_dir[d]]
            if not available:
                continue
            direction = "PURCHASE" if ("PURCHASE" in available and
                                        (rng.random() < PURCHASE_SHARE or "SALE" not in available)) else "SALE"
            dir_pool = by_dir[direction]
            weights = [p["weight"] for p in dir_pool]
            inv_date = start + timedelta(days=rng.randint(0, 760))
            period_end = date(inv_date.year + (inv_date.month == 12), inv_date.month % 12 + 1, 1) - timedelta(days=1)
            reporting_period = period_end.strftime("%d-%m-%Y")
            invoice_number = f"SYN{c['cui']}-{inv_i:06d}"
            logical_key = f"{c['cui']}_{reporting_period}"
            source_file = f"SYNTH_{c['cui']}_{reporting_period}_Inf.xml"
            sha = hashlib.sha256(f"{c['cui']}{invoice_number}".encode()).hexdigest()
            n_lines = rng.choices([1, 2, 3, 4, 5, 6, 7, 8],
                                   weights=[30, 25, 15, 10, 8, 6, 4, 2])[0]
            picks = rng.choices(dir_pool, weights=weights, k=n_lines)
            for ln, prod in enumerate(picks, start=1):
                account = pick_account(prod, c["cui"], rng)
                vat = pick_vat(prod, rng)
                desc, acct_type = ACCT_DESC[account]
                vat_int = int(float(vat)) if vat else 0
                tax_code = f"3{vat_int:02d}{prod['idx'] % 1000:03d}"

                if lexical_variation:
                    # Transform is applied to the already-lowercased base (prod["normalized"]),
                    # not the raw uppercase prod["name"] -- normalized_product is the field
                    # every mechanism actually matches on (kb.py/retrieval.py key on it), and
                    # it is unconditionally lowercased in the CLEAN path below. Transforming
                    # the uppercase name and then force-lowercasing the result would silently
                    # erase the "case" transform type's entire effect on the matching key
                    # (confirmed empirically while calibrating P_TRANSFORM -- see
                    # research/EXPERIMENT_1_REDESIGN_REVIEW.md's pilot report for the diagnostic
                    # that caught this). Transforming from a lowercase baseline means "case"
                    # introduces genuine, moderate case noise into the matching key instead.
                    surface, was_transformed, transform_types = lexical_variant(
                        prod["normalized"], seed, logical_key, ln, p_transform)
                    normalized_product = surface
                else:
                    surface, was_transformed, transform_types = prod["name"], False, []
                    normalized_product = surface.lower()

                row = {
                    "logical_key": logical_key, "cui": c["cui"], "company_name": c["name"],
                    "reporting_period": reporting_period, "source_file": source_file,
                    "sha256": sha, "schema_version": "2.0", "invoice_number": invoice_number,
                    "invoice_date": inv_date.isoformat(), "invoice_type": "380",
                    "direction": direction, "line_number": ln,
                    "product_code": f"{prod['idx']:08d}", "product_description": surface,
                    "normalized_product": normalized_product,
                    "quantity": f"{rng.uniform(1, 500):.3f}",
                    "unit_of_measure": rng.choice(["BUC", "KG", "L", "", ""]),
                    "unit_price": f"{rng.uniform(1, 500):.2f}",
                    "line_amount": "", "vat_percent": vat, "tax_code": tax_code,
                    "tax_type": "300", "tax_amount": "", "account_id": account,
                    "account_description": desc, "account_type": acct_type,
                    "warehouse_id": "", "warehouse_exists": "False", "validation_status": "VALID",
                }
                if lexical_variation:
                    # diagnostic-only fields (research/EXPERIMENT_1_REDESIGN_REVIEW.md §8/§17);
                    # never present when lexical_variation=False, so the default schema/output
                    # is untouched. lexical_original is the SAME lowercase baseline the
                    # transform was applied to, so severity diagnostics compare like-for-like.
                    row["lexical_original"] = prod["normalized"]
                    row["lexical_transformed"] = was_transformed
                    row["lexical_transform_types"] = transform_types
                lines.append(row)
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
        # extrasaction="ignore": lexical_variation=True rows carry extra diagnostic-only
        # keys (lexical_original/lexical_transformed/lexical_transform_types) that don't
        # belong in the committed schema; harmless no-op when those keys aren't present.
        w = csv.DictWriter(f, fieldnames=LINES_HEADER, extrasaction="ignore")
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


def main(seed=42, deterministic_share=DETERMINISTIC_SHARE, lexical_variation=False, p_transform=0.5):
    OUT.mkdir(parents=True, exist_ok=True)
    companies, lines = gen_dataset(seed=seed, deterministic_share=deterministic_share,
                                    lexical_variation=lexical_variation, p_transform=p_transform)
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

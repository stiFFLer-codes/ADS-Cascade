"""Knowledge base: per-company product rules + global patterns, built by streaming
evidence rows. Mirrors architecture/07 (company_account_rule, global_pattern) and the
Phase 1 ADS definition (rule ADS = dominant account's share of weighted evidence)."""
from collections import Counter, defaultdict


class Rule:
    __slots__ = ("by_dir", "tax", "vat", "name")

    def __init__(self):
        self.by_dir = defaultdict(Counter)   # direction -> Counter(account_id)
        self.tax = defaultdict(Counter)      # account_id -> Counter(tax_code)
        self.vat = defaultdict(Counter)      # account_id -> Counter(vat_percent)
        self.name = ""


class GlobalPat:
    __slots__ = ("by_dir", "companies", "vat")

    def __init__(self):
        self.by_dir = defaultdict(Counter)
        self.companies = set()
        self.vat = Counter()


def _best(counter):
    """(account, ads, evidence, top3) for a Counter of accounts; None if empty."""
    if not counter:
        return None
    acct, ct = counter.most_common(1)[0]
    total = sum(counter.values())
    return acct, ct / total, total, counter.most_common(3)


def _dir_counter(by_dir, direction):
    """Counter for a direction, falling back to all-directions aggregate."""
    c = by_dir.get(direction)
    if c:
        return c
    agg = Counter()
    for cc in by_dir.values():
        agg.update(cc)
    return agg


class KB:
    def __init__(self):
        self.rules = {}                            # (cui, product) -> Rule
        self.glob = {}                             # product -> GlobalPat
        self.company_products = defaultdict(list)  # cui -> [product]  (for fuzzy retrieval)
        self.company_name = {}
        self.acct_desc = {}                        # (cui, account) -> description

    def add(self, cui, name, product, direction, account, tax_code, vat, acct_desc=""):
        r = self.rules.get((cui, product))
        if r is None:
            r = Rule()
            r.name = name
            self.rules[(cui, product)] = r
            self.company_products[cui].append(product)
        r.by_dir[direction][account] += 1
        if tax_code:
            r.tax[account][tax_code] += 1
        if vat:
            r.vat[account][vat] += 1

        g = self.glob.get(product)
        if g is None:
            g = GlobalPat()
            self.glob[product] = g
        g.by_dir[direction][account] += 1
        g.companies.add(cui)
        if vat:
            g.vat[vat] += 1

        self.company_name[cui] = name
        if acct_desc:
            self.acct_desc[(cui, account)] = acct_desc

    # --- lookups used by the cascade ---
    def company_lookup(self, cui, product, direction):
        r = self.rules.get((cui, product))
        if not r:
            return None
        b = _best(_dir_counter(r.by_dir, direction))
        if not b:
            return None
        acct, ads, ev, top3 = b
        return {
            "account": acct, "ads": ads, "evidence": ev, "candidates": top3,
            "tax_code": r.tax[acct].most_common(1)[0][0] if r.tax[acct] else "",
            "vat": r.vat[acct].most_common(1)[0][0] if r.vat[acct] else "",
        }

    def global_lookup(self, product, direction, strict=False):
        # strict=True: only use evidence in this exact direction (a receipt PURCHASE must
        # not inherit a seller's SALE revenue account for the same product name).
        g = self.glob.get(product)
        if not g:
            return None
        if strict and direction not in g.by_dir:
            return None
        counter = g.by_dir[direction] if strict else _dir_counter(g.by_dir, direction)
        b = _best(counter)
        if not b:
            return None
        acct, gads, ev, top3 = b
        return {
            "account": acct, "global_ads": gads, "companies": len(g.companies),
            "candidates": top3,
            "vat": g.vat.most_common(1)[0][0] if g.vat else "",
        }


def build_from_rows(rows, keep=None):
    """Build a KB from an iterable of invoice-line dicts. `keep(row)->bool` filters
    (used to build from the train split only)."""
    kb = KB()
    for row in rows:
        if keep and not keep(row):
            continue
        kb.add(
            cui=row["cui"], name=row["company_name"],
            product=row["normalized_product"], direction=row["direction"],
            account=row["account_id"], tax_code=row["tax_code"],
            vat=row["vat_percent"].strip(), acct_desc=row["account_description"],
        )
    return kb

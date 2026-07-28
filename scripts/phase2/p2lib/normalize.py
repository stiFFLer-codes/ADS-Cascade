"""Product text normalization — identical to Phase 1 (scripts/03 normalize_product) so
receipt product text keys into the KB the same way invoice lines did."""
import re


def normalize_product(product: str) -> str:
    if not product:
        return ""
    p = product.lower()
    p = re.sub(r"\s+", " ", p)
    return p.strip()

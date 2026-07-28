"""P2 fuzzy fallback: company-scoped lexical similarity.

Scoped to the company's own product list first (small, and cross-company consistency is
only 0.695 so borrowing another company's account is unsafe). rapidfuzz is C-fast; global
embedding retrieval is the documented upgrade behind this same interface.
# ponytail: lexical baseline; swap to embeddings only if the tail accuracy demands it.
"""
from rapidfuzz import fuzz, process


def fuzzy_company(kb, cui, product, limit=3, cutoff=70):
    """Return [(matched_product, score, idx), ...] from the company's catalog, score 0..100."""
    pool = kb.company_products.get(cui)
    if not pool:
        return []
    return process.extract(product, pool, scorer=fuzz.WRatio, limit=limit, score_cutoff=cutoff)


def fuzzy_global(product, pool, limit=3, cutoff=70):
    """Nearest known products across the whole catalog (cold-start display: what a human/LLM
    would consider). `pool` is a pre-built list(kb.glob.keys()) so we don't rebuild it per call."""
    return process.extract(product, pool, scorer=fuzz.WRatio, limit=limit, score_cutoff=cutoff)

"""RULES_FIRST classification cascade (architecture/08 §2 order, §4 decision table).

P1 company rule -> P1b global rule -> P2 company-scoped fuzzy -> tiering. VAT is a
secondary signal (P3): the line's own VAT fills a gap but never overrides an account.
GL sanity screen (P4) and LLM inference (P5) are out of scope for Stage A (no accounts are
invented here — every candidate comes from real historical evidence).
"""
from . import confidence as C
from .retrieval import fuzzy_company, fuzzy_global


def _res(account, tax, vat, tier, method, conf, ev, cands):
    return {
        "account_id": account, "tax_code": tax, "vat_percent": vat,
        "tier": tier, "method": method, "confidence": round(float(conf), 4),
        "evidence_count": ev, "candidates": cands,
    }


def classify(kb, cui, product, direction, vat_hint="", global_strict=False, global_pool=None):
    """Predict (account_id, tax_code, vat, tier, method, confidence) for one line.
    global_strict=True forbids cross-direction global evidence (used for receipts).
    global_pool (list of KB product keys) enables the cold-start fuzzy bridge that repairs
    OCR-formatting gaps ('rovinieta a autoturisme' -> 'rovinieta') as REVIEW candidates."""
    cr = kb.company_lookup(cui, product, direction)

    # P1 — company deterministic
    if cr:
        ads, ev = cr["ads"], cr["evidence"]
        vat = cr["vat"] or vat_hint
        if ads >= C.T1_ADS and ev >= C.T1_MIN_EVIDENCE:
            return _res(cr["account"], cr["tax_code"], vat, 1, "COMPANY_RULE", ads, ev, cr["candidates"])
        if ads >= C.T2_ADS_LOW and ev >= C.T2_MIN_EVIDENCE:
            return _res(cr["account"], cr["tax_code"], vat, 2, "COMPANY_RULE_MID", ads, ev, cr["candidates"])
        # weak/ambiguous company rule -> review (08 row 7)
        return _res(cr["account"], cr["tax_code"], vat, 3, "COMPANY_RULE_WEAK", ads, ev, cr["candidates"])

    # P1b — global deterministic (only when no company precedent)
    gr = kb.global_lookup(product, direction, strict=global_strict)
    if gr:
        gads, nco = gr["global_ads"], gr["companies"]
        vat = gr["vat"] or vat_hint
        if gads >= C.T1_GLOBAL_ADS and nco >= C.GLOBAL_MIN_COMPANIES:
            return _res(gr["account"], "", vat, 1, "GLOBAL_RULE", gads, nco, gr["candidates"])
        if gads >= C.T2_GLOBAL_ADS_LOW and nco >= C.GLOBAL_MIN_COMPANIES:
            return _res(gr["account"], "", vat, 2, "GLOBAL_RULE_MID", gads, nco, gr["candidates"])

    # P2 — company-scoped fuzzy fallback
    matches = fuzzy_company(kb, cui, product)
    if matches:
        best_prod, score, _ = matches[0]
        mr = kb.company_lookup(cui, best_prod, direction)
        if mr:
            vat = mr["vat"] or vat_hint
            # Fuzzy measured ~49% even with top-3 agreement -> unsafe to auto-apply.
            # It attaches a candidate for the reviewer; a human confirmation later promotes
            # the alias (making it a deterministic T1 hit forever after).
            if C.FUZZY_AUTO_APPLY:
                accts = {kb.company_lookup(cui, mp, direction)["account"]
                         for mp, sc, _ in matches
                         if kb.company_lookup(cui, mp, direction)}
                if (score >= C.T2_SIM and mr["ads"] >= C.T1_ADS
                        and mr["evidence"] >= C.T1_MIN_EVIDENCE and len(accts) == 1):
                    return _res(mr["account"], mr["tax_code"], vat, 2, "FUZZY", score / 100,
                                mr["evidence"], mr["candidates"])
            return _res(mr["account"], mr["tax_code"], vat, 3, "FUZZY_REVIEW", score / 100,
                        mr["evidence"], mr["candidates"])

    # global weak (exact key) -> review
    if gr:
        return _res(gr["account"], "", gr["vat"] or vat_hint, 3, "GLOBAL_WEAK",
                    gr["global_ads"], gr["companies"], gr["candidates"])

    # cold-start fuzzy bridge: exact key missed, but the same product exists under a slightly
    # different OCR/spelling form. High cutoff, review only (never auto — cross-company is 0.695).
    if global_pool is not None:
        gm = fuzzy_global(product, global_pool, limit=3, cutoff=C.GLOBAL_FUZZY_CUTOFF)
        if gm:
            best_prod, score, _ = gm[0]
            mg = kb.global_lookup(best_prod, direction, strict=global_strict)
            if mg:
                return _res(mg["account"], "", mg["vat"] or vat_hint, 3, "GLOBAL_FUZZY_REVIEW",
                            score / 100, mg["companies"], mg["candidates"])

    # Tier 4 — no precedent anywhere
    return _res("", "", vat_hint, 4, "NO_PRECEDENT", 0.0, 0, [])

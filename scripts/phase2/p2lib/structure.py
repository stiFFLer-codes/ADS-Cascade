"""Stage B3 structuring: cached AWS Textract AnalyzeExpense JSON -> canonical receipt dict
(a flat projection of architecture/07 document + document_line).

Handles the messiness we saw in real output: the VAT bracket letter lives only in each
line's EXPENSE_ROW; TOTAL is ambiguous (real total vs "TOTAL TVA BON"); numbers carry noise.
"""
import re


def _num(s):
    if not s:
        return None
    m = re.search(r"-?\d+(?:[.,]\d+)?", s.replace(" ", ""))
    return float(m.group(0).replace(",", ".")) if m else None


def _bracket(expense_row):
    """Trailing single uppercase VAT bracket letter, e.g. '... 10.00 A' -> 'A'."""
    row = (expense_row or "").strip()
    m = re.search(r"\d[.,]\d{2}\s*([A-Z])\s*$", row)
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z])\s*$", row)
    return m.group(1) if m else ""


def _summary(doc):
    for f in doc.get("SummaryFields", []):
        yield (
            f.get("Type", {}).get("Text", ""),
            (f.get("ValueDetection", {}) or {}).get("Text", ""),
            (f.get("LabelDetection", {}) or {}).get("Text", ""),
        )


def parse_analyze_expense(resp):
    docs = resp.get("ExpenseDocuments", [])
    if not docs:
        return None
    doc = docs[0]
    sf = list(_summary(doc))

    def first(t):
        return next((v for typ, v, lab in sf if typ == t), "")

    # bracket letter -> VAT rate, from labels like 'TVA A' / 'TOTAL TVA A 21%'
    vat_map = {}
    for typ, val, lab in sf:
        m = re.search(r"TVA\s+([A-Z])", lab or "")
        pct = re.search(r"(\d+(?:[.,]\d+)?)\s*%", (val or "") + " " + (lab or ""))
        if m and pct:
            vat_map.setdefault(m.group(1), float(pct.group(1).replace(",", ".")))

    # grand total: prefer AMOUNT_PAID; else a TOTAL not labelled 'BON' (which is the VAT total)
    grand = _num(first("AMOUNT_PAID"))
    if grand is None:
        cands = [_num(v) for typ, v, lab in sf if typ == "TOTAL" and "BON" not in (lab or "").upper()]
        cands = [x for x in cands if x is not None]
        grand = max(cands) if cands else None

    items = []
    for g in doc.get("LineItemGroups", []):
        for li in g.get("LineItems", []):
            fm = {f.get("Type", {}).get("Text"): (f.get("ValueDetection", {}) or {}).get("Text", "")
                  for f in li.get("LineItemExpenseFields", [])}
            bracket = _bracket(fm.get("EXPENSE_ROW", ""))
            items.append({
                "raw_text": fm.get("ITEM", "").strip(),
                "expense_row": fm.get("EXPENSE_ROW", "").strip(),
                "quantity": _num(fm.get("QUANTITY", "")),
                "line_amount": _num(fm.get("PRICE", "")),
                "vat_bracket_letter": bracket,
                "vat_percent": vat_map.get(bracket),
            })

    return {
        "supplier": first("VENDOR_NAME") or first("NAME"),
        "supplier_cui": first("TAX_PAYER_ID"),
        "date": first("INVOICE_RECEIPT_DATE"),
        "grand_total": grand,
        "vat_map": vat_map,
        "items": items,
    }


def validate(receipt):
    """Light Stage-B3 validation: line-sum vs grand total, and VAT coverage from brackets."""
    amounts = [i["line_amount"] for i in receipt["items"] if i["line_amount"] is not None]
    line_sum = round(sum(amounts), 2) if amounts else None
    grand = receipt["grand_total"]
    sum_ok = (line_sum is not None and grand is not None and abs(line_sum - grand) <= 0.10)
    vat_from_bracket = sum(1 for i in receipt["items"] if i["vat_percent"] is not None)
    return {
        "line_sum": line_sum, "grand_total": grand,
        "sum_check": "PASS" if sum_ok else "REVIEW",
        "vat_resolved_by_bracket": f"{vat_from_bracket}/{len(receipt['items'])}",
    }

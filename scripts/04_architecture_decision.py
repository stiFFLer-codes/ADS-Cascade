"""
04_architecture_decision.py
----------------------------
Step 4 of the analysis pipeline — Architecture Decision Engine.

Reads Script 3.5's intelligence outputs and applies threshold-based decision
rules to produce a structured architecture recommendation for Phase 2.

Script 4 does NOT compute statistics — it interprets them.

Input:  data/outputs/intelligence/*.csv  (all from Script 3.5)
        data/outputs/invoice_statistics.csv
        data/outputs/gl_statistics.csv
Output: reports/architecture_decision.md
        data/outputs/intelligence/decision_matrix.csv
        data/outputs/intelligence/feature_selection.csv
"""

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.settings import (
    INTELLIGENCE_DIR, REPORTS_DIR, CSV_ENCODING,
    INVOICE_STATISTICS_CSV, GL_STATISTICS_CSV,
)
from utils.logger import get_logger
from utils.csv_writer import write_csv

logger = get_logger("04_architecture_decision", log_file="04_architecture_decision.log")

# ---------------------------------------------------------------------------
# Decision thresholds — named constants, not magic numbers.
# ponytail: all thresholds are starting points calibrated on the D406 dataset.
# Adjust these based on domain feedback; decision_matrix.csv records actuals
# vs thresholds for easy re-calibration.
# ---------------------------------------------------------------------------

# Rule 1: Retrieval strategy
THRESHOLD_ADS_GLOBAL          = 0.90   # ADS >= this AND cross-co >= its threshold → global
THRESHOLD_ADS_HYBRID          = 0.75   # ADS >= this but cross-co below → hybrid
THRESHOLD_CROSS_CO_GLOBAL     = 0.85   # cross-company consistency for global retrieval

# Rule 3: Model complexity
THRESHOLD_DETERMINISTIC_RULES = 0.90   # >= 90% deterministic → rules-first
THRESHOLD_DETERMINISTIC_EMBED = 0.70   # >= 70% → embedding-primary; else LLM

# Rule 4: VAT strategy
THRESHOLD_VAT_DISCRIMINATOR   = 0.95   # >= 95% single-VAT → use as discriminator
THRESHOLD_VAT_SECONDARY       = 0.70   # >= 70% → secondary feature; else ignore

# Rule 5: Warehouse
THRESHOLD_WAREHOUSE_DROP      = 0.90   # >= 90% missing → drop

# Rule 2: Feature AI-value mapping
AI_VALUE_ACTION = {
    "DROP":   "EXCLUDE",
    "LOW":    "EXCLUDE_OR_OPTIONAL",
    "MEDIUM": "INCLUDE_WITH_FALLBACK",
    "HIGH":   "INCLUDE_REQUIRED",
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _read_csv(path: Path) -> list[dict]:
    """Read a CSV into a list of dicts. Returns [] if file missing."""
    if not path.exists():
        logger.warning("File not found: %s", path)
        return []
    with open(path, "r", encoding=CSV_ENCODING) as f:
        return list(csv.DictReader(f))


def _safe_float(val: str | None, default: float = 0.0) -> float:
    try:
        return float(val) if val else default
    except (ValueError, TypeError):
        return default


def load_intelligence() -> dict:
    """Load all Script 3.5 CSVs into a single dict of lists."""
    files = {
        "product_ambiguity":         INTELLIGENCE_DIR / "product_ambiguity.csv",
        "company_consistency":       INTELLIGENCE_DIR / "company_consistency.csv",
        "cross_company_consistency": INTELLIGENCE_DIR / "cross_company_consistency.csv",
        "vat_consistency":           INTELLIGENCE_DIR / "vat_consistency.csv",
        "ai_readiness":              INTELLIGENCE_DIR / "ai_readiness.csv",
        "data_quality":              INTELLIGENCE_DIR / "data_quality_report.csv",
        "dataset_statistics":        INTELLIGENCE_DIR / "dataset_statistics.csv",
    }
    data = {}
    for key, path in files.items():
        rows = _read_csv(path)
        logger.info("Loaded %s: %d rows", key, len(rows))
        data[key] = rows
    return data


def load_headline_stats() -> dict:
    """Load invoice_statistics.csv and gl_statistics.csv for report context."""
    stats = {}
    for path in (INVOICE_STATISTICS_CSV, GL_STATISTICS_CSV):
        for row in _read_csv(path):
            # Both files have Metric/Value or metric/value columns
            key = row.get("Metric") or row.get("metric", "")
            val = row.get("Value") or row.get("value", "")
            stats[key] = val
    return stats


# ---------------------------------------------------------------------------
# Decision rules
# ---------------------------------------------------------------------------

def compute_dataset_ads(products: list[dict]) -> tuple[float, float]:
    """
    Compute weighted and unweighted dataset ADS from product_ambiguity.csv.

    Returns (weighted_ads, unweighted_ads).
    """
    if not products:
        return 0.0, 0.0

    total_occ = 0
    weighted_sum = 0.0
    det_sum = 0.0

    for p in products:
        occ = int(_safe_float(p.get("total_occurrences"), 1))
        det = _safe_float(p.get("determinism_score"), 0.0)
        weighted_sum += det * occ
        total_occ += occ
        det_sum += det

    weighted = weighted_sum / total_occ if total_occ else 0.0
    unweighted = det_sum / len(products) if products else 0.0
    return weighted, unweighted


def compute_cross_company_score(cross_co: list[dict]) -> float:
    """Average cross_company_determinism across all multi-company products."""
    multi = [r for r in cross_co
             if int(_safe_float(r.get("n_companies"), 0)) >= 2]
    if not multi:
        return 0.0
    return sum(_safe_float(r.get("cross_company_determinism"), 0.0) for r in multi) / len(multi)


def decide_retrieval_strategy(dataset_ads: float, cross_co_score: float) -> tuple[str, str, list[dict]]:
    """
    Rule 1: GLOBAL_RETRIEVAL / HYBRID / COMPANY_SPECIFIC.
    Returns (decision, rationale, matrix_rows).
    """
    rows = []

    if dataset_ads >= THRESHOLD_ADS_GLOBAL and cross_co_score >= THRESHOLD_CROSS_CO_GLOBAL:
        decision = "GLOBAL_RETRIEVAL"
        rationale = (
            f"Products map consistently to accounts across companies. "
            f"ADS={dataset_ads:.4f} >= {THRESHOLD_ADS_GLOBAL}, "
            f"cross-company={cross_co_score:.4f} >= {THRESHOLD_CROSS_CO_GLOBAL}. "
            f"A single global vector DB is sufficient."
        )
    elif dataset_ads >= THRESHOLD_ADS_HYBRID:
        decision = "HYBRID"
        rationale = (
            f"Products are internally consistent (ADS={dataset_ads:.4f} >= {THRESHOLD_ADS_HYBRID}) "
            f"but vary across companies (cross-company={cross_co_score:.4f} < {THRESHOLD_CROSS_CO_GLOBAL}). "
            f"Use global retrieval with company-specific overrides."
        )
    else:
        decision = "COMPANY_SPECIFIC"
        rationale = (
            f"High ambiguity (ADS={dataset_ads:.4f} < {THRESHOLD_ADS_HYBRID}). "
            f"Each company needs its own knowledge base."
        )

    rows.append({
        "rule_id": "R1", "rule_name": "retrieval_strategy",
        "metric_name": "dataset_ads", "metric_value": f"{dataset_ads:.4f}",
        "threshold": str(THRESHOLD_ADS_GLOBAL), "comparison": ">=",
        "decision": decision, "rationale": f"ADS {dataset_ads:.4f} vs threshold {THRESHOLD_ADS_GLOBAL}",
    })
    rows.append({
        "rule_id": "R1", "rule_name": "retrieval_strategy",
        "metric_name": "cross_company_consistency", "metric_value": f"{cross_co_score:.4f}",
        "threshold": str(THRESHOLD_CROSS_CO_GLOBAL), "comparison": ">=",
        "decision": decision, "rationale": f"Cross-co {cross_co_score:.4f} vs threshold {THRESHOLD_CROSS_CO_GLOBAL}",
    })

    return decision, rationale, rows


def decide_feature_selection(ai_readiness: list[dict], data_quality: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Rule 2: Feature selection based on AI readiness and data quality.
    Returns (feature_selection_rows, matrix_rows).
    """
    # Build missing_pct lookup from data_quality
    missing_by_field = {}
    for row in data_quality:
        field = row.get("field", "")
        missing_by_field[field] = _safe_float(row.get("missing_pct"), 0.0)

    features = []
    matrix_rows = []

    for row in ai_readiness:
        feature = row.get("feature", "")
        ai_value = row.get("ai_value", "").upper()
        action = AI_VALUE_ACTION.get(ai_value, "REVIEW")
        missing_pct = missing_by_field.get(feature, _safe_float(row.get("missing_pct"), 0.0))
        consistency_value = row.get("consistency_value", "")
        recommendation = row.get("recommendation", "")

        features.append({
            "feature": feature,
            "missing_pct": f"{missing_pct:.2f}",
            "consistency": consistency_value,
            "ai_value": ai_value,
            "action": action,
            "rationale": recommendation,
        })

        matrix_rows.append({
            "rule_id": "R2", "rule_name": f"feature_{feature}",
            "metric_name": "ai_value", "metric_value": ai_value,
            "threshold": "-", "comparison": "map",
            "decision": action, "rationale": recommendation,
        })

    return features, matrix_rows


def decide_model_complexity(products: list[dict]) -> tuple[str, str, list[dict]]:
    """
    Rule 3: RULES_FIRST / EMBEDDING_PRIMARY / LLM_REQUIRED.
    """
    if not products:
        return "LLM_REQUIRED", "No product data available.", []

    n = len(products)
    deterministic = sum(1 for p in products if _safe_float(p.get("determinism_score")) > 0.95)
    ambiguous = sum(1 for p in products if _safe_float(p.get("determinism_score")) < 0.50)

    det_pct = deterministic / n
    amb_pct = ambiguous / n

    if det_pct >= THRESHOLD_DETERMINISTIC_RULES:
        decision = "RULES_FIRST"
        rationale = (
            f"{det_pct:.1%} of products are deterministic (>{THRESHOLD_DETERMINISTIC_RULES:.0%}). "
            f"Use deterministic lookup for the majority; embedding search only for the "
            f"{amb_pct:.1%} ambiguous tail."
        )
    elif det_pct >= THRESHOLD_DETERMINISTIC_EMBED:
        decision = "EMBEDDING_PRIMARY"
        rationale = (
            f"{det_pct:.1%} deterministic, {amb_pct:.1%} ambiguous. "
            f"Significant minority of ambiguous products. "
            f"Embedding similarity is the primary classifier."
        )
    else:
        decision = "LLM_REQUIRED"
        rationale = (
            f"Only {det_pct:.1%} deterministic, {amb_pct:.1%} ambiguous. "
            f"High ambiguity across the dataset. LLM reasoning needed."
        )

    rows = [{
        "rule_id": "R3", "rule_name": "model_complexity",
        "metric_name": "deterministic_pct", "metric_value": f"{det_pct:.4f}",
        "threshold": str(THRESHOLD_DETERMINISTIC_RULES), "comparison": ">=",
        "decision": decision, "rationale": rationale,
    }, {
        "rule_id": "R3", "rule_name": "model_complexity",
        "metric_name": "ambiguous_pct", "metric_value": f"{amb_pct:.4f}",
        "threshold": "0.50", "comparison": "det_score<",
        "decision": decision, "rationale": f"{ambiguous} of {n} products are ambiguous",
    }]

    return decision, rationale, rows


def decide_vat_strategy(vat: list[dict]) -> tuple[str, str, list[dict]]:
    """
    Rule 4: DISCRIMINATOR / SECONDARY_FEATURE / IGNORE.
    """
    if not vat:
        return "IGNORE", "No VAT data available.", []

    n = len(vat)
    single_vat = sum(1 for v in vat if int(_safe_float(v.get("n_vat_rates"), 0)) == 1)
    stable_pct = single_vat / n if n else 0.0

    if stable_pct >= THRESHOLD_VAT_DISCRIMINATOR:
        decision = "DISCRIMINATOR"
        rationale = (
            f"VAT is highly informative: {stable_pct:.1%} of products have a single VAT rate "
            f"(>= {THRESHOLD_VAT_DISCRIMINATOR:.0%}). Use as primary ranking signal."
        )
    elif stable_pct >= THRESHOLD_VAT_SECONDARY:
        decision = "SECONDARY_FEATURE"
        rationale = (
            f"VAT is somewhat informative: {stable_pct:.1%} single-rate "
            f"(>= {THRESHOLD_VAT_SECONDARY:.0%}). Include as feature but don't rely on it."
        )
    else:
        decision = "IGNORE"
        rationale = (
            f"VAT varies too much: only {stable_pct:.1%} single-rate "
            f"(< {THRESHOLD_VAT_SECONDARY:.0%}). Not useful as discriminator."
        )

    rows = [{
        "rule_id": "R4", "rule_name": "vat_strategy",
        "metric_name": "vat_stable_pct", "metric_value": f"{stable_pct:.4f}",
        "threshold": str(THRESHOLD_VAT_DISCRIMINATOR), "comparison": ">=",
        "decision": decision, "rationale": rationale,
    }]

    return decision, rationale, rows


def decide_warehouse_strategy(data_quality: list[dict]) -> tuple[str, str, list[dict]]:
    """
    Rule 5: DROP / INCLUDE_OPTIONAL for warehouse field.
    """
    missing_pct = 100.0  # default: assume missing
    for row in data_quality:
        if row.get("field", "").lower() == "warehouse_id":
            missing_pct = _safe_float(row.get("missing_pct"), 100.0)
            break

    if missing_pct >= THRESHOLD_WAREHOUSE_DROP * 100:
        decision = "DROP"
        rationale = (
            f"Warehouse data is absent for {missing_pct:.1f}% of records "
            f"(>= {THRESHOLD_WAREHOUSE_DROP:.0%}). Exclude from Phase 2."
        )
    else:
        decision = "INCLUDE_OPTIONAL"
        rationale = f"Warehouse missing {missing_pct:.1f}% — include as optional feature."

    rows = [{
        "rule_id": "R5", "rule_name": "warehouse",
        "metric_name": "missing_pct", "metric_value": f"{missing_pct:.1f}",
        "threshold": str(THRESHOLD_WAREHOUSE_DROP * 100), "comparison": ">=",
        "decision": decision, "rationale": rationale,
    }]

    return decision, rationale, rows


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def _top_ambiguous(products: list[dict], n: int = 20) -> list[dict]:
    """Top N most ambiguous products (lowest determinism)."""
    scored = [(p, _safe_float(p.get("determinism_score"), 1.0)) for p in products]
    scored.sort(key=lambda x: x[1])
    return [p for p, _ in scored[:n]]


def _company_ranking(companies: list[dict]) -> tuple[list[dict], list[dict]]:
    """Top 5 most and least consistent companies."""
    ranked = sorted(
        companies,
        key=lambda c: _safe_float(c.get("consistency_pct"), 0),
        reverse=True,
    )
    return ranked[:5], ranked[-5:]


def generate_report(
    *,
    headline: dict,
    dataset_ads_w: float,
    dataset_ads_u: float,
    cross_co_score: float,
    retrieval: tuple[str, str],
    features: list[dict],
    complexity: tuple[str, str],
    vat: tuple[str, str],
    warehouse: tuple[str, str],
    products: list[dict],
    companies: list[dict],
    cross_co: list[dict],
    matrix: list[dict],
    data_quality: list[dict],
) -> str:
    """Build the architecture_decision.md report as a string."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    n_companies = headline.get("Total Companies", "?")
    n_invoices = headline.get("Total invoices", "?")
    n_lines = headline.get("Total invoice lines", "?")
    n_products = headline.get("Unique products", "?")

    ads_divergence = abs(dataset_ads_w - dataset_ads_u)
    ads_note = ""
    if ads_divergence > 0.10:
        ads_note = (
            f"\n\n> **⚠ ADS Divergence Warning:** Weighted ADS ({dataset_ads_w:.4f}) and "
            f"unweighted ADS ({dataset_ads_u:.4f}) differ by {ads_divergence:.4f} "
            f"(>{0.10}). High-volume products may be skewing the weighted score."
        )

    # Feature selection table
    feat_table = "| Feature | Missing % | Consistency | AI Value | Action | Rationale |\n"
    feat_table += "| ------- | --------- | ----------- | -------- | ------ | --------- |\n"
    for f in features:
        feat_table += (
            f"| {f['feature']} | {f['missing_pct']}% | {f['consistency']} "
            f"| {f['ai_value']} | {f['action']} | {f['rationale']} |\n"
        )

    # Top ambiguous products
    top_ambiguous = _top_ambiguous(products, 20)
    amb_lines = ""
    for i, p in enumerate(top_ambiguous, 1):
        name = p.get("normalized_product", "?")
        det = _safe_float(p.get("determinism_score"), 0)
        n_acc = p.get("n_accounts", "?")
        accs = p.get("all_accounts", "")
        amb_lines += f"{i}. **{name}** — determinism={det:.4f}, {n_acc} accounts ({accs})\n"

    # Company ranking
    best_co, worst_co = _company_ranking(companies)
    best_lines = "\n".join(
        f"  - {c.get('company', '?')}: {c.get('consistency_pct', '?')}% consistent, "
        f"avg determinism {c.get('avg_determinism', '?')}"
        for c in best_co
    )
    worst_lines = "\n".join(
        f"  - {c.get('company', '?')}: {c.get('consistency_pct', '?')}% consistent, "
        f"avg determinism {c.get('avg_determinism', '?')}"
        for c in worst_co
    )

    # Cross-company divergent products (those with low cross_company_determinism)
    divergent = sorted(
        [r for r in cross_co if int(_safe_float(r.get("n_companies"), 0)) >= 2],
        key=lambda r: _safe_float(r.get("cross_company_determinism"), 1.0),
    )[:20]
    divergent_lines = ""
    for i, r in enumerate(divergent, 1):
        name = r.get("normalized_product", "?")
        det = _safe_float(r.get("cross_company_determinism"), 0)
        n_co = r.get("n_companies", "?")
        n_acc = r.get("n_accounts_global", "?")
        divergent_lines += f"{i}. **{name}** — cross-co determinism={det:.4f}, {n_co} companies, {n_acc} global accounts\n"

    # Data quality issues
    dq_lines = ""
    for row in data_quality:
        field = row.get("field", "")
        missing = _safe_float(row.get("missing_pct"), 0)
        notes = row.get("notes", "")
        if missing > 0 or notes:
            dq_lines += f"- **{field}**: {missing:.1f}% missing{f' — {notes}' if notes else ''}\n"

    # Decision matrix table
    matrix_table = "| Rule | Metric | Value | Threshold | Comparison | Decision | Rationale |\n"
    matrix_table += "| ---- | ------ | ----- | --------- | ---------- | -------- | --------- |\n"
    for m in matrix:
        matrix_table += (
            f"| {m['rule_id']} | {m['metric_name']} | {m['metric_value']} "
            f"| {m['threshold']} | {m['comparison']} | {m['decision']} | {m['rationale']} |\n"
        )

    # Confidence level
    if dataset_ads_w >= 0.90:
        confidence = "HIGH"
    elif dataset_ads_w >= 0.75:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # Mermaid diagram
    mermaid = _generate_mermaid(retrieval[0], complexity[0], vat[0], warehouse[0])

    report = f"""# D406 Invoice Classification — Architecture Decision Report

Generated: {now}
Dataset: {n_companies} companies, {n_invoices} invoices, {n_lines} lines, {n_products} unique products

---

## Executive Summary

The D406 dataset exhibits a **weighted ADS of {dataset_ads_w:.4f}** (unweighted: {dataset_ads_u:.4f}) with a cross-company consistency score of {cross_co_score:.4f}. Based on evidence-driven threshold analysis, the recommended retrieval strategy is **{retrieval[0]}** with **{confidence}** confidence. The model complexity recommendation is **{complexity[0]}**, and VAT should be used as a **{vat[0]}** signal.{ads_note}

---

## 1. Accounting Determinism Score

- **Dataset ADS (weighted):** {dataset_ads_w:.4f}
- **Dataset ADS (unweighted):** {dataset_ads_u:.4f}
- **Cross-company consistency:** {cross_co_score:.4f}

**Interpretation:** {"The dataset shows high consistency — most products map to a single dominant account with high confidence." if dataset_ads_w >= 0.85 else "The dataset shows moderate to low consistency — many products map to multiple accounts, requiring more sophisticated classification." if dataset_ads_w >= 0.70 else "The dataset is highly ambiguous — products frequently map to multiple accounts across different contexts."}

### Per-Company ADS Distribution

**Top 5 most consistent:**
{best_lines}

**Top 5 least consistent:**
{worst_lines}

---

## 2. Retrieval Strategy Decision

- **Decision:** {retrieval[0]}
- **Evidence:**
  - Dataset ADS = {dataset_ads_w:.4f} (threshold: {THRESHOLD_ADS_GLOBAL} for global, {THRESHOLD_ADS_HYBRID} for hybrid)
  - Cross-company consistency = {cross_co_score:.4f} (threshold: {THRESHOLD_CROSS_CO_GLOBAL})
- **Rationale:** {retrieval[1]}

---

## 3. Feature Selection

{feat_table}

---

## 4. Model Complexity Decision

- **Decision:** {complexity[0]}
- **Evidence:** {complexity[1]}

---

## 5. VAT Strategy

- **Decision:** {vat[0]}
- **Evidence:** {vat[1]}

---

## 6. Key Findings

### Most Ambiguous Products (Top 20)

{amb_lines}

### Products That Differ Across Companies (Top 20)

{divergent_lines}

---

## 7. Risks & Limitations

### Data Quality Issues

{dq_lines if dq_lines else "No significant data quality issues detected."}

### Edge Cases

- Products with determinism scores between 0.50–0.70 exist in a "grey zone" — they may flip classification depending on context.
- Cross-company divergent products (listed above) may require manual review before Phase 2 training.
- Warehouse data is {warehouse[0]}ped from analysis due to {_safe_float(next((r.get('missing_pct', '0') for r in data_quality if r.get('field', '').lower() == 'warehouse_id'), '100')):.0f}% missing values.

### Recommendations for Data Collection

- Prioritize filling warehouse data if future analysis needs spatial features.
- Investigate the top ambiguous products to determine if they represent genuine accounting flexibility or data entry errors.
- Consider standardizing product descriptions across companies to improve cross-company consistency.

---

## 8. Recommended Phase 2 Architecture

```mermaid
{mermaid}
```

### Architecture Notes

- **Retrieval:** {retrieval[0]} — {retrieval[1][:120]}…
- **Model:** {complexity[0]} — handle the deterministic majority with lookup, use ML for the ambiguous tail.
- **VAT:** {vat[0]} — {"use as a primary ranking signal to disambiguate products." if vat[0] == "DISCRIMINATOR" else "include as secondary feature." if vat[0] == "SECONDARY_FEATURE" else "exclude from classification features."}
- **Warehouse:** {warehouse[0]} — {warehouse[1][:100]}

---

## Appendix: Decision Matrix

{matrix_table}

---

*Report generated by `04_architecture_decision.py` — all decisions are based on named thresholds and can be recalibrated by adjusting constants at the top of the script.*
"""
    return report


def _generate_mermaid(retrieval: str, complexity: str, vat: str, warehouse: str) -> str:
    """Generate a Mermaid flowchart of the recommended Phase 2 architecture."""

    # Determine retrieval nodes
    if retrieval == "GLOBAL_RETRIEVAL":
        retrieval_block = '    B["Global Vector DB"]'
        retrieval_note = '    B --> C["Similarity Search"]'
    elif retrieval == "HYBRID":
        retrieval_block = '    B["Global Vector DB + Company Overrides"]'
        retrieval_note = '    B --> C["Hybrid Similarity Search"]'
    else:
        retrieval_block = '    B["Per-Company Vector DBs"]'
        retrieval_note = '    B --> C["Company-Scoped Search"]'

    # Determine model nodes
    if complexity == "RULES_FIRST":
        model_block = '    C --> D{"Deterministic Lookup"}\n    D -->|Match| E["Return Account"]\n    D -->|No Match| F["Embedding Fallback"]'
    elif complexity == "EMBEDDING_PRIMARY":
        model_block = '    C --> D["Embedding Classifier"]\n    D --> E["Ranked Candidates"]\n    E --> F["Confidence Filter"]'
    else:
        model_block = '    C --> D["LLM Reasoning"]\n    D --> E["Context-Aware Classification"]\n    E --> F["Confidence Score"]'

    # VAT node
    if vat == "DISCRIMINATOR":
        vat_block = '    F --> G["VAT Discriminator Re-ranking"]'
    elif vat == "SECONDARY_FEATURE":
        vat_block = '    F --> G["VAT as Secondary Signal"]'
    else:
        vat_block = '    F --> G["Direct Output (no VAT)"]'

    return f"""flowchart TD
    A["Invoice Line Input"] --> |"product + context"| B
{retrieval_block}
{retrieval_note}
{model_block}
{vat_block}
    G --> H["Predicted Account ID"]
    H --> I["Confidence Score + Audit Trail"]"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("=" * 60)
    logger.info("  Script 4 — Architecture Decision Engine")
    logger.info("=" * 60)

    # 1. Load data
    data = load_intelligence()
    headline = load_headline_stats()

    products = data["product_ambiguity"]
    companies = data["company_consistency"]
    cross_co = data["cross_company_consistency"]
    vat_data = data["vat_consistency"]
    ai_readiness = data["ai_readiness"]
    data_quality = data["data_quality"]

    # 2. Compute dataset-level metrics
    dataset_ads_w, dataset_ads_u = compute_dataset_ads(products)
    logger.info("Dataset ADS: weighted=%.4f, unweighted=%.4f", dataset_ads_w, dataset_ads_u)

    cross_co_score = compute_cross_company_score(cross_co)
    logger.info("Cross-company consistency score: %.4f", cross_co_score)

    # 3. Run decision rules
    all_matrix_rows = []

    retrieval_decision, retrieval_rationale, r1_rows = decide_retrieval_strategy(dataset_ads_w, cross_co_score)
    all_matrix_rows.extend(r1_rows)
    logger.info("R1 Retrieval: %s", retrieval_decision)

    feature_rows, r2_rows = decide_feature_selection(ai_readiness, data_quality)
    all_matrix_rows.extend(r2_rows)
    logger.info("R2 Features: %d evaluated", len(feature_rows))

    complexity_decision, complexity_rationale, r3_rows = decide_model_complexity(products)
    all_matrix_rows.extend(r3_rows)
    logger.info("R3 Complexity: %s", complexity_decision)

    vat_decision, vat_rationale, r4_rows = decide_vat_strategy(vat_data)
    all_matrix_rows.extend(r4_rows)
    logger.info("R4 VAT: %s", vat_decision)

    warehouse_decision, warehouse_rationale, r5_rows = decide_warehouse_strategy(data_quality)
    all_matrix_rows.extend(r5_rows)
    logger.info("R5 Warehouse: %s", warehouse_decision)

    # 4. Write decision_matrix.csv
    matrix_fields = [
        "rule_id", "rule_name", "metric_name", "metric_value",
        "threshold", "comparison", "decision", "rationale",
    ]
    matrix_path = INTELLIGENCE_DIR / "decision_matrix.csv"
    n = write_csv(all_matrix_rows, matrix_path, fieldnames=matrix_fields)
    logger.info("Wrote %d rows → %s", n, matrix_path)

    # 5. Write feature_selection.csv
    feat_fields = ["feature", "missing_pct", "consistency", "ai_value", "action", "rationale"]
    feat_path = INTELLIGENCE_DIR / "feature_selection.csv"
    n = write_csv(feature_rows, feat_path, fieldnames=feat_fields)
    logger.info("Wrote %d rows → %s", n, feat_path)

    # 6. Generate report
    report = generate_report(
        headline=headline,
        dataset_ads_w=dataset_ads_w,
        dataset_ads_u=dataset_ads_u,
        cross_co_score=cross_co_score,
        retrieval=(retrieval_decision, retrieval_rationale),
        features=feature_rows,
        complexity=(complexity_decision, complexity_rationale),
        vat=(vat_decision, vat_rationale),
        warehouse=(warehouse_decision, warehouse_rationale),
        products=products,
        companies=companies,
        cross_co=cross_co,
        matrix=all_matrix_rows,
        data_quality=data_quality,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "architecture_decision.md"
    report_path.write_text(report, encoding="utf-8")
    logger.info("Wrote report → %s", report_path)

    # 7. Summary
    logger.info("=" * 60)
    logger.info("  SUMMARY")
    logger.info("  Retrieval:  %s", retrieval_decision)
    logger.info("  Complexity: %s", complexity_decision)
    logger.info("  VAT:        %s", vat_decision)
    logger.info("  Warehouse:  %s", warehouse_decision)
    logger.info("  Confidence: %s", "HIGH" if dataset_ads_w >= 0.90 else "MEDIUM" if dataset_ads_w >= 0.75 else "LOW")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

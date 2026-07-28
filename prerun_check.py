"""
prerun_check.py
---------------
Pre-run checks for the contai-analysis pipeline.

Usage
-----
    # Check step 1
    python prerun_check.py 01

    # Check step 1.5
    python prerun_check.py 01_5

    # Default — checks the most recently relevant step (01_5)
    python prerun_check.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# ── helpers ──────────────────────────────────────────────────────────────────

PASS  = "[OK  ]"
WARN  = "[WARN]"
FAIL  = "[FAIL]"

errors:   list[str] = []
warnings: list[str] = []


def ok(msg: str)   -> None: print(f"{PASS} {msg}")
def warn(msg: str) -> None: print(f"{WARN} {msg}"); warnings.append(msg)
def fail(msg: str) -> None: print(f"{FAIL} {msg}"); errors.append(msg)


def check_python(min_major: int = 3, min_minor: int = 11) -> None:
    v = sys.version_info
    label = f"Python {v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) < (min_major, min_minor):
        fail(f"{label} -- need {min_major}.{min_minor}+")
    else:
        ok(label)


def check_import(package: str, attr: str = "__version__") -> bool:
    try:
        mod = __import__(package)
        ver = getattr(mod, attr, "?")
        ok(f"{package} {ver}")
        return True
    except ImportError:
        fail(f"{package} not installed -> pip install {package}")
        return False


def check_config() -> bool:
    try:
        from config import settings  # noqa: F401
        ok("config.settings imported")
        return True
    except Exception as e:
        fail(f"config.settings import failed: {e}")
        return False


def check_utils() -> bool:
    try:
        from utils.logger     import get_logger      # noqa: F401
        from utils.filesystem import ensure_dir       # noqa: F401
        from utils.csv_writer import write_csv        # noqa: F401
        ok("utils package imported")
        return True
    except Exception as e:
        fail(f"utils import failed: {e}")
        return False


def check_file_exists(path: Path, label: str) -> bool:
    if path.exists():
        ok(f"{label} found -> {path}")
        return True
    fail(f"{label} NOT found -> {path}")
    return False


def check_dir_writable(path: Path, label: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    test = path / ".write_test"
    try:
        test.touch(); test.unlink()
        ok(f"{label} writable -> {path}")
    except OSError as e:
        fail(f"{label} not writable -> {path} ({e})")


def report() -> None:
    print()
    if warnings:
        for w in warnings:
            print(f"{WARN} {w}")
    if errors:
        print()
        for e in errors:
            print(f"{FAIL} {e}")
        print(f"\nPre-run check FAILED -- fix the {len(errors)} issue(s) above.")
        sys.exit(1)
    else:
        print("Pre-run check PASSED (OK)")


# ── step 01 ───────────────────────────────────────────────────────────────────

def check_step_01() -> None:
    print("=" * 60)
    print("  Pre-run check -- 01_build_inventory.py")
    print("=" * 60)

    check_python()
    check_import("pandas")
    check_config()
    check_utils()

    from config.settings import MANIFEST_DIR, OUTPUTS_DIR, LOGS_DIR

    dataset = MANIFEST_DIR / "Dev-D406-Dataset.json"
    if check_file_exists(dataset, "Dev-D406-Dataset.json"):
        try:
            with open(dataset, encoding="utf-8") as f:
                data = json.load(f)
            ok(f"Dataset valid JSON -- {len(data):,} records")
            expected = {"cui", "company_name", "caen_code",
                        "xml_file_name", "xml_file_url"}
            missing  = expected - (data[0].keys() if data else set())
            if missing:
                warn(f"First record missing fields: {missing}")
            else:
                ok(f"Schema fields present: {sorted(expected)}")
        except json.JSONDecodeError as e:
            fail(f"Dataset is not valid JSON: {e}")

    check_dir_writable(OUTPUTS_DIR, "outputs dir")
    check_dir_writable(LOGS_DIR,    "logs dir")

    report()


# ── step 01_5 ─────────────────────────────────────────────────────────────────

def check_step_01_5() -> None:
    print("=" * 60)
    print("  Pre-run check -- 01_5_xml_normalization.py")
    print("=" * 60)

    # 1. Runtime
    check_python()
    check_import("pandas")
    requests_ok = check_import("requests")
    check_config()
    check_utils()

    from config.settings import (
        OUTPUTS_DIR, DOWNLOADS_DIR, EXTRACTED_DIR, NORMALIZED_DIR, LOGS_DIR,
    )

    # 2. Script imports cleanly
    try:
        import importlib.util, types
        spec = importlib.util.spec_from_file_location(
            "xml_norm",
            ROOT / "scripts" / "01_5_xml_normalization.py",
        )
        # just compile, don't execute main()
        mod = types.ModuleType("xml_norm")
        src = (ROOT / "scripts" / "01_5_xml_normalization.py").read_text(encoding="utf-8")
        compile(src, "01_5_xml_normalization.py", "exec")
        ok("01_5_xml_normalization.py compiles without syntax errors")
    except SyntaxError as e:
        fail(f"Syntax error in script: {e}")

    # 3. Upstream input: metadata.csv
    metadata_path = OUTPUTS_DIR / "metadata.csv"
    if check_file_exists(metadata_path, "metadata.csv (step 1 output)"):
        with open(metadata_path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols   = reader.fieldnames or []
            rows   = list(reader)

        required_cols = {"cui", "file_name", "file_url", "extension", "logical_key"}
        missing_cols  = required_cols - set(cols)
        if missing_cols:
            fail(f"metadata.csv missing columns: {missing_cols}")
        else:
            ok(f"metadata.csv columns OK  ({len(rows):,} rows)")

        # Spot-check URLs look like real S3 links
        bad_urls = [
            r["file_url"] for r in rows[:20]
            if not urlparse(r.get("file_url", "")).scheme.startswith("http")
        ]
        if bad_urls:
            warn(f"{len(bad_urls)} rows in first 20 have non-HTTP file_url")
        else:
            ok("file_url values look valid (sample of 20)")

        # Check extensions are all zip or xml
        exts = {r["extension"].lower() for r in rows}
        unexpected = exts - {"zip", "xml"}
        if unexpected:
            warn(f"Unexpected file extensions in metadata: {unexpected}")
        else:
            ok(f"File extensions in metadata: {exts}")

    # 4. Output directories writable
    for d, label in [
        (DOWNLOADS_DIR,  "downloads dir"),
        (EXTRACTED_DIR,  "extracted dir"),
        (NORMALIZED_DIR, "normalized dir"),
        (OUTPUTS_DIR,    "outputs dir"),
        (LOGS_DIR,       "logs dir"),
    ]:
        check_dir_writable(d, label)

    # 5. Network reachability (quick HEAD on first URL)
    if requests_ok:
        try:
            import requests as req
            with open(metadata_path, encoding="utf-8-sig") as f:
                first_url = next(csv.DictReader(f))["file_url"]
            resp = req.head(first_url, timeout=10)
            if resp.status_code < 400:
                ok(f"S3 reachable (HTTP {resp.status_code}) -> {first_url[:60]}...")
            else:
                warn(f"S3 HEAD returned HTTP {resp.status_code} -- downloads may fail")
        except Exception as e:
            warn(f"Network check skipped / failed: {e}")

    report()


# ── step 03_5 ─────────────────────────────────────────────────────────────────

def check_step_03_5() -> None:
    print("=" * 60)
    print("  Pre-run check -- 03_5_dataset_intelligence.py")
    print("=" * 60)

    check_python()
    check_config()
    check_utils()

    from config.settings import (
        OUTPUTS_DIR, INVOICE_LINES_CSV, PRODUCT_ACCOUNT_MAPPING_CSV,
        GL_ACCOUNTS_CSV, COMPANIES_CSV, INVOICE_STATISTICS_CSV,
        GL_STATISTICS_CSV, INTELLIGENCE_DIR
    )

    # 4. & 5. invoice_lines_all_companies.csv
    if check_file_exists(INVOICE_LINES_CSV, "invoice_lines_all_companies.csv"):
        with open(INVOICE_LINES_CSV, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols = set(reader.fieldnames or [])
            req_cols = {"cui", "normalized_product", "account_id", "vat_percent", "validation_status", "direction"}
            missing = req_cols - cols
            if missing:
                fail(f"invoice_lines_all_companies.csv missing cols: {missing}")
            else:
                ok("invoice_lines_all_companies.csv schema OK")
            
            # Row count sanity
            row_count = 0
            for _ in reader:
                row_count += 1
                if row_count > 1000:
                    break
            if row_count > 1000:
                ok(f"invoice_lines_all_companies.csv has > 1000 rows")
            else:
                warn(f"invoice_lines_all_companies.csv has only {row_count} rows")

    # 6. & 7. product_account_mapping.csv
    if check_file_exists(PRODUCT_ACCOUNT_MAPPING_CSV, "product_account_mapping.csv"):
        with open(PRODUCT_ACCOUNT_MAPPING_CSV, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols = set(reader.fieldnames or [])
            req_cols = {"Company", "Normalized Product", "AccountID", "Count"}
            missing = req_cols - cols
            if missing:
                fail(f"product_account_mapping.csv missing cols: {missing}")
            else:
                ok("product_account_mapping.csv schema OK")

    # 8. company_gl_accounts.csv
    if not GL_ACCOUNTS_CSV.exists():
        warn("company_gl_accounts.csv missing (enrichment degrades without it)")
    else:
        ok("company_gl_accounts.csv found")

    # 9. companies_inventory.csv
    if not COMPANIES_CSV.exists():
        warn("companies_inventory.csv missing (stats degrade without it)")
    else:
        ok("companies_inventory.csv found")

    # 10. invoice_statistics.csv
    if not INVOICE_STATISTICS_CSV.exists():
        warn("invoice_statistics.csv missing")
    else:
        ok("invoice_statistics.csv found")

    # 11. gl_statistics.csv
    if not GL_STATISTICS_CSV.exists():
        warn("gl_statistics.csv missing")
    else:
        ok("gl_statistics.csv found")

    # 12. 03_5_dataset_intelligence.py compiles
    try:
        script_path = ROOT / "scripts" / "03_5_dataset_intelligence.py"
        if script_path.exists():
            src = script_path.read_text(encoding="utf-8")
            compile(src, "03_5_dataset_intelligence.py", "exec")
            ok("03_5_dataset_intelligence.py compiles without syntax errors")
        else:
            fail("03_5_dataset_intelligence.py not found in scripts/")
    except SyntaxError as e:
        fail(f"Syntax error in 03_5_dataset_intelligence.py: {e}")

    # 13. Output directory writable
    check_dir_writable(INTELLIGENCE_DIR, "intelligence output dir")

    # 15. Disk space (check if outputs dir has >= 100MB)
    try:
        import shutil
        total, used, free = shutil.disk_usage(OUTPUTS_DIR)
        free_mb = free / (1024 * 1024)
        if free_mb >= 100:
            ok(f"Disk space OK ({free_mb:.0f} MB free)")
        else:
            warn(f"Low disk space: {free_mb:.0f} MB free (want >= 100 MB)")
    except Exception as e:
        warn(f"Could not check disk space: {e}")

    report()


# ── step 04 ───────────────────────────────────────────────────────────────────

def check_step_04() -> None:
    print("=" * 60)
    print("  Pre-run check -- 04_architecture_decision.py")
    print("=" * 60)

    # 1–3. Standard checks
    check_python()
    check_config()
    check_utils()

    from config.settings import INTELLIGENCE_DIR, REPORTS_DIR

    # 4. Intelligence directory exists
    if not INTELLIGENCE_DIR.exists():
        fail(f"intelligence/ dir not found -- Script 3.5 must have run -> {INTELLIGENCE_DIR}")
    else:
        ok(f"intelligence/ dir found -> {INTELLIGENCE_DIR}")

    # 5–10. Core input files
    required_files = [
        ("product_ambiguity.csv",         True),
        ("company_consistency.csv",       True),
        ("cross_company_consistency.csv", True),
        ("vat_consistency.csv",           True),
        ("ai_readiness.csv",              True),
        ("data_quality_report.csv",       True),
    ]
    for fname, is_critical in required_files:
        path = INTELLIGENCE_DIR / fname
        if check_file_exists(path, fname):
            with open(path, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                row_count = sum(1 for _ in reader)
            if row_count > 0:
                ok(f"{fname} has {row_count:,} rows")
            elif is_critical:
                fail(f"{fname} is empty -- Script 3.5 output required")
            else:
                warn(f"{fname} is empty")
        elif is_critical:
            pass  # check_file_exists already called fail()

    # 11. dataset_statistics.csv (WARN only)
    ds_path = INTELLIGENCE_DIR / "dataset_statistics.csv"
    if not ds_path.exists():
        warn(f"dataset_statistics.csv missing -- report context will be limited")
    else:
        ok("dataset_statistics.csv found")

    # 12. Reports directory writable
    check_dir_writable(REPORTS_DIR, "reports dir")

    # 13. product_ambiguity.csv schema check
    pa_path = INTELLIGENCE_DIR / "product_ambiguity.csv"
    if pa_path.exists():
        with open(pa_path, encoding="utf-8-sig") as f:
            cols = set(csv.DictReader(f).fieldnames or [])
        required_cols = {"determinism_score", "normalized_product", "total_occurrences"}
        missing_cols = required_cols - cols
        if missing_cols:
            fail(f"product_ambiguity.csv missing columns: {missing_cols}")
        else:
            ok("product_ambiguity.csv schema OK")

    # 14. Script compiles
    try:
        script_path = ROOT / "scripts" / "04_architecture_decision.py"
        if script_path.exists():
            src = script_path.read_text(encoding="utf-8")
            compile(src, "04_architecture_decision.py", "exec")
            ok("04_architecture_decision.py compiles without syntax errors")
        else:
            fail("04_architecture_decision.py not found in scripts/")
    except SyntaxError as e:
        fail(f"Syntax error in 04_architecture_decision.py: {e}")

    # 15. ADS values sanity check
    if pa_path.exists():
        with open(pa_path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            bad_ads = 0
            for row in reader:
                try:
                    det = float(row.get("determinism_score", 0))
                    if det < 0 or det > 1:
                        bad_ads += 1
                except (ValueError, TypeError):
                    bad_ads += 1
        if bad_ads:
            warn(f"{bad_ads} rows in product_ambiguity.csv have ADS outside [0, 1]")
        else:
            ok("ADS values are all within [0, 1]")

    report()


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "03_5"
    if step == "01":
        check_step_01()
    elif step in ("01_5", "015"):
        check_step_01_5()
    elif step in ("03_5", "035"):
        check_step_03_5()
    elif step in ("04", "4"):
        check_step_04()
    else:
        print(f"Unknown step '{step}'. Use: 01, 01_5, 03_5, or 04")
        sys.exit(1)

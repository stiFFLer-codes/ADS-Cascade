"""
01_5_xml_normalization.py  —  Version 3
----------------------------------------
Pipeline stage: download → extract → validate → normalized/

v3 changes over v2
-------------------
1. Parallel downloads via ThreadPoolExecutor — configurable MAX_WORKERS.
2. Exponential backoff replacing flat single retry (1s → 2s → 4s … cap 30s).
3. Atomic writes — download to <target>.tmp, rename on success, delete on
   failure — so a partial file never passes the idempotency check.
4. --force flag — reprocess every row, ignoring files already on disk.
5. MAX_WORKERS and backoff constants moved to config/settings.py.

Usage
-----
    python scripts/01_5_xml_normalization.py                 # normal / resume
    python scripts/01_5_xml_normalization.py --retry-failed  # redo DOWNLOAD errors
    python scripts/01_5_xml_normalization.py --force         # reprocess everything
"""

from __future__ import annotations

import sys
import shutil
import time
import zipfile
import logging
import argparse
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

import pandas as pd
import requests
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.settings import (
    OUTPUTS_DIR,
    DOWNLOADS_DIR,
    EXTRACTED_DIR,
    NORMALIZED_DIR,
    LOGS_DIR,
    DOWNLOAD_WORKERS,
    DOWNLOAD_TIMEOUT,
    BACKOFF_BASE,
    BACKOFF_MAX,
    BACKOFF_MAX_ATTEMPTS,
    AWS_PROFILE,
)

# ---------------------------------------------------------------------------
# Module-level paths
# ---------------------------------------------------------------------------

METADATA   = OUTPUTS_DIR / "metadata.csv"
STATUS_CSV = OUTPUTS_DIR / "normalization_status.csv"
LOG_FILE   = LOGS_DIR    / "xml_normalization.log"

# Thread-safe lock for the progress bar counter
_progress_lock = threading.Lock()

# Thread-safe lock for disk writes to prevent race conditions on duplicate files
# ponytail: global lock on disk writes; upgrade path would be per-file or per-CUI locks
_file_write_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _safe_filename(name: str) -> str:
    """URL-decode percent-encoded characters (e.g. %281%29 → (1))."""
    return unquote(name)


def _exponential_backoff(attempt: int) -> float:
    """Return wait time in seconds for *attempt* (1-based)."""
    return min(BACKOFF_BASE * (2 ** (attempt - 1)), BACKOFF_MAX)


# ---------------------------------------------------------------------------
# Stage functions
# ---------------------------------------------------------------------------

def download_file(url: str, target: Path, logger: logging.Logger,
                  force: bool = False) -> str:
    """
    Download *url* to *target* atomically (via a .tmp file) using AWS CLI.

    Returns
    -------
    "SKIPPED"  — file already existed and --force not set
    "SUCCESS"  — freshly downloaded
    Raises on unrecoverable error.
    """
    if target.exists() and not force:
        return "SKIPPED"

    _mkdir(target.parent)
    tmp = target.with_suffix(target.suffix + ".tmp")

    # Extract S3 bucket and object key from URL
    parsed = urlparse(url)
    bucket = parsed.netloc.split(".")[0]
    key = unquote(parsed.path.lstrip("/"))
    s3_uri = f"s3://{bucket}/{key}"

    for attempt in range(1, BACKOFF_MAX_ATTEMPTS + 1):
        try:
            with _file_write_lock:
                if target.exists() and not force:
                    if tmp.exists():
                        tmp.unlink()
                    return "SUCCESS"

            cmd = ["aws", "s3", "cp", s3_uri, str(tmp), "--profile", AWS_PROFILE]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)

            if res.returncode == 0:
                with _file_write_lock:
                    if target.exists() and not force:
                        if tmp.exists():
                            tmp.unlink()
                        return "SUCCESS"
                    if target.exists() and force:
                        target.unlink()
                    tmp.rename(target)   # atomic on same filesystem
                return "SUCCESS"
            else:
                raise RuntimeError(res.stderr.strip() or f"Exit code {res.returncode}")

        except Exception as exc:
            if attempt == BACKOFF_MAX_ATTEMPTS:
                if tmp.exists():
                    tmp.unlink()
                raise

            wait = _exponential_backoff(attempt)
            logger.warning("Attempt %d/%d failed (%s) — retrying in %.0fs …",
                           attempt, BACKOFF_MAX_ATTEMPTS, exc, wait)
            time.sleep(wait)

    # Should never reach here
    raise RuntimeError("Download loop exited without result")


def extract_or_copy(downloaded: Path, extracted: Path,
                    force: bool = False) -> str:
    """Extract XML from ZIP or copy XML directly. Returns SKIPPED/SUCCESS."""
    _mkdir(extracted.parent)

    with _file_write_lock:
        if extracted.exists() and not force:
            return "SKIPPED"

        suffix = downloaded.suffix.lower()

        if suffix == ".xml":
            shutil.copy2(downloaded, extracted)
            return "SUCCESS"

        if suffix == ".zip":
            with zipfile.ZipFile(downloaded) as z:
                xmls = [x for x in z.namelist() if x.lower().endswith(".xml")]
                if not xmls:
                    raise RuntimeError("ZIP contains no XML files")
                with z.open(xmls[0]) as src, open(extracted, "wb") as dst:
                    shutil.copyfileobj(src, dst)
            return "SUCCESS"

    raise RuntimeError(f"Unsupported file extension: {suffix!r}")


def validate_xml(source: Path, normalized: Path,
                 force: bool = False) -> str:
    """Validate XML well-formedness and copy to normalized/. Returns VALID/SKIPPED."""
    _mkdir(normalized.parent)

    with _file_write_lock:
        if normalized.exists() and not force:
            return "SKIPPED"

        ET.parse(source)           # raises ParseError if malformed
        shutil.copy2(source, normalized)
        return "VALID"


# ---------------------------------------------------------------------------
# Per-row worker
# ---------------------------------------------------------------------------

def process_row(row: pd.Series, logger: logging.Logger,
                force: bool = False) -> dict:
    """
    Run download → extract → validate for one metadata row.
    error_stage is set inside each individual try/except — never inferred.
    """
    cui            = str(row["cui"])
    file_name      = _safe_filename(row["file_name"])
    url            = row["file_url"]

    download_path   = DOWNLOADS_DIR / cui / file_name
    xml_name        = Path(file_name).with_suffix(".xml").name
    extracted_path  = EXTRACTED_DIR  / cui / xml_name
    normalized_path = NORMALIZED_DIR / cui / xml_name

    dl_status  = "PENDING"
    ext_status = "PENDING"
    val_status = "PENDING"
    error_stage   = ""
    error_message = ""

    try:
        try:
            dl_status = download_file(url, download_path, logger, force=force)
        except Exception as exc:
            error_stage, error_message = "DOWNLOAD", str(exc)
            raise

        try:
            ext_status = extract_or_copy(download_path, extracted_path, force=force)
        except Exception as exc:
            error_stage, error_message = "EXTRACTION", str(exc)
            raise

        try:
            val_status = validate_xml(extracted_path, normalized_path, force=force)
        except Exception as exc:
            error_stage, error_message = "VALIDATION", str(exc)
            raise

    except Exception:
        pass

    return {
        "cui":               cui,
        "company_name":      row["company_name"],
        "logical_key":       row.get("logical_key", ""),
        "file_name":         file_name,
        "extension":         row["extension"],
        "download_status":   dl_status,
        "extraction_status": ext_status,
        "validation_status": val_status,
        "download_path":     str(download_path),
        "extracted_path":    str(extracted_path),
        "normalized_path":   str(normalized_path),
        "error_stage":       error_stage,
        "error_message":     error_message,
        "processed_at":      datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(retry_failed: bool = False, force: bool = False) -> None:

    # ── Logging ─────────────────────────────────────────────────────────────
    _mkdir(LOG_FILE.parent)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger("xml_normalizer")

    # ── Load metadata ────────────────────────────────────────────────────────
    if not METADATA.exists():
        raise FileNotFoundError(
            f"metadata.csv not found at {METADATA}\n"
            "Run 01_build_inventory.py first."
        )

    df = pd.read_csv(METADATA)
    logger.info("Loaded metadata: %d rows", len(df))

    # ── Narrow to failed rows if --retry-failed ──────────────────────────────
    if retry_failed and not force:
        if not STATUS_CSV.exists():
            logger.warning("--retry-failed: no previous status CSV — running full batch.")
        else:
            prev = pd.read_csv(STATUS_CSV)
            failed_names = set(
                prev.loc[prev["error_stage"] == "DOWNLOAD", "file_name"]
            )
            original_len = len(df)
            df = df[df["file_name"].apply(_safe_filename).isin(failed_names)]
            logger.info(
                "--retry-failed: %d / %d rows selected",
                len(df), original_len,
            )
            if df.empty:
                logger.info("Nothing to retry.")
                return

    if force:
        logger.info("--force: will reprocess all %d rows regardless of cached files.", len(df))

    # ── Parallel processing ──────────────────────────────────────────────────
    rows_list: list[dict] = [None] * len(df)   # pre-allocate to keep order
    df_records = list(df.iterrows())

    success = 0
    failed  = 0

    logger.info("Starting with %d worker thread(s) …", DOWNLOAD_WORKERS)

    with tqdm(total=len(df), desc="Normalizing", unit="file",
              dynamic_ncols=True) as bar:

        with ThreadPoolExecutor(max_workers=DOWNLOAD_WORKERS) as pool:
            future_to_idx = {
                pool.submit(process_row, row, logger, force): idx
                for idx, (_, row) in enumerate(df_records)
            }

            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    result = future.result()
                except Exception as exc:
                    # Should not happen — process_row catches internally
                    result = {**dict(df_records[idx][1]),
                              "error_stage": "UNEXPECTED",
                              "error_message": str(exc),
                              "processed_at": datetime.now().isoformat(timespec="seconds")}

                rows_list[idx] = result

                with _progress_lock:
                    if result["error_stage"]:
                        failed += 1
                        bar.set_postfix_str(
                            f"FAIL:{result['file_name'][:30]}", refresh=True)
                    else:
                        success += 1
                        bar.set_postfix_str(
                            f"OK:{result['file_name'][:33]}", refresh=True)
                    bar.update(1)

    # ── Write status CSV ─────────────────────────────────────────────────────
    status_df = pd.DataFrame(rows_list)
    _mkdir(STATUS_CSV.parent)

    if retry_failed and not force and STATUS_CSV.exists():
        prev_df  = pd.read_csv(STATUS_CSV)
        combined = pd.concat(
            [prev_df[~prev_df["file_name"].isin(status_df["file_name"])],
             status_df],
            ignore_index=True,
        )
        combined.to_csv(STATUS_CSV, index=False, encoding="utf-8-sig")
    else:
        status_df.to_csv(STATUS_CSV, index=False, encoding="utf-8-sig")

    # ── Summary ──────────────────────────────────────────────────────────────
    sep = "=" * 60
    print(sep)
    print("  XML NORMALIZATION COMPLETE")
    print(sep)
    print(f"  Workers         : {DOWNLOAD_WORKERS}")
    print(f"  Total Processed : {len(df)}")
    print(f"  Successful      : {success}")
    print(f"  Failed          : {failed}")
    if failed:
        by_stage = (
            status_df[status_df["error_stage"] != ""]
            .groupby("error_stage")
            .size()
        )
        for stage, count in by_stage.items():
            print(f"    {stage:<14}: {count}")
        print("\n  Tip: fix the URLs then re-run with --retry-failed")
    print(f"\n  Status CSV : {STATUS_CSV}")
    print(sep)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ADS-Cascade XML normalization pipeline — v3")
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Re-process only rows whose error_stage == DOWNLOAD from last run")
    parser.add_argument(
        "--force", action="store_true",
        help="Reprocess every row, ignoring files already on disk")
    args = parser.parse_args()
    main(retry_failed=args.retry_failed, force=args.force)

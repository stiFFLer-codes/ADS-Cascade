"""
utils/manifest.py
-----------------
Read / write the pipeline manifest that tracks which source files have been
processed and what outputs were produced.

The manifest is a JSON file at ``MANIFEST_FILE`` (see config/settings.py).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from config.settings import MANIFEST_FILE


def _load() -> dict:
    """Load the manifest from disk, returning an empty structure if missing."""
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "entries": []}


def _save(data: dict) -> None:
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def is_processed(source_file: str | Path) -> bool:
    """Return True if *source_file* already has an entry in the manifest."""
    name = Path(source_file).name
    return any(e.get("source_file") == name for e in _load().get("entries", []))


def mark_processed(source_file: str | Path, outputs: list[str] | None = None) -> None:
    """Add or update a manifest entry for *source_file*."""
    name = Path(source_file).name
    data = _load()
    # Remove stale entry for this file, then append a fresh one
    data["entries"] = [e for e in data["entries"] if e.get("source_file") != name]
    data["entries"].append({
        "source_file": name,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "outputs": outputs or [],
    })
    _save(data)


def get_all_entries() -> list[dict]:
    """Return all manifest entries."""
    return _load().get("entries", [])

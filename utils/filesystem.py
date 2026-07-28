"""
utils/filesystem.py
-------------------
File-system helpers: reading/writing JSON and XML, ensuring directories exist.
"""

import json
import shutil
from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """Create *path* (and any missing parents) if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Path) -> dict | list:
    """Read and return the contents of a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict | list, path: Path, indent: int = 2) -> None:
    """Serialise *data* to JSON at *path*, creating parent directories as needed."""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def read_text(path: Path, encoding: str = "utf-8") -> str:
    """Return the full text content of a file."""
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def write_text(content: str, path: Path, encoding: str = "utf-8") -> None:
    """Write *content* to *path*, creating parent directories as needed."""
    ensure_dir(path.parent)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def copy_file(src: Path, dst: Path) -> None:
    """Copy *src* to *dst*, creating parent directories as needed."""
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)


def list_files(directory: Path, pattern: str = "*") -> list[Path]:
    """Return a sorted list of files in *directory* matching *pattern*."""
    return sorted(directory.glob(pattern))

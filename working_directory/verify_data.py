"""Verify the assessment data is in place under ./data/.

Usage: uv run python verify_data.py

Run this after downloading the OneDrive zip and unzipping its contents
into this directory's `data/` subfolder.
"""
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Files at data/ root.
ROOT_FILES = ["leetcode_pool.txt"]

# Files under subfolders of data/.
SUBFOLDER_FILES = {
    "old microscope": [
        "old blue.tif",
        "old green.tif",
        "old red.tif",
        "old yellow.tif",
        "old mask.tif",
    ],
    "new microscope": [
        "new blue.tif",
        "new green.tif",
        "new red.tif",
        "new yellow.tif",
        "new mask.tif",
    ],
    "cells csv": [
        "old cells.csv",
        "new cells.csv",
    ],
}


def check_file(rel_path: str, full_path: Path, missing: list[str], found: list[str]) -> None:
    if not full_path.exists():
        missing.append(f"  - missing file: data/{rel_path}")
    else:
        size_mb = full_path.stat().st_size / (1 << 20)
        found.append(f"  - data/{rel_path} ({size_mb:.1f} MB)")


def main() -> None:
    if not DATA_DIR.exists():
        print(f"ERROR: {DATA_DIR} does not exist.", file=sys.stderr)
        print("Did you unzip the OneDrive download into this directory?", file=sys.stderr)
        sys.exit(1)

    missing: list[str] = []
    found: list[str] = []

    for f in ROOT_FILES:
        check_file(f, DATA_DIR / f, missing, found)

    for folder, files in SUBFOLDER_FILES.items():
        folder_path = DATA_DIR / folder
        if not folder_path.exists():
            missing.append(f"  - missing folder: data/{folder}/")
            continue
        for f in files:
            check_file(f"{folder}/{f}", folder_path / f, missing, found)

    if missing:
        print("Data verification FAILED:", file=sys.stderr)
        for line in missing:
            print(line, file=sys.stderr)
        print(file=sys.stderr)
        print("Expected layout under working_directory/data/:", file=sys.stderr)
        for f in ROOT_FILES:
            print(f"  {f}", file=sys.stderr)
        for folder, files in SUBFOLDER_FILES.items():
            print(f"  {folder}/", file=sys.stderr)
            for f in files:
                print(f"    {f}", file=sys.stderr)
        sys.exit(1)

    print(f"Data OK ({len(found)} files in {DATA_DIR}):")
    for line in found:
        print(line)


if __name__ == "__main__":
    main()

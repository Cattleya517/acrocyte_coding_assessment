"""Verify (and if needed, unzip) the assessment data under ./data/.

Usage: uv run python verify_data.py

If a `.zip` file is sitting in this directory (e.g. the OneDrive download),
the script will extract it into ./data/ first, flatten any wrapper folder,
and then verify.
"""
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"

ONEDRIVE_URL = "https://acrocyte-my.sharepoint.com/:f:/p/adam_wang/IgCXUmqzRV_LSLsSd-3Sk4vxAcgxz7Wjbdi__ONE4YsWgvk?e=BnLejB"

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


def find_zip_in(directory: Path) -> Path | None:
    """Return the first *.zip file at the top of `directory`, if any."""
    if not directory.exists():
        return None
    for f in directory.iterdir():
        if f.is_file() and f.suffix.lower() == ".zip":
            return f
    return None


def find_zip() -> Path | None:
    return find_zip_in(HERE)


def relocate_misplaced_zip() -> None:
    """If the user accidentally dropped the OneDrive zip one level above
    working_directory/ (the repo root), move it down here."""
    if find_zip_in(HERE) is not None:
        return  # already in the right place
    parent_zip = find_zip_in(HERE.parent)
    if parent_zip is None:
        return
    target = HERE / parent_zip.name
    print(f"Found {parent_zip.name} in {HERE.parent.name}/, moving into {HERE.name}/ ...")
    parent_zip.rename(target)


def show_download_instructions() -> None:
    print("ERROR: no data and no .zip found.", file=sys.stderr)
    print(file=sys.stderr)
    print("Download the OneDrive bundle (ask the interviewer for the password):", file=sys.stderr)
    print(f"  {ONEDRIVE_URL}", file=sys.stderr)
    print(file=sys.stderr)
    print(f"Then move the downloaded .zip into {HERE} and re-run this script.", file=sys.stderr)


IGNORE_NAMES = {".DS_Store", "__MACOSX"}


def clean_macos_cruft(directory: Path) -> None:
    """Recursively remove __MACOSX folders and .DS_Store files left over from
    macOS-created zips."""
    import shutil
    for p in list(directory.rglob("__MACOSX")):
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
    for p in list(directory.rglob(".DS_Store")):
        if p.is_file():
            p.unlink(missing_ok=True)


def flatten_wrapper(directory: Path) -> None:
    """If `directory` contains exactly one subfolder (ignoring macOS cruft),
    move its contents up one level and remove the wrapper."""
    children = [p for p in directory.iterdir() if p.name not in IGNORE_NAMES]
    if len(children) == 1 and children[0].is_dir():
        wrapper = children[0]
        print(f"  Detected wrapper folder '{wrapper.name}', flattening...")
        for item in wrapper.iterdir():
            item.rename(directory / item.name)
        wrapper.rmdir()


def extract_inner_zips(directory: Path) -> None:
    """SharePoint folder downloads zip each subfolder separately, so after the
    outer zip we may end up with `data/old microscope.zip`, `data/new microscope.zip`,
    etc. Extract each in place, flatten any wrapper, and remove the zip.
    """
    inner = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".zip")
    for zp in inner:
        target = directory / zp.stem  # e.g. "old microscope.zip" -> "old microscope"
        print(f"  Extracting {zp.name} -> {target.name}/")
        target.mkdir(exist_ok=True)
        with zipfile.ZipFile(zp) as zf:
            zf.extractall(target)
        flatten_wrapper(target)
        zp.unlink()


def maybe_extract() -> None:
    """Handle two extraction stages:
    1. The outer OneDrive zip in working_directory/ (if present).
    2. Inner per-subfolder zips inside data/ (SharePoint bundles each
       subfolder as its own zip when you download a folder).
    """
    zip_path = find_zip()
    if zip_path is not None:
        print(f"Found {zip_path.name}, extracting into {DATA_DIR}/ ...")
        DATA_DIR.mkdir(exist_ok=True)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(DATA_DIR)
        flatten_wrapper(DATA_DIR)
        print(f"  (You can delete {zip_path.name} when ready.)")

    if DATA_DIR.exists():
        extract_inner_zips(DATA_DIR)
        clean_macos_cruft(DATA_DIR)
        # Belt-and-braces: also flatten any subfolder that ended up with
        # an internal wrapper (idempotent, safe to re-run).
        for sub in DATA_DIR.iterdir():
            if sub.is_dir() and sub.name not in IGNORE_NAMES:
                flatten_wrapper(sub)


def check_file(rel_path: str, full_path: Path, missing: list[str], found: list[str]) -> None:
    if not full_path.exists():
        missing.append(f"  - missing file: data/{rel_path}")
    else:
        size_mb = full_path.stat().st_size / (1 << 20)
        found.append(f"  - data/{rel_path} ({size_mb:.1f} MB)")


def main() -> None:
    relocate_misplaced_zip()
    maybe_extract()

    if not DATA_DIR.exists():
        show_download_instructions()
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
        print("❌ Data verification FAILED:", file=sys.stderr)
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

    print(f"✅ Data OK ({len(found)} files in {DATA_DIR}):")
    for line in found:
        print(line)


if __name__ == "__main__":
    main()

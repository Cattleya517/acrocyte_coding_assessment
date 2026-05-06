"""Download assessment data from OneDrive into ./data/.

Usage: uv run python download_data.py
"""
import sys
import zipfile
from pathlib import Path

import requests

# OneDrive share URL — REPLACE in Task 7 with the real share link.
# Format: a "anyone with link can view" share URL.
# The script appends ?download=1 (or &download=1 if there's already a query)
# to force a direct file download instead of the preview page.
DATA_URL = "REPLACE_ME_IN_TASK_7"

DATA_DIR = Path(__file__).parent / "data"
ZIP_PATH = DATA_DIR / "assessment_data.zip"


def to_direct_download(share_url: str) -> str:
    sep = "&" if "?" in share_url else "?"
    return f"{share_url}{sep}download=1"


def download(url: str, dest: Path) -> None:
    print(f"Downloading from {url}")
    with requests.get(url, stream=True, allow_redirects=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\r  {downloaded // (1<<20)} / {total // (1<<20)} MB ({pct}%)", end="")
        print()


def main() -> None:
    if DATA_URL == "REPLACE_ME_IN_TASK_7":
        print("ERROR: DATA_URL not configured. Edit download_data.py.", file=sys.stderr)
        sys.exit(1)

    if (DATA_DIR / "old microscope").exists() and (DATA_DIR / "new microscope").exists():
        print(f"Data already present in {DATA_DIR}. Skipping download.")
        return

    download(to_direct_download(DATA_URL), ZIP_PATH)

    print(f"Extracting to {DATA_DIR}")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(DATA_DIR)

    ZIP_PATH.unlink()
    print(f"Done. Data is in {DATA_DIR}")


if __name__ == "__main__":
    main()

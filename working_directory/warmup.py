"""Print a random LeetCode warmup URL.

Usage: uv run python warmup.py

The problem pool is read from `data/leetcode_pool.txt` (one URL per line,
blank lines and lines starting with '#' are ignored). That file ships in
the OneDrive download — run `verify_data.py` first if you don't have it.
"""
import random
import sys
import webbrowser
from pathlib import Path

POOL_FILE = Path(__file__).parent / "data" / "leetcode_pool.txt"


def load_pool() -> list[str]:
    if not POOL_FILE.exists():
        print(f"ERROR: {POOL_FILE} not found.", file=sys.stderr)
        print("Did you download and unzip the OneDrive data?", file=sys.stderr)
        print("Run: uv run python verify_data.py", file=sys.stderr)
        sys.exit(1)

    urls = []
    for line in POOL_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)

    if not urls:
        print(f"ERROR: {POOL_FILE} is empty.", file=sys.stderr)
        sys.exit(1)

    return urls


def main() -> None:
    pool = load_pool()
    url = random.choice(pool)
    print("Your warmup problem:")
    print(f"  {url}")
    print()
    print("Solve it on leetcode.com. AI assistance is NOT allowed for this part.")
    try:
        opened = webbrowser.open(url, new=2)
        if opened:
            print()
            print("(Opened in your default browser.)")
    except Exception:
        pass


if __name__ == "__main__":
    main()

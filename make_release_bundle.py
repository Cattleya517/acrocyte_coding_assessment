"""Build the password-protected data bundles for GitHub Releases (interviewer tooling).

Produces two AES-256 encrypted assets that candidates decrypt from inside Colab:

  * data_encrypted.zip          -- Part 2 image data (old/new microscope + cells csv,
                                   plus leetcode_pool.txt). Extracts to ./data/...
  * leetcode_pool_encrypted.zip -- Part 1 only: just leetcode_pool.txt (a few KB), so
                                   the warmup notebook doesn't download the ~600 MB
                                   image bundle. Extracts to ./leetcode_pool.txt

Both ciphertexts are safe to host publicly on GitHub Releases — without the password
they're useless. The same password is given to candidates verbally at interview time.

Usage (pyzipper is installed ephemerally, not added to the project):

    uv run --with pyzipper python make_release_bundle.py

Then upload as Release assets:

    gh release upload data-v1 data_encrypted.zip leetcode_pool_encrypted.zip \
        --repo Cattleya517/acrocyte_coding_assessment --clobber

To rotate the password later: re-run this script with a new password and re-upload
with --clobber. The notebooks don't change (they prompt for the password at runtime).
"""
import getpass
import sys
from pathlib import Path

import pyzipper

HERE = Path(__file__).parent
SRC = HERE / "working_directory" / "data"
DATA_OUT = HERE / "data_encrypted.zip"
POOL_OUT = HERE / "leetcode_pool_encrypted.zip"
POOL_NAME = "leetcode_pool.txt"
ARCROOT = "data"  # big-bundle entries are stored as data/<...> -> extract to ./data/


def encrypt_zip(out: Path, entries: list[tuple[Path, str]], password: bytes) -> None:
    """Write `entries` (src_path, arcname) into an AES-256 encrypted, deflated zip."""
    with pyzipper.AESZipFile(
        out, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(password)
        zf.setencryption(pyzipper.WZ_AES, nbits=256)
        for i, (src, arcname) in enumerate(entries, 1):
            zf.write(src, arcname=arcname)
            print(f"  [{i}/{len(entries)}] {arcname}")


def main() -> None:
    if not SRC.exists():
        sys.exit(
            f"ERROR: {SRC} not found.\n"
            "Stage the data there first (the three microscope/csv subfolders plus "
            "leetcode_pool.txt)."
        )
    files = sorted(p for p in SRC.rglob("*") if p.is_file() and p.name != ".DS_Store")
    if not files:
        sys.exit(f"ERROR: no files under {SRC}.")
    pool_src = SRC / POOL_NAME
    if not pool_src.exists():
        sys.exit(f"ERROR: {pool_src} not found (needed for the Part 1 pool asset).")

    total_mb = sum(f.stat().st_size for f in files) / (1 << 20)
    print(f"Found {len(files)} files under {SRC} ({total_mb:.0f} MB uncompressed).")

    pw1 = getpass.getpass("Set data password: ")
    pw2 = getpass.getpass("Confirm password:  ")
    if pw1 != pw2:
        sys.exit("ERROR: passwords do not match.")
    if not pw1:
        sys.exit("ERROR: empty password.")
    password = pw1.encode()

    print(f"\nEncrypting Part 2 bundle -> {DATA_OUT.name} ...")
    big_entries = [(f, f"{ARCROOT}/{f.relative_to(SRC).as_posix()}") for f in files]
    encrypt_zip(DATA_OUT, big_entries, password)

    print(f"\nEncrypting Part 1 pool -> {POOL_OUT.name} ...")
    encrypt_zip(POOL_OUT, [(pool_src, POOL_NAME)], password)

    big_mb = DATA_OUT.stat().st_size / (1 << 20)
    pool_kb = POOL_OUT.stat().st_size / 1024
    print(f"\nDone:")
    print(f"  {DATA_OUT}  ({big_mb:.0f} MB)")
    print(f"  {POOL_OUT}  ({pool_kb:.1f} KB)")
    print("Next: upload both as GitHub Release assets (see this file's docstring).")


if __name__ == "__main__":
    main()

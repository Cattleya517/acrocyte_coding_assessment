"""Build the password-protected data bundle for GitHub Releases (interviewer tooling).

This packs `working_directory/data/` into a single AES-256 encrypted zip that
candidates download + decrypt from inside Colab (see working_directory/notebook_colab.ipynb).

The ciphertext is safe to host publicly on GitHub Releases — without the password
it's useless. The password is given to candidates verbally at interview time.

Usage (pyzipper is installed ephemerally, not added to the project):

    uv run --with pyzipper python make_release_bundle.py

Then upload the result as a Release asset:

    gh release create data-v1 data_encrypted.zip \
        --repo Cattleya517/acrocyte_coding_assessment \
        --title "Assessment data v1" \
        --notes "Encrypted Part 2 image data. Password provided at interview."

To rotate the password later: re-run this script with a new password and
`gh release upload data-v1 data_encrypted.zip --clobber`.
"""
import getpass
import sys
from pathlib import Path

import pyzipper

HERE = Path(__file__).parent
SRC = HERE / "working_directory" / "data"
OUT = HERE / "data_encrypted.zip"
ARCROOT = "data"  # entries are stored as data/<...> so they extract to ./data/


def collect_files(src: Path) -> list[Path]:
    if not src.exists():
        sys.exit(
            f"ERROR: {src} not found.\n"
            "Stage the data there first (extract the three OneDrive subfolder zips "
            "into working_directory/data/ as 'old microscope/', 'new microscope/', "
            "'cells csv/')."
        )
    files = sorted(p for p in src.rglob("*") if p.is_file() and p.name != ".DS_Store")
    if not files:
        sys.exit(f"ERROR: no files under {src}.")
    return files


def main() -> None:
    files = collect_files(SRC)
    total_mb = sum(f.stat().st_size for f in files) / (1 << 20)
    print(f"Found {len(files)} files under {SRC} ({total_mb:.0f} MB uncompressed).")

    pw1 = getpass.getpass("Set data password: ")
    pw2 = getpass.getpass("Confirm password:  ")
    if pw1 != pw2:
        sys.exit("ERROR: passwords do not match.")
    if not pw1:
        sys.exit("ERROR: empty password.")
    password = pw1.encode()

    print(f"Encrypting (AES-256, deflate) -> {OUT.name} ...")
    with pyzipper.AESZipFile(
        OUT, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(password)
        zf.setencryption(pyzipper.WZ_AES, nbits=256)
        for i, f in enumerate(files, 1):
            arcname = f"{ARCROOT}/{f.relative_to(SRC).as_posix()}"
            zf.write(f, arcname=arcname)
            print(f"  [{i}/{len(files)}] {arcname}")

    out_mb = OUT.stat().st_size / (1 << 20)
    print(f"\nDone: {OUT} ({out_mb:.0f} MB)")
    print("Next: upload as a GitHub Release asset (see this file's docstring).")


if __name__ == "__main__":
    main()

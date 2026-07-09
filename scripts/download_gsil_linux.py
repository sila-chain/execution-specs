#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests"]
# ///
"""
Helper script to download gsil for Linux.
"""

import argparse
import os
import shutil
import tarfile

import requests


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir", help="Directory to which gsil binary will be downloaded to"
    )

    return parser.parse_args()


def download_gsil_linux(target_dir: str) -> None:
    """Download gsil from windows.net."""
    gsil_release_name = "gsil-linux-amd64-1.10.8-26675454"
    url = (
        f"https://gsilstore.blob.core.windows.net/builds/"
        f"{gsil_release_name}.tar.gz"
    )
    r = requests.get(url)

    with open(f"{target_dir}/gsil.tar.gz", "wb") as f:
        f.write(r.content)

    gsil_tar = tarfile.open(f"{target_dir}/gsil.tar.gz")
    gsil_tar.extractall(target_dir)

    shutil.move(f"{target_dir}/{gsil_release_name}/gsil", target_dir)
    shutil.rmtree(f"{target_dir}/{gsil_release_name}", ignore_errors=True)
    os.remove(f"{target_dir}/gsil.tar.gz")


if __name__ == "__main__":
    args = parse_args()
    download_gsil_linux(args.dir)

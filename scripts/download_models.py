#!/usr/bin/env python3
"""Download HuggingFace models listed in a manifest into a target directory.

Usage:
    python download_models.py <manifest.txt> <target_dir>

Manifest format: one HF repo ID per line. `#` comments and blank lines ignored.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from huggingface_hub import snapshot_download


def parse_manifest(path: Path) -> list[str]:
    repos: list[str] = []
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            repos.append(line)
    return repos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to manifest file")
    parser.add_argument("target", type=Path, help="Directory to write model snapshots into")
    args = parser.parse_args()

    if not args.manifest.is_file():
        print(f"error: manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    repos = parse_manifest(args.manifest)
    if not repos:
        print(f"error: manifest {args.manifest} has no models", file=sys.stderr)
        return 1

    args.target.mkdir(parents=True, exist_ok=True)
    for repo_id in repos:
        print(f"Downloading {repo_id}...", flush=True)
        snapshot_download(repo_id=repo_id, local_dir=args.target / repo_id)
    print(f"Done. {len(repos)} model(s) in {args.target}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Resolve a registered asset id to its source repository + immutable reference.

Usage:
  python scripts/resolve.py <asset-id>            # print the resolution
  python scripts/resolve.py <asset-id> --check    # also verify tag refs via git ls-remote

Commit-SHA and digest references cannot be verified by ls-remote (which lists
refs, not object reachability); --check verifies tag references only and says
so for the other kinds.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TAG_RE = re.compile(r"^v\d+\.\d+\.\d+(-[a-z0-9.-]+)?$")


def find_record(asset_id: str) -> tuple[Path, dict]:
    for base in (ROOT / "registry", ROOT / "examples"):
        for path in sorted(base.rglob("*.yaml")):
            doc = yaml.safe_load(path.read_text())
            if isinstance(doc, dict) and doc.get("id") == asset_id:
                return path, doc
    raise SystemExit(f"FAIL — asset id {asset_id!r} is not registered")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("asset_id")
    ap.add_argument("--check", action="store_true", help="verify tag reference via git ls-remote")
    args = ap.parse_args()

    path, doc = find_record(args.asset_id)
    src = doc["source"]
    rel = doc["release"]
    repo_url = f"https://github.com/{src['organization']}/{src['repository']}"
    print(f"asset:      {doc['id']} ({doc['type']}, status={doc['status']})")
    print(f"record:     {path.relative_to(ROOT)}")
    print(f"source:     {repo_url}")
    print(f"version:    {rel['version']}")
    print(f"reference:  {rel['reference']}")
    print(f"conformsTo: {doc['conformsTo']['contract']['id']} @ {doc['conformsTo']['contract']['version']}")

    if not args.check:
        return 0

    ref = rel["reference"]
    if not TAG_RE.match(ref):
        print(f"check:      SKIP — {ref!r} is a commit/digest reference; "
              "ls-remote verifies tags only")
        return 0
    out = subprocess.run(
        ["git", "ls-remote", repo_url, f"refs/tags/{ref}"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        print(f"check:      FAIL — ls-remote error: {out.stderr.strip()}")
        return 1
    if not out.stdout.strip():
        print(f"check:      FAIL — tag {ref!r} not found on {repo_url}")
        return 1
    print(f"check:      OK — tag {ref} resolves on {repo_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

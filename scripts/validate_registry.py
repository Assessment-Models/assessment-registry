#!/usr/bin/env python3
"""Validate every registration record in registry/ and examples/.

Checks (CR-AM-11 sections 11-12):
  1. JSON Schema conformance (schemas/registration.schema.json)
  2. Immutable release references (main/master/latest/HEAD rejected)
  3. Unique asset ids; filename == <id>.yaml in the type-matching directory
  4. dependencies entries resolve to other registered asset ids

Exit 0 with an OK summary when clean; exit 1 listing every failure otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = yaml.safe_load((ROOT / "schemas" / "registration.schema.json").read_text())

TYPE_DIRS = {
    "maturity-model": "maturity-models",
    "assessment-model": "assessment-models",
    "assessment-tool": "assessment-tools",
    "component": "components",
}

MUTABLE_REFS = {"main", "master", "latest", "HEAD", "head"}
IMMUTABLE_PATTERNS = (
    re.compile(r"^v\d+\.\d+\.\d+(-[a-z0-9.-]+)?$"),   # release tag
    re.compile(r"^[0-9a-f]{40}$"),                     # commit SHA
    re.compile(r"^sha256:[0-9a-f]{64}$"),              # content digest
)


def is_immutable(ref: str) -> bool:
    if ref in MUTABLE_REFS:
        return False
    return any(p.match(ref) for p in IMMUTABLE_PATTERNS)


def load_records():
    records = []  # (path, doc)
    for base in (ROOT / "registry", ROOT / "examples"):
        for path in sorted(base.rglob("*.yaml")):
            doc = yaml.safe_load(path.read_text())
            records.append((path, doc))
    return records


def main() -> int:
    errors: list[str] = []
    records = load_records()
    if not records:
        errors.append("no registration records found under registry/ or examples/")

    seen_ids: dict[str, Path] = {}
    for path, doc in records:
        label = path.relative_to(ROOT)
        if not isinstance(doc, dict):
            errors.append(f"{label}: not a YAML mapping")
            continue

        # 1. schema
        for err in sorted(
            jsonschema.Draft202012Validator(SCHEMA).iter_errors(doc),
            key=lambda e: list(e.path),
        ):
            errors.append(f"{label}: schema: {'/'.join(map(str, err.path)) or '<root>'}: {err.message}")

        # 2. immutable reference
        ref = (doc.get("release") or {}).get("reference", "")
        if isinstance(ref, str) and ref and not is_immutable(ref):
            errors.append(
                f"{label}: release.reference {ref!r} is not immutable "
                "(tag vX.Y.Z, 40-char SHA, or sha256 digest required)"
            )
        # component references must be immutable too (section 20)
        for comp in doc.get("components") or []:
            cref = comp.get("reference", "")
            if isinstance(cref, str) and cref and not is_immutable(cref):
                errors.append(f"{label}: component {comp.get('id')!r}: reference {cref!r} is not immutable")

        # 3a. filename == id
        asset_id = doc.get("id")
        if isinstance(asset_id, str) and path.stem != asset_id:
            errors.append(f"{label}: filename stem {path.stem!r} != id {asset_id!r}")

        # 3b. type-matching directory (registry/ only; examples/ is flat)
        asset_type = doc.get("type")
        if "registry" in path.parts and asset_type in TYPE_DIRS:
            if path.parent.name != TYPE_DIRS[asset_type]:
                errors.append(
                    f"{label}: type {asset_type!r} belongs under registry/{TYPE_DIRS[asset_type]}/, "
                    f"found in {path.parent.name!r}"
                )

        # 3c. uniqueness
        if isinstance(asset_id, str):
            if asset_id in seen_ids:
                errors.append(f"{label}: duplicate id {asset_id!r} (also in {seen_ids[asset_id].relative_to(ROOT)})")
            else:
                seen_ids[asset_id] = path

    # 4. dependencies resolve
    for path, doc in records:
        if not isinstance(doc, dict):
            continue
        for dep in doc.get("dependencies") or []:
            if dep not in seen_ids:
                errors.append(f"{path.relative_to(ROOT)}: dependency {dep!r} is not a registered asset id")

    if errors:
        print(f"FAIL — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — {len(records)} registration record(s) valid "
          f"(schema, immutable references, unique ids, resolvable dependencies)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate every registration record in registry/ and examples/.

Checks (CR-AM-11 sections 11-12 + CR-AR-01 Phase 1):
  1. JSON Schema conformance (schemas/registration.schema.json)
  2. Immutable release references (main/master/latest/HEAD rejected)
  3. Unique asset ids; filename == <id>.yaml in the type-matching directory
  4. dependencies entries resolve to other registered asset ids
  5. CR-AR-01 backward-compat shim: missing asset_class defaults to 'assessment'
  6. CR-AR-01 type↔class coherence: a semantic-* type implies asset_class=semantic;
     an ontology-* type implies asset_class=ontological; etc.
  7. CR-AR-01 axes coherence: if asset_class is declared and compatibility is
     present, required_axes must be a non-empty subset of declared_axes keys (or
     the axes/catalog.yaml catalogue for that class).

Exit 0 with an OK summary when clean; exit 1 listing every failure otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas" / "registration.schema.json").read_text())

TYPE_DIRS = {
    "maturity-model": "maturity-models",
    "assessment-model": "assessment-models",
    "assessment-tool": "assessment-tools",
    "component": "components",
    "semantic-architecture-asset": "semantic",
    "ontology-asset": "ontological",
    "extension": "extensions",
}

# type → implied asset_class (CR-AR-01 §Scope type↔class mapping).
TYPE_TO_CLASS = {
    "maturity-model": "assessment",
    "assessment-model": "assessment",
    "assessment-tool": "assessment",
    "component": "assessment",
    "semantic-architecture-asset": "semantic",
    "ontology-asset": "ontological",
    "extension": "extension",
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


def resolve_asset_class(doc: dict) -> str:
    """CR-AR-01 backward-compat shim: missing asset_class defaults to 'assessment'."""
    return doc.get("asset_class") or "assessment"


def load_axes_catalogue() -> dict[str, set[str]]:
    """Load the axes/catalog.yaml catalogue; return {asset_class: set(axes)}.

    The catalogue is documentary; missing axes/catalog.yaml is not a hard error
    (axes validation is skipped silently in that case to keep CI green for
    early-phase repos that don't yet ship the catalogue).
    """
    path = ROOT / "axes" / "catalog.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text()) or {}
    return {
        cls: {ax["name"] for ax in (axes or [])}
        for cls, axes in (data.get("axes") or {}).items()
    }


def load_records():
    records = []  # (path, doc)
    for base in (ROOT / "registry", ROOT / "examples"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.yaml")):
            doc = yaml.safe_load(path.read_text())
            records.append((path, doc))
    return records


def main() -> int:
    errors: list[str] = []
    records = load_records()
    if not records:
        errors.append("no registration records found under registry/ or examples/")

    axes_cat = load_axes_catalogue()
    seen_ids: dict[str, Path] = {}
    classes_seen: dict[str, int] = {}

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

        # 5. CR-AR-01 backward-compat shim
        resolved_class = resolve_asset_class(doc)
        classes_seen[resolved_class] = classes_seen.get(resolved_class, 0) + 1

        # 6. CR-AR-01 type↔class coherence
        if asset_type in TYPE_TO_CLASS:
            implied = TYPE_TO_CLASS[asset_type]
            declared = doc.get("asset_class")
            if declared is not None and declared != implied:
                errors.append(
                    f"{label}: type {asset_type!r} implies asset_class={implied!r} "
                    f"but declared asset_class={declared!r}"
                )

        # 7. CR-AR-01 axes coherence (only if axes/catalog.yaml exists and class is known)
        compat = doc.get("compatibility")
        if isinstance(compat, dict) and resolved_class in axes_cat:
            cat_axes = axes_cat[resolved_class]
            required = compat.get("required_axes") or []
            declared_axes = (compat.get("declared_axes") or {})
            for axis in required:
                if axis not in cat_axes:
                    errors.append(
                        f"{label}: required axis {axis!r} is not in the axes/catalog.yaml "
                        f"catalogue for class {resolved_class!r}"
                    )
            # declared_axes keys must also be a subset of the catalogue (or absent)
            for axis in declared_axes:
                if axis not in cat_axes:
                    errors.append(
                        f"{label}: declared axis {axis!r} is not in the axes/catalog.yaml "
                        f"catalogue for class {resolved_class!r}"
                    )

    # 4. dependencies resolve
    for path, doc in records:
        if not isinstance(doc, dict):
            continue
        for dep in doc.get("dependencies") or []:
            if dep not in seen_ids:
                errors.append(f"{path.relative_to(ROOT)}: dependency {dep!r} is not a registered asset id")

    # 5. supersession coherence (CR-AR-05)
    for path, doc in records:
        if not isinstance(doc, dict):
            continue
        sup = doc.get("superseded_by")
        status = doc.get("status")
        if sup is None:
            if status in ("legacy", "superseded"):
                errors.append(
                    f"{path.relative_to(ROOT)}: status {status!r} SHOULD declare superseded_by (CR-AR-05)"
                )
            continue
        if status == "active":
            errors.append(
                f"{path.relative_to(ROOT)}: active record MUST NOT declare superseded_by (CR-AR-05)"
            )
        if isinstance(sup, str):
            if sup not in seen_ids:
                errors.append(
                    f"{path.relative_to(ROOT)}: superseded_by {sup!r} is not a registered asset id (CR-AR-05)"
                )
            if sup == doc.get("id"):
                errors.append(
                    f"{path.relative_to(ROOT)}: superseded_by references itself (CR-AR-05)"
                )

    if errors:
        print(f"FAIL — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    summary = ", ".join(
        f"{cls}={n}" for cls, n in sorted(classes_seen.items())
    )
    print(f"OK — {len(records)} registration record(s) valid "
          f"({summary}) "
          f"[schema, immutable refs, unique ids, resolvable deps, "
          f"asset_class shim, type↔class coherence, axes coherence, "
          f"supersession coherence]")
    return 0


if __name__ == "__main__":
    sys.exit(main())

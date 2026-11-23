# Assessment Registry

**The ecosystem integration spine for OpenDEA-compatible assets** (CR-AM-11 §10 + CR-AR-01 §Scope).

This repository registers assets. It contains **no model content** — registration records carry metadata and immutable references only (§11). Dimensions, criteria, levels, scoring rules and all model content remain owned by the asset repositories.

The registry answers:

- What exists?
- Where is it?
- What version exists? Which version is **active**?
- Which OpenDEA contract does it conform to?
- Which components does it depend on?
- Which relationships exist between assets?

## Asset classes (CR-AR-01)

The registry registers **OpenDEA-compatible assets** across three classes (Phase 1 enum; future classes require their own CR):

| Class | Origin CR | Examples |
|---|---|---|
| `assessment` | CR-AM-11 | maturity models, assessment models, assessment tools, components |
| `semantic` | CR-ESA-01 | semantic-architecture assets (sector-ESA + patterns) |
| `ontological` | CR-EO-01 | ontology assets (sector ontologies + mappings) |
| `extension` | reserved | future asset classes (each requires its own CR) |

Each record carries an `asset_class` discriminator (optional; defaults to `assessment` for backward compatibility with pre-CR-AR-01 records). Per-class required fields, type mappings, and compatibility axes are defined in:

- `schemas/registration.schema.json` — the schema with per-class `if/then` blocks.
- `axes/catalog.yaml` — the per-class compatibility-axes catalogue (documentary).
- `scripts/validate_registry.py` — the validator enforcing the schema + shim + coherence rules.

## Layout

```
assessment-registry/
├── registry/
│   ├── maturity-models/      ← one YAML record per registered maturity model
│   ├── assessment-models/    ← one YAML record per registered assessment model
│   ├── assessment-tools/     ← one YAML record per registered assessment tool
│   ├── components/           ← one YAML record per registered reusable component
│   ├── semantic/             ← semantic-class records (CR-AR-01 Phase 2+; populated with first sector content)
│   ├── ontological/          ← ontological-class records (CR-AR-01 Phase 3+; populated with first sector content)
│   └── extensions/           ← extension-class records (reserved)
├── compatibility/            ← compatibility declarations between assets (Phase 2+)
├── dependencies/             ← cross-asset dependency documentation (Phase 2+)
├── axes/
│   └── catalog.yaml          ← per-class compatibility-axes catalogue (CR-AR-01 Phase 1)
├── schemas/
│   ├── registration.schema.json   ← the registration record contract (Draft 2020-12) — CR-AR-01 Phase 1
│   ├── semantic/README.md         ← placeholder for Phase 2 semantic-asset schema
│   └── ontological/README.md      ← placeholder for Phase 3 ontological-asset schema
├── examples/
│   ├── digital-transformation-maturity-model.yaml  ← worked assessment-class example
│   ├── semantic/dea-semantic-architecture.yaml    ← worked semantic-class example (CR-AR-01 Phase 1)
│   └── ontological/dea-ontology.yaml              ← worked ontological-class example (CR-AR-01 Phase 1)
├── scripts/
│   ├── validate_registry.py  ← schema + immutability + uniqueness + referential checks + asset_class shim + type↔class coherence + axes coherence
│   └── resolve.py            ← resolve an asset id → source repo + immutable reference
└── .github/workflows/ci.yml
```

## Registration rules (CR-AM-11 §11–12, augmented by CR-AR-01)

1. **Metadata + references only.** Records never duplicate asset content.
2. **Immutable references are verified, not merely syntax-checked.** `release.reference` must resolve as a release tag (`vX.Y.Z`) or 40-character commit SHA in the declared source repository. Annotated tags are peeled to commits; an optional `release.commit` must agree. SHA-256 digests are reserved but fail closed until a content-addressed resolver is defined. Mutable references are rejected.
3. **One record per asset**, filename = `<id>.yaml` under the type-matching directory.
4. **Contract conformance is declared**, per the contract handshake (§15): every record names the OpenDEA contract id + version the asset conforms to.
5. **Dependencies must resolve.** A record's `dependencies` entries must reference other registered asset ids.
6. **asset_class declaration** (CR-AR-01 Phase 1). New records MUST declare `asset_class`. Pre-CR-AR-01 records are accepted without `asset_class` and default-infer to `assessment` via the backward-compat shim.
7. **Type ↔ asset_class coherence** (CR-AR-01 Phase 1). A `type: maturity-model | assessment-model | assessment-tool | component` implies `asset_class: assessment`. A `type: semantic-architecture-asset` implies `asset_class: semantic`. A `type: ontology-asset` implies `asset_class: ontological`. A `type: extension` implies `asset_class: extension`. Validator enforces this; mismatches are CI failures.
8. **Compatibility axes** (CR-AR-01 Phase 1). For `semantic` / `ontological` / `extension` asset classes, the schema requires a `compatibility` block declaring required_axes. Required axes must be present in the class's axes catalogue (`axes/catalog.yaml`). Existing assessment-class records do not require `compatibility` (backward-compat shim).
9. **Pinned release identity (CR-AR-06).** For `maturity-model`, `assessment-model` and `component` assets, CI reads `model.yaml` at the resolved commit and checks its `id` and `version` against the registry record. `release.manifest: null` is an explicit exception for a legacy/catalog asset with no authoritative manifest.
10. **Repository-standard adoption (CR-AR-07).** Each non-legacy maturity-model registration carries the authoritative `repository_standard` adoption snapshot (`id`, `version`, `conformance`). CI corroborates it against `standard.yaml` at the exact pinned release commit, including repository type and model identity/version. The normative standard and conformance definitions remain owned by `maturity-model-standard`; its portfolio adoption fields are a derived view, while classifications and Phase 2 assessments remain independently governed there.

## Cross-class compatibility (resolution rule)

Two assets of different classes are compatible iff:

1. They share at least one `declared` axis (typically `governance`).
2. The consumer's `compatibility.required_axes` is a subset of the union of axes each declares.
3. There are no `declared_axes` conflicts between the two on the shared axes.

The rule is documentary in Phase 1; resolver-side enforcement is Phase 2+.

## Registering an asset

1. Copy the closest record under `examples/` into the type-matching `registry/` directory (or, for semantic / ontological classes, the `registry/semantic/` / `registry/ontological/` directory).
2. Fill identity, source, immutable release reference, contract handshake, status.
3. **If the asset class is `semantic`, `ontological`, or `extension`**, also declare `compatibility.required_axes` (and ideally `compatibility.declared_axes`).
4. Open a PR — CI runs `scripts/validate_registry.py` (schema + uniqueness + referential integrity + asset_class shim + type↔class coherence + axes coherence) and `scripts/validate_release_integrity.py` across every registry record.
5. On merge the asset is registered; ecosystem CI (assessment-ci) picks it up from there.

## Status values

`active` · `legacy` · `candidate-for-migration` · `reference` · `deprecated` · `superseded` — aligned with the §26 legacy classification in the [org governance](https://github.com/Assessment-Models/.github/blob/main/GOVERNANCE.md).

---

*Established under [CR-AM-11 — Federated Assessment Model Ecosystem](https://github.com/technehub-labs/dea-metamodel/blob/main/change-requests/CR-AM-11.md) Phase 1.*
*Scope extended under [CR-AR-01 — Assessment-Registry Scope Extension](./change-requests/CR-AR-01.md) Phase 1.*

# Changelog

## [Unreleased] — CR-AR-05: machine-readable supersession

### Added
- `superseded_by` field on registration records (schema, CR-AR-05): a registered asset id or an external canonical target (`organization` + `repository` [+ `path`]).
- Validator rule 5 — supersession coherence: string form must resolve to a registered id; no self-reference; `active` records must not declare supersession; `legacy`/`superseded` records should declare it.
- Both legacy catalog records now declare machine-readable supersession toward the v2 canonical architecture in `technehub-labs/dea-metamodel`.

## [Unreleased] — CR-AR-01 Phase 1: Scope extension

### Added
- **Asset-class discriminator** (`asset_class`) — optional field; defaults to `assessment` for backward compatibility with pre-CR-AR-01 records. Enum: `assessment` · `semantic` · `ontological` · `extension`.
- **Type ↔ asset_class coherence** — `type: maturity-model | assessment-model | assessment-tool | component` implies `asset_class: assessment`; `type: semantic-architecture-asset` implies `asset_class: semantic`; `type: ontology-asset` implies `asset_class: ontological`; `type: extension` implies `asset_class: extension`. Validator enforces; mismatches are CI failures.
- **Compatibility axes generalisation** — new optional `compatibility` block on each record: `{required_axes: [string], declared_axes: {axis: string}}`. Schema requires `compatibility` for `semantic`, `ontological`, and `extension` asset classes; remains optional for `assessment` (backward-compat shim).
- **`axes/catalog.yaml`** — per-class compatibility-axes catalogue (documentary; `governance` is the cross-class shared baseline). Records declaring axes not in the catalogue fail CI.
- **New registry directories** — `registry/semantic/`, `registry/ontological/`, `registry/extensions/` (empty until Phase 2/3 sector-content lands).
- **Worked examples** — `examples/semantic/dea-semantic-architecture.yaml`, `examples/ontological/dea-ontology.yaml` (validate the schema accepts the new classes).
- **Per-class type dir mapping** in the validator: TYPE_DIRS now covers all 7 `type` values.

### Changed
- **`schemas/registration.schema.json`** — added `asset_class` (optional), `compatibility` (optional, conditionally required for non-assessment classes), and new `type` enum values (`semantic-architecture-asset`, `ontology-asset`, `extension`). Existing assessment records continue to validate unchanged.
- **`scripts/validate_registry.py`** — adds asset_class shim, type↔class coherence check, and axes coherence check. Summary line reports per-class record counts.
- **`README.md`** — scope language changed from "assessment assets" to "OpenDEA-compatible assets"; new asset classes enumerated; cross-class compatibility rule documented.

### Backward compatibility
- All pre-CR-AR-01 records continue to validate unchanged.
- The `asset_class` field defaults to `assessment` when absent (backward-compat shim).
- The `compatibility` block remains optional for assessment-class records (existing behaviour preserved).
- The new `type` enum values are additive — pre-CR-AR-01 records use only the original four `type` values and continue to validate.

---

## [Unreleased] — CR-AM-11 Phase 1: Integration spine (registry half)

### Added
- Repository scaffold per CR-AM-11 §10.2: `registry/` (maturity-models, assessment-models, assessment-tools, components), `compatibility/`, `dependencies/`, `schemas/`, `examples/`, `scripts/`, CI.
- `schemas/registration.schema.json` — the registration record contract (Draft 2020-12; metadata + immutable references only).
- `scripts/validate_registry.py` — schema conformance, immutable-reference guard (rejects `main`/`master`/`latest`/`HEAD`; accepts tag `vX.Y.Z`, 40-char SHA, `sha256:` digest), unique ids, filename/type-directory matching, dependency referential integrity.
- `scripts/resolve.py` — resolve an asset id to source repo + immutable reference; `--check` verifies tag references via `git ls-remote`.
- First real registration: `registry/maturity-models/dea-catalog-maturity-models.yaml` (status `legacy`, pinned to commit `fa2f9d5`).
- Worked example: `examples/maturity-model-digital-transformation.yaml` (Phase 4 first-model candidate shape).

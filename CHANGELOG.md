## [Unreleased] — CR-AR-06 immutable release integrity

### Added
- `scripts/validate_release_integrity.py`: resolves every registry tag or commit SHA, peels annotated tags, cross-checks commit claims, and validates authoritative manifests at the pinned commit.
- `tests/test_release_integrity.py`: positive and negative Git-reference and manifest-identity tests.
- `change-requests/CR-AR-06.md`: normative requirements and acceptance criteria.

### Changed
- Registration schema adds optional `release.manifest` path/null override; SHA-256 references are reserved but not treated as verified Git references.
- Legacy maturity catalogue explicitly declares `release.manifest: null`.
- Registry CI runs release-integrity validation and its test suite on pull requests and main pushes.
- README documents immutable resolution and pinned-manifest verification.

### Governance
- Repository-standard adoption remains authoritative in `maturity-model-standard/registry/conformance.yaml`; no duplicate adoption state is introduced here.

## [Unreleased] — reconcile current maturity-model release pins

### Changed

- `registry/maturity-models/maturity-model-autonomous-operations.yaml`: advance the active registration from 2.0.0 to 2.0.1 and pin it to the verified immutable source commit `75795a1e23e90edcfa268737e511fa16fcfc18eb`. Clarify that the registered release contains touchpoints v0.1.1-draft, while later v0.1.2-draft reconciliation on the source default branch is not part of that release snapshot.
- `registry/maturity-models/maturity-model-operations.yaml`: advance the active registration from 2.0.0 to 2.1.1 and pin it to the verified immutable source commit `c6da76d5f3db1f9a70dac3b0cfabdc74f4894094`. Replace the non-resolving `v2.0.0` tag reference with the commit SHA, and distinguish the release-pinned v0.2.2-draft touchpoint artifact from the later v0.2.3-draft default-branch state.
- No tags are created and no touchpoint contract or relationship semantics are promoted by this registry update.

# Changelog

## [Unreleased] — register maturity-model-digital-transformation v1.1.0-alpha

### Changed
- `registry/maturity-models/maturity-model-digital-transformation.yaml`: release bumped to
  `1.1.0-alpha`, immutable reference = PR #6 merge commit `616f5c53bb52cedfce6635511f1674f90a6c1f1c`
  (switch to the `v1.1.0-alpha` tag when created). Description/notes now cover the additive
  operationalized model line (`maturity/operationalized/`, 6/23/70 criteria, canonical L-0..L-4
  scale correlated to the composite scale). Validated against registration.schema.json.

## [Unreleased] — CR-AM-11 Phase 5: component reuse across models

### Changed

- `registry/maturity-models/maturity-model-digital-transformation.yaml`:
  release reference is now the immutable `v1.0.0` tag (peels to the previously
  registered commit 1e1a16d…), and the four component references point at the
  `v1.0.0` release of `Assessment-Models/maturity-components` instead of a
  placeholder SHA (§12/§20 immutable references).
- `registry/maturity-models/maturity-model-operations.yaml`: declares reuse of
  the `operations-modernization` component (v1.0.0 @ v1.0.0). With
  maturity-model-digital-transformation, this makes `operations-modernization`
  the first component reused by two independently versioned models — the
  CR-AM-11 Phase 5 exit criterion.

## [Unreleased] — CR-AR-05 follow-up: supersession resolution

### Added
- `scripts/resolve.py` surfaces `superseded_by` on resolution output: registered-asset form prints the transitive supersession chain (cycle-safe); external canonical target form prints `organization/repository (path)`. Active assets print nothing — the field is absent by schema coherence.

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

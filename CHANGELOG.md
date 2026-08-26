# Changelog

## [Unreleased] — CR-AM-11 Phase 1: Integration spine (registry half)

### Added
- Repository scaffold per CR-AM-11 §10.2: `registry/` (maturity-models, assessment-models, assessment-tools, components), `compatibility/`, `dependencies/`, `schemas/`, `examples/`, `scripts/`, CI.
- `schemas/registration.schema.json` — the registration record contract (Draft 2020-12; metadata + immutable references only).
- `scripts/validate_registry.py` — schema conformance, immutable-reference guard (rejects `main`/`master`/`latest`/`HEAD`; accepts tag `vX.Y.Z`, 40-char SHA, `sha256:` digest), unique ids, filename/type-directory matching, dependency referential integrity.
- `scripts/resolve.py` — resolve an asset id to source repo + immutable reference; `--check` verifies tag references via `git ls-remote`.
- First real registration: `registry/maturity-models/dea-catalog-maturity-models.yaml` (status `legacy`, pinned to commit `fa2f9d5`).
- Worked example: `examples/maturity-model-digital-transformation.yaml` (Phase 4 first-model candidate shape).

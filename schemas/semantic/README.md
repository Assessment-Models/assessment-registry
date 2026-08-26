# Semantic-asset registration schema

> **Status:** placeholder. Full schema lands in Phase 2 of [CR-AR-01](../change-requests/CR-AR-01.md) (lands alongside CR-ESA-01 Phase 2 telecom operator sector content).

This directory will hold the semantic-asset registration record contract — JSON Schema + worked examples — for assets whose `asset_class` is `semantic` (per CR-AR-01 Phase 1 discriminator).

## Phase 2 deliverable targets

- `registration-semantic.schema.json` — the schema.
- `examples/` — at least one worked example from the CR-ESA-01 Phase 2 telecom operator sector.
- CI integration: `scripts/validate_registry.py` extended to validate `asset_class: semantic` entries.
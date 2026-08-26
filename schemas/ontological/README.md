# Ontological-asset registration schema

> **Status:** placeholder. Full schema lands in Phase 3 of [CR-AR-01](../change-requests/CR-AR-01.md) (lands alongside CR-EO-01 Phase 2 telecom operator sector content).

This directory will hold the ontological-asset registration record contract — JSON Schema + worked examples — for assets whose `asset_class` is `ontological` (per CR-AR-01 Phase 1 discriminator).

## Phase 3 deliverable targets

- `registration-ontological.schema.json` — the schema.
- `examples/` — at least one worked example from the CR-EO-01 Phase 2 telecom operator sector; second example from the `dea-catalog-ontologies` promotion (Phase 4 of CR-EO-01).
- CI integration: `scripts/validate_registry.py` extended to validate `asset_class: ontological` entries.
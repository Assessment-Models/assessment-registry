# Cross-Reference: CR-AR-01 ↔ CR-EO-01 (dea-ontology)

> **Status:** cross-reference stub — full content lands in Phase 3 of [CR-AR-01](./CR-AR-01.md) (ontological-asset registration schema, lands alongside CR-EO-01 Phase 2 sector content).

This is a **cross-reference** file documenting the relationship between CR-AR-01 (registry scope extension) and CR-EO-01 (Enterprise Ontology).

## Primary CRs

- The full CR-AR-01 lives at: [`change-requests/CR-AR-01.md`](./CR-AR-01.md) in this repo.
- The full CR-EO-01 lives at: `https://github.com/technehub-labs/dea-ontology/blob/main/change-requests/CR-EO-01.md`.

## Sections of CR-AR-01 that affect CR-EO-01

| CR-AR-01 § | Effect on CR-EO-01 / dea-ontology |
|---|---|
| §Scope | EO outputs (ontological assets) will register through this registry once CR-AR-01 Phase 1 lands (discriminator + axes generalisation). |
| §Boundaries with sibling CRs | EO is a sibling of AR; EO's first sector-content PRs (Phase 2) carry `registry-entry.yaml` files that exercise AR-01's discriminator (`asset_class: ontological`). |
| §Phase plan Phase 3 | Ontological-asset registration schema ships alongside CR-EO-01 Phase 2 (telecom operator sector). |
| §Phase plan Phase 4 | Cloud service provider sector registration (ontological class) lands alongside CR-EO-01 Phase 3. |
| §Risks §3 | Cross-repo landing race is mitigated by forward-pointing cross-refs. |

## Sections of CR-EO-01 that affect CR-AR-01

| CR-EO-01 § | Effect on CR-AR-01 |
|---|---|
| §Boundaries with sibling CRs | EO's `registry-manifest.yaml` declares forward-compatible registration through AR; activation waits on CR-AR-01 Phase 1. |
| §Phase plan Phase 4 | Promote `dea-catalog-ontologies` under EO umbrella (cross-repo PR); that promotion ships `registry-entry.yaml` files for the fintech + healthcare sector pair. |
| §Phase plan Phase 2 | Telecom sector content ships in CR-EO-02; that PR carries `registry-entry.yaml` files exercising the new `asset_class: ontological` discriminator. |

## What this PR does NOT do

- No `registry-schema.yaml` discriminator change (Phase 1).
- No compatibility-axes generalisation (Phase 1).
- No backward-compat shim (Phase 1).
- No ontological-asset registration schema (Phase 3).
- No README scope-change in this repo (Phase 1).

## Parking lot

- Phase 1 (this repo): header + discriminator + axes generalisation + backward-compat shim.
- Phase 3 (this repo): ontological-asset registration schema.
- Phase 4 (this repo): cloud service provider sector registration (ontological class).
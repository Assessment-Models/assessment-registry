# Cross-Reference: CR-AR-01 ↔ CR-ESA-01 (dea-semantic-architecture)

> **Status:** cross-reference stub — full content lands in Phase 2 of [CR-AR-01](./CR-AR-01.md) (semantic-asset registration schema, lands alongside CR-ESA-01 Phase 2 sector content).

This is a **cross-reference** file documenting the relationship between CR-AR-01 (registry scope extension) and CR-ESA-01 (Enterprise Semantic Architecture).

## Primary CRs

- The full CR-AR-01 lives at: [`change-requests/CR-AR-01.md`](./CR-AR-01.md) in this repo.
- The full CR-ESA-01 lives at: `https://github.com/technehub-labs/dea-semantic-architecture/blob/main/change-requests/CR-ESA-01.md`.

## Sections of CR-AR-01 that affect CR-ESA-01

| CR-AR-01 § | Effect on CR-ESA-01 / dea-semantic-architecture |
|---|---|
| §Scope | ESA outputs (semantic assets) will register through this registry once CR-AR-01 Phase 1 lands (discriminator + axes generalisation). |
| §Boundaries with sibling CRs | ESA is a sibling of AR; ESA's first sector-content PRs (Phase 2) carry `registry-entry.yaml` files that exercise AR-01's discriminator (`asset_class: semantic`). |
| §Phase plan Phase 2 | Semantic-asset registration schema ships alongside CR-ESA-01 Phase 2 (telecom operator sector). |
| §Phase plan Phase 4 | Cloud service provider sector registration (semantic class) lands alongside CR-ESA-01 Phase 3. |
| §Risks §3 | Cross-repo landing race is mitigated by forward-pointing cross-refs. |

## Sections of CR-ESA-01 that affect CR-AR-01

| CR-ESA-01 § | Effect on CR-AR-01 |
|---|---|
| §Boundaries with sibling CRs | ESA's `registry-manifest.yaml` declares forward-compatible registration through AR; activation waits on CR-AR-01 Phase 1. |
| §Phase plan Phase 2 | Telecom sector content ships in CR-ESA-02; that PR carries `registry-entry.yaml` files exercising the new `asset_class: semantic` discriminator. |

## What this PR does NOT do

- No `registry-schema.yaml` discriminator change (Phase 1).
- No compatibility-axes generalisation (Phase 1).
- No backward-compat shim (Phase 1).
- No semantic-asset registration schema (Phase 2).
- No README scope-change in this repo (Phase 1).

## Parking lot

- Phase 1 (this repo): header + discriminator + axes generalisation + backward-compat shim.
- Phase 2 (this repo): semantic-asset registration schema.
- Phase 4 (this repo): cloud service provider sector registration (semantic class).
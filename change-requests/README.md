# Change Requests — assessment-registry

| CR | Title | Status | Date | PR |
|----|-------|--------|------|----|
| [CR-AM-11 Phase 1](../README.md) | Assessment-registry integration spine | MERGED | 2026-08-26 | #1 |
| [CR-AM-11 Phase 6](../README.md) | Legacy catalog record — migration plan pointer | MERGED | 2026-08-26 | #2 |
| [CR-AR-01](./CR-AR-01.md) | Assessment-Registry Scope Extension — umbrella / spec proposal | Proposed | 2026-08-26 | (Phase 0) |
| [CR-AR-01-xref-dea-semantic-architecture](./CR-AR-01-xref-dea-semantic-architecture.md) | Cross-ref: CR-AR-01 ↔ CR-ESA-01 (dea-semantic-architecture) | Proposed | 2026-08-26 | (Phase 0) |
| [CR-AR-01-xref-dea-ontology](./CR-AR-01-xref-dea-ontology.md) | Cross-ref: CR-AR-01 ↔ CR-EO-01 (dea-ontology) | Proposed | 2026-08-26 | (Phase 0) |

## Pipeline

- **CR-AR-01** — Scope-extension umbrella / spec proposal. Phase plan lives in the CR doc; each phase is one future PR.
  - Phase 1 — Header + discriminator + axes generalisation + backward-compat shim (runtime change to this repo).
  - Phase 2 — Semantic-asset registration schema (lands alongside CR-ESA-01 Phase 2).
  - Phase 3 — Ontological-asset registration schema (lands alongside CR-EO-01 Phase 2).
  - Phase 4 — Cloud service provider sector registration (both classes).
  - Phase 5 — Non-assessment-asset governance policy (CR-AR-04).
  - Phase 6 — Discovery UI updates (cross-repo PR on `dea-web-viewer`).

## How to add a CR

1. Author the CR doc following the umbrella CR's structure.
2. Land it in `change-requests/CR-<series>-NN-<slug>.md`.
3. Add a row to the table above.
4. Open a PR.
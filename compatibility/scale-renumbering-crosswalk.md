# Scale renumbering crosswalk — canonical v1 (zero-based) → v2 (L-0 Not Assessed + L-1..L-5)

**Status:** adoption complete across the Assessment-Models maturity-model portfolio; **ratification requested** from the canonical owners (`technehub-labs/dea-metamodel`) per [dea-metamodel#214](https://github.com/technehub-labs/dea-metamodel/issues/214).
**Basis:** dea-metamodel #214 — "align canonical scale level ordinals with band ordinals" (breaking; canonical scale instance v1.0.0 → v2.0.0; consuming models take a SemVer major on adoption).
**Prepared by:** Assessment-Models (ecosystem records maintained in `assessment-registry`).

## 1. The alignment this CR makes

The v1 scheme numbers the level ladder and the band ladder with different bases: five capability levels `L-0..L-4` (or `L0..L4`) paired with five bands `level-1-emergent … level-5-self-optimising` — a permanent off-by-one between a level and the band it maps to.

The v2 scheme aligns the ladders 1:1 and formalizes the unassessed state:

| | v1 (zero-based) | v2 (aligned) | Notes |
|---|---|---|---|
| Sentinel | — | **L-0 Not Assessed** | New: criterion not assessed, 0 points, lowers evidence-confidence, never inflates the index; **not a capability level** |
| Capability 1 | L-0 / L0 | **L-1** | ↔ band `level-1-emergent` (0–20, ×1.0) |
| Capability 2 | L-1 / L1 | **L-2** | ↔ band `level-2-structured` (21–45, ×1.5) |
| Capability 3 | L-2 / L2 | **L-3** | ↔ band `level-3-systematic` (46–70, ×2.5) |
| Capability 4 | L-3 / L3 | **L-4** | ↔ band `level-4-adaptive` (71–88, ×4.0) |
| Capability 5 | L-4 / L4 | **L-5** | ↔ band `level-5-self-optimising` (89–100, ×6.0) |

**Unchanged by the renumbering:** the band instance `dea:maturity-bands-v2` v1.0.0 (ids, ranges, effort multipliers), band ids `level-1-emergent…level-5-self-optimising`, all level names/definitions/characteristics, weights, scoring mechanics, gating rules. Historical index values and bands remain valid; only per-criterion level labels shift (+1).

## 2. Portfolio adoption crosswalk

| Repository | Release | Old level ids | New level ids | Adoption PR | Registry record |
|---|---|---|---|---|---|
| maturity-model-autonomous-operations | 2.0.0 | `L-0 Absent … L-4 Autonomous` | `L-0 Not Assessed` + `L-1 Absent … L-5 Autonomous` | [PR #7](https://github.com/Assessment-Models/maturity-model-autonomous-operations/pull/7) | release 2.0.0 @ `8ccf747e…` |
| maturity-model-operations | 3.0.0 (unreleased, gated on ratification) | `L0..L4` (v2 line) | `L-0 Not Assessed` + `L-1..L-5` (v3 line) | repo-internal v3 evolution | registry pending release |
| maturity-model-technology | 2.0.0 | `L0 Emergent … L4 Self-Optimising` | `L-0 Not Assessed` + `L-1 Emergent … L-5 Self-Optimising` | [PR #6](https://github.com/Assessment-Models/maturity-model-technology/pull/6) | release 2.0.0 @ `d8e345fc…` |
| maturity-model-services-delivery | 2.0.0 | `L0..L4` | `L-0 Not Assessed` + `L-1..L-5` | [PR #6](https://github.com/Assessment-Models/maturity-model-services-delivery/pull/6) | release 2.0.0 @ `703f8ff2…` |
| maturity-model-modernization | 2.0.0 | `L0 Emergent … L4 Self-Optimising` | `L-0 Not Assessed` + `L-1 Emergent … L-5 Self-Optimising` | [PR #5](https://github.com/Assessment-Models/maturity-model-modernization/pull/5) | release 2.0.0 @ `1e5ae437…` |
| maturity-model-digital-transformation | 2.0.0 (folds the unreleased 1.1.0-alpha) | `L-0 Absent/Piloting/Defined/Scaled/Self-Optimising` (composite **and** operationalized line) | `L-0 Not Assessed` + `L-1..L-5` in both lines | [PR #8](https://github.com/Assessment-Models/maturity-model-digital-transformation/pull/8) | release 2.0.0 @ `92691b6c…` |
| maturity-model-digital-transformation-operationalized | 2.0.0 | `level-1-unrealized … level-5-leading` (ordinals 0..4) | ids kept; **ordinals 1..5**; `level-0-not-assessed` sentinel; canonical correlation → `L-1..L-5` | [PR #5](https://github.com/Assessment-Models/maturity-model-digital-transformation-operationalized/pull/5) | release 2.0.0 @ `0b32c4ea…` |

Adoption pattern per repo (reference implementation: autonomous-operations PR #7): scale.yaml gains the L-0 sentinel and shifts capability ids/ordinals +1 with names byte-identical; evaluation/questionnaire level references renumber; register `scale_levels` + correlation blocks rewritten to the aligned numbering; validators enforce six levels with the Not-Assessed first-entry rule; identity files (VERSION / model.yaml / standard.yaml) lockstep at 2.0.0; CHANGELOG BREAKING entries carry the mapping/unchanged/comparability/lockstep bullets. All releases are annotated **adoption-pending** until this CR is ratified.

Registry integration: all six `assessment-registry` registration records declare **release 2.0.0** with immutable commit references ([registry PR #23](https://github.com/Assessment-Models/assessment-registry/pull/23)); `validate_registry.py` reports 17 records valid, `resolve.py` resolves the contract handshake (`maturity-scale-contract @ 1.0`).

## 3. What we ask of the canonical owners

1. **Ratify #214** (assign the CR slot; `CR-AM-12` is occupied) and release the renumbered canonical scale instance — `assessment-models/maturity/scale-examples/*-5level.yaml` at **v2.0.0** — with the L-0 Not Assessed sentinel formalized as proposed.
2. On release, the ecosystem will: (a) bump the Level-2 `contract-conformance` pins (`dea-metamodel-ref`) in every maturity-model repo, (b) flip the **adoption-pending** annotations to adopted across the six models and their registry records, (c) cut the deferred release tags (operations v3.0.0, and 2.0.0 tags where only commit references exist today).

Until then, the portfolio runs the aligned numbering as a draft-pairing convention — validator-enforced locally in every repository, coherence-checked by the repository-standard CI.

## 4. Comparability statement

Historical assessment results remain valid: aggregated scores, band resolutions and effort-adjusted values are computed against the unchanged band instance. Any stored per-criterion level label shifts by +1 (old L-0/L0 → new L-1, … old L-4/L4 → new L-5); the "Not Assessed" state was previously implicit (unanswered criteria) and is now explicit as L-0 with 0 points.

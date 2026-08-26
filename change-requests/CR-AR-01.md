# CR-AR-01 — Assessment-Registry Scope Extension

## Status

- **State:** Proposed — awaiting explicit "Merge" approval.
- **Series tag:** `CR-AR` (Assessment Registry). New umbrella series.
- **Numbering convention:** subsequent AR CRs use compliant numbering (e.g. `CR-AR-02` for semantic-asset registration schema; `CR-AR-03` for ontological-asset registration schema).
- **Primary repo:** `Assessment-Models/assessment-registry` (existing, public — established by CR-AM-11 Phase 1).
- **Visibility:** already public.
- **Sibling CRs:** `CR-ESA-01` (Enterprise Semantic Architecture — produces assets that will register through this scope extension); `CR-EO-01` (Enterprise Ontology — produces assets that will register through this scope extension).
- **Predecessors:** CR-AM-11 Phase 1 (Phase 1 spine landed 2026-08-26; established "OpenDEA-compatible **assessment** assets" scope).
- **Successors (parked):** CR-AR-02 (semantic-asset registration schema — landed alongside CR-ESA-01 Phase 2 sector content); CR-AR-03 (ontological-asset registration schema — landed alongside CR-EO-01 Phase 2 sector content); CR-AR-04 (governance policy for non-assessment asset registration).

## Primary objective

Extend the scope of `Assessment-Models/assessment-registry` from **OpenDEA-compatible assessment assets** (its current scope, established by CR-AM-11 Phase 1) to **OpenDEA-compatible assets** — explicitly including **semantic assets** (CR-ESA-01 outputs) and **ontological assets** (CR-EO-01 outputs) — without disrupting the existing assessment-asset registration pipeline.

## Why now

CR-AM-11 Phase 1 shipped `assessment-registry` as the "ecosystem integration spine for OpenDEA-compatible **assessment** assets — registration, immutable references, compatibility and dependency resolution." The federation's two new foundational pillars (CR-ESA-01, CR-EO-01) will produce assets that the federation needs to discover, version, and resolve — but the current registry scope excludes them.

Two paths forward:

1. **Extend the existing spine** (this CR). Reuse the proven registration, immutable-reference, compatibility, and dependency-resolution machinery. One registry, one ecosystem story.
2. **Build a parallel registry.** Two registries to maintain, governance fragmentation, drift risk.

Path 1 is the principled move (mirrors how the federation already invested in `assessment-registry`). Path 2 is the fallback if the spine cannot be cleanly extended.

CR-AR-01 establishes Path 1.

## Architectural principle

**The registry stays an ecosystem integration spine. Its scope expands to all OpenDEA-compatible assets; the spine is asset-class-agnostic.**

The scope expansion is a *header change*, not a *schema break*:

- Existing assessment-asset entries continue to validate unchanged.
- New asset classes (semantic, ontological) declare their own compatibility axes alongside the existing six.
- The compatibility resolver is generalised from "assessment-asset compatibility" to "OpenDEA-compatible asset compatibility" — a rename + light extension, not a rewrite.

## Scope

In scope:

- Header and README updates changing scope language from "assessment assets" to "OpenDEA-compatible assets" with explicit enumeration of in-scope asset classes (assessment, semantic, ontological; future extensions documented but not enumerated).
- A new `asset_class` discriminator in the registry entry schema (`assessment` / `semantic` / `ontological` / `extension`).
- Compatibility-axes generalisation: existing axes (scoring, vocabulary, examples, schema, runner, governance) remain; a *compatibility-axis registry* extension lets new asset classes declare their own axes.
- Dependency-resolution rules: existing rules remain; new rules documented for cross-asset-class dependencies (e.g. an ontological asset depending on a semantic asset).
- Backward-compatibility shim: existing assessment-asset entries infer `asset_class: assessment` by default if the field is absent. CI rejects new entries that omit `asset_class` after this CR lands.
- CR-ESA-01 and CR-EO-01 cross-references added to README.

Out of scope (handled by future CRs):

- Asset-class-specific registration schemas (CR-AR-02 for semantic, CR-AR-03 for ontological). This CR establishes the *header and discriminator*; the schemas ship with the first sector-content PRs of ESA and EO.
- Non-assessment-asset governance policy (CR-AR-04).
- Discovery UI updates (deferred — likely a future cross-repo PR on `dea-web-viewer`).
- CLI changes (deferred — `dea-cli` integration is a separate CR).

## Boundaries with sibling CRs

| Concern | Owner | Cross-ref |
|---|---|---|
| Registry header + discriminator + axes generalisation | AR-01 | — |
| Compatibility-resolver rename + extension | AR-01 | — |
| Semantic-asset registration schema | AR-02 (parked) | Lands with CR-ESA-01 Phase 2 sector content |
| Ontological-asset registration schema | AR-03 (parked) | Lands with CR-EO-01 Phase 2 sector content |
| Semantic-asset content | ESA | ESA's sector-content PRs reference AR-02 schema |
| Ontological-asset content | EO | EO's sector-content PRs reference AR-03 schema |
| Existing assessment-asset registration | AR inherits from CR-AM-11 Phase 1 | Backward-compat shim ensures no schema break |
| `Assessment-Models/assessment-ci` (CI runner) | AM-11 | CI runner picks up new asset classes via the discriminator |

The non-overlap table prevents future phases from duplicating or contradicting ESA, EO, or CR-AM-11.

## Design constraints

1. **No schema break for existing entries.** All current assessment-asset entries continue to validate after this CR lands. Backward-compat shim is mandatory.
2. **No scope expansion beyond three classes in this PR.** Asset classes enumerated: `assessment` (existing), `semantic` (new), `ontological` (new). Future classes (e.g. `agentic`, `twin`) require their own CR. This prevents silent scope creep.
3. **The compatibility-resolver rename is a rename, not a rewrite.** Generalising "assessment-asset compatibility" to "OpenDEA-compatible asset compatibility" must preserve the existing resolution algorithm; only the header language and the `asset_class` discriminator change.
4. **Land-as-authored.** This CR doc ships verbatim into `change-requests/CR-AR-01.md`. No silent re-writes.
5. **Cross-repo cross-links.** README updates must explicitly cite CR-ESA-01 and CR-EO-01 in their respective `technehub-labs` repos.

## Phase plan

Each phase is one future PR. The user picks the first phase after this proposal merges; later phases may shift but the boundaries hold.

| Phase | Scope | First deliverable |
|---|---|---|
| **1** | Header + discriminator + axes generalisation + backward-compat shim | `registry-schema.yaml` updated + README updated + CR-ESA-01 / CR-EO-01 cross-refs |
| **2** | Semantic-asset registration schema (CR-AR-02) | Lands alongside CR-ESA-01 Phase 2 sector content (telecom) |
| **3** | Ontological-asset registration schema (CR-AR-03) | Lands alongside CR-EO-01 Phase 2 sector content (telecom) |
| **4** | Cloud service provider sector registration (both classes) | Lands alongside CR-ESA-01 / CR-EO-01 Phase 3 |
| **5** | Non-assessment-asset governance policy (CR-AR-04) | Formalises what makes a non-assessment asset "OpenDEA-compatible" |
| **6** | Discovery UI updates (cross-repo PR on `dea-web-viewer`) | Surface non-assessment assets in viewer |

**Recommended first phase:** Phase 1 (Header + discriminator + axes generalisation). Without the discriminator, subsequent phases cannot reliably route entries to the right schema.

## Definition of Done for this proposal PR

The proposal PR ships ONLY:

1. `change-requests/CR-AR-01.md` (this doc, verbatim).
2. `change-requests/CR-AR-01-xref-dea-semantic-architecture.md` (cross-ref to CR-ESA-01).
3. `change-requests/CR-AR-01-xref-dea-ontology.md` (cross-ref to CR-EO-01).
4. `change-requests/README.md` row linking this CR.
5. README updates: language changed from "assessment assets" to "OpenDEA-compatible assets"; new asset classes enumerated; CR-ESA-01 / CR-EO-01 cross-refs added.
6. `CHANGELOG.md` entry.
7. Placeholder stubs for the future-phase schemas (`schemas/semantic/` and `schemas/ontological/`) — empty directories with READMEs only.

**Not shipped in this PR:** `asset_class` discriminator in `registry-schema.yaml`, compatibility-axes generalisation, backward-compat shim logic, asset-class-specific registration schemas, governance policy, discovery UI updates, CLI changes.

## Risks

1. **Backward-compat regression.** An existing assessment-asset entry could fail to validate if the schema changes break a previously-valid shape. Mitigation: shim is mandatory; CI runs the full existing asset suite against the new schema as a regression test.
2. **Scope creep.** Future asset classes (e.g. `agentic`) could enter silently. Mitigation: Phase 1 explicitly enumerates only three classes; future classes require their own CR.
3. **Cross-repo landing race.** ESA, EO, and AR PRs land in parallel. If AR-01 lands before ESA-01 / EO-01, the cross-refs in AR's README point at not-yet-merged siblings. Mitigation: cross-refs are forward-pointing; readers following them hit either merged content (good) or the proposal PR (acceptable — clearly labelled Proposed).
4. **Compatibility-resolver rename risk.** "Assessment-asset compatibility" → "OpenDEA-compatible asset compatibility" is a wide rename touching tests, CI jobs, and docs. Mitigation: rename is grep-and-replace only; no algorithm changes; CI regression suite proves no behavioural drift.
5. **Empty Phase 0 perception.** A proposal PR with header/README changes only can look like a copy-edit. Mitigation: the README change is clearly framed as scope expansion; the CR doc's Definition of Done enumerates what is and is not shipped.

## Decision points deferred to later phases

- Final wording of asset-class enumeration in README (Phase 1).
- Schema for semantic / ontological asset entries (Phase 2–3).
- Governance policy for "OpenDEA-compatible" outside assessment (Phase 5 — needs user input).
- Discovery UI priority (Phase 6 — depends on viewer roadmap).

## References

- OpenDEAM: `technehub-labs/dea-architecture-framework` (root authority).
- This repo: `Assessment-Models/assessment-registry` (current scope: "OpenDEA-compatible assessment assets").
- CR-AM-11 (Phase 1 — established this registry spine; Phase 2 onward — interoperability + ecosystem conformance).
- CR-AM-11 Phase 1 landing: 2026-08-26; PR and merge details in `cr-programme-state.md`.
- Sibling: CR-ESA-01 (Enterprise Semantic Architecture).
- Sibling: CR-EO-01 (Enterprise Ontology).
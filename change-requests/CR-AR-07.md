# CR-AR-07 — Repository-Standard Adoption Authority and Portfolio Reconciliation

## Status
- **State:** Implemented in review; acceptance pending CI and merge.
- **Origin:** [Issue #30](https://github.com/Assessment-Models/assessment-registry/issues/30).
- **Related:** [Issue #16](https://github.com/Assessment-Models/assessment-registry/issues/16) tracks the adoption-source-of-truth correction.

## 1. Objective
Make the assessment registry the authoritative store for each registered maturity-model repository's adoption snapshot, and make the maturity-model-standard portfolio adoption view a derived projection. Keep the standard repository authoritative for the standard's normative identity, requirements, conformance definitions, repository classifications, Phase 2 assessments, structure mappings and explanatory notes.

## 2. Ownership model
- `maturity-model-standard/standard.yaml` remains normative authority for standard identity and published version.
- `maturity-model-standard/specifications/`, schemas and validators remain normative authority for requirements and conformance interpretation.
- Each applicable `assessment-registry` maturity-model registration carries `repository_standard: { id, version, conformance }`. This is the authoritative adoption snapshot for that registered asset.
- The registered release's `standard.yaml` is the source declaration corroborated at the exact immutable release commit. It is not a second mutable registry.
- `maturity-model-standard/registry/conformance.yaml` retains repository classification, Phase 2 assessment results, structure mappings, achieved dates and notes. Its adoption fields for registered maturity-model repositories are a derived view of the assessment-registry snapshots.
- Assessment models, legacy-frozen assets, shared infrastructure and org-governance repositories remain classified by the standard portfolio registry and are not forced into the maturity-model adoption block.

## 3. Registration contract
For each non-legacy `type: maturity-model` record:
1. `repository_standard` is required and contains the standard ID, declared version and conformance level.
2. At the resolved `release.reference` commit, `standard.yaml` must exist.
3. Its repository type must be `maturity-model`.
4. Its standard ID, version and conformance must equal the registry snapshot.
5. Its model ID and version must equal the registration ID and release version.
6. All checks run against the exact resolved immutable commit, not the source default branch.

The legacy frozen maturity catalogue is excluded from adoption snapshots; its explicit `release.manifest: null` and immutable reference verification remain intact. No other asset classes are affected.

## 4. Migration
1. Correct the Digital Transformation Operationalized source declaration and publish the reviewed model patch release 2.0.1. Completed by source PR #9 (merge commit `617aabc106e991fdef1011c501f82f997f73a8ca`).
2. Update the registry record to release 2.0.1 and the exact merge commit.
3. Add adoption snapshots for the seven registered active maturity-model repositories.
4. Enforce pinned declaration/snapshot coherence in release-integrity CI.
5. Update the standard portfolio registry and report so adoption values are derived from the assessment registry, while preserving independent portfolio classification and Phase 2 metadata.

## 5. Invariants
- No historical release references or tags are rewritten.
- No tags/releases are created or moved by this CR.
- No maturity dimensions, criteria, evidence anchors, levels, scoring, assessment gates, dependencies, supersession or touchpoint relationships are changed.
- The standard remains normative; the registry does not redefine conformance requirements.
- The standard portfolio registry retains its non-adoption responsibilities.
- No duplicate adoption authority is introduced.

## 6. Acceptance criteria
- Seven applicable maturity-model registrations contain adoption snapshots.
- The DTO Operationalized registration points to 2.0.1 at the exact merged source commit.
- Release-integrity validation checks the declaration at each pinned source commit.
- Positive and negative tests cover snapshot agreement and mismatch.
- Non-maturity-model records and the legacy-frozen catalogue remain outside the adoption snapshot requirement.
- The portfolio adoption projection is reconciled without losing classification, Phase 2 assessments, mappings or notes.

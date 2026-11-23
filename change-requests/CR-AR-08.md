# CR-AR-08 — Canonical Asset Identity and Criterion-Register Discovery

## Status

- **State:** Proposed — contract design for review; no runtime or registration changes are included in this proposal.
- **Series:** CR-AR (Assessment Registry).
- **Primary repository:** `Assessment-Models/assessment-registry`.
- **Origin:** [Issue #32](https://github.com/Assessment-Models/assessment-registry/issues/32).
- **Related:** [assessment-ci#9](https://github.com/Assessment-Models/assessment-ci/issues/9) — Level 3 reciprocal touchpoint validation.
- **Predecessors:** CR-AM-11 registry and immutable-release integration; CR-AR-06 pinned release identity verification.
- **Dependent work:** a touchpoint-contract amendment is required if criterion mappings need explicit register selection or mapping-level pending status.

## 1. Problem

Level 3 semantic touchpoint validation needs to resolve two different identities without inference:

1. A touchpoint's `peer_asset` is a canonical OpenDEA asset identifier (for example, `dea:maturity-operations`), while the registry currently identifies the repository-backed asset with a repository-oriented record ID (for example, `maturity-model-operations`).
2. A touchpoint's `criteria_mapping` refers to model-owned criterion identifiers, but the registry has no machine-readable declaration identifying the authoritative criterion-register artifact and the rule for extracting its identifiers.

The registry's `source.repository`, registration `id`, and free-text `notes` are not substitutes for either declaration. The validator MUST NOT derive canonical asset IDs from repository slugs, parse prose, scan arbitrary YAML files, or treat every field named `id` as a criterion.

## 2. Objective

Extend the registration contract with explicit, release-scoped metadata for:

- the canonical asset identity used by semantic relationships; and
- the authoritative criterion-register artifact(s) and a deterministic selector for their criterion identifiers.

The registry remains metadata-only. Criterion definitions and all model semantics remain in the owning model repository.

## 3. Ownership and resolution model

### 3.1 Canonical asset identity

Add an optional `canonical_asset_id` string to registration records.

- It identifies the canonical OpenDEA asset represented by the registered repository/release.
- It is distinct from the registry record `id`, repository slug, and model-manifest `id`.
- It MUST be unique across active registrations in the same canonical identity namespace.
- It MUST be treated as an opaque identifier by the registry. The registry validates syntax and uniqueness; it does not redefine the identifier's ontology.
- The field is optional for backward compatibility. It becomes required for any registered asset that participates as a touchpoint endpoint, and for new active maturity-model registrations that declare touchpoints.

For a touchpoint endpoint, Level 3 resolves the `peer_repo` to exactly one registration using `source.organization` + `source.repository`, then compares `peer_asset` exactly with that registration's `canonical_asset_id`. A missing registration, missing canonical ID, duplicate source mapping, or mismatch is an explicit unresolved/error result. No slug-to-ID transformation is permitted.

### 3.2 Criterion-register declaration

Add an optional `criterion_registers` array to a registration record. Each declaration contains:

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Required, unique within the registration | Stable register key |
| `path` | Required | Safe repository-relative path to the authoritative YAML or JSON register artifact |
| `format` | Required; `yaml` or `json` | Serialization format |
| `selector` | Required | RFC 9535 JSONPath expression selecting criterion identifier values |

Illustrative shape (the path and selector below are examples, not claims about any current release):

```yaml
criterion_registers:
  - id: primary
    path: maturity/criteria-register.yaml
    format: yaml
    selector: "$..criteria[*].id"
```

Normative resolution rules:

1. Every path is resolved relative to the registered source repository at the commit resolved from `release.reference`.
2. The path MUST be relative, remain within the repository, exist at that commit, and match the declared format.
3. The selector MUST be evaluated using RFC 9535 JSONPath semantics. Implementations MUST NOT introduce repository-specific selector dialects.
4. The selector result MUST be a non-empty collection of non-empty strings. Non-string values, an empty result, duplicate IDs within a register, or selector evaluation errors are validation failures.
5. Criterion IDs are compared as exact strings. Numeric-looking IDs MUST NOT be coerced to numbers; leading zeroes and punctuation are significant.
6. The validator MUST retain the register key and source path with each resolved identifier so diagnostics can identify its provenance.
7. Criterion content is not copied into the registry. The registry stores only the release-scoped locator and extraction rule.

### 3.3 Mapping resolution across multiple registers

- The resolved criterion inventory for an asset is the union of its declared registers, preserving the register provenance for every identifier.
- If an identifier occurs in more than one register and the touchpoint mapping does not identify the intended register, the endpoint is **ambiguous**, not valid.
- If a model has no register declaration, or an identifier is absent from all declared registers, the endpoint is **unresolved**.
- The Level 3 validator MUST NOT guess a register from a filename, criterion label, numeric pattern, or free-text note.
- If real portfolio cases require selecting among registers where identifiers overlap, a separately versioned touchpoint-contract amendment MUST add explicit endpoint register selection. That amendment is a prerequisite to accepting those mappings, not a reason to weaken resolution.

### 3.4 Pending mappings

A pending mapping is not a valid resolved criterion. Level 3 reporting MUST distinguish:
- resolved;
- explicitly pending under a published touchpoint-contract status declaration;
- unresolved (no authoritative identifier match);
- ambiguous (multiple possible register matches); and
- invalid (malformed declaration or contract violation).

The current record-level `peer_status` may be used only for the scope it explicitly declares. It MUST NOT silently convert an individual unresolved criterion endpoint into a valid mapping. Any mapping-level pending status must be introduced through the touchpoint-contract owner and versioned contract, not invented by the registry validator.

## 4. Immutable-release boundary

All registry metadata and source artifacts are interpreted as one release snapshot:

1. Resolve `release.reference` using the existing CR-AR-06 rules.
2. Read the authoritative model manifest, touchpoint declaration, and every declared criterion-register artifact from that exact resolved commit.
3. Resolve the registry's canonical asset identity and criterion inventories from the registration record plus those pinned artifacts.
4. Never substitute a current default-branch file when the pinned release lacks a declaration or artifact.
5. A later release may add or correct metadata, but historical registrations and references remain unchanged.

The validator MUST report the registration ID, source repository, declared release reference, resolved commit, register key/path, selector, and offending identifier for each failure.

## 5. Migration and compatibility

1. Add the fields to `schemas/registration.schema.json` as optional fields initially.
2. Add schema and release-integrity tests before populating records.
3. Inventory all active maturity-model registrations and establish canonical IDs from authoritative model-owner decisions, not inferred slugs.
4. Declare criterion-register paths/selectors only after verifying the exact artifact at each registration's pinned release.
5. Do not change release references, create/move tags, rewrite historical manifests, or update touchpoint relationships as part of this CR.
6. Keep legacy/catalog registrations valid where canonical asset identity and criterion registers do not apply.
7. Require the metadata for registered touchpoint endpoints through Level 3 semantic validation. Missing metadata is reported explicitly; it is not silently defaulted.

## 6. Tests

Positive and negative fixtures MUST cover:

- unique canonical ID and exact peer-asset resolution;
- missing canonical ID, duplicate canonical ID, duplicate source repository mapping, and peer-asset mismatch;
- valid YAML and JSON register artifacts;
- safe relative paths and rejection of absolute paths, traversal, missing files, and format mismatch;
- valid RFC 9535 selectors, invalid selectors, empty results, non-string results, and duplicate criterion IDs;
- exact string handling for numeric-looking identifiers;
- successful resolution at a pinned commit when the default branch has advanced;
- unresolved and ambiguous identifiers across one or multiple registers;
- no fallback to arbitrary files, prose notes, or mutable default branches;
- legacy registrations without the new optional metadata remaining schema-valid.

## 7. Invariants and non-goals

- The registry remains a metadata and immutable-reference index; it does not own criterion definitions.
- The model repository remains authoritative for its dimensions, subdimensions, criteria, evidence, levels, scoring, and assessment semantics.
- The touchpoint contract remains authoritative for touchpoint record structure and mapping semantics.
- The assessment-ci repository owns validation execution; this CR does not implement Level 3.
- Existing Operations ↔ Autonomous Operations and other peer relationships are preserved exactly.
- Level 2 structural validation is unchanged.
- No model release, touchpoint artifact, registry release reference, or Git tag is changed by this design proposal.

## 8. Acceptance criteria

- The registration schema defines `canonical_asset_id` and `criterion_registers` with the constraints above.
- Registry release-integrity validation evaluates these declarations against the exact immutable source commit.
- The registry rejects malformed, duplicate, unsafe, missing, or ambiguous metadata as specified.
- Existing registrations remain backward-compatible until their records are deliberately migrated.
- Portfolio inventory identifies every touchpoint endpoint that cannot yet be resolved and records the owner decision needed; no guessed values are populated.
- A dependent touchpoint-contract change is identified and agreed where mapping-level status or register selection is needed.
- Assessment-ci#9 can consume the published registry contract without inferring identities or scanning arbitrary model files.

## 9. Implementation sequence

| Sequence | Owner | Deliverable |
|---|---|---|
| 1 | assessment-registry | Approve this contract design; implement schema, validator, fixtures, and documentation |
| 2 | Assessment-Models model owners | Populate canonical IDs and pinned criterion-register declarations after artifact-level verification |
| 3 | dea-metamodel touchpoint-contract owner | Version any required mapping-level register selector or pending-status fields |
| 4 | assessment-ci | Implement Level 3 peer identity, reciprocal mirror, and criterion resolution using only the published contracts |
| 5 | Portfolio | Run Level 3 against registry-pinned releases; report unresolved historical snapshots without rewriting them |

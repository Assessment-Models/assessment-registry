# CR-AR-06 — Immutable Source Reference and Release Identity Verification

## Status
- **State:** Accepted for implementation; PR review pending.
- **Series:** CR-AR (Assessment Registry).
- **Primary repository:** `Assessment-Models/assessment-registry`.
- **Origin:** [Issue #28](https://github.com/Assessment-Models/assessment-registry/issues/28).
- **Related governance decision:** [Issue #16](https://github.com/Assessment-Models/assessment-registry/issues/16), resolved by retaining the authority boundary established in CR-AM-ORG-RES-000.

## 1. Problem
The registry validator checks the syntax of `release.reference`, but not whether it resolves in the declared source repository. A syntactically valid but nonexistent tag can therefore pass CI. Commit-SHA and digest references are not verified. The registry also does not verify that `release.commit` agrees with the resolved reference or that the authoritative manifest at the pinned commit identifies the registered asset and release version.

## 2. Objective
Make registry CI verify every registered release against its exact immutable source snapshot. All checks MUST operate on the resolved commit, never the source repository's mutable default branch.

## 3. Normative requirements

### 3.1 Reference resolution
1. A release tag matching `vX.Y.Z[-prerelease]` MUST exist in the declared source repository.
2. Lightweight and annotated tags MUST both be supported; annotated tags MUST be peeled to the commit.
3. A 40-character commit SHA MUST be fetchable and resolve to that exact commit in the declared source repository.
4. `sha256:` digests are reserved for future content-addressed support. Until a resolver and artifact contract exist, CI MUST fail such registrations explicitly; it MUST NOT report them as verified.
5. Mutable references remain prohibited.

### 3.2 Commit coherence
If `release.commit` is present, it MUST equal the resolved commit. A SHA reference MUST resolve to itself. Any mismatch MUST fail CI.

### 3.3 Pinned manifest identity
For asset types with an authoritative root manifest, CI MUST read that manifest from the resolved commit and verify its `id` equals the registry record `id`, and its `version` equals `release.version`.

The default authoritative manifest is `model.yaml` for `maturity-model`, `assessment-model`, and `component` records. A record may override the path with `release.manifest`. An explicit `release.manifest: null` declares that no authoritative manifest exists for a legacy/catalog asset; reference and commit verification remain mandatory.

Asset types without a defined authoritative manifest are reference-verified only. A missing default manifest is a failure unless the record explicitly declares `manifest: null`.

### 3.4 CI coverage and diagnostics
The validator MUST run on every pull request and push to main, and MUST inspect every YAML registration under `registry/`. It MUST report asset ID, source repository, reference, resolved commit where available, and exact mismatch. Existing schema, uniqueness, dependency, asset-class, axes, and supersession validation MUST remain intact.

### 3.5 Tests
Tests MUST cover valid lightweight tag, valid annotated tag and peeling, valid commit SHA, missing tag, unresolvable SHA, commit mismatch, manifest ID mismatch, manifest version mismatch, and explicit digest rejection pending a resolver.

## 4. Design constraints
- No release tags are created, moved, or inferred by this CR.
- No registration record is silently rewritten to make validation pass.
- Historical immutable references remain valid historical records.
- No model semantics, scoring, evidence semantics, or touchpoint relationships are standardized by this CR.
- No model content is copied into the registry.
- Repository-standard adoption remains authoritative in `maturity-model-standard/registry/conformance.yaml`; this CR does not duplicate those fields.

## 5. Acceptance criteria
- Every existing registry record resolves its declared tag or SHA against its declared source repository.
- Every declared commit claim agrees with the resolved commit.
- Every applicable pinned manifest agrees on asset ID and release version.
- The legacy maturity catalogue explicitly declares the absence of an authoritative root manifest.
- Positive and negative fixtures pass.
- Registry CI runs the new validator alongside existing checks.
- Existing registration identities, dependencies, supersession declarations, and release history are preserved.

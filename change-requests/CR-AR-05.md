# CR-AR-05 — Machine-Readable Supersession

## Status

- **State:** Proposed — awaiting review.
- **Series tag:** `CR-AR` (Assessment Registry). Continues the AR series after CR-AR-01.
- **Numbering convention:** `CR-AR-05` per the numbering established in CR-AR-01 (CR-AR-02/03/04 are parked for their named concerns; this CR takes the next free number).
- **Primary repo:** `Assessment-Models/assessment-registry` (schema + validator).
- **Consumers:** `Assessment-Models/assessment-ci` (Level 3 ecosystem validation may surface supersession in future phases); discovery tooling (future CR-AR-04/06 concerns).
- **Predecessors:** CR-AM-11 (registration record contract, §11–12); CR-AR-01 (scope extension, per-class field sets); CR-AM-01 Release 1 decision record (D-1: freeze legacy cluster — supersession is now a live, decided concern, recorded prose-only in `notes`).
- **Origin:** Flagged during CR-AM-01 Release 1 execution (registry PR #7): the legacy maturity catalog's supersession could only be recorded as a note because the registration schema has `additionalProperties: false` and no `superseded_by` field.

## Primary objective

Give registration records a **machine-readable, validated supersession declaration**, so consumers (registry resolver, ecosystem CI, discovery tooling) can programmatically follow the chain `asset → superseding asset/contract` instead of parsing prose notes.

## Why now

- The CR-AM-01 Release 1 decision (D-1) froze the legacy cluster with supersession semantics — currently expressible only in `notes`.
- `MIGRATION.md` in the legacy catalog has always described "register with `superseded_by`" as the intended freeze mechanism; the schema never supported it. This CR closes that gap between documented intent and schema reality.
- Two records are affected today (`dea-catalog-maturity-models`, `dea-catalog-assessment-tools` is a candidate once its own supersession is decided); more will follow as the ecosystem evolves.

## Scope

In scope:

- One new **optional** schema field on registration records: `superseded_by`.
- Validation rules:
  1. If present, `superseded_by` must reference either (a) another **registered asset id**, or (b) an **external canonical target** expressed as a structured object (`organization`, `repository`, optional `path`), for supersession targets outside the registry (e.g. the v2 canonical maturity architecture in `technehub-labs/dea-metamodel`).
  2. Referential integrity: form (a) must resolve to an existing record id (same rule as `dependencies`).
  3. Coherence: a record with `status: legacy` or `status: superseded` SHOULD declare `superseded_by`; a record with `status: active` MUST NOT.
- Validator extension in `scripts/validate_registry.py` enforcing the above.
- Schema version note: additive-only, `additionalProperties: false` retained; existing records validate unchanged (the field is optional).

Out of scope (handled by future CRs or existing machinery):

- Chain analysis (transitive supersession graphs) — a possible `resolve.py` extension.
- Discovery-UI surfacing — CR-AR-04/06 territory.
- Automatic status flips — a record's `status` remains an explicit author choice; this CR only cross-checks.

## Schema shape

```json
"superseded_by": {
  "oneOf": [
    { "type": "string", "pattern": "^[a-z][a-z0-9-]*$", "description": "registered asset id" },
    {
      "type": "object",
      "additionalProperties": false,
      "required": ["organization", "repository"],
      "properties": {
        "organization": { "type": "string" },
        "repository": { "type": "string" },
        "path": { "type": "string" }
      }
    }
  ]
}
```

Record example (external canonical target):

```yaml
id: dea-catalog-maturity-models
status: legacy
superseded_by:
  organization: technehub-labs
  repository: dea-metamodel
  path: assessment-models/maturity/
```

## Design constraints

1. **Additive-only.** No existing record changes meaning; the field is optional; `additionalProperties: false` stays.
2. **No new asset class.** Supersession applies to all classes uniformly — this is not a CR-AR-01-style scope extension.
3. **Land-as-authored.** This CR doc ships verbatim into `change-requests/CR-AR-05.md`.
4. **Validator parity.** Schema and validator rules ship together in one PR; a record passing the schema must also pass the validator's referential + coherence checks.

## Execution checklist

| # | Action | Repo |
|---|--------|------|
| 1 | Land this CR doc | assessment-registry |
| 2 | Schema: add optional `superseded_by` (oneOf string / object) | assessment-registry |
| 3 | Validator: referential integrity + status coherence | assessment-registry |
| 4 | Convert the legacy catalog's prose supersession note to the field | assessment-registry |
| 5 | Self-test fixture: positive (external target) + negative (unresolvable id; active record with superseded_by) | assessment-registry |
| 6 | CHANGELOG entry | assessment-registry |

## Impact summary

No breaking change. Two records change today (one gains the field, one is validated); the rest of the registry is untouched. The registry's answer set gains a fourth resolution: *what supersedes this asset?* — alongside what exists, where it lives, and what it conforms to.

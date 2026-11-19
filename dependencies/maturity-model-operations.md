# Dependency documentation — maturity-model-operations

Machine-readable dependencies live in the registration record (validated for referential integrity). This
note is the human-readable companion (Phase 4+ format), covering the CR-AM-13 Handshake & Touchpoint Model.

## Why these dependencies exist

`dea:maturity-operations` v2 formalizes six seams with peers. Each touchpoint (declared in the model repo's
`touchpoints.yaml`, mirrored in the peer repos) makes overlap single-owner and evidence single-assessment:

| Peer asset | Touchpoint | Direction | What crosses the seam |
|---|---|---|---|
| maturity-model-autonomous-operations | tp-ops-x-autonomous-operations | we feed | D5 reliability evidence (observability 3.3.8, predictive detection 4.1.1, ICS 4.1.2, auto-remediation 3.1.3, SLO 4.2.5, cost 3.3.6). Peer owns OODA/closed-loop autonomy; we own human/assisted operations. |
| maturity-model-services-delivery | tp-ops-x-services-delivery | we feed | D1 flow/commitment evidence feeds their flow-efficiency criteria; blocked until the peer publishes a criteria register. |
| maturity-model-technology | tp-ops-x-technology | we consume | Platform/tool capability is the peer's; we assess only tool-use effectiveness; blocked until the peer publishes a register. |
| maturity-model-digital-transformation | tp-ops-x-digital-transformation | we consume | Strategy/transformation state informs D6; resolve to component criterion IDs at the reciprocity merge. |
| maturity-model-digital-transformation-operationalized | tp-ops-x-dt-operationalized | we consume | d2c1 strategy feeds D6; d5c2 TOM design stays the peer's, we own TOM execution (OPS-D6-SD2-C04); shared d4 evidence single-assessed. |
| maturity-model-modernization | tp-ops-x-modernization | shared-component | Shared operations-modernization component (v1.0.0); scoring semantics owned per model. |

## What breaks on a peer major version

- **Criterion renumbering in a peer major release** invalidates the `criteria_mapping.theirs` IDs in our
  `touchpoints.yaml` (and the peer's mirror). Required action: re-run the reconciliation, update both
  records, keep our OPS-* IDs untouched.
- **A peer removing an assessed subject** (e.g., a peer dropping its Operations dimension) orphans the
  touchpoint: mark `peer_status: orphaned`, detach the mapping, and re-home the criterion if needed.
- **The maturity-touchpoint-contract** moving from 0.1.0-draft to 1.0.0 is additive; a later major
  renegotiates the record fields — mirror files and the CI reciprocity check update together.

Mirror records merged: autonomous-operations PR #5, digital-transformation PR #7,
digital-transformation-operationalized PR #4, modernization PR #4 (peer release tags pending from owners).
Contract publication requested: technehub-labs/dea-metamodel#213.

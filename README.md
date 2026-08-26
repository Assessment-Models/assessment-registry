# assessment-registry

**The ecosystem integration spine for OpenDEA-compatible assessment assets** (CR-AM-11 §10).

This repository registers assets. It contains **no maturity model content** — registration records carry metadata and immutable references only (§11). Dimensions, criteria, levels, scoring rules and all model content remain owned by the model repositories.

The registry answers:

- What exists?
- Where is it?
- What version exists? Which version is **active**?
- Which OpenDEA contract does it conform to?
- Which components does it depend on?
- Which relationships exist between assets?

## Layout

```
assessment-registry/
├── registry/
│   ├── maturity-models/      ← one YAML record per registered maturity model
│   ├── assessment-models/    ← one YAML record per registered assessment model
│   ├── assessment-tools/     ← one YAML record per registered assessment tool
│   └── components/           ← one YAML record per registered reusable component
├── compatibility/            ← compatibility declarations between assets (Phase 2+)
├── dependencies/             ← cross-asset dependency documentation (Phase 2+)
├── schemas/
│   └── registration.schema.json   ← the registration record contract (Draft 2020-12)
├── examples/                 ← worked registration examples (validated in CI)
├── scripts/
│   ├── validate_registry.py  ← schema + immutability + uniqueness + referential checks
│   └── resolve.py            ← resolve an asset id → source repo + immutable reference
└── .github/workflows/ci.yml
```

## Registration rules (CR-AM-11 §11–12)

1. **Metadata + references only.** Records never duplicate model content.
2. **Immutable references are mandatory.** `release.reference` must be a release tag (`vX.Y.Z`), a 40-char commit SHA, or a content digest. `main`, `master`, `latest`, `HEAD` are rejected by CI.
3. **One record per asset**, filename = `<id>.yaml` under the type-matching directory.
4. **Contract conformance is declared**, per the contract handshake (§15): every record names the OpenDEA contract id + version the asset conforms to.
5. **Dependencies must resolve.** A record's `dependencies` entries must reference other registered asset ids.

## Registering an asset

1. Copy the closest record under `examples/` into the type-matching `registry/` directory.
2. Fill identity, source, immutable release reference, contract handshake, status.
3. Open a PR — CI runs `scripts/validate_registry.py` (schema + immutability + uniqueness + referential integrity) and `scripts/resolve.py` on changed records.
4. On merge the asset is registered; ecosystem CI (assessment-ci) picks it up from there.

## Status values

`active` · `legacy` · `candidate-for-migration` · `reference` · `deprecated` · `superseded` — aligned with the §26 legacy classification in the [org governance](https://github.com/Assessment-Models/.github/blob/main/GOVERNANCE.md).

---

*Established under [CR-AM-11 — Federated Assessment Model Ecosystem](https://github.com/technehub-labs/dea-metamodel/blob/main/change-requests/CR-AM-11.md) Phase 1.*

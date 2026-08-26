# Dependency documentation

Narrative documentation of cross-asset dependencies (why A depends on B, what breaks when B releases a major version).

Machine-readable dependencies live in each registration record's `dependencies` field and are validated for referential integrity by `scripts/validate_registry.py` on every PR. This directory holds the human-readable companion notes, introduced as the dependency graph grows beyond single assets (Phase 4+).

# ANIMO5

Controlled modernization programme for the ANIMO soil-water-quality model.

The repository is intentionally bootstrapped evidence-first. Production migration does not start until the legacy source, documentation, test behaviour and qualification baseline are sufficiently established.

Current initial work unit: `ANIMO-PREP01`.

Current PREP01 decision: `BLOCKED_AUTHORITATIVE_LEGACY_SOURCE_DOCUMENTATION_AND_EXECUTABLE_REQUIRED`.

The blocked decision is deliberate. The repository now contains the provenance framework, testcase identity/manifests, evidence inventories, governance, architecture invariants, test architecture and quality registers, but no legacy production source or production ANIMO5 migration code.

Top-level areas:

- `reference/`: immutable-evidence placeholders and testcase identity/manifests;
- `src/`: future ANIMO5 production source, intentionally empty during PREP01;
- `tests/`: evidence-integrity bootstrap tests and later scientific tests;
- `docs/`: architecture, governance, PREP, testing and quality evidence;
- `tools/`: reproducible evidence/audit tooling;
- `integration/`: machine-readable work-unit and qualification records.

No LICENSE is added until a legal basis is established.

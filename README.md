# ANIMO5

Controlled modernization programme for the ANIMO soil-water-quality model.

The repository is intentionally bootstrapped evidence-first. Production migration does not start until the legacy source, documentation, test behaviour and qualification baseline are sufficiently established.

Current initial work unit: `ANIMO-PREP01`.

Current PREP01 decision: `BLOCKED_REPRODUCIBLE_NATIVE_LEGACY_EXECUTION_AND_CONTROLLED_B0_RETENTION_REQUIRED`.

PREP01 now has three concrete evidence classes:

- supplied ANIMO 4.1.5 revision-53 source candidate, archive/member hashes persisted;
- supplied ANIMO 4.0 technical user's guide, document hash and scope persisted;
- nine-case ANIMO testbank, archive/member hashes and inventory persisted.

The remaining block is no longer missing material. It is qualification: exact controlled B0 byte retention, native/reference build reproduction, binary hydrology compatibility and successful capture of unrounded testcase behaviour are not yet established. No ANIMO5 process migration has started.

Top-level areas:

- `reference/`: cryptographically pinned legacy evidence identities and manifests;
- `src/`: future ANIMO5 production source, intentionally empty during PREP01;
- `tests/`: evidence-integrity bootstrap tests and later scientific tests;
- `docs/`: architecture, governance, PREP, testing and quality evidence;
- `tools/`: reproducible evidence/audit tooling;
- `integration/`: machine-readable work-unit and qualification records.

No LICENSE is added until a legal basis is established. The public repository does not republish supplied legacy source/document bytes without an established redistribution basis.

# ANIMO5

Controlled modernization programme for the ANIMO soil-water-quality model.

The repository is intentionally bootstrapped evidence-first. Production migration does not start until the legacy source, documentation, test behaviour and qualification baseline are sufficiently established.

Current initial work unit: `ANIMO-PREP01`.

Current PREP01 decision:

`BLOCKED_REFERENCE_QUALIFICATION_CONTROLLED_B0_RETENTION_AND_GHG_PROVENANCE_REQUIRED`

PREP01 now has three concrete legacy evidence classes:

- supplied ANIMO 4.1.5 revision-53 source candidate, archive/member hashes persisted;
- supplied ANIMO 4.0 technical user's guide, document hash and scope persisted;
- nine-case ANIMO testbank, archive/member hashes and inventory persisted.

Execution archaeology has advanced beyond the original build and binary-I/O blockers. Microsoft/Intel Fortran PowerStation-compatible hydrology framing is structurally recovered with payload-preserving qualification tooling. A fresh GNU Fortran 14.2 diagnostic build using evidence-derived legacy compiler semantics executes eight of nine testcases deterministically, with exact normalized output reproduction across repeated runs and an independent rebuild.

Those eight outputs are diagnostic evidence only. They are not admitted as a legacy behavioural oracle because equivalence to the historical Intel build has not yet been qualified.

The ninth testcase, `GHGMais`, passes binary hydrology handling but its supplied text input contract does not match the supplied revision-53 source. PREP01 does not modify or synthesize that testcase to force execution.

Remaining hard gates are controlled immutable B0 byte retention, native or independently qualified equivalent reference-build semantics, capture of trusted unrounded reference output, exact `GHGMais` source/testcase provenance, and fuller 4.1.x theory/change documentation.

No ANIMO5 production process migration has started.

Top-level areas:

- `reference/`: cryptographically pinned legacy evidence identities and manifests;
- `src/`: future ANIMO5 production source, intentionally empty during PREP01;
- `tests/`: evidence-integrity and qualification-tooling tests;
- `docs/`: architecture, governance, PREP, testing and quality evidence;
- `tools/`: reproducible evidence/audit and legacy-exchange tooling;
- `integration/`: machine-readable work-unit, execution and qualification records.

No LICENSE is added until a legal basis is established. The public repository does not republish supplied legacy source/document bytes without an established redistribution basis.

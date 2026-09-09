# ANIMO5

Controlled modernization programme for the ANIMO soil-water-quality model.

The repository is bootstrapped evidence-first. Production migration does not start until the legacy source, documentation, reference behaviour, corrected-legacy baseline and migration qualification gates are explicitly satisfied.

Current preparatory evidence baseline:

`9df84bd0ab9bc4ef8e214f01da616aa257a24b13`

Baseline scope: `ANIMO-PREP01` through `ANIMO-PREP05`. `ANIMO-PREP06` is reserved for a source-bound conserved-state and transfer-ledger audit but is not part of the PREP01-PREP05 qualification scope.

ANIMO-RG01 stabilizes that evidence baseline and separates future work from the historical shared bootstrap branch.

Current scientific boundary:

- PREP01 remains `BLOCKED_REFERENCE_QUALIFICATION_CONTROLLED_B0_RETENTION_AND_GHG_PROVENANCE_REQUIRED`;
- PREP02 remains `BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`;
- PREP03 is qualified only as preparatory documentation/source reconciliation and architecture-preparation evidence;
- PREP04 is qualified only as source-bound and GNU diagnostic causal defect evidence;
- PREP05 is qualified only for its stated source-bound diagnostic synthetic causal, composition and non-interference scope;
- no qualified historical or independently admitted equivalent reference exists yet;
- no corrected-legacy source change is admitted;
- no ANIMO5 production process migration is admitted.

The supplied evidence classes remain separate:

- ANIMO 4.1.5 revision-53 source candidate, cryptographically pinned and member-inventoried;
- ANIMO 4.0 user's guide, cryptographically pinned and explicitly version-limited;
- nine-case ANIMO testbank, cryptographically pinned and inventoried.

The public repository does not republish the supplied legacy source archive or copyrighted documentation without an established redistribution basis. Controlled immutable B0 byte retention remains an open gate.

Top-level areas:

- `reference/`: legacy evidence identities, manifests and inventories;
- `src/`: future ANIMO5 production source, intentionally empty while production migration is blocked;
- `tests/`: evidence-integrity and qualification-tooling tests;
- `docs/`: architecture, governance, preparatory, testing, quality and regie evidence;
- `tools/`: reproducible evidence/audit, legacy-exchange and diagnostic-build tooling;
- `integration/`: machine-readable work-unit, execution, baseline and qualification records.

No LICENSE is added until a legal basis is established.

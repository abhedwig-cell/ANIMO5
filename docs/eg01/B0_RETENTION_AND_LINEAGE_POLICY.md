# ANIMO-EG01 B0 retention and lineage policy

Status: `CONTRACT_DEFINED_EXTERNAL_CONTROLLED_STORAGE_NOT_YET_PROVEN`

This policy defines how ANIMO5 evidence is classified, retained and traced. It deliberately separates public provenance metadata from controlled raw evidence storage. Git history and Git object hashes are useful provenance aids, but they are not the sole preservation mechanism for B0.

## Evidence classes

### `B0_RAW_IMMUTABLE`

Exact received artifact bytes accepted as baseline evidence. These bytes are never edited, normalized, repacked, renamed in-place or silently replaced. Public Git stores only identity/provenance metadata unless redistribution is explicitly authorized.

### `B0_MANIFEST`

Public or controlled metadata describing B0 identity: cryptographic digests, size, archive member manifests, relevant archive metadata, evidence role and provenance/custody references. A manifest is not a substitute for the raw B0 bytes.

### `WORKING_COPY`

Disposable or regenerable copy used for inspection, compilation, tests or analysis. It must trace to one B0 artifact or a named descendant. A working copy has no authority to redefine B0.

### `COMPATIBILITY_TRANSFORM`

A deterministic derivative created only to make legacy material executable or inspectable in another environment, for example line-ending conversion, compiler-compatibility edits, file-format conversion or extraction/repacking. Every transformed result receives its own digest and derivation record. It never replaces the parent B0 identity.

### `DIAGNOSTIC_OUTPUT`

Output generated for investigation, compiler/runtime probing or defect localization. Diagnostic output may reveal behaviour but is not a qualified reference oracle unless separately admitted.

### `REFERENCE_OUTPUT`

Output admitted by a dedicated reference-qualification gate against a declared B0 input lineage and reference environment. The label is prohibited until that gate is satisfied.

### `CORRECTED_LEGACY`

A source descendant in which a documented legacy discrepancy is deliberately changed and separately qualified. Corrected legacy is never relabelled as B0.

### `MIGRATED_ANIMO5`

ANIMO5 implementation descendants admitted through the migration/qualification process. They must remain traceable through corrected-legacy/reference evidence to the relevant B0 inputs.

## Public provenance metadata versus controlled raw evidence

Public Git may contain:

- evidence IDs and classes;
- filenames when disclosure is acceptable;
- byte sizes;
- SHA-256 values and algorithm identifiers;
- archive-member manifests and derived inventories that do not reproduce restricted content beyond what is legally permitted;
- provenance, custody-state and qualification-state metadata;
- non-secret opaque controlled-storage record IDs;
- transform and run lineage records;
- generated output hashes when publication is permitted.

Public Git must not contain, without explicit legal/redistribution authorization:

- raw source archives;
- raw testcase archives when redistribution status is uncertain or restricted;
- the full copyrighted documentation PDF;
- storage credentials, access tokens, encryption keys, confidential storage paths or access-control lists containing sensitive identities;
- copies that are functionally equivalent to restricted raw artifacts merely because they were unpacked or renamed.

## `B0_RAW_IMMUTABLE` minimum control contract

### Storage authority

A named organizational role, `B0 Evidence Custodian`, owns evidence acceptance and retention. A separate authorized storage administrator may operate the storage platform. ChatGPT, GitHub metadata and transient project storage are not storage authorities.

The custodian must confirm that retention and access comply with the legal basis applicable to each artifact. Until that confirmation exists, the register must record redistribution/legal status as unknown, restricted or pending rather than inferring permission.

### Write protection

At least one authoritative retained copy must use a control that prevents ordinary users and automation from overwriting or deleting an accepted object during its retention period. Acceptable mechanisms include storage-enforced WORM/object retention or equivalent controlled immutable media. A read-only filesystem flag or protected Git branch alone does not satisfy this requirement.

After ingest, the authoritative B0 object is addressed by evidence ID plus cryptographic digest. Any later byte difference creates a new evidence object and never an in-place replacement.

### Access policy

- least privilege;
- read access only for explicitly authorized project roles;
- ingest, retention-policy changes and deletion authority restricted to designated custodial roles;
- all administrative and read-access events auditable where the storage platform supports it;
- no public URL or anonymous access;
- credentials kept outside Git and outside lineage records.

If the storage platform supports separation of duties, retention-policy override or destructive action should require a different role from ordinary evidence readers.

### Checksum policy

For every B0 object:

1. compute SHA-256 from the received bytes before ingest;
2. compare with the public B0 register before acceptance;
3. compute or independently verify the digest after ingest using stored-object bytes, not only upload metadata;
4. record size in bytes;
5. preserve the algorithm identifier with the digest;
6. repeat verification after any restore or custody transfer;
7. perform scheduled integrity revalidation at least annually while the evidence remains active.

If future policy requires algorithm migration, add a new digest field after recomputing it from verified B0 bytes. Do not discard the historical SHA-256 identity.

### Backup and resilience

B0 is not considered durably retained with a single physical/logical copy. Minimum target:

- one authoritative immutable copy;
- one independently recoverable secondary copy in a separate failure domain;
- both copies tied to the same evidence ID and byte digest;
- backup/replication must preserve immutability expectations and must not silently normalize, recompress or otherwise transform the artifact bytes.

The exact platform, geography and retention period remain organizational decisions and must be recorded in the controlled custody record, not invented in public Git.

### Revalidation

Revalidation is mandatory:

- immediately before first controlled ingest;
- immediately after ingest;
- after any custody transfer;
- after any restore;
- after any storage migration;
- on the scheduled integrity cycle;
- before declaring B0 evidence available for a high-consequence reference or corrected-legacy qualification event when the previous verification is outside the locally defined freshness window.

A digest mismatch causes fail-closed quarantine. The object must not be used as B0 until the discrepancy is resolved against another independently verified retained copy and a custody incident record is created.

### Custody/provenance metadata

The controlled record for each B0 object must include at least:

- evidence ID;
- evidence class;
- supplied filename and byte size;
- SHA-256;
- date/time of receipt or first observation if known;
- source/provenance description without asserting unsupported ownership or authorship;
- evidence role: source, testcase or documentation;
- legal/redistribution status and reviewing authority;
- storage authority/custodian role;
- opaque primary and secondary storage record IDs;
- ingest timestamp;
- immutability/retention control type and proof reference;
- checksum verification events;
- custody transfers;
- restore tests and results;
- incident references;
- current retention state.

Public Git may carry a redacted subset. Secret locations, personal access-control data and credentials stay outside Git.

### Restore procedure

1. Custodian selects the evidence ID and expected SHA-256 from the public B0 register plus controlled custody record.
2. Restore is made into a quarantined read-only or non-authoritative staging area, never over an existing working copy.
3. Compute SHA-256 and size from restored bytes before extraction or execution.
4. If digest or size differs, stop. Quarantine the restore and open a custody incident. Do not repair or normalize the bytes.
5. If identity matches, create a new `WORKING_COPY` lineage record referring to the unchanged B0 evidence ID.
6. Any extraction, conversion, patching or compatibility processing occurs only after this verification and is recorded as `WORKING_COPY` or `COMPATIBILITY_TRANSFORM`.
7. The restored B0 object itself remains untouched.

A successful restore test must be recorded before the stronger EG01 status `QUALIFIED_CONTROLLED_IMMUTABLE_B0_RETENTION` can be used.

## Compatibility transforms

Compatibility transforms are descendants, not corrections to B0.

Every transform record must contain:

- transform ID;
- parent evidence ID and parent SHA-256;
- reason;
- exact transformation description or script/tool identity;
- toolchain/version when material;
- transformed output filename or logical name;
- output size;
- output SHA-256;
- whether semantic equivalence is claimed and the evidence supporting that claim;
- author/operator or automated workflow identity in the controlled audit record;
- creation timestamp.

Extracting files from a ZIP for build use creates a working representation. Repacking the same members into another ZIP creates a different byte object with a different digest and must not inherit the B0 archive identity.

## Input lineage for every test or model run

Every persisted run that may influence ANIMO5 evidence must have a machine-readable lineage record. At minimum it records:

- unique run ID;
- run purpose and evidence class of outputs;
- source evidence/descendant ID and digest;
- testcase/input evidence IDs and digests;
- documentation/theory IDs only when actually used as an interpretation basis;
- compatibility-transform IDs, if any;
- executable/binary digest when a binary was run;
- compiler/build-tool identity and relevant flags for built executables;
- operating-system/runtime/environment identity at the level required to reproduce the run;
- configuration and testcase selector;
- start/end or recorded execution timestamp where available;
- Git commit/branch for public harness or analysis code;
- output file digests or an output-manifest digest;
- qualification label, explicitly distinguishing diagnostic from reference output;
- known deviations, warnings and unresolved provenance gaps.

A run may not be promoted to `REFERENCE_OUTPUT` if its B0 input identity or any required compatibility transform is unrecorded.

## Derived-output lineage

Expected lineage chain:

```text
B0_RAW_IMMUTABLE
  + B0_MANIFEST
        -> WORKING_COPY
        -> optional COMPATIBILITY_TRANSFORM
        -> DIAGNOSTIC_OUTPUT
        -> qualified REFERENCE_OUTPUT
        -> qualified CORRECTED_LEGACY
        -> qualified MIGRATED_ANIMO5
```

This is a provenance relationship, not an automatic admission chain. Each stronger class requires its own gate.

## External actions required before immutable retention can be claimed

The current ChatGPT/GitHub environment can define metadata and validate the supplied bytes, but it cannot prove an organizational controlled storage platform has been provisioned with the required immutability, access and backup controls.

An authorized human custodian must therefore perform and record, outside public Git where appropriate:

1. legal/redistribution handling determination for each raw artifact;
2. selection/provisioning of the controlled primary and secondary storage targets;
3. authenticated ingest of the three exact B0 byte objects;
4. storage-enforced immutability/retention configuration;
5. access-control configuration and audit logging;
6. post-ingest hash verification from retained bytes;
7. independent secondary-copy verification;
8. a restore test from at least one retained copy followed by byte-hash verification;
9. custody record approval with non-secret proof references exported to the public register.

Until those steps are evidenced, the correct work-unit status is:

`QUALIFIED_B0_RETENTION_CONTRACT_IMPLEMENTATION_PENDING_EXTERNAL_CONTROLLED_STORAGE`

PREP01 and PREP02 must keep their B0 blocker active. Only after the controlled-storage proof fields are populated and independently checked may EG01 transition to:

`QUALIFIED_CONTROLLED_IMMUTABLE_B0_RETENTION`.

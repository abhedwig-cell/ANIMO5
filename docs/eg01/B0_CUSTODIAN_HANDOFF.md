# ANIMO-EG01 B0 custodian handoff

Status: `EXTERNAL_CONTROLLED_STORAGE_ACTION_REQUIRED`.

This handoff translates the EG01 retention contract into a concrete procedure for an authorized human or organizational evidence custodian. Completing this procedure is necessary before ANIMO-EG01 may claim `QUALIFIED_CONTROLLED_IMMUTABLE_B0_RETENTION`.

## Scope

The custodian must retain exactly these three supplied byte objects, without repacking, line-ending changes, renaming inside archives, format conversion, metadata rewriting or other transformation:

| Evidence ID | Role | Supplied filename | SHA-256 |
| --- | --- | --- | --- |
| `ANIMO-B0-SRC-41553-R53` | source | `ANIMO_4.1.5.53(3).zip` | `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` |
| `ANIMO-B0-TB-202609` | testcase package | `ANIMO_testbank.zip` | `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` |
| `ANIMO-B0-DOC-UG40-2005` | documentation | ANIMO 4.0 User's Guide PDF | `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301` |

The public repository must not receive these raw bytes unless redistribution authority is separately established.

## Required storage controls

The authoritative B0 copy must be stored under an organizationally controlled storage authority that provides, or is configured to provide, all of the following:

1. storage-enforced write protection after ingest, preferably object-lock/WORM or an equivalent retention mechanism;
2. least-privilege access limited to authorized custodians and explicitly authorized users;
3. auditable administrative and read/write events where the platform supports this;
4. retention policy that prevents ordinary overwrite or deletion during the required evidence lifetime;
5. an independent secondary copy in a separate failure domain;
6. documented restore capability for both the primary and secondary retention chain.

A read-only folder convention or a Git branch is not sufficient technical immutability.

## Ingest procedure

For each evidence object:

1. calculate SHA-256 directly from the original supplied bytes before ingest;
2. confirm that the digest equals the frozen digest above and in `integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json`;
3. ingest the exact object as a single preserved byte object;
4. enable the immutable/retention control before the object is considered retained;
5. calculate SHA-256 from the retained object after ingest, not merely from the upload source;
6. confirm equality with the frozen digest;
7. create or verify the independent secondary copy;
8. calculate SHA-256 from the secondary retained bytes;
9. record non-secret proof references and custody metadata.

If any digest differs, stop. Do not repair or normalize the object and call it B0. Treat the differing object as a separate descendant and investigate provenance.

## Restore qualification

At least one restore qualification must be executed after retention is configured.

The restore test must:

1. restore each of the three B0 objects from the controlled retention system to a temporary recovery location;
2. calculate SHA-256 on the restored bytes;
3. compare each result with the frozen B0 digest;
4. record success or failure independently for each evidence object;
5. remove the temporary recovery copy according to the organization's data-handling policy after verification.

A metadata-only check or cloud-provider status flag is not a restore test.

## Evidence to return to ANIMO5

Do not publish credentials, encryption keys, internal share paths, bucket URLs containing sensitive information, access tokens, or unrestricted download locations.

Return only non-secret evidence suitable for the public repository:

- storage authority/custodian role;
- opaque primary storage record ID;
- opaque secondary storage record ID;
- immutability/retention proof reference;
- ingest timestamp;
- post-ingest SHA-256 verification result;
- secondary-copy SHA-256 verification result;
- restore-test timestamp and result;
- custodian approval/reference;
- any restriction or retention-policy identifier that can safely be disclosed.

Use `integration/evidence/ANIMO_B0_STORAGE_PROOF_SCHEMA.json` for the machine-readable return record.

## Legal handling

EG01 establishes evidence-preservation procedure, not redistribution rights. The source and testcase redistribution basis is not established. The supplied ANIMO 4.0 User's Guide contains an explicit reproduction/storage restriction. Storage and access must therefore follow the applicable organizational authorization and copyright/licensing assessment.

A legal or access decision may restrict who can retrieve B0 while still allowing a public cryptographic identity record.

## Admission gate

The stronger status may be considered only after all three evidence objects have:

- proven primary immutable retention;
- proven independent secondary retention;
- matching post-ingest SHA-256 values;
- matching restored SHA-256 values;
- a custodian approval/proof reference.

Until then:

`QUALIFIED_B0_RETENTION_CONTRACT_IMPLEMENTATION_PENDING_EXTERNAL_CONTROLLED_STORAGE`

remains the maximum ANIMO-EG01 status, and PREP01/PREP02 B0 blockers remain in force.

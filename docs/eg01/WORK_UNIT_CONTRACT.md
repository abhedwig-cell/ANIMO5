# ANIMO-EG01 work-unit contract

Work unit: `ANIMO-EG01 — Controlled Immutable B0 Evidence Retention`

Parent branch: `work/animo-rg01-baseline-stabilization`

Parent SHA: `662bca8aff40f4dca1f6ccdde6bef6274c6bede2`

## Intended change

Define the governance and machine-readable evidence contract required to retain the exact supplied ANIMO baseline artifacts outside the public Git repository under controlled immutable storage, while preserving public provenance metadata and strict lineage from B0 through diagnostic, reference, corrected-legacy and migrated ANIMO5 results.

## Affected components

- evidence governance documentation;
- machine-readable B0 evidence register;
- run-lineage contract;
- EG01 status metadata.

No raw source archive, raw testcase archive or raw documentation PDF may be added to the public repository by this work unit.

## Scientific and numerical scope

- physics change: `NO`
- numerical-policy change: `NO`
- legacy source modification: `NO`
- testcase-byte modification: `NO`
- documentation-byte modification: `NO`
- reference admission: `NO`
- corrected-legacy admission: `NO`
- production migration admission: `NO`

## Evidence basis inspected

- `PROVENANCE.md`;
- `docs/prep01/EVIDENCE_INVENTORY.md`;
- `reference/source/source_manifest.csv`;
- `reference/testcases/testbank_manifest.csv`;
- source, testcase and documentation SHA-256 files;
- `docs/governance/DEVELOPMENT_GOVERNANCE.md`;
- `docs/reg/ANIMO-RG01_BRANCH_AND_INTEGRATION_PLAN.md`;
- `integration/animo-reg/ANIMO-RG01_STATUS.json`.

The PREP01 evidence inventory contains earlier blocker wording that predates later source/documentation availability. EG01 does not rewrite PREP01-owned history; the newer provenance and RG01 records define the current repository state.

## Frozen artifact identities

| Evidence ID | Role | Supplied filename | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| `ANIMO-B0-SRC-41553-R53` | source | `ANIMO_4.1.5.53(3).zip` | 350696 | `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` |
| `ANIMO-B0-TB-202609` | testcase package | `ANIMO_testbank.zip` | 7659314 | `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` |
| `ANIMO-B0-DOC-UG40-2005` | documentation | ANIMO 4.0 User's Guide PDF | 1169499 | `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301` |

The supplied project bytes were re-hashed during EG01 setup and matched these SHA-256 values. That verification only proves identity of the bytes available to this work unit. It is not evidence that controlled immutable external storage already exists.

## Deliverables

1. `docs/eg01/B0_RETENTION_AND_LINEAGE_POLICY.md`;
2. `integration/evidence/ANIMO_B0_EVIDENCE_REGISTER.json`;
3. `integration/evidence/ANIMO_RUN_LINEAGE_SCHEMA.json`;
4. `integration/animo-eg/ANIMO-EG01_STATUS.json`.

## Verification contract

The work unit qualifies only the retention contract when all of the following hold:

- the register contains no raw artifact bytes or secret storage credentials;
- all three frozen SHA-256 values match the repository provenance metadata and supplied bytes;
- evidence classes and derivation rules are explicit;
- compatibility transforms cannot overwrite or masquerade as B0;
- every future run must identify input evidence and transform lineage;
- duties that require an external authorized custodian are explicitly marked external and pending;
- status does not claim immutable storage unless independent custody, write-protection and restore evidence have actually been recorded.

## Checkpoint and qualification boundary

Persistence of this contract is the first checkpoint. Subsequent policy/register/schema files may be developed and validated independently of runtime/scientific execution.

Permitted terminal decision without external storage proof:

`QUALIFIED_B0_RETENTION_CONTRACT_IMPLEMENTATION_PENDING_EXTERNAL_CONTROLLED_STORAGE`

The stronger decision:

`QUALIFIED_CONTROLLED_IMMUTABLE_B0_RETENTION`

is prohibited until controlled raw storage, access control, immutable retention, backup and restore/revalidation evidence are all actually demonstrated by an authorized human custodian or equivalent controlled service evidence.

# ANIMO-MP01 work-unit contract

## Title

Macropore Activated-Path, Solute Exchange & Conservation Qualification

## Repository and branch

- repository: `abhedwig-cell/ANIMO5`
- branch: `work/animo-mp01-macropore-qualification`
- branch base: `f7f3722b14f65340dc6d67a8f80d74f5d0ebb158`
- base role: qualified partial TH02 release-lineage evidence, not a production baseline

## Scope

Qualify the revision-53 macropore subsystem before any production migration. The work unit covers:

- activation and input contract;
- Main Bypass Flow and Internal Catchment semantics;
- macropore water storage;
- dissolved-solute storage for DOM, DON, DOP, NH4-N, NO3-N and PO4-P;
- matrix/macropore exchange;
- direct rapid drainage;
- boundary inputs;
- conservation identities;
- accepted/result state promotion and restart serialization;
- activated-path reassessment of `TCD-025`.

## Evidence pins

Frozen artifacts must remain unchanged.

- ANIMO 4.1.5 revision 53 source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- supplied testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- supplied ANIMO 4.0 guide SHA-256 as recorded by upstream work: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

Upstream evidence is branch/head specific:

- TH01: `work/animo-th01-rev53-theory-provenance` at `a3360415364ef4a66a81d7b6715bcd400829df1b`
- TH02: `work/animo-th02-rev41-lineage-recovery` at `f7f3722b14f65340dc6d67a8f80d74f5d0ebb158`
- PREP06: `work/animo-prep06-conserved-state-ledger` at `9b1f1ea51c24fb82823290193651830dc61ea3c8`
- TQ01: `work/animo-tq01-testcase-qualification` at `5c43ee16df37a0a1357614fdec527f25e5ca8c16`

These branches are divergent evidence branches. MP01 consumes their qualified findings without pretending they form one merged source tree.

## Evidence classes

Every conclusion must distinguish:

- `SOURCE_SUPPORTED`
- `THEORY_SUPPORTED`
- `B1_CAUSALLY_EXERCISED`
- `B2_HISTORICALLY_REFERENCED`
- `B3_READY`

Synthetic or transformed cases are diagnostic evidence only. They cannot become historical B2 evidence.

## Required diagnostic cases

Design controlled B0-derived descendants for:

1. storage only;
2. matrix/macropore exchange;
3. direct drainage;
4. solute input/transfer;
5. no-macropore negative control.

Source-level diagnostic probes may additionally isolate the frozen revision-53 kernels. Such probes remain `SYNTHETIC_DIAGNOSTIC_ONLY` and must not be described as historical whole-model cases.

## Non-goals and prohibitions

- no production implementation;
- no modification of frozen source or testbank;
- no corrected `TCD-025` implementation;
- no support claim from source presence alone;
- no B2 claim from synthetic evidence;
- no `B3_ADMITTED` status without a separate admission decision.

## Target deliverables

- `docs/macropore/MACROPORE_PROCESS_MODEL.md`
- `docs/macropore/MACROPORE_ACTIVATION_CONTRACT.md`
- `docs/macropore/MACROPORE_CONSERVATION_IDENTITIES.md`
- `docs/macropore/TCD025_QUALIFICATION.md`
- `integration/animo-macropore/ANIMO-MP01_STATUS.json`

Qualification-only diagnostic tooling and machine-readable evidence may be added when needed for reproducibility.

## Target closeout state

If source, theory and causal B1 path evidence are sufficient while historical active-reference evidence remains absent:

`QUALIFIED_MACROPORE_SOURCE_THEORY_AND_DIAGNOSTIC_PATH_EVIDENCE_HISTORICAL_REFERENCE_OPEN`

This is not a B3 admission.

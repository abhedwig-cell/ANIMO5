# ANIMO-MP02 — B0-derived Whole-Case Macropore Activation Qualification

Status: `IN_PROGRESS`

Base: `ANIMO-MP01` head `7b5979dd6301b9d55d23e8c22948a0dba24b229b`.

## Purpose

Execute the positive whole-case diagnostic descendants designed by MP01 against the frozen revision-53 source and frozen testbank, without modifying either frozen artifact and without promoting synthetic descendants to historical B2 evidence.

## Frozen identities

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- parent case: `CranGrass`

## Diagnostic cases

1. `MP02-NO-MP` negative control, exact B0 parent inputs under the existing GNU diagnostic runtime adapter.
2. `MP02-STORAGE` active macropore storage path.
3. `MP02-EXCHANGE` active matrix/macropore exchange path.
4. `MP02-DIRECT-DRAIN` active Main Bypass direct drainage path.
5. `MP02-SOLUTE-N` active NH4/NO3 solute transport path.
6. `MP02-SOLUTE-P` P-active DOP/PO4 path if the parent contract can be transformed without unrelated semantic changes.

## Evidence rules

- descendants are `SYNTHETIC_DIAGNOSTIC_ONLY`;
- every changed input record must be captured in an exact transform manifest;
- no synthetic output is B2 historical reference evidence;
- no TCD-025 correction is allowed in this workunit;
- no production implementation is allowed;
- fail closed on source/testbank hash mismatch;
- preserve MP01 activation semantics: detailed hydrology, `Ioptmp=1`, `Hlpimp=2`, dynamic reachability through nonzero macropore geometry.

## Qualification questions

- Does a complete ANIMO run reach the active macropore hydrology route?
- Does a complete run reach macropore solute transport for N, and where feasible P?
- Are specialized macropore water and solute balances numerically closed on full orchestration?
- Does the main/public ledger exhibit the TCD-025 gap under a complete active run?
- Are negative-control outputs stable under the diagnostic harness?
- Which activation and restart blockers remain after complete-case B1 exercise?

## Planned deliverables

- `docs/macropore/MP02_WHOLE_CASE_DESIGN.md`
- `docs/macropore/MP02_WHOLE_CASE_RESULTS.md`
- `integration/animo-macropore/ANIMO-MP02_TRANSFORMS.json`
- `integration/animo-macropore/ANIMO-MP02_DIAGNOSTIC.json`
- `integration/animo-macropore/ANIMO-MP02_STATUS.json`

## Admission boundary

A successful MP02 run raises only complete-case B1 causal evidence. It does not establish `B2_HISTORICALLY_REFERENCED`, `B3_READY`, `B3_ADMITTED`, or production migration readiness.

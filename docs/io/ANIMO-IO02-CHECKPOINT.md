# ANIMO-IO02 checkpoint

Status: `IN_PROGRESS_PERSISTED_SOURCE_CONTRACT_EXTRACTION`

## Work unit

`ANIMO-IO02 — GENERAL.INP Strict Legacy Grammar, Ordering & Normalized Representation Qualification`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-io02-general-input-normalization`

Upstream ANIMO-IO01 closeout head:

`2bcf65360b08d278f28f1cc61ac96714db4793a3`

## Frozen identities

Primary executable contract authority is the frozen revision-53 source archive:

- `ANIMO_4.1.5.53.zip` SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- frozen ANIMO testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- supplied ANIMO documentation SHA-256 inherited from IO01: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

IO02 does not modify frozen source/testbank bytes.

## Scope boundary

In scope:

- revision-53 `GENERAL.INP` only;
- exact section-label sequence and parser call order;
- line-oriented option grammar and sequential ordering dependencies;
- conditional fields and feature-gated GENERAL sections;
- repeated balance structures and output-selection structures;
- parser defaults, range/error behaviour, EOF/missing-label behaviour;
- lexical numeric conversion semantics required for a field-exact normalized representation;
- mapping to bounded normalized `ModelConfiguration`, `SimulationWindow` and `DiagnosticsConfiguration` records;
- representation-only equivalence properties.

Explicitly out of scope:

- production input migration;
- redesign or relaxation of GENERAL grammar;
- silent default insertion beyond source-observed legacy defaults;
- GHGMais schema admission or generic GHG normalization;
- binary hydrology;
- INITIAL/restart/checkpoint parsing;
- broad reopening of IO01;
- scientific/numeric policy delegated to TTUTIL.

## Initial source-bound observations

Revision-53 `input1.for` identifies ANIMO 4.1 GENERAL parsing by `AnimoVersion = 41`. The GENERAL reader calls `Findadr` for top-level labels in this source order:

1. `>simopt:`
2. `>simtim:`
3. `>outscr:`
4. `>outbal:`
5. `>outsel:`
6. `>outtot:`
7. conditional `>outGHG:` when `IoptGHG >= 1`

`Findadr` rewinds the file before every label search and requires exact equality of the first eight characters. Therefore top-level label blocks are located independently, but the records consumed *within* each located block are sequential and order-sensitive.

Within ANIMO 4.1 blocks, `ReadOp`, `ReadTs`, `Readvals` and `Readints` consume exactly the next formatted text record. They compare the record prefix through the first `=` with the expected option name. These helpers do not search forward for a missing or reordered option. This is the primary reason GENERAL cannot be represented as an unordered key/value map without changing legacy semantics.

Observed legacy defaults already source-bound in `GENERAL.INP` parsing:

- missing/mismatched `PClassOption=` is converted to `IoptPCl = 0` and clears `Error`;
- when `IoptPCl != 1`, `PClYrSw = 0` is assigned;
- missing/mismatched `HydroYearSwitch=` is converted to `HydrYrSw = 0` and clears `Error`;
- `ReadTs` treats missing `AnnDOMNtotNO3_1mGWL=` and `DOMNtotNO3_1mGWL=` specially as disabled output rather than fatal parser error.

No other defaults are admitted at this checkpoint.

## Representation policy under test

IO02 will not normalize GENERAL into a free-order property bag. The candidate representation must retain at least:

- canonical field identity;
- section identity;
- exact legacy sequence index within a section;
- repeated-group occurrence index where applicable;
- explicit/defaulted/inactive status;
- source lexical token and source location;
- source-observed feature condition;
- target object/path.

The normalized values may be projected into bounded typed target objects only after the legacy parser contract has been preserved and validated.

## Next qualification steps

1. extract the complete revision-53 GENERAL grammar and section/field sequence into a machine-auditable manifest;
2. characterize all conditional/repeated branches, including `NumberOfPrintBal`, `PrintBalNoUpd`, `SelectedComp`, `IntMedOutputTS`, `PClassOption`, and `IoptGHG` routing;
3. build negative probes for reordered fields, missing labels, missing ordered fields, EOF, malformed lexical values and conditional-field omissions;
4. compare normalized projection of natural non-GHG testbank GENERAL files;
5. persist a qualification result before any production-migration discussion.

## Current decision

`NOT_YET_QUALIFIED`

This checkpoint is intentionally persisted before running the full qualification suite.
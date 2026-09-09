# GENERAL.INP strict revision-53 input contract

Status: `QUALIFIED_BOUNDED_REPRESENTATION_CONTRACT`

Work unit: `ANIMO-IO02`

This document defines the bounded normalized-representation contract qualified for revision-53 `GENERAL.INP`. It is not a production parser specification and does not authorize input migration.

## Authority

Primary executable contract authority is the frozen revision-53 source:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- source member: `ANIMO_4.1.5.53/input1.for`;
- source revision: 53;
- supplied Intel project SHA-256: `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`;
- supplied project compiles `input1.for` with `RealKIND="realKIND8"`.

The ANIMO user documentation is corroborating documentation only. Where its older input description differs from revision-53 executable behaviour, IO02 preserves the revision-53 behaviour.

The complete machine-auditable field manifest is `integration/animo-io/GENERAL-REV53-GRAMMAR.json`.

## Core ordering rule

Revision-53 calls `Findadr` for the main GENERAL sections in this logical order:

1. `>simopt:`
2. `>simtim:`
3. `>outscr:`
4. `>outbal:`
5. `>outsel:`
6. `>outtot:`
7. `>outGHG:` only when `GreenHouseGasOption >= 1`

This call order is not the same thing as a requirement that complete top-level blocks occur in that physical file order. `Findadr` rewinds before each lookup and compares the first eight characters exactly. A complete block can therefore be moved relative to another complete block and still be found.

Ordering becomes strict after a label has been found. `ReadOp`, `ReadTs`, `Readvals` and `Readints` consume the next record. They do not search forward for a matching key. A normalized GENERAL representation therefore may not turn the legacy input into a free-order property bag.

## `>simopt:`

The sequential revision-53 fields are:

`HydrologicInput=`
`PhosphorusCycle=`
`SulphateSimulation=`
`AerationModel=`
`CropUptakeModel=`
`MacroPoreOption=`
`GreenHouseGasOption=`
`SoilTempFile=`
`PClassOption=`

When `PClassOption=1`, these records follow immediately:

`PClassYearSwitch=`
`PClass=`

The source-observed compatibility rule for a mismatch at `PClassOption=` is unusual but qualified: the attempted record is consumed by `ReadOp`, the caller clears the parser error, and `IoptPCl` becomes 0. IO02 records that state as `DEFAULTED` with rule `GEN-DEF-PCLASSOPTION-0`. It does not generalize this behaviour to other options.

When `PClassOption != 1`, the source assigns `PClassYearSwitch=0` and does not read `PClass=`. The normalized representation records the former as a source-defined default and the latter as inactive.

## `>simtim:`

Revision-53 consumes two raw date records followed by `HydroYearSwitch=`.

The source does not validate the lexical names `StartDate=` and `EndDate=` in the same way as `ReadOp`. Its date extraction is positional. IO02 qualifies only the bounded layout observed in the admitted natural files, with a `YYYY-MM-DD` token in the revision-53 fixed position. It does not claim that arbitrary malformed positional records have useful semantics.

A mismatch at `HydroYearSwitch=` follows a source compatibility path comparable to `PClassOption=` and results in `HydrYrSw=0` after the error is cleared.

There is also a source defect that is part of the executable input contract: after reading `HydroYearSwitch=`, revision-53 range-checks `IoptPCl` instead of `HydrYrSw`. The natural LWKM fixture contains `HydroYearSwitch=-30` and this value is preserved by the qualified representation. IO02 does not silently impose a new range check.

## `>outscr:`

`ProgressToScreen=` is read sequentially by `ReadOp` and checked in the source range 0 through 3.

## `>outbal:` repeated structures

`NumberOfPrintBal=` gives the number of repeated balance structures.

Each repeated structure is sequential:

`PrintBalLabel=`
`PrintBalWater=`
`PrintBalOrgMat=`
`PrintBalNitrogen=`
`PrintBalPhosphor=`
`PrintBalSulphate=`
`PrintBalTopLay=`
`PrintBalBotLay=`
`PrintBalNoUpd=`
`PrintBalUpdDate=` when required by the update count

`PrintBalLabel=` is not handled by the normal option helper. A prefix mismatch causes `Input1` to return without assigning the normal parser error. The qualification observer preserves that as an explicit non-normalized failure path rather than inventing an error code.

`PrintBalUpdDate=` is present when `PrintBalNoUpd` is neither -1 nor 0. Revision-53 sorts the values in place after parsing. The normalized semantic value therefore contains the sorted binary64 values, while the source lexical record is retained separately as provenance.

The source uses the `999` sentinel in `Checkint` for `PrintBalNoUpd`, which disables its lower-bound test. Values below -1 are consequently not rejected there, but they do not define a safe normalized repeat cardinality. IO02 refuses to assign them new repeat semantics.

## `>outsel:` and `ReadTs`

The section starts with `SelectedComp=`. If that value is at least 1, `CompartmentNo=` follows with that cardinality.

Revision-53 then consumes one separator record before each output group. The text in those separator records is not a scientific value, but consuming one record is part of the cursor contract and therefore part of the grammar.

The seven groups are, in order:

1. Hydrology
2. Nitrogen
3. Phosphorus
4. OrganicMatter
5. Aeration
6. GreenHouseGasses
7. WholeProfile

The complete ordered selector list and associated legacy `Outse` indexes are frozen in `integration/animo-io/GENERAL-REV53-GRAMMAR.json`.

`ReadTs` is not ordinary integer conversion. After validating the ordered key prefix, it scans the remainder of the record for the first character `0`, `1`, `2` or `3`. That first digit controls two flags:

- `0`: file 0, selected-compartment 0;
- `1`: file 1, selected-compartment 0;
- `2`: file 0, selected-compartment 1;
- `3`: file 1, selected-compartment 1.

Because the scan continues through the record, a digit in comment text can be the selected value. The qualified normalized observer preserves this lexical behaviour. Replacing it with a conventional integer parser would be a grammar change.

Two late WholeProfile records have a source-specific fallback:

`AnnDOMNtotNO3_1mGWL=`
`DOMNtotNO3_1mGWL=`

On mismatch the source sets file output to 0 and clears `Error`, but it does not assign the corresponding selected-compartment flag. IO02 therefore records file output 0 while marking the second flag `LEGACY_UNDEFINED_IF_OMITTED`. It does not fabricate zero.

There are related legacy storage hazards for several WholeProfile selectors whose second flag is read into `idum` while a later global range check still inspects the `OutseLn` array. Those storage states are not input-defined values and are excluded from the normalized representation claim.

## `>outtot:`

`IntMedOutputTS=` is read first. When it is 0, revision-53 then consumes:

`NumIntMedOutputTS=`
`IntMedOutFromStart=`

The second record has cardinality `NumIntMedOutputTS`. When `IntMedOutputTS=1`, these fields are not read and are represented as inactive, not silently defaulted configuration.

## GHG routing boundary

The GreenHouseGasses selector group inside `>outsel:` is part of the revision-53 GENERAL sequence even when GHG physics is inactive.

The separate `>outGHG:` section is different. Revision-53 attempts to find it only when `GreenHouseGasOption >= 1`. IO02 records that route but does not normalize or admit its payload. GHGMais remains outside the qualified schema.

## Missing labels, EOF and malformed records

A missing top-level label found through `Findadr` is represented by the revision-53 missing-label contract, including source error 1995.

A required `ReadOp`/`Readints`/`Readvals` record that is absent or in the wrong sequential position remains an input failure. A required `ReadTs` key mismatch remains the source 9871 path except for the two explicit optional late-output cases described above.

IO02 does not turn EOF, malformed records, source bugs or uninitialized storage into scientific defaults.

## Lexical numeric representation

For the supplied revision-53 build context, `Readvals` feeds default REAL variables compiled under `RealKIND="realKIND8"`. The bounded normalized observer therefore uses binary64 for those GENERAL real values. This is executable representation evidence, not a claim that TTUTIL defines ANIMO numerical semantics.

There is no blanket floating tolerance in IO02. Lexical source form is retained separately from the typed semantic value.

## Normalized representation

The qualified record model retains at least:

- canonical field identity;
- section identity;
- sequence index within the section;
- repeat index where relevant;
- typed value;
- `EXPLICIT`, `DEFAULTED` or `INACTIVE_NULL` presence state;
- source line and lexical form;
- feature condition;
- legacy parser path;
- typed target object and target path.

The admitted projections are limited to:

- `ModelConfiguration`;
- `SimulationWindow`;
- `DiagnosticsConfiguration`.

This follows the IO01 rule that parsing must not return one mutable mega-object spanning unrelated configuration, state, forcing and restart concerns.

## Equivalence claim

For admitted revision-53-compatible non-GHG GENERAL files, IO02 qualifies semantic representation equivalence at the parser boundary. The candidate representation preserves the typed configuration and diagnostics projection, source-observed compatibility defaults, sequential repeated structures, feature conditions and lexical/order provenance.

IO02 does not claim byte-for-byte text round-trip identity. Comments and formatting need not be regenerated identically for semantic equivalence. Conversely, a serializer or adapter may not exploit that fact to reorder sequential records, insert defaults, remove required separator records or otherwise broaden the accepted grammar.

## Natural testbank evidence

Nine GENERAL files occur in the frozen testbank.

Seven non-GHG files satisfy the bounded revision-53 representation contract:

- CranGrass;
- CranMais;
- LWKM grass;
- Puitmijn Cranendonck;
- RuurloGrass;
- STONE akkerbouw;
- Zuiderzeeland MeeuwenTocht.

`GrassPeat` is negative evidence. Its output-selection sequence contains `WFPS=` where revision-53 expects `O2_content=`. IO02 does not reinterpret that file as valid revision-53 GENERAL grammar.

`GHGMais` is excluded because the GHG schema is explicitly outside IO02 admission.

The detailed file-by-file and mutation-probe evidence is persisted in `integration/animo-io/ANIMO-IO02-QUALIFICATION.json`.

## TTUTIL boundary

TTUTIL 4.27 provenance remains inherited from IO01 and may be used as parser infrastructure in later work. IO02 does not make TTUTIL the authority for GENERAL ordering, defaults, feature activation, integer selection semantics or floating-point policy.

Any future TTUTIL-based GENERAL adapter must be constrained so that it cannot accept an ordering or default that revision-53 would not admit within the qualified scope.

## Non-admissions

ANIMO-IO02 does not authorize:

- production input migration;
- GENERAL grammar redesign;
- free ordering of sequential GENERAL records;
- silent default insertion beyond the source-observed rules qualified here;
- GHGMais or generic GHG schema admission;
- binary hydrology conversion;
- INITIAL, restart or checkpoint migration;
- broad reopening of IO01;
- TTUTIL as scientific or numerical authority;
- normalization of undefined legacy storage into fabricated values.

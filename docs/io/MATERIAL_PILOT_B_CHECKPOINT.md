# ANIMO-IO01 Pilot B closeout: bounded non-GHG MATERIAL core

Status: `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS`

## Scope

Pilot B is a bounded follow-on to DIRECT Pilot A. It is restricted to the revision-53 static `MATERIAL.INP` contract exercised by the natural non-GHG `RuurloGrass` case with:

- `PhosphorusCycle = 0`;
- `AerationModel = 0`;
- `GreenHouseGasOption = 0`;
- `PClassOption = 0`;
- `Nm = 11`;
- `Nf = 14`.

It does not include GHGMais, does not infer a cross-lineage GHG schema, does not change scientific equations and does not admit production migration.

Frozen B0 source and testbank bytes remain unchanged.

## Qualified parser surface

The active revision-53 sections are:

1. `>defmat:`
2. `>orgcom:`
3. `>deffra:`
4. `>defexu:`
5. `>defdom:`
6. `>defsdo:`
7. `>defhum:`
8. `>defntr:`
9. `>defden:`
10. `>matfra:`

`>sonicg:`, `>sonic2:` and post-`>matfra:` GHG validation are outside this pilot.

Legacy exact first-eight-character `Findadr` lookup and first-duplicate-section-wins remain compatibility semantics. The native TTUTIL v1 representation is a separate schema and does not inherit those quirks.

The normalized target is `MaterialParameterSet/v1`.

## Sparse FR / FRca semantics

Natural testbank lineage supplies both:

- `RuurloGrass/Input/MATERIAL_oud.INP`, with full 11 x 14 matrices;
- `RuurloGrass/Input/MATERIAL.INP`, with sparse `>matfra:` triples.

The persisted lineage audit proves:

- 154 cells per matrix;
- 24 explicitly represented sparse triples;
- 130 omitted cells per `FR` matrix and 130 per `FRca` matrix;
- filling omitted sparse cells with numeric zero makes the new `FR` matrix field-exact to the old full `FR` matrix;
- the same is true for `FRca`;
- the other cross-version fields recorded in the lineage evidence are also exact.

Therefore the intended normalized Ruurlo semantics are:

`omitted sparse (material,fraction) entry -> 0`

This is input-lineage evidence. It does not qualify the legacy runtime storage mechanism that happened to back the omitted array cells.

## IPO=0 presence semantics

For `IPO=0`, revision 53 consumes zero `Frpo` values from `>defmat:` and zero `Pofr` values from `>deffra:` through the conditional implied-DOs.

The trailing zero columns in natural Ruurlo are therefore lexical residue and do not become active phosphorus state.

Pilot B normalizes:

- material `Frpo` as `FEATURE_INACTIVE_NULL`;
- fraction `Pofr` as `FEATURE_INACTIVE_NULL`.

`Pofrex` and `Pofrhuma` remain explicit parsed fields because revision 53 reads them unconditionally from their own sections.

## TTUTIL numerical qualification

A direct typed TTUTIL 4.27 DOUBLE route is not field-exact for the natural Ruurlo case. The persisted comparison contains 26 numeric leaves that differ by exactly one binary64 ULP, with maximum absolute difference `1.1102230246251565e-16`.

No epsilon or tolerance is used to hide this.

The admitted candidate instead uses TTUTIL only for name-based CHARACTER scalar/array token retrieval. The adapter then performs explicit `REAL(8)` list-directed numeric conversion. That route produces field-exact `MaterialParameterSet/v1` semantics for the bounded case.

This keeps TTUTIL as parser infrastructure and prevents its numeric conversion implementation from becoming accidental ANIMO scientific authority.

## Runtime hazard exclusions

Two revision-53 runtime/storage hazards remain excluded from the representation claim.

### MAT-RH-001

Revision 53 assigns only explicit sparse `FR` / `FRca` cells and subsequently reads all cells. No explicit source initialization of omitted cells has been identified before those reads.

Disposition:

- intended normalized omitted-cell value: `0`, qualified by natural old/new lineage;
- legacy storage mechanism: `UNQUALIFIED`;
- routing: `ANIMO-BUILDQ01/B3I01`;
- migration rule: materialize zero explicitly rather than reproduce compiler or storage accidents.

### MAT-RH-002

At `IPO=0`, revision 53 reads no `Pofr(Frno)` input value but nevertheless range-checks `Pofr(Frno)`.

Disposition:

- normalized input presence: `FEATURE_INACTIVE_NULL`;
- checked legacy runtime value: `NOT_INPUT_DEFINED`;
- routing: `ANIMO-BUILDQ01/B3I01`;
- migration rule: do not invent a persistent value to imitate undefined storage.

No local canonical TCD number is assigned by IO01.

## Evidence and implementation

Persisted evidence:

- `integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json`;
- `integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json`;
- `integration/animo-io/MATERIAL-PILOT-B-STATUS.json`;
- `docs/io/MATERIAL_PILOT_B_RUNTIME_HAZARD_ROUTING.md`.

Implementation/qualification tooling:

- `tools/audit_material_ruurlo_lineage.py`;
- `tools/io01_material_pilot.py`;
- `tools/ttutil_material_probe.f90`;
- `tools/ttutil_material_probe_typed_double.f90`;
- `tools/qualify_io01_material_pilot.py`;
- `tests/io/test_io01_material_pilot.py`.

The qualification runner was hardened at commit `75c74dd710ab5804444f2be484c0edf5124a568b`. It can now start from the user-supplied frozen SWAP 4.3.1 and ANIMO testbank ZIPs, verify their hashes, materialize and build the exact official TTUTIL 4.27 source, build both probes, and additionally compare every numeric lexeme in the natural Ruurlo MATERIAL file bitwise against GNU Fortran external list-directed `REAL(8)` conversion.

GitHub Actions run `34336915868` passed for that hardened source-level qualification surface. The archive-dependent runtime reproduction is intentionally not run in GitHub CI because the frozen/user-supplied ZIP bytes are not vendored.

The persisted `MATERIAL-PILOT-B-QUALIFICATION.json` remains the recorded v1 runtime observation. The hardened runner emits v2 evidence on a future clean rerun; changing the reproducer does not silently upgrade or replace the already-recorded evidence.

## Admission boundary

Pilot B is qualified only as:

`QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS`

It does not admit:

- generic MATERIAL migration;
- GHG MATERIAL schema support;
- model-output equivalence;
- binary hydrology conversion;
- production input migration;
- B4.

No further input-family pilot is required to satisfy the original IO01 objective. Additional families should be selected only through a separate bounded follow-on decision.

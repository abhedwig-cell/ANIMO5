# ANIMO-IO01 Pilot B checkpoint: non-GHG MATERIAL core

Status: `STARTED_SOURCE_CONTRACT_RECONSTRUCTION`

## Scope

Pilot B is a bounded follow-on to the qualified DIRECT Pilot A. It is restricted to the revision-53 static `MATERIAL.INP` contract exercised by the natural non-GHG `RuurloGrass` case.

It does not include GHGMais, does not infer a cross-lineage GHG schema, does not change scientific equations and does not admit production migration.

## Authority and frozen evidence

The Pilot B analysis continues on `work/animo-io01-legacy-text-input-contracts` after DIRECT Pilot A.

Frozen B0 identities were rechecked before local inspection:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

No frozen bytes were modified.

The active natural case has, in `GENERAL.INP`:

- `PhosphorusCycle=0`;
- `AerationModel=0`;
- `GreenHouseGasOption=0`;
- `PClassOption=0`.

Its static material file is `RuurloGrass/Input/MATERIAL.INP`.

## Revision-53 active MATERIAL sections for RuurloGrass

Source: `input1.for`, MATERIAL block beginning near the `>defmat:` lookup.

The case exercises these required `Findadr` sections:

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

`>sonicg:` and `>sonic2:` are inactive because `Ioptae=0`. The post-`>matfra:` GHG validation is inactive because `IoptGHG=0`.

All listed active sections are found with `Findadr`, so section order is not the semantic ordering constraint. Exact first-eight-character label lookup and first-duplicate-section-wins remain part of the legacy grammar.

## Natural dimensions

RuurloGrass declares:

- `Nm = 11` materials;
- `Nf = 14` organic fractions;
- `IPO = 0` for the phosphorus cycle.

`>matfra:` is sparse: each material declares `NuFR` followed by `NuFR` triples `(frno, FR, FRca)`, and the list-directed read may continue across multiple physical records.

## Important parser-contract findings

### 1. Conditional implied-DO fields leave trailing lexical values unused when IPO=0

Revision 53 reads `>defmat:` as:

`Mty, Mn, Fror(Mn), Frnh(Mn), Frni(Mn), (Frpo(Mn), j=1,IPO)`.

With `IPO=0`, no `Frpo` value belongs to the input list. The natural RuurloGrass rows nevertheless contain a trailing sixth value (`0.`). List-directed input satisfies the shorter input list and does not make that lexical value part of normalized `Frpo` state.

The same pattern occurs in `>deffra:`. Revision 53 reads `Pofr(Frno)` only through an implied DO from 1 to `IPO`, while RuurloGrass carries a trailing zero column with `IPO=0`.

A native TTUTIL schema must not silently reinterpret these ignored legacy lexical residues as active phosphorus fields.

### 2. Other phosphorus-named values are read unconditionally

`pofrex` in `>defexu:` and `Pofrhuma` in `>defhum:` are read and range-checked regardless of `IPO`. They therefore remain part of the revision-53 parser contract even when phosphorus simulation is inactive. Scientific use and parser presence are separate questions.

### 3. Sparse `FR` / `FRca` assignment exposes an initialization dependency

After each sparse `>matfra:` row, revision 53 validates **all** `FR(Mn,Fn)` for `Fn=1..Nf`, sums all `FR(Mn,Fn)`, and then validates all `FRca(Mn,Fn)` for `Fn=1..Nf`.

The MATERIAL block itself does not initialize the unassigned entries to zero before these full-array reads. `FR` and `FRca` are main-program arrays passed into `Input1` and no explicit zero assignment has yet been found in the frozen source before the MATERIAL block.

This is not yet classified as a new defect. It is a runtime-semantics dependency candidate that must be reconciled with ANIMO-BUILDQ01 before Pilot B can claim exact legacy normalization for omitted sparse entries.

BUILDQ01 already states that no migrated read may rely on compiler zero fill, prior storage contents or operating-system page state. PREP01's deterministic GNU diagnostic recipe uses `-fno-automatic`, but does not define scientific zero initialization.

Until the exact legacy meaning of unassigned `FR` / `FRca` entries is qualified, Pilot B must fail closed rather than invent zeros merely because a diagnostic executable happens to observe them.

## Next qualification steps

1. qualify the sparse `FR` / `FRca` initialization dependency against BUILDQ01 and diagnostic runtime evidence;
2. define a narrow `MaterialParameterSet/v1` normalized schema with exact dimensions and source provenance;
3. distinguish parsed-but-scientifically-dormant fields from feature-conditional absent fields;
4. implement the revision-53 MATERIAL oracle for the RuurloGrass active schema;
5. implement a separately versioned TTUTIL native MATERIAL v1 representation;
6. compare every scalar, index, cardinality, sparse mapping and presence rule before model-output regression.

No Pilot B representation claim is admitted by this checkpoint.

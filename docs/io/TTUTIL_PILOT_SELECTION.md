# TTUTIL pilot selection and qualification

## Result

Two bounded representation pilots are now qualified as candidates:

- Pilot A, `DIRECT/animo.ini` -> `LegacyInputBinding/v1`:
  `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE`;
- Pilot B, non-GHG Ruurlo `MATERIAL.INP` -> `MaterialParameterSet/v1`:
  `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS`.

Both classifications are deliberately narrow. Neither admits production input migration, a general TTUTIL replacement for revision-53 input, binary hydrology conversion, restart/configuration conflation, GHG schema normalization, model-output equivalence or B4.

## Pilot A: DIRECT/animo.ini routing contract

Two separate representation contracts are preserved:

- `LegacyRevision53TextAdapter` for the historical A4/A80 DIRECT grammar;
- `TTUTILNativeTextAdapter/v1` for a new versioned, name-based TTUTIL representation.

The native representation is not a drop-in parser for legacy files. It is a second representation that normalizes to the same narrow object.

### Runtime qualification

The reproducible qualification harness is:

- `tools/io01_direct_pilot.py`;
- `tools/materialize_ttutil427.py`;
- `tools/ttutil_direct_probe.f90`;
- `tools/qualify_io01_direct_pilot.py`;
- `tests/io/test_io01_direct_pilot.py`.

The committed evidence is `integration/animo-io/DIRECT-PILOT-QUALIFICATION.json`.

Against the frozen ANIMO testbank:

- natural `animo.ini` cases: 10;
- field-exact semantic equivalence passes: 10/10;
- normalized object: `LegacyInputBinding/v1`;
- TTUTIL version: 4.27;
- exact SWAP 4.3.1 package SHA-256: `2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`;
- embedded TTUTIL archive SHA-256: `ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193`;
- TTUTIL files verified: 168;
- Fortran compilation units built: 153;
- qualification compiler: GNU Fortran 14.2.0.

GHGMais is included only at the routing-object level. This does not qualify the incompatible GHG input schema or erase its lineage issue.

### Legacy behaviour retained or made explicit

The compatibility normalizer preserves the defined revision-53 DIRECT behaviour needed by Pilot A, including exact `Animo40` / `Animo41` header recognition, A4/A80 selector records, defined `Strip` behaviour, last-wins known duplicates, legacy ignore-unknown behavior with diagnostics, the `message.Out` default, mandatory GEN validation and CHE/STE presence flags.

The native TTUTIL schema fails closed on duplicate keys, unknown keys and missing mandatory `SchemaVersion`, `AnimoVersion` or `GEN`.

One revision-53 `Strip` edge is excluded rather than normalized into fake deterministic behavior. An empty or whitespace-only quoted payload can produce an out-of-bounds `Fname(0:Ilast)` substring. Pilot A classifies this as `FAIL_CLOSED_NOT_NORMALIZED`.

## Pilot B: non-GHG Ruurlo MATERIAL core

Pilot B is now qualified as a bounded representation candidate.

Scope:

- natural case: `RuurloGrass`;
- `IPO=0`;
- `Ioptae=0`;
- `IoptGHG=0`;
- `Nm=11`;
- `Nf=14`;
- normalized object: `MaterialParameterSet/v1`.

The source contract and natural old/new input lineage were reconstructed before the native representation was admitted.

### Sparse FR / FRca semantics

The frozen testbank contains both the older full-matrix `MATERIAL_oud.INP` and the revision-53 sparse `MATERIAL.INP`. The reproducible lineage audit establishes exact shared-field equivalence when omitted sparse cells are normalized to zero:

- cells per full matrix: 154;
- explicit sparse triplets: 24;
- omitted cells per matrix: 130;
- old full FR equals zero-filled new sparse FR: exact;
- old full FRca equals zero-filled new sparse FRca: exact.

This makes zero for omitted Ruurlo sparse cells an input-lineage-qualified normalization rule, not an inference from compiler zero-fill.

### IPO=0 inactive phosphorus fields

Revision 53 consumes no material-level `Frpo` and no fraction-level `Pofr` elements from `>defmat:` / `>deffra:` when `IPO=0`. The trailing zero columns retained in Ruurlo are therefore recorded as lexical residue rather than active P state. The normalized fields are `FEATURE_INACTIVE_NULL`.

`Pofrex` and `Pofrhuma` remain explicit because revision 53 reads them unconditionally from their own sections.

### TTUTIL numeric conversion seam

Direct TTUTIL 4.27 DOUBLE decoding through `RDSDOU` / `RDADOU` was tested and rejected for the field-exact representation claim. On Ruurlo it produced 26 normalized numeric leaves that differ from compiler list-directed REAL(8) decoding by exactly one binary64 ULP, with maximum absolute difference `1.1102230246251565e-16`.

No epsilon or tolerance is used to hide this difference.

The admitted Pilot-B candidate therefore keeps TTUTIL as lexical/name/cardinality transport while retaining numeric conversion ownership in the ANIMO adapter:

- TTUTIL INTEGER for `IPO`, `Nm`, `Nf`;
- TTUTIL CHARACTER scalar/array tokens for real-valued leaves;
- explicit adapter-owned REAL(8) conversion after TTUTIL retrieval;
- dense normalized FR/FRca arrays;
- strict native-v1 unknown/duplicate/missing/cardinality rejection.

This path gives field-exact `MaterialParameterSet/v1` equivalence on the natural Ruurlo case with no numeric tolerance.

The typed-double comparison path is classified:

`REJECT_TYPED_DOUBLE_FOR_FIELD_EXACT_REPRESENTATION`.

### Runtime-hazard exclusions

Two legacy runtime hazards remain separate from the intended input representation:

1. revision 53 reads omitted sparse FR/FRca cells after sparse assignment without an identified explicit initialization;
2. revision 53 range-checks `Pofr(Frno)` even at `IPO=0`, after a zero-element implied-DO input.

The intended Ruurlo sparse zero semantics are lineage-qualified, but the first legacy storage mechanism is not. The IPO=0 checked Pofr runtime value is not input-defined. Neither accidental storage behavior is copied into the native adapter. They are routed for BUILDQ01/B3I01 runtime/governance qualification in `docs/io/MATERIAL_PILOT_B_RUNTIME_HAZARD_ROUTING.md`.

## Evidence and tooling

Pilot B artifacts include:

- `tools/io01_material_pilot.py`;
- `tools/audit_material_ruurlo_lineage.py`;
- `tools/qualify_io01_material_pilot.py`;
- `tools/ttutil_material_probe.f90`;
- `tools/ttutil_material_probe_typed_double.f90`;
- `tests/io/test_io01_material_pilot.py`;
- `integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json`;
- `integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json`;
- `docs/io/MATERIAL_PILOT_B_QUALIFICATION.md`.

## Next expansion boundary

The DIRECT and bounded Ruurlo MATERIAL results may not be generalized automatically.

A next pilot should remain independently bounded. Lower-risk options are another non-GHG static configuration family or a separately evidenced MATERIAL feature variant. Do not use GHGMais to infer a unified GHG schema. GENERAL remains high risk because its revision-53 ANIMO41 named records are sequentially order-sensitive. SOIL and PLANT remain higher-risk because they own geometry, feature-dependent arrays and source-side compatibility defaults. Management, external crop, soil temperature, restart/state and binary hydrology remain specialized adapters under IO01.

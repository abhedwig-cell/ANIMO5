# ANIMO-IO01 Pilot B qualification: non-GHG MATERIAL core

Status: `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS`

## Scope

Pilot B remains deliberately bounded to the natural `RuurloGrass` revision-53 MATERIAL contract with:

- `IPO=0`;
- `Ioptae=0`;
- `IoptGHG=0`;
- `Nm=11`;
- `Nf=14`.

No model physics was executed for the representation claim. GHG, SONIC, binary hydrology, restart/checkpoint and production input migration remain outside this qualification.

## Natural old/new lineage result

The frozen testbank contains both:

- `RuurloGrass/Input/MATERIAL_oud.INP`, the older full-matrix representation;
- `RuurloGrass/Input/MATERIAL.INP`, the revision-53 sparse representation.

`tools/audit_material_ruurlo_lineage.py` compares them after source-authorized structural mapping. The result is exact for the shared fields. In particular:

- `FR`: full old matrix equals sparse new matrix after zero-filling omitted cells;
- `FRca`: same result;
- explicit sparse triplets per matrix: 24;
- omitted cells per 11 x 14 matrix: 130;
- the shared decomposition, assimilation and nitrogen parameters are exact matches.

Therefore the normalized Pilot-B rule is:

`omitted sparse (material,fraction) cell -> numeric zero`

This rule is not inferred from compiler zero fill. It is supported by exact natural cross-version input lineage evidence.

## IPO=0 lexical residue

Revision 53 uses zero-length implied-DO input lists for `Frpo` in `>defmat:` and `Pofr` in `>deffra:` when `IPO=0`. Ruurlo nevertheless retains a trailing zero column in each row.

Those trailing columns are recorded as lexical residue and are not normalized as active P fields. Normalized `Frpo` and fraction-level `Pofr` are `FEATURE_INACTIVE_NULL` for this pilot.

`Pofrex` and `Pofrhuma` are different: revision 53 reads them unconditionally, so they remain explicit normalized values even with `IPO=0`.

## TTUTIL numeric precision seam

A direct TTUTIL 4.27 numeric implementation was tested using `RDSDOU` and `RDADOU`. It is **not** field-exact to the bounded legacy REAL(8) normalization.

For the natural Ruurlo parameter set:

- mismatching normalized numeric leaves: 26;
- maximum difference: 1 binary64 ULP;
- maximum absolute difference: `1.1102230246251565e-16`;
- no tolerance was used to hide the discrepancy.

Examples include `0.078`, `0.75`, `0.6`, `0.384`, `0.412`, `0.174`, `0.326` and `0.416`.

Source inspection explains the seam. TTUTIL 4.27 decodes floating tokens through its `RDLEX`/`VFLOAT` decimal accumulation path rather than delegating the token conversion to the compiler's list-directed REAL(8) input conversion. Both paths are numerically close, but they are not bit-identical for every decimal token.

The comparison-only typed-double path is therefore classified:

`REJECT_TYPED_DOUBLE_FOR_FIELD_EXACT_REPRESENTATION`

This is not a scientific defect in TTUTIL. It is an incompatibility with ANIMO-IO01's stronger parser-level field-exact representation requirement.

## Qualified native MATERIAL-v1 route

The qualified candidate keeps TTUTIL as the symbolic-name, array-cardinality and lexical transport layer, but does not let TTUTIL define ANIMO's floating conversion semantics.

`TTUTILNativeMaterialAdapter/v1` therefore uses:

- TTUTIL INTEGER for `IPO`, `Nm` and `Nf`;
- TTUTIL CHARACTER scalar/array tokens for real-valued leaves;
- explicit adapter-owned REAL(8) numeric conversion after TTUTIL retrieval;
- dense normalized `FR` and `FRca` arrays;
- strict native-v1 unknown-key, duplicate-key, missing-key and cardinality rejection.

On the natural Ruurlo case this path produces a field-exact `MaterialParameterSet/v1` semantic projection relative to the bounded legacy normalization oracle:

`FIELD_EXACT_EQUIVALENCE = PASS`

No numeric tolerance or epsilon is involved.

## Legacy runtime hazards excluded from the representation claim

Two source-level hazards remain distinct from the intended normalized input semantics.

### Sparse FR / FRca storage lifetime

Revision 53 assigns only explicit sparse cells but subsequently reads every `FR(Mn,Fn)` and `FRca(Mn,Fn)`. No explicit initialization of omitted cells has been found before those reads. The intended zeros are now lineage-qualified, but the legacy storage mechanism remains a BUILDQ01 runtime-semantics issue.

### IPO=0 Pofr check

Revision 53 reads no `Pofr(Frno)` input element when `IPO=0`, but then range-checks `Pofr(Frno)` unconditionally. That checked runtime value is not defined by the input record. The native adapter does not reproduce an undefined value merely to imitate accidental storage.

These exclusions mean Pilot B is a qualified representation candidate, not proof that every undefined or malformed revision-53 runtime path is deterministic.

## Artifacts

- `tools/io01_material_pilot.py`
- `tools/audit_material_ruurlo_lineage.py`
- `tools/qualify_io01_material_pilot.py`
- `tools/ttutil_material_probe.f90`
- `tools/ttutil_material_probe_typed_double.f90`
- `tests/io/test_io01_material_pilot.py`
- `integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json`
- `integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json`

## Admission boundary

Pilot B now supports the classification:

`QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS`

It does **not** admit:

- production replacement of revision-53 MATERIAL parsing;
- GHG schema normalization;
- model-output equivalence;
- binary hydrology conversion;
- checkpoint/state migration;
- B4.

The next safe expansion is another non-GHG static input family or a broader MATERIAL feature variant only after its feature-specific fields and runtime hazards are independently qualified.

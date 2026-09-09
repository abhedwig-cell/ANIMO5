# ANIMO-IO01 MATERIAL Pilot B runtime-hazard routing

Status: `ROUTED_TO_RUNTIME_QUALIFICATION_NOT_NORMALIZED_AWAY`

Pilot B qualified the intended non-GHG Ruurlo MATERIAL representation separately from two revision-53 runtime/storage hazards. These hazards are not allowed to become hidden parser defaults and are not corrected in frozen B0.

## MAT-RH-001: sparse FR / FRca omitted-cell storage

Revision 53 assigns only the explicit `(material,fraction)` entries from `>matfra:` and then reads every `FR(Mn,Fn)` and `FRca(Mn,Fn)` cell during validation. No explicit initialization of the omitted cells has been identified before those reads.

Independent natural lineage evidence now establishes the intended normalized value for the Ruurlo sparse representation: the older full matrices and newer sparse matrices are field-exact when omitted sparse cells are filled with numeric zero. See `integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json`.

Disposition:

- normalized intended input semantics: `OMITTED_SPARSE_CELL_IS_ZERO_FOR_QUALIFIED_RUURLO_LINEAGE`;
- legacy storage/runtime mechanism: `UNQUALIFIED`;
- migration owner: runtime/state qualification, principally ANIMO-BUILDQ01 with canonical discrepancy routing through B3I01 where required;
- IO01 action: do not reproduce compiler zero-fill or accidental storage lifetime. Materialize the intended zero explicitly in the normalized object.

This distinction permits a representation-only parser candidate without claiming that the legacy implementation's omitted-cell storage is deterministic.

## MAT-RH-002: IPO=0 Pofr unconditional range check

For `IPO=0`, revision 53's `>deffra:` implied-DO consumes zero `Pofr(Frno)` input elements. The source nevertheless range-checks `Pofr(Frno)` immediately afterwards.

The trailing zero column present in natural Ruurlo `>deffra:` rows is therefore lexical residue under the revision-53 input list, not an input-defined assignment to `Pofr(Frno)`.

Disposition:

- normalized input presence: fraction-level `Pofr = FEATURE_INACTIVE_NULL` for Pilot B;
- legacy checked runtime value: `NOT_INPUT_DEFINED`;
- migration owner: ANIMO-BUILDQ01/B3I01 runtime-semantics qualification;
- IO01 action: fail closed outside the admitted IPO=0 representation contract and do not invent a retained Pofr value to imitate undefined storage.

`Pofrex` and `Pofrhuma` remain explicit fields because revision 53 reads them unconditionally from their own sections.

## Admission consequence

These hazards do not invalidate the bounded `MaterialParameterSet/v1` representation claim because that claim concerns intended normalized input state supported by source plus natural lineage evidence. They do block any stronger statement that the entire legacy MATERIAL execution path is deterministic under arbitrary compiler storage semantics.

No TCD number is assigned here. Canonical discrepancy numbering or reconciliation belongs to B3I01 governance intake.

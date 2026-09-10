# ANIMO-B3D08 — TCD-026 B3 Admission Closeout

## Decision surface

Target: `TCD-026`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Atomic candidate:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

The candidate observes the already-existing initial root-exudate organic-matter state `Ex(Ln)` in the fresh-organic-matter beginning-storage ledger. It does not alter initialization physics, physical state, process fluxes, restart state, forcing, numerical policy, or other organic-matter TCDs.

## Authorities

Formal route disposition:

`ANIMO-B3D07@21766eaf3443bcf432f05fbf6ba89d365bc70988`

Independent second-line review:

`ANIMO-B3A04R2@767779127d092c54a298e2f76a21d544e9af9895`

Review result: `PASS`

Review validation: Actions run `34446939959`, job `102773677475`.

Historical route:

`ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`

No qualified B2 exists. Historical revision-53 behaviour therefore remains `UNKNOWN` and no historical fidelity is claimed.

## Admission decision

Subject to this workunit's fail-closed validation, admit the bounded scientific correction as:

`ADMIT_TCD026_ATOMIC_CLASS_A_SCIENTIFIC_ACCOUNTING_CORRECTION_WITH_HISTORICAL_UNCERTAINTY`

Final disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

## Retained boundaries

This admission does not qualify uninterrupted-execution versus formatted-restart whole-model identity. The known formatted-restart negative control remains a scope boundary, not a tolerance.

No TCD-026-specific SYNQ01 oracle exists. STATEQ02 remains continuation-state ownership support only and is not promoted to a TCD-026 ledger oracle, whole-model restart oracle, B2 reference, or admission authority.

No composition with other organic-matter TCDs is admitted. No production source is changed, no B4 gate is opened, and no production migration is authorized.

## Project effect

If validation is green, TCD-026 becomes one additional atomic B3 scientific admission. Whole-model B3 remains incomplete. A separate central-regie integration is required afterwards.

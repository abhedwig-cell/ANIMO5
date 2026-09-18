# ANIMO-UBFORCE01 Qualification Rationale

KT12 exposed a second missing input seam beyond resolved hydrology: the TCD-042 load term is chemistry-bearing forcing.

ARCH05 already states the ownership rule: water quantity and chemical composition are separate. IO01 inventories `BOUNDARY.INP` as a forcing family but explicitly does not qualify its migration.

Frozen revision-53 `UBoundconc` confirms the runtime consequence. Under the current detailed hydrology route, `Load1...Load6` combine water-flux terms with precipitation, irrigation, runon and run-in concentration forcings. They therefore cannot be supplied by KT11 hydrology packets alone.

UBFORCE01 qualifies only an explicit typed representation for the resolved load rates. This lets downstream transaction science bind chemistry-bearing load forcing without giving the hydrology owner chemical authority.

Dry deposition remains outside this carrier because revision-53 applies it separately as a state pulse before the wet/advective top-load calculation.

A successful qualification means:

`TCD042_UPPER_SOLUTE_LOAD_FORCING_HAS_AN_EXPLICIT_TYPED_SOURCE_MAPPED_BOUNDARY`

It does not mean:

`BOUNDARY_INP_OR_UBOUNDCONC_LOAD_RESOLUTION_HAS_BEEN_MIGRATED`.

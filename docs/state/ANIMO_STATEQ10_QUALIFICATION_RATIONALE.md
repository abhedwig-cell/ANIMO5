# ANIMO-STATEQ10 Qualification Rationale

HYDROEXEC01 made the first-interval origin dependency explicit. STATEQ09 resolves later interval continuation, but it cannot provide values before the first accepted endpoint exists.

Frozen revision-53 source contains an explicit initial-hydrology input block for the current detailed SWAP route. The values relevant to HYDROEXEC01 are read as REAL(4) and are not simply cast to REAL(8): revision-53 passes them through `Dble_trunc`.

STATEQ10 therefore treats the conversion itself as part of the source contract.

The implementation accepts already-read REAL(4) coordinates and reproduces the source `Dble_trunc` algorithm. Exact binary64 test oracles are used for representative positive, negative, integer and small values.

No parser is introduced.

No first-call `Runinu` value is introduced. That remains explicitly source-undefined according to STATEQ08.

Positive qualification would establish:

`REV53_HLPIMP11_IOPTHYVS1_FIRST_ORIGIN_MOFRO_SIC_PN_SNLA_CAN_BE_SOURCE_NORMALIZED_FROM_EXPLICIT_REAL4_INPUTS`.

It would not establish historical file contents, B2 equivalence, canonical state admission or production input migration.

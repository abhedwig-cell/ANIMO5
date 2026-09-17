# ANIMO-KT05 Qualification Report

## Disposition

KT05 qualifies a bounded nonproduction compiled adapter between the frozen KT03 hydrology-step contract and the producer-derived external portion of the revision-53 `Hydro_detailed` call boundary.

Exact verdict:

`QUALIFIED_NONPRODUCTION_EXPLICIT_STATE_FORTRAN_HYDROLOGY_CALL_BOUNDARY_ADAPTER_NO_HYDRO_DETAILED_EXECUTION_OR_RUNTIME_INTEGRATION`

Frozen implementation head:

`69dd607ba1efa28de3f83cc963526021352b3311`

Exact-head GitHub Actions run:

`35285836540 -> SUCCESS`

## Qualified capabilities

The frozen implementation establishes:

1. a compiled Fortran representation of the complete frozen `ANIMO_HYDROLOGY_STEP_V1` field set;
2. explicit `ANIMO_HYDROLOGY_UNITS_V1` identity;
3. fail-closed schema, unit, dimension, finite-value, explicit-interception and producer-duration validation;
4. projection of only the producer-derived external values needed at the bounded `Hydro_detailed` call surface;
5. exact machine-checked structural parity between the KT03 Python dataclass and the Fortran carrier;
6. exact machine-checked field-set control for `hydro_detailed_external_t`;
7. a public fail-closed validator for directly constructed or mutated projected carriers;
8. an explicit normalized-to-legacy slice mapper that writes producer values only to index-one-and-higher legacy slices while preserving ANIMO-owned index zero;
9. valid zero-drainage and unavailable-temperature paths, including zero-drainage legacy-slice mapping;
10. continued separation of legacy file provenance from physical forcing.

The exact slice contract is:

- `mofrt(1:Nl) -> Mofrt(1:Nl)`;
- `flev(1:Nl) -> Flev(1:Nl)`;
- `flab(1:Nl+1) -> Flab(1:Nl+1)`;
- `fldr(1:Nudr,1:Nl) -> Fldr(1:Nudr,1:Nl)`.

## Scientific ownership preserved

KT05 does not implement ANIMO hydrology science. It does not calculate or own accepted `Sic`, `Mofro`, `Pn`, `Snla`, runoff partitioning, `Dif`, the `Evso` correction, macropore state, `Modflux`, mass-balance acceptance, solute transport, timestep selection or retry policy.

Producer time remains producer metadata. KT05 does not map or advance KT02 runtime time.

## Relationship to KT03F01

KT05 has no dependency on the unresolved Hlpimp=1 candidate scientific disposition. It requires explicit interception storage and advances only the explicit-state path already evidenced by KT03.

The Tier-C independent-review requirement on KT03F01 remains unchanged.

## Review evidence

The initial implementation passed exact-head CI. Same-agent adversarial review identified KT05-R1 through KT05-R4; remediation and a second review identified KT05-R5 and KT05-R6. All six findings are closed at the frozen implementation head.

Review assurance remains:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

No independent scientific-review claim is made.

## Explicit nonclaims

KT05 does not qualify:

- Hlpimp=1 or Hlpimp=2 semantics;
- actual execution or numerical equivalence of revision-53 `Hydro_detailed`;
- `Modflux` or downstream transport equivalence;
- macropore coupling;
- mapping of producer time to KT02 exact runtime time;
- KT02 runtime integration;
- SWAP5 production coupling;
- B2 historical compiler equivalence;
- B3/B4 admission;
- production source;
- Status A or Status AA.

## Handoff

The next safe architecture step is a separate KT06 runtime-adapter workunit that combines:

- KT02 exact interval and transaction authority;
- the KT05 explicit-state compiled hydrology boundary;
- a bounded ANIMO scientific callback/stub.

KT06 must validate producer interval metadata against KT02 exact runtime interval authority before the ANIMO attempt runs. It must not create a second time owner and must not silently migrate `Hydro_detailed` science.

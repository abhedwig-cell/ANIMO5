# ANIMO-KT03 Qualification and Closeout Report

## Decision

KT03 is closed as a bounded nonproduction adapter/runtime-architecture qualification.

Qualification verdict:

`QUALIFIED_NONPRODUCTION_FILE_INDEPENDENT_TYPED_HYDROLOGY_EXCHANGE_WITH_BOUNDED_HLPIMP11_DOWNSTREAM_PROJECTION_AND_FAIL_CLOSED_HLPIMP1_SICT_BOUNDARY`

This means the first real ANIMO external-hydrology seam supports the intended architecture: legacy file grammar can terminate in an adapter, while ANIMO consumes an explicit normalized hydrology payload that a later in-memory producer can also construct. It does not mean ANIMO production migration or SWAP5-ANIMO production coupling is admitted.

## Frozen qualification target

- branch: `work/animo-kt03-real-hydrology-adapter`;
- frozen remediation target: `e844c7658a95819fc0463c55737f9bd41b29a6da`;
- exact-head GitHub Actions run: `35282453399`;
- conclusion: `SUCCESS`;
- assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`;
- evidence class: `B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`.

The closeout record is bookkeeping downstream of this frozen implementation/contract target.

## Qualified contract

The normalized payload is `ANIMO_HYDROLOGY_STEP_V1` with unit contract `ANIMO_HYDROLOGY_UNITS_V1`.

The following separation is qualified for this nonproduction scope:

`legacy SWATRE.UNF -> legacy adapter/normalization -> HydrologyStep -> ANIMO hydrology adapter -> Hydro_detailed`

Legacy framing, `Hlpimp` and source-record hashes are adapter provenance rather than required physical forcing. Producer endpoint/duration fields are explicitly producer metadata, not authoritative KT02 runtime time. KT02 remains model-neutral and does not know the legacy grammar or the hydrology field schema.

## Real-file evidence

### CranMais

Frozen `Swatre.unf` SHA-256:

`538827d517f7be4c060e2d62131e1942f8e0e76fdeae49dc0268486984cc9eaf`

The bounded probe establishes Hlpimp=1, 22 layers, 5 horizons, no drainage systems, 3287 timesteps, eight dynamic logical records per timestep, one-day producer steps, Ioptte=0 and no groundwater sentinel activation. File data reconstruct into the normalized payload, but Hlpimp=1 does not provide `sSict` and therefore fails closed for a complete downstream projection.

### LWKM

Frozen `Swatre.unf` SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

The bounded probe establishes Hlpimp=11, 30 layers, 30 horizons, five drainage systems, 1800 timesteps, thirteen dynamic logical records per timestep, producer steps of 8-11 days, Ioptte=1, explicit `sSict` in every dynamic first record and no groundwater sentinel activation. Within this envelope, the normalized packet can construct the complete file-derived subset of the existing `Hydro_detailed` call surface.

This is structural adapter evidence. It is not a claim that executing `Hydro_detailed` through a new production path is scientifically or numerically equivalent.

## Adversarial review and remediation

The pre-remediation same-agent adversarial review found four issues requiring action before close: legacy file identity leaked into the payload, producer time could be confused with runtime authority, units were implicit, and digest validation was weak.

At the frozen target:

- R1 is resolved by `LegacyStepProvenance` separation;
- R2 is resolved by explicit producer-time naming and ownership rules;
- R3 is resolved by `ANIMO_HYDROLOGY_UNITS_V1`;
- R4 is resolved by moving the digest to provenance and validating hexadecimal SHA-256;
- R5 remains an explicit B1-not-B2 normalization boundary;
- R6 remains the explicit Hlpimp=1 `Sict` boundary.

Post-remediation verdict:

`SELF_REVIEW_PASS_NONPRODUCTION_FILE_INDEPENDENT_TYPED_HYDROLOGY_CONTRACT_WITH_EXPLICIT_HLPIMP1_SICT_BOUNDARY`

No independent-review claim is made.

## KT03-F01 handoff

The remaining scientific/source finding is not an adapter-design ambiguity that KT03 may silently solve.

For Hlpimp=1, revision-53 input grammar omits initial and dynamic interception-storage values, while `input1`/`Input_hydro` still normalize local `sSic`/`sSict` and `Hydro_detailed` consumes `Sict-Sic` in detailed-hydrology balance expressions. KT03 therefore does not invent zero, previous-state carry, or another inferred value.

`KT03-F01` must be handled by a separate scientific/source-disposition workunit. TCD-018 is related because it concerns interception storage in a reporting ledger, but it does not settle this Hlpimp=1 missing-state question and must not be treated as automatic authority for it.

## Residual nonproduction design note

Revision-53 `Input_hydro` also returns `Wabaer`, and the legacy SWATRE record documents it as a water-balance error. Source-wide inspection found no downstream revision-53 consumer after the call. The V1 prototype retains it only as normalized producer diagnostic data and does not include it in the `Hydro_detailed` projection. A future production coupling-schema freeze should minimize or explicitly justify this field rather than inherit it by accident.

## Explicit nonclaims

KT03 does not qualify or admit:

- corrected Hlpimp=1 interception-storage science;
- B2 historical compiler/runtime equivalence;
- complete ANIMO production migration;
- B4 or production admission;
- a separately versioned production shared runtime library;
- online SWAP5-ANIMO production coupling;
- joint SWAP5-ANIMO timestep acceptance or retry policy;
- Status A or Status AA.

Production `src/` was not modified.

## Next safe action

Start a separate `KT03-F01` scientific/source-disposition workunit from the frozen KT03 evidence. Keep the typed adapter contract frozen while that workunit determines whether Hlpimp=1 scientifically has no interception-storage state, whether the unconditional Sic/Sict path is a bounded legacy defect, and what explicit corrected contract is defensible. Only after that disposition may a later adapter workunit reopen Hlpimp=1 full downstream projection.

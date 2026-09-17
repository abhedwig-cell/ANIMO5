# ANIMO-KT05 Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Reviewed implementation head:

`bcef06df5a7c07052e251f8adf8a4761edf67d44`

Exact-head CI:

`35285228675 -> SUCCESS`

This review treats KT05 as a future compiled boundary between a producer-neutral `ANIMO_HYDROLOGY_STEP_V1` packet and ANIMO science. Passing compilation is not sufficient; the contract must remain aligned with KT03 and must not create hidden indexing or scope assumptions.

## KT05-R1, HIGH: full KT03 schema parity is not machine-checked

The Fortran type manually repeats the KT03 carrier. Current structural testing checks schema/unit strings and the downstream projection field names, but it does not prove that the complete Fortran `hydrology_step_t` field set still matches the frozen Python `HydrologyStep` contract.

A future edit could omit, rename or add a field while retaining the same schema identifier and still pass current tests.

Disposition: `MUST_REMEDIATE_BEFORE_CLOSE`.

Required remediation: add an exact structural parity test against the frozen KT03 dataclass field set. The test must also verify the exact field set of `hydro_detailed_external_t`, not merely token presence somewhere in the source.

## KT05-R2, MEDIUM: normalized-array to legacy-array indexing boundary is implicit

The legacy routine declares several arrays with index zero, including `Mofrt(0:)`, `Flev(0:)`, `Flab(0:)` and `Fldr(:,0:)`, while the producer exchange populates the external slices beginning at index 1.

KT05 correctly stores only normalized producer-derived slices, but neither the contract nor the code comments make the mapping explicit. Without that boundary a later wrapper could shift the normalized arrays into index zero and create an off-by-one scientific defect.

Disposition: `MUST_REMEDIATE_BEFORE_CLOSE`.

Required remediation: document and test the slice contract:

- normalized `mofrt(1:Nl)` -> legacy `Mofrt(1:Nl)`;
- normalized `flev(1:Nl)` -> legacy `Flev(1:Nl)`;
- normalized `flab(1:Nl+1)` -> legacy `Flab(1:Nl+1)`;
- normalized `fldr(1:Nudr,1:Nl)` -> legacy `Fldr(1:Nudr,1:Nl)`.

Legacy index-zero entries remain ANIMO-owned and are not in the producer packet.

## KT05-R3, MEDIUM: zero-drainage and unavailable-temperature schema branches are untested

The implementation is structurally capable of zero-size drainage and temperature arrays, but the compiled test exercises only one drainage system and active temperature. The frozen schema explicitly represents optional temperature and permits zero drainage systems.

Disposition: `MUST_REMEDIATE_BEFORE_CLOSE`.

Required remediation: compile and run a valid explicit-state packet with `drainage_count=0`, `has_soil_temperature=.false.`, `fldr(0,Nl)` and `soil_temperature(0)`.

## KT05-R4, LOW: non-positive producer timestep is classified as a dimension error

A non-positive `producer_step_days` currently returns `KT05_ERR_DIMENSIONS`. This is fail-closed but weakens diagnostic precision at exactly the producer-time boundary that must later be reconciled with KT02 runtime time.

Disposition: `SHOULD_REMEDIATE`.

A dedicated producer-time validation status is preferable. This does not authorize runtime time advancement or timestep policy.

## Accepted boundaries

The review accepts the following as intentional nonclaims:

- KT05 does not execute or rewrite `Hydro_detailed`;
- KT05 does not own `Sic`, `Mofro`, `Pn`, `Snla`, runoff partitioning, `Dif`, `Evso` correction, macropore state or `Modflux`;
- KT05 does not map producer time to KT02 runtime time;
- KT05 does not parse legacy files or carry `Hlpimp`/record provenance;
- KT05 uses only explicit interception state and does not consume the blocked Hlpimp=1 candidate.

## Review verdict before remediation

`NOT_YET_QUALIFIABLE_AS_FROZEN_COMPILED_EXPLICIT_HYDROLOGY_ADAPTER`.

The architecture direction is sound and exact-head CI is green. R1 through R3 must be closed, and R4 should be cleaned up, before final nonproduction qualification.

# ANIMO-KT05 Post-remediation Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Initial post-remediation reviewed head:

`e4db83052d542021edf8c4f5d8e00bacc9d97ed9`

Exact-head CI:

`35285568227 -> SUCCESS`

The first remediation closed KT05-R1 through KT05-R4. A second review then identified two remaining public-boundary gaps: KT05-R5 and KT05-R6.

## Re-check of prior findings

- **KT05-R1 REMEDIATED**: the structural validator imports the frozen KT03 `HydrologyStep` dataclass and compares its exact field-name set with `hydrology_step_t`; it separately checks the exact `hydro_detailed_external_t` field set.
- **KT05-R2 REMEDIATED**: the explicit slice mapper and compiled sentinel tests prove producer values enter legacy indices 1 and higher while index zero remains ANIMO-owned.
- **KT05-R3 REMEDIATED**: a valid compiled packet exercises `drainage_count=0`, `fldr(0,Nl)`, unavailable temperature and a zero-length temperature payload.
- **KT05-R4 REMEDIATED**: non-positive producer duration returns dedicated `KT05_ERR_TIME`.

## Second-round findings

### KT05-R5, MEDIUM: public projected carrier could bypass complete validation

At `e4db83052d542021edf8c4f5d8e00bacc9d97ed9`, a caller could construct or corrupt public `hydro_detailed_external_t` and pass it to the slice mapper without a complete validation gate.

Required remediation was to add a public validator covering allocation, exact dimensions, finite scalars/profiles and positive `St`, and to make the mapper invoke it before copying.

### KT05-R6, LOW: zero-drainage path was not exercised through the slice mapper

The zero-drainage packet was projected but not mapped into legacy-shaped target arrays.

Required remediation was a compiled `Nudr=0` slice-mapping test.

## Final post-remediation review

Frozen remediated implementation head:

`69dd607ba1efa28de3f83cc963526021352b3311`

Exact-head CI:

`35285836540 -> SUCCESS`

Final dispositions:

- **KT05-R5 CLOSED**: `validate_hydro_detailed_external` is public, validates the complete projected carrier, is called after projection construction, and is called by `apply_projection_to_legacy_slices` before any target copy. The compiled test corrupts a public projection with NaN and proves the mapper rejects it before modifying target data.
- **KT05-R6 CLOSED**: the compiled test maps a valid zero-drainage projection into zero-extent `Fldr` target storage while preserving ANIMO-owned index-zero values in the other legacy arrays.

No material finding remains open inside the KT05 scope.

## Boundaries reconfirmed

KT05 does not change ANIMO scientific equations, production `src/`, KT02 runtime mechanics, Hlpimp=1 or Hlpimp=2 semantics, macropore semantics, `Modflux`, timestep selection or retry policy.

The Hlpimp=1 route remains outside KT05 and remains blocked in KT03F01 pending genuinely independent Tier-C review.

Final review verdict:

`SELF_REVIEW_PASS_NONPRODUCTION_EXPLICIT_STATE_FORTRAN_ADAPTER_ONLY`

This is same-agent review. It is not an independent scientific review and does not qualify new process semantics.

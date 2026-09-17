# ANIMO-KT05 Post-remediation Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Reviewed head:

`e4db83052d542021edf8c4f5d8e00bacc9d97ed9`

Exact-head CI:

`35285568227 -> SUCCESS`

The earlier material findings R1 through R3 and low finding R4 are remediated at this head. CI confirms strict Fortran compilation, frozen KT03 regression, the full schema-parity validator, legacy index-slice tests, zero-drainage/unavailable-temperature coverage, JSON validation and the production/runtime scope guard.

## Re-check of prior findings

### KT05-R1: full KT03 schema parity

Status: `REMEDIATED`.

The structural test imports the frozen KT03 `HydrologyStep` dataclass and compares its exact field-name set with `hydrology_step_t`. It separately checks the exact `hydro_detailed_external_t` field set.

### KT05-R2: normalized-to-legacy indexing

Status: `REMEDIATED`.

The adapter now contains an explicit slice-mapping helper. Compiled tests prove producer values enter legacy indices 1 and higher while sentinel values at index zero remain unchanged.

### KT05-R3: zero-drainage and unavailable-temperature branches

Status: `REMEDIATED`.

A compiled valid explicit-state packet exercises `drainage_count=0`, `fldr(0,Nl)`, `has_soil_temperature=.false.` and `soil_temperature(0)`.

### KT05-R4: producer-time diagnostic classification

Status: `REMEDIATED`.

Non-positive producer step duration has a dedicated `KT05_ERR_TIME` result.

## New finding after remediation

### KT05-R5, MEDIUM: public projected carrier can bypass source-step validation

`hydro_detailed_external_t` is a public type with public components. A caller can therefore construct one directly rather than obtaining it through `project_hydro_detailed_explicit`.

`apply_projection_to_legacy_slices` currently validates dimensions but not the complete projection contract. A manually constructed projection containing non-finite profile data or an invalid producer timestep could be copied into the legacy-shaped arrays. This weakens the fail-closed claim at the public adapter boundary.

Disposition: `MUST_REMEDIATE_BEFORE_CLOSE`.

Required remediation:

- add a public projection validator covering exact dimensions, allocation, finite scalar/profile values and positive `St`;
- make `apply_projection_to_legacy_slices` call that validator before copying;
- add a compiled negative test that directly constructs/corrupts a projected carrier and proves the mapping helper rejects it.

### KT05-R6, LOW: zero-drainage projection is not exercised through the legacy slice mapper

The zero-drainage packet is projected successfully but the new slice-mapping helper is tested only with one drainage system.

Disposition: `SHOULD_REMEDIATE`.

Add a zero-drainage target-array mapping test to ensure the `nudr=0` branch remains a valid no-op for `Fldr`.

## Boundaries reconfirmed

No evidence was found that KT05 changes ANIMO scientific equations, production `src/`, KT02 runtime mechanics, Hlpimp=1 semantics, Hlpimp=2 semantics, macropore semantics, `Modflux`, timestep selection or retry policy.

The Hlpimp=1 route remains outside KT05 and blocked in KT03F01 pending genuinely independent Tier C review.

## Post-remediation review verdict

`REMEDIATION_REQUIRED_FOR_PUBLIC_PROJECTION_FAIL_CLOSED_GATE`.

R5 is material to closing the public compiled adapter contract. R6 should be closed in the same bounded remediation.

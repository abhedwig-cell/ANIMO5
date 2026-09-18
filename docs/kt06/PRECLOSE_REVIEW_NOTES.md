# ANIMO-KT06 Pre-close Same-Agent Review Notes

Review mode: `same-agent / not genuinely independent`.

Assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Reviewed exact implementation head:
`7b15faa65355d1f12eeb6f737c24f962319af1e5`.

Exact-head CI:
`35286434233 -> SUCCESS`.

CI success is evidence, not a Tier C qualification.

## KT06-R1, medium: probe client naming could be mistaken for a scientific runtime client

The implementation intentionally returns an admissible no-op candidate after
validating interval binding and the KT05 projection. It does not execute ANIMO
science or calculate scientific admissibility.

The public type name
`animo_explicit_hydrology_runtime_client_t` did not make that limitation
structurally obvious enough for future reuse.

Disposition: remediate before independent handoff by renaming the type to
`animo_explicit_hydrology_runtime_probe_client_t`. The implementation remains
a nonproduction binding probe.

## KT06-R2, medium: real-producer fixture metadata and compiled test constants could drift independently

The derived LWKM metadata JSON was validated only as JSON while the Fortran
test repeated endpoint, duration, interception state and dimensions as
literals. A later edit could preserve green compilation while breaking the
claimed link to the pinned producer evidence.

Disposition: remediate before handoff with a dedicated Fortran fixture module
plus a Python parity check against
`reference/kt06/LWKM_FIRST_INTERVAL_METADATA.json`. The runtime test consumes
the fixture constants rather than duplicating them.

## Checks that remain clean

- KT02 remains the sole accepted-time and publication authority.
- Producer endpoint and duration are validation metadata only.
- The full KT05 explicit HydrologyStep is validated and projected before the
  no-op probe candidate is returned.
- Hydrology forcing is client-owned interval input, not accepted continuation
  state.
- Calendar identity and day-offset composition are explicit.
- Endpoint, duration, schema, explicit interception, fractional time and
  subday mismatches fail closed.
- The two-request stale-forcing test proves a first private working commit does
  not publish when a later request fails.
- KT03F01/Hlpimp=1 semantics are not consumed.

## Remaining bounded limitations

The proof still uses synthetic finite values for most LWKM HydrologyStep
fields. Only dimensions, first-interval endpoint, duration and explicit Sict
are derived from the pinned producer evidence.

The client owns one forcing packet at a time. No multi-packet forcing provider
or retry-aware forcing sequence is qualified.

The KT02 public interval reason still collapses detailed client failure to a
generic runtime failure. That is diagnostic debt, not a scientific PASS claim.

After remediation and exact-head CI, rerun same-agent review and prepare the
genuinely independent GOV04 Tier C handoff. Same-agent review cannot close the
workunit.

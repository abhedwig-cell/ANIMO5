# ANIMO-KT05 Pre-close Same-Agent Review Notes

Review mode: `same-agent / not genuinely independent`.

Assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

The first green implementation head `1744609baaf2d39c04ac3af2b4d128af62a3bc79`
passed exact-head CI run `35285609451`. CI success was not treated as
qualification because KT05 touches runtime interval semantics and is Tier C
under GOV04.

## KT05-R1, high: partial interval view was labelled as the full KT03 schema

The first implementation placed `ANIMO_HYDROLOGY_STEP_V1` directly in the
small interval-binding carrier even though that carrier contains only time and
explicit interception fields. That could let a partial view be mistaken for a
complete `HydrologyStep`.

Disposition: remediated by introducing a distinct
`ANIMO_KT05_EXPLICIT_INTERVAL_BINDING_V1` identity and separate immutable
source-contract pins for the KT03 schema, unit contract and frozen contract
authority. The binding is now explicitly a projection from an already
validated KT03 step, not an implementation of the full schema.

## KT05-R2, high: producer-day offset lacked a runtime calendar contract

A numeric day offset is not meaningful without the runtime calendar/epoch
contract to which it applies. The first implementation checked only that
origin and endpoint shared some calendar.

Disposition: remediated by requiring an explicit
`runtime_calendar_contract_id` in the client composition and rejecting any
origin or endpoint that does not match it.

## KT05-R3, medium: the proof used only synthetic producer metadata

The first green test used invented endpoint/duration values. That was adequate
for a mechanics smoke test but weak evidence that the bounded mapping matches
the real KT03 explicit-state envelope.

Disposition: remediated with a derived, non-B2 fixture from the pinned LWKM
Hlpimp=11 file. Its first dynamic record group has SHA-256
`2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7`
and supplies endpoint 10 d, duration 10 d and explicit `Sict=0 m`.
No raw legacy bytes are committed.

## KT05-R4, medium coverage: single forcing must not leak a partial interval

The client currently owns one forcing binding at a time. It is therefore not a
multi-packet forcing provider. Reuse across two accepted substeps must fail
closed rather than silently reusing stale forcing.

Disposition: a two-request test now proves that the first private working
commit is not published when the second request detects stale endpoint
identity. External accepted time, generation and payload remain unchanged.

## Remaining bounded limitations

The adapter still does not carry the full `HydrologyStep`, execute
`Hydro_detailed`, evaluate ANIMO scientific admissibility, expose detailed
client-failure diagnostics through `run_interval`, or support fractional or
subday time mapping. These are explicit exclusions, not PASS claims.

After remediation CI, same-agent review must be rerun against the exact head.
Even a clean same-agent result cannot satisfy the GOV04 Tier C independent
second-line review gate.

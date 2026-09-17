# ANIMO-KT05 Same-Agent Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Exact implementation/remediation head reviewed:
`c67c28f0475c42351c1a66f58d4d44ce8b584ee5`.

Exact-head CI:
`35285939129 -> SUCCESS`.

## Review result

The remediation resolves the material findings recorded in
`PRECLOSE_REVIEW_NOTES.md`.

Same-agent verdict:

`PASS_REMEDIATED_BOUNDED_RUNTIME_BINDING_CANDIDATE`

This is not a final qualification verdict. KT05 remains GOV04 Tier C and
requires genuinely independent second-line review.

## Adversarial checks

### Runtime authority

PASS within the bounded proof.

The KT02 runtime still owns accepted time, trial origin, requested endpoint,
private working commits and final publication. The KT05 client can validate
the requested interval against forcing metadata but cannot advance accepted
time or publish state independently.

### Forcing versus continuation state

PASS within the bounded proof.

The accepted payload contains only the synthetic ANIMO runtime-probe state
token. Hydrology forcing remains client-owned interval input. The success test
shows that the accepted state token is unchanged while runtime generation/time
advance through the ordinary KT02 transaction path.

This does not yet prove the shape of real ANIMO scientific continuation state.

### KT03 contract identity

PASS after remediation.

The compact KT05 carrier is no longer labelled as though it were the complete
`ANIMO_HYDROLOGY_STEP_V1` payload. It has its own interval-binding identity
and separately pins the upstream KT03 schema, unit contract and frozen contract
authority.

These string pins are semantic contract references, not cryptographic producer
authentication. Production composition must not treat possession of the
strings as proof of producer qualification.

### Time mapping

PASS only for the stated envelope.

The client requires:

- one pinned runtime calendar contract;
- exact whole-day runtime coordinates;
- exact nonnegative integer REAL64 producer endpoint/duration metadata;
- exact duration agreement with the runtime interval;
- exact endpoint agreement under a configured nonnegative day offset.

Fractional producer metadata and subday runtime mapping fail closed. No general
calendar conversion or tolerance policy is qualified.

### Real-producer contact

PASS as B1 derived fixture evidence only.

The first LWKM Hlpimp=11 dynamic interval is represented by derived metadata
from the pinned producer record group: endpoint 10 d, duration 10 d and
explicit `Sict=0 m`. The raw producer record is not committed.

This is not B2 historical executable evidence and does not establish full
`HydrologyStep` transport or `Hydro_detailed` equivalence.

### Single-forcing lifecycle

PASS for fail-closed nonpublication.

A two-request test reuses a forcing binding valid only for the first request.
The first request commits privately in the KT02 working store; the second
request rejects stale endpoint identity; the external accepted store remains
unchanged. This confirms the existing KT02 atomic publication boundary for
this failure mode.

KT05 does not yet provide a forcing sequence/provider capable of supplying a
different validated packet per accepted substep.

### Scientific admissibility

Not claimed.

The client returns an admissible no-op scientific candidate after binding
checks. It does not execute ANIMO science and therefore cannot qualify ANIMO
scientific admissibility, conservation, reactions or transport.

### Hlpimp=1 isolation

PASS.

KT05 neither imports nor executes the unresolved KT03F01 Hlpimp=1
absent-interception candidate. Explicit interception storage is mandatory.

## Remaining non-material limitations

The current `run_interval` public failure reason collapses detailed client
binding failures to the generic runtime reason `CLIENT_ATTEMPT_FAILED`.
Detailed adapter diagnostics are therefore not yet part of the external
runtime contract.

The client supports one forcing binding at a time. A multi-packet forcing
provider, retry-aware forcing identity, full typed hydrology transport and
real ANIMO scientific state are separate future surfaces.

## Governance disposition

No production source is changed. No KT02 runtime-core file is changed. No
B3/B4 or Status A/AA claim is made.

Current status:

`SELF_REVIEW_PASS_NONPRODUCTION_CANDIDATE_INDEPENDENT_TIER_C_REVIEW_REQUIRED`

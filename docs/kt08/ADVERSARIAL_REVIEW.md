# ANIMO-KT08 Same-Agent Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Frozen evidence/tooling head reviewed:

`6927d8f66bd5948797b163880a869ecc0be4c391`

Exact-head CI:

`35291286873 -> SUCCESS`

## Review verdict

`PASS_B1_FULL_LWKM_EXPLICIT_PRODUCER_SEQUENCE_EVIDENCE`

No material finding remains open.

KT08 is an evidence/tooling qualification only. It changes no scientific
process, state ownership, runtime transaction semantics, restart semantics,
solver/numerical policy or production source.

## Full-sequence coverage

PASS within the exact pinned LWKM source envelope.

The supplied source is pinned by SHA-256:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

The frozen derived sequence contains 1800 Hlpimp=11 packets with:

- 30 layers;
- 30 horizons;
- 5 drainage systems;
- explicit interception state on every packet;
- soil-temperature payload on every packet;
- producer-coordinate coverage from origin 0 d through endpoint 18263 d;
- no detected chain discontinuity after frozen KT03 diagnostic normalization.

Observed producer durations are:

- 8 d: 37 packets;
- 9 d: 13 packets;
- 10 d: 1400 packets;
- 11 d: 350 packets.

The duration sum is exactly 18263 d, equal to the final endpoint minus the
first origin.

## Complete sequence identity

PASS.

KT08 persists three independent aggregate identities:

1. ordered normalized typed-step digest sequence:
   `c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4`;
2. ordered dynamic logical-record-group digest sequence:
   `40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34`;
3. ordered packet-index/endpoint/duration/group-digest/typed-digest sequence:
   `eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1`.

These identities compactly commit to every packet and to the complete ordered
producer sequence without adding the 2.4 MB raw legacy file or a large
per-packet manifest to the repository.

Representative anchors cover all four duration classes and positions across
the sequence, including first and last packets.

## Validation path

PASS within B1 scope.

The raw-source materializer is fail closed on:

- raw source SHA mismatch;
- static Hlpimp/dimension/temperature mismatch;
- producer model header mismatch;
- incomplete dynamic record grouping;
- KT03 packet validation failure;
- missing explicit interception projection capability;
- producer-coordinate gap or overlap;
- any of the three aggregate sequence identity mismatches;
- duration-histogram mismatch;
- first/last temporal envelope mismatch;
- interception-storage summary mismatch.

CI cannot execute the raw-source materializer because the supplied B0 file is
not committed. CI instead verifies the frozen B1 summary, independent aggregate
pins, anchor identities, temporal arithmetic, and reruns KT03, KT05 and KT07
regression evidence.

This limitation is explicit and does not promote the evidence to B2.

## KT08-R1 disposition

CLOSED.

The initial rematerializer emitted all scientific/evidence identities but did
not reproduce all descriptive metadata in the committed summary. The first
remediation added exact semantic anchor-role metadata and stronger explicit
pins. A follow-up parity inspection found the title field still absent and
closed that residual mismatch at the frozen head.

No producer value, digest or temporal result changed during KT08-R1
remediation.

## Relationship to KT07

PASS.

KT07 proved full compiled KT05 consumption for the first real LWKM packet.
KT08 does not repeat that compiled payload proof for all 1800 packets. Instead
it strengthens the producer-side evidence from one packet to the full ordered
sequence.

The two workunits therefore have distinct claims:

- KT07: complete first real packet -> compiled KT05 boundary;
- KT08: complete pinned producer sequence -> normalized B1 sequence identity
  and temporal envelope.

## Relationship to KT06

PASS, no authority leakage.

KT08 does not consume KT06 as qualified authority and does not define a
multi-packet forcing provider.

The facts that real producer packets are chained and have durations 8 through
11 days do not decide:

- runtime packet selection;
- retry identity;
- timestep subdivision;
- forcing cache lifetime;
- accepted-state publication;
- calendar mapping.

Those remain future runtime/coupling semantics and cannot be inferred from
KT08.

The KT06 GOV04 Tier C independent-review gate remains unchanged.

## Evidence strength

The evidence classification remains:

`B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2`

The frozen KT03 `legacy_dble_trunc_diagnostic` remains diagnostic-only. KT08
does not claim historical Intel/compiler equivalence or historical executable
truth beyond the pinned byte-derived producer payload.

## Final disposition

`SELF_REVIEW_PASS_B1_FULL_SEQUENCE_EVIDENCE_TOOLING_ONLY`

Open material findings: none.

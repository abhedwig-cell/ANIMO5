# ANIMO-KT11 Independent GOV04 Tier C Second-Line Review

Review branch: `review/animo-kt11-multi-packet-hydrology-provider-independent`

Review target: `ANIMO-KT11 - Typed Multi-Packet Hydrology Provider and Forcing Lifecycle`

Frozen candidate head: `843ac357f8b86f84131ddc08bf2097bb5af4e080`

Frozen implementation:

`prototype/kt11/mod_animo_multi_packet_hydrology_provider.f90`

Frozen implementation blob:

`a41d0f61da6dd30a18dbfadbe4b29b00259fa41e`

Risk tier: `GOV04_TIER_C_RUNTIME_SEMANTICS`

Review mode: `GENUINELY_INDEPENDENT_SECOND_LINE` in the GOV04 sense of a
separate review context. This establishes process independence only, not
organizational or human independence. Earlier same-agent conclusions were read
only as review support and were not used as proof.

## Principal verdict

`PASS_CLAIM_UNCHANGED`

The frozen candidate supports the bounded claim as written:

> An immutable collection of complete KT05 explicit hydrology packets can
> deterministically select exactly one packet from a bounded whole-day KT02
> requested interval, remain stateless across repeated requests, fail closed on
> missing or duplicate interval keys, and delegate the selected packet through
> admitted KT06 without changing KT02 time, accepted-state or publication
> ownership.

No material finding requires a semantic change to packet identity, lookup
ownership, forcing ownership, time ownership, accepted-state semantics, interval
mapping or consumed scientific authority.

This review does not admit KT11. Formal disposition and admission remain
separate programme actions.

## Governance and review boundary

The review applied the qualified GOV04 risk-tiered policy from
`work/animo-gov04-risk-tiered-review-policy`, including:

- Tier C requires one genuinely independent second-line review;
- reused evidence must be pin-verified, scope-compatible, immutable and not
  superseded;
- reused evidence retains its original strength and cannot be promoted;
- Tier C remains fail closed and does not imply production authorization.

At review execution, the only repository branches matching KT11 were:

- `work/animo-kt11-multi-packet-hydrology-provider`;
- `review/animo-kt11-multi-packet-hydrology-provider-independent`.

Both pointed to the review-handoff support head
`ca732a050f3f6534883a5dec3ed2958f38ff4cc9` before this report was persisted.
No later KT11 implementation branch or competing semantic claim was found.

The review branch is one support commit ahead of the frozen candidate before the
independent review evidence is added. That support commit adds or updates only
workflow/review documentation and checkpoint material. The frozen KT11 provider
implementation remains the exact blob named above.

A comparison from admitted KT06 authority
`ANIMO-KT06-A1@56384db4107aed484218363e26dbb7be7f51e8de`
to frozen KT11 head adds KT11-owned workflow, documentation, reference evidence,
tests, tooling and provider source. It does not modify frozen KT02, KT05 or KT06
implementation surfaces and does not modify production source.

## Independently verified executable evidence

Exact frozen-candidate workflow run:

`35351056242 -> SUCCESS`

GitHub Actions job:

`105619025907 / provider-lifecycle -> SUCCESS`

The job log independently confirms checkout of exact head
`843ac357f8b86f84131ddc08bf2097bb5af4e080`, followed by successful execution
of:

- frozen KT02 dual-client runtime and structure tests;
- frozen KT05 compiled adapter and structural-contract tests;
- frozen KT06 explicit hydrology runtime-binding tests;
- KT11 KT08/KT09 upstream evidence identity checks;
- compiled KT11 multi-packet provider tests under gfortran with
  `-std=f2008 -Wall -Wextra -Werror -fcheck=all`;
- checkpoint JSON validation.

Observed terminal results include:

- `KT02 dual-client runtime tests: PASS`;
- `KT02 structure checks: PASS`;
- `KT05 explicit Fortran hydrology adapter tests: PASS`;
- `KT05 structural contract tests: PASS`;
- `KT06 explicit hydrology runtime binding tests: PASS`;
- `KT11 upstream KT08/KT09 evidence identity: PASS`;
- `KT11 multi-packet hydrology provider tests: PASS`.

The workflow pins the consumed frozen blobs:

- KT06 runtime binding:
  `9a24ea833291f761d2fa76ca4cc9fee28436c614`;
- KT05 explicit hydrology adapter:
  `9ed1d6d3e91d9f5522f8c2a49a5e19eed1d82a9a`;
- KT02 interval runtime:
  `ac8eed3b7385daad3cb7c926bd7dab9d99e0a888`;
- KT02 transactions:
  `182164ca4bf4a890d98f9c89366764e5d818b10c`;
- KT08 sequence summary:
  `6ba7fe07ca47a6f8d45f18d09b7276dc4ece66f3`;
- KT09 representative packet fixture:
  `8aa4f5dcc8041979d9dc2e2b4fc8cc7f1c88de84`.

## Independent reconstruction of the claim

### Packet identity and duplicate semantics

PASS.

KT11 converts each packet's producer endpoint and producer duration into exact
nonnegative INT64 keys under the explicit bounded REAL64 envelope
`0 .. 2^53-1`. Initialization rejects nonfinite, negative, fractional or
non-roundtripping metadata and rejects any duplicate exact
`(endpoint, duration)` pair before the provider becomes configured.

Within the claimed whole-day mapping, the pair is sufficient to identify the
producer interval because its origin is determined by
`endpoint - duration`. A second packet with the same endpoint and duration
would therefore be semantically ambiguous and is correctly rejected.

The implementation scans the full private key set and still has a defensive
runtime ambiguity guard. Storage order is not part of the lookup semantics.

### Equal endpoint with different duration

PASS.

Equal endpoints with different durations are distinct intervals because they
imply different origins. The runtime key is reconstructed from the KT02 origin
and endpoint as:

- `runtime_step = endpoint - origin`;
- `expected_endpoint = endpoint + configured producer_day_offset`.

The compiled test explicitly stores `(20,20)` and `(20,10)` and selects the
first from KT02 interval `0 -> 20` and the second from `10 -> 20`.
No endpoint-only ambiguity is introduced.

### Provider-owned deep copy

PASS.

The frozen KT05 `hydrology_step_t` contains scalar values and allocatable
components, with no pointer components. KT11 performs intrinsic derived-type
assignment into its private allocatable packet array. For allocatable components,
Fortran intrinsic assignment creates independently allocated value copies rather
than aliases to the caller's allocations.

The compiled KT11 harness then mutates the caller-owned packet after
initialization, including schema id, endpoint, duration, scalar forcing and an
allocated vector. The already configured provider still binds the original
interval successfully. This is a strong causal check because an alias of the
mutated schema/time metadata would fail KT05/KT06 validation.

The provider's packet arrays and key arrays are private, so no public in-place
mutation path exists after successful initialization.

### Stateless repeated lookup and lifecycle scope

PASS within the declared lifecycle definition.

There is no cursor, consumed flag, mutable selected index, request counter,
cache state or packet-removal operation in the provider. Every call derives its
key from the supplied KT02 interval and scans immutable private keys.

The repeated-selection test invokes the same request twice against the same
provider and origin payload and obtains valid candidates both times.

The type can of course be replaced or reinitialized by an owning caller as a
whole object. That is not a mutable in-provider lifecycle and is outside the
claim. Dynamic reload, streaming, cache eviction and external producer
orchestration remain explicit nonclaims.

### Sparse and unordered provider behaviour

PASS.

KT11 intentionally does not claim contiguous or complete provider storage.
Unordered storage is tested and has no semantic effect. Sparse storage is
permitted, but a requested absent key returns
`HYDROLOGY_PACKET_NOT_FOUND` before a KT06 candidate is produced.

This is fail-closed behaviour. It is not evidence that all producer intervals
have complete runtime payloads.

### Missing-packet atomicity

PASS.

Frozen KT02 executes an interval against a private `working` accepted store.
It assigns that working store back to the externally accepted store only after
the exact requested target is reached.

The KT11 missing-middle test deliberately permits one successful private
working commit, then encounters a missing second packet. The interval fails.
The external generation remains zero, external time remains at the original
origin and the external payload token remains unchanged.

KT11 therefore does not introduce a partial external publication path.

### KT06 delegation

PASS.

After lookup, KT11 constructs a local frozen KT06 runtime-binding client,
deep-copies the selected complete packet into its forcing field, supplies the
same calendar binding and producer-day offset, and calls the admitted KT06
`execute_attempt`.

KT06 independently revalidates:

- the KT05 complete packet;
- exact producer endpoint and duration;
- KT02 runtime duration;
- producer endpoint mapping;
- overflow;
- KT05 projection.

Only after those checks does KT06 return its bounded probe candidate and
admissibility result.

KT11 therefore adds lookup but does not replace KT06's binding/projection
authority and does not create an alternate publication mechanism.

### Forcing ownership and accepted continuation state

PASS.

The selected hydrology packet remains provider/client-side. Frozen KT06's
accepted probe payload contains only the synthetic `state_token`; forcing is
not copied into accepted continuation state.

KT11 multi-step and real-anchor tests verify that accepted time advances through
KT02 while the probe-state token is preserved. This supports the ownership
claim without turning the probe into a scientific ANIMO execution claim.

### KT02 time and publication ownership

PASS.

Frozen KT02 remains sole owner of accepted time, lineage/generation protection,
private interval commits and final external publication.

KT11 receives origin and endpoint coordinates as inputs. It does not construct,
advance or publish a `TimeCoordinate`. Producer endpoint metadata is used only
for matching against the KT02 request.

Frozen KT02 transaction code independently guards lineage, generation, origin
time, forward endpoints, admissibility, payload validity and generation
overflow.

### Calendar and producer-day offset

PASS within the stated bounded composition contract.

Both KT11 and frozen KT06 require origin and endpoint calendar ids to equal the
configured runtime calendar id and require whole-day coordinates for this
claim. The producer-day offset must be nonnegative.

No generic calendar conversion, producer epoch discovery or fractional/subday
mapping occurs. The calendar relation is therefore a composition assertion, not
producer-carried calendar provenance. That limitation is explicitly outside the
claim rather than silently inferred.

### Overflow and exact-integer boundary

PASS by direct source reconstruction plus inherited frozen regression evidence.

Packet endpoint and duration are bounded to exact nonnegative REAL64 integer
metadata up to `2^53-1`. The conversion is fail closed.

For runtime mapping, KT11 rejects a producer endpoint addition when:

`endpoint_time%day_index > huge(int64) - producer_day_offset`.

The runtime duration subtraction is safe under the preceding constraints
`origin >= 0` and `endpoint > origin`: the positive difference cannot exceed
the INT64 endpoint itself.

KT11 does not contain a dedicated test for every `2^53-1` boundary value, but
the relevant conversion and overflow logic was inspected directly, frozen KT06
uses the same bounded relation, and the exact-head workflow reruns frozen KT06
qualification. No uncovered arithmetic path was found that materially threatens
the KT11 claim.

This is retained as a test-coverage observation, not a semantic finding.

### Retry and timestep-selection exclusions

PASS as exclusions.

KT11 selects forcing for the interval that KT02 presents. It contains no
timestep controller, retry budget, endpoint proposal or retry policy.

Frozen KT02's retry flag applies only after an admissibility rejection. A hard
client failure such as a missing KT11 packet terminates the interval as
`CLIENT_ATTEMPT_FAILED`; KT11 does not silently enter a retry path.

Repeatable lookup makes a repeated request deterministic if an external policy
chooses to make one, but KT11 does not qualify that policy.

### KT08 and KT09 evidence strength

PASS.

KT08 is explicitly labelled
`B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2`. Its pinned summary reports 1800
packets, zero chain violations, 1800 unique endpoints and duration classes 8, 9,
10 and 11 days for the pinned LWKM producer file.

KT08 itself explicitly excludes multi-packet forcing-provider semantics and
runtime integration.

KT09 contributes eight representative complete real-derived packets spanning
those duration classes and sequence positions. Its fixture is source-linked to
the same pinned producer identity.

The KT11 evidence test checks these identities and nonclaims. This review does
not promote either KT08 or KT09 to B2, runtime authority, complete 1800-packet
payload execution or scientific admissibility.

## Material findings

None.

No semantic reopen trigger from the review entry contract was reached.

## Non-material observations and retained limitations

1. The provider is immutable through its configured public behaviour, but an
   owning caller may replace/reinitialize the whole provider object. Dynamic
   mutable lifecycle remains outside scope.
2. The calendar binding is configured composition metadata, not producer-carried
   calendar provenance.
3. Sparse-provider success proves deterministic lookup, not complete producer
   coverage. Missing coverage deliberately fails closed.
4. KT08 proves a pinned 1800-interval temporal sequence, while KT09 provides
   eight complete representative packets. Full 1800-packet complete-payload
   runtime execution is not demonstrated.
5. KT02 collapses detailed provider/delegate hard-failure reasons to
   `CLIENT_ATTEMPT_FAILED` at the public interval boundary. This is diagnostic
   debt, not a state/publication semantic defect.
6. KT11 has no dedicated test for every exact-integer/overflow boundary. The
   arithmetic path is directly bounded and inspected, and frozen KT06 regression
   is rerun, so this does not require semantic or non-semantic remediation for
   the present claim.
7. The successful runtime client remains a probe. It does not establish
   `Hydro_detailed` scientific execution or ANIMO scientific admissibility.

## Explicit nonclaims retained

This review does not qualify or admit:

- full 1800-packet complete-payload execution;
- runtime SWATRE.UNF decoding;
- dynamic streaming or mutable provider lifecycle;
- retry or timestep-selection policy;
- fractional or subday mapping;
- generic calendar conversion;
- Hlpimp scientific semantics;
- `Hydro_detailed` scientific execution;
- ANIMO scientific admissibility;
- production coupling or migration;
- B3 or B4;
- Status A or Status AA.

## Disposition

Principal verdict:

`PASS_CLAIM_UNCHANGED`

The genuinely independent GOV04 Tier C second-line review gate is satisfied for
the exact frozen KT11 candidate claim and implementation identified above.

The frozen implementation was not changed by this review. The next permitted
action is formal GOV04 Tier C disposition and admission bookkeeping against
these exact pins, without widening the claim.

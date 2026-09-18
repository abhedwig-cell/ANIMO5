# ANIMO-KT06 Independent GOV04 Tier C Second-Line Review

Review branch: `review/animo-kt06-explicit-hydrology-runtime-binding-independent`

Review target: `ANIMO-KT06 — Explicit Hydrology Runtime Interval Binding`

Frozen implementation head: `fc818917a46408d55cd7f03e2fa8257534683907`

Frozen implementation blob:

`prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`
= `9a24ea833291f761d2fa76ca4cc9fee28436c614`

Risk tier: `GOV04_TIER_C_RUNTIME_SEMANTICS`

Review mode: genuinely independent second-line review. The frozen implementation was treated read-only. Earlier same-agent conclusions were not used as proof of correctness.

## Principal verdict

`PASS_CLAIM_UNCHANGED`

The candidate claim is supported within its declared narrow envelope:

> Within the declared exact whole-day envelope, a complete explicit-state KT05
> hydrology packet can be bound to a KT02 requested interval without making
> producer time authoritative, without placing forcing in accepted continuation
> state and without bypassing KT02 atomic publication.

No material finding was identified that changes time ownership, forcing ownership, accepted-state semantics, interval mapping or consumed scientific authority.

This verdict does not qualify Hlpimp semantics, Hydro_detailed science, ANIMO scientific admissibility, retry/timestep policy, a multi-packet forcing provider, production coupling, B3/B4, Status A or Status AA.

## Independently reconstructed evidence boundary

The review verified the frozen KT06 implementation blob on the review branch is exactly `9a24ea833291f761d2fa76ca4cc9fee28436c614`.

The KT06 delta from the closed KT05 base `3319e57adbf6036a86684f8e26d9559454c07b82` to frozen head `fc818917a46408d55cd7f03e2fa8257534683907` adds only KT06 workflow, documentation, checkpoint, runtime-binding prototype, reference metadata and KT06 tests. It does not modify the KT02 runtime core or KT05 adapter.

Consumed frozen implementation surfaces were inspected directly:

- KT02 time: `prototype/kt02/runtime/mod_transient_time.f90`, blob `c43e3c761637054dd6166488ecb01902ce547771`;
- KT02 transactions: `prototype/kt02/runtime/mod_transient_transactions.f90`, blob `182164ca4bf4a890d98f9c89366764e5d818b10c`;
- KT02 interval runtime: `prototype/kt02/runtime/mod_transient_interval_runtime.f90`, blob `ac8eed3b7385daad3cb7c926bd7dab9d99e0a888`;
- KT05 explicit-state adapter: `prototype/kt05/mod_animo_hydrology_adapter.f90`, blob `9ed1d6d3e91d9f5522f8c2a49a5e19eed1d82a9a`.

The exact frozen KT06 CI run `35286651951` was independently checked through GitHub Actions job state. Its runtime-binding job completed successfully, including frozen KT02 qualification tests, frozen KT03 adapter tests, frozen KT05 compiled tests, KT06 fixture parity, KT06 runtime-binding tests and JSON validation.

KT10 was used only as supplemental adversarial evidence. At KT10 closeout `e4f7f4576cbe5b4d8f2b57b16ea98041fcc06428`, the KT06, KT02 interval/transaction and KT05 adapter blobs remain identical to the frozen blobs above. Exact-head KT10 run `35294863617` completed successfully. No semantic authority is imported from KT10.

KT07-KT09 were used only to narrow the producer/contact limitation. They strengthen B1 contact with real producer packets but do not define packet selection, forcing lifetime, calendar conversion, retry identity or publication policy.

## Review against required semantic questions

### Accepted-time ownership

PASS.

Surface: `prototype/kt02/runtime/mod_transient_interval_runtime.f90` and `prototype/kt02/runtime/mod_transient_transactions.f90`.

KT02 obtains the accepted origin from the accepted store, constructs private trials, commits only through `commit_trial`, and publishes externally only after the private working store reaches the requested target. KT06 receives `origin_time` and `endpoint_time` as inputs to `execute_attempt`; it has no path that writes accepted time.

Effect on review axes: no change to time ownership or accepted-state semantics.

### External-publication ownership and interval atomicity

PASS.

Surface: `prototype/kt02/runtime/mod_transient_interval_runtime.f90`, especially the private `working = external_accepted` interval execution and the final `external_accepted = working` publication after exact target completion.

The KT06 two-request stale-forcing test performs one successful private working commit and then fails the second request. External generation, time and payload remain unchanged. This demonstrates that KT06 does not introduce an alternate publication path.

Effect on review axes: no change to publication ownership or interval mapping.

### Producer endpoint and duration influence

PASS.

Surface: `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`, `execute_explicit_hydrology_attempt`.

Producer endpoint and step are converted only after KT05 validation, are required to be exact nonnegative REAL64 integers within the declared bounded envelope, and are compared against the KT02 request. They are never used to construct or advance a KT02 `TimeCoordinate`.

The runtime step is computed from the KT02 origin and endpoint. Producer duration must equal that runtime step. Producer endpoint must equal the KT02 endpoint plus the configured nonnegative day offset. Overflow fails closed.

Effect on review axes: producer time remains validation metadata; accepted-time ownership is unchanged.

### Calendar-id and integer-offset semantics

PASS within the stated envelope.

Surface: `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`.

Both runtime origin and endpoint must carry the configured runtime calendar contract id. Both must be whole-day coordinates. The producer offset is a configured nonnegative integer relation. KT06 performs no epoch inference and no calendar conversion.

A caller can configure the calendar-id string; therefore this is a composition assertion, not independently discovered producer calendar semantics. That limitation is already consistent with the claim because generic calendar conversion is excluded.

Effect on review axes: no interval-mapping change; the review accepts only the declared configured relation.

### Integer/REAL64 boundary and overflow

PASS.

Surface: `exact_nonnegative_integer` in `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`.

KT06 deliberately bounds producer integer metadata to `2^53 - 1`, rejects nonfinite, negative, fractional and negative-zero encodings, and bit-compares the REAL64 value against the round-tripped integer representation. Runtime origin is required nonnegative and endpoint strictly forward, so runtime-step subtraction is safe. Producer endpoint plus offset has an explicit int64 overflow guard.

KT10 additionally exercises the maximum admitted value, the immediately higher rejected value, NaN, infinity, negative values, negative zero and producer-mapping overflow.

Effect on review axes: no semantic reopening required.

### KT05 validation and projection ordering

PASS.

Surface: `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90` and frozen `prototype/kt05/mod_animo_hydrology_adapter.f90`.

KT06 first calls `validate_hydrology_step_explicit`. Only after successful structural validation and successful runtime-time relation checks does it call `project_hydro_detailed_explicit`. A candidate payload is allocated only after projection succeeds.

KT05 itself validates schema id, unit contract, dimensions, allocation/shape, explicit interception state, finite values and positive producer step before producing the bounded `Hydro_detailed` external subset.

Effect on review axes: consumed scientific authority remains KT05's already bounded call-boundary projection only.

### Forcing ownership and continuation-state exclusion

PASS.

Surface: KT06 client type and probe payload in `prototype/kt06/mod_animo_explicit_hydrology_runtime_binding.f90`.

The complete `hydrology_step_t` is a member of the transient client. The accepted payload type contains only `state_token`. The successful candidate clones only that token and does not copy forcing into accepted continuation state.

The tests explicitly verify the accepted state token remains unchanged after successful binding.

Effect on review axes: forcing ownership remains external/client-owned; accepted continuation-state semantics are unchanged.

### Lineage and generation protection

PASS.

Surface: `prototype/kt02/runtime/mod_transient_transactions.f90`.

Trials preserve origin lineage, generation and time. `commit_trial` rejects lineage mismatch, stale generation, origin-time mismatch, nonforward endpoint, incomplete/nonadmissible evidence, invalid payload and generation overflow. KT06 has no API to override these fields.

KT10 confirms generation overflow does not publish external state.

Effect on review axes: no change to lineage, generation or publication authority.

### Retry semantics

PASS as an exclusion, not as a qualified capability.

Surface: `prototype/kt02/runtime/mod_transient_interval_runtime.f90` and KT06 client.

KT02 owns the generic retry flag only for acceptance rejection. A KT06 structural/time/projection failure returns `client_ok = .false.`, which terminates the interval rather than entering the acceptance-retry path. KT06 itself contains no retry policy and no timestep selection.

KT10 explicitly verifies that setting the retry-permitted flag does not mask a KT06 hard client failure.

Effect on review axes: no retry semantics are imported into the candidate claim.

### Forcing lifecycle, stale forcing and packet selection

PASS with an explicit bounded limitation.

Surface: KT06 client has exactly one `forcing` packet and no provider/selector interface.

The implementation therefore proves one-packet binding only. It does not qualify packet lookup, multi-packet sequencing, retry-aware forcing identity or lifecycle management. The stale-forcing two-request test correctly demonstrates fail-closed nonpublication when the one packet ceases to match the next private request.

KT08 sequence evidence does not alter this conclusion because it explicitly does not define runtime packet selection or forcing lifetime.

Effect on review axes: no semantic reopening; these remain outside the candidate claim.

### Probe admissibility versus ANIMO scientific admissibility

PASS.

Surface: public type name `animo_explicit_hydrology_runtime_probe_client_t`, `animo_runtime_probe_state_t`, work-unit contract and tests.

After binding and KT05 projection, KT06 deliberately returns an admissible no-op probe candidate with the unchanged synthetic state token. It does not call `Hydro_detailed`, `Modflux`, reaction, transport or conservation logic.

The probe naming, synthetic payload and explicit documentation are sufficiently strong to prevent this result from being a legitimate basis for ANIMO scientific admissibility.

Effect on review axes: no consumed scientific authority is expanded.

### Hlpimp, Hydro_detailed science, production and B3/B4 claims

PASS as exclusions.

Surface: frozen KT06 source and base-to-head diff.

KT06 imports the KT05 explicit-state carrier/projection only. There is no Hlpimp branch, no KT03F01 authority use, no `Hydro_detailed` scientific execution, no production `src/` mutation, no timestep negotiation and no B3/B4/Status claim in the implementation.

Effect on review axes: no accidental scientific-authority or production-scope import found.

## Material findings

None.

No finding requires a change to time ownership, forcing ownership, accepted-state semantics, interval mapping or consumed scientific authority.

## Non-material observations and retained limitations

1. `runtime_calendar_contract_id` is configured by composition rather than carried by the producer packet. This is acceptable only because KT06 claims a configured exact relation and explicitly excludes generic calendar conversion.
2. KT06 owns one forcing packet at a time. Multi-packet provider semantics, packet selection and retry-aware forcing identity remain unqualified.
3. The KT02 public failure reason collapses detailed KT06 client failures to `CLIENT_ATTEMPT_FAILED`. This is diagnostic debt, not a semantic defect in the candidate claim.
4. The frozen KT06 test payload is synthetic for many fields. KT07-KT09 strengthen real-producer packet contact, but those later workunits remain supplemental and do not become runtime authority.
5. The deliberate `2^53 - 1` REAL64 integer bound is stricter than the set of all exactly representable floating values. It is nevertheless internally consistent, fail-closed and explicitly bounded.

None of these observations requires non-semantic remediation for this review verdict.

## Disposition

Principal verdict: `PASS_CLAIM_UNCHANGED`.

The independent Tier C review gate is satisfied for the candidate claim only. Formal qualification/admission bookkeeping, if required by programme governance, is a separate next action. No production, B3, B4, Status A or Status AA claim follows from this review.

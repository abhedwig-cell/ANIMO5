# ANIMO-STATEQ01 exact restore identity qualification

Status: `SYNTHETIC_EXACT_RESTORE_IDENTITY_RC_R6_RC_R7_PASS_REAL_ADAPTER_AND_FULL_SPLIT_RUN_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Canonical TIME admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

This qualification makes the fail-before-mutate identity side of checkpoint restore executable for the restricted `CORE_CNP_SUBSURFACE_ONLY` profile. It addresses RC-R6 external hydrology frame rebinding and reinforces RC-R7 exact physical-layout/P-site compatibility.

It contains no ANIMO physics and is not a production restart implementation.

## RC-R6 exact external-owner frame binding

Hydrology remains externally owned. A checkpoint therefore does not absorb a SWAP/WATBAL frame into ANIMO physical state. Instead, restore must bind a compatible frame for the next interval before any ANIMO state is constructed or mutated.

Using the TIME02 candidate identity, the qualification guard requires exact equality of:

- checkpoint accepted `t0` and frame `t0`;
- requested next-interval `t1` and frame `t1`;
- calendar contract;
- physical layout identity;
- geometry identity;
- hydrology schema identity;
- immutable frame content identity;
- producer accepted-generation identity.

No floating tolerance is used. A frame one exact second early at `t0` or `t1` is rejected. Floating-point values and non-normalized rational encodings are rejected as canonical time identity.

This matches the TIME02 principle that producer values are adapter inputs, while canonical interval identity uses exact normalized coordinates.

## RC-R7 checkpoint layout compatibility

The same precondition layer requires exact checkpoint/runtime agreement for:

- profile identity;
- normalized configuration identity;
- physical layout identity;
- geometry identity;
- accepted generation;
- soil-layer count;
- phosphorus activation;
- fast P-site count;
- slow P-site count.

For P-active state, the serialized site-resolved payload must also have exactly the declared `[soil_layer, fast_site]` and `[soil_layer, slow_site]` shapes. Extra legacy array capacity is not a compatibility escape hatch.

A mismatch is rejected before the accepted-state construction callback is entered. The guard does not transform, truncate, pad, reorder or project site state.

This independently reinforces the dedicated RC-R7 P-site layout qualification, whose workflow run `34336596224` passed 15/15 tests.

## Executable evidence

Qualification files:

- `tools/stateq01/restore_identity_guard.py`
- `tests/stateq01/test_restore_identity_guard.py`
- `.github/workflows/stateq01-restore-identity.yml`
- `integration/animo-state/RESTORE_IDENTITY_SENTINEL_STATUS.json`

GitHub Actions run `34336641147`, job `102417468899`, executed head `3deaa00ed6d7adeb64ffa1024866cf0ca5bd08a4` under CPython 3.12.14.

All 24 tests passed.

The suite includes positive compatible restore plus fail-closed sentinels for:

- one-second `t0` mismatch;
- one-second `t1` mismatch;
- calendar mismatch;
- stale producer generation;
- frame schema mismatch;
- frame content mismatch;
- frame layout mismatch;
- frame geometry mismatch;
- floating canonical time input;
- non-reduced rational time input;
- checkpoint/runtime profile, configuration, geometry, layout and generation mismatch;
- soil-layer mismatch;
- fast and slow P-site header cardinality mismatch;
- fast and slow P-state payload-shape mismatch;
- P activation mismatch.

Input non-mutation is also tested.

## Disposition

RC-R6 advances to:

`PASS_SYNTHETIC_EXACT_EXTERNAL_FRAME_BINDING_NON_B2`

RC-R7 remains:

`PASS_SYNTHETIC_EXACT_LAYOUT_FAIL_BEFORE_STATE_CONSUMPTION_NON_B2`

These passes establish candidate checkpoint preconditions, not behavioural restart equivalence.

Still open:

- qualification against real producer-specific SWAP/WATBAL frame adapters;
- profile-clean uninterrupted-versus-split ANIMO execution;
- canonical TIME admission;
- B2 historical-reference evidence;
- any production implementation.

No topology migration, physics change or hidden tolerance has been admitted.
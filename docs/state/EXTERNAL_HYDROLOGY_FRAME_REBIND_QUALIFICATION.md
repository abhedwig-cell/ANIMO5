# ANIMO-STATEQ01 external hydrology frame rebind qualification

Status: `QUALIFICATION_GUARD_PERSISTED_EXECUTION_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Canonical TIME admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

RC-R6 tests the checkpoint-side rule for hydrology-owned state. ANIMO must not duplicate the hydrology owner's physical state as its own canonical owner. After restore it must instead bind the external frame that exactly belongs to the restored interval.

This addendum is qualification-only. It contains no hydrology or ANIMO physics and does not define a production adapter.

## Contract basis

TIME02 candidate semantics require exact interval identity and reject a one-second frame mismatch without floating tolerance. ARCH01/ARCH02 require external-owner state to be restored through the exact compatible producer generation and schema rather than through an ANIMO duplicate. ARCH04 requires geometry/configuration compatibility before physical state is consumed.

The qualification guard therefore binds:

- exact candidate `t0`;
- exact candidate `t1`;
- producer accepted generation;
- geometry identity;
- hydrology exchange schema identity;
- normalized configuration identity.

The hydrology frame also carries a non-empty frame identity and content fingerprint as provenance. This sentinel does not yet qualify a registry that proves an existing frame ID can never be rebound to changed content; that remains adapter/provenance work.

## Fail-closed rule

Any bound mismatch must reject before the callback that first consumes hydrology frame content or constructs ANIMO process state.

This includes an exact one-second mismatch at `t1`:

```text
interval t1 = D + 0/1 day
frame    t1 = D-1 + 86399/86400 day
```

No epsilon or floating tolerance is permitted.

Changing `t1` also means a different interval. A longer or shorter producer frame cannot be silently truncated or extended by this contract.

## Executable sentinel

Harness:

`tools/stateq01/external_hydrology_frame_rebind_harness.py`

Tests:

`tests/stateq01/test_external_hydrology_frame_rebind_harness.py`

The suite checks exact-match success and fail-before-consume behavior for chronology, stale generation, geometry, schema and configuration mismatch. It also rejects floating and non-reduced time representations.

A passing sentinel closes only the synthetic RC-R6 rebind-guard gap. Behavioural uninterrupted-versus-split equivalence still requires a profile-clean executable case and canonical TIME admission remains external to STATEQ01.

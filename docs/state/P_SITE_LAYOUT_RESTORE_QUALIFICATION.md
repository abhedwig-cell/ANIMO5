# ANIMO-STATEQ01 P-site layout restore qualification

Status: `QUALIFICATION_GUARD_PERSISTED_EXECUTION_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

RC-R7 asks whether a checkpoint can be rejected before state construction when the target physical topology differs from the checkpoint topology.

This addendum narrows that question to phosphorus site cardinality and the directly related physical-layout coordinates. It adds no ANIMO physics and does not implement a production checkpoint reader.

## Source and architecture basis

STATEQ01 classifies:

- `P-002` equilibrium fast sorbed phosphorus as `[soil_layer;fast_site]` persistent state;
- `P-003` non-equilibrium slow sorbed phosphorus as `[soil_layer;slow_site]` persistent state.

Both require site-resolved restore with exact site cardinality.

ARCH04 separately requires exact physical-layout compatibility before checkpoint state bytes are consumed. Its fail-closed examples include different fast or slow P site counts, different layer geometry and incompatible precision representation. It explicitly forbids implicit resizing, truncation, zero filling or site-count conversion without a separately qualified migration procedure.

The logical site counts therefore belong to checkpoint topology even if the legacy implementation stores the values in arrays whose physical capacity is larger than the active count.

## RC-R7 qualification contract

The qualification-only guard binds these fields:

- state schema identity;
- geometry identity;
- soil-layer count;
- fast P site count;
- slow P site count;
- organic-fraction count;
- phosphorus activation;
- precision-policy identity.

Restore is allowed only when all bound fields match exactly.

A mismatch must fail before the first callback that can consume or construct persistent state. In particular:

```text
checkpoint fast_site_count = 2
runtime    fast_site_count = 3
```

must not become a three-site state by appending zero, and the reverse direction must not truncate a site. The same rule applies to slow sites.

## Executable sentinel

The persisted harness is:

`tools/stateq01/p_site_layout_restore_harness.py`

with tests in:

`tests/stateq01/test_p_site_layout_restore_harness.py`

The sentinel tests both directions of fast-site and slow-site cardinality mismatch, plus geometry, soil-layer, organic-fraction, state-schema and precision-policy mismatch. A callback counter verifies that incompatible layouts are rejected before state payload consumption.

This is synthetic contract evidence. It does not prove revision-53 uninterrupted-versus-split trajectory equivalence and does not authorize any topology migration.

## Admission consequence

A passing sentinel may close the explicit RC-R7 site-cardinality guard gap, but RC-R7 remains qualification evidence rather than STATE admission evidence until checkpoint restore is exercised in an admitted/profile-clean executable split-run context.

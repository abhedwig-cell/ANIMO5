# ANIMO-STATEQ01 management checkpoint addendum

Status: `SOURCE_QUALIFIED_CURSOR_CONTRACT_NOT_STATE_ADMISSION`

This addendum supersedes the earlier STATEQ01 wording that allowed `MGMT-002` to be either serialized or reconstructed from accepted time plus schedule identity.

## Mandatory continuation

For source-equivalent checkpoint continuation, the checkpoint must retain:

```text
management_schedule_identity
next_management_event_id / source-row identity
```

The next event identity is mandatory accepted continuation metadata.

## Derived event time

The exact event boundary need not be a second independently mutable owner. It is resolved from the bound schedule record under the admitted canonical TIME representation.

Until canonical TIME is admitted, this derivation remains an integration blocker rather than a reason to store a floating duplicate as canonical truth.

## Why time-only reconstruction is rejected

Revision 53 accepts a next raw event time at least `Tito+1e-6` and then applies a `-0.5` mapping into the Julian coordinate used by the event gate. Therefore a parser-valid next record can map at or before the just-completed accepted boundary while `Adnr` already points to that record.

Consequently, `first schedule event after accepted time` is not a universally source-equivalent reconstruction rule.

A future normalized configuration may choose to forbid such schedules. That would be a narrower admitted input-domain contract and still requires separate equivalence evidence. STATEQ01 does not silently impose it.

## Noncanonical legacy state

The open sequential-file position used by `Findadrfix` is implementation state. A normalized schedule index can locate the event from its explicit identity, so a raw byte/record offset is not part of the canonical checkpoint.

## Restore rule

Restore must fail before physical mutation if:

- the schedule identity does not match;
- the restored next-event identity is missing or duplicated;
- the event identity is not valid under the active configuration/P-class interpretation;
- its event boundary cannot be resolved exactly under the admitted TIME contract.

Event replay and event skipping remain hard split-run failures.

Canonical STATE remains `NOT_ADMITTED`.

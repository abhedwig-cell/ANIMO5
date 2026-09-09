# ANIMO-STATEQ01 management cursor continuation qualification

Status: `SOURCE_QUALIFIED_EXPLICIT_NEXT_EVENT_CURSOR_REQUIRED_FOR_SOURCE_EQUIVALENT_CHECKPOINT`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Scope

This audit qualifies the legacy management-addition continuation state around `Adnr`, `Tinead` and the `MANAGEMENT.INP` read position. It answers a narrow checkpoint question: can the next management event be reconstructed from accepted model time plus immutable schedule identity alone, or must canonical continuation retain an explicit event cursor?

The conclusion is that accepted time plus schedule identity is not universally sufficient for source-equivalent continuation. A canonical checkpoint must carry an explicit next-event identity/source-row cursor unless a future normalized schedule contract deliberately narrows the admitted input domain and separately proves reconstruction equivalence.

## 2. Initialization establishes a next-event cursor

`input1.for:1508-1519` initializes:

```fortran
Adnr = 1
...
Findadr(..., '>add001:')
Read(Uiad,*) Tinead
Tinead = Tinead + Judami - 0.5
```

Thus `Adnr` identifies the addition record whose event boundary is held in `Tinead`.

`Findadr` rewinds the management file before searching. After the first event time is read, no later `Uiad` access occurs in `Input1`, so the legacy file pointer remains positioned immediately after the first event-time record for the first `Input_addit` call.

## 3. Runtime progression is explicit and stateful

The main loop calls `Input_addit` when:

```fortran
Juda >= Tinead .and. (Juda-St) < Tinead
```

`Animo.for:459-467` therefore gives the event a half-open interval membership rule: an event on the current interval end is consumed in that interval, while an event on the previous boundary is not replayed.

For `Adnr >= 2`, `Input_addit.for:69-83` constructs the exact `>addNNN:` label and calls `Findadrfix`. Unlike `Findadr`, `Findadrfix` does not rewind; it searches forward from the current file position.

After the selected event payload has been read, `Input_addit.for:211-218` reads the next raw event time, validates it, increments the record index and converts the next event boundary:

```fortran
Read(Uiad,*) Tinead
rarg1 = Tito + 0.000001
Call Checkrea(..., Tinead, rarg1, ...)
Adnr = Adnr + 1
Tinead = Tinead + Judami - 0.5
```

Therefore the legacy continuation after a consumed event is explicitly:

```text
next addition record identity + next event boundary + forward file position
```

The physical file position is an implementation detail, but the next record identity is not.

## 4. `Tinead` is a schedule-derived coordinate, not an independent owner

The source computes `Tinead` from the management schedule plus `Judami`. Once the exact next event record and the exact schedule/time interpretation are known, its event boundary can in principle be resolved from immutable schedule data.

For a future normalized schedule, STATEQ01 therefore does not require both a mutable integer cursor and a duplicate mutable event-time owner. The candidate canonical continuation is:

```text
management_schedule_identity
next_management_event_id / source-row identity
```

The exact event boundary is a derived property of that schedule record under the admitted canonical TIME contract.

This derivation is not yet executable B3 evidence because canonical TIME is separately governed.

## 5. Accepted time alone is not sufficient

A tempting reconstruction rule would be:

```text
next event = first schedule event strictly after accepted time
```

Revision 53 does not justify that rule for the full parser domain.

`Input_addit` validates the next raw schedule time only against:

```text
next_raw_time >= Tito + 0.000001
```

It then maps that raw value to:

```text
next_absolute_time = next_raw_time + Judami - 0.5
```

Meanwhile the main-loop boundary satisfies structurally:

```text
accepted Juda = Judami + Tito
```

because `Juda` and `Tito` are initialized at `Judami` and zero respectively and are incremented by the same `St` each interval.

Consequently, a next raw event time in the source-valid interval:

```text
Tito + 0.000001 <= next_raw_time <= Tito + 0.5
```

passes the legacy lower-bound validation but maps to an absolute event boundary at or before the just-completed accepted boundary.

`Input_addit` is called only once in that interval. The cursor can therefore advance to a next event whose mapped boundary is already in the past. On the following interval the event gate requires previous `Juda < Tinead`, so that event is not consumed.

This source-level counterexample proves that `accepted_time + schedule_identity` cannot universally reconstruct `Adnr` by simply counting or searching future event times.

No claim is made that supplied production cases use this pathological spacing. The point is narrower: the legacy parser does not exclude it, so time-only reconstruction is not a generally source-equivalent checkpoint rule.

## 6. Testbank schedule identity evidence

A scan of the supplied testbank found 11 `Management*.inp` files containing addition schedules. In all 11, `>addNNN:` labels are unique, contiguous and start at 1.

This supports using an explicit normalized event identifier as a stable candidate cursor for the supplied corpus. It does not prove that arbitrary external management files obey the same property. A canonical configuration parser should validate event-ID uniqueness rather than relying on the legacy forward file pointer.

## 7. Canonical checkpoint consequence

For source-equivalent checkpoint readiness, `MGMT-002` is refined to:

```text
MANDATORY_EXPLICIT_NEXT_EVENT_ID
```

Restore must:

1. bind the exact immutable management schedule identity;
2. restore the exact next event/source-row identity;
3. resolve its exact event boundary from the admitted schedule/time representation;
4. reject a missing, duplicate or incompatible event identity before physical mutation;
5. never infer the cursor solely as the first event after accepted time unless that reconstruction rule has its own separately admitted input-domain contract and equivalence evidence.

A raw byte/file offset is not canonical state. A normalized event identity replaces that implementation-specific cursor.

## 8. Interaction with event ordering

The cursor only identifies which event record is next. It does not relax TS01 ordering requirements. Same-step management mutation must still occur at the source-qualified point in the process schedule, and an event must be neither replayed nor skipped after restore.

P-class-dependent event payload selection is part of configuration/schedule interpretation and must be bound by configuration identity. It is not free runtime cursor state.

## 9. Restart payload boundary

`Output_Init.for` contains no `Adnr` or `Tinead` serialization. Therefore legacy `INITIAL.OUT` cannot by itself restore this explicit reader progression state.

This is a checkpoint sufficiency gap, not by itself a newly allocated TCD. STATEQ01 does not assign a discrepancy number here because TS01 already identified the omitted management cursor and the present work qualifies its canonical representation requirement rather than establishing a new corrected-legacy behaviour.

## 10. Admission consequence

Management continuation is now structurally better specified:

- schedule identity: mandatory immutable checkpoint identity;
- next event/source-row identity: mandatory continuation field for source-equivalent replay;
- next event time: derived from the bound schedule under canonical TIME;
- file offset: noncanonical adapter implementation state;
- time-only reconstruction: not generally admitted.

What remains open is behavioural split-run qualification at event-adjacent boundaries and integration with the concrete TIME representation.

Final classification:

`SOURCE_QUALIFIED_EXPLICIT_NEXT_EVENT_CURSOR_REQUIRED_FOR_SOURCE_EQUIVALENT_CHECKPOINT`

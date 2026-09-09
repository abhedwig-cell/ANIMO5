# ANIMO-TIME02 calendar and exact boundary contract

Status: `QUALIFIED_CANDIDATE_CONTRACT_ONLY`.

## 1. Calendar contract

TIME02 defines candidate calendar identity:

`ANIMO_PG_86400_NOLEAPSECONDS_V1`

Semantics:

- proleptic Gregorian civil calendar;
- Gregorian leap rule: divisible by 4, except divisible by 100 unless divisible by 400;
- 24 hours per civil day;
- 60 minutes per hour;
- 60 seconds per minute;
- exactly 86,400 nominal seconds per civil day;
- no leap seconds;
- no time zone, daylight-saving or locale semantics in model time;
- year 0 is outside the TIME02 legacy-compatibility qualification envelope;
- `0001-01-01T00:00:00` has `day_index=0`.

The comments in the legacy Julian-day routines mention UTC conversion, but revision 53 contains no time-zone or leap-second model. TIME02 therefore treats these routines as civil-calendar/Julian-day arithmetic, not as evidence for a UTC timescale contract.

## 2. Simulation envelope

For revision-53 4.1 input:

- `StartDate=Y-M-D` maps to exact `Y-M-D 00:00:00`;
- `EndDate=Y-M-D` maps to exact next-day `00:00:00` because the source constructs the end with hour 24.

A completed run ending on the stated end date therefore has its final accepted boundary at the following midnight.

The first runtime interval is still semantically special under TS01 because initialization constructs the first accepted state before the ordinary lifecycle. TIME02 does not turn the first interval into evidence for generic retry or restart semantics.

## 3. Event classes keep their source endpoint predicates

Endpoint membership belongs to the event class, not to the interval object.

### Management packet

Source-equivalence predicate:

` t0 < E <= t1 `

Consequences:

- `E == t0`: excluded;
- `E == t1`: included.

This is an exact rational comparison.

### Annual harvest/root-residue trigger

Source-equivalence predicate:

` t0 <= H < t1 `

Consequences:

- `H == t0`: included;
- `H == t1`: excluded.

This asymmetry is retained. TIME02 does not classify it as correct science or as a defect; that requires its owning scientific/discrepancy gate.

### Report/balance boundary

Revision 53 uses a separate half-step report-crossing rule. It is diagnostic continuation semantics and must not be reused as a physical event or trial-acceptance predicate.

## 4. Exact just-before and just-after

"Just before" and "just after" in qualification vectors mean explicit exact coordinates, not a hidden epsilon. For civil tests TIME02 uses one exact second:

- one second = rational `1/86400` day;
- `t1 - 1 second` and `t1 + 1 second` are distinct canonical coordinates.

The representation can distinguish finer rational values, but no finer civil unit is asserted by this test convention.

## 5. Year boundary lifecycle

TS01 source evidence requires two different hooks around a year transition:

1. physical processing reaches `t1`;
2. if `t1` is 1 January, prior-year closeout/output occurs after physical execution;
3. the next interval begins at the same exact coordinate;
4. new-year initialization/input selection is evaluated from that next interval's `t0`.

TIME02 represents the shared boundary once. Scheduler semantics decide which hook is on which side. No `+epsilon` or `-epsilon` duplicate boundary is permitted.

## 6. Leap handling

Leap validation is exact and calendar-based:

- 2000-02-29 is valid because 2000 is divisible by 400;
- 1900-02-29 is invalid because 1900 is divisible by 100 but not by 400;
- 2004-02-29 is valid;
- 2100-02-29 is invalid.

Date parsing must fail closed on invalid civil dates before a coordinate is created.

## 7. Restart and checkpoint boundary

A checkpoint may identify only an accepted boundary under TIME01. It binds at least:

- exact accepted `TimeCoordinate`;
- `calendar_contract_id`;
- accepted state generation;
- configuration/layout identities;
- external-owner continuation/rebind requirements;
- event schedule/cursor continuation required by the restart contract.

On restore, the exact checkpoint coordinate becomes the new accepted `t0`. No event may be replayed or skipped merely because a reader cursor was reset.

The endpoint asymmetry has a concrete split consequence. If a split is exactly at `S`:

- a management event `E=S` belongs to the interval ending at `S`, not to the interval starting at `S`;
- a harvest event `H=S` belongs to the interval starting at `S`, not to the interval ending at `S`.

A correct restart must preserve that distinction without tolerance.

Revision-53 `INITIAL.OUT` alone is not evidence that arbitrary split/restart is complete. TS01 identifies missing temporal/report/external continuation concerns. TIME02 vectors therefore remain synthetic/non-B2.

## 8. Retry with changed t1

TIME01 identity rules are retained exactly:

- same `t0`, same `t1`, same accepted generation and immutable frames may be retried with a fresh `trial_id`;
- changing `t1` creates a new `interval_id`;
- all interval-scoped hydrology/crop frames and event membership must be rebound/recomputed for the new interval;
- a longer producer frame cannot be silently truncated unless a separately admitted adapter contract defines an exact transformation.

The old trial's selected physical events remain uncommitted after rejection.

## 9. Hydrology frame binding

A canonical hydrology frame is valid only if the producer adapter explicitly maps producer chronology to the ANIMO interval and binds exact canonical `t0` and `t1`.

Fail closed before process mutation for at least:

- frame `t0` differs from interval `t0`;
- frame `t1` differs from interval `t1`;
- frame and interval use different calendar contracts;
- producer accepted generation is stale;
- geometry/layout/configuration/schema identity differs;
- content changes under an existing frame ID.

No tolerance is permitted for these identity checks.

Legacy raw `TIWA` or `ST` values are adapter inputs, not canonical identity by themselves. `Tiwa == Juda`, `Tiwa == Tito`, or `Juda-St == previous Tiwa` may only be asserted by a producer-mode mapping that is separately evidenced.

## 10. External producer calendar shifts

Legacy `HydroYearSwitch` demonstrates that producer chronology may be deliberately remapped. Such mapping must be explicit and provenance-bearing:

```text
raw producer coordinate
+ producer calendar/schema identity
+ declared year/calendar transform
-> exact canonical frame coordinate
```

The transformed canonical coordinate is used for interval identity. The raw producer coordinate remains trace/provenance and must not be silently overwritten.

## 11. Acceptance rules for TIME02 boundary vectors

The vectors in `integration/animo-time/TIME02_TEST_VECTORS.json` pass only when:

- all coordinate comparisons are exact;
- management and harvest endpoints retain their distinct predicates;
- leap/date validity follows the calendar contract;
- split/restart does not change event ownership at the split;
- changed `t1` invalidates the old interval identity and requires frame rebind;
- any one-second hydrology frame mismatch is rejected;
- no test invokes floating tolerance.

These are candidate-contract tests. They are not B2 historical comparison evidence.

# ANIMO-STATEQ01 exact year-boundary continuation qualification

Status: `QUALIFICATION_HARNESS_PERSISTED_EXECUTION_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Canonical TIME admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

RC-R3 qualifies the state/checkpoint ordering at a year transition. It does not add annual physics, change deposition semantics or define a production scheduler.

TS01 source evidence establishes two different hooks around the same 1 January boundary:

1. the interval reaches its end `t1` and physical processing completes;
2. if `t1` is 1 January, prior-year output closeout occurs after that physical processing;
3. the following interval starts from the same coordinate as `t0`;
4. `Init` sees 1 January at interval start and activates new-year start semantics from the `t0` side.

TIME02 represents that boundary once, with an exact coordinate. No `+epsilon` or `-epsilon` duplicate boundary is permitted.

## Candidate checkpoint rule

A checkpoint at the year boundary binds the already accepted state at the exact shared coordinate after the prior interval's physical work and prior-year closeout. Restore returns that accepted state at exactly the same coordinate. The next-interval new-year hook then executes from the start side.

The checkpoint does not itself replay prior-year closeout, and restore does not pre-apply new-year initialization before the next interval begins.

This ordering is deliberately narrow. Reporting closeout is diagnostic continuation and does not become a physical state owner merely because it is sequenced around the accepted boundary.

## Executable sentinel

Harness:

`tools/stateq01/year_boundary_continuation_harness.py`

Tests:

`tests/stateq01/test_year_boundary_continuation_harness.py`

The synthetic sentinel checks:

- physical execution precedes prior-year closeout;
- checkpoint time and next interval start use one exact coordinate;
- split and uninterrupted lifecycle give the same synthetic physical/new-year state;
- restore does not replay prior-year closeout;
- new-year initialization occurs only on the next-interval side;
- a one-second offset from the shared boundary is rejected rather than treated as a hidden epsilon;
- floating and non-reduced rational coordinates are rejected by the candidate fixture.

## Evidence boundary

A passing sentinel is synthetic contract evidence only. It does not prove a revision-53 behavioural split across an actual supplied year boundary, does not admit TIME02 as canonical TIME and does not make reporting accumulators part of physical checkpoint state.

Source basis:

- TS01 `EVENT_BOUNDARY_SEMANTICS.md`, year-boundary section;
- TIME02 `CALENDAR_AND_BOUNDARY_CONTRACT.md`, year-boundary lifecycle and checkpoint rules.

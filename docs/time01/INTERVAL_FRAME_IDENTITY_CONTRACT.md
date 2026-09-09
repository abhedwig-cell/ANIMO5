# ANIMO-TIME01 interval and frame identity contract

Status: `CANDIDATE_CONTRACT_ONLY`.

## 1. Purpose

TIME01 needs a deterministic way to say which accepted state, model interval, external frames and attempt belong together. Revision 53 largely relies on call order and sequential input consumption. The candidate architecture makes these relationships explicit without claiming that the legacy source already carries such IDs.

## 2. Required identities

### `accepted_generation_id`

Identifies one immutable accepted ANIMO continuation state at `t0`.

It SHALL change only when an interval is accepted or an admitted state transition creates a new accepted generation. Rejecting a trial does not change it.

### `interval_id`

Identifies one proposed physical interval. Its semantic key includes at least:

- `t0`;
- `t1`;
- `calendar_contract_id`;
- accepted start generation identity;
- configuration/layout identity relevant to interpreting the interval.

Two attempts over the same unchanged interval may share `interval_id` but never `trial_id`.

If `t1`, calendar interpretation, accepted start generation or layout-bearing configuration changes, a new `interval_id` is required.

### `trial_id`

Identifies one execution attempt. Every begin-trial operation creates a fresh `trial_id`, including retries.

A `trial_id` may never be reused after reject or accept.

### `frame_id`

Every immutable external frame has its own content identity. At minimum hydrology and external crop frames are separate objects. A frame ID binds payload plus the metadata required to interpret that payload.

Changing any semantically relevant field or metadata under the same frame ID is forbidden.

### `event_id`

An event identity must survive retry/restart reasoning without relying on event occurrence order alone. It binds schedule/event source identity, event class, event time and row/packet ordering identity.

The same logical scheduled event may be observed by more than one rejected trial, but it may contribute physically only through the accepted trial journal for the interval that selects it.

### `checkpoint_id`

Identifies one accepted checkpoint bundle and manifest. It binds the accepted generation, accepted time coordinate, configuration/layout/schema identities, component versions and optional diagnostic continuation payload.

## 3. Canonical interval coordinate semantics

A candidate `TimeCoordinate` consists semantically of:

- `calendar_contract_id`;
- exact coordinate value in the representation selected by the future canonical implementation;
- optionally a derived civil/calendar view for event rules and reporting.

The representation SHALL support deterministic exact ordering and equality. Hidden epsilon comparison is forbidden for event membership and transaction identity.

TIME01 deliberately does not select a numeric storage type or minimum time quantum. That decision is a later implementation/numerical compatibility question.

## 4. Event endpoint classes

The interval identity itself does not imply event inclusion. Each event class declares an endpoint predicate.

Source-equivalence classes currently include:

| event class | predicate | TS01 basis |
|---|---|---|
| management packet | `t0 < E <= t1` | revision-53 main loop |
| annual harvest/root residue | `t0 <= H < t1` | `Addit` harvest logic |
| annual start logic | evaluated at interval start | `Init` |
| annual closeout output | evaluated at interval end after physical execution | main output path |
| balance/report closure | report-specific crossing rule | `Outbal_calc` |

A scheduler must route each event through its declared class. It must not infer a universal left-open/right-closed or left-closed/right-open convention.

## 5. External hydrology frame binding

A hydrology frame bound to a trial SHALL identify:

- producer/owner identity;
- producer accepted generation at `t0`;
- `t0` and `t1` under the same calendar contract as `interval_id`;
- spatial geometry and physical layout;
- schema/version identity;
- configuration/exchange binding identity;
- immutable content identity.

For source-equivalence, the frame must contain the begin/end storage coordinates and interval flux information required by the selected hydrology mode. TIME01 does not redefine ARCH05 field content.

A frame is rejected before process execution if its interval, generation, geometry, schema or configuration binding is stale or inconsistent.

## 6. External crop frame binding

Where crop state is externally owned, the crop frame follows the same interval/generation identity rules and additionally binds:

- crop owner identity;
- crop-state generation at `t0`;
- demand/state observation validity for the proposed interval;
- explicit residue/export bundles where physical transfers occur.

A crop state observation is not ANIMO-owned persistent state. Realized uptake is an interval result and must remain linked to the accepted trial and one physical transfer identity.

## 7. Retry identity rules

### Same interval, same immutable frames

Allowed as a new `trial_id` if retry policy permits it. The accepted generation and frame contents remain unchanged.

### Same interval, changed frame contents

Requires new frame IDs. Rebinding is explicit before retry. Silent mutation under prior IDs is forbidden.

### Changed `t1`

Requires a new `interval_id`. All interval-scoped frames/events must be revalidated for the new interval. A longer-period frame may not be silently truncated unless an admitted adapter contract explicitly defines that transformation.

### Changed configuration/layout/topology

Not a retry of the same interval. It requires an accepted-boundary transition under a separately admitted transition/state migration contract.

## 8. Restart identity rules

A restore must establish exactly one accepted generation at the checkpoint time and then rebind external owner state to that same accepted time/layout before creating the next `interval_id`.

A restart implementation must not infer event cursor correctness merely from 'next row'. It must either restore the cursor or deterministically reconstruct event selection from absolute schedule identity and accepted time, then prove no replay/skip under later B2 behaviour tests.

## 9. Required scheduler trace identity

Every diagnostic trace entry for a physical process boundary should carry at least:

- `interval_id`;
- `trial_id`;
- `accepted_generation_id`;
- `t0`, `t1`, `calendar_contract_id`;
- process/boundary ID;
- state generation read/written;
- external frame IDs used;
- selected event IDs when applicable;
- provisional/physical/diagnostic classification;
- accept/reject outcome when known.

Trace data is diagnostic and does not itself own physical state.

## 10. Fail-closed mismatches

The candidate contract requires failure before process execution for at least:

- `t0` mismatch between accepted state and interval;
- external frame generated from a different accepted producer generation;
- different calendar contract;
- stale geometry/layout/configuration identity;
- changed payload under an existing frame ID;
- reused `trial_id`;
- changed `t1` under the same `interval_id`;
- undeclared event endpoint class;
- feature/topology data inconsistent with active layout.

## 11. Qualification boundary

This identity model is a specification. It does not prove that independently developed hydrology or crop adapters can generate correct frames, and it does not admit exact split-run continuity or a concrete time encoding.

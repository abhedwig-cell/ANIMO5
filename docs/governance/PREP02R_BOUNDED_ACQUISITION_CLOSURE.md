# PREP02R bounded B2 acquisition closure

Work unit: `ANIMO-GOV02`

This document defines governance closure states for historical-reference recovery. It does not claim that an external request has been sent, answered or exhausted.

## Closure states

### `B2_REFERENCE_OBTAINED`

A candidate historical artifact has been recovered and its provenance is sufficient to enter the B2 qualification workflow. This state does not by itself mean the artifact is already qualified as B2.

### `B2_PARTIAL_HISTORICAL_EVIDENCE_OBTAINED`

Some independent historical evidence exists, but it is incomplete for the intended behavioural claim, path, environment or output surface. It may support reconciliation but cannot be treated as a complete B2 oracle beyond its qualified scope.

### `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

No usable reference was recovered after the bounded acquisition contract below was actually executed and independently reviewed. This is the only absence state that may open consideration of the strict historical-uncertainty scientific route. It is not a B2 substitute.

### `B2_ACQUISITION_STILL_ACTIVE`

Plausible acquisition work remains pending or in progress. The historical-uncertainty route is closed.

### `B2_ACQUISITION_INSUFFICIENTLY_ATTEMPTED`

The acquisition record does not yet meet the minimum reasonable-effort contract. The historical-uncertainty route is closed.

## Documented reasonable B2 acquisition effort

`DOCUMENTED_REASONABLE_B2_ACQUISITION_EFFORT` requires all of the following:

1. a targeted WUR archival request is actually sent via a verified institutional route;
2. the response is persisted, or a documented evidence trail shows that no recoverable artifact was obtained; silence must be represented as silence, not as a fictitious negative response;
3. at least one additional plausible archive/contact route is attempted where such a route is materially plausible, or a reviewed reason is recorded for why this requirement is not applicable;
4. the public-search history, terms, relevant repositories/catalogues and dates are persisted;
5. a stopping rationale explains why additional search has sufficiently low expected value for the defined scope;
6. an independent reviewer approves that stopping rationale;
7. no concrete, known, high-probability route remains deliberately unexplored.

The contract is bounded. It does not require an infinite search. It does require actual execution of the high-value routes identified before declaring unavailability.

## State-transition rules

```text
B2_ACQUISITION_INSUFFICIENTLY_ATTEMPTED
        |
        | actual targeted effort begins
        v
B2_ACQUISITION_STILL_ACTIVE
        |\
        | +--> candidate/partial evidence --> B2_PARTIAL_HISTORICAL_EVIDENCE_OBTAINED
        |                                   |
        |                                   +--> continued qualification/search
        |
        +--> qualified artifact recovered --> B2_REFERENCE_OBTAINED
        |
        +--> all reasonable-effort checks complete + independent stop review
              --> B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT
```

No state transition to `UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` may be inferred merely from elapsed time, inconvenience, tool limitations or failure of one public-web search.

## Current PREP02R mapping

The authoritative PREP02R status at GOV02 start records:

- `external_request_sent=false`;
- `historical_reference_artifact_obtained=false`;
- `native_reference_run_completed=false`;
- `native_vs_gnu_comparison_completed=false`;
- `reference_qualified=false`.

It also records that a targeted institutional request draft is prepared and that the next action is to send it through a verified WUR route.

Therefore GOV02 maps the current state to:

`B2_ACQUISITION_STILL_ACTIVE`

This means:

`historical_uncertainty_route_eligible=false`

No statement in GOV02 may call PREP02R exhausted or unavailable-after-reasonable-effort until the external acquisition actions have genuinely been performed and reviewed.

## Relationship to partial evidence

Documentation, source archives, testbank inputs, public reports and source-bound semantic reconstructions can all be historically informative without being a complete B2 behavioural reference. They retain their own evidence roles. Partial historical context must not be silently upgraded to `B2_REFERENCE_OBTAINED`.

## Reopening

Even after `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`, later discovery of a credible artifact reopens B2 qualification. The prior stopping rationale remains valid as historical provenance; it is not an argument to ignore new evidence.

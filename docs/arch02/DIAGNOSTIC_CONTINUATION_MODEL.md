# ANIMO-ARCH02 diagnostic continuation model

Status: `CANDIDATE_ARCHITECTURE_DESIGN_ONLY`.

ARCH01 correctly classifies legacy balance arrays as observers rather than physical state. ARCH02 adds one further distinction: some observer state can still be continuation-critical for reproducible reporting across a restart.

## Physical state and diagnostic continuation are different

`DiagnosticsLedger` does not own water, OM, N or P. It observes canonical state and committed transfer events. Therefore it must never be used to reconstruct physical model state and must never participate as an additional source or sink in conservation.

However, cumulative reporting over a period has memory. If a run is checkpointed halfway through such a period, discarding already accumulated diagnostic totals can change later reports even when the physical trajectory is identical.

ARCH02 therefore separates two promises:

1. **physical restart equivalence**: the restored simulation continues from the same accepted physical state;
2. **report-continuation equivalence**: cumulative reports after restart are identical to an uninterrupted run for the same reporting policy.

The second promise requires either diagnostic continuation payload or checkpoint placement at a diagnostic reset boundary.

## Candidate policy

### Main balances

`diagnostics.mass_balance` may be serialized in `DiagnosticContinuationState` when a checkpoint is created inside an active reporting period. Its contents remain observer state only.

Where checkpoints are restricted to balance-period boundaries, these accumulators may be reset and omitted.

### Detailed process accumulators

`diagnostics.process_transfers` follows the same rule. TCD-027 and TCD-028 show why these arrays cannot be considered authoritative physical transfers: defects in reporting accumulators can occur without a physical trajectory change.

A future implementation should preferably regenerate detailed reporting from committed typed transfer events over the reporting period. If the event history itself is not retained, the accumulated diagnostic view becomes the compact continuation payload for report continuity.

## Trial diagnostics

Diagnostics produced while evaluating a trial are provisional. They are either:

- discarded when the trial is rejected; or
- folded into committed diagnostic continuation state when the trial is accepted.

A normal checkpoint does not serialize provisional trial diagnostics.

## Restart integrity checks

When diagnostic continuation is restored, the manifest must bind it to:

- the same accepted model time as physical state;
- the same reporting interval definition;
- the same diagnostic schema version;
- the same process/quantity identifiers;
- the same control-volume definition.

If those identities differ, the diagnostic payload must not be silently reused. The caller may either fail closed or explicitly start a new reporting period according to a later qualified policy.

## Architectural consequence

`PersistentState` should not become a catch-all structure. A future checkpoint package can contain separate named sections such as:

- `ModelState`;
- `ExternalOwnerBindings`;
- `DiagnosticContinuationState`;
- `CheckpointManifest`.

This keeps scientific continuation state compact while still supporting reproducible operational restart.

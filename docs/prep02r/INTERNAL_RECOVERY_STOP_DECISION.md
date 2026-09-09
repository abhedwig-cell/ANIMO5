# ANIMO-PREP02R — Internal recovery stop decision

Date: 2026-09-09

Decision:

`STOP_FURTHER_INTERNAL_REFERENCE_RECOVERY_AND_PROCEED_WITH_AVAILABLE_EVIDENCE_WITHIN_EXISTING_GOV02_SCOPE`

## Why stop the internal search here

The internal PREP02R line has now extracted nearly all useful evidence available from the material currently in hand:

- B0 source and testbank identities are pinned;
- the GNU B1 diagnostic is reproducible;
- the supplied Intel Visual Fortran project materially reconstructs important build semantics, including eight-byte default REAL and saved local storage;
- the received `animo41.exe` is provenance-classified as a modern 2026 native rebuild rather than a historical release executable;
- Windows capture, fail-closed ingestion and file-level native-vs-GNU comparison machinery are prepared;
- a fresh explicit GNU Ruurlo file-level comparison surface is qualified for cross-runtime diagnostic use.

Further internal archaeology or additional tooling is unlikely to recover historical behavioural truth. No provenance-qualified ANIMO 4.1.5 revision-53 historical executable or executable-linked output has been found.

## What this decision does mean

For project planning, PREP02R is no longer an open-ended internal research task. Downstream work may use the available B0, B1, source, theory, conservation and synthetic evidence according to the claim-specific rules of the relevant work units.

Historical behaviour must remain explicitly `UNKNOWN` whenever B2 is absent.

The modern 2026 native executable may still be run later as cross-runtime diagnostic evidence if useful, but such a run is optional for internal reconstruction and cannot create historical B2.

## What this decision does not mean

This is not a governance relaxation and not a historical-reference admission.

GOV02 states that its no-B2 scientific admission route may only be activated after PREP02R reaches:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

GOV02 also records that an unsent prepared archival request leaves the acquisition state at:

`B2_ACQUISITION_STILL_ACTIVE`

That condition has not changed. The prepared WUR archival/provenance request has not been sent. Therefore:

- `normal_B2_reference_available = false`;
- `historical_uncertainty_route_eligible = false`;
- no historical-fidelity claim is admitted;
- no B3 correction may be admitted through the GOV02 historical-uncertainty route merely because internal PREP02R work has stopped.

Changing that rule to fit the available evidence would be a governance-policy change, not evidence recovery, and is intentionally not done here.

## Practical downstream rule

Use the current evidence as the best available technical basis, but keep the distinction between scientific readiness and historical fidelity intact.

This means the project can continue with claim-scoped readiness, qualification tooling, architecture, state, time, mass, runtime and other work that is not logically blocked by historical fidelity. Items whose actual admission contract requires the GOV02 no-B2 route remain fail-closed until acquisition closure and their other class-specific gates are satisfied.

## Reopening

PREP02R should only be reopened for substantive work if one of the following occurs:

1. a provenance-qualified historical executable, output bundle, build archive or release record is received;
2. the prepared external archival request is actually pursued and produces new evidence or a documented negative result;
3. a governing work unit identifies a specific unresolved historical question for which additional internal evidence can realistically be obtained.

Absent one of those triggers, additional internal PREP02R work should be treated as low-value scope expansion.

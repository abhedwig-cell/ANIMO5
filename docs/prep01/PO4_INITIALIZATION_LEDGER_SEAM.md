# CranGrass first-step PO4 initialization / mass-ledger seam

Status: `CAUSALLY_LOCALIZED_DIAGNOSTIC_NOT_REFERENCE`.

## Scope

This artifact localizes the largest PO4-P balance deviation observed in the deterministic PREP01 GNU diagnostic corpus. It does not change the frozen source or the original CranGrass testcase, and it does not establish a scientific acceptance tolerance.

Source identity and diagnostic build identity are pinned by the surrounding PREP01 evidence.

## Observation

For `CranGrass/bappTP.Out`, balance profile layer `0..22`, the first simulated balance period is the unique large full-profile PO4 deviation. A temporary instrumentation-only build captured the unformatted internal `Bapp(Ddev)` value before output formatting:

`-0.7235825146799 kg/ha P`

Subsequent first-day records in later years and subsequent timesteps in 1992 are orders of magnitude smaller. The anomaly is therefore tied to the initial-state transition, not to a recurring daily P-process drift.

## Source mechanism

The testcase uses `INPO=1`. In `Inicalc_P`, this mode accepts both:

- initial solution concentration `Copo`;
- initial instantaneous/fast sorption store `Amcxfa`;
- initial slow sorption stores `Amcxsl`;
- precipitated P `Ampopr`.

`Inicalc_P` recomputes the fast sorption amount with the source function `Fast(Optcxfa,...,Copo)` and emits a message only when the absolute volumetric difference exceeds `1.0d-4 kg/m3`. It does not make the supplied state exactly consistent with the sorption relation.

For CranGrass, every layer is below that per-layer message threshold, so initialization continues without a P-consistency warning.

During the first transport step, `Transorp`/`Transgen` evolves the instantaneous sorption pool according to the sorption relation. `Transgen` checks its own layer mass balance, but the check is conditional on an absolute difference larger than `1.0d-5 kg/m2` as well as a relative criterion. This absolute floor equals `0.1 kg/ha` per layer.

The largest first-step layer mismatch observed in CranGrass is `0.09584577676 kg/ha`, so every layer remains below the local absolute warning floor even though the profile-total mismatch is much larger.

## Quantitative attribution

A diagnostic `Inicalc_P` trace was generated from an execution-only copy of the source. For every soil layer, the supplied `Amcxfa` value was compared with the value returned by the source's own `Fast(...)` relation at the supplied initial `Copo`.

Integrated over the 22 layers, using the actual layer thicknesses, the initial fast-sorption inconsistency is:

`+0.7236806065523 kg/ha P`

A separate first-step `Transgen` trace decomposed each layer into:

- zero-order P source `Rekopo * St * He`;
- transport `Toou - Toin`;
- precipitated-P storage change;
- solution-P storage change;
- fast-sorption storage change;
- slow-sorption storage change.

Summed over the profile, the difference

`(transport + storage change) - Rekopo source`

is:

`+0.7235825146784 kg/ha P`

The corresponding source-computed `Outbal_calc` residual is:

`-0.7235825146799 kg/ha P`

The magnitudes agree to approximately `1.5e-12 kg/ha`, with opposite sign as expected from the two residual conventions.

The initial fast-sorption inconsistency differs from the first-step `Transgen` profile mismatch by only about `9.81e-05 kg/ha`; the small remainder is associated with the actual first-step solution/slow-sorption/transport evolution.

## Causal input-only control

To test causality without changing source code, a temporary copy of CranGrass was made in which only the 22 supplied fast-sorption initial values were replaced by the exact `Fast(...)` values computed by the same revision-53 source. The original testcase remains unchanged.

Results:

- original first-step `Bapp(Ddev)`: `-0.7235825146799 kg/ha P`;
- consistency-control first-step `Bapp(Ddev)`: `+9.808290724322e-05 kg/ha P`;
- reduction in absolute first-step residual: `99.9864%`;
- residual integrated fast-sorption initialization inconsistency in the control: approximately `1.12e-10 kg/ha P`.

This establishes causal evidence that essentially the entire large first-step PO4 deviation is an initialization-state consistency effect.

## Classification

Current PREP01 classification:

`INITIAL_STATE_CONSISTENCY_AND_MASS_LEDGER_SEAM`

This is not yet classified as a legacy scientific defect. Three possible interpretations remain distinguishable:

1. the supplied CranGrass initial sorption values are intentionally rounded legacy input and the first-step residual is an accepted initialization adjustment;
2. the legacy initialization consistency threshold is too loose for a profile-integrated conservation invariant;
3. the model should book the instantaneous first-step sorption projection as an explicit initialization adjustment in its mass ledger rather than allowing it to appear as unexplained balance residual.

A qualified historical executable and 4.x theory/change evidence are still required before choosing among those interpretations for the corrected legacy baseline.

## ANIMO5 implication

ANIMO5 must not hide this seam behind per-layer tolerances. For coupled state variables such as solution concentration and equilibrium sorption storage, initialization should use one explicit contract:

- derive dependent stores from an authoritative independent state; or
- accept externally supplied coupled stores but validate them against a profile-aware conservation tolerance; or
- preserve the supplied state and book any projection/reconciliation amount explicitly as an initialization mass-ledger term.

Whichever policy is chosen must be qualified against the historical reference. Silently changing legacy initial state is not admitted by PREP01.

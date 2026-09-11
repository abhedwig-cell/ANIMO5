# TCD-037-A4 Tier-A atomic admission decision

## Decision surface

This workunit evaluates one canonical child atom only: `TCD-037-A4`, the N2O atmosphere-emission observer accounting seam in `Outbal_calc`.

The source-owned accepted-timestep quantity is `(QEmN2ODif + QEmN2OFlw) * St`. The bounded reporting identity is:

`Delta Bani(N2Oe) = 10000 * (QEmN2ODif + QEmN2OFlw) * St`.

The only admitted expected-difference surface is `Bani(N2Oe)`. Physical state, process fluxes, restart/checkpoint state, solver and numerical policy, `Banh(N2On)`, `Bani(N2Od)`, `QRdN2O`, sibling atoms, TCD-032 through TCD-036 and unrelated observer fields remain outside the difference surface.

## Evidence disposition

B3A09 qualified the retained GOV04 Tier-A waiver predicate on an exact final green head. SYNQ05 supplies B1 synthetic causal and scope evidence including a source-owner discriminator, signed uptake control, component permutation, rate-time-equivalent control and inactive control. RUNTIMEQ03 pins the physical/accounting owner. B3I07 pins A4 as `A_ACCOUNTING_REPORTING_ONLY` and preserves the historical route naming `ANIMO-B3A08`; that historical identifier is not rewritten here.

GOV05 `GOV04_VERIFY_AND_REUSE` is applied to the immutable evidence. Pin identity, scope compatibility, immutable provenance, absence of superseding or contradictory evidence, and no evidence-strength promotion are all required. No separate Tier-A review is performed or claimed.

No qualified B2 executable reference exists. Therefore historical revision-53 behaviour remains `UNKNOWN`. Admission is scientific/accounting admission with historical uncertainty, not a historical-fidelity claim.

## Admission

Subject to exact-head validation of this package, admit `TCD-037-A4` only as `ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY` under the retained GOV05/GOV04 Tier-A waiver.

This does not admit parent `TCD-037`, does not re-admit A1 through A3, does not compose siblings, does not modify production source, and does not open B4. Once A4 is exact-final green, the child set must be reconciled live and parent handling must remain a separate explicit decision surface.
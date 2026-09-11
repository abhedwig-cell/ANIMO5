# TCD-037-A4 Tier-A readiness

## Claim boundary

TCD-037-A4 is restricted to N2O exchange with the atmosphere as an accounting observer. The accepted timestep amount is `(QEmN2ODif+QEmN2OFlw)*St`. At the existing balance conversion factor `Z=10000`, the bounded observer increment is `10000*(QEmN2ODif+QEmN2OFlw)*St` into `Bani(N2Oe)`.

This does not redefine denitrification or nitrification production accounting, the N2O reduction sink, any physical state, process flux, restart state, solver behavior or numerical policy.

## Why the ownership claim is discriminating

The frozen source contains two different concepts that must not be conflated: N2O production totals and N2O atmosphere-emission fluxes. SYNQ05 tested both hypotheses directly. When atmosphere emission was nonzero and production was zero, the accepted A4 observer changed while the production-total emulation did not. With production nonzero and atmosphere emission zero, the accepted A4 observer remained unchanged while the production-total emulation changed. This makes the evidence causal rather than merely correlational.

The component-permutation and rate-time controls preserve the accepted emission amount exactly. The signed-uptake case confirms that the observer follows the signed atmosphere exchange. The inactive case protects branch non-interference. O0 and O2 outputs are required to be byte-identical for the chosen dyadic values.

## Evidence limit

SYNQ05 is B1 synthetic evidence. It is not B2 and does not establish what a qualified historical executable did. The natural active-GHG testcase remains blocked by the source-testcase lineage mismatch. Historical behavior therefore remains `UNKNOWN` under GOV03.

## Tier-A readiness

The canonical atom is already classified `A_ACCOUNTING_REPORTING_ONLY`. With the exact source/accounting owner, predeclared single-observer difference surface, exact accounting identity, correction-specific synthetic activation, non-interference controls and explicit historical uncertainty, all retained GOV04 Tier-A readiness predicates are satisfied at this claim scope under GOV05. This workunit still does not grant the final waiver and does not admit A4. Those are decisions for a later atomic admission workunit after a fresh live authority and identifier check.

## Identifier reconciliation

B3I07's historical handoff named `ANIMO-B3A08` for A4. That label cannot now be used because B3A08 was subsequently allocated to the TCD-025 macropore main-ledger readiness workunit. Rewriting B3I07 would damage provenance. A live check found B3A09 free, so A4 readiness proceeds here as B3A09 while retaining the canonical identity `TCD-037-A4` unchanged.

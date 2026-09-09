# B3 Composition Rules

Work unit: `ANIMO-B3Q01`

Individually qualified B3 items do not compose automatically.

A combined B3 candidate is a new qualification object with its own evidence and decision.

## Composition preconditions

A composition candidate may be evaluated only when every component has:

- an explicit B3 disposition record;
- an atomic qualification scope;
- an admitted component state where admission is required;
- exact source, patch and evidence identities;
- declared expected changed and unchanged surfaces;
- residual uncertainty recorded.

If one required component is not admitted, the composition is not admitted.

Class F evolution is not composable into the preservation baseline under this framework. Class E items remain unavailable for composition until their separate numerical qualification is complete.

## Required composition checks

Every composition must demonstrate all of the following.

### No contradictory assumptions

The components must not rely on incompatible definitions of:

- conserved state;
- control volume;
- process ordering;
- initialization or restart semantics;
- species identity;
- numerical precision or convergence policy;
- authoritative theory.

Any contradiction blocks composition until resolved explicitly.

### No double correction

Two components must not correct the same physical or reporting term twice.

The composition record must map every changed expression, state, flux, ledger entry and interface field to exactly one correction owner unless a shared change is explicitly justified.

A parent TCD and one of its atomized child corrections may not both be applied as separate corrections.

### No cancellation masking

A small combined residual is not evidence that the composition is correct.

Qualification must retain the individual component deltas and evaluate the combined deltas. Opposite-sign errors are not allowed to cancel silently.

For every conserved quantity, report at least:

- baseline residual;
- each component residual or local identity result;
- combined residual;
- expected combined state and flux deltas.

If only the final residual is checked, the composition fails closed.

### Expected combined differences

The composition record must declare before evaluation:

- expected changed states;
- expected changed process fluxes;
- expected changed ledgers and reports;
- expected unchanged surfaces;
- any interaction term that means the combined difference is not the arithmetic sum of component differences.

Unexpected changes block admission until causally explained and requalified.

### Conservation

All applicable conservation identities must be rerun on the combined candidate.

Passing conservation in each component separately is insufficient because components may share state, control volumes or process ordering.

### Non-interference

Non-interference must be rerun for the combined candidate.

For Class A compositions this includes proof that physical state and process flux trajectories remain unchanged after all ledger-only corrections are applied together.

For Class B, C or E compositions, unaffected process domains must be compared explicitly. A combined correction is not allowed to widen scope silently.

### Coverage

Composition coverage must activate:

- each component path individually;
- relevant overlapping paths together;
- boundary conditions where one component changes inputs seen by another;
- restart or initialization paths when either component touches state ownership.

Synthetic cases remain coverage evidence, not historical B2 evidence.

## Ordering and interaction rules

If correction order can affect the result, order is part of the scientific contract and must be qualified.

A composition may be treated as order-independent only when this is demonstrated mathematically or by an exhaustive applicable ordering test.

When one component changes state or flux values consumed by another, an interaction test is mandatory even if the source edits are in different routines.

A representation-only Class D change may wrap an admitted correction only after equivalence to the already composed B3 target is demonstrated.

## Uncertainty propagation

A composition inherits the strictest unresolved uncertainty of its components.

In particular:

- a component admitted through `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` makes the composition historically uncertain;
- a Class D representation change cannot remove that uncertainty;
- a B2-backed component cannot upgrade a different non-B2 component to historical certainty;
- unknown path prevalence remains unknown after composition.

The composition record must list inherited uncertainty item by item.

## Composition admission decision

A composition is admitted only when:

- all component records are admitted and immutable by identity;
- every composition gate is `PASS`;
- no component disposition requires a still-pending separate qualification;
- expected combined differences are observed or any deviation is independently requalified;
- conservation and non-interference checks pass;
- independent review approves the composition itself.

The composition must receive its own identifier and admission record. It may not reuse one component's record.

## Examples relevant to current ANIMO findings

TCD-019 and TCD-024 must remain separate until TCD-019 receives Class E numerical qualification and TCD-024 receives Class B qualification. The fact that a synthetic TCD-024 probe leaves residual drift attributable in part to TCD-019 does not authorize their combined correction.

TCD-017, TCD-026 and TCD-027 are provisionally Class A surfaces, but even if each later qualifies independently, their combined ledger candidate must still prove unchanged physical trajectories and no accumulator or balance-term overlap.

TCD-016 cannot be composed as a local transport correction until its missing-state problem receives a Class C theory-qualified state model. A small-flux workaround that conserves mass by generating an extreme concentration is not an admissible substitute.

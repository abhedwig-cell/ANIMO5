# ANIMO-STATEQ08 Runinu Execution Continuation Contract

## Question

Does revision-53 `Runinu` behave only as a step-local derived flux, or can its call-entry value affect a later detailed-hydrology interval and therefore require explicit continuation handling?

## Source finding

The answer is conditional but material.

`Runinu` is a scalar owned in the main ANIMO execution context and passed by reference into `Hydro_detailed` each timestep.

Revision-53 detailed hydrology has three runoff branches:

- `Ru<0`: assign `Runinu=-Ru`;
- near-zero `Ru`: assign `Rupr=Rurv=Ruso=0` but do not assign `Runinu`;
- remaining route: assign `Runinu=0` before runoff partition.

Therefore the near-zero detailed route consumes the call-entry `Runinu` value.

The aggregated hydrology routine does not have this behavior. Its nonnegative runoff branch explicitly sets `Runinu=0`.

## Scientific consequence

The carried value is observable. Downstream source uses `Runinu` in:

- upper-boundary water-balance algebra;
- `UBoundconc` Load1 through Load6;
- transport upper-boundary flow;
- water, DOM, N and P balance accumulation.

Omitting it at a split boundary can therefore alter a future trajectory.

## Classification

STATEQ08 classifies this as:

`EXECUTION_CONTINUATION_STATE`

for exact revision-53 detailed-mode reproduction.

It is not classified as conserved physical storage and is not admitted as canonical physical state.

This is analogous to other continuation-critical runtime coordinates: checkpoint relevance follows future-trajectory dependence, not whether the quantity is a mass store.

## First-call limitation

The frozen source does not explicitly initialize `Runinu` before the first `Hydro_detailed` call.

The historical project uses static local storage and one configuration explicitly requests saved-scalar zeroing, but that is not a uniform source-level initialization contract across all configurations.

STATEQ08 therefore does not claim an exact historical first-call value and does not create B2 evidence.

## Restart rule

For source-faithful detailed-mode execution, a checkpoint/restore boundary is exact only if one of the following is proven:

1. the next detailed hydrology call deterministically assigns `Runinu` before any use; or
2. the call-entry `Runinu` continuation is restored exactly.

A generic restart cannot assume condition 1.

## Model-evolution alternative

A future ANIMO5 design could choose the deterministic rule `Runinu=0` for the near-zero detailed branch. STATEQ08 does not authorize that rule.

Such a choice changes frozen-source semantics and requires a separately reviewed scientific/corrected-legacy disposition.

## Governance

The issue affects state, restart and runtime branching with scientific consequences. Under GOV04 it is Tier C.

Same-agent review is not independent. No canonical state admission or production migration occurs here.

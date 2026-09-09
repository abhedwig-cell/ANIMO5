# B2 requirement scope

Work unit: `ANIMO-GOV02`

B2 is not downgraded by this policy. This document determines when B2 is logically required by the claim being made and when a different independent scientific authority can answer a different claim.

## Claim-first decision rule

Before selecting evidence, write the atomic claim type.

| Claim type | B2 rule |
|---|---|
| `HISTORICAL_FIDELITY_CLAIM` | B2 mandatory. No historical-uncertainty route can turn scientific evidence into proof of historical behaviour. |
| `SCIENTIFIC_CORRECTION_CLAIM` | B2 strongly useful but not intrinsically mandatory if the strict historical-uncertainty route is eligible and the class-specific scientific burden is met. Historical status remains unknown. |
| `REPRESENTATION_EQUIVALENCE_CLAIM` | B2 mandatory when the reference is historical behaviour. For B3-to-B4 representation equivalence, the admitted B3 contract can be the reference, but all historical uncertainty is inherited. |
| `NUMERICAL_POLICY_CLAIM` | B2 can characterize historical numerical behaviour but is not a solver-correctness oracle. Scientific admission requires separate numerical authority. A historical-equivalence subclaim still requires B2. |
| `PHYSICS_MODEL_CLAIM` | B2 is not scientific authority for new physics. Historical characterization may use B2. Physics/model admission uses separate scientific governance. |

## What qualifies as B2-required historical use

B2 is mandatory when any acceptance sentence states or implies one of the following:

- the new or corrected implementation preserves the relevant historical result;
- a GNU/runtime/compiler semantic is equivalent to the historical Intel semantic;
- a historical output file is the expected acceptance surface;
- a regression is described as historical rather than merely internal-to-B1;
- historical process ordering, runtime state or rounding behaviour is asserted from execution rather than only reconstructed from source.

A B1 GNU run cannot satisfy these requirements, even if it is reproducible. A source reconstruction such as TS01 can establish revision-53 source semantics but cannot by itself establish the runtime behaviour of an unavailable historical Intel environment.

## Scientific-oracle role by B3 class

Legend:

- `R`: normally required for a no-B2 scientific route when applicable to the class.
- `S`: acceptable supporting evidence but not universally required.
- `I`: insufficient on its own.
- `N/A`: not the governing authority for this class.

| Class | Analytical | Conservation | Metamorphic | Independent numerical | High precision | Theory-derived | No-B2 minimum interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| A accounting/reporting | S | R | S | I | I | S | Closed identity plus independent physical state/flux non-interference, B1 causality, path coverage and second-line review. |
| B local algebra/index/species | R or theory-R | S | S | S | S | R or analytical-R | Unambiguous local mathematical/species authority plus independent cross-check, at least two causal/oracle forms where feasible, and strong path coverage. |
| C missing physical state | I | S | S | S | I | R | Theory/state authority must define the missing state, ownership, units, initialization, restart, phase transfer and conservation. Mass closure alone is invalid. |
| D representation only | S | S | R | S | S | S | Reference must be an admitted B3 representation/process contract for B3-to-B4 equivalence. Historical representation equivalence remains B2-mandatory. |
| E numerical policy | S | S | S | R | R | R or formulation-equivalent authority | Separate numerical qualification: formulation, convergence, precision/discretization, fallback semantics and independent numerical review. Smaller residual alone is invalid. |
| F physics/model evolution | S | S | S | S | S | R | Separate physics/model governance and empirical validation where applicable. Not a legacy-correction admission merely because synthetic or B2 evidence agrees. |

`R or theory-R` means the route must contain at least one primary normative authority of the stated family and an independent cross-check. It is not permission to use two implementations derived from the same assumption as independent oracles.

## Class A

A Class A change is reporting/accounting-only. It can be unusually well bounded because the physical state and flux trajectory must be identical while a closed accounting identity supplies an independent expected result.

Without B2, admissibility still requires documented B2 acquisition closure, B1 causality, path activation, exact physical non-interference on the qualified observation surface, the closed identity, changed-output whitelisting where applicable, independent cross-check and second-line review.

Synthetic or analytical evidence is supporting evidence. It cannot replace physical non-interference or the acquisition gate.

## Class B

A Class B correction targets a local algebra, index, species or mapping error. Without B2, the target expression or mapping must be unambiguous from authoritative source/theory/mathematics. The corrected result must be tested through independent causal formulations and sufficient natural or synthetic path coverage.

One synthetic example that happens to give the expected number is not enough.

## Class C

Class C introduces or repairs missing physical state. Historical evidence may show what an old program did, but it does not define what scientifically complete state must exist.

No-B2 admission therefore requires independent state-model authority. At minimum the state definition, phase ownership, units, initialization, restart semantics, transfers and conservation role must be specified and cross-checked. Conservation closure can detect a gap but cannot by itself define the missing state.

## Class D

Representation-only modernization has two distinct possible claims.

1. `historical representation equivalence`: B2 mandatory.
2. `admitted B3-to-B4 representation equivalence`: B2 is not intrinsically required because the admitted B3 process contract is the reference, but historical uncertainty attached to that B3 contract must propagate unchanged.

A Class D migration cannot silently convert `historical_behaviour_status=UNKNOWN` into a historical-equivalence claim.

## Class E

Numerical-policy claims require their own numerical evidence. B2 can tell us how the historical implementation behaved on a path. It cannot tell us that a nonlinear solver, stopping rule or fallback policy is mathematically correct.

Without B2, a narrow Class E scientific admission can only be considered after the general historical-uncertainty gate and after independent numerical qualification of formulation, convergence, precision/discretization sensitivity, relevant fallback/branch semantics and independent numerical review. Improvement of one balance residual is evidence of effect, not proof of solver correctness.

The current NQ02 state exemplifies this distinction: it contains strong causal and high-precision evidence for parts of TCD-019 but still leaves fallback policy, tolerances, historical B2 equivalence and independent numerical review unresolved. GOV02 does not change that disposition.

## Class F

Class F changes physics or the model itself. B2 is not an oracle for new physics. B2 may still characterize how the legacy system behaved, but scientific model evolution requires theory, independent scientific evidence and empirical validation where applicable.

Class F is therefore outside the historical-uncertainty route as a legacy-correction shortcut. It requires explicit physics/model governance.

## Evidence that is always insufficient on its own

The following never independently satisfy a no-B2 scientific admission:

- a synthetic test result merely matching the implementation under test;
- a B1 GNU output treated as historical expected behaviour;
- a smaller residual or better apparent mass balance;
- one conservation closure for a Class C missing-state decision;
- source comments without independent theory or mathematical support when the claim is scientific;
- unreviewed stopping of PREP02R acquisition;
- a representation comparison against an unadmitted candidate;
- historical agreement used as proof of scientific correctness.

# ANIMO-NQ05 — TCD-019 Restricted Exact-Storage / No-Legacy-Fallback Numerical Policy Qualification

Status: `AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW`

## Purpose and scope

This workunit revisits canonical `TCD-019` under the current GOV05 assurance model and the post-NQ02 authority state. It deliberately does **not** attempt to qualify the complete historical nonlinear phosphorus solver. Instead it defines a bounded numerical-policy envelope in which the known constitutive conservation defect can be corrected without inventing a tolerance and without accepting the distinct, unqualified legacy fallback equation.

Base authority: `ANIMO-B3D41@3ac98899dd4e6b7a5133cbecd758fab0b81e945d`.

Primary historical numerical evidence: `ANIMO-NQ02@40a41089020f78ee1d5181b8afc7bdb511af3193`.

Cross-cutting `Iflsol=4` coefficient semantics are no longer an unresolved local NQ02 candidate: the cancellation-safe binary64 policy is separately qualified/admitted by `ANIMO-NQ04@bfd736b88b6fc4f2a66970b812172729c1923562` and `ANIMO-B3D36@b74ec4461ab4d7b62ecfaf175e1eeeec8c58f7b2`.

Historical B2 remains unavailable; historical behaviour is therefore `UNKNOWN_WITHOUT_B2` under GOV03.

## What NQ02 already establishes

NQ02 source reconstruction and controlled runs establish all of the following:

1. the legacy fast-Langmuir small-delta tangent is not the finite conserved storage change;
2. the threshold-free cancellation-safe Langmuir secant removes the constitutive storage bias down to binary64 rounding scale;
3. the supplied natural fast-Langmuir cases show a stable pre-fallback convergence region when exact storage is used;
4. the legacy fallback is **not** merely the scalar form of the original two-variable Newton equations: it imposes `Rsc=2*Avc-Con` and can use slow-sorption `Recfso` inherited from unsuccessful Newton history;
5. tightening either the Newton or fallback threshold does not provide a monotone scientific correctness argument;
6. fast-Freundlich exact-storage mechanics have strong synthetic support but no supplied natural/B2 case, so NQ05 does not broaden the restricted policy to fast Freundlich.

The safe consequence is not to choose a new `Small` or fallback tolerance. It is to admit a narrower equation-and-acceptance contract and fail closed outside it.

## Restricted constitutive domain

NQ05 qualifies instantaneous **fast Langmuir** sorption only (`Optcxfa=2`). Slow sorption may be linear or Freundlich (`Optcxsl in {1,3}`); slow Langmuir remains outside this workunit so TCD-024 is not silently composed into TCD-019.

The start fast-sorption store must be constitutively consistent with the accepted start concentration. Any material off-relation start state remains a TCD-014 initialization concern and is outside the NQ05 envelope.

For one fast Langmuir site define

`S(C) = a*C/(1+b*C)`

with `a>=0`, `b>=0`, `C0>=0`, `C>=0` and finite positive denominators. For `C != C0`, the finite storage coefficient is represented by the algebraically exact cancellation-safe form

`D(C,C0) = a / ((1+b*C)*(1+b*C0))`.

At `C=C0`, the same expression is the analytic limit. No `|C-C0|` evaluation switch exists in this policy. For multiple fast Langmuir sites, coefficients and derivatives are summed site-wise.

The derivative used by the nonlinear equation is

`dD/dC = -a*b / ((1+b*C)^2*(1+b*C0))`.

If an intermediate or denominator is non-finite, the state is outside the qualified domain and must fail closed.

## Nonlinear equation identity

The target equations remain the reconstructed `C_unl` two-variable equations for end concentration `Rsc` and step-average concentration `Avc`, evaluated with the accepted exact-storage representation.

Slow-sorption adsorption/desorption rate selection is **state-local**: `Recfso` must be recomputed from the current trial `Avc` and the current slow-store state each time the equation/Jacobian is evaluated. It may not be inherited from an unsuccessful historical Newton path into a different fallback equation.

Where the analytical coefficient path selects `Iflsol=4`, the already-qualified NQ04/B3D36 cancellation-safe `Detcoef/Coefdc` policy is a required dependency. NQ05 does not modify that policy.

## Tolerance-free acceptance contract

NQ05 does not select `Small=1e-7`, `1e-8`, or any other production tolerance. A candidate `(Rsc,Avc)` is accepted only when all of the following hold in the selected binary64 arithmetic contract:

1. `Rsc>=0` and `Avc>=0` and all equation/Jacobian quantities are finite;
2. the current state-local slow-sorption branch is recomputed before the final equation/Jacobian evaluation;
3. the 2x2 Jacobian determinant is finite and non-zero;
4. the Newton correction `(dR,dA)` computed from that final equation/Jacobian is finite;
5. applying that correction produces **no representable state change**: `fl(Rsc-dR)==Rsc` and `fl(Avc-dA)==Avc`;
6. the accepted residual L1 value is no greater than the residual L1 at each finite, non-negative immediate binary64 neighbour of `(Rsc,Avc)` that remains in the same state-local slow-sorption branch.

Conditions 5–6 define a representation-stable discrete binary64 root neighbourhood. They are exact predicates, not tolerances. A production implementation may use Newton, damping, trust-region or another method to find such a state, but the acceptance contract is invariant to that search method.

## Legacy fallback exclusion

The legacy midpoint/bisection fallback is not part of the qualified policy. If a representation-stable state satisfying the contract is not obtained, the restricted TCD-019 route must fail closed rather than accept the historical fallback's distinct equation.

This is an explicit scope restriction, not a claim that fallback-triggering states are unphysical. NQ02 demonstrates that such states occur naturally in supplied P-active cases. They remain outside the restricted NQ05 admission envelope pending a separately qualified joint nonlinear/fallback policy.

Likewise, NQ05 does not promise that every timestep or supplied testcase lies inside the restricted envelope. It qualifies the scientific/numerical identity of accepted states, not universal model coverage.

## Evidence and controls

The permanent arithmetic oracle `tools/nq05/tcd019_restricted_policy_oracle.py` checks the cancellation-safe Langmuir secant against high-precision arithmetic across deterministic finite-domain cases and checks the exact representation-stable acceptance predicate on controlled systems. It introduces no model tolerance.

NQ02 natural evidence remains B1 diagnostic evidence for route reachability and convergence behaviour. It is not promoted to B2. The absence of a natural fast-Freundlich case is handled by scope exclusion, not by synthetic promotion.

Adversarial controls include:

- replacing the exact secant with the legacy tangent must fail finite-storage identity for finite `Delta C`;
- accepting a one-ulp-displaceable candidate must fail the representation-stability predicate;
- enabling legacy midpoint fallback must violate the bounded policy;
- using inherited rather than state-local `Recfso` in the final equation evaluation must violate the policy;
- admitting fast Freundlich or slow Langmuir must violate the scope boundary.

## Hard boundaries

No production source is modified. No `Small`, fallback threshold, residual tolerance or model-output tolerance is selected. Fast Freundlich, slow Langmuir/TCD-024, TCD-014 initialization inconsistency, fallback-triggering states, historical fidelity, B4 and production migration remain outside scope. This workunit performs no B3 admission; any restricted top-level TCD-019 admission is a separate workunit.

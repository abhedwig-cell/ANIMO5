# TRACE-ELEM-ANIMO-B02-003 reconciliation

Date closed: 2026-09-19
Prospective result: `NO_CONFIRMED_DISCREPANCY`
Candidate: `TRACE-ANIMO-0005`
Candidate disposition: `EXCLUDED`

## Element

TCD-019 restricted exact-storage / no-legacy-fallback numerical policy, selected before detailed inspection as the Batch-02 numerical-scientific convention.

## Bounded policy

NQ05 qualifies a deliberately restricted numerical identity for fast Langmuir sorption:

- exact cancellation-safe finite storage coefficient
  `D(C,C0)=a/((1+b*C)*(1+b*C0))`;
- no `|C-C0|` switch or selected `Small`;
- derivative
  `dD/dC=-a*b/((1+b*C)^2*(1+b*C0))`;
- reconstructed two-variable `C_unl` target equations;
- state-local recomputation of slow-sorption branch state;
- NQ04/B3D36 cancellation-safe coefficient dependency when `Iflsol=4`;
- exact binary64 representation-stability checks plus local neighbour residual ordering;
- fail closed when the contract is not satisfied;
- legacy midpoint fallback excluded.

Fast Freundlich, slow Langmuir/TCD-024, off-relation initialization/TCD-014, fallback-triggering-state coverage and production implementation remain outside scope.

## Prospective candidate and exclusion

TRACE-ANIMO-0005 was registered before reading freeze semantics because the reviewer document remained pending-review while NQ05 status and B3D42 showed qualification/admission.

Resolution found that the reviewer document is explicitly part of the immutable NQ05 authoring object. The NQ05 validator permits only review/status changes after the exact reviewed head, and the reviewer blob is unchanged between reviewed authoring and exact-final NQ05 authority.

B3D42 is a separate successor admission workunit with its own freeze/review/status chain.

The observed state difference is therefore intentional temporal provenance, not a current scientific contradiction.

## TRACE disposition

No confirmed discrepancy remains for this element.

The candidate trigger and exclusion mechanism remain part of the prospective record. No repair is appropriate.

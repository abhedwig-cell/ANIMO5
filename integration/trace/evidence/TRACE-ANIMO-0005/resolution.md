# TRACE-ANIMO-0005 resolution

Date: 2026-09-19
Outcome: `EXCLUDED`
Prospective candidate: yes
Confirmed discrepancy: no

## Frozen observation

The reviewer-facing NQ05 TCD-019 policy document remained labelled:

`AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW`

and stated that B3 admission was separate.

At the same current integration state:

- NQ05 machine status recorded a completed Tier-C review and qualified policy;
- B3D42 recorded the bounded TCD-019 numerical policy admitted at B3.

## Freeze-contract reconstruction

`ANIMO-NQ05_AUTHORING_FREEZE.json` explicitly defines a substantive authoring freeze before GOV05 Tier-C review.

The frozen substantive files include the reviewer policy document, machine policy, arithmetic oracle, validator and workflow. The freeze contract requires:

- exact green authoring head before review;
- any substantive change to reset review;
- only NQ05 internal-review and NQ05 status files may change after review;
- exact-final head CI before final authority.

The NQ05 validator enforces the same contract. Once the review exists it computes the diff from the reviewed head and requires all post-review changes to be limited to:

- `integration/animo-numerics/ANIMO-NQ05_INTERNAL_ADVERSARIAL_REVIEW.json`;
- `integration/animo-numerics/ANIMO-NQ05_STATUS.json`.

Direct comparison confirms the intended immutability:

- reviewed authoring head: `141cad58d03f963522a5631cb9e2e219dbc1ef0d`;
- exact-final NQ05 authority: `62080a8e731681407e2e7e759decc49c1a47fa7b`;
- reviewer document blob at both heads: `770b882398c9aeefc848751185ceb1ec0ccaca35`.

Only the review and status artifacts changed between those heads.

## Successor admission

NQ05 final status is the mutable post-review qualification authority and explicitly records:

- `CLOSED_QUALIFIED_SCIENTIFIC_POLICY`;
- `qualified=true`;
- B3 admission not performed in NQ05.

B3D42 separately consumes exact-final `ANIMO-NQ05@62080a8e731681407e2e7e759decc49c1a47fa7b` and admits the same bounded policy under historical uncertainty.

## Scientific consistency

The frozen authoring object and successor authorities agree on the restricted policy:

- fast Langmuir only;
- slow sorption limited to linear or Freundlich;
- cancellation-safe exact Langmuir storage secant;
- no small-delta switch;
- reconstructed two-variable nonlinear target;
- state-local slow-rate selection;
- binary64 representation-stable accepted-state predicate plus immediate-neighbour residual guard;
- no legacy fallback;
- fail closed outside the qualified domain;
- no selected `Small`, fallback tolerance or global numerical tolerance;
- historical behaviour remains `UNKNOWN_WITHOUT_B2`;
- no production implementation is authorized.

## Disposition

The apparent pending-versus-qualified/admitted mismatch is intentional temporal provenance under an explicit immutable authoring-review contract.

TRACE-ANIMO-0005 is excluded, not confirmed.

No repair is warranted. Rewriting the frozen NQ05 reviewer object after review would invalidate the reviewed scientific object unless Tier-C review were reset.

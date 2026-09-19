# TRACE-ANIMO-0004 resolution

Date: 2026-09-19
Outcome: `EXCLUDED`
Prospective candidate: yes
Confirmed discrepancy: no

## Frozen observation

At the pre-resolution state, the reviewer-facing GHG02 TCD-033 qualification document still carried the authoring-time status:

`CANDIDATE_SCIENTIFIC_POLICY_PENDING_EXACT_HEAD_REVIEW`

and stated that separate B3 admission remained required.

At the same current integration state, machine authorities recorded:

- GHG02 review completed;
- GHG02 scientific policy qualified and closed;
- B3D40 TCD-033 atomic B3 admission qualified/admitted.

## Freeze-contract reconstruction

`ANIMO-GHG02_AUTHORING_FREEZE.json` explicitly defines the GHG02 scientific object as substantive authoring that must be frozen before GOV05 Tier-C review.

The contract states:

- the review must pin the exact green authoring head;
- substantive change resets review;
- after review, only the internal-review and GHG02-status artifacts may change.

The GHG02 validator enforces that rule directly. Once the review artifact exists it computes the diff from the reviewed head and requires that every post-review change belongs to exactly:

- `integration/animo-ghg/ANIMO-GHG02_INTERNAL_ADVERSARIAL_REVIEW.json`;
- `integration/animo-ghg/ANIMO-GHG02_STATUS.json`.

The reviewer qualification document therefore cannot be rewritten from pending to qualified without invalidating the reviewed object.

Direct blob comparison confirms this intended immutability:

- authoring head `fb751d90af6563ec27c0dabea5bbc6d2f1966841`;
- exact-final GHG02 authority `28306877152972a9a8ba1a19e1c61fda56b658a0`;
- document blob at both heads: `3b89c05677c8647a16869a7a7c66c0aa5b2d96b4`.

The only files changed between those GHG02 heads are the review artifact and status object.

## Successor authority

GHG02 final status is the mutable post-review authority for qualification state. It explicitly records:

- `CLOSED_QUALIFIED_SCIENTIFIC_POLICY`;
- `qualified=true`;
- review completed;
- B3 admission not performed inside GHG02.

B3D40 then consumes exact-final `ANIMO-GHG02@28306877152972a9a8ba1a19e1c61fda56b658a0` and performs the separate TCD-033 B3 admission under its own authoring-freeze/review/status contract.

The document, GHG02 status and B3D40 status therefore represent successive layers, not competing current scientific authorities.

## Scientific consistency

Across the frozen authoring object and successor authorities, the bounded scientific identity remains:

- existing `A < 1.0e-8` early return gives zero parent/daughters;
- `S=0` gives zero parent/daughters;
- otherwise `Q_i = Q*S_i/S`;
- equivalently `Q_i = E*A*S_i`;
- `sum_i(Q_i)=Q`;
- source-share proportions are preserved.

Historical revision-53 behaviour remains `UNKNOWN_WITHOUT_B2`; no production implementation is authorized by these admission records.

## Disposition

The apparent status mismatch is intentional temporal provenance under an explicit immutable authoring-review contract.

TRACE-ANIMO-0004 is excluded, not confirmed.

No repair is warranted. Updating the frozen reviewer document after review would violate GHG02 qualification semantics unless the Tier-C review were reset.

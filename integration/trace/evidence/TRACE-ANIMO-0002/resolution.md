# TRACE-ANIMO-0002 resolution

Date: 2026-09-19
Outcome: `EXCLUDED`
Prospective candidate: yes
Confirmed discrepancy: no

## Frozen observation

At pre-resolution commit `42829a645dfdb1cf99e71ab0955795503e099230` the GHG03 scientific qualification document still stated:

`AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW`

while the current GHG03 status object recorded a completed review and qualified policy, and B3D41 recorded a candidate B3 admission.

## Freeze-contract reconstruction

`integration/animo-ghg/ANIMO-GHG03_AUTHORING_FREEZE.json` explicitly defines the qualification document, policy, oracle, validator and workflow as the **substantive authoring freeze before GOV05 Tier-C review**.

It also states:

- review must pin the exact green authoring head;
- any substantive change resets review;
- after review, the only allowed changes are the adversarial-review artifact and the GHG03 status object.

The GHG03 validator enforces this contract. Before a review artifact exists it requires the status to remain pending. Once the review artifact exists it requires that only review/status files changed after the frozen reviewed head and that the status moves to the qualified final state.

The current internal review records a same-agent adversarial review and explicitly disclaims genuine independence. The GHG03 status correspondingly records the qualified scientific policy and leaves B3 admission separate.

B3D41 then consumes the exact qualified GHG03 authority and performs the separate B3 admission decision, again with its own authoring freeze, review and status layer.

## Scientific consistency

The frozen qualification document, machine policy and later B3D41 workunit agree on the bounded carbon-transfer identity:

`G_j = Q_j*dt/(f_C*(1-a_j))`

`I_j = a_j*G_j`

`f_C*(G_j-I_j)=Q_j*dt`

with exactly one source debit owner, one matching internal credit when nonzero, and no duplicated DOM debit.

Current source-manifest hashes for `ghgasses.for`, `ghg_ch4.for`, `Rates.for` and `resp_miner.for` equal the hashes pinned by GHG03.

Historical active-GHG transfer behaviour remains explicitly `UNKNOWN_WITHOUT_B2`; production implementation is not admitted.

## Disposition

The apparent status mismatch is an intentional separation between immutable pre-review scientific authoring evidence and mutable post-review status evidence. These files serve different temporal roles by explicit contract.

TRACE-ANIMO-0002 is therefore excluded, not confirmed.

No repair is warranted. Changing the frozen qualification document after review would itself violate the qualification design unless the review were reset.

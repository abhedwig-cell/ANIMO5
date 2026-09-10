# ANIMO-RG05H — Post-RG05G Canonical Routing Refresh & TCD-038 Admission Integration

## Decision target

`QUALIFIED_EARLY_AGGREGATE_ROUTING_REFRESH_PLUS_ONE_POST_RG05G_ATOMIC_ADMISSION_NO_PRODUCTION`

ANIMO-RG05H is an early central-regie refresh over the immutable RG05G aggregate. It integrates one already-qualified post-RG05G atomic scientific admission and updates the central traceability snapshot to the qualified B3I07 canonical routing authority. It does not review, re-admit, compose, implement, or migrate any scientific correction.

Base aggregate authority:

`ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`

New atomic admission consumed without reinterpretation:

`ANIMO-B3D20@4f0a352bd354c971db0d972967296bf64505da5b — TCD-038`

Current canonical routing authority consumed without scientific reinterpretation:

`ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`

## Why an early aggregate is required

GOV04 normally batches 3 to 5 new atomic admissions. It also requires earlier central integration when a real project gate changes, explicitly including canonical routing, and permits earlier integration when this materially reduces ambiguity.

B3I07 changes canonical routing by atomizing parent TCD-037 into four governed child qualification targets. RG05G still names B3I06 as the latest observed routing authority. Leaving RG05G as the only current central snapshot would therefore make central routing state stale precisely when downstream Tier-A readiness is about to consume the new child boundaries.

The early-update trigger is therefore:

`CANONICAL_ROUTING_CHANGED_AND_CURRENT_CENTRAL_SNAPSHOT_WOULD_OTHERWISE_BE_MISLEADING`

This is not a claim that the normal three-admission threshold has been reached. It has not. The already-qualified TCD-038 admission is integrated opportunistically in the same central refresh because atomic admission authority is already final and exact-head CI is green.

## Admission-state update

RG05G records ten atomic B3 scientific admissions, all with historical uncertainty. B3D20 subsequently admitted TCD-038 under GOV04 Tier C with historical behaviour still `UNKNOWN_WITHOUT_B2`.

RG05H therefore records eleven atomic scientific admissions:

`TCD-017, TCD-018, TCD-024, TCD-026, TCD-015, TCD-027, TCD-041, TCD-030, TCD-023, TCD-028, TCD-038`.

No admission is re-evaluated here. B3D20 remains the scientific authority for TCD-038. RG05H is only the aggregate traceability authority after incorporation.

## Canonical routing update

B3I07 is now the latest canonical routing authority consumed by central regie.

Its TCD-037 decision is retained exactly at routing scope:

- parent `TCD-037` remains a registered top-level discrepancy and is not itself an atomic admission target;
- canonical child qualification keys are `TCD-037-A1`, `TCD-037-A2`, `TCD-037-A3`, and `TCD-037-A4`;
- all four are Class-A accounting/reporting-only candidates;
- all four remain `TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE`;
- no child is admitted;
- no Tier-A review waiver is granted;
- no new top-level TCD is allocated;
- the top-level canonical register tail remains `TCD-042`;
- `TCD-043` remains unreserved by this route.

The four downstream readiness lanes remain separate:

- `TCD-037-A1 -> ANIMO-B3A05`;
- `TCD-037-A2 -> ANIMO-B3A06`;
- `TCD-037-A3 -> ANIMO-B3A07`;
- `TCD-037-A4 -> ANIMO-B3A08`.

A PASS in one lane cannot admit or waive any sibling or the parent.

## Evidence boundaries retained

For TCD-037 child readiness, the RUNTIMEQ03 evidence limitations remain authoritative through B3I07:

- natural active-GHG revision-53 execution is blocked by source/testcase lineage mismatch;
- the synthetic semantic discriminator is B1 only and is not independent B2;
- historical Intel/revision-53 behaviour remains `UNKNOWN`;
- physical-state, process-flux, restart-state and solver/numerical-policy expected differences are all none at the qualified observer-only direction;
- correction-specific identity, activation and waiver gates still have to be demonstrated separately per child.

For TCD-038, B3D20's historical uncertainty is retained exactly. No B2 is fabricated by aggregation.

## Project state after RG05H

- atomic B3 scientific admission count: 11;
- historical-uncertainty admission count: 11;
- normal B2 admission count: 0;
- current central canonical routing authority: B3I07;
- TCD-037 parent: atomized into A1/A2/A3/A4, no admission;
- TCD-038: admitted atomically with historical uncertainty;
- B3: incomplete;
- B4: closed;
- production migration: closed.

RG05H does not recompute a global canonical queue cardinality. Later routing/readiness work is distributed, and a simplistic subtraction from an older queue snapshot would be misleading.

## Hard boundaries

RG05H does not modify production source, frozen B0, the top-level TCD register, any scientific evidence, any review result or any correction candidate. It performs no scientific re-admission, no composition, no B4 authorization and no production migration. It does not turn a Tier-A candidate into a Tier-A waiver and does not turn historical uncertainty into historical fidelity.

## Next valid route

After exact-final-head validation, downstream TCD-037 work may consume RG05H as the current central snapshot and B3I07 as the atomic routing authority. The first recommended child lane is:

`ANIMO-B3A05 — TCD-037-A1 CH4 Layer Formation Observer Tier-A Readiness`.

That workunit must recheck all GOV04 Tier-A waiver predicates. Because the natural active-GHG case is unavailable and the existing synthetic B1 was produced in the prior qualification context, no waiver may be assumed at entry. If independent activation evidence cannot be obtained under the permitted evidence model, the workunit must fail closed rather than self-approve the missing gate.

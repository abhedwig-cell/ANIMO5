# ANIMO-RG05F First GOV04 Batched Atomic B3 Admission Integration

Work unit: `ANIMO-RG05F`

Branch: `work/animo-rg05f-first-gov04-batched-admission-integration`

Authoring base and prior aggregate authority: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`

Governance authority: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`

This is a governance-only central-regie aggregation. It integrates the two authoritative atomic B3 admissions that existed after RG05E at the live start of this workunit:

- `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4`, TCD-027, GOV04 Tier A waiver admission;
- `ANIMO-B3D14@d672992bbc32d40d7e0fbdf03f3fa9bc4cd5a522`, TCD-041, GOV04 Tier B admission after one genuinely independent second-line review.

No later `ANIMO-B3D*` admission and no `ANIMO-RG05F` branch existed at the live pre-write check.

## Why aggregate now

GOV04 defines a normal central-regie batch cadence of 3 to 5 new atomic admissions, but explicitly allows an earlier aggregate update when it materially reduces ambiguity. This workunit uses that early-update allowance. The normal threshold has not been reached: exactly two post-RG05E atomic admissions are integrated here.

The early update is justified because RG05E still reports five admissions while two later atomic admission authorities are already independently qualified under different GOV04 review tiers. Keeping both outside the aggregate while continuing parallel B3 work would make the phrase "current central regie" materially less informative. RG05F therefore reconciles the aggregate reporting layer without changing either scientific decision.

## Integrated atomic authorities

### TCD-027

TCD-027 is the detailed organic-P `redis_EXP` reporting accumulator correction. Its admission authority is `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4`.

It is risk Tier A and uses the qualified GOV04 Tier-A independent-review waiver. Historical revision-53 behaviour remains `UNKNOWN`. The admission is reporting-only and authorizes no physical-state change, process-flux change, composition, B4 step or production migration.

### TCD-041

TCD-041 defines the lower external GHG advective air-boundary coordinate `Flair(Nl+1)` as the source-implied closed-boundary value zero before its same-call first use. Its admission authority is `ANIMO-B3D14@d672992bbc32d40d7e0fbdf03f3fa9bc4cd5a522`.

It is risk Tier B. The required independent review is `ANIMO-B3B07R@3587c7a94a992f3779034c4c1e5f4134192d54f3` with outcome `PASS_TIER_B_READY_FOR_POST_REVIEW_DISPOSITION`. Historical revision-53 behaviour remains `UNKNOWN_WITHOUT_B2`. TCD-041 is not composed with TCD-032 through TCD-037 and changes no restart, checkpoint, solver or numerical-policy semantics.

## Aggregate result

RG05E contained five atomic B3 admissions: TCD-017, TCD-018, TCD-024, TCD-026 and TCD-015. RG05F adds exactly TCD-027 and TCD-041, producing seven authoritative atomic B3 admissions in the aggregate snapshot.

B3 remains incomplete. B4 remains closed. Production migration remains closed. Historical uncertainty is preserved for all seven admissions. The canonical TCD register is not modified by this workunit.

## Queue delta

Relative to RG05E:

- TCD-027 leaves `WAITING_ON_ROUTE_AND_REVIEW` and becomes `ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY`;
- TCD-041 leaves `READY_FOR_ADMISSION_READINESS` and becomes `ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY`.

The aggregate active queue therefore decreases from 20 to 18 entries. `WAITING_ON_ROUTE_AND_REVIEW` decreases from 2 to 1 and `READY_FOR_ADMISSION_READINESS` decreases from 4 to 3. All other queue-state counts are unchanged.

## Authority boundary

RG05F integrates only the two exact admission records named above. Branch recency does not promote any other readiness, review, remediation, disposition or admission workunit. No TCD is composed or reclassified by this aggregate.

Future atomic admissions remain authoritative from their own qualified records until a later central aggregate incorporates them. A later aggregate should normally wait for the GOV04 cadence of 3 to 5 new post-RG05F admissions unless a real project-gate change or another explicit ambiguity-reduction trigger justifies earlier integration.

## Hard boundary

This workunit changes no production source, no frozen source or testcase, no canonical TCD register, no B4 object and no production-migration authority. It creates no new scientific admission and reopens no completed review. It only records the already-qualified TCD-027 and TCD-041 atomic admissions in the central aggregate snapshot.

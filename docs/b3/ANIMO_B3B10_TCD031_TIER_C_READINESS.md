# ANIMO-B3B10 TCD-031 Tier-C admission readiness

Work unit: `ANIMO-B3B10`

Target: `TCD-031`

Branch: `work/animo-b3b10-tcd031-macropore-restart-state-readiness`

Authoring base: `ANIMO-STATEQ04@ef9a5998cafae433deeba701a8e9a8a08eacc92f`

Status: `QUALIFIED_CLASS_C_ADMISSION_READINESS_GOV04_TIER_C_REVIEW_HANDOFF_PENDING_MACHINE_GATE`

## 1. Decision

TCD-031 is ready to enter one separate GOV04 Tier-C independent second-line review, but it is not B3-admitted and no production implementation is authorized.

The atomic correction identity is a complete accepted-state transfer across a restart boundary for active macropore solutes. The correction has two inseparable transaction halves:

1. project all enabled accepted macropore solute concentrations into the checkpoint;
2. restore those accepted concentrations and establish the runtime result alias from the restored owner before ordinary accepted-to-result lifecycle promotion can overwrite it.

These are not two independent scientific mechanisms. A writer without a valid restore transaction remains incomplete; a restore transaction without the complete checkpoint coordinates remains incomplete.

## 2. Authority pins

- aggregate central regie: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`;
- GOV04: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- GOV03: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3 qualification framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- MP02: `6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- STATEQ01: `4adae99576eb56978da71f7c8a250e4445fd3bc4`;
- STATEQ02: `cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`;
- STATEQ03: `10c50e65d1369d5f3b26736c4b12d3a482379eb5`;
- STATEQ04: `ef9a5998cafae433deeba701a8e9a8a08eacc92f`;
- MASSQ02: `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`;
- latest checked canonical routing: `ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`.

No later B3B10 or TCD-031 readiness branch was found before creation.

## 3. Risk classification

B3 qualification class: `C_MISSING_OR_INCOMPLETE_STATE_RESTART_MODEL`.

GOV04 risk tier: `C`.

Tier C is forced by state ownership, restart serialization, restore direction and checkpoint lifecycle semantics. The small source-edit footprint of a possible future implementation is irrelevant to this risk classification.

Historical revision-53 behaviour without a trusted active B2 restart reference remains `UNKNOWN`. GOV03 historical-uncertainty rules therefore remain active and may not be replaced by synthetic agreement.

## 4. Persistent state contract

For each active macropore domain the accepted owner coordinates are:

- DOM: `CoMpDiorMa`;
- DON: `CoMpDiorNi`;
- NH4-N: `CoMpNh`;
- NO3-N: `CoMpNi`;
- DOP-P when P is active: `CoMpDiorPo`;
- PO4-P when P is active: `CoMpPo`.

There are two macropore domains. The complete persistent inventory is therefore 8 scalars with P disabled and 12 scalars with P enabled.

The corresponding `RsCoMp*` values are result aliases of the same physical owner, not second independent checkpoint coordinates. At restore the accepted owner is loaded first and the result alias may then be initialized from that accepted owner under the qualified restore transaction.

Current-interval arrays such as `AvCoMp*`, `AvCoML*` and `MpReKo*` remain workspace and are not serialized as accepted physical state.

Macropore water storage and geometry remain externally hydrology-owned and require an exact compatible accepted-frame binding.

## 5. Evidence chain

STATEQ03 established fail-closed that native revision 53 is incomplete in two independent implementation locations belonging to the same restart transaction:

- `Output_Init` serializes none of the required macropore solute records;
- the first resumed lifecycle can copy an unrestored `RsCoMp*` alias over a freshly loaded `CoMp*` accepted coordinate.

STATEQ04 then qualified a correction contract without modifying production source. Against the frozen `MAPOTRANSPORT` kernel it exercised all six solute families separately. A split after accepted step 5 followed by a fresh-process restore produced exact bytewise equality for five continuation steps for every species when the complete owner and alias-bootstrap contract was used.

Two causal negative controls also passed as discriminators:

- retaining the native bad alias condition caused divergence for every species;
- dropping either macropore domain from the checkpoint caused divergence for every species.

No numerical tolerance was introduced.

MP02 independently supplies complete-model synthetic active-macropore reachability for the six enabled solute paths over complete ANIMO orchestration. It does not supply a historical B2 oracle and does not itself supply the split-run proof.

The frozen B0 testbank contains no naturally active macropore case. This limitation remains explicit.

## 6. Readiness gates

The following admission-readiness gates are satisfied for independent review:

- atomic state/restart correction identity is bounded;
- persistent state owner and dimensionality are explicit;
- result alias is distinguished from independent owner state;
- deterministic reconstruction is rejected for nonzero stored macropore solute mass;
- input, serialization and restore directions are traced;
- all six species share the qualified state transaction and were individually discriminated;
- both domains are required by executable negative controls;
- comparison policy is exact, with no invented tolerance;
- frozen source and frozen testbank remain unchanged;
- no production patch or canonical STATE admission is present.

The following are not claimed as already satisfied:

- historical active B2 reference behaviour;
- whole-model active-macropore split equivalence for a production checkpoint implementation;
- production serializer implementation;
- production restore implementation;
- canonical STATE admission;
- TCD-025 ledger correction or composition.

These limits do not prevent an independent reviewer from deciding the narrower atomic TCD-031 state/restart correction. They do prevent promotion of that decision into a production checkpoint claim without later implementation-level qualification.

## 7. Independent review question

The second-line reviewer must independently decide whether the evidence supports the following bounded proposition:

`For active macropore solute continuation, the accepted CoMp concentrations for every enabled species and both domains are mandatory persistent restart state; a valid restart must serialize those coordinates and restore them before establishing the RsCoMp result alias, without invoking a physical process or reconstructing missing concentrations from matrix state.`

The reviewer must fail closed if any species/domain owner, lifecycle transition, external hydrology dependency, or evidence identity is not independently reproducible from the pinned material.

The authoring context may not sign the Tier-C review gate.

## 8. TCD-025 boundary

B3B10 does not compose TCD-025. STATEQ03/04 remove the state-owner ambiguity needed for later TCD-025 storage terms, but TCD-025 still requires its own Class-A observer qualification covering direct drainage/Dra4 integration, conservation identity and exact state/flux non-interference.

## 9. Hard boundaries

- no production source modification;
- no frozen B0 modification;
- no canonical register modification;
- no B3 admission;
- no canonical STATE admission;
- no B4;
- no central-regie update;
- no TCD-025 composition;
- no new numerical tolerance.

Final readiness decision, subject to machine validation:

`QUALIFIED_CLASS_C_ADMISSION_READINESS_GOV04_TIER_C_INDEPENDENT_REVIEW_REQUIRED`

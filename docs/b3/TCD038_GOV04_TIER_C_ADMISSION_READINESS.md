# ANIMO-B3B09 — TCD-038 Crop Actual Uptake Restart Initialization Direction Qualification

## Decision

`TCD-038` remains a **B3 Class B local implementation correction**, but its admission-readiness route is **GOV04 risk Tier C**.

The requested workunit identifier `ANIMO-B3B08` could not be reused: live GitHub inspection found that `ANIMO-B3B08` is already the qualified TCD-028 readiness workunit. To avoid authority collision or overwrite, this TCD-038 workunit is allocated the next free identifier `ANIMO-B3B09` and branch `work/animo-b3b09-tcd038-crop-actual-uptake-restart-readiness`.

This is readiness qualification only. No production source is patched, no canonical STATE admission is made, no composition with TCD-039 is performed, no B4 or production migration is opened, and RG05G is not created or updated.

## Authority snapshot

Authoring base and aggregate central-regie authority:

`ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`

Post-RG05F atomic admissions observed at workunit start:

- `ANIMO-B3D15@22e48f7e2c1eaa1245f034de2d909191d9cfa227` — TCD-030;
- `ANIMO-B3D16@8650ea9e716336520d8d7df5f9ea2b393d17ab98` — TCD-023.

Governance and routing authorities:

- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4` for the TCD-038/039 canonical intake supplement;
- `ANIMO-B3I03@814ea660d367494432beb63ea78298d1f6cd73d7` for the later canonical register state through TCD-042;
- `ANIMO-B3I04@400b7cd79f89043e091751707dfa96537587dcf6` for later STATEQ02 incremental intake without new TCD allocation;
- `ANIMO-STATEQ01@4adae99576eb56978da71f7c8a250e4445fd3bc4`;
- `ANIMO-STATEQ02@ada93a409aa054f9aebac32728e79f80468215a7` as restricted-core split-run evidence only;
- `ANIMO-PREP12@3d86de057247adcfeefb82c11d7cf7d5b2cbdf73`, provenance-preserving rehome of PREP10 restart evidence;
- underlying `ANIMO-PREP10@761db23269b45ba79df3be97ea85289682e57106`.

No dedicated TCD-038 readiness or review branch and no later TCD-038 workunit was found before creating B3B09.

## Canonical target

At `ANIMO-B3I03`, canonical `TCD-038` is `crop actual uptake restart initialization`. The registered defect is that revision-53 reads nonzero cumulative actual N and optional P uptake into `Rsamplni_act` and `Rsamplpo_act`, but `Inicalc` copies in the opposite direction before accepted state has been restored. The canonical row remains `OPEN`.

TCD-039 is different. It concerns missing restart representation of potential cumulative uptake. TCD-039 is not composed with, repaired by, or admitted through this workunit.

## Frozen B0 identity

Pinned frozen identities:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Relevant frozen source members:

| member | SHA-256 | role |
| --- | --- | --- |
| `Inicalc.for` | `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1` | initialization seam |
| `input1.for` | `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95` | reads `>orgpla:` actual uptake |
| `Output_Init.for` | `6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f` | serializes actual uptake |
| `Init.for` | `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058` | ordinary accepted-step handoff |
| `Upintg_Plant.for` | `d6a6afd6bbc2515697e9bb294ea6bb06ce8a552760f99c2686442d78d19274af` | plant result-state update |
| `Upintg_Extern.for` | `d4f4ae0730e6ea0556c339a98268ed5b94262634c5aecce2e19aed058929069e` | external-crop result-state update |

The source archive and testbank remain untouched.

## Exact source seam and lifecycle ownership

The frozen `Inicalc.for` seam is lines 394-403. The active trigger is:

```fortran
If ( Kicr(1).Ne.6 .Or. (Kicr(1).Eq.6 .And. Ioptcu.Eq.1)) Then
```

Within that branch revision-53 executes:

```fortran
If(Rsamplni_act.Lt.1.0d-4) Amplni_act = 0.0
Rsamplni_act = Amplni_act
Amplni_pot = 0.0
If(Ipo.Eq.1)Then
   If(Rsamplpo_act.Lt.1.0d-4) Amplpo_act = 0.0
   Rsamplpo_act = Amplpo_act
   Amplpo_pot = 0.0
End If
```

`input1.for` reads `Rsamplni_act` and, with P enabled, `Rsamplpo_act` from `>orgpla:`. `Output_Init.for` writes those same result-side actual-uptake coordinates to `>orgpla:`. During ordinary accepted timesteps `Init.for` maps `Rsampl*_act -> Ampl*_act`, while `Upintg_Plant` and `Upintg_Extern` seed the next result state from `Ampl*_act` before adding interval uptake.

The ownership is therefore a lifecycle alias, not two independent scientific owners:

`serialized/result-side Rsampl*_act -> accepted/current Ampl*_act -> next result-side Rsampl*_act -> serialized Rsampl*_act`.

The required initialization direction is unambiguous within this source contract: a represented nonzero `Rsampl*_act` value must first become the accepted `Ampl*_act` value. Revision-53 instead performs `Ampl*_act -> Rsampl*_act` before that handoff and can erase the represented continuation value.

## Bounded candidate identity, not a production patch

The atomic candidate is defined only as the missing read-to-accepted assignments before the existing small-value logic:

```fortran
Amplni_act = Rsamplni_act
```

and, inside the existing `Ipo.Eq.1` branch:

```fortran
Amplpo_act = Rsamplpo_act
```

All existing threshold, P guard, trigger logic and result-side copies remain unchanged. This candidate is recorded as an evidence identity only. It is not applied to `src/`, the frozen archive, or any production source surface in B3B09.

## Cold-start and restart semantics

Revision-53 does not expose a separate restart discriminator on this `>orgpla:` initialization path. The same input surface is used for an initial state and for a state emitted by `Output_Init` and read back later. That is precisely why the correction cannot be treated as GOV04 Tier B merely because the edit is local.

The bounded semantics are:

- if the applicable trigger is false, TCD-038 makes no change;
- for N on the applicable path, a serialized/imported value below `1.0d-4` remains subject to the existing zeroing policy;
- for N at or above the threshold, accepted `Amplni_act` must equal the imported `Rsamplni_act` before the existing result-side copy;
- P follows the same rule only when `Ipo.Eq.1`;
- the candidate does not create a new checkpoint field, change serialization layout, or define potential-uptake continuation;
- a cold start supplying zero or a sub-threshold actual-uptake value is unchanged;
- a cold start or restart supplying a represented nonzero above-threshold cumulative actual uptake now preserves that explicitly supplied state rather than erasing it.

Thus checkpoint **representation** is unchanged, but checkpoint/initialization **restore semantics** change. That is a high-risk GOV04 trigger.

## Natural causal evidence

PREP10/PREP12 supplies four natural nonzero testbank cases in which the represented actual-uptake state is lost immediately after `Inicalc`:

| case | input N kg/m2 | input P kg/m2 | post-Inicalc N | post-Inicalc P |
| --- | ---: | ---: | ---: | ---: |
| `LWKM_gras_1040.2021.2045` | 0.0666813 | 0.0088759 | 0.0 | 0.0 |
| `GrassPeat` | 0.0632935 | 0.00675465 | 0.0 | 0.0 |
| `STONE_akk_0006.2001.2015` | 0.0195003 | 0.00295112 | 0.0 | 0.0 |
| `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA` | 0.0235216 | 0.00322743 | 0.0 | 0.0 |

The PREP10 minimal causal probe adds only the missing direction assignments. For LWKM, immediately after `Inicalc`, it preserves N `0.0666813` and P `0.0088759` on both accepted and result-side aliases. The probe changes downstream diagnostic output, so TCD-038 is not accounting-only. Those downstream diagnostic magnitudes are not scientific acceptance tolerances.

This is B1/source-bound diagnostic evidence. It is not B2 and is not promoted by B3B09.

## First post-restore use and consequence

The restored actual-uptake coordinate is carried into crop uptake integration and demand logic. Plant pathways use cumulative uptake and, for plant modes with potential uptake, later logic includes potential-minus-actual quantities. Therefore erasing actual cumulative uptake can alter later nutrient-demand, crop-uptake and dependent nutrient trajectories.

B3B09 does not quantify a field-scale or full-horizon magnitude. The exact predeclared difference is narrower: on the active above-threshold path, the first accepted post-initialization actual-uptake value changes from the legacy erased value to the represented imported value. Only causally dependent later crop/nutrient states, fluxes and outputs may then differ.

## Split-run evidence boundary

STATEQ01 establishes that a real external-crop split route can be executed, but its earlier split did not isolate TCD-038 from other restart/frame and serializer effects. STATEQ02 later proves exact restricted-core checkpoint/restore continuation in its guarded profile, but explicitly excludes unresolved internal-crop restart state and does not retire or admit TCD-038.

Accordingly:

`TCD038_SPECIFIC_SPLIT_RUN_DISCRIMINATOR = NOT_CAUSALLY_ISOLATED`

The existing split evidence is retained only as route/context evidence. It is not promoted to proof of TCD-038 whole-trajectory equivalence or magnitude.

## GOV04 risk classification

B3 qualification class and GOV04 risk tier are separate axes.

`B3 qualification class = B_LOCAL_ALGEBRA_INDEX_SPECIES`

This remains Class B because the candidate is a bounded local assignment-direction correction, introduces no new state variable or representation, changes no governing physics, numerical policy, solver, tolerance or precision rule, and does not compose TCD-039.

`GOV04 risk tier = C`

Under `STRICTEST_APPLICABLE_RISK_TRIGGER_WINS`, Tier B is forbidden here. The following Tier-C triggers apply:

1. `RESTART_OR_COLD_START_DISCRIMINATION`: the same initialization surface is used for ordinary initial values and serialized continuation, and the candidate changes treatment of above-threshold supplied state;
2. `INITIALIZATION_SEMANTICS`: the candidate changes the accepted state established by `Inicalc`;
3. `CHECKPOINT_SEMANTICS`: `>orgpla:` representation is unchanged, but the meaning of reading a represented continuation value changes from erasure to restoration.

The ownership itself is not ambiguous after source reconstruction, so `SCIENTIFIC_STATE_OR_SOURCE_OWNERSHIP_AMBIGUITY` is not used as an additional trigger. No `MISSING_OR_REDEFINED_PHYSICAL_STATE`, `NUMERICAL_POLICY`, `SOLVER_OR_TOLERANCE_CHANGE`, or composition trigger applies.

Formal classification:

`GOV04_TIER_C__B3_CLASS_B_LOCAL_RESTART_INITIALIZATION_DIRECTION`

## Tier-C restart/state contract

The claim-scoped restart/state contract is qualified for readiness as follows:

- state coordinate: cumulative actual crop N uptake, and cumulative actual crop P uptake when P is enabled;
- accepted/current alias: `Amplni_act`, conditional `Amplpo_act`;
- result/serialized alias: `Rsamplni_act`, conditional `Rsamplpo_act`;
- units: kg N m-2 and kg P m-2 respectively, as evidenced by PREP10/test input interpretation;
- serialization surface: existing `>orgpla:` fields only;
- read direction: serialized/result-side alias to accepted/current alias;
- normal accepted-step direction: result-side to accepted in `Init`, then accepted to result-side and interval increment in uptake integration;
- cold-start rule: retain existing input value semantics and existing `1.0d-4` small-value reset;
- P activation: existing `Ipo.Eq.1` guard retained;
- trigger boundary: existing crop route predicate retained;
- checkpoint representation: unchanged;
- potential uptake: explicitly outside this TCD and owned by TCD-039;
- first restored-state discriminator: exact equality to imported above-threshold actual uptake before later process execution;
- numerical policy, solver and tolerance: unchanged.

The direction is therefore not scientifically ambiguous at the claim-scoped handoff. What remains unknown is historical native manifestation and the isolated full split-run magnitude, not the source-level restore ownership/direction.

## Conservation and non-interference

TCD-038 does not introduce an independent N or P storage or an immediate physical mass transfer. The corrected assignment restores a cumulative continuation coordinate. Conservation is therefore not a separate local transfer identity at the assignment itself. Any later uptake differences must flow through the existing crop/nutrient process and balance equations and may not be hidden with a tolerance.

Non-interference is bounded structurally:

- no source file is changed in B3B09;
- the candidate identity contains only the two guarded read-to-accepted assignments;
- existing crop trigger, P guard and small-value threshold remain unchanged;
- no potential uptake state, management, hydrology, GHG, macropore, stable-DOM, solver, precision, tolerance, ledger-definition or serialization-layout logic is part of TCD-038;
- no global whole-model equivalence is claimed.

## Historical route and residual uncertainty

GOV03 records `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and permits the governed historical-uncertainty route subject to claim-scoped B3 requirements. It does not create B2.

Therefore:

`historical revision-53 native behaviour = UNKNOWN_WITHOUT_B2`.

Residual uncertainties retained for independent review are:

- no qualified historical Intel/native TCD-038 split-run exists;
- the existing STATEQ01 split route does not causally isolate TCD-038;
- downstream full-horizon magnitude after preserving actual uptake is not a qualified tolerance or prevalence estimate;
- TCD-039 can independently affect crop continuation and must remain outside this atomic correction.

## Independent-review gate

The claim-scoped Tier-C prerequisites for authoring readiness are satisfied: B0 identity, B1 causal evidence, GOV03 route, exact local/domain contract, lifecycle ownership and units, initialization/restart semantics, expected difference, structural non-interference, edge/guard semantics, explicit residual uncertainty and preservation of historical unknown are all persisted.

The next gate is exactly one genuinely independent GOV04 Tier-C second-line review in a separate context. This authoring context does not perform or sign that review.

Subject to the machine validator and scope guard passing on the final branch head, the readiness decision is:

`QUALIFIED_CLASS_B_ADMISSION_READINESS_GOV04_TIER_C_RESTART_SEMANTICS_INDEPENDENT_REVIEW_REQUIRED`

# ANIMO-B3B05 - TCD-023 Stable-DOM P Cross-Species Partition Admission Readiness

## Decision

`TCD-023` is qualified as an atomic `B_LOCAL_ALGEBRA_INDEX_SPECIES` admission-readiness claim under `ANIMO-GOV04` Tier B.

This is readiness for exactly one genuinely independent second-line review. It is not a B3 admission, not a production authorization, not a historical-fidelity claim, and not a correction to the frozen B0 source.

The qualified atomic candidate is limited to these two `Resp_miner` Case(2) expressions:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfop(17,Ln)
```

No other stable-DOM, phosphorus, sorption, reporting, restart or numerical change is part of this workunit.

## Live authority and collision check

Before branch creation on 2026-09-10, live GitHub discovery found no `ANIMO-B3B05`, no dedicated TCD-023 readiness branch, no later TCD-023 review/readiness workunit and no TCD-023 review issue.

The workunit was created from the then-current aggregate central-regie authority:

`ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`

The later sibling admission `ANIMO-B3D13 / TCD-027@b20841eb71c338cad21abd8164fa025d8efc75c4` was observed but was deliberately not merged into this workunit.

The pinned governance and evidence authorities are:

- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- PREP04 source-bound diagnostic evidence as evidence input only

The canonical TCD register still records TCD-023 as `OPEN` and classifies the defect as a confirmed legacy cross-species algebra defect with low-rate process/state coupling. This readiness workunit does not modify that register.

## Frozen B0 identity

The supplied frozen artifacts were independently hashed before diagnostic work:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- `resp_miner.for` member SHA-256: `938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106`

These values match the pinned repository hash records and source manifest. The frozen archives were not modified.

A clean GNU diagnostic rebuild reproduced the pinned PREP01 deterministic executable SHA-256 exactly:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

This strengthens diagnostic reproducibility, but does not turn the GNU executable into a qualified historical revision-53 reference.

## Exact causal seam

Independent extraction of the frozen source confirms the Case(2) selector:

```text
Recfhu < 1e-12
AND RecfHUSDO < 1e-12
AND recfSDO >= 1e-12
```

Case(2) is the stable-DOM to humus path when humus decay is effectively disabled at the selector threshold while stable-DOM decay remains active.

The frozen source constructs separate parents:

```fortran
Transfon(17,Ln) = Mofr(Ln)*recfSDO(Ln)*AvcoStdiorni(Ln)*Hest
Transfop(17,Ln) = Mofr(Ln)*recfSDO(Ln)*AvcoStdiorpo(Ln)*Hest
```

but then assigns the P daughters from the N parent:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)
```

The source locations in the frozen member are Case(2) at line 518, `Transfon(17)` at 556, `Transfop(17)` at 563, and the two disputed P daughters at 564 and 565. `Tomnpo` consumes the P daughters at line 1042 and `Rekopo` is formed at line 1270.

## Species ownership, units and local identity

`Hest = He(Ln) * St`. With `recfSDO` in d-1 and the stable-DOM N and P concentrations in their respective mass-per-volume units, `Transfon(17)` is an N-owned areic transfer and `Transfop(17)` is a P-owned areic transfer. `AsfaSDO` is dimensionless.

The required species-local P identity is therefore:

```text
Transfop(19) + Transfop(20) = Transfop(17)
```

The candidate satisfies this algebraically without a tolerance:

```text
[(1 - AsfaSDO) + AsfaSDO] * Transfop(17) = Transfop(17)
```

The frozen expression instead closes the P daughter sum to `Transfon(17)`. Its local P residual is therefore `Transfon(17) - Transfop(17)` whenever the N and P parent values differ.

An independent exact-decimal discriminator, deliberately different from SYNQ-O004, gives:

```text
Transfon(17) = 0.00164052
Transfop(17) = 0.000248724
candidate P19 = 0.00018903024
candidate P20 = 0.00005969376
candidate P19 + P20 - P17 = 0
legacy P19 + P20 - P17 = 0.001391796
```

This makes the species substitution observable rather than accidentally masked by equal parent values.

## No intended implicit N/P conversion at this seam

No local evidence supports an implicit N-to-P conversion in these two assignments.

The source already computes the P parent immediately before the disputed daughter assignments. Carbon and nitrogen each partition their own species parent. Other active stable-DOM P cases in the same routine partition `Transfop(17)`. PREP05 independently isolates exactly these two statements as high-confidence N/P sibling asymmetries while retaining explicit, scientifically meaningful N/P couplings elsewhere as negative controls. There is no N:P ratio, stoichiometric coefficient or conversion function in the disputed Case(2) assignment.

This conclusion is deliberately narrow. It qualifies the absence of an intended hidden conversion at the atomic Case(2) partition seam. It does not qualify every stable-DOM formulation in ANIMO.

## SYNQ-O004 and SYNQ-O005

Both SYNQ01 oracles are applicable and strongly independent of the frozen implementation path.

`SYNQ-O004` is an analytical oracle. Per species X it defines `X17 = m*k*C_X*H`, `X19 = (1-a)*X17`, and `X20 = a*X17`. Deliberately asymmetric N and P parents expose the frozen cross-species substitution.

`SYNQ-O005` is a metamorphic oracle. Permuting species labels together with species inputs must permute the corresponding species-local daughter outputs. The frozen Case(2) P assignments violate that relation when N and P parent values differ.

Neither oracle establishes historical prevalence or historical executable behaviour. Their shared assumption that no hidden cross-species conversion is intended is separately checked by the exact source seam and PREP05 negative controls.

## Natural activation and independent diagnostic replay

`Puitmijn_Cranendonck_60` has the phosphorus cycle active and naturally exercises the disputed Case(2) path.

An independently rebuilt observer replay reproduced 9,658 unique Case(2) time-layer activation coordinates in layers 17 through 23. Repeated raw observer writes at identical coordinates were byte-identical at the seam and were deduplicated only for event counting. The independently observed ranges also reproduce PREP04:

```text
Recfhu: 8.33707622733057e-15 .. 9.996862028415146e-13 d-1
recfSDO: 1.0004491472796685e-12 .. 1.1996234434098174e-10 d-1
recfSDO / Recfhu: 120
```

The accumulated frozen local identity mismatch is:

`1.0806894643265774e-11 kg P m-2`, equal to `1.0806894643265774e-7 kg P ha-1`.

The largest single-event mismatch is `1.0228664519933875e-14 kg P m-2`.

These independently reproduce the PREP04 causal values.

## Candidate conservation closure and process consequence

The two-line candidate was applied only to a temporary diagnostic execution copy. No production or frozen source was edited.

The independent replay reproduces the expected unrounded downstream change:

- maximum absolute `Tomnpo` delta: `1.0228664519933892e-14 kg P m-2 per step`
- maximum absolute `Rekopo` delta: `9.327856586446364e-15 kg P m-3 d-1`
- changed unique time-layer coordinates: 9,658, exactly the natural Case(2) activation surface

Thus the effect is small but not zero. TCD-023 cannot be treated as accounting or reporting only.

The whole-case organic-P balance response is also reproduced independently. For `bapoLO.Out`, the maximum absolute period deviation falls from `1.40e-8` to `5.59e-12 kg/ha P`, and the final cumulative deviation moves from `-1.08e-7` to `2.31e-11 kg/ha P`. For `bapoTP.Out`, the final cumulative deviation moves from `-1.05e-7` to `2.74e-9 kg/ha P`.

The remaining total-profile residual is not assigned to TCD-023. This workunit only claims removal of the TCD-023 causal contribution.

## Eight-case regression surface

The baseline and two-line candidate were independently executed across the eight PREP02-compatible cases. All reached `Successful completion of simulation` followed by the legacy `STOP 100` convention.

Comparison used no scientific numeric tolerance. Only the five already declared volatile metadata forms from the pinned PREP02 comparator were normalized.

Seven cases have no normalized scientific output difference:

- CranGrass
- CranMais
- GrassPeat
- LWKM_gras_1040.2021.2045
- RuurloGrass
- STONE_akk_0006.2001.2015
- Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA

Only `Puitmijn_Cranendonck_60` differs, in exactly the predeclared five files:

- `ani_pLO.Bal`
- `ani_pTP.Bal`
- `bapoLO.Out`
- `bapoTP.Out`
- `message.out`

There are no missing candidate outputs, no extra candidate outputs and no unexplained changed files.

## GOV04 risk tier

The scientific qualification class is Class B and the GOV04 risk tier is Tier B.

Tier A is not available because the correction changes `Tomnpo` and `Rekopo` at unrounded precision. Therefore physical/process non-interference, required for the Tier-A waiver, is false.

No Tier C or Tier D forcing trigger was found within the atomic candidate. The candidate does not change state ownership, initialization, restart or checkpoint semantics, branch thresholds, solver behaviour, tolerance policy, precision policy, missing-state representation, composition or production-bound source. A tiny downstream process consequence of a local wrong-species correction is expected Class-B behaviour and is not, by itself, a state-semantics change.

Any independent-review finding of broader state, restart, numerical, domain-contract, composition or production semantics must fail this Tier-B scope closed and trigger GOV04 escalation.

## Historical uncertainty

There is no qualified B2 for TCD-023. Under GOV03 the acquisition route is closed as unavailable after reasonable effort and the G6U historical-uncertainty route is eligible subject to claim-scoped B3 requirements.

Therefore:

`historical revision-53 behaviour = UNKNOWN`

No historical-fidelity claim is made. PREP04 and the independent GNU replay are diagnostic causal evidence, not historical reference evidence.

## Scope guard

This workunit does not compose with TCD-019, TCD-024, TCD-027 or any other stable-DOM or phosphorus correction. It does not modify production source, frozen B0, the canonical TCD register, B4, production migration, or the central RG05 aggregate.

The validator enforces the allowed-file set against the immutable RG05E authoring base.

## Readiness result and next gate

The atomic readiness result is:

`QUALIFIED_CLASS_B_ADMISSION_READINESS`

GOV04 Tier B requires exactly one genuinely independent second-line review in a separate ChatGPT context. This authoring context may not sign that gate.

The independent reviewer must independently verify the pinned source and scope, the P species identity, absence of a hidden conversion at this seam, SYNQ-O004/O005 applicability, natural activation, the nonzero process consequence, eight-case non-interference, the historical-unknown boundary, and the absence of a Tier C or D escalation trigger.

Only after one independent PASS should a later workunit decide disposition and admission closeout. Under GOV04 those two later stages should preferably be combined for this Tier-B item.

# ANIMO-B3B05R — Independent Second-Line Review Contract for TCD-023

## Purpose

This branch is a handoff for one genuinely independent second-line review of the atomic TCD-023 admission-readiness claim prepared by ANIMO-B3B05.

The review is not performed by this contract. The authoring context that prepared ANIMO-B3B05 may not sign the independent review gate.

## Frozen review object

Review the exact validated readiness head:

`ANIMO-B3B05@e76345bf984c58ff0b30a24b39dc8e037a2f4fd6`

Readiness branch:

`work/animo-b3b05-tcd023-stable-dom-p-partition-readiness`

Green readiness workflow:

- workflow: `ANIMO-B3B05 TCD-023 readiness`
- run: `34480049339`
- job: `102880280314`
- conclusion: `success`

The clean review branch was created directly from the exact validated readiness head above.

## Authorities to recheck independently

Do not inherit the authoring conclusions merely because they are persisted. Recheck the live authorities and pinned evidence before deciding PASS, FAIL or INCOMPLETE.

- aggregate central regie at readiness branch creation: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`
- risk-tier governance: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- historical-uncertainty route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- synthetic oracle authority: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`

Historical revision-53 behaviour remains `UNKNOWN` unless a qualified B2 has appeared. Do not infer historical fidelity from GNU diagnostic evidence.

## Frozen B0 identity

Recheck these exact identities:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- `ANIMO_4.1.5.53/resp_miner.for` SHA-256: `938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106`
- source-member size: `62997` bytes

## Atomic review object

Routine: `Resp_miner`

Source member: `resp_miner.for`

Branch: `Case(2)`, source description `no decay of humus pool; transfer from SDO to HU pool`.

Frozen legacy statements:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)
```

Atomic candidate:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfop(17,Ln)
```

Required local identity:

```text
Transfop(19) + Transfop(20) = Transfop(17)
```

The review must independently determine whether the P daughter transfers must partition the P parent `Transfop(17,Ln)`, rather than the N parent `Transfon(17,Ln)`.

## Required fail-closed review surface

A PASS requires independent resolution of every applicable point below. Any unresolved mandatory point is `INCOMPLETE` or `FAIL`, not PASS by inference.

1. Verify frozen B0 source and testbank identity and the exact `resp_miner.for` member identity.
2. Verify the exact Case(2) source seam, including selector conditions and source ownership of `Transfon(17,Ln)` and `Transfop(17,Ln)`.
3. Verify the disputed legacy statements at the frozen source seam rather than accepting the readiness report as source authority.
4. Verify units and species ownership. In particular, determine whether `Transfon(17)` is N-owned mass and `Transfop(17)` is P-owned mass at this seam.
5. Independently test whether any scientifically intended N-to-P conversion, N:P ratio, stoichiometric coefficient, conversion function or equivalent factor can justify using `Transfon(17)` in the P daughter assignments. If this remains ambiguous, fail closed.
6. Re-derive the local partition identity and verify that the proposed two-line candidate closes it without a numerical tolerance.
7. Verify the asymmetric exact-decimal discriminator and its negative controls. Synthetic evidence establishes causal algebra only, not historical prevalence or field realism.
8. Recheck applicability and independence boundaries of `SYNQ-O004` and `SYNQ-O005`. Neither oracle may be promoted to B2.
9. Recheck natural activation in `Puitmijn_Cranendonck_60`: phosphorus active, 9658 unique actual nonpotential Case(2) events, affected layers 17 through 23.
10. Recheck the local accumulated legacy mismatch `1.0806894643265774e-11 kg m-2 P`, corresponding to `1.0806894643265774e-7 kg ha-1 P`, and the maximum single-event mismatch `1.0228664519933875e-14 kg m-2 P`.
11. Recheck that the execution-only candidate removes the TCD-023 causal contribution to the P conservation mismatch without claiming that all whole-case P residuals must become zero.
12. Recheck the unrounded downstream process effect: maximum absolute `Tomnpo` delta `1.0228664519933892e-14 kg m-2 per step` and maximum absolute `Rekopo` delta `9.327856586446364e-15 kg m-3 d-1`.
13. Confirm that the process effect is genuinely nonzero. Therefore TCD-023 is not `A_ACCOUNTING_REPORTING_ONLY` and no GOV04 Tier-A waiver applies.
14. Reassess whether `B_LOCAL_ALGEBRA_INDEX_SPECIES`, GOV04 Tier B, is sufficient. If state ownership, initialization, restart, checkpoint, numerical-policy, solver, tolerance, ambiguous domain-contract, composition or production-bound risk is materially stronger than a local algebra-species consequence, escalate according to GOV04 rather than forcing Tier B.
15. Recheck the eight-case diagnostic regression surface. All eight compatible cases must complete. Only `Puitmijn_Cranendonck_60` may contain the predeclared normalized scientific differences: `ani_pLO.Bal`, `ani_pTP.Bal`, `bapoLO.Out`, `bapoTP.Out`, `message.out`. The other seven cases must have zero normalized scientific differences. No missing, extra or unexplained changed output is allowed.
16. Confirm that the comparison uses no scientific numeric acceptance tolerance. Only declared volatile timestamp and elapsed-time text may be normalized.
17. Confirm that affected unrounded source/state quantities are compared where formatted output precision hides the effect.
18. Recheck GOV03 route eligibility live. Without qualified B2, historical revision-53 behaviour remains `UNKNOWN` and no historical-fidelity statement is allowed.
19. Keep TCD-019, TCD-024, TCD-027 and every other stable-DOM or P correction outside the review object. Evidence from those workunits may not be composed into this candidate.
20. Confirm no production source modification, frozen-B0 modification, canonical TCD-register change, B4, production migration or central RG05 integration is part of this review.

## Primary evidence to inspect

At the frozen readiness head, inspect at minimum:

- `docs/b3/TCD023_CLASS_B_ADMISSION_READINESS.md`
- `integration/animo-b3/ANIMO-B3B05_STATUS.json`
- `integration/animo-b3/TCD023_UPSTREAM_EVIDENCE.json`
- `integration/animo-b3/TCD023_READINESS_FIXTURE.json`
- `integration/animo-b3/TCD023_EXPECTED_DIFFERENCE.json`
- `integration/animo-b3/TCD023_INDEPENDENT_RECHECK.json`
- `integration/animo-prep/PREP04_STABLE_DOM_P_PARTITION.json`
- `docs/prep04/STABLE_DOM_P_PARTITION_DEFECT.md`
- `integration/animo-prep/PREP05_CROSS_SPECIES_SYMMETRY_AUDIT.json`
- `integration/animo-prep/PREP01_DIAGNOSTIC_EXECUTION.json`
- `docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv`
- frozen source/testbank hash manifests and `reference/source/source_manifest.csv`

PREP04 and the ANIMO-B3B05 authoring recheck are evidence inputs. They are not independent-review conclusions.

## Independence boundary

Perform ANIMO-B3B05R in a separate ChatGPT context from ANIMO-B3B05 authoring. This establishes process independence only. Do not claim organizational or human independence unless that is actually true.

The current ANIMO-B3B05 authoring context must not write the scientific review result.

## Result contract

Persist a human-readable independent-review report and a machine-readable result on this review branch. The semantic result must be exactly one of:

- `PASS`
- `FAIL`
- `INCOMPLETE`

Record exact reviewed heads, evidence identities, residual uncertainties, validator result and scope-guard result.

A PASS is independent review evidence only. It is not B3 admission.

Under GOV04 Tier B, after one independent PASS the later formal disposition and admission closeout should preferably be combined in one separate workunit.

Stop before any admission, production patch, B4, production migration or central-regie update.

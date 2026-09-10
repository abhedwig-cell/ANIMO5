# ANIMO-B3D16 — TCD-023 GOV04 Tier-B Formal Disposition and Atomic B3 Admission

## Decision scope

This workunit consumes the completed, genuinely separate `ANIMO-B3B05R` second-line review and performs the GOV04-permitted post-review formal disposition and atomic B3 admission for the unchanged TCD-023 claim. It does not repeat or relabel the independent review.

Atomic claim:

> In `Resp_miner` Case(2), change only the two phosphorus daughter-transfer parent selectors so `Transfop(19,Ln)` and `Transfop(20,Ln)` partition `Transfop(17,Ln)` rather than `Transfon(17,Ln)`.

The admitted scientific scope is strictly the stable-DOM phosphorus cross-species parent-selector defect. No production source is changed here.

## Live authority snapshot before disposition

- Current aggregate central regie: `ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`.
- RG05F already integrates `TCD-027` through `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4` and `TCD-041` through `ANIMO-B3D14@d672992bbc32d40d7e0fbdf03f3fa9bc4cd5a522`.
- Latest qualified post-RG05F atomic admission observed before B3D16 authoring: `ANIMO-B3D15@22e48f7e2c1eaa1245f034de2d909191d9cfa227` for TCD-030. It is a sibling authority and is not composed into TCD-023.
- Readiness: `ANIMO-B3B05@e76345bf984c58ff0b30a24b39dc8e037a2f4fd6`.
- Independent second-line review: `ANIMO-B3B05R@4e277cfe98bf815b09e4d40d4e9f4af61e11a7fb`.
- Final review validation: GitHub Actions run `34483286125`, job `102891135467`, conclusion `success`, validator PASS and review-only scope guard PASS.
- GOV04: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`.
- GOV03: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`.
- B3Q01: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.
- SYNQ01: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`.

Immediately before B3D16 branch creation, no B3D16 branch and no TCD-023 disposition/admission branch were found. No RG05G branch existed. The B3D16 branch was created from the exact final independent-review head `4e277cfe98bf815b09e4d40d4e9f4af61e11a7fb`.

## Scientific disposition

The independent review returned semantic result `PASS` and independently re-established the exact frozen Case(2) seam:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)
```

while the qualified candidate is:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfop(17,Ln)
```

The required species-local phosphorus identity is:

`Transfop(19) + Transfop(20) = Transfop(17)`.

The candidate closes this identity exactly, without a numerical tolerance. The frozen legacy statements instead close to the nitrogen parent `Transfon(17)`.

`Transfon(17)` is N-owned and has units `kg N m-2 per interval`; `Transfop(17)`, `Transfop(19)` and `Transfop(20)` are P-owned and have units `kg P m-2 per interval`. No N:P ratio, stoichiometric conversion, conversion function or other intended N-to-P mechanism exists at this exact seam. PREP05 legitimate N/P-coupling negative controls remain valid and are not reinterpreted as TCD-023.

## Causal and expected-difference boundary

Natural activation is demonstrated in `Puitmijn_Cranendonck_60` with phosphorus active, 9,658 unique actual/nonpotential Case(2) events in layers 17 through 23.

The accumulated local legacy mismatch is `1.0806894643265774e-11 kg P m-2`, equivalent to `1.0806894643265774e-7 kg P ha-1`. The largest single-event mismatch is `1.0228664519933875e-14 kg P m-2`.

The candidate removes the TCD-023 causal contribution. It does not claim that all whole-case phosphorus residuals become exactly zero.

The unrounded downstream effect is genuinely nonzero:

- max `|delta Tomnpo| = 1.0228664519933892e-14 kg P m-2 per step`;
- max `|delta Rekopo| = 9.327856586446364e-15 kg P m-3 d-1`.

Therefore Tier A is not available.

Across the eight qualified regression cases, only `Puitmijn_Cranendonck_60` changes after volatile-metadata normalization, in exactly:

- `ani_pLO.Bal`;
- `ani_pTP.Bal`;
- `bapoLO.Out`;
- `bapoTP.Out`;
- `message.out`.

The other seven cases have zero normalized scientific differences. No missing, extra or unexplained outputs are admitted, and no scientific numerical tolerance is used.

## GOV04 risk disposition

The strictest applicable GOV04 trigger remains Tier B:

`GOV04_TIER_B__B_LOCAL_ALGEBRA_INDEX_SPECIES`

The correction is limited to two wrong-species parent selectors in a local algebraic partition. No persistent state ownership, initialization semantics, restart/checkpoint representation, state reconstruction, runtime architecture, branch threshold, solver, tolerance, precision policy, exact-zero policy or domain contract is changed.

Any future candidate wider than these two selector substitutions, or any later evidence that activates a stronger Tier-C or Tier-D trigger, invalidates this Tier-B disposition and requires fresh requalification.

## Evidence and historical uncertainty

Frozen evidence remains pinned to:

- source ZIP SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `ANIMO_4.1.5.53/resp_miner.for` SHA256 `938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106`, size 62997 bytes.

SYNQ-O004 and SYNQ-O005 remain synthetic independent oracles and are not B2. The GNU diagnostic replay is causal evidence, not historical fidelity evidence.

No qualified B2 historical reference exists for TCD-023. Under GOV03 the historical revision-53 behaviour therefore remains `UNKNOWN_WITHOUT_B2`. No historical fidelity claim is made.

## Non-composition

TCD-023 remains atomic. This workunit does not compose it with TCD-019, TCD-024, TCD-027, TCD-030, or any other stable-DOM or phosphorus correction.

No production source, frozen B0 artifact, canonical TCD register, B4 surface, production migration surface or aggregate central-regie artifact is modified.

## Atomic B3 admission decision

Subject to the fail-closed machine validation in this workunit, TCD-023 is dispositioned as:

`QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B`

The one independent second-line review required by GOV04 Tier B is satisfied by `ANIMO-B3B05R@4e277cfe98bf815b09e4d40d4e9f4af61e11a7fb`. B3D16 itself makes no independence claim.

This admission qualifies only the scientific correction identity and the bounded expected-difference surface. It does not authorize a production source patch.

## Hard boundary and aggregate cadence

B3D16 does not modify production or frozen source, edit the canonical TCD register, compose TCD-023 with other corrections, open B4, open production migration, or update aggregate central regie.

RG05F defines a normal cadence of 3 to 5 new atomic admissions before the next aggregate unless an earlier GOV04 trigger applies. With TCD-030 already qualified as the first post-RG05F atomic admission, TCD-023 becomes the second post-RG05F atomic admission if this workunit validates. Aggregate integration therefore remains pending.

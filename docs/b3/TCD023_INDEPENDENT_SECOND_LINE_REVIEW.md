# ANIMO-B3B05R — Independent Second-Line Review of TCD-023

Semantic result: **PASS**

This is independent second-line review evidence under ANIMO-GOV04. It is not B3 admission, disposition, production authorization or a historical-fidelity claim. Independence recorded here is process independence from the ANIMO-B3B05 authoring context only.

## Reviewed object and pins

- Repository: `abhedwig-cell/ANIMO5`
- Review branch: `review/animo-b3b05r-tcd023-independent-second-line`
- Review handoff: `284afb6ebe8047087f3444d198d55e633bdbc617`
- Readiness candidate reviewed: `ANIMO-B3B05@e76345bf984c58ff0b30a24b39dc8e037a2f4fd6`
- Aggregate authority rechecked live: `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`
- GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`
- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- SYNQ01: `842f72300fd03ede0b9024537a7ee6126722a121`
- Readiness Actions run/job: `34480049339` / `102880280314`, rechecked `success`

No later ANIMO-B3B05R review result or competing TCD-023 review issue was found before writing this result. Issue #45 was open and had no review comments.

## Frozen source identity

The review independently rechecked repository custody evidence rather than treating the readiness narrative as source authority.

- Source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- Testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- `ANIMO_4.1.5.53/resp_miner.for` SHA-256: `938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106`
- source-member size: `62997` bytes

The archive hashes come from the frozen repository hash files and the member identity comes from `reference/source/source_manifest.csv`. The reviewed source object is therefore unambiguously pinned even though the raw source archive itself is not committed.

## Independent scientific reconstruction

### Case(2) seam and species ownership

The pinned evidence converges on `Resp_miner`, Case(2), selected by:

`Recfhu < 1e-12 AND RecfHUSDO < 1e-12 AND recfSDO >= 1e-12`.

At the seam the species parents are separately constructed. In particular:

- `Transfon(17,Ln)` is built from `AvcoStdiorni`, hence is N-owned, with dimensions `kg N m-2 per interval`;
- `Transfop(17,Ln)` is built from `AvcoStdiorpo`, hence is P-owned, with dimensions `kg P m-2 per interval`;
- `Transfop(19,Ln)` and `Transfop(20,Ln)` are P transformation daughters, also `kg P m-2 per interval`.

The dimensional result follows from concentration `kg species m-3`, `recfSDO` in `d-1`, and `Hest = He*St` in `m d`, with dimensionless multipliers.

Frozen legacy statements:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)
```

Candidate:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)
Transfop(20,Ln) = AsfaSDO * Transfop(17,Ln)
```

### No intended N-to-P conversion at this seam

No N:P ratio, stoichiometric coefficient, conversion function or dimensional conversion occurs in either disputed assignment or its local Case(2) parent construction. Carbon and nitrogen daughters partition their own species parent and the P parent is calculated immediately before the disputed P daughters. PREP05 is used only as an orthogonal structural cross-check: its negative controls deliberately retain legitimate reciprocal N/P uptake coupling and an explicit N/P ratio relationship elsewhere, while only the two TCD-023 assignments are promoted by the narrow sibling-asymmetry rule.

The broader stable-DOM formulation remains outside this atomic claim. This review therefore does not infer a general species-decoupling law beyond this source seam.

### Exact local identity

Required:

`Transfop(19) + Transfop(20) = Transfop(17)`.

For the candidate:

`((1-AsfaSDO) + AsfaSDO) * Transfop(17) = Transfop(17)` exactly.

No numerical acceptance tolerance is required. The frozen legacy instead closes to `Transfon(17)`, with causal residual `Transfon(17)-Transfop(17)` whenever the two parent values differ.

An asymmetric exact-decimal discriminator independently makes that substitution observable. It is a causal algebra test, not historical or field evidence.

## SYNQ-O004 and SYNQ-O005

Both oracles apply to TCD-023 and are strongly independent of ANIMO implementation code in the SYNQ01 register.

- `SYNQ-O004` checks the species-local analytical parent/daughter identity.
- `SYNQ-O005` checks species-label permutation symmetry.

Their shared assumption is absence of an explicit cross-species conversion. That assumption is separately checked at the source seam and against PREP05 legitimate-coupling negative controls. Neither oracle is B2 and neither proves historical activation frequency, field realism or historical revision-53 behaviour.

## Natural activation and causal replay

The review did not accept the B3B05 headline counts in isolation. It cross-checked the independently persisted PREP04 diagnostic record against the later B3B05 source/replay record at the same frozen B0 identity, including the latter's raw observer-row and deduplication description. They agree on:

- case: `Puitmijn_Cranendonck_60`;
- phosphorus active: yes;
- unique actual/nonpotential Case(2) events: `9658`;
- affected layers: `17..23`;
- accumulated local legacy P mismatch: `1.0806894643265774e-11 kg P m-2`;
- equivalent scale: `1.0806894643265774e-7 kg P ha-1`;
- largest single-event mismatch: `1.0228664519933875e-14 kg P m-2`.

The causal explanation is exact at the local algebra level: legacy daughter sum minus the required P parent equals `Transfon(17)-Transfop(17)`. The accumulated observer mismatch agrees with the organic-P whole-case residual at the reported precision and the execution-copy candidate collapses the TCD-023 contribution. This review does not require unrelated whole-case P residuals to become zero.

## Downstream effect and risk tier

The replay evidence records genuinely nonzero unrounded consequences:

- max `|delta Tomnpo| = 1.0228664519933892e-14 kg m-2 per step`;
- max `|delta Rekopo| = 9.327856586446364e-15 kg m-3 d-1`.

Therefore Tier A/accounting-only is unavailable.

The atomic candidate does not change state ownership, initialization, restart/checkpoint semantics, branch thresholds, solver logic, solver tolerances, numerical precision policy or production source. No composition with TCD-019, TCD-024, TCD-027 or any other correction is present. Under GOV04 the strictest applicable trigger is therefore `B_LOCAL_ALGEBRA_INDEX_SPECIES`, Tier B. No Tier C or Tier D trigger was found.

## Eight-case regression surface

The pinned independent replay records successful completion for all eight required cases:

- CranGrass
- CranMais
- GrassPeat
- LWKM_gras_1040.2021.2045
- Puitmijn_Cranendonck_60
- RuurloGrass
- STONE_akk_0006.2001.2015
- Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA

Only `Puitmijn_Cranendonck_60` has normalized scientific differences, confined to:

- `ani_pLO.Bal`
- `ani_pTP.Bal`
- `bapoLO.Out`
- `bapoTP.Out`
- `message.out`

The other seven have zero normalized scientific differences. The evidence records no missing outputs, no extra outputs and no unexpected changed files. No scientific numerical tolerance is used; normalization is limited to declared volatile timestamp/elapsed-time metadata. Unrounded `Tomnpo` and `Rekopo` observations prevent formatted-output precision from masking the real process effect.

## Historical behaviour

GOV03 still records no qualified B2. Therefore historical revision-53 behaviour is **UNKNOWN**. GNU diagnostic execution and SYNQ evidence are not historical-reference evidence and are not promoted here.

## Residual uncertainty

The following uncertainties remain explicit and do not invalidate this narrow review:

1. No qualified historical B2 exists, so no historical-fidelity claim is made.
2. The naturally observed effect is tiny and demonstrated in one P-active supplied case near the Case(2) rate threshold. This review establishes causal correctness of the local species partition, not population-level field magnitude.
3. The broader stable-DOM theory/documentation gap remains outside the atomic TCD-023 seam.
4. Other phosphorus residual mechanisms remain outside scope; whole-case TP closure is not claimed.

## Scope guard

Excluded from this review and unchanged:

- TCD-019, TCD-024, TCD-027 and every other stable-DOM/P correction;
- production source;
- frozen B0;
- canonical TCD register;
- B4;
- production migration;
- central RG05 integration;
- B3 admission and formal disposition.

No admission or production modification was performed.

## Decision

**PASS**.

The independent GOV04 Tier-B second-line review gate for the exact TCD-023 readiness candidate `ANIMO-B3B05@e76345bf984c58ff0b30a24b39dc8e037a2f4fd6` is satisfied, subject to the persisted review validator and scope guard being green at the review head.

This PASS is review evidence only. It is not B3 admission.

The next allowed workunit after validated closeout of this review is one separate **combined GOV04 Tier-B formal-disposition + B3 admission-closeout workunit** for TCD-023. That workunit must start from the then-current authorities, pin this review head, preserve historical behaviour as UNKNOWN unless a qualified B2 has appeared, and must not silently compose other TCDs.
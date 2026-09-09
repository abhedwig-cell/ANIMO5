# ANIMO-B3B01 — TCD-015 Class-B Admission Readiness

Status: `QUALIFIED_TCD015_CLASS_B_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

This workunit qualifies an atomic Class-B readiness package for `TCD-015`. It does **not** admit corrected legacy behaviour, does not change production source, and does not claim B2 historical-reference evidence.

## 1. Scope

Target:

- TCD: `TCD-015`
- process: NO3 negative-concentration transport mass conservation
- B3 class: `B_LOCAL_ALGEBRA_INDEX_SPECIES`
- atomicity: `ATOMIC_LOCAL_ALGEBRA_CLAIM`

The only scientific hypothesis qualified here is:

> In the nitrate negative-concentration reconstruction, `Hv` is counted twice because `Hv1` already contains `Hv`, while `(Mt*Rsc-Mto*Co)/St` already represents the complete storage change.

Out of scope:

- clipping-policy redesign;
- any tolerance change;
- solver-policy or analytical-branch changes;
- broader transport-physics changes;
- automatic extension of this correction to non-NITRATE call paths;
- historical Intel-behaviour claims not supported by B2.

The present feature scope is core nitrate transport with `GreenHouseGasOption=0`. GHG-enabled downstream consequences remain residual uncertainty because the supplied `GHGMais` testcase is not contract-compatible with revision 53.

## 2. Frozen identities

The workunit is bound to the exact B0 identities:

- source evidence ID: `ANIMO-B0-SRC-41553-R53`;
- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 User's Guide SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`;
- source member: `ANIMO_4.1.5.53/Transsub.for`;
- source member SHA-256: `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`.

The supplied guide gives the general conservation and transport equation for dissolved substances, including NO3-N, but it does not define the revision-53 negative-concentration clipping algebra. The local correction therefore cannot be justified by documentation alone. Its scientific basis is the frozen source equation, an exact local conservation identity, natural B1 activation, and an independent synthetic conservation oracle.

EG01 has qualified the B0 retention contract and proof machinery, but external controlled immutable storage proof is still pending. This does not change the byte identities above and is retained as governance uncertainty rather than silently promoted to stronger B0 custody evidence.

## 3. Governing Class-B and route contract

The B3Q01 classification for TCD-015 is Class B and explicitly records that the proposed correction changes state/flux behaviour, so it is not an accounting-only correction.

Class-B readiness requires at least:

- exact causal code path;
- mathematical/species identity;
- affected states and fluxes;
- branch coverage;
- conservation evidence;
- non-interference evidence;
- historical disagreement or uncertainty recorded.

For a normal route, B3Q01 requires a qualified B2 path reproduction with unrounded affected NO3 state/flux comparison and exact clipping-branch activation.

For the historical-uncertainty route, GOV02 requires a documented failed B2 acquisition effort, scientific basis, independent cross-check, and second-line review. The route may not be used while PREP02R is still an active acquisition attempt.

Current PREP02R status is `BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`. The external archival request has not been sent, no historical artifact has been obtained, and no reference is qualified. Therefore neither the normal B2 route nor the historical-uncertainty route is currently available.

This is a hard admission blocker, not a reason to weaken the route.

## 4. Exact source expression and proposed atomic change

Frozen `Transsub.for` defines:

```text
Hv = (Mt-Mto)/st

Hv1 = Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv
```

In the second negative-concentration reconstruction, after `Rsc` has been set to the small non-negative value, the frozen revision-53 expression is:

```text
Reko = (Mt*rsc-Mto*Co)/St
     - (-Avc*Hv1 + Flo*Con/ld + Flb*Cb/ld + Fid*Coid/ld)
```

The candidate atomic nitrate algebra is:

```text
Reko = (Mt*rsc-Mto*Co)/St
     - (-Avc*(Hv1-Hv) + Flo*Con/ld + Flb*Cb/ld + Fid*Coid/ld)
```

Hence:

```text
Delta(Reko) = Reko_corrected - Reko_legacy = -Avc*Hv
```

The scientific change is only the removal of the duplicated moisture-storage contribution from the reconstructed zero-order term.

A future admitted implementation should preserve legacy behaviour for non-NITRATE paths unless a broader generic correction is separately classified and admitted. The earlier generic execution-only probe is therefore evidence, not authority for a generic production edit.

## 5. PREP01 causal evidence and natural activation

PREP01 localizes the largest 1997 LWKM nitrate balance residual to the transport mass-balance seam:

- case: `LWKM_gras_1040.2021.2045`;
- year: 1997;
- annual `baniGP.Out` residual: `+0.5760503022407 kg/ha N`.

The dominant natural event is:

- TITO: `2312`;
- layer: `1`;
- substance: `NITRATE`;
- analytical branch: `Iflsol=1`;
- `BAPD = -8.4267311478156e-4 kg/m2`;
- `BATR = -9.0054430498043e-4 kg/m2`;
- `BAPD-BATR = +5.7871190198869e-5 kg/m2`;
- equivalent: `+0.5787119019887 kg/ha N`;
- `Hv = 3.4507e-3 d-1`;
- `Hv1 = 6.4698353471977e-2 d-1`;
- legacy reconstructed `Reko = -1.6853462295631e-3 kg/m3/d`.

The exact duplicated mass contribution is:

```text
Avc * Hv * St * Ld
= 5.7871190198869e-5 kg/m2
= 0.5787119019887 kg/ha N
```

This equals the local `BAPD-BATR` discrepancy to floating-point roundoff. The causal claim is therefore equation-bound and does not depend on choosing a residual tolerance.

The legacy model itself reports the event as a nitrate mass-balance deviation exceeding its warning criteria, so the observed residual must not be reclassified as an acceptable numerical envelope.

## 6. Existing execution-only correction probe

PREP01 already ran a temporary correction probe on an execution copy. The frozen source remained unchanged.

At TITO 2312, layer 1:

- corrected `Reko = -1.8010886099609e-3 kg/m3/d`;
- corrected `BAPD = -9.0054430498043e-4 kg/m2`;
- corrected `BATR = -9.0054430498043e-4 kg/m2`;
- corrected local residual: approximately `-1.08e-19 kg/m2`.

For the 1997 LWKM GP nitrate balance, the residual falls from about `+5.76e-1 kg/ha N` to `+2.28e-7 kg/ha N`.

The baseline diagnostic execution emits three nitrate `TRANSPORT` mass-balance warnings in this case, at TITO 2312, 3042 and 4513. The correction probe emits none.

This is causal diagnostic evidence only. It is not corrected-legacy admission.

## 7. Independent SYNQ01 conservation oracle

SYNQ01 qualifies `SYNQ-O001` for TCD-015 as a strongly independent exact local conservation oracle.

Oracle identity:

```text
Hv appears once.
duplicated storage term = Avc * Hv * St * Ld
```

Synthetic discriminator:

- `Avc = 0.2 kg/m3`;
- `Hv = 0.1 d-1`;
- `St = 2 d`;
- `Ld = 0.1 m`.

Expected exact results:

- conservative residual: `0 kg/m2`;
- duplicated-Hv residual: `0.004 kg/m2`.

The oracle shares no ANIMO code, control flow, indexing, convergence logic, or approximation logic. It independently reconstructs the equation-level identity.

It does **not** establish historical Intel behaviour, choose clipping physics, create B2, or admit TCD-015.

## 8. Predeclared expected-difference surface

`integration/animo-b3/TCD015_EXPECTED_DIFFERENCE.json` was persisted before the broad eight-case B1 non-interference matrix.

Expected changed surfaces under an activated species-scoped nitrate probe:

- nitrate `Reko` in the exact second negative-concentration reconstruction;
- corresponding process-side `BAPD`;
- NO3 local and aggregated balance residuals caused by the duplicated-Hv term;
- mass-balance warnings caused solely by that term;
- downstream effective denitrification bookkeeping `Rekonide` when the existing `CORRECTION(2)` rule propagates the changed `Rekoni`;
- NO3 balance/report fields derived from that existing bookkeeping path.

Expected unchanged surfaces:

- clipping trigger and `Optneg` policy;
- `Vsmall` and all clipping/tolerance constants;
- `Ttry` and analytical branch selection;
- the already computed direct `Rsc` and `Avc` event values;
- hydrological states and fluxes;
- nitrate transport inputs and boundary concentrations;
- all non-NITRATE call paths under the species-scoped candidate;
- all paths not entering the exact reconstruction;
- all other transport physics.

No numerical tolerance is used to define this surface.

## 9. Additional B1 non-interference qualification

ANIMO-B3B01 rebuilt the deterministic GNU diagnostic baseline from the frozen source and reproduced the PREP01 executable SHA-256 exactly:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

An execution-only species-scoped nitrate probe was then compiled. It changes the `Hv1` expression only when `Substname` is nitrate.

Candidate diagnostic executable SHA-256:

`10686a76d914e661badeb8ba36057d43f23c5dbffd39e8b95ce367db24525b94`

Candidate execution-copy `Transsub.for` SHA-256:

`2e28838db0b03ab6571694e386c20eca0eb7ea2bb9d414a1facbb25dbd2f149b`

The frozen B0 source and testbank were not modified.

All eight PREP01-compatible natural cases completed for baseline and candidate:

| Case | Scientific differences after declared volatile normalization |
|---|---|
| `CranGrass` | none |
| `CranMais` | none |
| `GrassPeat` | N-balance outputs only |
| `LWKM_gras_1040.2021.2045` | N-balance outputs plus removal of the three nitrate mass-balance warnings |
| `RuurloGrass` | none |
| `STONE_akk_0006.2001.2015` | N-balance outputs only |
| `Puitmijn_Cranendonck_60` | none |
| `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA` | none |

Across 550 compared files, excluding captured process stdout:

- `430` files were raw-byte identical;
- `99` matched after only the five already-declared volatile metadata normalizations;
- `21` were scientifically different;
- all `21` differences were inside the predeclared N-balance/message surface.

No numerical tolerance was applied.

For every changed formatted `bani*.Out` line in the three activated cases:

- record 1 changes were confined to residual/cumulative-residual fields;
- record 3 changes were confined to the final denitrification field;
- beginning storage, end storage, other balance inputs/outputs, and all non-balance state outputs remained exact after declared volatile normalization.

The generic unguarded execution probe and the nitrate-scoped probe were scientifically identical across the same eight natural cases after declared volatile normalization. This shows that no additional non-nitrate activation was observed in this natural suite. It does not authorize a generic production correction.

## 10. Affected state and flux interpretation

The correction occurs after the direct `Rsc` and `Avc` event values have been reconstructed. Therefore the immediate direct concentration state at the activated local event is unchanged by this algebraic edit.

The corrected `Reko`, however, is used by the transport process accounting and can be propagated by the existing `CORRECTION(2)` bookkeeping into `Rekonide`. Consequently the scientifically affected surface is not merely a report ledger. It includes the nitrate process/source bookkeeping exposed downstream, which is consistent with the Class-B classification.

This is why TCD-015 must not be reclassified as Class A merely because the observed natural-suite output differences are concentrated in N balances.

## 11. Historical-reference status

No B2 claim is made from GNU B1 or SYNQ01.

Current facts from PREP02R:

- historical reference artifact obtained: `false`;
- external archival request sent: `false`;
- native reference run completed: `false`;
- native versus GNU comparison completed: `false`;
- reference qualified: `false`.

Therefore:

```text
NORMAL_B2_AVAILABLE = false
HISTORICAL_UNCERTAINTY_ROUTE_ELIGIBLE = false
```

The B3 disposition schema cannot yet validly express a final route for this target because current PREP02R is neither `AVAILABLE_QUALIFIED_REFERENCE` nor `UNAVAILABLE_AFTER_DOCUMENTED_ACQUISITION_ATTEMPT`.

The workunit therefore stops at admission readiness.

## 12. Independent second-line review

Independent second-line review is still required and is intentionally not self-certified by this workunit.

The review must independently check at least:

1. the frozen `Hv`, `Hv1`, storage and `Reko` algebra;
2. the PREP01 TITO-2312 causal arithmetic;
3. the independence and scope of `SYNQ-O001`;
4. the predeclared changed/unchanged surfaces;
5. the eight-case B1 non-interference matrix;
6. the PREP02R/GOV02 route state at review time;
7. that no clipping, tolerance, solver, or broader transport-policy change is being smuggled into the atomic claim.

Until that review is complete, `independent_review = FAIL_PENDING` for admission purposes.

## 13. Residual uncertainty

The remaining uncertainty is explicit:

- historical Intel/Windows behaviour on this exact path is unknown because B2 is not qualified;
- the frozen generic `Transsub` expression is shared by substances other than nitrate, while the TCD-015 admission candidate is intentionally nitrate-scoped;
- GHG-enabled downstream consequences are not naturally qualified because `GHGMais` is not revision-53 contract-compatible;
- optional macropore interaction is outside this natural TCD-015 non-interference matrix;
- external controlled immutable B0 storage proof is still pending under EG01.

None of these uncertainties is hidden by a tolerance or residual correction.

## 14. Readiness decision

The following Class-B readiness components pass:

- B0 byte identity;
- source-bound exact causal code path;
- natural B1 branch activation;
- PREP01 exact causal reconciliation;
- closed local nitrate conservation identity;
- independent SYNQ01 exact conservation oracle;
- predeclared expected-difference surface;
- broad natural B1 non-interference within the current core non-GHG feature scope;
- explicit historical uncertainty statement.

The following admission prerequisites do not pass yet:

- B2 or a GOV02-valid historical-uncertainty route;
- independent second-line review.

Therefore no B3 admission is performed.

Final workunit decision:

`QUALIFIED_TCD015_CLASS_B_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

# ANIMO-B3D09 — TCD-015 NO3 transport algebra GOV03 disposition

## Decision boundary

This workunit reconciles the already qualified TCD-015 Class-B readiness evidence with the later ANIMO-GOV03 historical-reference acquisition closure. It does not implement a source correction and does not admit TCD-015.

Formal disposition:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03`

The historical-uncertainty route gate is now PASS. The genuinely independent second-line review gate is still blocking.

Historical behaviour remains `UNKNOWN`. No historical fidelity is claimed.

## Live authorities

The disposition is pinned to:

- central regie: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`;
- historical route: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- TCD-015 readiness: `ANIMO-B3B01@b982242949aecab32b9067cf7910ad75abfc2b19`;
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- independent synthetic-oracle authority: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`.

At disposition start, no `ANIMO-B3D09` branch, later TCD-015 disposition branch, TCD-015 review branch or separate TCD-015 review issue was found. Existing PR #21 is the B3B01 readiness handoff. Its same-account `COMMENTED` review is not independent second-line evidence.

## Frozen B0 identity and direct source recheck

The authoring environment rehashed the supplied raw B0 archives before relying on the readiness wording:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `ANIMO_4.1.5.53/Transsub.for` SHA-256: `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`.

Direct inspection of the frozen `Transsub.for` confirms:

```fortran
Hv = (Mt-Mto)/st
Hv1 = Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv
...
Reko = (Mt*rsc-Mto*Co)/St - (-Avc*Hv1 + Flo*Con/ld + &
       Flb*Cb/ld + Fid*Coid/ld)
```

The target line is the second negative-concentration reconstruction after `Rsc = Vsmall`, `Hv2 = Zero` and the weighted `Avc` recomputation. The local candidate is:

```fortran
Reko = (Mt*rsc-Mto*Co)/St - (-Avc*(Hv1-Hv) + Flo*Con/ld + &
       Flb*Cb/ld + Fid*Coid/ld)
```

Thus candidate minus legacy is exactly `-Avc*Hv` at that reconstruction.

The source recheck also confirms that `Transsub` is a generic shared routine. In `Animo.for`, the main nitrate transport path calls `Transport` with `Substname='NITRATE'`, and `Transport.for` forwards that substance to `Transsub`. Therefore TCD-015 is nitrate-scoped by admission contract, not because the underlying source line is nitrate-exclusive.

**No generic shared-substance correction is authorized.**

## Scientific reconciliation

The B3B01 evidence remains internally consistent with the direct source recheck.

Natural activation is the supplied `LWKM_gras_1040.2021.2045` case. The dominant 1997 event occurs at TITO 2312, layer 1, `NITRATE`, `Iflsol=1`. Its local `BAPD-BATR` discrepancy is `5.7871190198869e-5 kg/m2`, equivalent to `0.5787119019887 kg/ha N`. The source-bound identity attributes exactly that term to `Avc*Hv*St*Ld`. The diagnostic execution-only candidate collapses the local discrepancy to approximately `-1.08e-19 kg/m2`, changes the annual GP residual from about `0.5760503022407` to `2.28e-7 kg/ha N`, and removes the three associated nitrate transport warnings. These values are causal evidence, not a tolerance and not historical truth.

`SYNQ-O001` independently states the same local conservation identity without using the ANIMO implementation. For `Avc=0.2`, `Hv=0.1`, `St=2` and `Ld=0.1`, one duplicated moisture-storage contribution is exactly `0.004 kg/m2`; the conservative form gives zero residual. SYNQ-O001 is a conservation oracle only. It is not B2 and does not establish historical prevalence.

The additional natural B1 matrix covers eight revision-53-compatible cases and 550 compared files. There are 430 raw-equal files, 99 equal after declared volatile metadata normalization and 21 scientific differences. All 21 differences stay within the predeclared nitrate/N-balance and warning surface. No numerical tolerance is used. Five cases remain scientifically unchanged; three naturally activate the scoped difference.

The IFLSOL supplement records 508 natural entries into the exact target reconstruction, all for `NITRATE`: 486 with `Iflsol=1` and 22 with `Iflsol=3`. `Iflsol=3` is an exact zero-delta control because `Hv=0`. An isolated frozen-source harness exercises reachable `Iflsol=4`. For valid positive storage denominators, the frozen pre-adjustment makes the target second reconstruction structurally unreachable for `Iflsol=2` and `Iflsol=5`. The reachable target modes are therefore covered without inventing a numerical tolerance.

## Class and scope

TCD-015 remains `B_LOCAL_ALGEBRA_INDEX_SPECIES`. It is not Class A because changing reconstructed `Reko` can change downstream nitrate process/source accounting and can propagate through existing nitrate bookkeeping. The qualified claim is limited to removal of the duplicated moisture-storage contribution at the stated nitrate reconstruction seam.

The following remain outside the claim:

- any clipping-policy redesign or change to `Optneg`, `Vsmall` or target selection;
- any solver, analytical-branch, iteration or convergence-policy change;
- any numerical tolerance change;
- any generic change to all substances using `Transsub`;
- any transport-physics change beyond the single duplicated storage contribution;
- GreenHouseGasOption-enabled consequences;
- optional macropore interaction outside the qualified natural matrix;
- composition with another TCD.

The qualified feature boundary is `GreenHouseGasOption=0`. GHG-enabled downstream effects remain residual uncertainty. This is a scope restriction, not evidence that GHG behaviour is equivalent.

## GOV03 route reconciliation

B3B01 was closed while PREP02R acquisition was still active, so its then-correct route field said the historical-uncertainty route was ineligible. That route state is obsolete.

GOV03 later qualified:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

and:

`G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`.

RG05D carries that route authority forward. The present disposition therefore marks the TCD-015 route gate PASS under GOV03. This does not turn the frozen-source Intel rebuild or GNU B1 evidence into B2. It does not establish historical behaviour. Historical behaviour remains `UNKNOWN`.

## Gate result

All claim-scoped scientific/Class-B gates required here are reconciled as PASS: frozen B0 identity, exact source algebra, natural causal activation, exact local conservation, SYNQ-O001 scope, predeclared expected difference, eight-case non-interference, reachable IFLSOL coverage, nitrate-only scope and the `GreenHouseGasOption=0` feature boundary.

The only blocking B3 admission gate after this disposition is a genuinely independent second-line review. Existing B3B01 authoring and the same-account PR #21 comment cannot satisfy that gate.

TCD-015 therefore remains **NOT ADMITTED**.

## Independent-review handoff

Prepare a clean branch:

`review/animo-b3b01r-tcd015-independent-second-line`

The reviewer must work in a separate ChatGPT context from B3B01/B3D09 authoring and independently recheck the source/evidence rather than treating this disposition as scientific authority. Separate-context independence may be claimed; organizational or human independence must not be claimed unless it actually exists.

A passing review is review evidence only. It does not itself admit TCD-015. Any later admission closeout must be a separate workunit and must preserve the GOV03 historical-uncertainty statement.

## Hard stop

ANIMO-B3D09 authorizes no production patch, no B4 step, no central RG05 update, no composition and no independent-review execution in this authoring context.

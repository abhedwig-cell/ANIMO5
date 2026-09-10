# TCD-026 GOV03 Formal B3 Disposition

## Scope

This workunit reconciles the already-qualified TCD-026 Class-A readiness claim with the current GOV03 historical-uncertainty route. It does not perform independent second-line review and does not admit TCD-026.

Atomic candidate:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

The claim is limited to observing the already-existing initial root-exudate organic-matter storage in the fresh-organic-matter reporting ledger. No initialization physics, physical state, process flux, restart state, numerical policy or production source is changed.

## Live authorities

- `ANIMO-RG05C@2d3cc363599ed32b6537f318462c27db5ffaa7c2`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-B3A04@5eaf02298603b85f802d8e35d6a63941d0878879`
- same-context technical review `ANIMO-B3A04R@27b1700a330959d1b5eae23a2094cad579630f14`
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`

Frozen B0 identities remain:

- source SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Route reconciliation

The older B3A04/B3A04R route statements predate GOV03 and are therefore stale as route authority. GOV03 now qualifies:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

and:

`G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`

For TCD-026, the B2 route gate is therefore PASS under the historical-uncertainty route. Historical revision-53 behaviour remains `UNKNOWN`; no historical fidelity is claimed.

## Readiness evidence retained

B3A04 and B3A04R establish a bounded Class-A readiness dossier with three causal activation families:

1. PREP06 synthetic activation with `10.0 kg/ha` initial Ex and a legacy first-period fresh-OM residual of `-10.0 kg/ha`.
2. Model-produced CranMais replay with `5989.6594 kg/ha` initial Ex and a legacy first-period printed deviation of approximately `-5990 kg/ha`.
3. Chronological CranMais 1974-to-1975 formatted restart activation with `642.718929 kg/ha` initial Ex and a legacy first-period deviation of approximately `-642.7/-643.0 kg/ha` depending on output precision.

In the chronological activation, the candidate closes the intended ledger term to numerical roundoff while legacy and candidate final restart state remain byte-identical from identical restart input. The bounded expected-difference surface is reporting-only.

No TCD-026-specific SYNQ01 oracle is registered. This is retained explicitly. STATEQ02 supports root-exudate continuation-state ownership relevance only and is not promoted to a TCD-026 ledger oracle or B2 reference.

## Negative boundary

The chronological formatted restart probe does not establish exact whole-model continuous-versus-formatted-restart identity. Its observed token-level differences remain a negative scope boundary, not a tolerance target and not a reason to broaden the TCD-026 claim.

The same-context B3A04R technical PASS is useful supporting evidence but cannot satisfy the independent second-line gate.

## Formal disposition

All claim-scoped readiness gates and the GOV03 route gate are presently reconcilable as PASS except genuine independent second-line review.

Therefore the formal disposition is:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03`

TCD-026 remains not admitted. No production patch, B4 migration, composition, whole-model equivalence or historical-fidelity claim is authorized.

## Next gate

Create a clean review branch and perform a genuinely separate second-line review from source/evidence. A PASS from that review may feed a later, separate TCD-026 admission-closeout workunit. The review itself must not perform admission.

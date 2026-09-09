# ANIMO-B3E01 - TCD-042-E1 finite-positive upper-reservoir Class-E admission readiness

Status: `PARTIAL_TCD042_E1_CLASS_E_READINESS_POSITIVE_HETOP_POLICY_QUALIFIED_FULL_CHILD_DOMAIN_AND_ADMISSION_ROUTE_FAIL_CLOSED`

Date: 2026-09-09

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-b3e01-tcd042-e1-class-e-admission-readiness`

Target: `TCD-042-E1`

Parent: `TCD-042`

Class: `E_NUMERICAL_POLICY`

Requested child trigger: `Flpn = 0 AND 0 < Flux < 1.0d-8`.

This workunit evaluates admission readiness only. It makes no production patch, B3 admission, parent TCD-042 admission, new TCD reservation, canonical-register change or TCD-042-B1 change.

## 1. Upstream qualification state

B3I05 canonically routes the existing parent `TCD-042` into two child qualification atoms:

- `TCD-042-B1`, exact zero;
- `TCD-042-E1`, finite-positive subthreshold numerical evaluation.

The child keys are not new top-level TCD rows and `TCD-043` remains unreserved.

NQ03 selected the restricted binary64 policy

`NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY`

for

`Flpn=0`, `0<Flux<1.0d-8`, `Hetop>0`, and `0<P<=3.8510200002999744e-7`,

with

`P = St*Flux/Hetop`,

`A1 = exp(-P)`,

`f = 1-P/2+P^2/6`,

`g = 1/2-P/6+P^2/24`,

`A2 = (St/Hetop)*f`,

`B1 = f`,

`B2 = (St/Hetop)*g`.

NQ03R then independently reconstructed the governing equation with a 120-decimal-digit oracle and passed the restricted policy. The independent review reproduced direct binary64 cancellation, rejected `expm1` as a complete policy because the second-order `g` coordinate still cancels, confirmed degree 2 as the minimum declared series order, verified conservation and interval subdivision, and confirmed one-sided continuity to the UBQ01 exact-zero limit.

Thus the numerical-policy evidence required by Class E is materially stronger than at B3I05 intake. The restricted positive-`Hetop` numerical formulation is qualified and independently reviewed.

## 2. Exact expected difference from the legacy finite-positive fallback

The legacy `Flux < 1.0d-8` fallback uses

`A1=1`, `A2=0`, `B1=1`, `B2=0`,

so

`C1_legacy = C0`

and

`Cavg_legacy = C0`.

For the qualified positive-`Hetop` policy,

`C1_candidate = C0*exp(-P) + Load*(St/Hetop)*f(P)`

and

`Cavg_candidate = C0*f(P) + Load*(St/Hetop)*g(P)`.

Therefore the declared immediate differences are

`Delta C1 = C0*(exp(-P)-1) + Load*(St/Hetop)*f(P)`

and

`Delta Cavg = C0*(f(P)-1) + Load*(St/Hetop)*g(P)`.

Unlike the exact-zero B1 atom, finite positive flow also permits a same-interval exported-mass change:

`Delta Export = St*Flux*Delta Cavg`.

The accepted upper-reservoir end state can therefore change, the same-interval reservoir export can change, and later chemistry can change through the existing causal continuation path. Hydrology and external forcing are not changed by the policy itself.

This is a numerical solution change to the represented reservoir equation. It is not an accounting-only correction.

## 3. Natural reachability and materiality boundary

UBQ02 found 1,238 natural finite-positive subthreshold records in six executed cases. The observed coordinate envelope is

`4.2351647362715017e-20 <= P <= 3.8510200002999744e-7`.

Only four persisted records have nonzero mineral-N load, all in Ruurlo at `TITO=527, 533, 595, 847`. Natural loaded-event materiality is therefore directly demonstrated for mineral N.

The trace also contains 748 P-enabled E1 records, but no nonzero P load in those records. No nonzero DOM or DON load is present in the persisted E1 trace. B3E01 does not convert the species-independent coefficient proof into a false claim that natural loaded-event materiality has been demonstrated for every reservoir species.

The numerical policy itself remains species-independent because `A1`, `A2`, `B1` and `B2` depend on `P`, `St` and `Hetop`, not on species identity. This supports generic coefficient qualification while preserving the narrower natural-materiality statement.

## 4. Domain reconciliation exposes a hard readiness boundary

A live source-bound peer recheck in ANIMO-B3B02 identified a fact that is also material to E1: frozen revision-53 input validation accepts `Hetop = 0`. The input read at `input1.for:1826-1829` uses lower bound zero, and the legacy `Checkrea` semantics reject values below the bound rather than equality with it.

This is independently supported by the pinned ANIMO 4.0 user's guide, SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`. Alterra Report 224 (2005), Table 6 on report page 42 defines `HETOP` as the thickness of the virtual reservoir from which fertilizer additions leach proportional to cumulative precipitation and gives the documented range `[0.0 ... 0.2] m`. Zero is therefore not merely an accidental parser edge inferred from source. The reviewed documentation does not supply a separately qualified zero-thickness transport rule that would resolve E1.

NQ03 intentionally requires

`Hetop > 0`.

That is not cosmetic. Its conditioning coordinate and coefficients contain division by `Hetop`:

`P = St*Flux/Hetop`,

`A2 = (St/Hetop)*f`,

`B2 = (St/Hetop)*g`.

At `Hetop=0` and finite positive Flux, `P` is not a finite conditioning coordinate. The recovered differential reservoir equation

`Hetop*dC/dt = Load - Flux*C`

degenerates to the algebraic relation

`0 = Load - Flux*C`.

NQ03 did not qualify that zero-thickness model semantics, and B3E01 does not invent one.

This creates a precise scope mismatch:

- B3I05 routes E1 as `Flpn=0 AND 0<Flux<1.0d-8`;
- NQ03/NQ03R qualify only the positive-`Hetop` subset of that child trigger;
- source validation and the pinned user guide both admit/document `Hetop=0`;
- therefore the complete routed child trigger is not covered by the qualified policy.

B3E01 does not silently add `Hetop>0` as a production guard. Such a guard would encode an unresolved policy for an accepted zero-thickness configuration. Either an authoritative model contract must exclude `Hetop=0`, or zero-thickness semantics must be qualified separately, or the canonical child scope must be explicitly refined through governance. Until then the full E1 child domain fails closed.

## 5. Implementation-order finding remains downstream-visible

NQ03R found that the exact-rounded dense-envelope claim is evaluation-order dependent.

The Horner evaluation used by the qualification validator matches the rounded high-precision reference at all 2,008 probes. A mathematically equivalent literal binary64 expression differs by about one ulp on some probes:

- 67 `f` probes differ;
- 73 `g` probes differ;
- 129 unique probes differ in at least one coordinate.

This does not invalidate the mathematical degree-2 policy. NQ03 selected no production implementation. It does block any later claim of bitwise production binding until the coefficient evaluation order and FP contraction/reassociation semantics are frozen, or the chosen implementation is separately qualified against an equation-derived ulp bound.

No epsilon or balance-residual-derived tolerance is introduced here.

## 6. Governance route is currently closed

B3Q01 requires a formal admission route. GOV02 makes B2 claim-scoped rather than globally mandatory, but it does not permit the historical-uncertainty route while reasonable B2 acquisition remains open.

The current authoritative PREP02R head is `a2fda49871ee3c7104daf7e06cd8dffdac06b125`. Its status is

`PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED`.

PREP02R records:

- no qualified historical B2 reference;
- no provenance-qualified historical reference artifact;
- the supplied 2026 executable is a modern native rebuild, not historical B2;
- the external WUR archival/provenance request remains unsent;
- `historical_uncertainty_route_eligible = false`.

The separate PREP02R internal-stop record is explicit that stopping further internal archaeology does not close GOV02 acquisition. It retains `B2_ACQUISITION_STILL_ACTIVE` and prohibits using the internal stop as no-B2 admission eligibility.

Consequently both available B3 routes fail closed today:

`NORMAL_B2_AVAILABLE = false`

and

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY eligible = false`.

The successful NQ03/NQ03R scientific work cannot override this route gate.

## 7. Formal child disposition carrier is not yet reconciled

The qualified B3Q01 disposition schema currently constrains `tcd_ids` with

`^TCD-[0-9]{3}$`.

`TCD-042-E1` does not match that pattern. B3I05 simultaneously states that `TCD-042-E1` is a child atom key, not a top-level TCD row.

B3E01 therefore does not fabricate a formal B3 disposition by writing `tcd_ids=["TCD-042"]`. That would silently replace the atomic child with its non-atomic parent and would weaken B3Q01's atomicity rule.

Before an actual admission disposition is encoded, governance needs an explicit child-atom disposition convention or schema adapter that preserves:

- parent `TCD-042` identity;
- atomic child `TCD-042-E1` identity;
- no new top-level TCD reservation;
- no false claim that the parent as a whole is admitted.

This is a disposition-carrier issue, not a reason to reserve `TCD-043`.

## 8. Independent numerical review is complete, B3 disposition review is not

NQ03R is a completed methodologically independent numerical review of the restricted policy. That satisfies the dedicated Class-E numerical-review gate for the policy itself.

It is not an independent second-line review of a future B3 admission disposition. No such disposition exists yet because the route and domain gates are closed. B3E01 therefore records

`independent_numerical_review = PASS`

but

`independent_B3_disposition_review = FAIL_CLOSED_NOT_PERFORMED`.

No organizational-independence claim is made for NQ03R.

## 9. Readiness matrix

| Gate | Result |
| --- | --- |
| frozen B0 identity | PASS |
| canonical child routing | PASS |
| governing reservoir equation | PASS |
| legacy finite-positive fallback reconstruction | PASS |
| dimensionless conditioning coordinate P | PASS |
| high-precision oracle | PASS |
| degree-2 policy selection | PASS, restricted domain |
| direct binary64 cancellation characterization | PASS |
| expm1-only rejection | PASS |
| binary64 precision study | PASS, restricted domain |
| binary32 sensitivity | PASS, sensitivity only, not admitted |
| conservation identity | PASS, restricted domain |
| interval subdivision study | PASS, restricted domain |
| exact-zero one-sided continuity | PASS, no B1 redefinition |
| independent numerical review | PASS |
| natural E1 reachability | PASS |
| natural loaded-event materiality | PASS for mineral N, limitation recorded |
| documented `HETOP` input range | PASS, `[0.0 ... 0.2] m` confirms zero is in documented range |
| implementation order frozen for production | FAIL_CLOSED |
| complete routed child domain | FAIL_CLOSED, `Hetop=0` accepted/documented but unqualified |
| zero-thickness semantics | FAIL_CLOSED_UNRESOLVED |
| normal B2 route | FAIL_CLOSED_UNAVAILABLE |
| GOV02 historical-uncertainty route | FAIL_CLOSED_NOT_ELIGIBLE |
| formal child disposition carrier | FAIL_CLOSED_UNRESOLVED |
| independent B3 disposition review | FAIL_CLOSED_NOT_PERFORMED |

## 10. Decision

The positive-`Hetop`, observed-natural-envelope binary64 numerical policy is qualified and independently reviewed. That is a real advance from B3I05.

The complete TCD-042-E1 child is nevertheless not B3 admission-ready. The current decision is

`PARTIAL_TCD042_E1_CLASS_E_READINESS_POSITIVE_HETOP_POLICY_QUALIFIED_FULL_CHILD_DOMAIN_AND_ADMISSION_ROUTE_FAIL_CLOSED`.

The blockers are independent of each other:

1. the routed child trigger still contains source-accepted and documentation-listed `Hetop=0`, outside the NQ03 qualified domain;
2. historical B2 is unavailable and GOV02 acquisition closure is not complete, so neither admission route is open;
3. the existing formal B3 disposition schema does not directly encode the B3I05 child atom key without losing atomicity;
4. any future B3 disposition still needs its own independent second-line review;
5. production binding must carry the NQ03R evaluation-order constraint.

No corrected-legacy admission, numerical-policy B3 admission, production implementation or parent TCD-042 admission is made by B3E01.

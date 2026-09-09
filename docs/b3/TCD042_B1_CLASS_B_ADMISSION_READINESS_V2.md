# ANIMO-B3B02 - TCD-042-B1 Exact-Zero Upper-Boundary Reservoir Algebra Admission Readiness, domain-refined closeout

Status: `PARTIAL_TCD042_B1_CLASS_B_READINESS_HETOP_ZERO_DOMAIN_UNRESOLVED_ROUTE_AND_REVIEW_FAIL_CLOSED`

Date: 2026-09-09

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-b3b02-tcd042-b1-class-b-readiness`

Target: `TCD-042-B1`

Class: `B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`

Requested trigger: `Flpn = 0 AND Flux = 0`

This document supersedes the qualification boundary stated in `TCD042_B1_CLASS_B_ADMISSION_READINESS.md`. The earlier dossier remains valid evidence for the exercised positive-`Hetop` domain, but its unqualified readiness wording was too broad because frozen revision-53 input validation accepts `Hetop = 0`.

No production source is modified. No admission is made.

## 1. Frozen identity and authority

The claim remains pinned to:

- B0 source archive SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- B0 testbank SHA256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 documentation SHA256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`;
- `ANIMO_4.1.5.53/UBoundconc.for` SHA256 `b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7`.

Upstream authorities remain:

- UBQ01 head `6895b67799f26888025eced7188e7190b2a0d07d` for exact-zero source, analytical, synthetic and natural B1 evidence;
- B3Q01 head `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54` for fail-closed admission rules;
- GOV02 head `db7add6f9561730bbf352aa7fd3f3968405cfaa3` for evidence-route policy;
- SYNQ01 head `842f72300fd03ede0b9024537a7ee6126722a121`, with no direct TCD-042 oracle registered;
- B3I05 head `7fa0162415e02a6f0167e71b48ae38177a9e06e0` for canonical child routing.

B3I05 remains authoritative that `TCD-042` is the parent and that its children are `TCD-042-B1` and `TCD-042-E1`. No `TCD-043` is created here.

## 2. Exact legacy algebra

For `Flpn = 0`, frozen `UBoundconc.for:110-149` computes

```text
Flux = Max(0.0, Flib(1) + Rurv)
```

and, when `Flux >= 1.0d-8`, uses

```text
P  = St * Flux / Hetop
A1 = exp(-P)
A2 = (1-A1) / Flux
B1 = (1-A1) / P
B2 = (1-B1) / Flux

C1   = A1*C0 + A2*Load
Cavg = B1*C0 + B2*Load
```

For `Flux < 1.0d-8`, including exact zero, legacy instead uses

```text
A1 = 1
A2 = 0
B1 = 1
B2 = 0
```

so at exact zero

```text
C1   = C0
Cavg = C0
```

regardless of nonzero load.

The source applies the same coefficient family to the existing upper-reservoir concentration families. The natural Ruurlo witness directly exercises NH4 and NO3 only.

## 3. Positive-`Hetop` exact-zero limit

For `Hetop > 0`, the positive-flow expression is the solution of the existing reservoir balance

```text
Hetop * dC/dt = Load - Flux*C.
```

With

```text
P = St*Flux/Hetop
```

the mathematically unique `Flux -> 0` limit is

```text
A1 = 1
A2 = St/Hetop
B1 = 1
B2 = St/(2*Hetop)
```

and therefore

```text
C1   = C0 + Load*St/Hetop
Cavg = C0 + Load*St/(2*Hetop).
```

For `Hetop > 0`, this is an exact limit, not a threshold approximation and not a tolerance-based choice.

The corresponding control-volume identity is

```text
Hetop*C1 = Hetop*C0 + St*Load - St*Flux*Cavg.
```

At exact zero this becomes

```text
Hetop*C1 = Hetop*C0 + St*Load.
```

The legacy fallback omits exactly `St*Load` from represented end storage when `Load != 0`.

Same-step exported mass remains exactly zero because

```text
St*Flux*Cavg = 0.
```

## 4. Closeout discovery: frozen input grammar admits `Hetop = 0`

A source-level recheck of the same hash-pinned B0 archive found an admission-domain issue that UBQ01 did not need to resolve for its exercised cases.

Frozen `input1.for:1826-1829` reads and validates `Hetop` with a lower bound of exactly zero:

```text
Read(Uiso,*,Err=7000) Hetop, He(0)
rarg1 = 0.0; rarg2 = 0.2
Call Checkrea(Uoer,Error,Label,'Hetop ',Hetop,rarg1,rarg2)
```

`Checkrea` rejects a value only when `Value .Lt. Low`. Equality with the lower bound is accepted. Therefore the frozen grammar admits

```text
Hetop = 0.
```

This is material to the proposed Class-B algebra because the positive-`Hetop` zero-flow limit contains `St/Hetop` and `St/(2*Hetop)`.

At `Hetop = 0`, the recovered differential equation degenerates to

```text
0 = Load - Flux*C.
```

For the B3B02 trigger `Flux = 0`:

- if `Load != 0`, the equation becomes inconsistent as a finite concentration-storage balance;
- if `Load = 0`, the equation does not determine concentration evolution;
- the expressions `St/Hetop` and `St/(2*Hetop)` are undefined.

Consequently, the unique exact-zero limit is qualified only on the domain `Hetop > 0`. It is not a globally defined correction over every configuration accepted by the frozen input validator.

## 5. Why this changes readiness, not UBQ01's positive-`Hetop` evidence

UBQ01's natural Ruurlo witness has

```text
Hetop = 0.02 m.
```

The supplied frozen testbank cases inspected for this closeout likewise use positive `Hetop`, with the observed testbank value `0.02 m` in the exercised profiles. Thus the analytical formula, synthetic exact-zero oracle and natural Ruurlo first-difference evidence remain applicable to the domain they actually exercise.

What changes is the admission-readiness boundary. B3Q01 requires the affected path and residual uncertainty to be explicit. A candidate that is undefined for an accepted input value cannot be called ready for the full requested trigger without either:

1. proving from an authoritative higher-level contract that `Hetop = 0` is outside admissible model semantics despite the parser accepting it; or
2. separately qualifying the zero-thickness semantics and its safe treatment.

B3B02 does neither. It therefore fails closed on the full trigger domain.

## 6. Atomic correction candidate that is currently qualified only as a subdomain hypothesis

For `Hetop > 0`, the narrow candidate remains:

```text
IF Flpn == 0 AND Flux == 0 THEN
    A1 = 1
    A2 = St / Hetop
    B1 = 1
    B2 = St / (2 * Hetop)
ELSE
    preserve existing legacy behavior in this workunit
END IF
```

This is a semantic candidate only. It is not implemented here.

B3B02 does not authorize adding `Hetop > 0` as a new production branch condition. Doing so would itself encode a policy for the zero-thickness configuration and therefore needs explicit qualification rather than silent insertion.

## 7. Natural activation and exact controls

UBQ01's B0-hash-pinned natural diagnostic probe remains the direct B1 witness.

At Ruurlo `TITO = 1915`:

```text
Flpn = 0
Flux = 0
St = 1 d
Hetop = 0.02 m
NH4 Load = 5.069031338e-7 kg/m2/d
NO3 Load = 1.68034188e-7 kg/m2/d
```

The first baseline/candidate difference occurs exactly at TITO 1915. All 1,914 prior accepted trace records are bitwise identical. The only direct coordinates that differ at the first difference are

```text
Rsconhtop
Rsconitop
Avconhtop
Avconitop
```

and all four corrected binary64 values are bitwise equal to the analytical predictions.

The exact negative controls remain:

- exact-zero, zero-load TITO 10: bitwise unchanged;
- ordinary positive-flow TITO 1 with `Flux = 0.0024002409999999996`: bitwise unchanged;
- forcing and hydrology at TITO 1915: unchanged;
- beginning upper-reservoir state at TITO 1915: unchanged;
- immediate layer-1 state at TITO 1915: unchanged;
- later layer-1 chemistry first appears among differences at TITO 1917, after propagation through the existing accepted-state path.

Comparison is exact bitwise. No numerical tolerance is used.

GitHub Actions run `34365508588` independently confirms the UBQ01 integrated validator and scope guard passed on tested head `87171f13e2492e8f467bc456c2a90564b54ffe5c`.

## 8. Affected and unchanged surfaces for the qualified positive-`Hetop` subdomain

Directly affected under `Flpn=0`, `Flux=0`, `Hetop>0`, `Load!=0`:

```text
Delta(C1)   = Load*St/Hetop
Delta(Cavg) = Load*St/(2*Hetop).
```

Expected unchanged at the activation step:

- hydrology and external forcing;
- `Load`, `St`, `Hetop` and beginning `C0`;
- same-step reservoir solute export, because `Flux=0`;
- immediate soil-layer state unless reached through another existing path;
- exact-zero, zero-load behavior in the exercised positive-`Hetop` control;
- ordinary positive-flow behavior;
- all finite-positive `0 < Flux < 1.0d-8` behavior in this workunit;
- all `Flpn != 0` behavior;
- the legacy threshold and all tolerance policy;
- parent `TCD-042` status and `TCD-042-E1` status.

Later differences are allowed only as causal descendants of the changed accepted upper-reservoir storage.

No expected-difference statement is made for `Hetop = 0`. That domain is unresolved and fail closed.

## 9. TCD-042-E1 remains separate

Nothing in this refinement changes the finite-positive seam.

B3B02 still excludes

```text
0 < Flux < 1.0d-8.
```

No threshold is changed. No tolerance or epsilon is introduced. No cancellation-safe finite-positive evaluation is selected. Those questions remain exclusively `TCD-042-E1` Class-E work.

The `Hetop = 0` discovery is therefore not evidence for E1 and does not compose B1 and E1.

## 10. SYNQ01 applicability

SYNQ01 has no registered direct TCD-042 oracle. B3B02 therefore continues to rely on the dedicated UBQ01 exact-zero analytical and synthetic oracle for this atom.

Synthetic evidence is not B2.

## 11. Admission-route state remains fail closed

The live PREP02R state remains without a provenance-qualified historical B2 reference for this path. The received 2026 executable is a modern native rebuild and cannot substitute for historical B2. The historical-uncertainty route is also not eligible because the documented acquisition closure required by GOV02 is incomplete.

Thus:

```text
NORMAL_B2_AVAILABLE = false
INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY eligible = false
```

No route is passed by B3B02.

## 12. Independent review remains fail closed

No independent second-line B3 admission review has been performed for B3B02.

Any later review must now explicitly assess not only the exact-zero derivation and Ruurlo causal evidence, but also the `Hetop = 0` accepted-input domain and whether a higher-level semantic contract legitimately excludes it.

Until then:

```text
independent_review = FAIL_CLOSED_PENDING
```

## 13. Revised readiness matrix

| Gate | Result |
| --- | --- |
| frozen B0 identity | PASS |
| canonical child routing | PASS |
| exact legacy expression | PASS |
| exact trigger identified | PASS |
| positive-`Hetop` zero-flow limit | PASS |
| positive-`Hetop` conservation identity | PASS |
| natural Ruurlo activation | PASS, mineral-N scope |
| exact negative controls | PASS |
| local non-interference | PASS, exercised mineral-N positive-`Hetop` scope |
| expected-difference envelope | PASS for `Hetop > 0` |
| finite-positive E1 separation | PASS |
| threshold unchanged | PASS |
| tolerance absent | PASS |
| full legacy input-domain coverage | FAIL_CLOSED |
| `Hetop = 0` semantics | FAIL_CLOSED_UNRESOLVED |
| normal B2 route | FAIL_CLOSED_UNAVAILABLE |
| GOV02 historical-uncertainty route | FAIL_CLOSED_NOT_ELIGIBLE |
| independent second-line review | FAIL_CLOSED_PENDING |

## 14. Revised decision

The prior broad readiness decision is superseded by:

```text
PARTIAL_TCD042_B1_CLASS_B_READINESS_HETOP_ZERO_DOMAIN_UNRESOLVED_ROUTE_AND_REVIEW_FAIL_CLOSED
```

Qualified:

- exact legacy algebra;
- existing reservoir ownership;
- unique exact-zero limit for `Hetop > 0`;
- exact positive-`Hetop` conservation identity;
- atomic positive-`Hetop` correction hypothesis;
- affected and unchanged surface contract for that subdomain;
- natural Ruurlo NH4/NO3 activation;
- exact negative controls;
- bounded causal propagation;
- strict separation from `TCD-042-E1`.

Not qualified:

- a correction over the complete requested trigger domain `Flpn=0 AND Flux=0` because revision-53 input accepts `Hetop=0`;
- zero-thickness reservoir semantics;
- historical B2 truth;
- GOV02 historical-uncertainty admission route;
- independent B3 admission review;
- corrected-legacy admission;
- production migration;
- parent `TCD-042` admission.

The positive-`Hetop` subdomain is scientifically ready for later route and review work. The complete TCD-042-B1 trigger is not yet admission-ready and remains fail closed.

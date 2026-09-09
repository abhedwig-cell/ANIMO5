# ANIMO-B3B02 — TCD-042-B1 Exact-Zero Upper-Boundary Reservoir Algebra Admission Readiness

Status: `QUALIFIED_TCD042_B1_ATOMIC_CLASS_B_READINESS_ROUTE_AND_REVIEW_FAIL_CLOSED`

Date: 2026-09-09

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-b3b02-tcd042-b1-class-b-readiness`

Target: `TCD-042-B1`

Class: `B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`

Trigger: `Flpn = 0 AND Flux = 0`

This workunit assembles and qualifies the atomic Class-B admission-readiness dossier for the exact-zero upper-boundary reservoir algebra. It does not admit corrected legacy, does not admit parent `TCD-042`, and does not modify production source.

## 1. Frozen identities and evidence authority

The scientific claim is pinned to the frozen B0 archive and testbank already used by UBQ01:

- source archive SHA256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 user-guide SHA256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`;
- frozen source member `ANIMO_4.1.5.53/UBoundconc.for` SHA256: `b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7`.

Authoritative upstream evidence used here:

- UBQ01 exact-zero qualification head `6895b67799f26888025eced7188e7190b2a0d07d`;
- B3Q01 scientific-admission framework head `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- GOV02 evidence-DAG / historical-uncertainty policy head `db7add6f9561730bbf352aa7fd3f3968405cfaa3`;
- SYNQ01 synthetic-oracle head `842f72300fd03ede0b9024537a7ee6126722a121`, used only to check whether a separately registered TCD-042 oracle exists;
- B3I05 canonical child-routing head `7fa0162415e02a6f0167e71b48ae38177a9e06e0`.

B3I05 is the base of this branch because it is the latest qualified authority for the child split. It keeps `TCD-042` as the canonical parent and routes this atom as `TCD-042-B1`, separate from `TCD-042-E1`.

## 2. Atomic scope

In scope is one claim only:

> For the existing upper-reservoir response with `Flpn = 0` and exactly `Flux = 0`, the legacy fallback coefficients omit the unique zero-flow limit of the already implemented positive-flow reservoir solution. The exact-zero algebra can therefore be corrected locally, without changing the threshold, numerical policy, reservoir ownership, hydrology, or any finite-positive branch.

Explicitly out of scope:

- `TCD-042-E1`, including every case `0 < Flux < 1.0d-8`;
- any change to the legacy `1.0d-8` branch threshold;
- any floating-point tolerance or epsilon;
- a general upper-boundary redesign;
- any change to the `Flpn != 0` ponding path;
- production source modification;
- corrected-legacy admission;
- parent `TCD-042` admission;
- any claim that UBQ01 or UBQ02 provides B2 historical-reference evidence.

## 3. Exact legacy source expression

UBQ01 pins the relevant source to `UBoundconc.for:110-149` on the frozen B0 member above. For `Flpn = 0`, the implemented reservoir response first defines

```text
P = St * Flux / Hetop
```

For the ordinary positive-flow solution the coefficients are

```text
A1 = EXP(-P)
A2 = (1 - A1) / Flux
B1 = (1 - A1) / P
B2 = (1 - B1) / Flux
```

and the state response is

```text
C1   = A1 * C0 + A2 * Load
Cavg = B1 * C0 + B2 * Load
```

where `C0` is the beginning upper-reservoir concentration, `C1` its accepted end concentration, `Cavg` its time-average concentration over the step, `Load` the areic solute loading rate, `St` the time-step length, `Hetop` the reservoir thickness, and `Flux` the water throughflow.

The legacy sub-threshold fallback, which also contains exact zero because the source test is `Flux < 1.0d-8`, sets

```text
A1 = 1
A2 = 0
B1 = 1
B2 = 0
```

Thus, at exactly `Flux = 0`, legacy gives

```text
C1   = C0
Cavg = C0
```

regardless of a non-zero `Load`.

This workunit does not alter or qualify the finite-positive behavior of that fallback.

## 4. Mathematically unique `Flux -> 0` limit

The positive-flow expression is the exact solution of the existing well-mixed reservoir balance

```text
Hetop * dC/dt = Load - Flux * C.
```

Let

```text
P = St * Flux / Hetop.
```

Using the exact limits

```text
lim(P->0) exp(-P) = 1
lim(P->0) (1-exp(-P))/P = 1
lim(P->0) (1-(1-exp(-P))/P)/P = 1/2
```

the unique zero-flow coefficients are

```text
A1 = 1
A2 = St / Hetop
B1 = 1
B2 = St / (2 * Hetop)
```

and therefore

```text
C1   = C0 + Load * St / Hetop
Cavg = C0 + Load * St / (2 * Hetop).
```

This is not a chosen numerical approximation. It is the exact `Flux -> 0` limit of the same reservoir equation already used for positive flow.

## 5. Exact conservation identity

For the positive-flow solution, the step-integrated control-volume identity is

```text
Hetop * C1 = Hetop * C0 + St * Load - St * Flux * Cavg.
```

At exactly `Flux = 0`, this reduces exactly to

```text
Hetop * C1 = Hetop * C0 + St * Load.
```

Substituting the unique zero-flow state gives equality identically:

```text
Hetop * (C0 + Load*St/Hetop)
= Hetop*C0 + St*Load.
```

The legacy fallback instead gives `Hetop*C1 = Hetop*C0`; when `Load != 0`, the omitted storage increment is exactly `St*Load`.

Because `Flux = 0`, the same-step exported solute mass `St*Flux*Cavg` remains exactly zero under both legacy and candidate algebra. The defect is therefore local storage response, not a same-step transport-flux redefinition.

## 6. Proposed atomic algebraic correction

The admission candidate is deliberately narrower than the existing threshold branch:

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

This is a semantic patch description only. No production source is changed on B3B02.

The candidate must not be implemented by replacing `Flux < 1.0d-8`, changing its threshold, or treating finite-positive values as zero. Those actions belong to the separately routed `TCD-042-E1` numerical-policy atom.

## 7. Existing state ownership

UBQ01 source-bound evidence establishes that this algebra acts on the already existing upper-boundary reservoir, not a new state model. The persistent upper-reservoir owner includes:

- reservoir thickness `Hetop`;
- beginning-state concentrations `Conhtop`, `Conitop`, `Codiormatop`, `Codiornitop`, `Copotop`, `Codiorpotop`;
- accepted end-state counterparts `Rs*top`;
- time-average counterparts `Av*top`.

The user guide independently describes `HETOP` as the thickness of the virtual reservoir from which fertilizer additions leach and documents initial virtual-top-layer concentrations. The code-bound owner and acceptance mapping remain authoritative for this readiness claim.

## 8. Directly affected surfaces

For an exact-zero step with non-zero loading, the only direct algebraic differences are the loaded upper-reservoir solute-family end and average concentrations:

```text
Delta(C1)   = Load * St / Hetop
Delta(Cavg) = Load * St / (2 * Hetop).
```

The source ownership is species-generic across the six upper-reservoir concentration families recorded by UBQ01. The natural Ruurlo witness, however, directly activates only the mineral-N subset. This dossier does not turn that one natural witness into an execution claim for every species family.

The accepted `Rs*top` state can become the next-step beginning `Con*top` state through the existing acceptance path. Consequently, later downstream chemistry may legitimately diverge after the corrected stored mass is subsequently transported or transformed.

## 9. Expected unchanged surfaces

The atomic candidate is required to leave the following unchanged:

- all records before the first exact-zero, non-zero-load activation;
- hydrological forcing and water fluxes;
- `Load`, `St`, `Hetop`, and beginning `C0` at the activation step;
- same-step exported solute mass at exact zero, because `Flux*Cavg = 0` exactly;
- immediate soil-layer chemistry at the activation point unless reached through another existing path;
- exact-zero steps with `Load = 0`;
- ordinary positive-flow behavior;
- every finite-positive case `0 < Flux < 1.0d-8` in this workunit;
- all `Flpn != 0` behavior;
- all thresholds and tolerances;
- source/testbank identity;
- parent `TCD-042` status and the separate `TCD-042-E1` status.

Any candidate that violates one of these surfaces is no longer the B3B02 atomic claim and must fail closed.

## 10. Natural Ruurlo activation

UBQ01 provides a B0-hash-pinned diagnostic execution witness on the natural Ruurlo case. It is diagnostic B1 evidence, explicitly not B2.

At `TITO = 1915`:

```text
Flpn = 0
Flux = 0
Pr = 0.0002000407 m/d
St = 1 d
Hetop = 0.02 m
Coprnhyn = 0.002534 kg/m3
Coprniyn = 0.00084 kg/m3
```

The corresponding loads are

```text
NH4 Load = 5.069031338e-7 kg/m2/d
NO3 Load = 1.68034188e-7 kg/m2/d
```

and the booked mineral-N input is

```text
0.005069031338 + 0.00168034188
= 0.006749373218 kg/ha/d.
```

The independent observer nonclosure recorded by UBQ01 is

```text
0.0067493732130969875 kg/ha N,
```

which identifies the same missing-storage scale without introducing a tolerance.

Under the isolated exact-zero candidate, the first baseline/candidate difference occurs exactly at `TITO = 1915`. The direct state changes are:

```text
NH4 end increment = 2.534515669e-5 kg/m3
NO3 end increment = 8.4017094e-6 kg/m3
NH4 average increment = 1.2672578345e-5 kg/m3
NO3 average increment = 4.2008547e-6 kg/m3.
```

The formula predictions are bitwise reproduced by the diagnostic probe.

## 11. Negative controls and non-interference

UBQ01's isolated candidate probe supplies the following exact negative controls:

1. Ruurlo records through `TITO = 1914` are bitwise identical between baseline and candidate.
2. At the activation record `TITO = 1915`, forcing, hydrology, beginning upper-reservoir state, and immediate layer-1 state are unchanged. Only the expected mineral-N upper-reservoir `Rs*top` and `Av*top` surfaces differ.
3. An exact-zero, zero-load control at `TITO = 10` remains bitwise identical.
4. An ordinary positive-flow control at `TITO = 1`, with `Flux = 0.0024002409999999996`, remains bitwise identical.
5. No numerical tolerance is used in these equality checks.

Observed descendant propagation is also bounded: the next step inherits the corrected upper-reservoir end state, and layer-1 chemistry first appears among the differences only later, at `TITO = 1917`. This is consistent with stored mass propagating through existing transport, not with a direct same-step layer-1 rewrite.

These controls qualify local non-interference for the exercised natural mineral-N path. They do not establish historical B2 equivalence and do not prove all-species integrated non-interference by themselves.

## 12. Expected-difference envelope

The admissible difference envelope for a future implementation is:

| Situation | Expected difference |
| --- | --- |
| before first exact-zero non-zero-load activation | none |
| `Flpn=0`, `Flux=0`, `Load=0` | none |
| `Flpn=0`, `Flux=0`, `Load!=0` | only direct upper-reservoir `C1` and `Cavg` according to the exact formulas above |
| same activation step, water and external forcing | none |
| same activation step, solute export through this reservoir | none, because `Flux=0` |
| later steps | only causal descendants of the corrected accepted upper-reservoir storage may differ |
| `0<Flux<1.0d-8` | none in B3B02; reserved to `TCD-042-E1` |
| ordinary positive flow | none |
| `Flpn!=0` | none |

A full-output comparison is therefore not expected to stay bitwise identical after a natural activation, because the purpose of the candidate is to retain mass that legacy drops and that retained mass can later enter existing chemistry. The required invariant is causal containment, not blanket trajectory identity after activation.

## 13. SYNQ01 applicability

Live SYNQ01 evidence was checked. Its registered TCD coverage contains TCD-015, TCD-017, TCD-018, TCD-019, TCD-023, TCD-024, and TCD-025, but no `TCD-042` row.

Therefore:

- B3B02 does not claim a direct SYNQ01 TCD-042 oracle;
- SYNQ01 does not supply B2;
- the dedicated exact-zero analytical/synthetic oracle qualified within UBQ01 is the applicable causal oracle for this atom.

This distinction prevents accidental promotion of general synthetic-oracle infrastructure into evidence it does not contain.

## 14. B3Q01 Class-B readiness mapping

The atomic evidence now satisfies the readiness-side Class-B questions as follows:

| Class-B question | B3B02 evidence state |
| --- | --- |
| exact trigger and path identified | PASS, `Flpn=0 AND Flux=0` |
| violated identity identified | PASS, exact upper-reservoir control-volume conservation |
| intended local algebra identifiable | PASS, unique `Flux->0` limit |
| proposed correction atomic | PASS, exact-zero coefficients only |
| affected state surfaces bounded | PASS |
| affected flux surfaces bounded | PASS, same-step reservoir export unchanged at exact zero |
| natural B1 activation | PASS for Ruurlo NH4/NO3 |
| negative controls | PASS for pre-activation, zero-load, and ordinary positive-flow controls |
| local non-interference | PASS within exercised natural mineral-N scope |
| threshold/tolerance policy unchanged | PASS by workunit contract |
| finite-positive numerical seam excluded | PASS, routed to `TCD-042-E1` |
| historical B2 route | FAIL_CLOSED, unavailable |
| GOV02 no-B2 route entry | FAIL_CLOSED, not eligible |
| independent second-line admission review | FAIL_CLOSED, not yet performed |

This is enough to qualify an atomic admission-readiness dossier. It is not enough to admit the correction.

## 15. Route gate, live and fail closed

The live PREP02R state remains:

```text
PARTIAL_RECOVERY_WINDOWS_NATIVE_CAPTURE_READY_HISTORICAL_REFERENCE_STILL_BLOCKED
```

Material route facts are:

- `normal_B2_reference_available = false`;
- `historical_reference_artifact_obtained = false`;
- `reference_qualified = false`;
- `historical_uncertainty_route_eligible = false`;
- the narrowed WUR archival/provenance request has not been sent;
- the received 2026 native executable is classified as a modern rebuild, not as historical B2 truth.

GOV02 therefore forbids using the historical-uncertainty route at this time. B3B02 records this as a hard route failure, not as an administrative TODO that can be waived.

## 16. Independent review gate

No independent second-line B3 admission review is performed by this workunit. A later admission packet must obtain a reviewer who is independent of the evidence assembly and must explicitly assess at least:

- atomicity of the `Flux=0` claim;
- correctness and uniqueness of the limit derivation;
- conservation identity;
- affected and unchanged surfaces;
- the Ruurlo activation and negative-control interpretation;
- separation from `TCD-042-E1`;
- validity of the selected B2 or GOV02 route at that later time.

Until such a review exists, the review gate remains `FAIL_CLOSED`.

## 17. Qualification decision

Decision:

```text
QUALIFIED_TCD042_B1_ATOMIC_CLASS_B_READINESS_ROUTE_AND_REVIEW_FAIL_CLOSED
```

Qualified here:

- exact legacy algebra and exact-zero defect;
- mathematically unique zero-flow limit;
- exact conservation identity;
- atomic correction contract;
- direct affected and expected-unchanged surfaces;
- natural Ruurlo mineral-N activation;
- exact negative controls;
- bounded expected-difference envelope;
- local non-interference within the exercised scope;
- strict separation from `TCD-042-E1` and parent `TCD-042`.

Not qualified or admitted here:

- historical B2 truth;
- GOV02 historical-uncertainty route entry;
- independent B3 admission review;
- corrected-legacy admission;
- production migration;
- finite-positive numerical policy;
- parent `TCD-042` admission.

The admissible next state is therefore readiness only. Admission remains fail closed until a valid evidence route and independent review are both present.

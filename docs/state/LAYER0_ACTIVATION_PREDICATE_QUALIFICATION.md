# ANIMO-STATEQ01 layer-0 activation predicate qualification

Status: `SOURCE_QUALIFIED_ACTIVATION_PREDICATES_RESTRICTED_CORE_GUARD_REFINED`

Frozen source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Scope

This source audit qualifies the revision-53 predicates that make layer 0 participate in ordinary dissolved-solute transport. It refines the `CORE_CNP_SUBSURFACE_ONLY` application envelope. It does not change legacy thresholds or claim that layer 0 is a separately selectable feature.

## 2. Hydrology sets the transport activation flag

For detailed hydrology, `Hydro_detailed.for:111-118` sets:

```fortran
If((Pnt+Snt).Gt.1.0d-4 .Or. (Pn+Snla).Gt.1.0d-4) Then
   Flpn = 1
Else
   Flpn = 0
End If
Mofro(0) = Amax1(0.0,(Pn+Snla)  / He(0))
Mofrt(0) = Amax1(0.0,(Pnt+Snt) / He(0))
```

Thus detailed-hydrology layer-0 transport activation depends on both current/start and end/result surface water-equivalent storage. Snow terms `Snla/Snt` participate in the predicate and in the layer-0 moisture coordinate.

For aggregated hydrology, `Hydro_aggregated.for:74-84` defines nonnegative ponding from `Wale/Walet` and sets `Flpn=1` when either `Pn` or `Pnt` exceeds `1.0d-4`.

## 3. `Flpn` determines whether layer 0 enters the standard transport sequence

`MODFLUX.FOR:69-75` begins the transport sequence at:

```fortran
Ln = 1 - Flpn
```

`TRANSPORT.FOR:129-134` independently uses:

```fortran
K1 = 1-Flpn
Cob(K1) = Cotop
K = K1
```

The same `1-Flpn` boundary is used in the phosphorus transport path. Therefore, for ordinary C/N/P dissolved transport, `Flpn=1` makes layer 0 part of the active transport domain; `Flpn=0` starts the domain at soil layer 1.

This is the source-qualified central activation predicate.

## 4. Same-step additions have a second direct layer-0 predicate

`Addit.for:342-366` routes dissolved management additions directly to layer 0 when `Wyad(I)=0` and current liquid ponding satisfies:

```fortran
Pn > 1.0d-4
```

Otherwise the dissolved mass is placed in the `Con*top` upper-boundary reservoir.

Under the hydrology source domain, a strict restricted-core guard that excludes positive layer-0 surface storage also excludes this direct-addition route. Merely checking `Flpn=0` is weaker because legacy permits small positive surface storage below the `Flpn` threshold.

## 5. Upper-boundary reservoirs are core continuation, not an optional add-on

`UBoundconc.for:110-168` evolves `Conhtop/Conitop/Codiormatop/Codiornitop/Copotop/Codiorpotop` when `Flpn=0` and flushes them into the active upper boundary when `Flpn=1`.

`TRANSPORT.FOR:129-130` uses the passed `Cotop` value as the concentration boundary for the first active transport compartment. When `Flpn=0`, that first compartment is soil layer 1.

Therefore the `Con*top/Rscon*top` family remains continuation-critical even inside a subsurface-only profile. It must not be treated as a separate optional feature merely because no layer-0 compartment is active.

The previous `CORE_CNP_WITH_ADDITION_RESERVOIRS` profile distinction is withdrawn by this audit.

## 6. Dry deposition does not weaken the guard

`UBoundconc.for:62-69` routes dry NH4/NO3 deposition to soil layer 1 if `Flpn=0` or `(Pn+Snla)<1.0d-3`, and to layer 0 only when `Flpn=1` and `(Pn+Snla)>=1.0d-3`.

A restricted profile that requires no positive layer-0 surface storage therefore prevents the dry-deposition layer-0 route as well.

## 7. Correct restricted-core guard

A robust source-bound restricted-core envelope is stronger than the legacy `Flpn` threshold.

At every accepted boundary and for every bound hydrology end frame that could become accepted:

### Aggregated hydrology

```text
Pn  == 0
Pnt == 0
```

### Detailed hydrology

```text
Pn   + Snla == 0
Pnt  + Snt  == 0
```

In addition:

- restart/input layer-0 solute coordinates must be zero or otherwise handled by a separately admitted general-core restore contract;
- no profile transition may become accepted if the next hydrology frame creates positive layer-0 storage;
- top/upper-boundary reservoirs remain part of the restricted-core checkpoint state;
- no residual layer-0 mass may be discarded, projected into the top reservoir or mapped to the unadmitted SQ01 continuation state.

The equality requirement is an application-envelope invariant, not a replacement for the legacy `1.0d-4` process threshold. It is deliberately stricter so the restricted profile does not hide physically nonzero low-storage state below the legacy activation threshold.

## 8. Fail-before-mutate placement

The guard can be evaluated after the exact hydrology frame for the candidate interval has been bound and before chemistry/management mutation begins.

A trial must fail closed if either the accepted start frame or candidate end frame violates the zero-surface-storage envelope. Such a trial cannot be promoted to accepted state under `CORE_CNP_SUBSURFACE_ONLY`.

## 9. Remaining qualification

The activation predicate itself is now source-qualified. Still open:

- executable fail-closed sentinel implementation/test;
- uninterrupted versus split-run qualification inside the envelope;
- management cursor continuation;
- the independent layer-0 restart initialization finding documented separately;
- general surface-capable state admission, including TCD-016-C1.

Final classification:

`SOURCE_QUALIFIED_LAYER0_ACTIVATION_AND_RESTRICTED_CORE_GUARD_REFINED`

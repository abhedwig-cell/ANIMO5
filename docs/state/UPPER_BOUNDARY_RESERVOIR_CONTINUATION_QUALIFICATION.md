# ANIMO-STATEQ01 upper-boundary reservoir continuation qualification

Status: `SOURCE_QUALIFIED_ACCEPTED_BOUNDARY_OWNER_AND_TRANSPORT_FEED_RC_R12_EXECUTION_OPEN`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

This audit qualifies the continuation role of the revision-53 upper-boundary C/N/P reservoirs for the restricted `CORE_CNP_SUBSURFACE_ONLY` candidate. It answers four narrow questions:

1. what is the accepted-boundary owner;
2. what is merely a start-of-step alias or interval-average derived value;
3. whether the reservoir feeds the first active soil compartment when `Flpn=0`;
4. what must round-trip for RC-R12.

Evidence is source-bound to frozen ANIMO 4.1.5 revision 53 SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

No source or testcase bytes were changed.

## 1. State lifecycle across accepted boundaries

`Animo.for:262-295` calls `Init` at the start of every timestep before hydrology and process execution.

Except for the first timestep, `Init.for:322-337` performs the direct lifecycle transfer:

```text
Conhtop       <- Rsconhtop
Conitop       <- Rsconitop
Codiormatop   <- Rscodiormatop
Codiornitop   <- Rscodiornitop
Copotop       <- Rscopotop       when P is active
Codiorpotop   <- Rscodiorpotop   when P is active
```

and then clears the `Rs*top` work/result coordinates before the new interval is evaluated.

This establishes two source roles rather than two independent physical owners:

- `Con*top`: start-of-current-interval alias;
- `Rs*top`: end-of-current-interval accepted-boundary value.

A modern checkpoint should not serialize both as independent mutable state. At an accepted boundary the candidate owner payload is the `Rs*top` value, or an equivalent canonical field with the same physical meaning. Restore constructs the next start alias from that owner.

## 2. Initial input and restart output are lifecycle-compatible

`input1.for:3197-3218` reads initial `Conhtop` and `Conitop` from `INITIAL.INP`.

`input1.for:3263-3286` reads `Codiormatop` and `Codiornitop`.

For P-active configurations, `input1.for:3321-3325` or `3367-3376` reads `Copotop` depending on P initialization mode, while `input1.for:3390-3394` reads `Codiorpotop`.

The restart writer uses the end-state side of the lifecycle instead. `Output_Init.for:82-87` writes `Rsconhtop` and `Rsconitop`; `Output_Init.for:102-105` writes `Rscodiormatop` and `Rscodiornitop`; P-active output writes `Rscopotop` and `Rscodiorpotop` at `Output_Init.for:121-134`.

Thus the legacy text restart itself already embodies the end-state-to-next-start mapping. It is not evidence that both `Con*top` and `Rs*top` should be independently checkpointed.

## 3. Physical storage meaning

`Hetop` is read from the profile geometry input at `input1.for:1819-1829` and is not a dynamic reservoir state coordinate in these routines.

The legacy balances represent reservoir material as concentration times `Hetop`:

- final NH4 and NO3 upper-boundary storage: `Rsconhtop*Hetop` and `Rsconitop*Hetop` at `Outbal_calc.for:1173-1179`;
- final DON upper-boundary storage: `Rscodiornitop*Hetop` at the same location;
- final DOM upper-boundary storage: `Rscodiormatop*Hetop` at `Outbal_calc.for:688-699`;
- final PO4 and DOP upper-boundary storage: `Rscopotop*Hetop` and `Rscodiorpotop*Hetop` at `Outbal_calc.for:1585-1590`.

Candidate canonical storage identity therefore requires the bound geometry/configuration identity containing `Hetop`. The mutable state coordinate can remain concentration because the corresponding physical amount is deterministic only under that immutable geometry binding.

## 4. Restricted-core update rule

`Animo.for:499-518` calls `UBoundconc` after management mutation and before transport.

For `Flpn=0`, `UBoundconc.for:110-150` computes a residence-time update. With

```text
Flux = max(0, Flib(1) + Rurv)
```

and, for `Flux >= 1e-8`,

```text
P  = St*Flux/Hetop
A1 = exp(-P)
A2 = (1-A1)/Flux
B1 = (1-A1)/P
B2 = (1-B1)/Flux
```

it derives for every active species family:

```text
end concentration     Rs*top = Con*top*A1 + Load*A2
interval-average      Av*top = Con*top*B1 + Load*B2
```

For `Flux < 1e-8`, the source sets `A1=B1=1` and `A2=B2=0`, so both end and average concentration equal the current `Con*top` exactly.

The external load terms are assembled at `UBoundconc.for:72-99` from precipitation, irrigation, runon and input-boundary concentrations according to hydrology mode.

The `Av*top` coordinates are therefore interval-derived quantities. They are not independent accepted-boundary owners.

## 5. Management mutation precedes the reservoir update

The ordering matters. `Animo.for:456-490` processes the current management addition and calls `Addit` before `UBoundconc`.

Inside `Addit`, when the surface is not ponded under its legacy threshold route, dissolved additions are placed directly into the upper-boundary reservoirs: `Conitop`, `Conhtop`, `Copotop`, `Codiormatop`, `Codiornitop` and `Codiorpotop` at `Addit.for:342-372`.

Ploughing explicitly includes reservoir material in the mixed amount at `Addit.for:448-470` and subsequently empties all six top-reservoir start coordinates at `Addit.for:691-697`.

Consequently a correct split/restart contract must preserve process ordering. A checkpoint cannot restore a pre-management reservoir value after the corresponding management event cursor has already advanced.

## 6. The interval-average reservoir concentration feeds layer 1 when `Flpn=0`

The general transport routine sets:

```text
K1 = 1-Flpn
Cob(K1) = Cotop
```

at `TRANSPORT.FOR:129-131`. Therefore `Flpn=0` makes compartment 1 the first active transport compartment and uses the supplied top concentration as its incoming boundary concentration.

The main program passes:

- `Avconhtop` into NH4 transport at `Animo.for:810-823`;
- `Avconitop` into NO3 transport at `Animo.for:846-859`;
- `Avcodiormatop`, `Avcodiornitop` and `Avcodiorpotop` through `Transca` at `Animo.for:736-756`, with the corresponding `Transport` calls at `Transca.for:97-120`, `151-174` and `185-208`;
- `Avcopotop` into `Transgen` at `Animo.for:887-903`, where `Transgen.for:212-215` sets `Cob(1-Flpn)=Avcopotop`.

Upper-boundary reservoirs are therefore core continuation state for the restricted profile. They are not a management-only optional feature.

## 7. RC-R12 checkpoint contract

For the restricted profile the candidate accepted-boundary checkpoint must retain these mutable owner values:

```text
upper_boundary.nh4 = Rsconhtop
upper_boundary.no3 = Rsconitop
upper_boundary.dom = Rscodiormatop
upper_boundary.don = Rscodiornitop
upper_boundary.po4 = Rscopotop       if P active
upper_boundary.dop = Rscodiorpotop   if P active
```

and bind immutable geometry/configuration identity that fixes at least `Hetop`, P activation and the normalized external-input schemas used to derive loads.

Restore must construct the next-step `Con*top` aliases from these values before any management or upper-boundary mutation. It must not restore stale `Av*top` values, because those are recomputed for the new interval.

## 8. Numerical and evidence boundary

The nonzero-flux source rule contains `exp(-P)`. STATEQ01 does not invent a local numeric comparison tolerance for RC-R12. Full nonzero-flux uninterrupted-versus-split equivalence must use the admitted numerical comparison policy.

A narrower exact synthetic sentinel can nevertheless test lifecycle wiring without touching this numerical question by using the source branch `Flux < 1e-8` with nonzero reservoir concentration and zero external load. In that branch source semantics give exactly:

```text
Rs*top = Con*top
Av*top = Con*top
```

Such a sentinel can prove that a nonzero accepted-boundary owner round-trips and feeds the first compartment, but it remains synthetic contract evidence rather than revision-53 split-run evidence.

## Result

Source-level RC-R12 ownership and feed semantics are now qualified:

`SOURCE_QUALIFIED_ACCEPTED_BOUNDARY_OWNER_AND_TRANSPORT_FEED_RC_R12_EXECUTION_OPEN`

What remains is executable split continuity. The next safe step is an exact no-flux, nonzero-reservoir synthetic wiring sentinel, followed later by a profile-clean real split-run under the admitted numerical policy.

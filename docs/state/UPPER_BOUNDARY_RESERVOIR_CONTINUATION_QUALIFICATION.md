# ANIMO-STATEQ01 upper-boundary reservoir continuation qualification

Status: `SOURCE_QUALIFIED_FROZEN_SOURCE_COMPONENT_RC_R12_PASS_FULL_MODEL_SPLIT_RUN_OPEN`

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

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

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

This establishes three source roles:

- `Con*top`: start-of-current-interval alias;
- `Rs*top`: end-of-current-interval accepted-boundary value;
- `Av*top`: interval-average derived transport boundary.

A modern checkpoint should not serialize these as independent mutable owners. At an accepted boundary the candidate owner payload is the `Rs*top` value, or an equivalent canonical field with the same physical meaning. Restore constructs the next start alias from that owner. `Av*top` is recomputed for the new interval.

## 2. Initial input and restart output are lifecycle-compatible

`input1.for:3197-3218` reads initial `Conhtop` and `Conitop` from `INITIAL.INP`.

`input1.for:3263-3286` reads `Codiormatop` and `Codiornitop`.

For P-active configurations, `input1.for:3321-3325` or `3367-3376` reads `Copotop` depending on P initialization mode, while `input1.for:3390-3394` reads `Codiorpotop`.

The restart writer uses the end-state side of the lifecycle instead. `Output_Init.for:82-87` writes `Rsconhtop` and `Rsconitop`; `Output_Init.for:102-105` writes `Rscodiormatop` and `Rscodiornitop`; P-active output writes `Rscopotop` and `Rscodiorpotop` at `Output_Init.for:121-134`.

Thus the legacy text restart already embodies the end-state-to-next-start mapping. This is restart-intent evidence only. It does not establish `INITIAL.OUT` as a canonical checkpoint format.

## 3. Physical storage meaning

`Hetop` is read from profile geometry input and is not a dynamic reservoir state coordinate in these routines.

The legacy balances represent reservoir material as concentration times `Hetop`, including final NH4, NO3, DOM, DON, PO4 and DOP upper-boundary storage.

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

For `Flux < 1e-8`, the source sets `A1=B1=1` and `A2=B2=0`.

The external load terms are assembled from precipitation, irrigation, runon and input-boundary concentrations according to hydrology mode.

The `Av*top` coordinates are therefore interval-derived quantities, not independent accepted-boundary owners.

## 5. Management mutation precedes reservoir update

The ordering matters. The current management addition is processed before `UBoundconc`.

`Addit` can place dissolved additions directly into `Conitop`, `Conhtop`, `Copotop`, `Codiormatop`, `Codiornitop` and `Codiorpotop`. Ploughing can include reservoir material in the mixed amount and subsequently clear the six top-reservoir start coordinates.

Consequently a correct split/restart contract must preserve process ordering. A checkpoint cannot restore a pre-management reservoir value after the corresponding management event cursor has already advanced.

## 6. The interval-average reservoir concentration feeds layer 1 when `Flpn=0`

The general transport routine uses:

```text
K1 = 1-Flpn
Cob(K1) = Cotop
```

Therefore `Flpn=0` makes compartment 1 the first active transport compartment and uses the supplied top concentration as its incoming boundary concentration.

The main program passes `Avconhtop`, `Avconitop`, the DOM/DON/DOP upper-boundary averages through `Transca`, and `Avcopotop` through `Transgen`.

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

Restore must construct the next-step `Con*top` aliases from these values before any management or upper-boundary mutation. It must not restore stale `Av*top` values.

## 8. Exact synthetic RC-R12 sentinel

A qualification-only exact sentinel used the source `Flux < 1e-8` branch, further restricted to zero flux and zero external load, with deliberately nonzero reservoir concentrations. Under this branch:

```text
Rs*top = Con*top
Av*top = Con*top
```

`tools/stateq01/upper_boundary_reservoir_wiring_harness.py` represents concentrations and `Hetop` as exact rational `Fraction` values. GitHub Actions run `34335620989`, job `102414197663`, executed the persisted harness at head `d19cc018dc67636b9d3501a88e63cc7499bbf6c2` under CPython 3.12.14. All 10 tests passed.

The sentinel verifies exact accepted-owner round trip, first-compartment feed wiring, single ownership, exact amount calculation and fail-closed geometry/P-activation mismatch. It is `SYNTHETIC_SOURCE_BRANCH_CONTRACT_NON_B2` evidence and does not execute revision-53 physics.

## 9. Frozen-source nonzero-flux component probe

STATEQ01 subsequently executed the original hash-pinned `UBoundconc.for` itself with a qualification-only Fortran driver.

The probe uses:

- `Flpn=0`;
- detailed hydrology mode;
- P active;
- six nonzero initial top-reservoir concentrations: `2,3,4,5,6,7`;
- nonzero `Flux`;
- nonzero external load terms.

Three two-interval component paths were compared:

1. uninterrupted component lifecycle, where first-step `Rs*top` is promoted to the second-step `Con*top`;
2. explicit split/restore, where the six first-step `Rs*top` values are captured and restored before interval two;
3. an omission sentinel, where those six checkpoint values are deliberately replaced by zero before interval two.

The probe was executed with GNU Fortran 14.2.0 at `-O0` under both compiler default REAL and the separate `-fdefault-real-8` qualification variant.

For both build variants independently:

```text
uninterrupted final reservoir vector == split/restore final reservoir vector  exactly
omitted-checkpoint final reservoir vector != uninterrupted final vector
```

The default-REAL uninterrupted/split final vector was:

```text
1.514901876449585
2.160053014755249
2.5053133964538574
3.129020929336548
3.900608777999878
4.3541669845581055
```

The default-REAL-8 qualification variant also produced exact uninterrupted-versus-split equality within that build, although its absolute floating values differ from the default-REAL build. STATEQ01 does not interpret that cross-build difference as a numerical discrepancy and does not invent a tolerance to reconcile it.

Machine-readable evidence, source hashes and executable hashes are persisted in:

`integration/animo-state/UPPER_BOUNDARY_RESERVOIR_SOURCE_PROBE.json`

The reusable driver and local hash-checking runner are persisted at:

- `tests/stateq01/fixtures/stateq01_rc12_upper_boundary_probe.f90`
- `tools/stateq01/run_rc12_upper_boundary_source_probe.py`

This evidence class is `B0_HASH_PINNED_SOURCE_COMPONENT_EXECUTION_NOT_B2`. It is stronger than the synthetic wiring sentinel because frozen revision-53 source is executed, but it is still not a complete ANIMO uninterrupted-versus-restart run.

The probe does not prove the historical Intel default-REAL build contract. The two compiler variants are qualification probes only.

## Result

RC-R12 advances to:

`PASS_FROZEN_SOURCE_COMPONENT_CONTINUITY_FULL_MODEL_SPLIT_RUN_OPEN`

The six active upper-boundary reservoir values are checkpoint-mandatory continuation state. Explicit restoration reproduces the uninterrupted second-step `UBoundconc` result within each tested build; deliberate omission changes that result.

Remaining RC-R12 boundary:

- full profile-clean ANIMO uninterrupted-versus-split execution remains open;
- canonical serialization precision remains open;
- combined event/crop/report continuation at the same split remains open;
- B2 historical-reference comparison remains unavailable;
- canonical STATE remains `NOT_ADMITTED`.

No production code or physics was changed.
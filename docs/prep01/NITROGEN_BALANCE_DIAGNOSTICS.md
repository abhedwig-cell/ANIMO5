# Nitrogen balance diagnostics

Status: `SOURCE_BOUND_NO3_NEGATIVE_CONCENTRATION_REKO_DEFECT_CAUSALLY_CONFIRMED_NH4_CAUSE_OPEN`.

This note records PREP01 diagnostic evidence only. The frozen ANIMO source and frozen testcases are not modified.

## 1. LWKM NO3 annual residual

The deterministic GNU diagnostic execution reports the largest NO3-N balance-period deviation in:

- case: `LWKM_gras_1040.2021.2045`;
- balance file: `baniGP.Out`;
- year: 1997;
- TITO: 2557;
- annual residual: `+0.5760503022407 kg/ha N`.

An instrumented copy of `TRANSPORT.FOR` was used to emit the source's layer/timestep quantities `BAPD` (processes) and `BATR` (transport + storage). Summing `BAPD-BATR` over the corresponding 1997 profile and transport steps gives:

`+0.5760503022406 kg/ha N`

which matches the annual `Bani(Ddev)` residual to floating-point noise. The annual residual is therefore localized to the legacy `TRANSPORT` mass-balance seam and is not an artefact of `Outbal_calc` or formatted balance output.

## 2. Dominant local event

The annual residual is not a smooth accumulation. One event dominates:

- TITO: `2312`;
- layer: `1`;
- substance: `NITRATE`;
- `BAPD = -8.4267311478156e-4 kg/m2`;
- `BATR = -9.0054430498043e-4 kg/m2`;
- `BAPD-BATR = +5.7871190198869e-5 kg/m2`;
- equivalent profile contribution: `+0.5787119019887 kg/ha N`.

Other events partially compensate this amount, giving the annual `+0.5760503022407 kg/ha N` residual.

The frozen legacy code itself reports this event in `message.out` as:

`subr. TRANSPORT: deviation in massbalance >5.0 % concerning substance NITRATE`

with TITO 2312, layer 1 and the same rounded `BAPD`/`BATR` values.

## 3. Exact `Transsub` branch at TITO 2312

Source-consistent diagnostic instrumentation of `Transsub.for` shows that the main ANIMO transport call enters analytical solution branch `Iflsol=1` with:

- start concentration `Co = 9.8366822861654e-2 kg/m3`;
- `Mto = 0.350588`, `Mt = 0.385095`;
- layer thickness `Ld = 0.05 m`;
- timestep `St = 10 d`;
- `Hv = (Mt-Mto)/St = 3.4507e-3 d-1`;
- `Hv1 = 6.4698353471977e-2 d-1`;
- initial `Reko = -1.8671499776003e-3 kg/m3/d`;
- pre-clipping analytical `Rsc = -1.7678655437962e-3 kg/m3`.

Because negative concentrations are not admitted for this call, `Transsub` enters its negative-concentration protection branch. It sets the final concentration to approximately `1e-12` and recomputes the zero-order term. The legacy recomputation is:

```text
Reko = (Mt*Rsc - Mto*Co)/St
     - (-Avc*Hv1 + inflow_per_volume)
```

At this event it returns:

`Reko = -1.6853462295631e-3 kg/m3/d`.

## 4. Confirmed algebraic mass-accounting defect

The `Hv1` coefficient already contains the moisture-change term `Hv`:

```text
Hv1 = outflow/ld + root_uptake/ld + first_order_terms + Hv
```

But the first term in the `Reko` correction already uses the complete storage change `(Mt*Rsc-Mto*Co)/St`. Reusing full `Hv1` therefore counts the `Hv` contribution a second time when `Reko` is reconstructed after clipping.

For TITO 2312 the exact spurious mass term is:

```text
Avc * Hv * St * Ld
= 5.7871190198869e-5 kg/m2
= 0.5787119019887 kg/ha
```

This is numerically identical to `BAPD-BATR` to floating-point roundoff. The local NO3 mass nonclosure is therefore explained exactly by the extra `Avc*Hv` term in the negative-concentration `Reko` reconstruction.

The conservative algebraic form uses the disappearance/outflow coefficient without the storage derivative:

```text
Avc * (Hv1 - Hv)
```

rather than `Avc*Hv1` in that reconstruction.

Classification: `CONFIRMED_LEGACY_CODE_DEFECT` for local mass conservation in the negative-concentration adjustment branch. This classification is source- and equation-bound and does not depend on assuming a particular acceptable legacy residual tolerance.

## 5. Causal correction probe

A temporary execution-only source copy was changed at exactly this expression from `Hv1` to `(Hv1-Hv)`. The frozen source remained unchanged.

For TITO 2312, layer 1:

- corrected `Reko = -1.8010886099609e-3 kg/m3/d`;
- `BAPD = -9.0054430498043e-4 kg/m2`;
- `BATR = -9.0054430498043e-4 kg/m2`;
- `BAPD-BATR = -1.08e-19 kg/m2`.

For the 1997 LWKM GP NO3 balance, the period residual changes from approximately:

`+5.76e-1 kg/ha N`

to:

`+2.28e-7 kg/ha N`.

The baseline diagnostic run emits three `TRANSPORT` mass-balance warnings for nitrate in this case, including TITO 2312, 3042 and 4513. The correction probe emits none. This is a causal diagnostic result, not yet an admitted corrected-legacy patch.

## 6. Legacy warning contract

`TRANSPORT.FOR` warns only when both conditions are true:

- relative difference exceeds `Help1 = 0.05` (5%);
- absolute difference exceeds `Help2 = 1e-5 kg/m2`, equivalent to `0.1 kg/ha` for one layer event.

The TITO-2312 event exceeds both criteria. Therefore the observed annual NO3 envelope must not be interpreted as an ordinary acceptable numerical tolerance. It contains an event that the legacy model itself classifies as mass-balance nonclosure.

## 7. Qualification consequence

The `+0.576 kg/ha N` diagnostic maximum is evidence of a correctable legacy nonclosure, not an acceptance threshold. A future qualification policy must distinguish:

- floating-point or discretization-scale closure;
- initialization/reset seams;
- locally detected transport nonclosure;
- physically justified ledger exchanges.

ANIMO5 must not adopt the largest legacy residual as its mass-balance tolerance. The corrected-legacy reference should retain explicit evidence of the original defect and independently qualify the correction before production migration.

## 8. NH4 follow-up

The largest diagnostic NH4-N residual remains:

- case: `Puitmijn_Cranendonck_60`;
- file: `banhL1.Out`;
- year: 2006;
- residual: approximately `+0.139 kg/ha N`.

The earlier instrumented Puitmijn attempt used a different path/staging layout than the successful deterministic diagnostic case. The successful case tree is still available, including the converted `input/swap.bun` and compatibility filename aliases. The next audit step is therefore to clone that exact successful runtime tree, instrument it in place, and determine whether the NH4 residual is caused by the same negative-concentration `Reko` branch or a different ledger seam.

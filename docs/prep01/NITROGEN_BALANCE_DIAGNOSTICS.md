# Nitrogen balance diagnostics

Status: `SOURCE_BOUND_DIAGNOSTIC_NO3_TRANSPORT_NONCLOSURE_LOCALIZED_NH4_CAUSE_OPEN`.

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

## 3. Legacy warning contract

`TRANSPORT.FOR` warns only when both conditions are true:

- relative difference exceeds `Help1 = 0.05` (5%);
- absolute difference exceeds `Help2 = 1e-5 kg/m2`, equivalent to `0.1 kg/ha` for one layer event.

The TITO-2312 event exceeds both criteria. Therefore the observed annual NO3 envelope must not be interpreted as an ordinary acceptable numerical tolerance. It contains an event that the legacy model itself classifies as mass-balance nonclosure.

## 4. Current causal boundary

The nonclosure is now localized to the `TRANSPORT`/`Transsub` calculation path for nitrate in layer 1 at TITO 2312.

The source still requires causal discrimination between:

- one of the analytical-solution branches selected by `Iflsol`;
- the dry/wet special-case paths;
- zero-order production (`Reko`) adjustment used to avoid negative concentrations;
- the later negative-concentration clipping/return logic;
- another mismatch between the state/flux quantities used by `Transsub` and those used in the subsequent `BAPD`/`BATR` check.

No one of these branches is yet classified as the cause until an instrumented source-consistent run records the exact branch and values at TITO 2312.

## 5. Qualification consequence

The `+0.576 kg/ha N` diagnostic maximum is evidence of a legacy nonclosure event, not an acceptance threshold. A future qualification policy must distinguish:

- floating-point or discretization-scale closure;
- initialization/reset seams;
- locally detected transport nonclosure;
- physically justified ledger exchanges.

ANIMO5 must not simply adopt the largest legacy residual as its mass-balance tolerance.

## 6. NH4 follow-up

The largest diagnostic NH4-N residual remains:

- case: `Puitmijn_Cranendonck_60`;
- file: `banhL1.Out`;
- year: 2006;
- residual: approximately `+0.139 kg/ha N`.

A separate instrumented rerun exposed a runtime/input-path discrepancy relative to the earlier successful diagnostic execution. That route must be reproduced exactly before the NH4 residual is causally analysed, otherwise the audit would compare a different runtime configuration.

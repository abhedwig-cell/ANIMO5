# ANIMO-GHG09: TCD-034 selector sensitivity & parameter-transfer qualification

## Scope

GHG09 consumes the exact green GHG08 parent-readiness synthesis and owns only `TCD034_MODEL_EVOLUTION_SELECTOR_SENSITIVITY_AND_PARAMETER_TRANSFER`.

It introduces no new selector, no production source change, no calibration values and no admission. Its purpose is to turn one GHG08 material gap into a bounded analytical contract: how a change in plant-growth temperature selector propagates through `fGrow`, plant-mediated CH4 transfer and existing parameters.

Exact predecessor: `ANIMO-GHG08@97913b04906eb23c28b47a68ec9def7392174be5`.

## Growth-response function

For selector temperature `T`, start temperature `Tgr = Tegr`, and `Tmat = Tgr + 10 degC`, the frozen source response is represented as

`g(T)=0` for `T <= Tgr`

`g(T)=4*(1-((Tmat-T)/10)^2)` for `Tgr < T < Tmat`

`g(T)=4` for `T >= Tmat`.

The function is continuous. In the active transition interval,

`dg/dT = 0.08*(Tmat-T)`.

Therefore `0 <= dg/dT <= 0.8`, and the complete piecewise function is globally Lipschitz with constant `0.8 per degC`:

`|g(Ta)-g(Tb)| <= 0.8*|Ta-Tb|`.

This is a mathematical sensitivity bound, not an empirical uncertainty bound.

## Propagation into the plant pathway

For rooted layer `i`, with nonnegative phase-storage factor `S_i`, methane concentration `C_i` and layer thickness `He_i`,

`Kraw_i = Kpl * FvegCH4 * fRoot_i * g(T)`

and

`Qplant_i = Kraw_i * S_i * C_i * He_i`.

With frozen `Kpl=0.24 d-1`, two selector values `Ta` and `Tb` therefore satisfy

`|Delta Kraw_i| <= 0.192 * FvegCH4 * fRoot_i * |Ta-Tb|`

and

`|Delta Qplant_i| <= 0.192 * FvegCH4 * fRoot_i * S_i * C_i * He_i * |Ta-Tb|`.

The same propagation applies to profile totals after summation of nonnegative layer terms.

`PvCH4Ox` does not control total `Qplant`. It only partitions that total:

`Qox = PvCH4Ox*Qplant`

`Qem = (1-PvCH4Ox)*Qplant`.

Consequently a selector-induced change in total plant-mediated transfer cannot be compensated by changing `PvCH4Ox`; that parameter changes the split, not the total.

## Parameter-transfer consequences

`Kpl` and `FvegCH4` multiply `g(T)`. At one isolated state where both old and new growth factors are positive, a multiplicative compensation can be written formally as a scale factor `g_old/g_new`. That fact does **not** establish transferable calibration.

A single multiplicative scale cannot in general compensate a selector change over multiple temperature states because `g_old/g_new` varies with temperature and can become singular when one selector is below `Tegr` while the other is active. The selector change can also move a state between OFF, TRANSITION and MATURE branches.

Changing `Tegr` is not a neutral calibration compensation either. `Tegr` shifts the onset threshold and, through `Tmat=Tegr+10`, the entire nonlinear response interval. Adjusting it to absorb selector differences would redefine scientific process semantics rather than merely rescale a coefficient.

Therefore existing values of `Tegr`, `FvegCH4` and `Kpl` must not be presumed transferable from revision-53 selector behavior to the GHG06A fixed-depth T50 selector. `PvCH4Ox` remains transferable only with respect to its bounded partition role, not as a compensator for total plant transfer.

## Qualified implications

GHG09 qualifies the following bounded conclusions:

- selector-temperature differences propagate continuously into `fGrow` with absolute sensitivity bounded by `0.8 per degC`;
- near the growth onset, relative sensitivity can be arbitrarily large because the denominator `g(T)` approaches zero;
- selector changes can activate or deactivate plant transfer by crossing `Tegr`;
- selector changes can move a state into or out of the mature plateau;
- no single global rescaling of `Kpl*FvegCH4` can generally reproduce the old response across varying temperature states;
- `Tegr` adjustment is a semantic change to the response function, not a harmless calibration scaling;
- `PvCH4Ox` cannot compensate total plant-transfer differences because it only partitions `Qplant`.

## What this does not close

GHG09 does not quantify how often or how strongly `Te(Nuroup+1)` and the GHG06A T50 operator differ in real or frozen-reference simulations. It therefore narrows, but does not close, the GHG08 application-envelope gap.

It also does not determine revised parameter values. The remaining calibration question is empirical/application-specific: whether existing parameter values remain acceptable when the selector is changed, and if not, how they should be re-estimated.

## Decision

The bounded result is:

`QUALIFIED_TCD034_SELECTOR_SENSITIVITY_AND_PARAMETER_NONTRANSFERABILITY_RISK_V1`.

The GHG08 calibration gap is reduced from an undefined gap to a qualified non-transferability risk plus a still-open empirical recalibration/validation requirement. The application-envelope difference gap remains open and should next be addressed by a frozen-reference or otherwise representative selector-replay study.

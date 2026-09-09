# NH4 dry-down mass-ledger seam in the surface layer

Status: `CONFIRMED_LEGACY_LOCAL_MASS_LOSS_CORRECTION_POLICY_REQUIRES_EXPLICIT_DRY_SOLUTE_STATE`.

This note records diagnostic evidence against the frozen Puitmijn testcase and supplied revision-53 source. The frozen source and testcase are unchanged.

## Event

The largest deterministic diagnostic NH4-N balance-period deviation occurs in `Puitmijn_Cranendonck_60`, `banhL1.Out`, year 2006:

`+0.139 kg/ha N`.

The legacy `message.out` identifies a matching local `TRANSPORT` warning at TITO 1490, layer 0, for `AMMONIUM` in both the potential and main ANIMO transport calls. In the main call:

- `BAPD = 0`;
- `BATR = -1.3880242022597072e-5 kg/m2`;
- local difference = `+1.3880242022597072e-5 kg/m2`;
- equivalent = `+0.13880242022597072 kg/ha N`.

This accounts for essentially the full annual residual.

## Exact dry-down branch

At TITO 1490, layer 0, the main NH4 `Transsub` call has:

- analytical solution class `Iflsol = 2`;
- initial concentration `Co = 0.12767937602481674 kg/m3`;
- initial water content `Mto = 5.435585e-4 m3/m3`;
- final water content `Mt = 1.628217e-5 m3/m3`;
- layer thickness `Ld = 0.2 m`;
- timestep `St = 1 d`;
- leaving water flux `Fu = 4.1184400265397315e-10 m/d`;
- evaporation-related flux `Fev = 1.05455e-4 m/d`;
- zero-order source `Reko = 0`;
- first-order source `Reki = 0`;
- sorption terms are zero for this surface layer event.

The remaining dissolved NH4 mass at the beginning of the dry-down solve is:

```text
Mto * Ld * Co
= 1.3880242022597072e-5 kg/m2
= 0.13880242022597072 kg/ha
```

The source uses `Factor=100` for layer 0 and enters the dry-down branch because the water storage crosses its dry threshold. The branch sets `Rsc=0`. It only transfers the remaining solute mass to the leaving-water flux when `Fu > 1e-6 m/d`. Here `Fu` is positive but far below that threshold, so for `Iflsol=2` the branch also sets `Avc=0` and returns. The entire remaining dissolved mass is therefore removed from the represented state without a corresponding ledger transfer.

Classification: `CONFIRMED_LEGACY_CODE_DEFECT` for local mass conservation.

## One-step retention probe

A temporary, event-specific diagnostic change retained the dissolved mass in the tiny remaining water volume by setting `Rsc=Mto*Co/Mt`. This closes `TRANSPORT` at TITO 1490 exactly, but does not solve the model-level issue.

At TITO 1491, `Init` correctly carries the retained concentration forward. The next hydrologic state has `Mt=0`. The subsequent NH4 transport call then zeroes the concentration because no liquid-water volume remains. The same `0.1388024 kg/ha` therefore disappears one timestep later. This demonstrates that the legacy state representation has no explicit dry-solute reservoir for this path.

## Outflow-conservation probe

A second temporary event-specific probe used the source's existing layer-0 export formula for any positive `Fu`, rather than only `Fu > 1e-6`.

Result at TITO 1490:

- `Rsc = 0`;
- `Avc = 3.37026688094305e4 kg/m3`;
- exported mass `Toou = 1.3880242022597072e-5 kg/m2`;
- solution-storage change `-1.3880242022597072e-5 kg/m2`;
- `BAPD-BATR = 0`.

The 2006 `banhL1.Out` period deviation falls from approximately `+0.139 kg/ha N` to `-6.62e-10 kg/ha N`, and the NH4 `TRANSPORT` mass-balance warning disappears.

This is strong causal evidence that the `Fu > 1e-6` branch threshold is the immediate reason the legacy ledger loses mass.

However, the resulting flux concentration is about `3.37e4 kg/m3`. That is not a credible general production representation of solute transport. The water leaving the layer is extremely small; most water disappears through evaporation, which must not remove dissolved NH4. Forcing all remaining solute through the tiny `Fu` flux repairs accounting but creates an extreme concentration artifact.

## Architectural interpretation

The mass-conservation defect and the correct future representation must be kept separate.

The legacy model has no explicit state for solute mass remaining when a surface liquid-water compartment dries completely. A robust ANIMO5 state model should therefore represent one of the following explicitly, after theory reconciliation:

- a dry surface solute/residue store that can redissolve when water returns;
- an explicitly justified transfer to another conserved surface phase;
- another physically documented conservative dry-down state.

It should not silently destroy the mass and should not rely on arbitrarily huge flux concentrations merely to force ledger closure.

The eventual corrected-legacy reference may use a minimal compatibility correction, but that correction must be scientifically qualified separately from the ANIMO5 state design.

## Qualification consequence

The observed `+0.139 kg/ha N` residual is not a candidate mass-balance tolerance. It is a deterministic, source-localized mass-loss event that the legacy model itself warns about.

Qualification must separately test:

1. local transport closure;
2. conservation across wet-to-dry and dry-to-wet state transitions;
3. surface-residue continuation across timesteps;
4. absence of numerically pathological concentration spikes introduced solely to conserve mass;
5. profile and annual ledger closure after the local transition.

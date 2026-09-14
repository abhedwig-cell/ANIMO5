# ANIMO-GHG06A: TCD-034 bounded model-evolution T50 depth operator qualification

## Scope and authority

This workunit owns only `TCD034_T50_0P50M_DEPTH_OPERATOR_MODEL_EVOLUTION`. It starts from the exact green GHG06 closeout `ANIMO-GHG06@730f09f1567461a45bff4566368db05963b200fa` and does not rewrite the historical interpretation of revision-53 ANIMO.

Consumed authorities are pinned and read-only: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`, `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`, `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, `ANIMO-GOV06@7a7d3a1f5a5c07bf36b7e6e2915338dabde20660`, `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`, `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700` and `ANIMO-B3I10@942f26fe32eaf91679e59a1968ae173a3703e22d`.

Parallelism is `PARALLEL_AFTER_PINNING`. No production source, frozen B0, canonical TCD register, central B3 queue, aggregate authority, routing authority, production migration surface or central testbank registry is modified.

## Scientific starting point

GHG06 established two separate facts that must not be collapsed:

1. the current revision-53 expression is reconstructed as `Te(Nuroup+1)` under current standard Fortran semantics for the positive-root path, and this is not a stable fixed-depth coordinate;
2. the Walter-Heimann formulation fingerprint makes **daily mean soil temperature at 0.50 m depth** the strongly supported physical concept behind `Te50`, but not a historical ANIMO selector authority.

GHG06 therefore closed negatively because a fixed-depth physical quantity was not yet mapped to one exact ANIMO discretization rule. GHG06A is deliberately a model-evolution workunit. It is allowed to define a new bounded rule, but it may not relabel that rule as historical ANIMO truth.

## Frozen source geometry facts used by this design

The frozen revision-53 source manifest pins:

- `ghg_ch4.for` SHA-256 `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`;
- `Temper.for` SHA-256 `643e4460a897ec629068dc97ab4589a745304b8fa7adb7597dfadc1a9a9d41e5`;
- `Inicalc.for` SHA-256 `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`;
- `Input_hydro.for` SHA-256 `5f07ce68969d749308595d6b4f9f789b6b3646ae226c233e2f8e49565a7dad64`.

The source defines layer thickness `He` in metres, cumulative layer-bottom depth `Bo`, and midpoint depth

`z_i = Bo(i) - 0.5 * He(i)`.

`Temper` explicitly evaluates `Te(i)` at the middle of the layer. The external-hydrology route supplies `Te(1:Nl)` directly. GHG06 already established that `Te(0)` is not a safe universal substitute for a soil-temperature observation at depth and is therefore excluded from this operator.

## Qualified model-evolution operator v1

The new semantic target is:

`T50 := daily mean soil temperature represented at z* = 0.50 m below the soil surface`.

The bounded discrete operator is defined only from the current layer-centre temperature field and layer geometry.

For `i = 1..Nl`:

`Bo(i) = sum(He(1:i))`

`z_i = Bo(i) - 0.5 * He(i)`.

Preconditions:

- `Nl >= 1`;
- every `He(i)` is finite and strictly positive;
- every consumed `Te(i)` is finite;
- `z_i` is strictly increasing;
- the target depth is centre-bracketed: `z_1 <= 0.50 <= z_Nl`.

Evaluation:

- if `0.50 == z_i` in working precision, return `Te(i)`;
- otherwise choose the unique adjacent pair with `z_i < 0.50 < z_(i+1)` and set

`w = (0.50 - z_i) / (z_(i+1) - z_i)`

`T50 = (1-w) * Te(i) + w * Te(i+1)`.

No tolerance band, nearest-layer rule, containing-layer rule, root-depth rule or extrapolation is part of v1. If a precondition fails, the operator result is `UNAVAILABLE_FAIL_CLOSED`. A consumer must not silently fall back to `Te(Nuroup+1)`, `Te(1)`, `Te(0)` or another temperature.

## Why this particular rule is scientifically admissible as model evolution

The rule is deliberately modest. It does not assert that historical ANIMO used interpolation. It defines one new discretization of the already narrowed physical quantity.

Within its declared domain it has four useful properties that can be tested without empirical tuning:

- **root independence**: the value depends only on temperature and physical depth geometry, not on `Nuroup` or crop-root dynamics;
- **locality**: only the two adjacent temperature samples bracketing 0.50 m are consumed;
- **affine exactness**: if the represented temperature field is affine in depth, the operator returns the exact value at 0.50 m for any valid non-uniform bracketing mesh;
- **route neutrality**: the same operator consumes the final `Te(1:Nl)` field whether those values came from ANIMO's internal temperature model or the hydrological input route.

Linear interpolation is therefore not being promoted as historical evidence. It is selected as the minimum local reconstruction that preserves exact node values and affine depth profiles while avoiding dependence on crop state.

## Boundary semantics

The no-extrapolation rule is intentional. A physical profile may extend across 0.50 m while its first or last layer centre does not bracket that depth. GHG06A does **not** invent a surface or bottom boundary temperature to fill that gap. Such cases return `UNAVAILABLE_FAIL_CLOSED` even when 0.50 m lies inside the physical first or last compartment.

This makes the qualification bounded rather than universal. A later version may add a separately qualified boundary reconstruction, but doing so would be a semantic change and must not silently alter v1.

## State, transaction and restart semantics

`T50` is a derived per-time-step quantity. It is not conserved storage, persistent state, restart state or a new forcing. It is recomputed from the temperature field belonging to the same scientific candidate/time coordinate that consumes it.

No cached `T50` may cross a rejected candidate, retry, restart boundary or changed temperature field in a future transactional implementation. GHG06A does not implement that production architecture; it freezes the semantic requirement so later migration has an unambiguous target.

## Qualification evidence

The machine-readable contract is `integration/animo-ghg/GHG06A_TCD034_T50_OPERATOR_CONTRACT.json`. Synthetic oracles in `GHG06A_TCD034_T50_OPERATOR_ORACLES.json` test exact-node selection, non-uniform interpolation, affine-field invariance across two meshes, independence from root state, single-layer exact-centre behavior and fail-closed top/bottom/invalid-geometry cases.

These are **synthetic model-evolution oracles**. They are not B2 historical behavior and not a whole-model golden baseline.

## Decision

The bounded model-evolution result is:

`QUALIFIED_BOUNDED_MODEL_EVOLUTION_T50_DEPTH_OPERATOR_V1`.

The historical revision-53 selector remains:

`UNRESOLVED_NOT_HISTORICALLY_QUALIFIED`.

No B3 admission is performed here. No production use is authorized here. The operator becomes a scientific design authority only for later model-evolution qualification work that explicitly pins GHG06A.

## Next handoff

Because one exact model-evolution selector is now defined and qualified for its bounded domain, a separate `ANIMO-GHG07` may assess active `FvegCH4>0` reachability and positive-control behavior **against this model-evolution contract**. GHG07 must still distinguish synthetic/model-evolution evidence from historical B2 evidence and must fail closed for geometries where the v1 operator is unavailable.

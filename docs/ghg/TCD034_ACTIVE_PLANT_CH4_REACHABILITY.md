# ANIMO-GHG07: TCD-034 active plant-mediated CH4 reachability and positive-control qualification

## Scope and authority

This workunit consumes the exact green bounded selector authority `ANIMO-GHG06A@2573686af69a8d68a94010bb663272b35871a6e1` and owns only `TCD034_MODEL_EVOLUTION_ACTIVE_PLANT_CH4_REACHABILITY`.

It does not modify production source, frozen B0, the central TCD register, the B3 queue, aggregate or routing authority, or the central testbank registry. It does not convert the GHG06A model-evolution selector into historical revision-53 truth. Parallelism is `PARALLEL_AFTER_PINNING`.

The scientific question is narrow: once the GHG06A fixed-depth T50 operator is available, is the plant-mediated methane pathway algebraically reachable under valid positive inputs, does the vegetation switch behave as an actual switch, does the growth-temperature selector control the pathway in the expected bounded way, and does the plant oxidation/emission split conserve the plant-mediated methane removal term?

## Frozen source pathway reconstructed

Revision-53 source establishes the following bounded pathway:

1. `LnRoot=Nuroup` defines the current rooted domain.
2. Root mass is normalized over that domain. If the crop supplies effectively zero root mass, the source substitutes layer thickness over the root zone, giving an even depth-based fallback.
3. The plant growth factor is zero at and below `Tegr`, rises quadratically between `Tegr` and `Tegr+10 degC`, and is 4 at and above `Tegr+10 degC`.
4. For rooted layers, the unadapted plant transfer coefficient is `Kpl * FvegCH4 * fRoot * fGrow`, with `Kpl=0.24 d-1` in the frozen source.
5. The coefficient is multiplied by the local phase-storage factor used by the CH4 transport system.
6. The resulting plant-mediated CH4 removal is partitioned between plant oxidation and atmospheric emission by `PvCH4Ox` and `1-PvCH4Ox` respectively.

The revision-53 input parser constrains `FvegCH4` to 0..100 and `PvCH4Ox` to 0..1. The natural frozen GHG testcase has `FvegCH4=0`, so it cannot provide an active plant-mediated positive control. GHG07 therefore uses synthetic model-evolution controls rather than altering the frozen testbank.

## Relation to GHG06A

GHG07 replaces only the disputed selector input to the growth response with the already qualified GHG06A contract:

`T50 = TCD034_T50_0P50M_DEPTH_OPERATOR_V1(He, Te)`.

If that operator returns `UNAVAILABLE_FAIL_CLOSED`, the GHG07 positive-control harness also returns unavailable and does not fall back to root depth, nearest layer, containing layer, `Te(0)` or another temperature.

This is a model-evolution reachability test. It is not a production patch and not a claim that historical ANIMO executed the same T50 lookup.

## Algebraic invariants

For an active rooted layer `i`:

`fRoot_i = AmRo_i / ToRo * ToZr / He_i`

and therefore over the rooted domain:

`sum(fRoot_i * He_i) = ToZr`.

For the source's zero-root-mass fallback `AmRo_i=He_i`, this gives `fRoot_i=1` in every rooted layer.

Let `Kraw_i = 0.24 * FvegCH4 * fRoot_i * fGrow` and let `S_i` be the local phase-storage factor already used by the source. Then `Kplant_i = Kraw_i*S_i`. The bounded plant-mediated removal rate is

`Qplant_i = Kplant_i * AvCoCH4_i * He_i`.

The source partitions this term as

`Qox_i = PvCH4Ox * Qplant_i`

`Qem_i = (1-PvCH4Ox) * Qplant_i`.

Hence, for every active layer and for their sum,

`Qox + Qem = Qplant`.

GHG07 treats this identity as an atomic conservation oracle for the plant-mediated pathway only. It is not a whole-model carbon balance.

## Synthetic positive control

The principal active control uses four 0.25 m layers with layer-centre temperatures `[8, 10, 14, 16] degC`. The GHG06A operator interpolates `T50=12 degC`. With `Tegr=7 degC`, `fGrow=3`. The root zone contains the upper two layers with equal root mass, so `fRoot=1` in both. With `FvegCH4=0.5`, saturated phase fraction `0.4`, `AvCoCH4=0.1 kg C m-3` in each rooted layer, and `PvCH4Ox=0.25`, the source algebra gives:

- unadapted `Kraw=0.36 d-1` in each rooted layer;
- adapted `Kplant=0.144 d-1` in each rooted layer;
- total plant-mediated removal `0.0072 kg C m-2 d-1`;
- plant oxidation `0.0018 kg C m-2 d-1`;
- plant-mediated atmospheric emission `0.0054 kg C m-2 d-1`.

All are strictly positive. Their partition closes exactly to the removal term under the synthetic arithmetic.

## Negative and boundary controls

The permanent bounded oracle fragment also checks:

- `FvegCH4=0` gives zero plant-mediated transfer while leaving the selector otherwise available;
- `T50=Tegr` gives `fGrow=0` and zero plant-mediated transfer;
- `T50=Tegr+10` gives the saturated growth multiplier 4;
- `Nuroup=0` gives no rooted layers and zero plant-mediated transfer without a root-normalization divide;
- an unavailable GHG06A T50 geometry fails closed before active plant calculation;
- `PvCH4Ox=0` sends all plant-mediated removal to emission and none to plant oxidation;
- `PvCH4Ox=1` sends all plant-mediated removal to plant oxidation and none to emission;
- unequal root masses preserve the depth-weighted root normalization identity;
- zero supplied root mass in a positive root zone activates the source-equivalent thickness fallback and produces `fRoot=1` per rooted layer.

## Qualification boundary

GHG07 qualifies **synthetic active-path reachability and internal algebraic conservation** against the GHG06A model-evolution selector. It does not qualify:

- historical revision-53 T50 intent;
- empirical correctness of plant-mediated CH4 flux magnitude;
- whole GHG process behavior;
- CH4 transport solver coupling outside this bounded pathway;
- B2 historical behavior;
- B3 admission;
- production migration.

The correct evidence class is `SYNTHETIC_MODEL_EVOLUTION_POSITIVE_CONTROL_NOT_B2`.

## Decision

If all exact-head controls pass, the bounded result is:

`QUALIFIED_TCD034_MODEL_EVOLUTION_ACTIVE_PLANT_CH4_REACHABILITY_AND_PARTITION_V1`.

This closes the specific GHG06/GHG06A blocker that no `FvegCH4>0` positive control existed for the proposed selector pathway. It does not close historical TCD-034. Any later TCD-034 composition or B3 decision must state explicitly that the historical selector remains unresolved while a separate model-evolution contract is scientifically bounded and synthetically reachable.

# ANIMO-GHG01 - GHG restart and phase-state continuity audit

Status: `SOURCE_CONFIRMED_GHG_RESTART_PHASE_STATE_DISCONTINUITIES_REFERENCE_UNEXERCISED`

This post-closeout audit reconstructs the revision-53 greenhouse-gas continuation path through `INITIAL.OUT`. It distinguishes conservation of the serialized total gas-system concentration from behavioural continuity of the dissolved and gas-phase views used by the next simulation step. It does not claim historical executable behaviour, create a corrected restart format, or admit production migration.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant frozen source-file SHA-256 identities:

- `Output_Init.for`: `6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f`;
- `input1.for`: `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`;
- `Inicalc.for`: `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`;
- `Init.for`: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`;
- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`;
- `ghg_n2o.for`: `493bf88d4b321df64817a7c0eaa2725ad614a45df0a0f16cefa96ac348254175`;
- `ghgtransport.for`: `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`.

## 1. Serialized GHG owner state

`Output_Init.for:22-24` states that final model-profile results are written to `INITIAL.OUT`. When GHG is active, `Output_Init.for:155-165` writes:

- `>methan:` as `(RsCsCH4(Ln),Ln=0,Nl)`;
- `>nitoxi:` as `(RsCsN2O(Ln),Ln=0,Nl)`.

`input1.for:3429-3454` reads the same labels into `CsCH4(0:Nl)` and `CsN2O(0:Nl)`.

The serialized GHG quantity is therefore the total system concentration, not the dissolved concentration `Co` and not separate water/gas phase inventories.

This is consistent with the physical-state interpretation already used by GHG01 and ARCH02: one canonical system state may be sufficient if all derived phase views can be reconstructed deterministically from the accepted checkpoint coordinates.

## 2. Continuous-run continuation is different from INITIAL.OUT restore

For an uninterrupted simulation, `Init.for` accepts the previous result dissolved concentrations directly:

`CoCH4(Ln) = RsCoCH4(Ln)`

`CoN2O(Ln) = RsCoN2O(Ln)`

for `Ln=0..Nl` on continuation steps.

The `INITIAL.OUT` restore path is different. `Inicalc.for` reconstructs dissolved concentrations for soil layers from serialized total concentration using the reciprocal Bunsen coefficient evaluated at the fixed reference temperature `Terf`:

`ReBuTCH4 = 1 / AlfaBunsen('CH4',Terf)`

`ReBuTN2O = 1 / AlfaBunsen('N2O',Terf)`

`Co = Cs / (theta + ReBuT * (theta_sat-theta))`

where `theta=Mofro(Ln)` and `theta_sat=Mofrsa(Ln)`.

`Terf` is a model input reference temperature. It is not the accepted end-of-step soil temperature.

By contrast, the active CH4 and N2O routines later update their reciprocal Bunsen coefficients from actual average layer temperature `Te(Ln)` in `ghg_ch4.for:169-177` and `ghg_n2o.for:101-108`.

## 3. Source-algebraic restart phase-partition discontinuity

For one unsaturated layer define:

- `Cs` as the accepted total system gas concentration;
- `theta` as accepted water content;
- `a = theta_sat - theta` as air-filled pore volume;
- `r_prev` as the reciprocal Bunsen coefficient associated with the accepted pre-checkpoint gas state;
- `r_ref` as the reciprocal Bunsen coefficient evaluated at `Terf` during `Inicalc` restore.

The uninterrupted accepted dissolved state is represented by:

`Co_cont = Cs / (theta + r_prev*a)`.

The `INITIAL.OUT` restart reconstructs:

`Co_rst = Cs / (theta + r_ref*a)`.

Therefore:

`Co_rst / Co_cont = (theta + r_prev*a) / (theta + r_ref*a)`.

Exact phase-state continuity follows only when at least one of these holds:

1. `r_ref = r_prev`;
2. `a = 0`, so the layer is saturated;
3. the gas concentration is trivially zero.

For an unsaturated nonzero state at a checkpoint temperature different from `Terf`, the serialized total concentration can remain unchanged while the reconstructed dissolved and gas-phase concentrations change.

This is not an immediate total-mass-loss claim. It is a continuation-state discontinuity: the same total owner state is mapped to a different phase view at restart.

Local reconciliation key:

`GHG01-LCL-GHG-RESTART-PHASE-PARTITION`

Classification:

`SOURCE_CONFIRMED_RESTART_PHASE_STATE_RECONSTRUCTION_DISCONTINUITY_REFERENCE_UNEXERCISED`

## 4. Why the phase discontinuity can alter subsequent behaviour

The phase views are not passive output quantities.

Revision-53 GHG calculations use dissolved and gas concentrations in active kinetics and transport, including:

- CH4 oxidation;
- N2O production/reduction competition;
- gas and water diffusion;
- water advection;
- air-flow advection;
- CH4 plant transport and ebullition conditions.

Thus equality of serialized `Cs` alone is insufficient to prove behavioural restart equivalence.

The source `AlfaBunsen` function is strongly temperature dependent. As an analytical source-function sensitivity, reciprocal CH4 Bunsen coefficients are approximately 19.48 at 0 C, 30.54 at 25 C and 38.51 at 40 C. For N2O they are approximately 0.821, 1.670 and 2.415 at the same temperatures. These values show that replacing checkpoint-time phase partition with `Terf` partition is not algebraically negligible in general. They are not historical testcase results.

## 5. Separate layer-0 ponding reconstruction gap

The layer-0 path is stronger than the soil-layer phase-partition issue.

`Output_Init` serializes `RsCsCH4(0)` and `RsCsN2O(0)`, and `input1` reads them as `CsCH4(0)` and `CsN2O(0)`.

However, the GHG reconstruction block in `Inicalc.for` runs inside the soil-layer loop and calculates `CoCH4(Ln)` and `CoN2O(Ln)` only for `Ln=1..Nl`. After the loop it copies only `ReBuTCH4(1)` and `ReBuTN2O(1)` to index 0. No corresponding reconstruction of `CoCH4(0)` or `CoN2O(0)` from the serialized layer-0 state was found.

The active CH4 routine immediately evaluates `CaCH4(0)=ReBuTCH4(0)*CoCH4(0)` before transport.

Shared `GHGtransport` uses `Ln1=1-Flpn`. When ponding is active, `Ln1=0`. The routine overwrites `Co(0)` from atmospheric and layer-1 water only for a newly detected ponding event with `Pn<1.0e-4`. For already existing ponding, the saved layer-0 total concentration is not deterministically mapped to the runtime layer-0 dissolved concentration by this branch.

The source therefore contains a restart/initialization reconstruction gap for active pre-existing ponding.

Local reconciliation key:

`GHG01-LCL-GHG-PONDING-RESTART-LAYER0`

Classification:

`SOURCE_CONFIRMED_PONDING_GHG_LAYER0_RESTART_STATE_RECONSTRUCTION_GAP_REFERENCE_UNEXERCISED`

Historical runtime manifestation and numerical magnitude remain `REFERENCE_BLOCKED`. No claim is made that a historical executable produced any specific undefined value.

## 6. Continuous-run Bunsen update is a related but distinct issue

The CH4 and N2O routines contain commented old-state assignments immediately before updating the reciprocal Bunsen coefficient from current `Te(Ln)`. Active source instead assigns `ReBu0` after the update, making `ReBu0` and current `ReBuT` equal for that step.

This means revision 53 does not retain a separate previous-temperature Bunsen coefficient in the active transport call. That is a broader continuous-run numerical/state approximation and should not be conflated with the restart finding.

The restart discrepancy remains independently established because the uninterrupted path accepts `RsCo` directly while the restore path reconstructs `Co` from `Cs` using `Terf`.

## 7. ARCH02 reconciliation

Authoritative ARCH02 candidate head observed for this audit:

`work/animo-arch02-restart-checkpoint-sufficiency@a079d93c965f6073586c55ee4b3544dd8873b723`

ARCH02 correctly classifies GHG aqueous phase views as recomputed state derived from canonical system state and requires externally owned hydrology to be synchronized to the exact accepted model time.

GHG01 strengthens that design with two explicit sufficiency conditions:

`GHG_PHASE_VIEW_RECONSTRUCTION_USES_ACCEPTED_CHECKPOINT_THERMODYNAMIC_AND_HYDROLOGY_STATE`

`ACTIVE_PONDING_GHG_STATE_HAS_EXPLICIT_LAYER0_OWNER_OR_DETERMINISTIC_RECONSTRUCTION`

A portable ANIMO5 checkpoint does not need to serialize both `Cs` and `Co` merely to imitate the legacy file. It does need enough accepted thermodynamic and hydrological state to reconstruct the phase view uniquely and identically, including the active ponding compartment when present.

## 8. PREP12 restart-evidence reconciliation

The current restart evidence rehome is `work/animo-prep12-restart-state-continuity-rehome@3d86de057247adcfeefb82c11d7cf7d5b2cbdf73`.

Its preserved `RESTART_STATE_CONTINUITY_BASELINE.md` explicitly says that CH4 and N2O have matching `>methan:` and `>nitoxi:` read/write surfaces but that this proves only source-level representation symmetry, not split-run qualification. Its `RESTART_STATE_INVENTORY.csv` classifies both GHG rows as `STRUCTURAL_SYMMETRY_GHG_REFERENCE_BLOCKED`.

GHG01 does not contradict that baseline. It makes the previously unresolved semantics more precise. The GHG row crosses representations:

- accepted runtime process view includes dissolved concentration `Co`;
- final physical system state includes `RsCs` and dissolved `RsCo`;
- restart serialization writes `RsCs` only;
- restart reconstruction derives `Co` using `Terf` and omits layer-0 dissolved reconstruction.

Therefore label-level read/write symmetry is insufficient to classify GHG continuation state as restart-complete. The PREP12 GHG rows should remain reference-blocked and, when that evidence line is next reconciled, should consume the two GHG01 local findings rather than creating competing restart identifiers.

This is an evidence handoff only. GHG01 does not modify or requalify PREP12.

## 9. Required qualification experiment

A future revision-53-compatible activated GHG case should test a split-run continuation against an uninterrupted run at an accepted checkpoint where:

- at least one unsaturated GHG-active layer has `Te != Terf`;
- CH4 and/or N2O storage is nonzero;
- exact pre-checkpoint `RsCs`, `RsCo`, water content and temperature are captured;
- restored `Cs`, reconstructed `Co`, first-step gas-phase concentrations and subsequent process rates are compared before aggregate outputs;
- a separate case exercises pre-existing ponding with nonzero layer-0 GHG state.

A synthetic case can establish causal restart sensitivity, but cannot become B0 or B2 historical reference evidence.

## 10. Qualification consequence

Revision-53 `INITIAL.OUT` is sufficient to carry total CH4-C and N2O-N system concentration textually, but GHG01 cannot qualify it as a behaviourally sufficient GHG restart representation.

Two distinct source findings now block such a claim:

- soil-layer phase state is reconstructed with `Terf` rather than proven accepted checkpoint-time thermodynamic state;
- saved layer-0 GHG state is not reconstructed to the runtime dissolved state for pre-existing ponding.

These findings do not change the final GHG01 closeout and do not establish historical numerical magnitude.

Final GHG01 qualification remains:

`QUALIFIED_GHG_THEORY_SOURCE_AND_INPUT_LINEAGE_EVIDENCE_WITH_HISTORICAL_REFERENCE_GAPS`

B3 and production migration remain not admitted.
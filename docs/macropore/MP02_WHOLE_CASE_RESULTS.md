# ANIMO-MP02 whole-case results

Decision: `QUALIFIED_COMPLETE_CASE_B1_MACROPORE_ACTIVATION_WITH_TCD025_SYMPTOM_EVIDENCE_GNU_FPE_SEAM_AND_HISTORICAL_REFERENCE_RESTART_OPEN`

Production migration: `NOT_ADMITTED`

Historical B2 reference: `ABSENT`

## 1. Execution result

The frozen revision-53 source was rebuilt with the already qualified GNU diagnostic recipe. The executable SHA-256 was reproduced exactly as:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

All six prepared complete cases reached `Successful completion of simulation` over 2922 simulated timesteps.

The five positive labels reported revision-53 macropore iteration activity for every timestep and every enabled macropore substance:

- DOC: 2922 first-iteration hits;
- DON: 2922;
- NH4: 2922;
- NO3: 2922;
- DOP: 2922;
- PO4: 2922.

No positive run emitted the `MAPOHYDRO` macropore water-balance warning or the `MAPOTRANSPORT` macropore mass-balance warning.

This upgrades the evidence from frozen-kernel B1 exercise in MP01 to complete ANIMO orchestration B1 exercise. It still remains synthetic diagnostic evidence.

## 2. Negative control

`MP02-NO-MP` retained the frozen `CranGrass` scientific inputs. It completed with the known CranGrass diagnostic-input warnings already present in the baseline path and without macropore iteration statistics.

The negative control does not provide positive macropore evidence. Its role is to anchor the descendant comparisons.

## 3. Storage-only result needs a precise interpretation

The active `STORAGE` case did not deliberately inject matrix exchange or direct drainage, but its full species trajectories are not expected to equal `NO-MP`.

The reason is source-bound: `MAPOHYDRO` calculates `MpWfps` from matrix water plus macropore stored water. `MpWfps` enters downstream process conditions. Thus macropore water storage is not merely a passive extra ledger stock in revision 53.

This strengthens the architectural conclusion from MP01: macropore storage must be treated as model state with process coupling, not as a reporting-only extension.

## 4. Activated-path evidence for TCD-025

The public water balance is the clearest control-volume symptom.

`bawaTP.Out` is byte-identical across:

- `NO-MP`;
- `STORAGE`;
- `EXCHANGE`;
- `DIRECT-DRAIN`;
- both combined solute-transfer labels.

The human-readable `ani_waTP.Bal` is also byte-identical across all six cases.

This remains true even though the positive hydrology streams contain nonzero macropore storage and, depending on the case, an explicit `0.02 mm` matrix-to-macropore exchange or direct macropore drainage event. The specialized macropore water balance emits no warning. The public water observer therefore does not expose the complete active macropore control volume in these diagnostics.

That observation is consistent with the source:

- macropore water storage is absent from the public `Bawa` storage calculation;
- the source lines that would add `FlMpOuDrMp` to public water drainage are commented out.

### Matrix-to-macropore exchange symptom

At timestep 1, `EXCHANGE` differs from `STORAGE` by a designed `2e-5 m` matrix-to-domain2 transfer and an equal macropore storage gain.

The public first-step residual changes by approximately:

- labile DOM: `+5.59e-3 kg ha-1`;
- NH4-N: `+5.82e-4 kg ha-1`;
- NO3-N: `+5.07e-4 kg ha-1`;
- DON-N: `+9.36e-5 kg ha-1`;
- DOP-P: `+1.43e-5 kg ha-1`.

The PO4-P residual changes by about `+1e-3 kg ha-1`, but its absolute first-step value is superposed on the already known CranGrass P-initialization residual (`about -0.724 kg ha-1` in the control). Therefore the differential is useful as path evidence, while the absolute PO4 residual is not attributable to TCD-025 alone.

The water residual is unchanged (`-6e-7 mm` in both cases), despite the explicit internal water transfer and macropore storage change.

This is complete-case causal evidence for the existing TCD-025 interpretation: the specialized matrix/macropore process can close while the public main ledger omits part of the conserved state and transfer system.

### Direct drainage

`DIRECT-DRAIN` also leaves the public water output byte-identical to the control. That does not mean the direct drainage event was absent. In this design, direct drainage and macropore storage loss are paired. Omitting both from the public control volume can therefore hide the event rather than create a residual.

Source inspection remains necessary for species-specific `Dra4` semantics:

- water `Dra4` population is commented out;
- DOM `Dra4` population is commented out;
- NH4, NO3 and DON `Dra4` are populated;
- those N `Dra4` terms are not included in the corresponding `Ddev` formulas;
- equivalent public P direct-drain integration is absent.

MP02 does not propose a correction.

## 5. Solute-label reconciliation and replication

The prepared scientific inputs for `SOLUTE-N` and `SOLUTE-P` are byte-identical. Treating them as independent evidence would be wrong.

The pair is instead useful as an exact-input replication test. After normalizing only run timestamps, elapsed time and file-created timestamps, both complete output bundles have the same SHA-256:

`04915574e59fb36b49a38bdcc80f9ae062e6c4a452c5833e60acf19f033453bf`

So the active diagnostic route is reproducible under the investigated GNU build despite the floating-point status finding below.

The scientific claim remains one combined P-active N/P macropore transfer case. It exercises DOC, DON, NH4, NO3, DOP and PO4 through the complete orchestration, but it is not a species-isolation experiment.

## 6. New GNU diagnostic floating-point seam

Every active complete case finished successfully but the GNU runtime reported:

`IEEE_INVALID_FLAG`

The negative `NO-MP` control did not.

A diagnostic rebuild adding `-ffpe-trap=invalid,zero,overflow`, `-g` and `-fbacktrace` localized the first active-route trap to `MAPOTRANSPORT.FOR:670`, inside `MpTransp`:

`If (Abs(BaDev).Gt.1.d-5 .And. Abs(BaDev/BaMx).Gt.0.005) ...`

The active storage case traps when the ratio is evaluated for a zero-mass balance state. Under the GNU evaluation used here, that produces an invalid `0/0` operation. The no-macropore control reaches normal legacy `STOP 100` without the trap.

Classification:

`GNU_DIAGNOSTIC_ACTIVE_ROUTE_INVALID_FLAG_FROM_BALANCE_WARNING_GUARD_HISTORICAL_COMPILER_EFFECT_UNPROVEN`

This is not evidence that the historical Intel executable trapped or altered scientific state. Fortran does not require the short-circuit behaviour that this expression appears to assume. The finding therefore belongs to build/numerical-policy qualification before migration, rather than being silently treated as historical model behaviour.

No output nondeterminism was observed in the exact-input replication after timestamp normalization.

## 7. Persistent restart remains incomplete

The complete active run writes `Output/initial.out`, but that file does not contain the `>MPnitr:`, `>MPorgs:` or `>MPphos:` macropore end-state records.

This matches `Output_Init.for`, where the macropore output arguments and writer block are commented out.

The MP01 source finding is therefore now supported by complete-case observation:

`SOURCE_AND_COMPLETE_CASE_CONFIRMED_PERSISTENT_MACROPORE_SOLUTE_RESTART_OMISSION`

A continuous-versus-split active macropore test is not meaningful as an equivalence qualification until a complete persistent restart representation exists or a separately governed diagnostic patch is introduced.

## 8. Evidence ladder after MP02

- `SOURCE_SUPPORTED`: yes;
- `THEORY_SUPPORTED`: yes for hydrological architecture and conservation ownership, partial for exact ANIMO solute formulation;
- `B1_CAUSALLY_EXERCISED`: yes, now including complete ANIMO orchestration;
- `B2_HISTORICALLY_REFERENCED`: no;
- `B3_READY`: no;
- `B3_ADMITTED`: no.

## 9. What remains open

The most important blockers are now narrower:

1. no native active historical macropore case or independently trusted B2 output has been recovered;
2. persistent macropore solute restart state is incomplete;
3. TCD-025 is behaviourally visible but remains uncorrected and unadmitted;
4. exact revision-53 ANIMO solute-transfer theory is still only partially independently documented;
5. the MP01 initial-NO3 validation seam remains outside TCD-025 and needs canonical discrepancy governance;
6. the GNU active-route invalid-operation warning guard needs numerical/build-policy disposition.

Production implementation remains out of scope.

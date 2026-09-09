# ANIMO-STATEQ01 PREP12 restart-evidence reconciliation

Status: `QUALIFIED_RECONCILIATION_NO_EVIDENCE_STRENGTH_UPGRADE`

Production migration: `NOT_ADMITTED`

This note reconciles STATEQ01 with the provenance-preserving PREP12 rehome at `work/animo-prep12-restart-state-continuity-rehome@3d86de057247adcfeefb82c11d7cf7d5b2cbdf73`. PREP12 preserves PREP10 source/diagnostic findings without scientifically requalifying them. Its source-local labels `TCD-032`, `TCD-033` and `TCD-034` do not have canonical TCD allocations. PREP12 records `canonical_tcd_id = null` for all three and assigns RG02 reconciliation keys. STATEQ01 therefore consumes the findings by exact reconciliation key and does not allocate canonical discrepancy numbers.

## 1. Macropore correction

The initial STATEQ01 closeout incorrectly described the persistent macropore solute writer omission as part of `TCD-025`.

That is too broad. The evidence must remain separated:

- `TCD-025` concerns the incomplete public/main macropore conserved control volume and direct-drainage integration identified by PREP06/MP01/MP02;
- the persistent restart writer omission is the PREP12 local finding `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`, source-local label `TCD-032`, canonical TCD not allocated.

Revision 53 actively reads `>MPnitr:`, `>MPorgs:` and conditional `>MPphos:` state and carries the corresponding result state between ordinary timesteps, while the writer blocks in `Output_Init.for` are commented out. MP02 independently observes the omission in complete active cases. This blocks the macropore checkpoint profile in addition to TCD-025, but it must not be renamed TCD-025.

## 2. Crop continuation correction

PREP12 materially sharpens the crop checkpoint blocker.

For applicable plant modes, cumulative actual uptake state is carried between ordinary accepted timesteps:

- `Amplni_act <-> Rsamplni_act`;
- `Amplpo_act <-> Rsamplpo_act`.

The `>orgpla:` restart representation contains the actual uptake values, but `Inicalc.for` does not copy a nontrivial restart value into the accepted actual-uptake state before copying in the opposite direction. The PREP12 reconciliation key is:

`RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`

Source-local label: `TCD-033`; canonical TCD: not allocated.

Potential cumulative uptake is also carried between ordinary timesteps and is used by `Uptpar_Plant` through potential-minus-actual demand logic:

- `Amplni_pot <-> Rsamplni_pot`;
- `Amplpo_pot <-> Rsamplpo_pot`.

It has no `>orgpla:` restart representation and is initialized to zero on restart. The PREP12 reconciliation key is:

`RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`

Source-local label: `TCD-034`; canonical TCD: not allocated.

STATEQ01 therefore separates crop root/shoot and actual plant N/P physical stocks from continuation-critical potential uptake state. Potential uptake is not a conserved crop stock, but it is persistent scientific continuation because future behaviour depends on its accepted value.

## 3. NH4 adsorbed-state checkpoint interpretation

PREP06 correctly identifies adsorbed NH4 as physical nitrogen storage. PREP12 adds a checkpoint-specific distinction: revision 53 does not serialize `Cxnh/Rscxnh` as an independent restart coordinate because it is reconstructed from NH4 solution concentration and the admitted sorption relation/parameters.

STATEQ01 therefore no longer requires a second independent checkpoint owner for adsorbed NH4. The physical adsorbed amount remains part of the nitrogen control volume, but its checkpoint representation is `DERIVED_RECOMPUTABLE` provided the reconstruction is deterministic from accepted aqueous NH4, hydrology/soil coordinates, configuration and numerical policy. Later split-run qualification is still required before this omission can be B3-admitted.

This distinction avoids duplicating one equilibrium degree of freedom while preserving the physical storage term in conservation accounting.

## 4. P initialization-mode canonicalization

PREP12 confirms structural read/write coverage for aqueous P, every configured fast/slow sorption site, precipitated P and DOP, but `Output_Init` always emits explicit `Inpo=1` restart state. Input modes `Inpo=2/3` are therefore canonicalized to explicit state at restart.

STATEQ01 keeps site-resolved accepted P state as the candidate canonical checkpoint shape. This does not prove that a legacy trajectory initialized through modes 2 or 3 is split-run equivalent after the 2/3-to-1 conversion. That remains an initialization/restart qualification condition, not a reason to add duplicate P owners.

## 5. Governance consequence

The corrected feature-scoped interpretation is:

- `CORE_CNP`: still a readiness candidate, with source-level core restart symmetry but no portable split-run admission;
- `CORE_CNP_WITH_CROP`: blocked by explicit crop restart-continuity findings plus any remaining continuation-family minimization;
- `CORE_CNP_WITH_MACROPORES`: blocked independently by TCD-025 and `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`;
- no PREP12 source-local TCD label is promoted to canonical TCD by STATEQ01.

The canonical allocation owner for those local findings remains ANIMO B3 governance. STATEQ01 only consumes their state/readiness consequences.
# ANIMO-B3D37 — TCD-039 Atomic B3 Admission Decision

## Decision

Admit the bounded revision-53 internal-crop potential-uptake restart continuation contract qualified by ANIMO-B3B11, with historical uncertainty preserved.

Admitted identity:

`TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_OWNER_RESTORE_N_AND_CONDITIONAL_P`

## Supported scope

- frozen ANIMO 4.1.5 revision 53;
- internal ANIMO crop mode, `Ioptplant == 1`;
- cumulative potential N uptake owner `Rsamplni_pot` restored to `Amplni_pot` before future crop-demand calculation;
- cumulative potential P uptake owner `Rsamplpo_pot` restored to `Amplpo_pot` when `Ipo == 1`;
- nonzero accepted continuation state is not replaced by the cold-start zero path at an arbitrary restart boundary.

The scientific correction is behavioral ownership/restoration. It does not prescribe a checkpoint file format or production serialization layout.

## Classification and assurance

B3 qualification class: `B_LOCAL_RESTART_CHECKPOINT_OMISSION_EXISTING_CONTINUATION_OWNER`.

Review risk remains Tier C because restart/checkpoint semantics can change future state and flux trajectories. The Class-B resolution therefore does not reduce the GOV05 evidence gate.

The GOV05 review model is same-agent adversarial review. It is explicitly not genuinely independent.

## Historical disposition

Historical revision-53 behavior remains `UNKNOWN_WITHOUT_B2`.

The B1 source-shaped split witnesses establish bounded causality and owner necessity. They are not B2 and do not establish historical prevalence.

## Expected effect

Within the supported restart profile, corrected continuation may change subsequent crop demand, uptake and connected trajectories relative to a legacy restart that omitted the accepted potential-uptake owner. That difference is expected and is the admitted correction effect.

Outside this bounded surface, no behavior is admitted or changed by this decision.

## Exclusions

This admission does not:

- reopen TCD-038 actual uptake;
- resolve STATEQ01 CROP-007 broader stage/rotation continuation;
- admit external crop mode;
- admit canonical STATE as a whole;
- claim whole-model split-run equivalence;
- define checkpoint file-format migration;
- modify production source;
- open B4 or production migration.

## Aggregate cadence

RG05M remains the current central aggregate. TCD-039 is the first exact-final admission after RG05M if this workunit closes green. No aggregate update is required until the normal three-admission threshold is reached, absent a separate project gate.

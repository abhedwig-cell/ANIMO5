# ANIMO-STATEQ05 — TCD-039 Internal-Crop Potential-Uptake Continuation State

## Purpose

Qualify the narrow persistent-state question behind canonical TCD-039 without admitting canonical STATE, changing production source, or broadening into the unresolved full crop checkpoint set.

The supported profile is frozen-revision-53 internal crop mode (`Ioptplant == 1`). The scientific question is whether cumulative potential crop uptake is an accepted continuation owner or may be reset/reconstructed from restart configuration alone.

## Frozen source evidence

Source archive SHA256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

The pinned revision-53 source establishes:

- `Upintg_Plant.for` initializes `Rsamplni_pot` from `Amplni_pot` and, when P is active, `Rsamplpo_pot` from `Amplpo_pot`; it then advances those accumulated potential-uptake values and can reduce them under nutrient-shortage logic.
- `Uptpar_Plant.for` consumes `Amplni_pot - Amplni_act` as N deficit and `Amplpo_pot - Amplpo_act` as P deficit. Potential uptake therefore influences later process demand/selectivity and is not report-only state.
- `Init.for` restores the accepted backing values into the working potential-uptake coordinates during normal continuation.
- `Inicalc.for` uses cold-start initialization that zeros the potential working accumulators.
- `Output_Init.for` serializes actual crop uptake but omits the potential uptake continuation values from the legacy restart surface.
- `Animo.for` routes the internal crop path through these potential-uptake arguments.

The corresponding exact source-file hashes are in the machine-readable contract and are checked against the repository source manifest.

## Qualified ownership contract

TCD-039 contains two logical continuation quantities, represented by working/backing runtime pairs:

1. N potential uptake: accepted backing `Rsamplni_pot`, working alias `Amplni_pot`.
2. P potential uptake: accepted backing `Rsamplpo_pot`, working alias `Amplpo_pot`, only when `Ipo == 1`.

At an accepted restart boundary, the backing values are persistent continuation owners. The working aliases are restored from those accepted owners before future uptake-demand calculations. A restart that replaces a nonzero accepted potential value by zero is not equivalent for this bounded process contract.

This qualification does **not** claim that the complete crop state is only these quantities. STATEQ01 `CROP-007` remains outside scope and unresolved. Actual uptake state belongs to the already separate TCD-038 route and is not reopened here.

## Synthetic oracle

The executable oracle is B1/source-derived evidence, not B2 and not a full frozen-Fortran split-run. It checks:

- nonzero potential uptake changes the later deficit at fixed actual uptake;
- continuation advances from the prior accepted value rather than from zero;
- shortage logic changes potential uptake, making the accepted value history-dependent under the source process;
- exact owner restore preserves a source-shaped split sequence;
- zero-reset at the split produces a different future result;
- P continuation is conditional on `Ipo == 1`;
- N/P potential state remains distinct from actual uptake ownership.

## Boundaries

No production source is modified. No B0 bytes are modified. No canonical register or queue is modified. No canonical STATE admission is made. No TCD-038 reopening occurs. No `CROP-007` closure is claimed. No historical B2 is created. No full-model split-run or whole-model golden baseline is claimed. B4 and production remain closed.

The intended outcome is readiness for a separate GOV05 Tier-C TCD-039 admission decision, not admission by STATEQ05 itself.

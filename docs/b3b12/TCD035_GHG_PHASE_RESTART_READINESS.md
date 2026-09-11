# ANIMO-B3B12 — TCD-035 GHG soil-layer phase restart admission readiness

## Decision question

After STATEQ06 resolves the checkpoint owner model, is TCD-035 a bounded admission candidate under an existing-owner local restart reconstruction, or does it still require a new physical phase/state model?

## Classification resolution

The B3Q04 queue carried TCD-035 as `C provisional` while checkpoint phase ownership and deterministic reconstruction were unresolved. STATEQ06 resolves that bounded soil-layer question for frozen revision 53:

- gas-specific total system concentration `Cs/RsCs` is the accepted checkpoint owner;
- aqueous concentration `Co` is a derived phase view, not a second independent checkpoint owner;
- exact `Co` reconstruction uses accepted checkpoint `theta`, `theta_sat` and soil temperature with the frozen source Bunsen relation;
- revision-53 restart instead uses `Terf`, which is not generally equivalent;
- no physical storage, phase, constitutive relation or transfer law is added or redefined.

The atomic correction mechanism is therefore:

`B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER`

The review risk remains Tier C because a restart reconstruction change can alter subsequent trajectories.

## Atomic admission candidate

Identity:

`TCD035_GHG_SOIL_LAYER_PHASE_VIEW_RECONSTRUCT_FROM_ACCEPTED_CS_HYDROLOGY_AND_CHECKPOINT_TEMPERATURE`

Scope:

- frozen ANIMO 4.1.5 revision 53;
- `IoptGHG >= 1`;
- soil layers `1..Nl` only;
- CH4 and N2O separately with their source-specific Bunsen coefficients;
- accepted total-system gas state preserved;
- accepted checkpoint hydrology and thermodynamic coordinates used for deterministic aqueous phase reconstruction.

The correction does not serialize a second independent `Co` owner and does not change the Bunsen/Henry-law formulation.

## Causal evidence

1. Frozen-source lifecycle/algebra, pinned through GHG01 and STATEQ06: revision 53 serializes total-system state and reconstructs `Co` with `Terf`.
2. Qualified STATEQ06 ownership authority: exact accepted checkpoint hydrology and temperature define deterministic phase reconstruction; layer0 remains excluded.
3. Executable source-shaped oracle: 72 CH4/N2O cases with both exact-continuity controls and nontrivial `Terf` divergence cases.

These establish bounded causality/readiness. They do not establish historical prevalence. The oracle is B1, not B2.

## Historical disposition

Historical revision-53 behavior remains `UNKNOWN_WITHOUT_B2`. A later scientific admission can only carry historical uncertainty explicitly and must not claim historical fidelity.

## Excluded scope

- TCD-036 layer0/ponding restart continuity;
- GHG hidden within-timestep solver context from BUILDQ03;
- TCD-032, TCD-033 and TCD-034;
- continuous-run Bunsen update policy;
- canonical STATE admission;
- checkpoint file-format migration;
- full-model GHG split-run equivalence;
- production source changes;
- B4 and production migration.

## Readiness conclusion

If this exact package passes CI and GOV05 adversarial review, the bounded TCD-035 identity is ready for a separate Tier-C atomic B3 admission decision with historical uncertainty. B3B12 itself performs no admission.

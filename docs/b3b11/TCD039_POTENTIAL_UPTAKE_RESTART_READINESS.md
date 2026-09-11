# ANIMO-B3B11 — TCD-039 Potential-Uptake Restart Admission Readiness

## Decision question

Does the now-qualified TCD-039 state contract remain a Class-C missing-state problem, or is the canonical discrepancy a bounded Class-B restart/checkpoint omission with Tier-C review risk?

## Classification resolution

The provisional queue label was `C provisional` because owner versus deterministic reconstruction was unresolved. STATEQ05 resolves that uncertainty for the frozen revision-53 internal-crop profile:

- accepted potential N uptake already exists as `Rsamplni_pot`, with working alias `Amplni_pot`;
- conditional accepted potential P uptake already exists as `Rsamplpo_pot`, with working alias `Amplpo_pot` when `Ipo == 1`;
- later demand calculations consume those values;
- `Init` restores the working aliases from accepted backing state;
- `Output_Init` omits the potential continuation values from the legacy restart surface;
- cold-start zeroing is a different lifecycle path.

No new physical storage, phase, constitutive law, transfer process, or missing-state model is needed to state the correction. The discrepancy is therefore not Class C under B3Q01's defining test. It is a bounded Class-B local restart/checkpoint omission involving an existing future-influencing continuation owner.

The **scientific review risk remains Tier C** because restart/checkpoint semantics can alter future trajectories. Reclassification of the B3 qualification class does not reduce the GOV05 evidence gate.

## Admission candidate

Bounded identity:

`TCD039_INTERNAL_CROP_POTENTIAL_UPTAKE_RESTART_CONTINUATION_OWNER_RESTORE_N_AND_CONDITIONAL_P`

Scope:

- frozen ANIMO 4.1.5 revision 53;
- internal crop mode, `Ioptplant == 1`;
- N potential continuation always in that profile;
- P potential continuation only when `Ipo == 1`;
- exact accepted owner restored before future crop demand calculation;
- a nonzero accepted owner may not be replaced by the cold-start zero path at an arbitrary restart boundary.

Excluded:

- actual uptake TCD-038;
- STATEQ01 CROP-007 broader crop stage/rotation continuation;
- external crop mode;
- canonical STATE admission;
- checkpoint file-format implementation;
- whole-model split-run equivalence;
- production migration.

## Evidence disposition

B0: exact revision-53 source semantics are archive/member-hash pinned by STATEQ05.

B1: source-shaped executable positive/negative restart witnesses pass. This is not B2.

Prior authority: STATEQ01 independently records CROP-005 and CROP-006 as accepted continuation state with mandatory restore semantics and zero-reset forbidden absent qualification.

Historical behavior remains `UNKNOWN_WITHOUT_B2`. A later admission may therefore only use the historical-uncertainty disposition and must preserve that uncertainty explicitly.

## Readiness conclusion

If this package and its GOV05 adversarial review pass at exact heads, the bounded TCD-039 identity is ready for a separate Tier-C scientific admission decision. B3B11 itself performs no admission.

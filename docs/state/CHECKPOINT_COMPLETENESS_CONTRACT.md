# ANIMO5 checkpoint completeness contract

Work unit: `ANIMO-STATEQ01`

Status: `CANDIDATE_COMPLETENESS_CONTRACT_NOT_STATE_ADMISSION`

Production migration: `NOT_ADMITTED`

## 1. Purpose

This contract defines when an accepted-boundary checkpoint is structurally complete for one declared ANIMO5 state profile. It does not define a binary file format, admit any feature, or convert legacy `INITIAL.OUT` into a canonical checkpoint.

The checkpoint is a serialization of an already accepted state plus the identities required to resume it. It is never the operation by which a trial becomes accepted.

## 2. Boundary rule

A physical checkpoint may be created only in `ACCEPTED_IDLE`, after the completed actual result for interval `t0 -> t1` has passed the applicable acceptance barrier and become the accepted generation at `t1`.

For the final interval this logical promotion still occurs even though revision 53 has no subsequent ordinary `Init` call. Legacy final-result serialization is evidence about fields, not the canonical acceptance mechanism.

The following are forbidden as portable physical checkpoint sources:

- `G_PROVISIONAL` potential-pass state;
- an executing or rejected trial;
- trial-local transfer journals that have not been committed;
- report accumulators treated as substitutes for physical stocks;
- serializer-created corrections or clamps.

## 3. Required checkpoint sections

A complete checkpoint for profile `P` contains five logical sections.

### 3.1 Identity header

Mandatory identities are:

- checkpoint schema/version identity;
- `accepted_generation_id`;
- exact accepted model time and calendar contract identity;
- `configuration_identity`;
- `physical_layout_id` and geometry identity;
- configured P fast/slow site cardinalities when P is active;
- numerical/precision policy identity needed to interpret state and continuation;
- event schedule identity;
- active feature topology/profile identity;
- source/evidence compatibility identity when required by the admission contract.

Changing configuration, feature topology, geometry or site cardinality across restore is a state migration, not an ordinary restart. It requires a separately admitted transition contract.

### 3.2 ANIMO-owned accepted physical state

Serialize every matrix row whose class is `CORE_STATE_READY_CANDIDATE` and is required by profile `P`.

For an enabled optional feature, serialize every required row classified `OPTIONAL_FEATURE_STATE_READY_CANDIDATE` only if the feature itself has been admitted for the profile. A row classified `FEATURE_STATE_BLOCKED` makes the profile checkpoint incomplete and restore must fail closed.

A physical quantity can be excluded as an independent checkpoint coordinate when its matrix class is `DERIVED_RECOMPUTABLE` and the reconstruction contract is admitted. This does not mean the physical storage disappears from conservation. It means there is no second independent checkpoint degree of freedom.

### 3.3 External-owner bindings

For every `EXTERNAL_OWNER_REFERENCE` required by profile `P`, the checkpoint binds an exact compatible external accepted generation or frame identity. At minimum the binding must establish the accepted time, geometry/layout/schema compatibility and immutable content identity required by TIME01.

ANIMO may cache external coordinates during execution, but the canonical checkpoint does not silently convert those mirrors into ANIMO ownership.

If the referenced external generation cannot be recovered or proven identical, restore fails before ANIMO state mutation.

### 3.4 Accepted continuation metadata and state

Every `NUMERICAL_CONTINUATION` row required at the accepted boundary is serialized or deterministically reconstructed under an admitted rule.

This includes management progression. The event schedule identity alone is insufficient when the next-event cursor cannot be reconstructed uniquely. Conversely, an implementation may omit a cursor only after equivalence evidence proves exact deterministic reconstruction from accepted coordinates and schedule identity.

Continuation-critical scientific coordinates that are not conserved stocks must also survive when future behaviour depends on them. PREP12 demonstrates this for cumulative potential crop N/P uptake in applicable plant modes. These values are not disposable trial scratch merely because PREP06 classified them as derived demand/reference state.

Within-step nonlinear solver arrays and potential-pass scratch are not accepted continuation merely because a legacy procedure retains them between task calls.

### 3.5 Optional diagnostic continuation

`DIAGNOSTIC_ONLY` rows are outside physical checkpoint completeness.

If the run contract promises exact mid-report-period output continuity, the checkpoint must additionally include a versioned diagnostic observer section containing the required report-period accumulators and report cursor. That section is restored after physical state compatibility is established and never modifies the accepted physical owner state.

If exact diagnostic continuity is not promised, the observer section may be omitted. A project may instead restrict report-continuity checkpoints to report boundaries.

## 4. Completeness predicate

For a profile `P`:

```text
checkpoint_complete(P) =
    identity_header_complete(P)
AND model_owned_state_complete(P)
AND continuation_complete(P)
AND external_owner_bindings_complete(P)
AND every_enabled_feature_is_admitted(P)
AND every_enabled_feature_state_is_complete(P)
AND every_required_reconstruction_contract_is_admitted(P)
AND (
      report_continuity_not_requested(P)
      OR diagnostic_observer_state_complete(P)
    )
```

A checkpoint can be structurally complete under this predicate and still lack B3 admission until independent restart/replay qualification is satisfied.

## 5. Restore transaction

Restore is fail-before-mutate.

1. Parse and validate the identity header.
2. Resolve the declared state profile and feature guards.
3. Reject unsupported, unadmitted or blocked enabled features.
4. Resolve all external-owner bindings and verify accepted time plus layout/schema compatibility.
5. Allocate only state families enabled by the validated profile.
6. Load ANIMO-owned accepted physical state without projection, clipping or chemistry changes.
7. Restore accepted continuation metadata/state or execute only an admitted deterministic reconstruction rule.
8. Recompute `DERIVED_RECOMPUTABLE` views in the declared dependency order from the restored accepted state and bound frames.
9. Restore diagnostic observer continuation separately when requested.
10. Establish a new runtime `ACCEPTED_IDLE` object representing the restored accepted generation. No physical process is run as part of restore.

Any failure before step 10 leaves no partially accepted model state.

## 6. Derived-state rule

A quantity may be excluded from the serialized owner set as `DERIVED_RECOMPUTABLE` only when all of the following hold:

- it has no independent accepted-boundary degree of freedom;
- every input to its reconstruction is present in accepted state, configuration or a bound external frame;
- the reconstruction is deterministic under the admitted numerical/thermodynamic policy;
- reconstruction does not invoke an unadmitted physical process;
- split-run evidence later confirms that the reconstruction preserves the promised trajectory equivalence.

A convenient formula is not sufficient evidence.

Revision 53 provides a source-level example for NH4 adsorption: adsorbed NH4 is real physical N storage but is reconstructed from aqueous NH4 and the sorption relation rather than serialized independently. STATEQ01 therefore treats the checkpoint coordinate as derived/recomputable, subject to later split-run qualification.

## 7. `Output_Init` purity boundary

Revision-53 `Output_Init` is not a canonical serializer.

Its useful evidence is that it writes many final `Rs*` physical coordinates directly. Its limitations include incomplete feature state and missing identities/continuation metadata. In addition, TS01 identifies a negative crop-P clamp that mutates the final result before output.

The ANIMO5 checkpoint serializer must be observationally pure:

```text
serialize(accepted_state) does not change accepted_state
```

If legacy compatibility ever requires a clamped export representation, that must be an explicit output projection outside the canonical accepted checkpoint and governed by its own discrepancy/compatibility decision.

## 8. PREP12 governance boundary

PREP12 is a provenance-preserving rehome of PREP10 restart evidence. It explicitly records its source-local labels `TCD-032`, `TCD-033` and `TCD-034` with `canonical_tcd_id = null`.

STATEQ01 therefore uses the following reconciliation keys without allocating canonical TCD numbers:

- `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`;
- `RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`;
- `RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`.

Canonical allocation remains owned by ANIMO B3 governance.

## 9. TCD-016 boundary

`M_surface_NH4_non_aqueous_continuation` is not a canonical checkpoint field in STATEQ01.

SQ01 classifies it as a preferred proposed model extension that is review-ready but scientifically not admitted. Therefore:

- a profile requiring scientifically complete surface-NH4 wet/dry continuation is blocked;
- restore may not synthesize the proposed mass from an aqueous concentration;
- cold initialization may not invent a zero field and thereby imply admission;
- no checkpoint is called complete for that profile by silently dropping residual surface NH4.

If C1 is later scientifically admitted, its accepted areic mass would become mandatory persistent state and its restart semantics would require separate qualification.

## 10. Phosphorus canonicalization boundary

The candidate canonical accepted P state is explicit site-resolved state. A checkpoint therefore stores aqueous PO4, each configured fast site, each configured slow site, precipitated P and DOP under the exact layout/cardinality identity.

Revision 53 `Output_Init` always emits `Inpo=1` explicit restart state even when the original initialization used `Inpo=2/3`. STATEQ01 does not treat the original initialization mode as an extra persistent owner. However a legacy trajectory originating in mode 2 or 3 is not admitted as restart-equivalent until a dedicated split-run qualification shows that the 2/3-to-1 canonicalization preserves the promised trajectory.

## 11. Macropore boundary

For `CORE_CNP_WITH_MACROPORES`:

- macropore water remains an external hydrology-owner reference;
- ANIMO-owned macropore solute state must be present for every enabled species/domain required by the admitted feature;
- `TCD-025` remains the separate public/main control-volume and transfer-integration blocker;
- the revision-53 `Output_Init` omission of `>MPnitr:`, `>MPorgs:` and `>MPphos:` is the independent PREP12 finding `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`, not TCD-025;
- missing macropore state may not be reconstructed as zero.

Until both the control-volume issue and the independent restart finding are canonically disposed and the feature is qualified, the profile fails closed.

## 12. GHG boundary

For `CORE_CNP_WITH_GHG`, total `CsCH4` and `CsN2O` owner state alone does not establish behavioural checkpoint sufficiency.

Before a GHG checkpoint profile can be complete, governance must admit a deterministic phase reconstruction contract that uses the correct accepted thermodynamic/hydrology coordinates, including layer 0 when ponding is active. The current legacy `Terf` reconstruction and layer-0 gap are not adopted as canonical behaviour.

Hidden cross-call GHG task locals are not automatically added to the accepted checkpoint. They must first be classified as explicit trial state, deterministic recomputation, or genuinely persistent science under a separate GHG qualification. STATEQ01 makes no intended-physics claim about them.

## 13. Crop continuation boundary

ANIMO-owned crop root/shoot dry matter and actual N/P are persistent optional physical-owner candidates.

Checkpoint continuity is nevertheless blocked by two concrete PREP12 findings in applicable plant modes.

`RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`: actual cumulative N/P uptake is represented in `>orgpla:` but the restart-to-accepted initialization direction loses nontrivial values.

`RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`: cumulative potential N/P uptake is carried between ordinary timesteps and influences later demand, but has no restart representation and is reset to zero.

Potential uptake is continuation state, not a conserved crop stock. Additional TS01 crop demand/deficit/stage continuation still requires minimization. Therefore a checkpoint that stores only root/shoot and actual crop N/P is not sufficient for `CORE_CNP_WITH_CROP`.

In `crop_mode=external`, ANIMO instead binds the exact external crop frame/generation and does not duplicate an external crop owner.

## 14. Report-period boundary

Balance-period closeout is a reporting event, not physical acceptance. A report reset can happen after a physical interval without altering the physical state generation.

Thus:

```text
physical_checkpoint_complete != report_continuation_complete
```

The two may be bundled in one file container, but their ownership and validation remain separate.

## 15. Admission tests still required

This contract is ready for later implementation/test design, but canonical STATE admission still requires evidence beyond structure:

- uninterrupted versus split-run equivalence for `CORE_CNP` at multiple accepted boundaries;
- explicit verification of NH4 adsorbed-state reconstruction under checkpoint restore;
- checkpoints adjacent to management events and year/crop transitions;
- P mode-2/3 origin to explicit-state restart qualification when those initialization modes are in scope;
- final-interval serializer-purity testing;
- explicit external-frame rebind/reject tests;
- P site-cardinality mismatch rejection;
- optional report-continuation equivalence when promised;
- feature-specific tests only after those features are scientifically and architecturally admitted.

Final status:

`CANDIDATE_COMPLETENESS_CONTRACT_READY_FOR_LATER_ADMISSION_TESTING`

`CANONICAL_STATE_ADMISSION = NOT_ADMITTED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
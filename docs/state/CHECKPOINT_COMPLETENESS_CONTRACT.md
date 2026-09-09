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

No aggregate is serialized as a second owner when its matrix class is `DERIVED_RECOMPUTABLE`.

### 3.3 External-owner bindings

For every `EXTERNAL_OWNER_REFERENCE` required by profile `P`, the checkpoint binds an exact compatible external accepted generation or frame identity. At minimum the binding must establish the accepted time, geometry/layout/schema compatibility and immutable content identity required by TIME01.

ANIMO may cache external coordinates during execution, but the canonical checkpoint does not silently convert those mirrors into ANIMO ownership.

If the referenced external generation cannot be recovered or proven identical, restore fails before ANIMO state mutation.

### 3.4 Accepted continuation metadata

Every `NUMERICAL_CONTINUATION` row required at the accepted boundary is serialized or deterministically reconstructed under an admitted rule.

This includes management progression. The event schedule identity alone is insufficient when the next-event cursor cannot be reconstructed uniquely. Conversely, an implementation may omit a cursor only after equivalence evidence proves exact deterministic reconstruction from accepted coordinates and schedule identity.

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
7. Restore accepted continuation metadata or execute only an admitted deterministic reconstruction rule.
8. Recompute `DERIVED_RECOMPUTABLE` views in the declared dependency order from the restored accepted state and bound frames.
9. Restore diagnostic observer continuation separately when requested.
10. Establish a new runtime `ACCEPTED_IDLE` object representing the restored accepted generation. No physical process is run as part of restore.

Any failure before step 10 leaves no partially accepted model state.

## 6. Derived-state rule

A quantity may be excluded from the serialized owner set as `DERIVED_RECOMPUTABLE` only when all of the following hold:

- it has no independent conserved ownership;
- every input to its reconstruction is present in accepted state, configuration or a bound external frame;
- the reconstruction is deterministic under the admitted numerical/thermodynamic policy;
- reconstruction does not invoke an unadmitted physical process;
- split-run evidence later confirms that the reconstruction preserves the promised trajectory equivalence.

A convenient formula is not sufficient evidence.

## 7. `Output_Init` purity boundary

Revision-53 `Output_Init` is not a canonical serializer.

Its useful evidence is that it writes many final `Rs*` physical coordinates directly. Its limitations include incomplete feature state and missing identities/continuation metadata. In addition, TS01 identifies a negative crop-P clamp that mutates the final result before output.

The ANIMO5 checkpoint serializer must be observationally pure:

```text
serialize(accepted_state) does not change accepted_state
```

If legacy compatibility ever requires a clamped export representation, that must be an explicit output projection outside the canonical accepted checkpoint and governed by its own discrepancy/compatibility decision.

## 8. TCD-016 boundary

`M_surface_NH4_non_aqueous_continuation` is not a canonical checkpoint field in STATEQ01.

SQ01 classifies it as a preferred proposed model extension that is review-ready but scientifically not admitted. Therefore:

- a profile requiring scientifically complete surface-NH4 wet/dry continuation is blocked;
- restore may not synthesize the proposed mass from an aqueous concentration;
- cold initialization may not invent a zero field and thereby imply admission;
- no checkpoint is called complete for that profile by silently dropping residual surface NH4.

If C1 is later scientifically admitted, its accepted areic mass would become mandatory persistent state and its restart semantics would require separate qualification.

## 9. Macropore boundary

For `CORE_CNP_WITH_MACROPORES`:

- macropore water remains an external hydrology-owner reference;
- ANIMO-owned macropore solute state must be present for every enabled species/domain required by the admitted feature;
- the revision-53 `Output_Init` omission of `>MPnitr:`, `>MPorgs:` and `>MPphos:` is evidence of incompleteness, not permission to reconstruct zero state.

Until TCD-025 and restart qualification close, the feature profile fails closed.

## 10. GHG boundary

For `CORE_CNP_WITH_GHG`, total `CsCH4` and `CsN2O` owner state alone does not establish behavioural checkpoint sufficiency.

Before a GHG checkpoint profile can be complete, governance must admit a deterministic phase reconstruction contract that uses the correct accepted thermodynamic/hydrology coordinates, including layer 0 when ponding is active. The current legacy `Terf` reconstruction and layer-0 gap are not adopted as canonical behaviour.

Hidden cross-call GHG task locals are not automatically added to the accepted checkpoint. They must first be classified as explicit trial state, deterministic recomputation, or genuinely persistent science under a separate GHG qualification. STATEQ01 makes no intended-physics claim about them.

## 11. Crop continuation boundary

ANIMO-owned crop root/shoot dry matter and actual N/P are physical owner candidates. Exact checkpoint completeness additionally depends on the future-use continuation set for crop demand, deficit, stage and cumulative uptake logic.

Because TS01 identifies omitted continuation variables that may affect future demand, `CORE_CNP_WITH_CROP` remains blocked for canonical checkpoint qualification until the minimal set is source-qualified and split-run tested. A checkpoint that stores only the four obvious crop stocks is not yet proven sufficient.

In `crop_mode=external`, ANIMO instead binds the exact external crop frame/generation and does not duplicate an external crop owner.

## 12. Report-period boundary

Balance-period closeout is a reporting event, not physical acceptance. A report reset can happen after a physical interval without altering the physical state generation.

Thus:

```text
physical_checkpoint_complete != report_continuation_complete
```

The two may be bundled in one file container, but their ownership and validation remain separate.

## 13. Admission tests still required

This contract is ready for later implementation/test design, but canonical STATE admission still requires evidence beyond structure:

- uninterrupted versus split-run equivalence for `CORE_CNP` at multiple accepted boundaries;
- checkpoints adjacent to management events and year/crop transitions;
- final-interval serializer-purity testing;
- explicit external-frame rebind/reject tests;
- P site-cardinality mismatch rejection;
- optional report-continuation equivalence when promised;
- feature-specific tests only after those features are scientifically and architecturally admitted.

Final status:

`CANDIDATE_COMPLETENESS_CONTRACT_READY_FOR_LATER_ADMISSION_TESTING`

`CANONICAL_STATE_ADMISSION = NOT_ADMITTED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`

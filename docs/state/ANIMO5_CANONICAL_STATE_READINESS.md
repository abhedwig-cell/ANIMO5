# ANIMO-STATEQ01 canonical state readiness

Work unit: `ANIMO-STATEQ01`

Status: `QUALIFIED_CANONICAL_STATE_READINESS_MATRIX_STATE_ADMISSION_STILL_BLOCKED`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## 1. Scope and decision

STATEQ01 defines a feature- and application-envelope-scoped readiness model for persistent ANIMO5 state at an accepted transaction boundary. It does not admit canonical STATE, change physics, repair legacy restart behaviour or implement production state containers.

The current conclusion is deliberately narrower than the first STATEQ01 closeout. A restricted `CORE_CNP_SUBSURFACE_ONLY` profile can be specified as a readiness candidate only if layer-0 aqueous solute activation is explicitly outside the application envelope and that invariant is enforceable fail-closed. General `CORE_CNP`, in which layer-0 aqueous state may activate, is not state-complete while TCD-016-C1 remains scientifically unresolved.

Optional crop, stable-DOM, macropore and GHG profiles remain independently guarded. The matrix architecture is qualified as a readiness model only. No profile has B3 STATE admission.

## 2. Evidence basis

STATEQ01 reconciles, without evidence-strength upgrade, the following streams:

- RG02-G5 independent-stream attachment;
- PREP06 conserved-state inventory and observer separation;
- PREP12 provenance-preserving restart-continuity rehome;
- ARCH01 state ownership;
- ARCH02 checkpoint sufficiency;
- ARCH04 feature/state allocation;
- TS01 legacy temporal semantics;
- TIME01 accepted-boundary transaction semantics;
- ARCHG01/ARCHG02 architecture reconciliation;
- MP02 complete-case macropore evidence;
- GHG01 GHG state/restart qualification;
- SQ01 TCD-016 scientific-state qualification.

PREP12 source-local labels `TCD-032`, `TCD-033` and `TCD-034` are not canonical TCD allocations. STATEQ01 consumes only their RG02 reconciliation keys and leaves canonical allocation to B3 governance.

## 3. State classes

The machine-readable matrix uses these readiness classes:

- `CORE_STATE_READY_CANDIDATE`;
- `OPTIONAL_FEATURE_STATE_READY_CANDIDATE`;
- `FEATURE_STATE_BLOCKED`;
- `EXTERNAL_OWNER_REFERENCE`;
- `DERIVED_RECOMPUTABLE`;
- `NUMERICAL_CONTINUATION`;
- `DIAGNOSTIC_ONLY`;
- `UNRESOLVED_SCIENTIFIC_STATE`.

A readiness class is not an admission class.

## 4. Accepted-boundary semantics

TIME01 supplies the governing transaction boundary. Accepted state at `t0` is immutable while a modern trial executes. Same-step management mutation belongs to the trial, potential-pass results are provisional and only the completed actual result can become the next accepted generation.

TS01 shows that revision 53 implements this only implicitly. Middle-step continuation is staged by the next `Init`, while the final interval is serialized directly from result fields without another ordinary `Init`. STATEQ01 therefore defines acceptance logically: after the actual interval result satisfies the acceptance barrier, it is the candidate accepted state at `t1`; checkpoint serialization merely observes that accepted state.

## 5. Core soil state and external hydrology ownership

PREP06/PREP12 support persistent soil-layer ownership for fresh organic matter, humus, exudate-derived humus, exudate organic matter, labile dissolved organic C/N/P, aqueous mineral N, aqueous/site-resolved mineral P and precipitated P.

Hydrological quantities such as soil water, ponding, snow, interception and required temperature coordinates are external-owner state. ANIMO checkpoints bind the exact compatible accepted hydrology/thermodynamic frame rather than creating competing physical ownership.

Adsorbed NH4 is physical nitrogen storage but PREP12 shows it need not be serialized as an independent checkpoint coordinate if deterministic reconstruction from accepted aqueous NH4, hydrology/soil state and the admitted sorption relation is later split-run qualified. STATEQ01 therefore records it as `DERIVED_RECOMPUTABLE` for checkpoint representation, not as absent from the nitrogen control volume.

Site-resolved P state remains the candidate canonical coordinate. Legacy `Output_Init` canonicalizes P initialization origins to explicit `Inpo=1`; trajectories originating from `Inpo=2/3` still require separate split-run qualification.

## 6. Surface-state topology correction

The first STATEQ01 matrix incorrectly conflated two different revision-53 families:

1. virtual management/addition reservoirs `Con*top/Rscon*top`;
2. actual layer-0 aqueous coordinates in the normal dissolved-state arrays.

SQ01 shows that TCD-016 concerns the second family. The natural finding is a layer-0 aqueous NH4 wet-to-low-storage transition for which no admitted dry/non-aqueous continuation owner exists. The artificial addition reservoir cannot be reused as that owner because its provenance and release semantics differ.

STATEQ01 therefore separates:

- soil dissolved state, layers `1..Nl`;
- layer-0 aqueous state, activated by surface hydrology;
- management/addition reservoir state, `Con*top/Rscon*top`.

The proposed SQ01 `M_surface_NH4_non_aqueous_continuation` remains `UNRESOLVED_SCIENTIFIC_STATE`. It is not created, initialized, restored or treated as canonical.

This correction means general `CORE_CNP` is blocked on TCD-016-C1. A narrower `CORE_CNP_SUBSURFACE_ONLY` remains a readiness candidate only under an explicit no-layer0-activation envelope.

## 7. Crop state and continuation

ANIMO-owned crop root/shoot dry matter and cumulative actual N/P are persistent crop-owner candidates when `crop_mode=animo`.

PREP12 sharpens the restart blockers:

- `RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION`: actual uptake is present in `>orgpla:` but the restart initialization dataflow overwrites the restart value in the wrong direction;
- `RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE`: cumulative potential N/P is carried between ordinary timesteps and used by later demand logic, but has no restart representation and is reset to zero.

Potential uptake is not a conserved crop stock, but it is continuation-critical accepted state. Additional crop demand/deficit/stage/rotation continuation identified by TS01 still requires minimization and source qualification.

The crop profile therefore remains blocked. Source-local PREP12 TCD numbers are not promoted to canonical TCDs.

## 8. Management continuation

The event schedule identity is immutable configuration. Progress through it is accepted continuation metadata. TS01 shows that reader/cursor quantities such as `Adnr` and `Tinead` are not represented in `INITIAL.OUT`, while same-row event order is temporally material.

A canonical checkpoint must therefore either serialize an exact next-event identity/cursor or use a deterministic reconstruction rule that is independently split-run qualified. Event replay or event skipping on restore is a hard failure.

## 9. Macropores

Macropore water is hydrology-owned external state. Macropore solutes are ANIMO persistent process state when the feature is active.

Two blockers must remain distinct:

- TCD-025: main/public macropore control-volume and transfer/direct-drainage integration gap;
- `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER`: persistent macropore solute state is read and carried between timesteps, but the corresponding `Output_Init` writer blocks are commented out.

The second finding is PREP12 source-local `TCD-032`, not a canonical allocation. `CORE_CNP_WITH_MACROPORES` fails closed on both blocker families.

## 10. GHG state

GHG01 supports total `CsCH4` and `CsN2O` as owner coordinates, but matching restart labels do not establish sufficient restart semantics. Legacy restoration reconstructs phase partition using `Terf`, has a layer-0 ponding gap and contains hidden cross-call task locals whose intended persistence remains unresolved.

STATEQ01 therefore keeps GHG owner state feature-blocked. Dissolved/gas phase views may be `DERIVED_RECOMPUTABLE` only after an admitted deterministic reconstruction contract exists. Hidden task locals are not canonized as physical state.

## 11. `INITIAL.OUT` is evidence, not the canonical checkpoint

Legacy `INITIAL.OUT` serializes many end-state fields, but it does not bind schema, configuration, layout, external owner generations or complete continuation metadata. It omits active macropore restart state, does not establish complete crop continuation, and GHG restoration is not behaviourally qualified.

`Output_Init` also has a negative crop-P clamp that can mutate the result before writing. A canonical checkpoint serializer must be observationally pure.

## 12. Diagnostic continuation

Balance/report accumulators remain `DIAGNOSTIC_ONLY`. They do not own physical state and cannot repair a missing physical store or transfer.

Exact mid-report-period output continuation may add a separate versioned observer section. Report rollover does not define a physical acceptance boundary.

## 13. Feature/application profiles

The corrected profile matrix contains at least:

- `CORE_CNP_SUBSURFACE_ONLY`: restricted readiness candidate under an enforceable no-layer0 aqueous activation envelope;
- `CORE_CNP`: general surface-capable core, blocked on TCD-016-C1;
- `CORE_CNP_WITH_ADDITION_RESERVOIRS`: structurally adds separate `TOP-*` reservoir state but inherits the general-core surface blocker;
- `CORE_CNP_WITH_CROP`: blocked by explicit PREP12 crop restart findings plus unresolved continuation minimization;
- `CORE_CNP_WITH_EXTERNAL_CROP`: restricted-core candidate requiring exact external crop frame admission;
- `CORE_CNP_WITH_STABLE_DOM`: blocked on stable-DOM science/discrepancy qualification;
- `CORE_CNP_WITH_MACROPORES`: fail closed on TCD-025 plus the independent PREP12 restart-writer finding;
- `CORE_CNP_WITH_GHG`: fail closed on GHG restart/phase/task-state blockers;
- `CORE_CNP_WITH_REPORT_CONTINUITY`: restricted physical profile plus separate optional observer continuation.

Profile names are declarative readiness envelopes, not claims that revision 53 exposes identical feature switches.

## 14. Admission consequence

Canonical STATE remains `NOT_ADMITTED` because at minimum:

1. no B3-admitted uninterrupted-versus-split portable restart exists for even the restricted core profile;
2. the restricted core requires a formally enforceable no-layer0 activation envelope;
3. general core is blocked on TCD-016-C1;
4. management continuation reconstruction/cursor semantics are not split-run qualified;
5. P `Inpo=2/3` origin to explicit-state restart is unqualified when those modes are in scope;
6. crop restart and continuation blockers remain open;
7. stable DOM, macropore and GHG feature profiles remain independently blocked;
8. PREP12 local findings still require B3 canonical intake/allocation.

Final disposition:

`QUALIFIED_CANONICAL_STATE_READINESS_MATRIX_STATE_ADMISSION_STILL_BLOCKED`

`CANONICAL_STATE_ADMISSION = NOT_ADMITTED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`

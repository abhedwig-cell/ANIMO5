# ANIMO-RG04 Project Regie

Work unit: `ANIMO-RG04`

Branch: `work/animo-rg04-state-mass-b2-reconciliation`

Starting parent: `ANIMO-RG03@820ba9a9bbc90aceb892ac9ac36ecf7fb782b136`

Status target: `QUALIFIED_LATE_WAVE_STATE_MASS_B2_RECONCILIATION_NO_ADMISSIONS`

Production migration: `NOT_ADMITTED`

## Purpose

RG04 is a new governance checkpoint after RG03. It exists because the late evidence wave materially changed the project state and should not be folded indefinitely into an already closed RG03 record.

RG04 reconciles, without increasing evidence strength:

- `ANIMO-STATEQ02` restricted-core executable split-run qualification;
- `ANIMO-MASSQ02` residual causality reconciliation and typed-event projection;
- `ANIMO-B3I03` post-MASSQ02 intake and the append-only canonical registration of `TCD-042`;
- the current `ANIMO-PREP02R` recovery state after receipt of the supplied Intel project metadata and native executable;
- current TCD-015, TCD-017, TCD-018 and TCD-027 admission-readiness states;
- `ANIMO-B3A03R` as a technical review recheck that explicitly fails the independence gate and prepares a separate handoff;
- the newly opened `ANIMO-UBQ01` TCD-042 atomization workunit.

RG04 changes no physical model, frozen source, frozen testbank, scientific equation, corrected-legacy behaviour, canonical runtime implementation, B3 admission, B4 baseline or production code.

## Authority rule

RG04 inherits RG03 governance and selects newer authority from explicit status/decision artifacts and live branch heads. A later branch name alone is never authoritative.

The canonical discrepancy identity surface is now:

`work/animo-b3i03-canonical-register-append@814ea660d367494432beb63ea78298d1f6cd73d7`

with canonical tail:

`TCD-042`

The append is explicitly append-only, preserves the pre-existing logical rows and performs no scientific admission.

## Historical fidelity track

PREP02R is no longer accurately described as merely lacking all native/build evidence.

Current authority:

`work/animo-prep02r-historical-reference-recovery@60f3c57a3299a1890b4cdd66befd5a120a306383`

Current decision:

`PARTIAL_RECOVERY_BUILD_CONTRACT_STRONGLY_IMPROVED_MODERN_NATIVE_REBUILD_IDENTIFIED_HISTORICAL_REFERENCE_STILL_BLOCKED`

The supplied artifacts materially improve the build contract:

- `animo41.vfproj` identifies Intel Fortran project settings including eight-byte default REAL and SAVE/static local storage;
- `animo41.exe` is a PE32+ x64 Windows console executable and is useful for cross-runtime diagnostics;
- the executable is demonstrably a 2026 development rebuild, not the missing historical 4.1-era release oracle.

Therefore:

- `G6H` remains not passed;
- the modern native executable may not substitute for historical B2;
- `G6U` remains ineligible because the prepared archival/external request has still not been sent and the acquisition effort is not closed.

This is progress in provenance and runtime-contract knowledge, not progress to historical behavioural truth.

## Canonical STATE track

STATEQ02 is a genuine change from RG03's state picture.

Current authority:

`work/animo-stateq02-restricted-core-executable-split-run@ada93a409aa054f9aebac32728e79f80468215a7`

Decision:

`QUALIFIED_RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_CANONICAL_STATE_ADMISSION_PENDING`

For profile `RESTRICTED_CORE_CNP_WITH_EXTERNAL_CROP_SURFACE_EXCLUDED`, the natural `LWKM_gras_1040.2021.2045` witness now has executable evidence for:

`continuous run == run -> accepted boundary -> exact checkpoint -> restore -> continue`

at five accepted boundaries. Comparisons are exact/bitwise with no tolerance. Split 67 reproduces all 833 remaining accepted records exactly.

This is not whole-model STATE admission. The qualified profile excludes GHG, macropores, TCD-016-C1 dry-solute continuation, the nonzero TCD-040 layer-0 restart path, unresolved internal-crop restart state, active stable-DOM state and active P-class state.

STATEQ02 therefore changes `GSTATE` from readiness-only to executable restricted-core qualification, while canonical STATE admission remains pending.

## Canonical MASS track

MASSQ02 also materially changes the mass-gate picture.

Current authority:

`work/animo-massq02-residual-causality-typed-events@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`

Decision:

`QUALIFIED_TYPED_MASS_EVENT_PROJECTION_AND_RESIDUAL_RECONCILIATION_MASS_ADMISSION_PENDING`

For the current evidence set:

- all 23 nonzero residual records are classified;
- unexplained residual count is now zero;
- 6 map to known TCD context;
- 2 are reporting-semantic differences TCD-017/TCD-018;
- 15 are newly causal findings;
- no acceptance epsilon or residual correction was introduced.

The typed transfer projection is qualified as a candidate owner/event model. It is not an implemented or admitted canonical runtime event journal.

MASSQ02 therefore closes the previous unexplained-residual blocker but does not admit GMASS. Remaining blockers include governed disposition of causal findings, existing TCD constraints, executable nested soil/crop state-plus-event closure, active macropore/GHG completeness and whole-system elemental carbon scope.

## TCD-042

B3I03 reconciled the 15 MASSQ02 causal findings. It reserved exactly one new fail-closed discrepancy, `TCD-042`, and left ten findings without a new ID because evidence was insufficient for an atomic discrepancy claim.

`TCD-042` concerns the upper-boundary precipitation/deposition solute transaction at zero top throughflow. The observed RuurloGrass N residual matches the booked precipitation/deposition input, while the zero-throughflow UBoundconc branch retains the prior top concentrations.

The corrected semantics are not selected. TCD-042 still requires atomization between possible accounting-only, persistent-state and local-transfer interpretations.

`ANIMO-UBQ01@f3500990e7eaa1f5c02c6093186eb1ac369c5a42` is only an in-progress persisted checkpoint and creates no admission.

## Process-scoped B3 readiness

Four atomic readiness dossiers are complete but not admitted:

- TCD-015, Class B;
- TCD-017, Class A;
- TCD-018, Class A;
- TCD-027, Class A.

All four remain blocked by a valid admission route. Independent second-line review is also still pending. In TCD-018, B3A03R performed a technical recheck but explicitly records that it is not independent because it was executed in the same authoring context; a separate handoff has been prepared.

The remaining direct readiness queue remains TCD-023, TCD-024, TCD-026, TCD-030, TCD-038, TCD-040 and TCD-041.

## Gate reading

| Gate | RG04 state | Meaning |
|---|---|---|
| G6H | PARTIAL_RECOVERY_HISTORICAL_B2_NOT_PASSED | Build/runtime contract evidence improved; historical behavioural oracle still absent. |
| G6U | NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED | External archival request remains unsent. |
| G7 | NO_ATOMIC_SCIENTIFIC_ADMISSIONS_YET | Four readiness dossiers complete; route/review pending; TCD-042 atomization open. |
| GSTATE | RESTRICTED_CORE_EXECUTABLE_SPLIT_RUN_QUALIFIED_ADMISSION_PENDING | Exact split-run semantics qualified for a declared restricted profile only. |
| GTIME | CONCRETE_CANDIDATE_QUALIFIED_ADMISSION_BLOCKED | TIME02 remains a candidate; RG04 does not promote canonical TIME. |
| GMASS | TYPED_EVENT_AND_RESIDUAL_CAUSALITY_QUALIFIED_ADMISSION_PENDING | Unexplained residuals closed for current evidence; runtime journal and feature closure remain open. |
| GEX | SYNTHETIC_CONTRACT_FIXTURE_QUALIFIED_REAL_ADAPTER_BLOCKED | No new real producer-adapter admission. |
| GARCH | QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED | Candidate architecture remains ready, not production-admitted. |
| B4(profile) | NOT_ADMITTED | No composition from readiness-only upstream results. |
| PRODUCTION | NOT_ADMITTED | No production migration. |

## Immediate work ordering

The current highest-leverage non-conflicting work is:

1. continue UBQ01 until TCD-042 is atomized or fails closed;
2. execute the real PREP02R archival acquisition action; the modern native rebuild does not remove that need;
3. preserve and independently review the four completed readiness dossiers instead of redoing them;
4. open remaining atomic readiness work where capacity exists;
5. keep feature-scoped state and mass admission work separate from whole-model claims.

RG04 itself must not admit any correction or canonical gate.

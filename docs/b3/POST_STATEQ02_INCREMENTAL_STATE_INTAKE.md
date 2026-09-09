# ANIMO-B3I04 — Post-STATEQ02 Restricted-Core State Evidence Intake & Prior Split-Run Artifact Reconciliation

Status: `QUALIFIED_POST_STATEQ02_INCREMENTAL_STATE_EVIDENCE_INTAKE_NO_NEW_TCD_NO_ADMISSIONS`

Branch: `work/animo-b3i04-stateq02-incremental-intake`

Canonical discrepancy authority at branch start:

`work/animo-b3i03-canonical-register-append@814ea660d367494432beb63ea78298d1f6cd73d7`

Canonical register tail at branch start: `TCD-042`.

STATEQ02 evidence head:

`work/animo-stateq02-restricted-core-executable-split-run@ada93a409aa054f9aebac32728e79f80468215a7`

STATEQ02 status:

`QUALIFIED_RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_CANONICAL_STATE_ADMISSION_PENDING`

## Purpose

B3I04 is an incremental discrepancy-intake pass over the newly completed STATEQ02 evidence. It does not reopen B3I02 or B3I03, does not perform canonical STATE admission and does not change production code.

The question is narrow: does STATEQ02 establish any new scientific discrepancy identity, retire or reclassify any earlier local restart finding, or strengthen an existing canonical route?

## STATEQ02 evidence boundary

STATEQ02 provides direct hash-pinned executable evidence for the restricted profile:

`run -> accepted boundary -> exact checkpoint -> restore -> continue`

The natural witness is `LWKM_gras_1040.2021.2045` with C/N/P, P active, external crop continuation, detailed external hydrology, nonzero upper-boundary reservoirs, management continuation and exact accepted-state comparison.

Five accepted split boundaries, 66, 67, 68, 71 and 72, restore exactly and continue with exact bitwise physical trajectories. Split 67 reproduces the entire remaining 833 accepted records exactly. No comparison tolerance is used.

The qualified profile remains restricted. It explicitly excludes GHG, macropores, TCD-016-C1 dry-solute continuation, the nonzero TCD-040 layer-0 aqueous restart path, unresolved internal-crop restart state, active stable-DOM state, active P-class state and report accumulators as physical owners.

Therefore this evidence cannot support a whole-model STATE claim.

## Incremental finding reconciliation

### 1. TCD-040 activation sentinel

STATEQ02 natural step 282 has positive surface storage and nonzero layer-0 dissolved restart coordinates. The qualification route rejects the checkpoint before creation with exit code 95. No value is clipped, zeroed or accepted through a tolerance.

Disposition:

`EXISTING_TCD`

Canonical route:

`TCD-040`

This is executable boundary evidence for the already registered layer-0 aqueous restart-initialization discrepancy. It is not a new mechanism and does not justify a child TCD.

### 2. Earlier first-post-restart Pn divergence

STATEQ01 previously observed one first-post-restart surface-frame mismatch in the external-crop split route: uninterrupted `Pn=0` versus restarted `Pn=5e-5 m`. B3I02 correctly left that observation uncanonicalized because single-cause attribution was not yet available.

STATEQ02 now rebinds external hydrology by replaying the immutable hydrology stream to the exact accepted frame index before continuation. In that route, `Pnt`, `Snt`, `Sict`, `Walet` and all `Mofrt` coordinates are exact at restore and throughout every compared future record. The STATEQ02 qualification explicitly records that the earlier `Pn=5e-5` seam is absent.

B3I04 therefore reclassifies the earlier local observation as:

`RUNTIME_HAZARD_NO_SCIENTIFIC_TCD`

The qualified claim is limited to restart/hydrology-frame binding in the earlier qualification route. B3I04 does not infer a new physical or scientific model defect and does not allocate a TCD.

### 3. Earlier final-state divergence

STATEQ01 also observed a non-byte-identical final checkpoint after the earlier external-crop split, with differences in `ammoni`, `humorg`, `inipho`, `nitrat`, `orgfsh` and `orgsol`.

STATEQ02 is strong negative evidence against a generic restricted-core checkpoint-completeness defect: within its guarded profile, accepted restore snapshots and future physical trajectories are exact, including the full 833-record remainder from split 67.

However, STATEQ02 does not reproduce and causally decompose the exact older formatted/external-crop restart route that produced those six final-state differences. The earlier final-state observation therefore remains:

`INSUFFICIENT_EVIDENCE_PENDING_CAUSAL_ISOLATION`

No TCD is allocated from this symptom.

## Resp_miner diagnostic observation

STATEQ02 explicitly does not retain the intermediate `Resp_miner` hidden-context hypothesis as a STATEQ02 blocker. The final hash-pinned exact campaign gives no basis for creating a new scientific TCD from that provisional diagnostic observation. Any independent source-quality concern remains owned by the BUILDQ/B3 intake process.

Disposition in B3I04:

`NO_NEW_TCD_FROM_INTERMEDIATE_DIAGNOSTIC_HYPOTHESIS`

## Collision and reservation decision

The canonical register already contains `TCD-042` under B3I03 authority. A fresh incremental collision check therefore treats `TCD-043` as the next observed unallocated identifier only.

No STATEQ02 finding crosses the threshold for a new canonical scientific discrepancy identity. Consequently:

`reservations = []`

`TCD-043 reservation = false`

`canonical register append = false`

## Admission boundary

B3I04 performs no scientific admission, no corrected-legacy admission, no canonical STATE admission and no production migration.

The exact STATEQ02 result remains:

`restricted-core executable checkpoint semantics = QUALIFIED`

`canonical STATE admission = PENDING`

`whole-model STATE claim = false`

`production implementation = NONE`

## Final decision

The new STATEQ02 evidence strengthens existing state/restart governance without creating a new TCD:

- the active layer-0 rejection sentinel strengthens existing `TCD-040` scope;
- the earlier first-post-restart `Pn=5e-5` observation is reclassified as a runtime/rebind hazard rather than a scientific TCD candidate;
- the earlier six-coordinate final-state divergence remains insufficiently isolated;
- the provisional `Resp_miner` hypothesis does not become a TCD;
- `TCD-043` is not reserved.

Final status:

`QUALIFIED_POST_STATEQ02_INCREMENTAL_STATE_EVIDENCE_INTAKE_NO_NEW_TCD_NO_ADMISSIONS`

# ANIMO-BUILDQ03 — B3 governance handoff

Status: `EVIDENCE_STRENGTHENING_FOR_TCD011_PLUS_ONE_SEPARATE_RUNTIME_INITIALIZATION_HAZARD`

## Canonical context

BUILDQ03 operates under the existing B3I01 routing:

`GHG01-LCL-GHG-HIDDEN-TASK-STATE-PERSISTENCE -> TCD-011`

No new canonical TCD is requested for the GHG hidden-task-state family. BUILDQ03 provides stronger runtime-semantic evidence and a qualified explicit ownership model for active GHG hidden locals.

Authority checked at closeout:

- BUILDQ03 branch head lineage from `work/animo-buildq02-tcd011-storage-runtime-qualification@e7c675c6654026d5c12836f36f2fd347e9d547c2`;
- latest B3I01 head checked: `work/animo-b3i01-canonical-register-append@8e3ce76a3b842814d3f1e3bbebdcbf84e77768f3`;
- GHG01 evidence head: `dac7b7b5c591b781b82ec968896edb5957664c88`.

## TCD-011 evidence strengthening

All six active GHG cross-call hidden-local families identified by GHG01 now have controlled B1 explicit-context qualification:

| Family | Semantic owner | Persistent ModelState | Controlled equivalence |
| --- | --- | --- | --- |
| `GHGponding` | scoped GHG ponding phase snapshot | no | confirmed |
| `CH4oxid` | CH4 nonlinear solver context | no | confirmed |
| `N2Oproreduc` + `NO3N2OReduc` | N2O nonlinear solver and correction context | no | confirmed |
| `GHGtransport` | gas transport branch and representation snapshot context | no | confirmed |
| `GHGtranssub` | fixed timestep transport coefficient context | no | confirmed |
| `GHGasses` | GHG timestep phase context | no | confirmed |

The principal governance consequence is narrower than a generic storage fix: compiler-retained lifetime is not itself the intended architecture. The retained information has routine-specific ownership and lifetime. None of these six families is qualified as checkpointed persistent physical state.

Requested canonical action:

`STRENGTHEN_EXISTING_TCD_011_GHG_EVIDENCE_ONLY`

Do not close TCD-011. Historical Intel project/storage semantics remain unresolved, and non-GHG TCD-011 families remain separate qualification scope.

## Runtime materiality now demonstrated

GNU diagnostic variants show that lost local lifetime can change physical or solver-visible behaviour, not merely reporting:

- `GHGponding`: NaN restoration of temporarily replaced layer-0 hydrology;
- `CH4oxid`: O0 crash and O2 false convergence;
- N2O solver/correction: false convergence and NaN finalization;
- `GHGtransport`: invalid Task-2 captured gas state;
- `GHGtranssub`: invalid Task-2 concentration results;
- `GHGasses`: loss of Task-1 phase projection before final N2O phase.

Explicit context reproduces the retained/static controlled reference in each qualified family.

This is B1 causal/runtime evidence only. It is not a historical Intel reference and does not admit corrected legacy behaviour.

## Separate new local runtime finding

BUILDQ03 also isolates:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

Phenomenon:

when `La < Nl`, `GHGasses` can read `Flair(Nl+1)` in the bottom-layer air-flow transformation without a source assignment to that slot. The resulting `Flaiio(Nl)`/`Flaiou(Nl)` values feed GHG gas transport and air-flow-dependent coefficient calculations.

Evidence:

- source-confirmed first-read gap;
- controlled GNU O0 probe produces NaN in affected bottom-layer flow terms;
- O2 happens to produce retained/static-like values in the controlled case;
- historical Intel effect unknown;
- no intended bottom boundary value is established by BUILDQ03.

The value `Flair(Nl+1)=0.0` was used only as a diagnostic control to isolate phase-context equivalence. It is not admitted as theory, historical behaviour or a correction.

Requested B3 disposition:

`RUNTIME_INITIALIZATION_HAZARD_PENDING_INTAKE`

BUILDQ03 does not request a new TCD. B3 should first decide whether the finding remains a build/runtime contract hazard, maps to an existing initialization/build discrepancy family, or warrants scientific discrepancy allocation after intended boundary semantics and state/flux materiality are independently established.

Do not merge it automatically with GHG science TCD-032 through TCD-037. Do not merge it automatically with TCD-011 either: the causal mechanism is conditional initialization, not cross-call storage duration.

## Admission state

`new_canonical_tcd_requested=false`

`tcd011_close_requested=false`

`historical_intel_equivalence_qualified=false`

`corrected_legacy_admitted=false`

`b3_scientific_admitted=false`

`production_migration_admitted=false`

## Handoff artifacts

Primary BUILDQ03 evidence:

- `docs/build/GHG_EXPLICIT_CONTEXT_QUALIFICATION.md`;
- `integration/animo-build/BUILDQ03_GHG_CONTEXT_MATRIX.json`;
- `integration/animo-build/ANIMO-BUILDQ03_STATUS.json`;
- persisted diagnostic reproduction assets under `tools/buildq03/`.

Gate:

`QUALIFIED_GHG_HIDDEN_TASK_CONTEXT_OWNERSHIP_AND_CONTROLLED_EQUIVALENCE_FLAIR_BOTTOM_BOUNDARY_RUNTIME_HAZARD_SEPARATE_HISTORICAL_INTEL_OPEN`

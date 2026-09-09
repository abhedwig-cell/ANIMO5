# ANIMO-B3I01 live post-G5 intake supplement 03

Status: `BUILDQ03_GHG_RUNTIME_EVIDENCE_ROUTED_NO_NEW_TCD_NO_ADMISSION`

This supplement consumes completed ANIMO-BUILDQ03 GHG runtime-semantic evidence. It strengthens existing `TCD-011` and routes one newly isolated runtime initialization hazard. It does not append to the canonical TCD register and does not admit corrected behaviour.

## Authority checked

B3I01 prior head:

`8e3ce76a3b842814d3f1e3bbebdcbf84e77768f3`

BUILDQ03 source head:

`work/animo-buildq03-ghg-task-context-qualification@8b1e4006be86eea344cf9f7da978218261ee1a15`

BUILDQ03 remains based on BUILDQ02 and keeps historical Intel storage semantics unresolved.

Canonical register tail remains:

`TCD-040`

No TCD-041 reservation is made by this supplement.

## 1. TCD-011 evidence strengthening

B3I01 had already routed the GHG01 umbrella hidden-task-state finding to existing `TCD-011`, local storage duration.

BUILDQ03 now provides controlled B1 qualification for all six active GHG hidden cross-call families:

| Family | Qualified explicit owner | Persistent ModelState? |
| --- | --- | --- |
| `GHGponding` | scoped GHG ponding phase snapshot | no |
| `CH4oxid` | CH4 nonlinear solver context | no |
| `N2Oproreduc` + `NO3N2OReduc` | N2O nonlinear solver and correction context | no |
| `GHGtransport` | gas transport branch and representation snapshot context | no |
| `GHGtranssub` | fixed timestep transport coefficient context | no |
| `GHGasses` | GHG timestep phase context | no |

The evidence changes the interpretation of TCD-011 materially. Compiler-retained storage duration is not an acceptable semantic owner. The information belongs to routine-specific transaction, phase or solver context. None of the six active families is qualified as accepted persistent physical state or restart state.

GNU diagnostics also show runtime materiality beyond reporting. Losing hidden context can produce NaN restoration, solver false convergence, crashes, invalid gas-state continuation and loss of phase projection. Explicit context reproduces the controlled retained/static reference in the qualified probes.

Canonical action:

`STRENGTHEN_EXISTING_TCD_011_EVIDENCE_ONLY`

TCD-011 remains open. BUILDQ03 does not establish historical Intel equivalence and does not qualify all non-GHG local-storage families.

## 2. New BUILDQ03 local runtime finding

BUILDQ03 isolates:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

The finding is distinct from the hidden cross-call lifetime family.

When `La < Nl`, `GHGasses` can read `Flair(Nl+1)` during the bottom-layer air-flow transformation before a source assignment to that array slot. The affected `Flaiio(Nl)` and `Flaiou(Nl)` values feed shared gas transport and air-flow-dependent coefficient calculations.

Evidence at intake:

- source first-read gap confirmed;
- controlled GNU O0 automatic-local execution produces NaN in the affected bottom-layer terms;
- O2 happened to produce retained/static-like values in the controlled case;
- downstream source path into `GHGtransport` and `GHGtranssub` is identified;
- historical Intel behaviour is unknown;
- intended scientific bottom-boundary value is not established.

BUILDQ03 used `Flair(Nl+1)=0.0` only as a diagnostic control to isolate phase-context equivalence. That value is not theory evidence, is not historical-reference evidence and is not admitted as a correction.

Canonical disposition at current evidence strength:

`BUILD_RUNTIME_INITIALIZATION_HAZARD_NOT_TCD_PENDING_BOUNDARY_SEMANTICS`

This is not automatically merged into TCD-011 because its causal mechanism is conditional initialization rather than cross-call lifetime. It is also not automatically merged into GHG science discrepancies TCD-032 through TCD-037.

A future qualification should first establish the intended bottom air-flow boundary semantics, activation envelope and unrounded state/flux materiality. Only after that should governance decide whether the item remains a runtime contract hazard, maps to an existing TCD or requires a new scientific TCD.

## 3. Register and admission consequence

The canonical register is unchanged. Tail remains `TCD-040`.

No new TCD is allocated.

No production source is changed.

No diagnostic compiler setting is promoted to scientific semantics.

`new_corrections_admitted=false`

`b3_baseline_established=false`

`production_migration_admitted=false`

`evidence_strength_increased_by_routing=false`

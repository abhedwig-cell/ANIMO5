# ANIMO-BUILDQ03 — GHGasses phase context and bottom-boundary initialization probe

Status: `QUALIFIED_EXPLICIT_PHASE_CONTEXT_EQUIVALENCE_WITH_SEPARATE_BOTTOM_BOUNDARY_RUNTIME_HAZARD`

## Scope

This probe addresses the last active GHG hidden cross-invocation family left open by BUILDQ03: the Task-1 to Task-2 phase context in `GHGasses`.

It also records a separate same-invocation initialization hazard found while isolating that context. The two phenomena are kept separate:

1. hidden cross-call phase context is a `TCD-011` storage-duration issue;
2. `Flair(Nl+1)` can be read without a source assignment in a reachable air-flow topology and is a new local runtime candidate requiring B3 disposition.

No production correction or new canonical TCD is admitted here.

Frozen source ZIP SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank ZIP SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Diagnostic compiler:

`GNU Fortran 14.2.0`

## 1. Exact hidden cross-call phase context

Revision-53 `GHGasses` dispatches through separate Task 1 and Task 2 invocations.

Task 1 constructs temporary hydrology and air-flow projections. Task 2 later calls final N2O processing and consumes retained locals without recomputing them.

The exact hidden Task-1 to Task-2 family is:

- `Floux(0:Nl)`;
- `Mofrx(0:Nl)`;
- `Mofrsax(0:Nl)`;
- `Flaiib(0:Nl)`;
- `Flaiio(0:Nl)`;
- `Flaiou(0:Nl)`;
- `FlaiAtmos`.

Two earlier inventory details are refined here:

- `Flair` is a Task-1 helper only. It is not itself consumed after return and therefore is not cross-call context;
- `Mofrox` and `Mofrtx` are formal `GHGasses` arguments and are caller-visible. They are not hidden procedure-local state, although Task 1 can populate their temporary projection values for later Task-2 use.

Qualified hidden-context owner:

`GHG_TIMESTEP_PHASE_CONTEXT`

Persistent `ModelState` candidate:

`false`

The context exists between two GHG phases inside one accepted timestep. BUILDQ03 finds no basis for checkpoint ownership merely because the legacy implementation obtains lifetime through local retention.

## 2. Why direct recomputation is not yet the qualified representation

The Task-1 projection is generated before intervening nitrate and chemistry processing. Revision-53 top-level execution returns from `GHGasses(1,...)`, performs additional rates, transport, denitrification, crop/chemistry and correction calls, and then invokes `GHGasses(2,...)`.

Several projection inputs are formally available again at Task 2, so recomputation is a plausible future simplification. However, BUILDQ03 has not established that every required hydrological/macropore input is invariant across all intervening calls, nor that reprojection would be byte-equivalent in all activated GHG states.

Therefore the currently qualified migration surface is explicit threading of the seven Task-1 products, not silent Task-2 recomputation.

## 3. Controlled 16-case phase-context matrix

A synthetic B1 projection kernel was constructed from the revision-53 `GHGasses` hydrology/air-flow projection equations and `GHGMapohydro` calculations. It does not execute the full CH4/N2O subsystem and is not a B2 historical reference.

The matrix contains 16 cases varying:

- `IoptMp = 0/1`;
- ponding/air-cover branch state;
- saturated versus unsaturated air-flow topology;
- initial/final ponding moisture pattern.

Each case executes the Task-1 projection, returns, clobbers automatic local storage and then captures the values that Task 2 requires.

Diagnostic source identities:

- hidden-local projection kernel: `f6161e49bbfa62d7a0d2368cd49d43cde1291aa1c22580aff71cdf9b4e3e65ab`;
- explicit-context kernel: `dcf1c2923c5e49218cf69350b903fc10476e1bad383d879e87d84ee48f47e482`;
- hidden-local kernel with diagnostic bottom-boundary initialization: `bf5d3a368d3ee2f9e36d651e207814a25a31510f8b8bcf4df92228ce4f94f6d3`;
- explicit-context kernel with the same diagnostic boundary initialization: `2439d63bfe2dc9753dff7d302f7434117265609512ffc4832c59e08646eab9b2`;
- hidden-local driver: `107196e03c3fd1c06b667ea1ac1782e54fde5f2c7c6c908c54f3d6cdbfc242f3`;
- explicit-context driver: `900e2e477e69c416b544655b1669a9ae2009802ba1833f02d0456aae3d9212a6`.

Original retained/static O0 and O2 outputs are byte-identical across all 16 cases:

`c4f47a3e09b6087a37d7351dcea62aa103a4e2421e1a018693eba8d9edbfcc55`

The original hidden-local automatic-storage O0 and O2 variants both lose the phase context after return. With signalling-NaN initialization all captured Task-2 context members become NaN. Their common output SHA-256 is:

`411f2ee264dbdb4c3f5bd80eed58e17f131f610512bb57d7545113335febdc46`

Thus the Task-1 to Task-2 storage-duration dependency is independently runtime-material in this controlled projection kernel.

## 4. Separate finding: `Flair(Nl+1)` is not always initialized

While making the explicit-context candidate independent of static local storage, the O0 probe exposed a second phenomenon.

Revision-53 declares:

`Flair(Manl+1)`

Task 1 determines `La`, then executes:

`Flair(La+1) = 0.0`

followed by:

- a backward loop filling `Flair(La:1)`;
- a forward loop filling `Flair(La+2:Nl)`.

The later transformation loop executes for every `Ln=1..Nl` and evaluates:

`Flaiio(Ln) = -Min(0.0,Flair(Ln+1))`

`Flaiou(Ln) = Max(0.0,Flair(Ln+1))`

When `La < Nl`, the preceding assignments cover through `Flair(Nl)` but do not assign `Flair(Nl+1)`. The bottom-layer transformation at `Ln=Nl` nevertheless reads `Flair(Nl+1)`.

When `La=Nl`, `Flair(Nl+1)` is assigned by `Flair(La+1)=0.0`; therefore this is topology-dependent rather than unconditional.

Local reconciliation key:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

Qualified source classification:

`SOURCE_CONFIRMED_CONDITIONAL_UNINITIALIZED_LOCAL_BOUNDARY_SLOT`

The controlled automatic O0 explicit-context run without a separate boundary initializer produced NaN in bottom-layer `Flaiio`/`Flaiou`, while O2 happened to match the static reference. This optimization dependence is exactly why compiler or stack contents cannot be treated as a semantic initialization contract.

The downstream source path is direct: `Flaiio` and `Flaiou` enter `GHGtransport`/`GHGtranssub`, where they contribute to air-flow transport terms and fixed coefficients such as `Y2` and `Y3`. BUILDQ03 therefore establishes a source-level path from the uninitialized slot into numerical gas-transport state. It does not claim a historical whole-case magnitude because a qualified revision-53 historical GHG runtime remains unavailable.

Historical Intel effect:

`UNKNOWN`

Canonical disposition:

`PENDING_B3_RUNTIME_INTAKE_NO_NEW_TCD_REQUESTED_BY_BUILDQ03`

This finding must not be silently folded into the cross-call phase-context fix. One is storage duration across calls; the other is first-use initialization within Task 1.

## 5. Isolation of the two phenomena

To qualify the cross-call phase context independently, the synthetic diagnostic kernel was given one explicit boundary initialization:

`Flair(Nl+1) = 0.0`

This line is a diagnostic control only. It is not an admitted revision-53 correction and is not used to infer intended science. It isolates the storage-duration question by preventing an unrelated uninitialized local from contaminating the phase-context comparison.

With that diagnostic control:

- original hidden-local automatic O0/O2 still lose all Task-1 phase context after return;
- explicit seven-member phase context under automatic O0/O2 becomes byte-identical to the retained/static reference across all 16 cases;
- both explicit-context outputs have SHA-256 `c4f47a3e09b6087a37d7351dcea62aa103a4e2421e1a018693eba8d9edbfcc55`.

This supports the following narrow conclusion:

`EXPLICIT_GHG_TIMESTEP_PHASE_CONTEXT_EQUIVALENCE_SUPPORTED_WHEN_SEPARATE_BOTTOM_BOUNDARY_INITIALIZATION_HAZARD_IS_CONTROLLED`

It does not admit the boundary initializer itself.

## 6. Consequence for BUILDQ03 and TCD-011

All active GHG hidden cross-invocation families identified by GHG01/BUILDQ01 now have a qualified explicit owner and controlled explicit-context equivalence surface:

- `GHGponding`: scoped ponding snapshot;
- CH4 oxidation: nonlinear solver context;
- N2O production/reduction: nonlinear solver and correction context;
- `GHGtransport`: branch and representation snapshot context;
- `GHGtranssub`: fixed timestep transport coefficient context;
- `GHGasses`: timestep phase context.

This closes BUILDQ03's GHG hidden-context audit scope. It does not close canonical `TCD-011`, because historical Intel project storage semantics and non-GHG storage-duration families remain unresolved.

The new `Flair(Nl+1)` first-use finding is handed to B3 governance separately and does not increase evidence strength through routing alone.

## Gate

`QUALIFIED_GHG_HIDDEN_TASK_CONTEXT_OWNERSHIP_AND_CONTROLLED_EQUIVALENCE_FLAIR_BOTTOM_BOUNDARY_RUNTIME_HAZARD_SEPARATE_HISTORICAL_INTEL_OPEN`

`new_canonical_tcd_requested=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`

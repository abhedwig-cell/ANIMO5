# ANIMO-NQ02 — TCD-019 convergence study

Status: `DESIGN_PERSISTED_EXECUTION_PENDING`.

This study follows the NQ01 numerical-policy contract. No experiment may define a production tolerance from the observed legacy residual or from closeness to one B1 output.

## Primary case

Historical B0 testcase: `LWKM_gras_1040.2021.2045`.

Activated sorption scope in this case:

- fast sorption: Langmuir, one site;
- slow sorption: Freundlich, three sites;
- slow-Langmuir TCD-024 path: inactive.

The case is therefore suitable for TCD-019 causal and convergence study without the known TCD-024 wrong-index defect being naturally active.

## Capture contract

Every B1 descendant run must record:

- frozen source SHA-256 and testbank SHA-256;
- exact diagnostic patch or transformation identity;
- diagnostic source-tree or patch SHA-256;
- compiler identity and complete flags;
- executable SHA-256;
- testcase identity and execution-copy metadata;
- changed factor and unchanged factors;
- accepted/fallback branch path;
- iteration count and convergence reason where instrumented;
- `R_eq`, `R_cons`, and `R_constitutive`;
- `Rsc`, `Avc`, fast sorbed P, slow sorbed P and precipitated P;
- external P transfers and cumulative P ledger surfaces available from the case;
- run completion and any error/fallback event.

Unrounded scientific captures must follow the NQ01 precision and representation semantics. Ordinary rounded reports are not an oracle.

## Controlled experiment matrix

The initial matrix deliberately separates constitutive linearization from nonlinear stopping policy.

### Baseline

`NQ02-LWKM-000`

Frozen source logic, deterministic GNU B1 build contract, no scientific source modification.

### Small-delta switch refinement

One factor only: `Sorpfast` fast-sorption switch `abs(Ct-Ct0) < delta_switch`.

Planned sequence:

- `NQ02-LWKM-D1`: `1e-5`;
- `NQ02-LWKM-D2`: `1e-6` legacy baseline;
- `NQ02-LWKM-D3`: `1e-7`;
- `NQ02-LWKM-D4`: `1e-8`;
- `NQ02-LWKM-D5`: `1e-10`;
- `NQ02-LWKM-D6`: `1e-12`.

This sequence diagnoses switch sensitivity only. It cannot qualify a switch value because the exact constitutive secant provides a threshold-free mathematical alternative.

### Newton `Small` refinement

One factor only: `C_unl Small`.

Planned monotone sequence:

- `NQ02-LWKM-S1`: `1e-3`;
- `NQ02-LWKM-S2`: `1e-4` legacy baseline;
- `NQ02-LWKM-S3`: `1e-5`;
- `NQ02-LWKM-S4`: `1e-6`;
- `NQ02-LWKM-S5`: `1e-8`;
- `NQ02-LWKM-S6`: `1e-10`.

No member is a candidate tolerance until a stabilization envelope is demonstrated for equation residuals, conserved stores and relevant trajectories.

### Exact constitutive representation

`NQ02-LWKM-E1`

Replace only the small-delta Langmuir tangent representation with the exact cancellation-free constitutive secant and exact derivative, while retaining legacy nonlinear stopping policy. This experiment is valid only where the start fast-sorption store is on the constitutive relation. Any off-relation event must be captured and routed to TCD-014 rather than normalized away.

`NQ02-LWKM-E2`

Same exact constitutive representation, with solver refinement performed as a separate submatrix. This is the main route for deciding whether a threshold-free conservative formulation has a stable numerical solution.

### Stopping-criterion structure

The source uses signed `Vec` tests rather than `abs(Vec)`. A diagnostic experiment may replace only those signed comparisons with magnitude comparisons while leaving `Small` unchanged. This is not a proposed correction yet. Its purpose is to determine whether apparent convergence is materially affected by residual sign.

### Late-iteration and fallback characterization

Instrumentation-only runs must record:

- entry into iterations 16 to 20 where running-average corrections are used;
- minimum-residual `Avc_opt` capture;
- Newton exit reason;
- entry into bisection;
- bisection accepted residual and iteration count;
- `Recfso` values inherited at bisection entry;
- whether a recomputed adsorption/desorption selection would differ at any bisection trial.

No fallback-policy change is admitted in this work unit merely because another path has a lower residual.

## Precision study

The canonical deterministic GNU B1 build uses default REAL promoted to 8 bytes and static locals because the frozen source is sensitive to compiler defaults. NQ02 will preserve that path as the primary B1 execution contract.

Precision sensitivity must include, where technically feasible:

1. canonical GNU B1 path;
2. higher-precision independent evaluation of the local constitutive and residual formulas, without relabelling that evaluation as a historical executable;
3. if a compiler-supported higher-precision diagnostic source descendant is used, exact kind/flag changes and all interface consequences must be recorded.

A four-byte-default-REAL build is already known to produce unstable interface behaviour and NaNs under the current reconstructed build contract. It is therefore not a clean precision-only experiment unless the interface/build semantics are separately repaired and qualified.

## Time-step study

Time-step refinement is required only after a controlled method is defined that preserves the same forcing and event semantics. Directly editing timestep values in a historical testcase can alter process splitting and event timing. Such a run must therefore be labelled synthetic B1 and must not be interpreted as historical-reference evidence.

The study should compare aligned physical times and integrated P transfers, not merely final values.

## Decision logic

A route can become `CONVERGENT_POLICY_CANDIDATE` only if all applicable evidence shows:

- `R_eq` decreases or reaches a precision-consistent floor under refinement;
- `R_cons` loses the systematic formulation-driven bias rather than merely moving closer to zero by cancellation;
- accepted P state trajectories stabilize;
- branch/fallback behaviour is understood;
- precision sensitivity does not reveal an unresolved representation artefact;
- the result is not dependent on TCD-024 being silently changed;
- TCD-014 off-constitutive initialization is either absent in the tested segment or explicitly separated.

Otherwise classify as `LEGACY_NUMERICAL_POLICY_NONCONVERGENT_OR_BIASED`, `INSUFFICIENT_EVIDENCE`, `REFERENCE_DEPENDENT`, or `THEORY_DEPENDENT` as appropriate.

Current tolerance status: `TOLERANCE_NOT_YET_QUALIFIED`.

# ANIMO-NQ01 Numerical Policy Change Qualification

Status: `QUALIFICATION_CONTRACT_DEFINED_NO_NUMERICAL_CHANGE_ADMITTED`.

## Purpose

This document defines the minimum evidence required before ANIMO5 may admit a change to numerical policy.

Numerical policy includes more than a solver tolerance. It includes any implementation choice that can change the accepted trajectory while leaving the intended physical equations nominally unchanged.

This contract is intentionally separate from ordinary historical equivalence. A numerical change can disagree with B2 and still become a justified B3 correction, but only through explicit qualification. Conversely, a change that improves a mass balance is not automatically acceptable.

## In-scope numerical policy changes

A separate numerical qualification is required for changes to any of the following:

- nonlinear iteration method;
- nonlinear stopping tolerance;
- convergence norm;
- tangent or secant approximation;
- constitutive linearization;
- clipping or bounding;
- precision kind;
- mixed precision;
- fallback method;
- bisection or safeguarded iteration;
- order of evaluation;
- accumulation order;
- summation policy;
- time-step acceptance logic;
- retry or rollback logic;
- local iteration cap;
- underflow, overflow or exceptional-value handling when it affects accepted scientific state.

A formatting change, parser change or path compatibility change is not a numerical policy change unless it changes scientific values or accepted control flow.

## Required classification before implementation

Every candidate numerical change must declare:

- physical equations changed: `true` or `false`;
- constitutive relation changed: `true` or `false`;
- discrete control path may change: `true` or `false`;
- accepted state trajectory may change: `true` or `false`;
- ledger trajectory may change: `true` or `false`;
- output formatting only: `true` or `false`;
- precision representation changed: `true` or `false`;
- expected affected variables;
- expected unaffected variables;
- known discrepancy or theory motivation;
- B2 reference coverage available: `true` or `false`.

If the physical equations or constitutive theory change, this contract alone is insufficient. The work must also pass the scientific-admission route for a physics change.

## Evidence principle

A numerical-policy change must be justified against the governing numerical and scientific contract, not against the desire to match one observed output.

Evidence should distinguish:

1. historical behaviour;
2. equation-solving accuracy;
3. conservation behaviour;
4. precision behaviour;
5. temporal discretization behaviour;
6. trajectory effects;
7. control-flow effects;
8. process-level scientific consequences.

No single scalar metric can stand in for all eight.

## Prohibited acceptance arguments

The following arguments are insufficient by themselves:

- the new result has a smaller balance residual;
- the new result is closer to B1;
- the new result is closer to one rounded B2 report value;
- the new result uses a tighter tolerance;
- the new result uses more precision;
- the new method converges in fewer iterations;
- the final state changed only a little;
- no legacy warning was triggered;
- the change is numerically standard in another model.

Each can be supporting evidence, but none is an admission argument on its own.

## Baseline evidence required

Before a changed numerical policy is qualified, preserve the unchanged baseline for the same case and process scope.

Where B2 exists, preserve:

- B2 raw outputs and capture;
- B2 trajectory records;
- B2 control-flow and solver-path records where exposed;
- B2 precision metadata.

Where B2 does not exist, use the strongest available evidence but explicitly mark the historical uncertainty. B1 remains diagnostic and cannot be relabelled B2.

For a B3 fallback without B2, the stronger independent scientific-admission requirements from the B0 to B4 governance model still apply.

## Minimum convergence evidence

A future numerical change must perform the following studies when technically relevant.

### 1. Tolerance refinement study

Required when a convergence or stopping parameter exists.

Run a monotone sequence of stricter solver tolerances over a range wide enough to reveal whether accepted scientific quantities stabilize.

Record for every refinement level:

- solver tolerance value;
- iteration count;
- fallback use;
- nonlinear residual;
- conservation residual;
- accepted state values;
- important fluxes;
- cumulative ledgers;
- run failures or branch changes.

Do not define the production tolerance as the largest value that happens to reproduce one baseline output.

A qualified tolerance needs a plateau or convergence argument tied to scientific quantities and solver correctness.

### 2. Time-step refinement study

Required when the changed policy interacts with time discretization, process splitting, cumulative transfers, event timing, nonlinear convergence per step, or a time-step dependent constitutive approximation.

Use at least one meaningful refinement sequence where the driving inputs permit it.

Compare:

- state trajectories at aligned physical times;
- integrated external fluxes;
- cumulative ledgers;
- event timing;
- process-specific transfers;
- final states.

A time-step study is not required for a strictly local change that can be proven independent of time discretization, but that exemption must be argued explicitly.

### 3. Precision sensitivity study

Required when:

- variable kind changes;
- compiler default precision changes;
- summation order changes materially;
- the discrepancy is close to precision limits;
- a solver uses cancellation-prone expressions;
- B1 and B2 differ in low-level floating representation.

At minimum characterize the canonical precision path and one higher-precision or independently evaluated check where technically feasible.

Record whether differences scale with precision, remain invariant, or reveal a separate formulation issue.

Precision improvement is supporting evidence, not automatic acceptance.

### 4. Solver path characterization

Required when nonlinear iteration or fallback behaviour can change.

Capture:

- initial guess;
- iteration count;
- residual sequence where practical;
- accepted convergence condition;
- fallback or bisection activation;
- clipping or bound activation;
- branch identifiers;
- final accepted solution.

A changed path with the same final printed value is still a real numerical difference and may matter for nearby cases.

### 5. Conservation convergence

Required for processes that transfer conserved C, N, P or water-coupled mass.

Check whether local and cumulative conservation residuals converge consistently with numerical refinement.

The study must separate:

- exact ledger structure;
- constitutive storage evaluation;
- nonlinear equation residual;
- transport balance residual;
- reporting roundoff.

A legacy residual must not become the acceptance tolerance.

### 6. Trajectory convergence

Required whenever accepted state can change.

Assess at least:

- initial state;
- post-process state;
- accepted end-of-step state;
- cumulative period balances;
- final state.

For nonlinear P or coupled nutrient processes, assess the coupled downstream quantities that respond to the changed state.

Final-value agreement alone is insufficient if intermediate differences can cancel.

## Change-specific evidence matrix

| Change family | Minimum additional evidence |
| --- | --- |
| nonlinear stopping tolerance | tolerance refinement, solver path, trajectory convergence, conservation convergence |
| tangent or secant approximation | constitutive identity, tolerance refinement where solver-coupled, trajectory convergence, conservation convergence |
| clipping or bounds | activation frequency, pre and post values, conservation impact, scientific admissibility of the bound |
| precision kind | precision sensitivity, raw representation characterization, trajectory and ledger sensitivity |
| fallback method | solver path characterization, failure envelope, accepted-solution comparison |
| order of evaluation | precision sensitivity, reproducibility, trajectory and ledger sensitivity |
| summation policy | accumulation-order sensitivity, ledger closure, deterministic reduction contract |
| time-step acceptance | time-step refinement, retry-path characterization, trajectory and ledger convergence |

## Tolerance qualification architecture

NQ01 intentionally defines no scientific numerical thresholds.

A future tolerance artifact must be scoped to a named quantity or quantity family and must record:

- variable class;
- quantity identifier;
- units;
- applicable state, layer, species or process scope;
- comparison metric;
- absolute threshold if used;
- relative threshold if used;
- near-zero policy;
- temporal aggregation rule;
- evidence basis;
- convergence-study artifact identity;
- precision-study artifact identity when relevant;
- reviewer or qualification decision;
- validity limits.

A tolerance artifact is invalid if its evidence basis is only an observed B1 to B2 difference or the maximum legacy residual.

Global catch-all tolerances are prohibited unless a later independent qualification establishes a defensible common scale, which is not presently expected for ANIMO's heterogeneous states and fluxes.

## Exact versus approximate acceptance

### Exact equality required

Exact equality remains mandatory for:

- option state;
- branch identifiers when same-path equivalence is claimed;
- integer indices;
- species identity;
- state and ledger keys;
- ledger member and sign mapping;
- input and artifact hashes;
- declared period boundaries;
- count and identity of accepted steps when that is part of the claimed equivalence.

### Approximate numerical equality may be admissible later

Approximate acceptance can be scientifically reasonable for:

- physical floating state across qualified compilers;
- fluxes computed through different but mathematically equivalent floating evaluation paths;
- nonlinear residuals;
- cumulative floating ledgers;
- solver iterates.

But approximate acceptance is only valid after a quantity-specific or process-specific policy has been qualified.

The existence of floating-point arithmetic does not itself create a tolerance.

## Historical equivalence versus numerical improvement

Three outcomes must remain distinct.

### Historical preservation

A changed implementation reproduces B2 under the qualified comparison criteria.

This supports preservation, not necessarily scientific correctness.

### Corrected numerical legacy behaviour

A changed implementation intentionally differs from B2, but the difference is admitted because stronger numerical and scientific evidence establishes a defect or inferior numerical policy in the historical path.

This requires explicit expected-difference records and B3 disposition.

### New numerical evolution

A changed implementation is not merely a legacy correction and introduces a new algorithmic policy for ANIMO5.

This requires a broader scientific and numerical admission. It must not be smuggled into B3 as equivalence work.

## Special contract for TCD-019 nonlinear P conservation

Existing diagnostic evidence localizes a recurring PO4 conservation drift to numerical policy in `Transorp`, especially the small-delta Langmuir tangent substitution combined with nonlinear stopping policy.

The current evidence is B1 causal evidence. It does not establish B2 historical reproduction and does not admit a correction.

A future TCD-019 qualification must include, at minimum:

- unrounded frozen-reference P states and ledgers where B2 can expose them;
- exact constitutive storage identity for linear, Langmuir and Freundlich options;
- comparison of actual start and end stored P with the storage change represented in the solve;
- solver tolerance refinement;
- solver path characterization;
- conservation convergence;
- aqueous PO4 trajectory;
- fast sorbed P trajectory;
- slow sorbed P trajectory;
- precipitated P trajectory;
- external P fluxes;
- plant uptake where active;
- cumulative P ledgers;
- coupled downstream N and organic-matter outputs where affected;
- initialization interaction with the separate TCD-014 policy;
- multi-case coverage rather than one LWKM case only.

A mass-balance improvement is expected supporting evidence, but is not the acceptance criterion by itself.

## Non-interference requirement

When a numerical correction is intended to affect one process path, quantify what remains unchanged.

Non-interference evidence should cover, where technically applicable:

- unaffected species;
- unaffected layers or process options;
- cases that do not activate the changed branch;
- input parsing;
- external boundary forcing;
- unrelated ledger structures;
- event timing outside the changed solver path.

Bitwise identity is preferred for truly unaffected discrete and report surfaces when practical. For floating coupled quantities, use the same qualified comparison policy that applies to their class.

## Fail-closed decision states

A numerical-policy work unit may conclude with one of the following:

- `CHARACTERIZED_NOT_QUALIFIED`;
- `BLOCKED_REFERENCE_OR_CONVERGENCE_EVIDENCE_REQUIRED`;
- `QUALIFIED_HISTORICAL_NUMERICAL_EQUIVALENCE`;
- `QUALIFIED_CORRECTED_LEGACY_NUMERICAL_POLICY`;
- `QUALIFIED_NEW_ANIMO5_NUMERICAL_POLICY`;
- `UNRESOLVED_NOT_ADMITTED`.

The last three require evidence beyond NQ01 architecture itself.

## NQ01 boundary

ANIMO-NQ01 only defines the architecture and tooling needed to perform these qualifications.

It does not:

- choose a tolerance;
- change `C_unl`;
- change `Transorp`;
- change compiler precision;
- change production code;
- admit TCD-019;
- establish B2;
- establish B3 or B4.

Until independent B2 data exist, the maximum NQ01 status remains:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.

Production migration remains `NOT_ADMITTED`.

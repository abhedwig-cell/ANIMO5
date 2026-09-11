# ANIMO-TB06A Numerical, Compiler & Runtime Qualification Bank Adoption

## Scope

TB06A adopts only bounded reusable numerical and runtime contracts into a fragment package. It does not modify production source, perform scientific admission, update the central testbank registry, define a global numerical tolerance, or establish repository-wide compiler/runtime correctness.

The workunit follows TB01 permanence criteria and TB02 fragment governance. TCD-specific probes are not promoted merely because they were useful for a discrepancy investigation.

## Adopted numerical contracts

### Fail-closed comparison

NQ01 provides the reusable policy boundary. Exact or discrete contracts remain exact. A nonexact floating scientific difference does not become acceptable because it is small. It requires a separately qualified numerical policy. B1 evidence cannot be relabelled as independent B2 reference evidence, rounded report output cannot stand in for unrounded scientific state, and evidence-packet completeness is not numerical equivalence.

### Precision-aware capture

Scientific capture must preserve sufficient precision and round-trip evidence. Precision metadata is part of the evidence identity. Representation comparison and scientific-value comparison remain separate layers. Predefined comparison subjects prevent post-hoc selection after a result is known.

### Domain-bounded policy qualification

NQ03R is used only as a methodological exemplar. Its TCD-042-E1 polynomial, threshold and natural envelope are not generalized. The reusable rule is narrower: a numerical policy is valid only inside its explicitly justified domain and precision envelope; outside that envelope the bank fails closed. Before claiming bitwise production binding, floating-point evaluation order and contraction/reassociation semantics must either be fixed or bounded by an equation-derived qualification.

## Adopted runtime ownership contract

RUNTIMEQ02 exposed a reusable architecture invariant: a value consumed as current-call/current-step workspace must have an explicit valid producer before first read and a declared lifetime. Silent stack persistence, compiler accidents, or historic behaviour are not ownership. Workspace does not become restart state by implication. Observer probes must be non-interfering.

The TCD-037-specific CH4/N2O accounting mapping is not promoted by TB06A.

## Deliberate gaps

TB06A records two fail-closed gaps. First, ANIMO5 still lacks a shared representative O0/O2 and cross-compiler qualification matrix spanning compiler family, floating-point contraction/reassociation and active scientific cases. Isolated workunit probes are insufficient for a repository-wide equivalence claim.

Second, BUILDQ and RUNTIMEQ provide valuable bounded evidence, but they do not yet constitute a repository-wide runtime initialization, producer/consumer, lifetime and task-order qualification across every active subsystem.

## GOV05 adversarial self-review

The review asks whether this fragment creates a hidden tolerance, universalizes a TCD-specific numerical policy, turns TCD-specific runtime accounting into general scientific truth, treats isolated compiler probes as whole-model qualification, or mutates the central registry. Each is rejected. Assurance remains `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Qualification boundary

A green exact-head CI qualifies only the bounded TB06A fragment package. It does not qualify numerical equivalence of ANIMO5 as a whole, compiler portability, whole-model runtime correctness, production numerical-policy binding, B3 admission, or a whole-model golden baseline.

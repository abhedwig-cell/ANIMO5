# ANIMO5 Scientific Verification, Conservation, State & Release Testbank Architecture

Work unit: **ANIMO-TB01**

Authority base used for this architecture: **ANIMO-RG05I@94afe7d649a8c60758a41996f0059de0acddd2fc**. RG05I is the current qualified aggregate at authoring time and carries GOV05 plus the three post-RG05H atomic admissions B3D21, B3D24 and B3D23. The current canonical TCD/routing authority remains **ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808**. GOV05 is qualified at **f65a47724e4a4fca7f2d8b8d6de9eeee51867904** with exact-final workflow run 34546470484 green. GOV04, GOV03 and B3Q01 remain explicit upstream scientific-governance authorities.

This document defines architecture only. It does not modify scientific production source, admit a TCD, compose B3, open B4, authorize production migration, create historical B2, or create a corrected whole-model golden baseline.

## 1. Design position

ANIMO-TB is a layered evidence system, not one regression script and not a claim that green automation proves scientific correctness. Every reusable test must say what claim it tests, at what scale, against which source and input identity, where its expectation comes from, how comparison is performed, what it costs, how strong the result is, and which gate it may block.

The historical ANIMO taxonomies are retained exactly:

- test level: `UT`, `CT`, `IT`, `INV`, `RR`, `QG`;
- cost class: `FAST`, `FOCUSED`, `BROAD`, `QUALIFICATION`;
- expected-value provenance: `ANALYTICAL`, `THEORY`, `FROZEN_LEGACY`, `CORRECTED_LEGACY_REFERENCE`, `QUALIFIED_GOLDEN_CASE`, `INVARIANT`, `UNKNOWN`.

Execution profiles add scheduling semantics, not replacement terminology. Profiles map explicitly to one or more existing cost classes.

A test identity is stable across file moves. The chosen identifier form is `ATB-{DOMAIN}-{NNN}`. Controlled domains are `PROV`, `ORACLE`, `SPC`, `CONS`, `TRN`, `STATE`, `BND`, `SUB`, `INT`, `REG`, `NUM`, `ARCH`, and `REL`. The registry, not the filesystem path, is authoritative for traceability.

## 2. Layer model

### TB-L0 Provenance & Evidence Integrity

L0 proves what was tested, not whether the science is correct. Qualification use requires immutable source identity, testcase/input identity, manifest identity, evidence-artifact hashes and, when executable behaviour matters, compiler/build identity. Incomplete source custody or a missing required hash fails closed.

The existing EG01/B0 contract is retained: the revision-53 source archive, testcase archive and ANIMO 4.0 guide have explicit SHA-256 identities, but controlled external retention is not yet proven by the B0 evidence register. That limitation must remain visible. A provenance PASS can never be converted into a scientific PASS.

### TB-L1 Atomic Scientific Oracles

L1 isolates one equation, identity or scientific relationship. Allowed oracle origins include `ANALYTICAL`, `THEORY`, `INVARIANT`, and `QUALIFIED_SYNTHETIC_ORACLE`. SYNQ01 patterns are reusable here, but synthetic evidence remains synthetic and is never historical B2.

Typical targets are partition identities, sorption limit cases, species-separated transaction laws, simple conservation identities, dimensional relationships and carefully bounded process laws.

### TB-L2 Species, Units & Stoichiometry

L2 is first-class because many ANIMO defects are ownership defects rather than numerical instability. Tests cover C/N/P ownership, NH4 versus NO3, dissolved versus solid, organic versus mineral, array/species index correspondence, units, dimensional consistency, stoichiometric ratios, parent/daughter transfers and cross-species symmetry only where science justifies symmetry.

A symmetry test must record both the scientific reason for symmetry and the fields intentionally excluded. Textual similarity alone is not an oracle.

### TB-L3 Local Reaction & Transaction Conservation

L3 expresses each scientifically closed transformation as a transaction contract. A canonical form is `initial storage + inputs - outputs - final storage = residual`, or an algebraically equivalent signed ledger. It covers mineralisation, immobilisation, decomposition, humification, DOM conversion, sorption/desorption, crop uptake, exudation, gas production and redistribution where the process is closed at the chosen boundary.

Exact algebraic conservation and tolerance-qualified numerical conservation are separate qualification strengths. No tolerance may enter a manifest without a cited numerical or scientific contract.

### TB-L4 Profile, Transport & Control-Volume Conservation

L4 checks control-volume ownership across layers, vertical transport, upper/lower boundaries, drainage, plant uptake, matrix/macropore domains and inter-domain exchange. Whole-profile closure may supplement but not hide local compensating errors where local terms are observable.

Every balance test states its control volume, included storage pools, external flux signs, internal-transfer cancellation rules and residual definition.

### TB-L5 Persistent State, Restart & Split-Run

L5 classifies every restart-sensitive datum as `PERSISTENT_STATE`, `DETERMINISTIC_RECONSTRUCTION`, `EPHEMERAL_WORKSPACE`, or `DERIVED_DIAGNOSTIC`. Split-run tests compare continuous execution with checkpoint, restore and continuation. They record checkpoint inventory, serialization owner, restore direction, cold-start/restart discriminators, first-post-restore observation and a bounded continuation trajectory.

Interfaces must support ordinary aqueous solutes, crop state, macropore solutes, GHG state, layer-0 state and event-local accumulators. Subsystem identity never implies whole-model restart identity.

### TB-L6 Boundary & Initialization Contracts

L6 covers initial concentrations/stocks, upper and lower boundaries, deposition, precipitation solute input, crop initialization, GHG air and boundary initialization, zero/nonzero cases, and valid/invalid input branches. Each test declares `COLD_START`, `RESTART`, or `BOTH`, plus the owner of produced state.

### TB-L7 Subsystem Scientific Banks

The registry defines modular banks for `NITROGEN`, `PHOSPHORUS`, `CARBON_ORGANIC_MATTER`, `DOM`, `PLANT_CROP_UPTAKE`, `SORPTION`, `TRANSPORT`, `MACROPORES`, and `GHG`. A subsystem manifest records scope, state inventory, key conservation laws, atomic oracles, integrated cases, restart obligations and known gaps. Uniform structure is required; identical scientific tests are not.

### TB-L8 Integrated Scientific Cases

L8 uses small, interpretable multi-process cases. Each case lists active processes, inactive controls, expected interaction surface, element balances, state inventory and why each process is enabled. A large case that merely runs is behavioural evidence, not an integrated scientific oracle.

### TB-L9 Reference & Behavioural Regression

L9 separates `FROZEN_LEGACY_BEHAVIOUR` from `SCIENTIFICALLY_QUALIFIED_EXPECTED_BEHAVIOUR`. Captured output never becomes golden merely because it is stable.

Two machine-readable availability classes are mandatory:

- `ATOMICALLY_QUALIFIED_COMPONENT_EXPECTATIONS`: available only per admitted/qualified scope;
- `COMPOSED_WHOLE_MODEL_GOLDEN_BASELINE`: `UNAVAILABLE_NOT_AUTHORIZED` in TB01.

No qualified composed B3 baseline exists at TB01. Revision-53 output may be compared for behavioural drift when its provenance is pinned, but it is not scientific truth.

### TB-L10 Numerical & Compiler Qualification

L10 records compiler family/version, flags and optimization. It supports O0/O2 comparison where feasible, deterministic/reproducible output, exact-zero domains, singular/near-singular domains, clipping, fallback branches, iteration-sensitive paths, cancellation-sensitive algebra and IEEE754-sensitive cases.

Allowed comparison policies are `BIT_EXACT`, `TEXT_NORMALIZED_EXACT`, `INTEGER_EXACT`, `ABS_REL_TOLERANCE`, and `DOMAIN_SPECIFIC_NUMERICAL_CONTRACT`. A tolerance contract requires a non-empty justification reference and applicable domain.

### TB-L11 Architecture & Runtime Invariants

L11 qualifies first-write-before-read, initialized-before-use, array extent/index consistency, producer-consumer ownership, lifetime, observer non-interference, stale workspace, accidental persistence, hidden reconstruction, process-order mutation and observer/state-mutator distinctions. BUILDQ and runtime qualification evidence are adapters into this layer, not reasons to rewrite historical workunits.

### TB-L12 Release Qualification

L12 defines the future aggregate gate. A release qualification object must enumerate exactly which claims it carries and aggregate provenance, atomic oracles, conservation, subsystem qualification, state/restart, integrated cases, regression, numerics/compiler and architecture invariants. The manifest itself is part of the evidence object. `all processes exited zero` is never by itself a release decision.

## 3. Stable test records and many-to-many traceability

A registry test entry supports `test_id`, `title`, `level`, `layer`, `subsystem`, `scientific_claims`, `risk_class`, `cost_class`, `execution_profile`, `source_identity`, `input_identity`, `expected_value_provenance`, `comparison_policy`, `dependencies`, `outputs`, `qualification_strength`, `blocks`, `owner`, and `status`. Fields are optional only where their scientific meaning is genuinely absent. Numerical expectations always require expected-value provenance.

Scientific requirements and tests are many-to-many. A requirement can require several tests, while one invariant may support several requirements. A reusable result is valid only when its immutable pins and applicability predicates match the new decision context.

## 4. Expected-value governance

Every numerical expectation records authority, hash, date as metadata, source/testcase identity, behavioural versus scientific status, comparison policy and whether it may block admission or release. `UNKNOWN` may be retained as an inventory state but can never act as qualification truth or be automatically upgraded.

`FROZEN_LEGACY` is behavioural by default. `CORRECTED_LEGACY_REFERENCE` is not automatically scientific either; it requires discrepancy-specific authority. `QUALIFIED_GOLDEN_CASE` is allowed only within the exact qualified scope that created it.

Volatile normalization must be explicit and allowlisted by field or line class. Timestamps are metadata and may not become expectations.

## 5. Failure semantics

Runners and adapters should emit one or more controlled failure classes when possible: `SCIENTIFIC_IDENTITY_FAILURE`, `MASS_CONSERVATION_FAILURE`, `SPECIES_OWNERSHIP_FAILURE`, `STATE_RESTART_FAILURE`, `BOUNDARY_CONTRACT_FAILURE`, `NUMERICAL_POLICY_FAILURE`, `ARCHITECTURE_INVARIANT_FAILURE`, `PROVENANCE_FAILURE`, `REGRESSION_UNEXPECTED_DIFFERENCE`, or `TOOLING_FAILURE`.

A tooling failure is not evidence that the scientific claim failed, but it blocks any gate that requires the unavailable evidence. Likewise, an unexpected regression difference is not automatically a scientific defect; it requires classification against admitted expected-difference contracts.

## 6. Coverage model

Scientific completeness is multidimensional. The bank tracks process, species, element, state-owner, boundary, restart, branch/domain, numerical-policy, subsystem-interaction and admitted-TCD regression coverage. Source-code line coverage may be attached as supplemental metadata only.

Coverage is explicitly three-valued or stronger where useful: `COVERED_QUALIFIED`, `COVERED_DIAGNOSTIC_ONLY`, `PARTIAL`, `GAP`, `NOT_APPLICABLE`. A green aggregate cannot erase a `GAP` in a required dimension.

## 7. Execution profiles and gates

`DEVELOPER_FAST` selects FAST structural/atomic checks. `SCIENTIFIC_FOCUSED` selects FOCUSED subsystem and workunit evidence. `CANONICAL_BROAD` selects BROAD cross-subsystem/regression surfaces. `ADMISSION_QUALIFICATION` selects pinned evidence-producing QUALIFICATION runs. `RELEASE` is a future complete qualification profile and remains unavailable until release authority exists. `DEEP_AUDIT` is an expensive qualification matrix for compiler, restart, numerical robustness and architecture probes.

Ordinary development requires the applicable developer-fast set. TCD readiness adds focused scientific gates. GOV05 adversarial review uses `VERIFY_AND_REUSE`: resolve required ATB IDs, verify immutable evidence pins and applicability, run only missing or invalidated gates, then adversarially inspect failures and alternative hypotheses. Same-agent adversarial review is explicitly not genuinely independent. Atomic B3 admission uses pinned admission qualification. Composition requires broad plus qualification evidence under separate composition authority. B4 and production release remain unopened by TB01.

## 8. TCD integration and permanence

A future TCD declares relevant existing test IDs, new test IDs, regression guards, expected differences and evidence gaps. It does not build a private test architecture.

A workunit-specific probe is eligible for permanent-bank promotion only when: its claim is reusable beyond the originating workunit; its oracle provenance and comparison policy are explicit; inputs and source applicability can be pinned; the result is deterministic or has a justified numerical contract; ownership is clear; and the probe is maintainable without carrying transient review scaffolding. Otherwise it remains historical evidence or a fixture/runner adapter.

Admitted TCDs should contribute reusable regression guards, but admission does not automatically make every probe permanent.

## 9. Reproducible qualification object

Qualification and future release profiles produce a manifest containing source head/tree, compiler/tool identity, testbank manifest identity, testcase/input hashes, selected tests, comparison policies, normalized-field allowlist, result artifact hashes, timestamps as metadata, upstream authority pins and the decision. Evidence reuse requires matching pins or an explicit requalification rationale.

## 10. Architecture boundaries

TB01 changes only documentation, testbank manifests, its validator and its workflow. Production scientific source is out of scope. Finalized PREP/SYNQ/STATEQ/MASSQ/MP/GHG/BUILDQ/NQ/UBQ/EG evidence is referenced immutably rather than reorganized. The old `tests/` layout remains valid in Phase TB1.

The suggested `tests/bank/` hierarchy is a destination for later adapters and shared runners, not a migration requirement now. A registry-first approach prevents cosmetic file motion from breaking evidence lineage.

## 11. SWAP5 lessons translated, not copied

SWAP5 currently separates test families such as FCI, FMQ, FMR, FPM, FSI, FVQ, FWOF and runtime, with family-specific runners and exact qualification workflows. Useful principles for ANIMO are: keep qualification families explicit; separate runtime/state checks from scientific formulation checks; bind runners to evidence; preserve exact-head qualification; and keep expensive matrices separate from developer checks.

ANIMO differs materially because C/N/P species ownership, transaction conservation, chemical pools, macropores, GHG pathways and legacy evidence status are central scientific dimensions. Therefore ANIMO uses scientific layers and subsystem manifests rather than importing SWAP family names.

## 12. Parallel implementation contract

Follow-on work can run in parallel in lanes for provenance/registry, C/N/P atomic oracles, conservation, state/restart, macropores, GHG, numerical/compiler qualification and runner/tooling. Parallel lanes must publish fragment manifests with stable ATB IDs. Only a designated consolidation workunit may edit the central registry for a batch. This prevents competing central-registry rewrites.

## 13. Implementation roadmap

**TB1, architecture + inventory + schemas + registry.** Prerequisite: qualified aggregate/governance authority. Deliverables are this architecture, migration plan, registries, coverage matrix, validator and exact-head CI. Parallelism: inventory research may be parallel, final registry integration is serialized. Gate affected: testbank architecture only. Production code: no.

**TB2, shared runner and manifest resolver.** Prerequisite: TB1. Deliver a selector/resolver, fragment-manifest contract, evidence receipt format and failure taxonomy emitter. Parallel with early oracle-fixture preparation if central registry is not edited concurrently. Gate: tooling/evidence integrity. Production code: no.

**TB3, adopt existing synthetic/conservation/species tests.** Prerequisite: TB1 and preferably TB2. Wrap SYNQ01 and current audits without rewriting historical evidence. Parallel lanes for C/N/P oracles and conservation. Gate: readiness/review evidence. Production code: no.

**TB4, state/restart and boundary banks.** Prerequisite: TB1, state classification and runner support. Adapt STATEQ and UBQ evidence, then add narrowly scoped split-run cases. Can run in parallel with TB3 and GHG/macropore banks if ATB ID ranges are reserved. Gate: state/restart and boundary qualification. Production code: no unless a separate scientific remediation workunit is opened.

**TB5, subsystem integration banks.** Prerequisite: atomic and conservation foundations for each subsystem. Deliver small interpretable multi-process cases. Subsystems can progress in parallel. Gate: subsystem/integration qualification. Production code: no by default.

**TB6, numerical/compiler/architecture qualification.** Prerequisite: stable runners and representative cases. Adapt NQ, BUILDQ/runtime and O0/O2 matrices. Parallel numerical and runtime lanes are allowed. Gate: numerical/runtime qualification. Production code: no.

**TB7, future composed regression baseline.** Prerequisite: separate scientific authority showing B3 composition completeness. Only then may a scientifically qualified composed baseline be considered. Gate: composition/reference qualification. Production code: no merely to construct a baseline.

**TB8, release qualification suite.** Prerequisite: TB7 where applicable plus explicit release governance. Deliver a release manifest aggregator and exact release evidence package. Gate: future release. Production code: no; production changes remain separate workunits.

TB01 therefore qualifies a testbank architecture for incremental implementation. It does not qualify a whole-model scientific baseline.
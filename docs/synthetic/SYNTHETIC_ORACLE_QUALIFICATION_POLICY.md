# ANIMO-SYNQ01 synthetic oracle qualification policy

Status: `QUALIFIED_POLICY_FOR_INDEPENDENT_SYNTHETIC_EVIDENCE_NO_B2_CLAIM`

## Scope

ANIMO-SYNQ01 defines a non-production evidence layer for scientific microcases whose expected result can be established without treating ANIMO output as truth. The layer can support later process-level B3 work, but it does not itself admit a corrected legacy baseline.

The workunit is based on the qualified RG02-G5 attachment at commit `5c278152eacc33660f1c5870c7d419b8041b20a9` and preserves the B3Q01 fail-closed admission rules. The frozen B0 identities used for source inspection are:

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

No frozen source or frozen testcase was modified. No diagnostic ANIMO execution was needed for SYNQ01 because the relevant B1 activation and defect evidence already exists in qualified predecessor workunits. The frozen source was read only to bind equations, source locations and index domains.

## Evidence vocabulary

The following evidence labels remain distinct:

- `B1_DIAGNOSTIC_OBSERVATION`: an observation produced by a diagnostic ANIMO execution or source-bound harness;
- `SYNTHETIC_CAUSAL_CASE`: a deliberately constructed activation case used to discriminate causal alternatives;
- `ANALYTICAL_ORACLE`: an expected result obtained from a closed mathematical solution;
- `CONSERVATION_ORACLE`: an exact control-volume identity with explicit stores and boundary transfers;
- `METAMORPHIC_ORACLE`: an exact or scientifically required relation between transformed cases;
- `INDEPENDENT_NUMERICAL_ORACLE`: an independently implemented solution of the same mathematical problem;
- `HIGH_PRECISION_ORACLE`: a reference solution computed at substantially higher precision than the production or legacy path, with sufficient formulation authority;
- `THEORY_DERIVED_ORACLE`: a relation derived from an authoritative or explicitly scoped theoretical contract;
- `B2_HISTORICAL_REFERENCE`: independently trustworthy historical executable behaviour.

`B2_HISTORICAL_REFERENCE` is forbidden as an evidence class for every SYNQ01 record. A synthetic oracle can strengthen a historical-uncertainty B3 route, but it cannot answer what an unavailable historical executable actually did.

## Oracle levels

SYNQ01 uses the following independence levels:

| Level | Meaning | Acceptance basis |
| --- | --- | --- |
| O1 | Exact mathematical oracle | algebra, exact cancellation, exact indexing or limiting identity |
| O2 | Analytical process oracle | closed solution of the intended equation |
| O3 | Independent numerical oracle | separate implementation and control flow for the same mathematical problem |
| O4 | High-precision oracle | reference computation at materially higher precision with qualified formulation authority |
| O5 | Metamorphic oracle | exact relation under a transformation, permutation, split or equivalent decomposition |
| O6 | Conservation oracle | closed control volume with explicit beginning storage, transfers and ending storage |

An oracle can carry more than one level when the evidence genuinely satisfies both. For example, TCD-015 is both exact algebra and a conservation identity.

## Independence rule

Expected results must not be obtained by running the same legacy ANIMO route and freezing its output. Determinism is not independence.

Every oracle record answers six self-confirmation questions:

1. Does it share ANIMO code?
2. Does it share ANIMO control flow?
3. Does it share the same indexing structure?
4. Does it share the same convergence logic?
5. Does it share the same numerical approximations?
6. Was the equation or identity independently reconstructed at the scope claimed?

The result is classified as:

- `STRONGLY_INDEPENDENT`;
- `PARTIALLY_INDEPENDENT`;
- `STRUCTURALLY_CORRELATED`;
- `NOT_AN_ORACLE`.

Sharing the mathematical problem is not by itself a loss of implementation independence. Reusing the same code path, indexing loop, stopping rule or finite-difference approximation is. A contract test can remain useful while being `STRUCTURALLY_CORRELATED`, but its evidence strength must be stated accordingly.

The SYNQ01 Python reference implementation imports no ANIMO production or legacy code. It uses only Python standard-library arithmetic and independently written functions. The TCD-019 high-precision root uses monotone bisection plus an independently derived quadratic cross-check rather than ANIMO Newton/fallback control flow.

## Tolerance policy

SYNQ01 does not establish arbitrary tolerances.

Exact O1, O5 and O6 identities use exact equality where the chosen decimal inputs make this possible. O2 analytical calculations use high-precision decimal transcendental evaluation when an exponential is required. O4 reference computations report bracket width, equation residual and precision rather than translating those numbers into a production acceptance tolerance.

For `SYNQ-O009`, the bisection stopping resolution is derived from the selected 80-digit working precision. It is a reference-computation resolution only. It is not `Small`, a fallback threshold or a global ANIMO5 tolerance.

## Separation from B1 and B2

B1 and synthetic evidence are deliberately compared but never collapsed.

A B1 result can be:

- a legacy failure of an independently known identity;
- a natural-path corroboration of a synthetic mechanism;
- a complete-case activation showing that a ledger seam is reachable;
- unavailable for a synthetic-only branch.

The B1 result is never used as the source of the expected oracle value.

No successful comparison to a SYNQ01 oracle is labelled `HISTORICAL_EQUIVALENCE_PASS`. The strongest generic result from this workunit is `SCIENTIFIC_MICROCASE_PASS`.

## Process-specific scope

### TCD-015

The oracle is the local conservation identity after negative-concentration clipping. The exact discriminator is the duplicate storage term `Avc*Hv*St*Ld`. This is independent of the observed LWKM B1 magnitude. It tests the reconstruction algebra, not the scientific choice of clipping policy itself.

### TCD-017

The oracle is an internal organic-P redistribution with explicit source and destination stores. Internal transfers sum to zero exactly. This supports a ledger-only interpretation but does not replace the required non-interference evidence for later B3 admission.

### TCD-018

The oracle makes interception storage an explicit state in the selected water control volume. It establishes the storage identity independently of the legacy main water-balance report.

### TCD-023

The oracle uses deliberately asymmetric C/N/P states. Each species has its own parent transfer and daughter partition. A permutation relation detects accidental cross-species reuse without relying on a field-scale absolute output.

### TCD-024

Two oracles are used. The first is the per-site analytical Langmuir relaxation. The second is an exact index-domain proof: a trial counter with domain `1..20` cannot be a valid site selector for a site dimension of at most three. The analytical relation is classified `PARTIALLY_INDEPENDENT` because the kinetic formulation authority is partly source-bound, even though the numerical evaluation is independently implemented.

### TCD-025

The qualified oracle is ledger-level only. Matrix-to-macropore exchange is internal and cancels. Direct drainage is external and must remain in the whole-control-volume residual. This does not promote the partially documented revision-53 solute transfer law to an independently qualified process equation.

### TCD-019

SYNQ01 adds a narrow O4/O3 reference for one-site nonlinear Langmuir storage. The expected concentration is solved independently at 80 decimal digits and cross-checked against the exact positive quadratic root. This is sufficient to test a constitutive solution point but is intentionally insufficient to qualify ANIMO fallback policy, a global numerical tolerance, fast-Freundlich behaviour or any particular `Small` value.

## Temporal microcases

TIME01 preserves these candidate endpoint rules:

- management: `t0 < E <= t1`;
- harvest: `t0 <= H < t1`.

SYNQ01 tests both with exact values at `t0`, inside the interval and at `t1`. These endpoint oracles are `STRUCTURALLY_CORRELATED` because the relation is intentionally inherited from the source-reconstructed candidate contract. They prove contract conformance only. They do not establish B2 historical behaviour or canonical TIME.

A changed `t1` changes event membership exactly and therefore must be treated as a different interval identity by any transaction implementation following TIME01. No hidden epsilon is introduced.

## Restart identity

SYNQ01 qualifies only the mathematical split-run identity for a deliberately complete explicit scalar state:

`continuous == run_to_accepted_boundary -> serialize_complete_state -> restore -> continue`.

This is not extended to actual ANIMO state when persistent state is unresolved or incomplete. In particular:

- TCD-016 dry-solute continuation state remains outside this oracle;
- GHG hidden cross-invocation/task state remains outside this oracle;
- MP02 has already shown incomplete persistent macropore solute restart serialization.

Therefore SYNQ01 does not claim an ANIMO continuous-versus-split restart pass.

## Limiting-case library

The independent harness contains exact or metamorphic negative controls for:

- zero reaction rate;
- zero transport;
- zero sorption capacity;
- zero crop demand;
- zero external forcing;
- a single-layer profile;
- one active species;
- one active sorption site;
- identical-site permutation;
- identical-layer permutation;
- zero macropore exchange;
- inactive feature state.

These are weak if used alone. Their purpose is to catch unintended coupling and branch leakage before stronger nonzero cases are interpreted.

## Qualification versus admission

SYNQ01 qualifies an evidence layer, not a corrected model.

A future B3 disposition still needs the class-specific B3Q01 gates, including B0 identity, route selection, coverage, expected differences, non-interference where required, independent second-line review and residual uncertainty. The historical-uncertainty route also requires a documented failed B2 acquisition effort. SYNQ01 does not satisfy those administrative and review gates by itself.

The following remain false at closeout:

`B2_reference_created=false`

`historical_behaviour_claimed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`

`B3_admission_performed=false`

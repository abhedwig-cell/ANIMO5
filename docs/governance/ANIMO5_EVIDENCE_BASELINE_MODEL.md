# ANIMO5 Evidence and Baseline Model

Work unit: `ANIMO-EB01`

Status: `GOVERNANCE_MODEL_PERSISTED_NOT_PRODUCTION_ADMISSION`

Source-bound starting point: `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`

## Purpose

ANIMO5 cannot use a single undifferentiated legacy baseline.

The supplied evidence does not form one fully self-consistent reference package:

- the frozen source identifies ANIMO 4.1.5 revision 53;
- the main supplied technical guide documents ANIMO 4.0;
- the supplied testbank contains nine cases, of which eight execute under the reconstructed GNU diagnostic contract;
- `GHGMais` is not aligned with the supplied revision-53 input contract;
- several source-bound defects have already been causally demonstrated;
- no independently trusted historical revision-53 executable or native unrounded output oracle has yet been admitted.

For this reason the project separates provenance, reproducible observation, historical behaviour, scientific qualification and modern admission into distinct baselines.

A baseline level is a statement about evidential role. It is not automatically a statement that the contained model behaviour is scientifically correct.

## Baseline hierarchy

### B0: Historical artifact baseline

B0 consists of immutable original evidence bytes and their identities.

Current B0 identities:

- source archive `ANIMO_4.1.5.53(3).zip`
  - SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
  - embedded version `animo4.1.5`
  - embedded revision `53`
- testbank archive `ANIMO_testbank.zip`
  - SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- ANIMO 4.0 User's Guide
  - SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

B0 proves provenance and identity only.

B0 does not prove:

- scientific correctness;
- behavioural correctness;
- source and testcase lineage consistency;
- compiler equivalence;
- numerical equivalence;
- completeness of documentation for revision 53.

B0 raw bytes are immutable. Compatibility transforms, converted binary files, edited steering files, generated outputs and corrected source are never B0.

Controlled immutable storage of the raw B0 bytes remains a separate governance requirement until demonstrably implemented.

### B1: Reproducible diagnostic legacy observation baseline

B1 is a reproducible environment used to observe, probe and causally analyse the frozen source.

The current B1 candidate is the GNU Fortran diagnostic reconstruction with executable SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Its current evidential role is:

`DIAGNOSTIC_NOT_REFERENCE`

B1 may support:

- deterministic reruns;
- source-bound defect localization;
- causal probes;
- non-interference tests;
- conservation analysis;
- compiler/runtime sensitivity analysis;
- preparation of later qualification cases.

B1 must not be promoted to historical truth merely because it is reproducible.

A B1 output may become supporting evidence for B3 only through an explicit qualification argument.

### B2: Independent historical behavioural reference

B2 represents independently trusted evidence of what a historical ANIMO executable actually did.

Preferred B2 evidence is:

1. an exact ANIMO 4.1.5 revision-53 executable with provenance;
2. original Intel Visual Fortran build metadata or build logs;
3. historical output for one or more frozen cases tied to an executable identity;
4. if revision 53 cannot be recovered, the nearest provenance-qualified 4.1.x executable, explicitly marked as non-identical lineage.

B2 must remain independent from the B1 GNU reconstruction.

B2 is currently not established.

B2 proves historical behaviour only within the scope actually exercised and captured. It does not automatically prove that the historical behaviour is scientifically correct.

Rounded report values alone are insufficient as a general numerical oracle. Reference capture should preserve unrounded quantities wherever later qualification depends on them.

### B3: Qualified scientific legacy baseline

B3 is the legacy scientific behaviour that ANIMO5 is intended to preserve before intentional model evolution.

B3 is produced by reconciliation, not by copying one executable wholesale.

Its evidence may include:

- B0 source identity and implementation evidence;
- B2 historical behaviour where available;
- authoritative model theory and version-specific documentation;
- closed conservation identities;
- source-bound causal defect evidence;
- dedicated corrected-legacy tests;
- non-interference evidence;
- numerical convergence and precision evidence where numerical policy is involved.

Each historical discrepancy must receive an explicit disposition before it can enter B3.

Allowed dispositions include:

- `PRESERVE_HISTORICAL_BEHAVIOUR`
- `ADMIT_CORRECTED_LEGACY_BEHAVIOUR`
- `REPRESENTATION_CHANGE_ONLY`
- `NUMERICAL_POLICY_CHANGE_REQUIRES_SEPARATE_QUALIFICATION`
- `PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION`
- `UNRESOLVED_NOT_ADMITTED`

B3 must never silently absorb a defect correction.

#### Evidence precedence for closed conservation identities

When a local physical conservation identity is unambiguous and source-bound evidence proves that legacy code creates, destroys or duplicates conserved mass through bookkeeping, indexing, clipping or missing state, matching the historical numerical output is not sufficient scientific justification to preserve the defect.

Such a correction may be admitted to B3 only after its own qualification contract demonstrates:

- the violated identity;
- the exact causal source path;
- the proposed correction;
- expected changed variables;
- conservation closure after correction;
- non-interference outside the affected path, where applicable;
- provenance and uncertainty status.

Historical disagreement remains recorded rather than hidden.

#### Numerical-policy changes

Changes to nonlinear solution methods, tolerances, linearisations, precision policy or convergence criteria are not treated as simple defect corrections merely because they improve a balance residual.

They require separate numerical qualification against:

- governing equations;
- convergence behaviour;
- precision sensitivity;
- conservation behaviour;
- affected state trajectories;
- reference behaviour where available.

#### Physics changes

A change in governing process formulation, constitutive theory or scientific model scope is not a B3 defect correction unless authoritative evidence establishes that the legacy implementation contradicted the intended model theory.

Otherwise it is an explicit ANIMO5 scientific evolution and requires a separate admission after the preservation baseline is established.

### B4: ANIMO5 canonical admission baseline

B4 is the first modern ANIMO5 implementation admitted against B3.

B4 is established only when:

- the implemented process scope has explicit ownership;
- state and transfer contracts are explicit;
- intended B3 behaviour is reproduced within qualified criteria;
- admitted corrected-legacy differences are traceable to their dispositions;
- unresolved legacy behaviour is not silently reinterpreted;
- integration and mass-accounting gates pass;
- the relevant Status A requirements are met.

Once established, B4 becomes the canonical baseline for subsequent ANIMO5 development within its qualified scope.

Historical B0 to B3 evidence remains retained and traceable after B4 exists.

## Current project mapping

At the source-bound starting point of this work unit:

- B0: identity frozen by hashes and manifests; controlled immutable external retention still open;
- B1: established for diagnostic use; eight supplied cases execute successfully and reproducibly under the current GNU diagnostic contract;
- B2: not established;
- B3: not established, but preparatory discrepancy and causal evidence exists;
- B4: not started.

Existing PREP work is therefore evidence preparation for B2 and B3, not ANIMO5 production migration.

## Current defect evidence and baseline meaning

Existing findings such as TCD-014 through TCD-019, TCD-023 and TCD-024 are not automatically B3 corrections.

Their current status remains defined by their originating work units.

In particular:

- causal demonstration under B1 is stronger than static suspicion;
- diagnostic correction is not the same as corrected-legacy admission;
- corrected-legacy admission is not the same as B4 migration;
- historical equivalence is not the same as scientific correctness.

## Reference-unavailable fallback

ANIMO5 must not become permanently impossible to qualify solely because an exact historical executable cannot be recovered.

If a documented, reasonable historical-reference acquisition effort fails, a B3 item may still be considered through an `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY` route.

This route requires stronger evidence than ordinary historical comparison. At minimum:

- exact B0 source identity;
- causal source-level argument;
- authoritative theory or a closed conservation identity;
- dedicated tests;
- expected-difference declaration;
- non-interference evidence where technically applicable;
- explicit recording that exact historical behaviour is unavailable;
- independent review or equivalent second-line qualification before production migration.

This fallback cannot be used to waive uncertainty for poorly documented physics, arbitrary tolerances or broad numerical-policy changes.

## Admission rules

The following implications are prohibited:

- `REPRODUCIBLE` does not imply `REFERENCE`;
- `REFERENCE` does not imply `SCIENTIFICALLY_CORRECT`;
- `DIAGNOSTIC_DEFECT_CAUSALITY` does not imply `CORRECTED_LEGACY_ADMITTED`;
- `CORRECTED_LEGACY_ADMITTED` does not imply `ANIMO5_MIGRATED`;
- `TESTED` does not imply `QUALIFIED`;
- small numerical magnitude does not imply scientific acceptability;
- agreement with rounded output does not prove unrounded behavioural equivalence.

Every work unit that compares behaviour must declare which baseline level is being used and which conclusion that level permits.

## Required lineage for future artifacts

Every generated qualification artifact should record, where applicable:

- B0 source hash;
- B0 testcase hash or testcase member identities;
- documentation/theory identity;
- B1 executable identity when diagnostic execution is used;
- B2 reference identity when available;
- compatibility transformations and their hashes;
- corrected-legacy patch identity;
- work-unit head;
- qualification decision;
- expected differences;
- unresolved uncertainties.

## Migration gate

Production ANIMO5 process migration remains blocked until a project-level B3 admission strategy is established for the process scope being migrated.

This does not require every historical process in ANIMO to be fully qualified before any migration work can ever begin. It does require that each migrated process has a defined B3 evidence basis and that shared state, mass-accounting and numerical contracts have passed their serial gates.

Source-bound analysis, test construction, ownership audits, conservation-ledger work and reference recovery may continue in parallel.

## Governance consequence

The project progression is therefore:

```text
B0 historical artifacts
        -> B1 reproducible diagnostic observation
        -> B2 independent historical behaviour where obtainable
        -> reconciliation and explicit discrepancy disposition
        -> B3 qualified scientific legacy baseline
        -> ANIMO5 migration and qualification
        -> B4 ANIMO5 canonical admission baseline
        -> Status A
        -> continued scientific maturation
        -> Status AA
```

B1 and preparation of B3 evidence may proceed while B2 acquisition is still open. B4 production admission may not use unresolved B1 observations as if they were B2 or B3 evidence.

# ANIMO-NQ01 Numerical Reference Comparison Policy

Status: `QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.

## Purpose

This policy defines how ANIMO5 will compare a reproducible B1 diagnostic run with an independent B2 historical behavioural reference once such a reference exists.

It is deliberately fail-closed. No scientific tolerance is established by this work unit. No solver, precision, convergence or production code is changed.

The governing evidence distinction is the ANIMO-EB01 B0 to B4 model:

- B0 proves historical artifact identity;
- B1 provides reproducible diagnostic observations;
- B2 provides independent historical behaviour;
- B3 is the reconciled qualified scientific legacy baseline;
- B4 is an admitted ANIMO5 implementation against B3.

A B1 GNU result never becomes B2 by agreement with itself or by deterministic repetition.

## Hard prohibitions

The following are not permitted:

1. choosing a tolerance because it makes a comparison pass;
2. using the largest observed legacy residual as the tolerance;
3. using report rounding as evidence of unrounded equivalence;
4. treating a small relative difference as automatically scientifically irrelevant;
5. hiding a trajectory difference by comparing final values only;
6. normalizing scientific values as if they were timestamps or CPU metadata;
7. using B1 output as an independent historical oracle;
8. changing solver, precision or production behaviour within this work unit.

## Comparison surfaces

The machine-readable class definitions are in:

`integration/animo-numerics/COMPARISON_VARIABLE_CLASSES.json`

The minimum scientific comparison classes are:

| Class | Default semantics | Approximate acceptance in NQ01 |
| --- | --- | --- |
| `DISCRETE_CONTROL_FLOW` | exact equality | forbidden |
| `INTEGER_OPTION_STATE` | exact equality | forbidden |
| `EXACT_ACCOUNTING_IDENTITY` | exact term, sign, index and unit mapping; unrounded evaluation | no threshold defined |
| `PHYSICAL_STORAGE_STATE` | unrounded numeric comparison | no threshold defined |
| `INTERNAL_TRANSFER_FLUX` | unrounded numeric comparison | no threshold defined |
| `EXTERNAL_BOUNDARY_FLUX` | unrounded numeric comparison | no threshold defined |
| `CUMULATIVE_LEDGER` | unrounded, temporally aligned trajectory comparison | no threshold defined |
| `NONLINEAR_SOLVER_STATE` | exact discrete path fields plus unrounded float fields | no threshold defined |
| `DIAGNOSTIC_RESIDUAL` | diagnostic magnitude and sign comparison only | no threshold defined |
| `FORMATTED_REPORT_VALUE` | lexical or parsed report comparison | never sole unrounded oracle; differing report values fail closed pending classification |
| `TIMING_OR_NONSCIENTIFIC_METADATA` | declared normalization allowed | not scientific acceptance |

Two additional representation classes are defined:

- `ARTIFACT_IDENTITY`, using exact SHA-256 identity;
- `BINARY_RECORD_REPRESENTATION`, using exact byte or declared record-layout comparison unless a separate representation-only disposition exists.

## Exact equality and bitwise equality

Exactness is mandatory where the object is inherently discrete or where identity is the claim being tested.

Bitwise or hash identity is required for:

- B0 artifacts and frozen inputs;
- executable identity records;
- raw capture files before normalization;
- binary records when record identity itself is under test;
- repeat-determinism claims that explicitly state byte identity.

Exact logical equality is required for:

- option integers;
- branch identifiers;
- fallback identifiers when the same numerical path is claimed;
- index mappings;
- ledger membership and sign conventions;
- event ordering when the compared contract claims the same control path.

Bitwise floating-point equality is useful as stronger evidence when it occurs, but it is not a universal cross-compiler scientific requirement. Historical Intel and reconstructed GNU executions may legitimately differ in representation or final low bits without that fact alone proving a physics difference. Conversely, that possibility does not authorize a tolerance. A non-exact floating difference remains unqualified until its cause and acceptance basis are established.

This avoids both unnecessary bitwise fetishism and permissive tolerances that can mask real process differences.

## Floating scientific values

For physical states, fluxes, ledgers, solver states and residuals:

1. compare unrounded values when available;
2. record exact source precision and capture encoding;
3. require the capture to establish round-trip or exact binary reconstruction for a floating scientific value;
4. report exact equality when it occurs;
5. otherwise report the absolute and relative numerical difference as diagnostics only;
6. classify the result as `UNQUALIFIED_NUMERICAL_DIFFERENCE` until a separate evidence-backed acceptance policy exists.

No global relative or absolute tolerance exists in this policy.

A capture declared `rounded_report_only = true` cannot supply `PHYSICAL_STORAGE_STATE`, transfer, ledger, nonlinear state or residual values as an unrounded scientific oracle. Such a capture can still provide formatted report evidence, but it cannot pass the structured unrounded comparison gate for those quantities.

A future tolerance may only be admitted when its derivation is traceable to relevant evidence such as numerical convergence, analytical scale, measurement or discretization meaning, precision limits, or process-specific scientific sensitivity. It may not be reverse-engineered from the observed B1 to B2 mismatch.

## Accounting identities

`EXACT_ACCOUNTING_IDENTITY` is intentionally stricter than a generic floating variable class.

The following parts are exact:

- which stores are included;
- which transfers are included;
- ledger member identity;
- sign convention;
- species identity;
- layer or compartment indices;
- index mapping where one legacy array index represents a scientific member;
- period reset semantics;
- units and conversion factors;
- initial-state inclusion policy.

The capture schema therefore carries `ledger_member_id`, `ledger_sign` and `index_mapping_id` explicitly. A mismatch in these semantics is an accounting-identity failure even when the floating value itself happens to match.

The numerical evaluation of the identity is floating-point work and must be captured unrounded. A nonzero closure residual is not accepted merely because it is below a historical warning floor.

This is especially relevant to already localized bookkeeping, initialization and P-conservation discrepancies.

## B1 versus B2 roles

B1 is the source-bound GNU diagnostic reconstruction. Its present role remains `DIAGNOSTIC_NOT_REFERENCE`.

B2 must be independently sourced and provenance-qualified. Preferred evidence remains an exact revision-53 native executable or executable-linked historical output. A nearby 4.1.x lineage can be used only when its non-identical lineage is explicit.

The first comparison must record both sides independently:

### B1 side

- GNU executable SHA-256;
- source archive SHA-256;
- compiler and flags;
- compatibility transforms;
- frozen testcase identity;
- output-tree manifest;
- capture method.

### B2 side

- native executable or historical output identity;
- receipt and provenance record;
- claimed version and revision;
- operating environment or historical build metadata;
- frozen testcase identity actually used;
- any path-only compatibility staging;
- output-tree manifest;
- capture method.

The comparator output must state that B1 and B2 are evidence roles, not symmetric labels that imply equal authority.

## Difference categories

Every mismatch must be assigned to one or more of the following categories.

### `file_path_compatibility`

Examples:

- executable expects a historical relative path;
- drive mapping is needed;
- filenames differ only by environment conventions;
- a required file is missing or unexpectedly created.

Path staging may be representation-only only when input bytes remain unchanged and the staging is recorded.

### `formatting`

Examples:

- whitespace;
- exponent letter `D` versus `E`;
- line endings;
- timestamps;
- report column width.

Formatting classification does not prove numerical equivalence if the report is rounded. A differing `FORMATTED_REPORT_VALUE` is not automatically normalized or declared harmless by the structured comparator. It fails closed until the difference is shown to be lexical or another explicitly non-scientific representation issue. Only `TIMING_OR_NONSCIENTIFIC_METADATA` receives non-failing representation-only treatment by default.

### `binary_record_representation`

Examples:

- record markers;
- endian order;
- `REAL(4)` payload layout;
- compiler-specific unformatted sequential record structure.

A representation difference can block native execution even when scientific values would be equivalent. Conversion is never silent and converted bytes are not B0.

### `precision_representation`

Examples:

- four-byte exchange values converted into eight-byte internal values;
- decimal output with insufficient round-trip digits;
- different final low bits under different floating implementations.

This category does not by itself decide scientific acceptability.

### `state_trajectory`

Differences in physical storage or concentration through time, layer, compartment or species.

### `flux_trajectory`

Differences in internal transfers or external boundary fluxes through time.

### `ledger_trajectory`

Differences in cumulative or period balances, including reset behaviour and exact ledger-member semantics.

### `control_flow_branch`

Differences in option state, branch path, nonlinear iteration route, fallback path or event timing.

The structured comparator compares captured `branch_id` and `fallback_id` even when the resulting floating quantity is numerically equal. Same-value agreement must not hide a different solver or constitutive route.

## Temporal comparison contract

A valid scientific comparison must not rely on final values alone when internal trajectory affects interpretation.

The standard checkpoints are:

1. `INITIAL_STATE`;
2. `PRE_PROCESS_STATE`;
3. `POST_PROCESS_STATE`;
4. `ACCEPTED_END_OF_STEP_STATE`;
5. `CUMULATIVE_PERIOD_BALANCE`;
6. `FINAL_STATE`.

`TRIAL_STATE` may additionally be captured for nonlinear qualification, but it must be explicitly distinguished from accepted model state.

Records are aligned by a composite scientific key containing at least:

- testcase;
- step index and time;
- checkpoint;
- layer;
- compartment;
- species;
- quantity name;
- state, transfer or ledger identity;
- cumulative versus instantaneous semantics;
- accepted versus trial context.

Missing or unexpected records fail closed. The comparator must never silently interpolate unmatched time points.

## Report output and ordinary legacy files

The historical ANIMO documentation exposes balances, per-time-step state and rate outputs, and unformatted hydrological exchange files. These are useful comparison surfaces, but ordinary formatted output may have insufficient precision for equivalence claims.

Use formatted output for:

- file-set agreement;
- event presence;
- lexical representation;
- coarse trajectory screening;
- balance report reproduction.

Do not use it as the only oracle for an unrounded state or flux when later admission depends on differences below the printed precision.

## Unrounded capture precedence

Preferred capture encodings are, in order of evidential strength for an individual floating value:

1. exact IEEE binary bits when the runtime representation is known and safely observable;
2. round-trip decimal text with enough digits to reconstruct the captured value;
3. a declared binary record value whose representation and kind are independently known;
4. ordinary formatted decimal output, which is report evidence only unless proven round-trip exact.

The capture schema is:

`integration/animo-numerics/REFERENCE_CAPTURE_SCHEMA.json`

Current schema version:

`1.1.0`

Observer instrumentation must remain observer-only and must first demonstrate that it reproduces the ordinary native output contract before its added quantities are trusted.

## Comparator decisions

The structured comparator can emit result classes including:

- `EXACT_MATCH`;
- `REPRESENTATION_ONLY_DIFFERENCE` only for declared non-scientific metadata;
- `FORMATTED_REPORT_DIFFERENCE_FAIL_CLOSED`;
- `UNQUALIFIED_NUMERICAL_DIFFERENCE`;
- `CONTROL_FLOW_DIFFERENCE`;
- `ACCOUNTING_IDENTITY_DIFFERENCE`;
- `UNIT_MISMATCH`;
- missing or unexpected record evidence;
- `SCHEMA_OR_PROVENANCE_FAILURE`.

Only exact matches and explicitly non-scientific representation-only differences can be non-failing in NQ01. A floating scientific difference remains failing because no tolerance is qualified here. A formatted report difference also fails closed because the comparator cannot infer from the text alone whether the cause is merely lexical or scientifically meaningful.

An exact comparison against a `B2_HISTORICAL_REFERENCE_CANDIDATE` remains explicitly a candidate match and does not upgrade the artifact to a qualified B2 reference.

## Relationship to the existing formatted-tree comparator

`tools/compare_legacy_output_trees.py` remains useful for raw and normalized legacy output-tree comparison. It intentionally does not accept scientific numerical differences.

`tools/compare_b1_b2_reference.py` adds a structured scientific-record comparison layer. It is not a replacement for raw-tree preservation. Both layers are required for the first B2 exercise:

1. preserve and hash raw trees;
2. run formatted-tree comparison;
3. validate structured capture records;
4. run structured B1 to B2 comparison;
5. classify all differences;
6. stop before acceptance if a non-exact scientific difference has no qualified policy.

## PREP02R first-comparison readiness

Live PREP02R status at NQ01 start remains:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`.

The preferred first native case remains `RuurloGrass`.

The first comparison is ready to start immediately once PREP02R supplies a provenance-qualified B2 artifact and ordinary native run. Before execution confirm:

- B2 receipt manifest and SHA-256 exist;
- lineage classification is explicit;
- frozen `RuurloGrass` input bytes are unchanged;
- native path compatibility staging is documented;
- native ordinary output is captured raw before normalization;
- repeat determinism is characterized when practical;
- B1 run uses the pinned diagnostic executable and same frozen testcase;
- all compared output files have manifests;
- structured unrounded observer capture is used only after its ordinary-output non-interference gate passes;
- B1 and B2 capture files validate against schema version `1.1.0`;
- each floating scientific record is proven round-trip or exact-binary capture;
- no tolerance file is supplied unless separately qualified;
- initial, process, end-of-step, period and final checkpoints are represented where the variable class requires them;
- comparator output is retained as evidence, not as automatic B2 or B3 admission.

## Exit status

Before actual independent B2 data, the maximum NQ01 status is:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.

The following status is forbidden without actual B2 evidence:

`QUALIFIED_NUMERICAL_EQUIVALENCE`.

Production migration remains:

`NOT_ADMITTED`.

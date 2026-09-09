# ANIMO-NQ01 Unrounded Reference Capture Contract

Status: `OBSERVER_CAPTURE_ARCHITECTURE_DEFINED_AWAITING_B2_REFERENCE`.

## Purpose

This contract defines how ANIMO legacy runs may be instrumented to capture unrounded scientific quantities for B1 to B2 comparison without changing model behaviour.

The contract does not authorize an observer build by itself. PREP02R still requires an ordinary provenance-qualified native reference contract first. Observer output becomes trustworthy only after the observer build reproduces the ordinary native output surface for the same frozen inputs.

## Core rule

Capture must be observer-only.

The observer may read state that the historical program already computed and serialize that state to a separate evidence stream. It must not:

- change solver inputs;
- change variable values;
- change evaluation order in the scientific path;
- change compiler precision policy;
- introduce new convergence tests;
- clamp or round model state;
- reuse observer values in the production calculation;
- replace legacy formatted outputs;
- alter frozen input bytes.

Any instrumentation that cannot demonstrate non-interference is not an observer and must be classified as a numerical or production modification.

## Required ordinary-output gate

Before using observer values as unrounded reference evidence:

1. run the ordinary native executable or ordinary native build on the frozen case;
2. preserve the complete raw output tree and hashes;
3. create the observer build from the same qualified source/build lineage;
4. run the observer build on a clean copy of the same frozen inputs;
5. compare all ordinary legacy outputs;
6. require exact identity or only explicitly declared volatile metadata differences;
7. fail closed on any other ordinary-output difference.

Only then may the extra capture stream be treated as observer evidence.

This gate is stronger than merely checking final scientific values. The observer must not perturb event timing, formatted balances, warnings or file creation semantics.

## Capture schema

Machine-readable records must validate against:

`integration/animo-numerics/REFERENCE_CAPTURE_SCHEMA.json`

The schema records run identity, evidence role, observer contract, representation observations and scientific records.

Each scientific record identifies:

- time and step;
- checkpoint;
- layer;
- compartment;
- species;
- variable class;
- state identity;
- transfer identity;
- ledger identity;
- units;
- precision;
- source routine;
- call context;
- accepted or trial state;
- iteration and branch information where relevant;
- exact serialized value.

## Time and temporal context

The minimum temporal context is:

- `step_index`;
- simulation year when available;
- simulation time or Julian day when available;
- checkpoint.

Allowed checkpoints are:

- `INITIAL_STATE`;
- `PRE_PROCESS_STATE`;
- `POST_PROCESS_STATE`;
- `ACCEPTED_END_OF_STEP_STATE`;
- `CUMULATIVE_PERIOD_BALANCE`;
- `FINAL_STATE`;
- `TRIAL_STATE`.

Accepted and trial state must never be conflated. A nonlinear trial iterate can explain solver-path differences but is not part of the accepted physical trajectory unless the legacy algorithm accepted it.

## Spatial and species context

Every quantity must be spatially located as far as the legacy semantics permit.

Record explicitly:

- layer number;
- compartment number;
- sorption site or organic fraction when relevant;
- species or material identity.

Use `null` only when the dimension genuinely does not apply. Do not use a sentinel integer such as `0` to mean both a real top reservoir and not-applicable.

Where compartment `0` is a real ANIMO reservoir or surface compartment, record it as `0` and keep not-applicable as `null`.

## State and transfer identity

A capture record should carry one or more semantic identifiers:

- `state_id` for stored mass, concentration or other state;
- `transfer_id` for process or boundary transfer;
- `ledger_id` for a period or cumulative accounting surface.

Names should be stable and semantic. A Fortran variable name may be included in `quantity_name` or notes, but it should not be the only identity when one symbol has context-dependent meaning.

## Units

Units are mandatory.

No comparator may assume unit equivalence from matching variable names.

If a legacy report applies a scale conversion, such as kg/m2 to kg/ha, the capture should prefer the native model quantity with its actual unit and separately record the formatted report representation. A converted observer quantity is permitted only if the exact conversion is declared and the raw source quantity is also available where practical.

## Precision and exact serialization

The capture must distinguish computational precision from print precision.

For each value record:

- storage kind or best source-supported kind;
- bit width when known;
- number of emitted decimal digits when decimal serialization is used;
- whether the serialization is proven round-trip;
- whether compiler-wide default-kind policy is involved.

Preferred value encodings are:

1. `ieee_binary64_hex` or `ieee_binary32_hex` when the representation is known and the observer can expose bits without changing computation;
2. `decimal_text` with enough digits to reconstruct the captured value exactly;
3. `raw_hex` for binary exchange or representation diagnostics;
4. legacy formatted decimal only as a report surface.

A decimal value is not called unrounded merely because many digits are printed. Round-trip adequacy must be established for the captured kind.

## Historical precision boundary

Current source-bound evidence strongly supports an eight-byte default `REAL` computational path combined with explicit `REAL(4)` hydrology staging at the legacy exchange boundary. Exact historical Intel flag settings are still unresolved.

The observer must therefore record precision at the variable boundary rather than assuming one global precision for all values.

In particular, do not reinterpret four-byte hydrological payloads as native eight-byte records. Capture the exchange value and the converted internal value as distinct quantities when that distinction matters to a discrepancy.

## Call and source context

Each capture record must identify the source routine when known and enough call context to disambiguate repeated calculations.

Examples of useful context include:

- transport of a specific species through one compartment;
- entry and exit of a sorption routine;
- pre and post management event;
- balance accumulation for a specific profile;
- accepted Newton solution after fallback;
- period ledger reset.

The capture contract does not require full call-stack tracing. It requires enough context to prevent two semantically different values from sharing one key.

## Nonlinear solver capture

When numerical-policy qualification is in scope, capture at minimum:

- initial nonlinear state;
- accepted final nonlinear state;
- nonlinear residual;
- iteration count;
- branch or constitutive path;
- fallback or bisection use;
- clipping or bound activation;
- convergence decision.

Trial iterates may be captured when needed for path characterization. They must be marked `TRIAL_STATE` and `trial_state = true`.

No convergence tolerance is defined by this contract.

## Cumulative ledgers

Cumulative quantities require explicit period semantics.

Record:

- ledger identifier;
- period identifier;
- whether the value is running cumulative or final period total;
- reset event if applicable;
- checkpoint before and after reset where the distinction matters.

A final cumulative total is insufficient when two implementations can reach the same total through different internal trajectories or period-reset behaviour.

## Initial state

Initial-state capture occurs before the first process mutation.

Where legacy initialization derives one stored quantity from another, capture both the supplied quantity and the resulting active state if possible. This is especially important for known initial-state ledger and P-sorption initialization seams.

The observer must not silently project an inconsistent initial store onto a constitutive relation.

## Raw capture preservation

The exact observer evidence stream must be retained before parsing, normalization or unit conversion.

Record:

- observer capture file size;
- SHA-256;
- encoding;
- schema version;
- parser version used to create any derived comparison file.

Derived JSON is evidence derived from the raw capture, not a replacement for it.

## File and path representation

Path compatibility is recorded separately from scientific values.

Permitted staging can include:

- historical directory structure recreation;
- relative path recreation;
- drive mapping;
- case-preserving or case-insensitive filesystem accommodation.

Input content changes are not path staging. Any content transform creates a distinct non-B0 artifact and must be declared before comparison.

## Binary record representation

Unformatted files may depend on compiler record conventions. Capture representation observations including:

- record marker size;
- byte order;
- scalar kind sizes;
- record lengths;
- file-level hash;
- any compatibility conversion.

A converted file may be useful diagnostic input but is never silently substituted for the frozen original in a B2 claim.

## Formatting and volatile metadata

Only declared non-scientific metadata may be normalized. Examples include run timestamps and CPU duration.

Scientific decimal tokens, event dates, layer identifiers, balance periods and control-flow text are not volatile merely because they occur in a formatted file.

## First PREP02R use

The preferred first native case remains `RuurloGrass` according to the live PREP02R status used to start NQ01.

For that first case, the minimum sequence is:

1. qualify provenance sufficiently to attempt the native run;
2. run ordinary native `RuurloGrass` unchanged;
3. preserve and hash ordinary output;
4. repeat ordinary run when practical;
5. establish observer build lineage;
6. prove ordinary-output non-interference;
7. capture unrounded state and flux records;
8. run the pinned B1 diagnostic case with corresponding capture;
9. compare structured records fail-closed;
10. retain every unqualified difference for later B3 disposition.

## Acceptance boundary

This contract can establish that values were captured faithfully from an execution.

It cannot establish:

- that B2 historical behaviour is scientifically correct;
- that a B1 to B2 mismatch is acceptable;
- a numerical tolerance;
- a corrected numerical method;
- B3 admission;
- B4 migration.

The maximum status before actual independent B2 data is:

`QUALIFIED_NUMERICAL_QUALIFICATION_ARCHITECTURE_AWAITING_INDEPENDENT_REFERENCE_DATA`.

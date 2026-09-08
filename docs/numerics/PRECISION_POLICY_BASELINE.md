# Precision policy baseline

## Legacy precision

Status: `SOURCE_BOUND_REAL8_INTERNAL_INTENT_STRONGLY_SUPPORTED_HISTORICAL_FLAGS_UNRESOLVED`.

The supplied ANIMO 4.1.5 revision-53 source gives substantially stronger precision evidence than the initial testcase-only inventory.

### Source facts

The code contains three relevant categories:

1. a very large body of ordinary default `REAL` declarations for model variables and process calculations;
2. explicit `REAL(4)` staging variables around legacy hydrology input and timing data;
3. explicit `REAL(8)` numerical utilities and selected calculations.

`Function.for` is particularly explicit. `Dble_trunc` is documented as:

`conversion from Real(4) to Real(8)`

and declares its input `R4` as `REAL(4)` and its function result as `REAL(8)`.

Active callers in `input1.for`, `Input_hydro.for` and the main program read hydrological values into `S*` variables declared `REAL(4)` and pass them through `Dble_trunc` into ordinary default-`REAL` ANIMO variables. Comments in the transport sources also describe an historical `REAL*4/REAL*8` conversion and retain former `S*` staging-variable forms in comments.

This source structure strongly supports the interpretation that the principal ANIMO calculation path was intended to use an eight-byte default `REAL`, while legacy binary hydrology exchange remained four-byte real and was explicitly converted at the boundary.

### Diagnostic confirmation

A GNU Fortran build with four-byte default `REAL` is internally inconsistent with this pattern: callers declare the `REAL(8)` `Dble_trunc` function as default `REAL`, producing return-kind corruption under an implicit interface.

A diagnostic GNU build with:

```text
-fdefault-real-8
-fdefault-double-8
```

makes the caller result declarations consistent with `Dble_trunc`, while the explicit `REAL(4)` hydrology staging arguments retain their four-byte representation. Eight supplied testcases then execute deterministically when the separate local-storage semantics are also reproduced.

This is strong evidence for intended legacy precision semantics. It is not yet proof of the exact historical Intel compiler switch because the original project/command line has not been supplied.

### Audit consequence

The earlier interpretation of the `Dble_trunc` caller/result declaration pattern as a confirmed legacy defect is withdrawn. The actual defect risk is architectural: precision correctness depends on an unstated compiler-wide default-kind policy plus implicit interfaces.

For future migration, that dependency must be replaced by explicit kinds and interfaces without changing the qualified numerical contract.

## Provisional ANIMO5 reference policy

The evidence now strengthens the conservative reference policy:

- canonical scientific/reference computation should initially use explicit `real64` or a project kind proven equivalent to the qualified legacy eight-byte path;
- legacy exchange formats must declare their on-disk precision separately from computational precision;
- four-byte hydrology payloads must be converted explicitly at the exchange boundary rather than by compiler-global assumptions;
- mass accounting must remain at reference precision unless qualification evidence supports another policy;
- precision is numerical policy and must not be hidden in compiler defaults;
- FP32 or mixed precision may only be introduced as an explicit execution policy with qualification against the canonical reference path;
- precision changes and physical-model changes must be qualified separately where practical.

## Remaining qualification question

Recover the historical Intel project flags or another authoritative build record. Until then the distinction is:

- internal eight-byte `REAL` intent: `STRONGLY_SOURCE_SUPPORTED`;
- exact historical compiler flag spelling/settings: `NOT_ASSESSED`;
- numerical equivalence of the GNU diagnostic build to the historical release executable: `NOT_QUALIFIED`.

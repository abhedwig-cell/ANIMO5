# ANIMO-B3I05 post-UBQ02 incremental numerical-seam intake

Work unit: `ANIMO-B3I05`

Branch: `work/animo-b3i05-ubq02-numerical-seam-intake`

Status target: `QUALIFIED_POST_UBQ02_INCREMENTAL_ATOMIZATION_TCD042_B1_E1_NO_NEW_TCD_NO_ADMISSIONS`

## Purpose

B3I05 consumes the completed UBQ01/UBQ02 qualification evidence for parent `TCD-042` and decides only the canonical atomic routing needed for later scientific qualification. It does not admit corrected legacy, select a numerical policy, append a new top-level TCD, change the canonical register, or modify production source.

## Authority

Canonical discrepancy identity remains the append-only register at:

- branch `work/animo-b3i03-canonical-register-append`;
- head `814ea660d367494432beb63ea78298d1f6cd73d7`;
- tail `TCD-042`.

The immediately preceding incremental intake authority is B3I04:

- branch `work/animo-b3i04-stateq02-incremental-intake`;
- head `400b7cd79f89043e091751707dfa96537587dcf6`;
- next observed unallocated top-level candidate `TCD-043`, explicitly not reserved.

Scientific evidence consumed here is immutable and external to the B3I05 branch:

- UBQ01 head `6895b67799f26888025eced7188e7190b2a0d07d`;
- UBQ02 head `bb572bb5d431f91d780018a1acbb345fbcfced37`;
- UBQ02 status `QUALIFIED_TCD042_FINITE_POSITIVE_SUBTHRESHOLD_CLASS_E_SEAM_NUMERICAL_POLICY_PENDING`;
- UBQ02 CI run `34369848923`, conclusion `success`.

Evidence strength is preserved. UBQ01/02 remain B0-hash-pinned diagnostic and analytic qualification evidence, not B2.

## Parent phenomenon

The canonical TCD-042 row was intentionally broad because MASSQ02/B3I03 could not yet distinguish whether the zero-throughflow mismatch was accounting-only, missing state, or local algebra. UBQ01 has now resolved the exact-zero branch, while UBQ02 has exposed a second finite-positive mechanism under the same source fallback.

Both mechanisms arise in the same parent upper-reservoir transaction and the same legacy `Flux < 1.0d-8` fallback surface. They do not justify a new top-level discrepancy identity merely because they require different qualification classes.

Therefore B3I05 does **not** reserve `TCD-043`.

## Canonical child-atom routing

B3Q01 requires a compound TCD to be atomized before admission and permits an admission record to cite a parent TCD while each correction has one atomic causal claim and one class.

B3I05 assigns two governed child-atom keys under the existing parent. These keys are not new rows in `THEORY_CODE_DISCREPANCY_REGISTER.csv` and do not advance the top-level TCD sequence.

### `TCD-042-B1`

Title: `exact-zero upper-reservoir load-transfer algebra`

Scope:

`Flpn=0 AND Flux=0`

Class:

`B_LOCAL_ALGEBRA_ZERO_FLOW_LIMIT`

Qualified causal identity from UBQ01:

- persistent upper-reservoir owner already exists;
- Class A accounting-only interpretation rejected;
- Class C missing-state interpretation rejected;
- governing local equation is `Hetop*dC/dt = Load - Flux*C`;
- unique exact-zero coefficients are `A1=1`, `A2=St/Hetop`, `B1=1`, `B2=St/(2*Hetop)`;
- legacy exact-zero fallback sets `A2=B2=0` and omits `St*Load` from represented end storage when `Load != 0`;
- exact-zero synthetic oracle and isolated natural Ruurlo probe are qualified with no tolerance.

State:

`ATOM_QUALIFIED_ADMISSION_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

This child can proceed to a dedicated Class-B admission-readiness record without waiting for selection of the E1 numerical policy, provided composition remains forbidden until both active child semantics needed by a claimed profile are admitted.

### `TCD-042-E1`

Title: `finite-positive subthreshold upper-reservoir numerical evaluation policy`

Scope:

`Flpn=0 AND 0<Flux<1.0d-8`

Class:

`E_NUMERICAL_POLICY`

Qualified seam characterization from UBQ02:

- 1,238 natural activations across six executable testbank cases;
- observed `P=St*Flux/Hetop` range `4.2351647362715017e-20` through `3.8510200002999744e-7`;
- direct binary64 `1-exp(-P)` collapses to zero in 1,189 records;
- four natural Ruurlo records carry nonzero mineral-N load and show material local residuals;
- cancellation-safe analytic evaluation candidates exist for comparison;
- no threshold, switch coordinate, series order, tolerance, or production algorithm is admitted.

State:

`ATOM_CHARACTERIZED_NUMERICAL_POLICY_QUALIFICATION_REQUIRED`

Next owner:

A dedicated Class-E numerical-policy workunit, recommended identifier `ANIMO-NQ03`, should select and qualify the numerical policy under NQ01/B3Q01 rules. B3I05 does not perform that selection.

## Why no new top-level TCD

A new top-level ID requires a collision-checked discrepancy phenomenon with a distinct correction boundary. The finite-positive seam is not a newly discovered independent process. It is the positive-flow portion of the same upper-reservoir fallback that defines TCD-042.

The distinction is scientific atomicity, not phenomenon identity:

- exact zero needs an algebraic limiting correction;
- finite positive flow needs a finite-precision numerical policy for the already defined positive-flow equation.

Child atomization preserves that distinction without falsely inflating the canonical TCD register.

## Parent state after intake

Parent `TCD-042` becomes:

`ATOMIZED_B1_EXACT_ZERO_PLUS_E1_FINITE_POSITIVE_NO_ADMISSION`

This is stronger routing information than the original `REQUIRES_ATOMIZATION` row, but it does not rewrite the canonical register row. The append-only register remains the historical identity surface. The child map is a downstream governance artifact.

Parent TCD-042 remains open and unadmitted because:

1. `TCD-042-B1` still lacks the applicable GOV02/B3Q01 route and independent second-line admission review;
2. `TCD-042-E1` has no selected or admitted numerical policy;
3. the parent cannot be composed as corrected legacy while either required child is unadmitted.

## Numerical-policy boundary

NQ01 remains controlling for E1:

- no global tolerance exists;
- observed B1 residuals cannot define a tolerance;
- low-bit floating differences are not automatically acceptable;
- a future acceptance policy must derive from conditioning, convergence, precision limits, analytical scale or scientific sensitivity evidence;
- B1 and synthetic/high-precision calculations do not become B2.

B3I05 therefore records UBQ02's stable evaluation only as a candidate method and evidence axis.

## Canonical consequences

- canonical top-level register tail remains `TCD-042`;
- `TCD-043` remains unreserved;
- new top-level TCD count: zero;
- child atom keys created: `TCD-042-B1`, `TCD-042-E1`;
- canonical register append: none;
- B3 admission: none;
- numerical policy admission: none;
- production source change: none.

## Recommended next work

1. Start `ANIMO-NQ03` on `TCD-042-E1` to select and qualify a cancellation-safe positive-flow evaluation policy over a declared domain, including continuity at exact zero and the ordinary positive-flow region.
2. Preserve `TCD-042-B1` as an independently ready Class-B admission-readiness target; do not couple its evidence package to an E1 policy choice.
3. After NQ03, open a separate B3 admission-readiness/review path for each child under the legitimate GOV02 route.
4. Do not admit parent TCD-042 by composition until every active child needed by the claimed scope is explicitly admitted.

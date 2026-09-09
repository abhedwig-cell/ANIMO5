# B3 Scientific Admission Framework

Work unit: `ANIMO-B3Q01`

Scope: governance only. This document admits no corrected legacy behaviour and starts no production migration.

## Purpose

B3 is `QUALIFIED_SCIENTIFIC_LEGACY_BASELINE`.

It is not a copy of B0 source, B1 diagnostic behaviour or B2 historical executable behaviour. B3 is built process by process through explicit scientific reconciliation and disposition.

The canonical evidence semantics are source-bound to ANIMO-EB01, specifically `docs/governance/ANIMO5_EVIDENCE_BASELINE_MODEL.md` blob `8b7c6f4197ecc953740e740e64610c3ae3196392` and `integration/animo-governance/ANIMO_EVIDENCE_BASELINE_MODEL.json` blob `5360e14d30b1c0b823540506701df83703f4e70f` on `work/animo-eb01-evidence-baseline-model`.

The current discrepancy input is the canonical TCD register through `TCD-027`, blob `224acc350fde69d3c4aebed8628c0f945e0b3367`, observed on `work/animo-prep06-conserved-state-ledger`.

## Baseline meaning

The following implications are prohibited:

- B0 identity does not prove behavioural or scientific correctness.
- B1 reproducibility does not make a result a historical reference.
- B2 historical agreement does not prove scientific correctness.
- A causal B1 defect finding does not admit a corrected legacy result.
- A passing test does not imply qualification.
- A smaller balance residual does not by itself justify a numerical or physics change.
- Corrected legacy admission does not imply B4 migration.

Every B3 decision is scoped to an identified process, code path, state or ledger surface and a declared evidence set.

## Canonical dispositions

A disposition record must use one of the following values:

- `PRESERVE_HISTORICAL_BEHAVIOUR`
- `ADMIT_CORRECTED_LEGACY_BEHAVIOUR`
- `REPRESENTATION_CHANGE_ONLY`
- `NUMERICAL_POLICY_CHANGE_REQUIRES_SEPARATE_QUALIFICATION`
- `PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION`
- `UNRESOLVED_NOT_ADMITTED`

The narrow fallback disposition `HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY` may be used only when the historical reference acquisition route has been exhausted and the scientific behaviour itself is independently qualified. It must never be used to imply that historical behaviour is known.

## Admission routes

### Normal route

Route identifier:

`NORMAL_B2_AVAILABLE`

This route requires a provenance-qualified B2 reference that exercises the relevant path or provides an otherwise defensible behavioural anchor. B2 is evidence of historical behaviour, not an authority that can override a closed conservation identity or authoritative theory.

Minimum route evidence is:

1. exact B0 source identity and applicable testcase identity;
2. B1 causal evidence for the claimed discrepancy;
3. B2 reference identity and path relevance;
4. theory or conservation basis appropriate to the qualification class;
5. expected difference declaration;
6. conservation evidence where the process is conservative;
7. non-interference evidence where applicable;
8. testcase and branch coverage;
9. independent review;
10. explicit residual uncertainty.

### Historical uncertainty route

Route identifier:

`INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

This route may be considered only after a documented reasonable B2 acquisition effort has failed. It is intentionally stricter than the normal route.

It requires all evidence that remains technically obtainable plus:

- explicit evidence that exact historical behaviour is unavailable;
- a documented acquisition history and stopping rationale;
- authoritative theory or an unambiguous closed conservation identity, not only plausibility;
- at least one dedicated causal test and one independent cross-check that do not merely repeat the same implementation assumption;
- independent second-line review separate from the correction authoring activity;
- narrower scope than would be allowed with B2 if historical path activation is uncertain;
- explicit uncertainty propagation to every later composition and B4 comparison that depends on the item.

The route cannot waive uncertainty for poorly documented physics, arbitrary tolerances or broad numerical-policy changes. If those conditions apply, the disposition remains `UNRESOLVED_NOT_ADMITTED` or is redirected to separate numerical or scientific qualification.

## Minimum evidence model

Every qualification record must contain the following evidence groups, even when a field is explicitly not applicable:

| Evidence group | Minimum content |
| --- | --- |
| B0 identity | source SHA-256, relevant testcase identity or explicit no-historical-case statement, documentation or theory identity |
| B1 evidence | executable or harness identity, causal observation, exact code path and diagnostic limitations |
| B2 requirement/status | route, B2 identity when available, or documented failed acquisition effort |
| Theory requirement | authoritative formulation, closed identity, or explicit statement that theory is insufficient |
| Causal evidence | source location, trigger conditions, observed cause and proposed correction mechanism |
| Conservation evidence | control volume, conserved quantity, before and after residual or explicit non-conservative rationale |
| Expected difference | exact states, fluxes, ledgers or outputs expected to change and expected unchanged surfaces |
| Non-interference | unchanged trajectories or outputs outside intended scope, with method and comparison identity |
| Testcase/path coverage | natural and synthetic coverage separated, branch activation demonstrated |
| Independent review | reviewer or second-line workunit, review scope and result |
| Residual uncertainty | unresolved provenance, theory, path coverage, numerical or observational uncertainty |

Synthetic cases are causal and coverage evidence. They are not B2 historical reference evidence.

## Fail-closed admission rule

`integration/animo-b3/B3_DISPOSITION_SCHEMA.json` is the machine-readable contract.

A record is admitted only when all mandatory gates for its class and route are explicitly `PASS` and the record itself states `admitted: true`.

Missing fields, omitted gates, `FAIL`, unresolved atomicity, unknown B0 identity, absent required review or route mismatch all fail closed.

An admission decision must never be inferred from a filename, test result, corrected branch, reduced residual, commit message or TCD status.

The following dispositions are not themselves admissions:

- `NUMERICAL_POLICY_CHANGE_REQUIRES_SEPARATE_QUALIFICATION`
- `PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION`
- `UNRESOLVED_NOT_ADMITTED`

A Class F item cannot be admitted as a B3 legacy correction under this framework. A Class E item may become corrected legacy only through a separate numerical qualification workunit that satisfies the Class E contract.

## Atomicity before qualification

A TCD that combines more than one scientific correction mechanism must be split before admission.

Examples include:

- a ledger omission plus an initialization threshold change;
- a missing state plus a transport clipping policy;
- a wrong index plus a solver tolerance change.

One record may cite the parent TCD, but each admitted correction must have one atomic causal claim, one qualification class and one expected-difference contract.

## When a TCD cannot enter B3

A TCD cannot be admitted when any of the following applies:

- the relevant B0 source or testcase identity is not fixed;
- B1 evidence is being used as if it were B2;
- B2 is unavailable and the documented acquisition precondition for the historical uncertainty route is not met;
- the item is compound and has not been atomized;
- the authoritative theory needed by Class C or F is absent or contradictory;
- only a lower residual is offered for a Class E change without convergence and precision evidence;
- a synthetic test is presented as historical reference evidence;
- the affected branch is not actually activated by any qualification case and applicability remains unknown;
- expected changed and unchanged variables are not declared before evaluation;
- non-interference is not demonstrated where the contract requires it;
- conservation is violated or the control volume is undefined;
- rounded report output is the only numerical oracle where unrounded behaviour matters;
- the proposed correction changes physics or numerical policy while being treated as Class A or B;
- independent review is missing;
- residual uncertainty is hidden or replaced by an unsupported tolerance.

In these cases the disposition is `UNRESOLVED_NOT_ADMITTED` or the item is redirected to the required separate qualification class.

## Admission workflow

The required sequence for each future discrepancy is:

1. bind B0 identities and exact TCD scope;
2. classify and atomize the discrepancy;
3. declare the intended disposition before correction evidence is interpreted;
4. declare the expected difference contract;
5. gather B1 causal evidence;
6. select and justify the B2 route;
7. satisfy class-specific theory, conservation and coverage gates;
8. run non-interference checks;
9. complete independent review;
10. record residual uncertainty;
11. issue the disposition record;
12. if admitted, qualify any composition separately before use as a combined B3 baseline.

No step in this workflow changes frozen source, testcases or production code.

## Current project consequence

The preliminary classification in `integration/animo-b3/B3_EXISTING_TCD_CLASSIFICATION.csv` is classification only. It admits no correction.

At ANIMO-B3Q01 closeout:

- B3 process governance may be qualified;
- B3 itself remains incomplete;
- no TCD is promoted to corrected legacy admission by this workunit;
- production migration remains `NOT_ADMITTED`.

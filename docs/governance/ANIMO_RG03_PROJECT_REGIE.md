# ANIMO-RG03 Project Regie

Work unit: `ANIMO-RG03`

Branch: `work/animo-rg03-post-g5-gate-reconciliation`

Status target: `QUALIFIED_POST_G5_CANONICAL_GATE_RECONCILIATION_NO_SCIENTIFIC_ADMISSIONS`

Production migration: `NOT_ADMITTED`

## Purpose

RG03 reconciles the post-G5 evidence wave into one canonical governance view. It changes neither ANIMO science nor legacy behaviour. It does not admit corrected legacy, a B3 baseline, canonical STATE/TIME/MASS/EX, B4, or production migration.

RG03 replaces one obsolete global reading of the RG02 G6 gate. The historical-reference track remains fully active and important, but it is claim-scoped rather than a universal prerequisite for every independently qualifiable B3 readiness activity.

## Authority method

Authority is selected from live repository evidence, not branch names. RG03 uses, in order:

1. explicit work-unit status/decision artifacts;
2. cross-workunit authority pins and reconciliation records;
3. ancestry/current-head observations;
4. append-only canonical register reconciliation for TCD identity;
5. absence of an explicit later authority transfer.

A later branch name, `final`, `copy`, `ignore`, `stop`, or similar label is never sufficient by itself.

The canonical TCD identity surface observed by RG03 is the B3I01 append-only integration branch at `383c7a83e84a578969f92113280dc715b7bdddb4`, with register tail `TCD-041`. The append evidence states that existing rows were preserved and that register presence does not constitute scientific admission.

## Reconciled gate interpretation

The prior RG02 field

`G6_B2_reference_acquisition_and_comparison = BLOCKED_BY_PREP02R`

is retained as historical provenance but is not used as a global project stop.

RG03 uses:

- `G6H`: B2 historical fidelity acquisition/comparison. This remains active and not passed.
- `G6U`: bounded historical-acquisition closure. This is not eligible yet because the real PREP02R external request has not been sent.
- `G7`: atomic, process-scoped B3 qualification. Readiness work can proceed independently where class-specific dependencies are satisfied. Admission still requires the legitimate claim-scoped route.
- `GSTATE`: profile-scoped canonical persistent state.
- `GTIME`: canonical exact time and event-boundary semantics.
- `GMASS`: canonical observer/ledger semantics over admitted state and transfers.
- `GEX`: canonical external exchange and producer-adapter contract.
- `GARCH`: candidate architecture readiness.
- `B4(profile)`: composition only from explicitly admitted upstream scopes.

`G6U` does not pass `G6H`. A historical-uncertainty scientific route, once genuinely eligible, preserves historical uncertainty rather than manufacturing historical fidelity.

## PREP02R

Current policy state is explicitly:

`B2_ACQUISITION_STILL_ACTIVE`

The authoritative PREP02R head remains `e29aa75f782a17e1cca6b0c2791ba04077e8bde7`. The acquisition packet, receipt tooling, and native capture contract are ready, but:

- `external_request_sent = false`;
- no historical reference artifact has been obtained;
- no native reference run has been completed;
- no B2 comparison has been completed;
- `G6H` is not passed;
- `G6U` is not eligible.

This blocks historical-fidelity claims and any admission route that currently requires G6H/G6U. It does not block source, theory, runtime, numerical, state, oracle, or non-interference readiness work that has an independent evidence contract.

## Post-G5 evidence wave

The minimum requested post-G5 streams are all present. Additional authoritative support streams relevant to RG03 were also observed:

- `B3A01`, which has qualified TCD-027 Class A readiness but is route-blocked;
- `TIMEQ01`, a qualified synthetic runtime transaction/scheduler fixture;
- `TIMEQ02`, a qualified synthetic external-owner adapter fixture;
- `ARCHG02`, the final TS01/TIME01 candidate-architecture temporal revalidation;
- B3I01 append-only canonical-register supplements, now extending the canonical identity surface through `TCD-041`.

These streams are attached by immutable branch/head reference. Their evidence class is preserved.

## Current project reading

Historical fidelity is unresolved. Scientific qualification is no longer represented as one monolithic post-B2 gate.

The project can safely run several process-scoped readiness workunits in parallel. In particular, TCD-015, TCD-017, TCD-018, TCD-023, TCD-024, TCD-026, TCD-030, TCD-038, TCD-040 and TCD-041 have enough bounded evidence to justify an atomic admission-readiness workunit without pretending that an admission route is already open.

Other items have real non-B2 blockers:

- TCD-019 and TCD-029 are numerical-policy work.
- TCD-016 and several GHG items remain theory blocked.
- TCD-025, TCD-031, TCD-035, TCD-036 and TCD-039 depend on state ownership/restart completeness.
- TCD-028 and TCD-037 depend on runtime-lifetime/interface resolution.
- TCD-027 has already completed readiness and is now specifically waiting for G6H or legitimate G6U eligibility.

This distinction is intentional. `WAITING_ON_B2_OR_G6U` is not assigned to every item merely because B2 is currently absent.

## Canonical gate status

| Gate | State | Meaning |
|---|---|---|
| G6H | ACTIVE_B2_ACQUISITION_NOT_PASSED | Historical fidelity remains open and important. |
| G6U | NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED | The prepared external request has not been executed. |
| G7 | NO_ATOMIC_SCIENTIFIC_ADMISSIONS_YET | Process-scoped readiness queue is active; no scientific admission is created by RG03. |
| GSTATE | READINESS_QUALIFIED_ADMISSION_BLOCKED | STATEQ01 is a strong readiness matrix, not canonical STATE admission. |
| GTIME | CONCRETE_CANDIDATE_QUALIFIED_ADMISSION_BLOCKED | TIME02 selected an exact rational candidate; canonical TIME remains closed. |
| GMASS | B1_OBSERVER_READINESS_QUALIFIED_ADMISSION_BLOCKED | MASSQ01 is observer-only B1 evidence, not a canonical ledger admission. |
| GEX | SYNTHETIC_CONTRACT_FIXTURE_QUALIFIED_REAL_ADAPTER_BLOCKED | TIMEQ02/ARCH contracts are nonproduction; real producer adapters remain absent. |
| GARCH | QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED | ARCHG02 closes the candidate temporal revalidation task, not production architecture. |
| B4(profile) | NOT_ADMITTED | No profile can be composed until its included upstream gates are admitted. |
| PRODUCTION | NOT_ADMITTED | RG03 makes no production change. |

## B4 composition rule

B4 is profile-scoped and compositional. A future B4 record must name the exact process/feature profile it includes. Every included scientific atom must have an admitted G7 disposition. Active state, time, mass and external-exchange gates must be admitted for that profile, and GARCH must be ready.

An optional feature that is explicitly disabled does not need its active-feature scientific state to be admitted merely to define a narrower future profile. Conversely, a feature cannot be silently omitted while claiming a whole-model B4 baseline.

Any future B4 route that uses G6U rather than a recovered B2 reference must carry the resulting historical uncertainty explicitly.

## Production boundary

RG03 modifies governance documents and integration registers only. It does not modify frozen source, frozen testcases, scientific equations, numerical policies, corrected legacy, runtime production code, adapters, or deployment logic.

The project-level production state remains:

`NOT_ADMITTED`

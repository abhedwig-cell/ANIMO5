# ANIMO-GOV02 work-unit contract

## Scope

ANIMO-GOV02 reconciles ANIMO5 evidence governance so that B0-B4 remain stable evidence labels while their dependencies are represented as an evidence DAG rather than a universal linear ladder. The work unit is governance-only. It may define process-scoped B2 requirements, a bounded historical-uncertainty route, uncertainty propagation, machine-readable policy and fail-closed validation.

It does not admit any scientific correction, create or admit a TCD, establish a global B3 baseline, admit B4, modify production source, or admit production migration.

## Authority resolution at start

Authority was resolved by persisted status, ancestry, reconciliation and downstream consumption rather than by branch naming. The GOV02 branch starts from the RG02 G5 integration head `5c278152eacc33660f1c5870c7d419b8041b20a9`.

Relevant live authorities inspected before policy authoring:

| Stream | Authoritative branch / head | GOV02 use |
|---|---|---|
| RG02 | `work/animo-rg02-g5-independent-stream-attachment@5c278152eacc33660f1c5870c7d419b8041b20a9` | integration DAG, gate ownership and branch authority |
| EB01 | `work/animo-eb01-evidence-baseline-model@52411b9d2d6d80717914bc6642544290a54ded21` | B0-B4 meanings and evidence separation |
| B3Q01 | `work/animo-b3q01-scientific-admission-framework@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54` | process-scoped scientific admission and strict historical-uncertainty route |
| PREP02R | `work/animo-prep02r-historical-reference-recovery@e29aa75f782a17e1cca6b0c2791ba04077e8bde7` | current B2 acquisition state |
| SYNQ01 | `work/animo-synq01-independent-synthetic-oracles@e1134630b5ff4cded17dfd33ba13881ec3264ae0` | candidate independent scientific-oracle classes; still in progress |
| TQ01 | `work/animo-tq01-testcase-qualification@5c43ee16df37a0a1357614fdec527f25e5ca8c16` | testcase/path-coverage semantics |
| NQ01 | `work/animo-nq01-numerical-qualification-architecture@e558dff12b127e0662cad62beea7527b42ad89ac` | fail-closed numerical qualification contract |
| NQ02 | `work/animo-nq02-tcd019-nonlinear-p-qualification@12e874559d484417cea1ca5d4ef719ea0b359585` | live Class E evidence and unresolved numerical-policy blockers |
| TS01 | `work/animo-ts01-temporal-semantics@ed12a678cfba19ce851eb2f380e6da3f49203fe4` | source-bound temporal semantics without B2 promotion |
| B3A01 | `work/animo-b3a01-tcd027-class-a-readiness@b2bac82512fef0fa232e759f0c68b472567c11d5` | recent Class A readiness; explicitly not admitted |

## Fixed evidence boundaries

1. `B0` identifies and pins source, testcase and documentation artifacts. It is not a behavioural oracle.
2. `B1` is reproducible diagnostic execution. It can establish causality, path activation, conservation observations and non-interference, but it is not an independent historical oracle.
3. `B2` is an independently trusted historical behavioural reference for the claim and path actually exercised. It is not scientific truth.
4. `B3` is a process-scoped scientific disposition produced by reconciliation of evidence appropriate to the claim. It is not implied by B2 agreement.
5. `B4` is a migrated implementation baseline and inherits all unresolved uncertainty from admitted B3 inputs.
6. Synthetic evidence is never B2.
7. A scientific oracle does not prove historical behaviour; a historical oracle does not prove scientific correctness.

## Historical-uncertainty guardrail

The only no-B2 scientific-admission route considered by this work unit is `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`. It must be at least as strict as B3Q01. It is unavailable merely because B2 acquisition is inconvenient.

At work-unit start PREP02R has not sent its prepared external archival request. Therefore GOV02 records its current policy state as `B2_ACQUISITION_STILL_ACTIVE`. GOV02 must not manufacture a response, failure, exhaustion state or fallback eligibility.

## Ownership rule

GOV02 reconciles EB01 and B3Q01 but does not silently replace owner-qualified documents. New GOV02 policy documents provide the cross-stream interpretation. RG02-owned integration/gate documents may be updated where needed. Owner documents can consume the reconciliation in a later owner-authoritative update.

## Persist-first checkpoint

This contract is deliberately persisted before implementation of the validator or execution of tests. Testing must follow persistence, and the status record must distinguish persisted, tested and qualified states.

## Required final invariants

The work unit may close only with all of the following false:

- `B2_devalued`
- `synthetic_evidence_promoted_to_B2`
- `historical_uncertainty_route_weakened`
- `new_TCD_admissions`
- `B3_global_baseline_established`
- `B4_admitted`
- `production_migration_admitted`

The target governance-only closeout status is `QUALIFIED_EVIDENCE_DAG_AND_PROCESS_SCOPED_B2_REQUIREMENT_NO_SCIENTIFIC_ADMISSIONS`.

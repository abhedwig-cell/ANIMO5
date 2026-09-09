# ANIMO-TIMEQ02 work unit contract

Status: `RESERVED_AND_STARTED`.

## Work unit

`ANIMO-TIMEQ02 - Non-Production External-Owner Adapter Transaction Fixture Qualification`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-timeq02-adapter-transaction-fixtures`

Starting head: `ddd5de478165d51a53352033bc92c55ce672d3aa` from qualified `ANIMO-TIMEQ01`.

## Purpose

Build and execute concrete, non-production external-owner adapter fixtures that instantiate the candidate ARCH05 exchange schema, ARCH07 adapter qualification cases and TIME01/TIMEQ01 transaction semantics.

The fixtures use explicit synthetic hydrology and external-crop producer states. They are intended to prove that schema, identity, ownership, reject/commit and event-link rules can be enforced by executable adapter code before any SWAP, WOFOST or other production coupling exists.

## Evidence class

Primary evidence: `ADAPTER_RUNTIME_SYNTHETIC_PRODUCER`.

Coupled transaction evidence produced here remains synthetic candidate architecture evidence. It is not B2 historical behaviour, not a scientific oracle and not production adapter qualification.

## Authoritative inputs

- `ARCH05` exchange architecture and all 42 declared exchange fields.
- `ARCH05_TRANSACTION_RULES.csv`, 18 transaction rules.
- `ARCH07` qualification specification and its 41-case matrix.
- `TIME01` candidate time/transaction contract at `246128dd14732173a6f27c15c923970d50c14e2a`.
- `TIMEQ01` executable synthetic transaction fixture at `ddd5de478165d51a53352033bc92c55ce672d3aa`.
- `ARCHG02` temporal revalidation at `db8183802631902f41aa5bec518a3c2e63e03ab7`.

No newer branch name may override these inputs without explicit authority refresh.

## Required executable scope

TIMEQ02 must implement a generic candidate frame adapter/validator and synthetic external owners sufficient to execute, where not scientifically blocked:

1. valid detailed and aggregated hydrology frame construction;
2. required/forbidden conditional field enforcement;
3. exact semantic unit and shape validation without inferred conversion;
4. explicit native-to-canonical sign normalization with immutable normalized frames;
5. geometry, physical-layout, configuration, exchange-binding and accepted-generation identity rejection;
6. chemistry/hydrology boundary separation;
7. TCD-018 interception storage/evaporation observability fixture without corrected-legacy admission;
8. macropore-disabled and unadmitted-macropore fail-closed cases, while positive macropore qualification remains deferred;
9. external crop owner-mode, demand, root-distribution and state-observation validation;
10. explicit crop residue/export bundles and prohibition of delta inference;
11. realized N/P uptake trial results linked to exactly one typed physical transfer event;
12. coupled reject atomicity, accept barrier, retry identity and checkpoint owner separation using TIMEQ01;
13. precision-policy reference mismatch as identity failure only, never as an invented numerical tolerance;
14. static diagnostic/parameter/layout/schema identity mutation cases from ARCH07.

`T008 split_run_equivalence` and `T009 rollback_replay_equivalence` remain `REFERENCE_BEHAVIOR` cases and may not be upgraded by TIMEQ02 synthetic execution.

Positive active macropore adapter qualification remains blocked by its scientific/admission dependencies even though MP02 now has complete-case synthetic B1 activation evidence.

## Fail-closed rules

- Do not resize, reorder, pad or truncate exchange arrays.
- Do not infer units from producer names or values.
- Do not accept stale or mutated frame identity.
- Do not mix accepted generations.
- Do not move externally owned persistent hydrology or crop state into ANIMO ownership.
- Do not infer residue, exudate or export transfers from crop state deltas.
- Do not commit rejected trial results or events.
- Do not add numerical tolerances.
- Do not treat diagnostic observations as physical state or transfer.
- Do not treat a passing synthetic fixture as B2, B3, canonical EX, B4 or production evidence.

## Deliverables

- `docs/timeq02/ADAPTER_RUNTIME_FIXTURE_MODEL.md`
- `integration/animo-time/TIMEQ02_ARCH07_CASE_DISPOSITION.csv`
- `tools/timeq02_adapter_fixture.py`
- `tools/test_timeq02_adapter_fixture.py`
- `.github/workflows/timeq02-adapter-runtime.yml`
- `integration/animo-time/TIMEQ02_RUNTIME_RESULT.json`
- `integration/animo-time/ANIMO-TIMEQ02_STATUS.json`

## Qualification target

`QUALIFIED_CANDIDATE_EXTERNAL_OWNER_ADAPTER_RUNTIME_FIXTURE_SYNTHETIC_NON_B2_NONPRODUCTION`

Qualification requires executable evidence and fail-closed test coverage, but must retain:

- `historical_reference_qualified = false`;
- `canonical_state_admitted = false`;
- `canonical_time_admitted = false`;
- `canonical_mass_admitted = false`;
- `canonical_exchange_admitted = false`;
- `b3_scientific_admission = false`;
- `b4_baseline_admitted = false`;
- `production_migration_admitted = false`.

## Change boundary

No frozen legacy source modification. No historical testcase modification. No production SWAP/WOFOST adapter. No ANIMO process-physics implementation. No solver/tolerance change. No canonical discrepancy allocation or corrected-legacy admission.

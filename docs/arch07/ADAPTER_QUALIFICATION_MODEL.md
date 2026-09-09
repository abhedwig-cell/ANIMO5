# ANIMO-ARCH07 adapter qualification model

Status: `CANDIDATE_QUALIFICATION_SPECIFICATION`.

## Specification qualification is not adapter qualification

ARCH07 has two different questions that must not be conflated:

1. is the **test specification** complete and internally consistent with ARCH05/ARCH06?;
2. has a **concrete adapter implementation** executed the required tests and produced admissible evidence?

Only the first question can be answered in ARCH07.

## Evidence tiers

The machine-readable test matrix uses four evidence tiers.

### `SPEC_STRUCTURAL`

Checks architecture identities and specification consistency without a runtime adapter. These cases can be executed now.

### `ADAPTER_RUNTIME`

Requires a concrete adapter implementation. It covers frame construction/validation, presence, units, shapes, sign normalization, immutability, conditional features and owner boundaries.

### `COUPLED_RUNTIME`

Requires an adapter plus transaction orchestration and accepted/trial generations. It covers trial binding, realized crop uptake results, reject atomicity, retry and logical commit barriers.

### `REFERENCE_BEHAVIOR` / `SCIENTIFIC_ADMISSION`

Requires evidence outside adapter conformance. Split-run/replay comparisons need an admitted comparison policy/reference. Macropore qualification needs an admitted scientific feature contract and active case.

A runtime adapter cannot promote itself through these tiers merely by passing schema tests.

## Fail-closed result taxonomy

The specification deliberately distinguishes:

- `ACCEPT_FRAME`: schema/identity-valid immutable input frame;
- `ACCEPT_NORMALIZED_FRAME`: producer-native representation normalized explicitly at boundary;
- `REJECT_FRAME` / `REJECT_BINDING`: fail before ANIMO process execution;
- `REJECT_MUTATION`: immutable identity violation;
- `ACCEPT_TRIAL_RESULT`: trial result exists but remains uncommitted;
- `DISCARD_RESULT`: rejected result disappears from physical continuation;
- `COMMIT_GROUP`: accepted transaction crosses one logical coupled barrier;
- `DEFER_*`: cannot be passed under current evidence/admission status.

## Exact coverage

Every one of the 42 ARCH05 exchange fields has a row in `ARCH07_FIELD_COVERAGE.csv`. Every one of the 18 ARCH05 transaction rules has a row in `ARCH07_TRANSACTION_RULE_COVERAGE.csv`.

The structural audit must compare these registries directly against ARCH05 and fail on missing, duplicate or extra field/rule IDs.

## No tolerance policy

ARCH07 may require exact schema, identity, integer cardinality, unit name and logical relation checks. It may also specify a future numerical comparison test. It must not choose an epsilon, relative tolerance or ULP policy. Those values belong to numerical qualification.

Where an adapter performs a unit or representation conversion, the conversion itself must be explicit and separately qualified. ARCH07 rejects implicit producer-specific interpretation.

## Qualification record for a future adapter

A future adapter qualification package should minimally persist:

- adapter implementation identity and source revision;
- adapter-contract schema identity;
- admitted producer contract/version range;
- ARCH06 normalized configuration identities for each case;
- exact input frame identities;
- test-case IDs executed;
- per-case result and evidence artifacts;
- transaction/journal IDs for coupled tests;
- comparison policy/reference IDs where applicable;
- blocked or waived cases, with explicit external admission basis.

A list of green unit tests without those identities is not sufficient qualification evidence.

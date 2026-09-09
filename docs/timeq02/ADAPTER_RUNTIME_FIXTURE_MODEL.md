# ANIMO-TIMEQ02 adapter runtime fixture model

Status: `CANDIDATE_EXECUTABLE_FIXTURE`.

## Scope

TIMEQ02 instantiates the qualified ARCH05/ARCH07 candidate contracts with executable Python objects and synthetic external-owner frames. It is deliberately one layer more concrete than TIMEQ01: values are organized into hydrology and external-crop frames with declared units, shapes, topology/configuration identities and producer provenance.

It is still not a SWAP, WOFOST or ANIMO production adapter and executes no ANIMO process equations.

Evidence class: `ADAPTER_RUNTIME_SYNTHETIC_PRODUCER`.

## Frame model

A candidate producer frame contains:

- immutable `frame_id`;
- exact interval/trial identity;
- exact accepted-generation identity;
- producer model/build identity;
- exchange schema identity;
- physical layout, geometry, feature-set, configuration and exchange-binding identities;
- a field map keyed by ARCH05 field IDs;
- each field's declared semantic unit and declared shape contract;
- optional producer-native sign mapping that must be normalized before ANIMO-side consumption.

The validator reads the persisted 42-row `ARCH05_EXCHANGE_FIELDS.csv` schema. A frame is valid only if its active field set equals the fields required by the selected synthetic feature/configuration conditions. No missing active field and no inactive conditional field is silently tolerated.

## Required-condition interpretation

TIMEQ02 evaluates the candidate `required_when` expressions only for fixture selection. This is not production configuration logic. It covers:

- `always_for_transport`;
- `always_for_detailed_water_ledger`;
- detailed hydrology;
- snow activation;
- lateral drainage/infiltration, runon, irrigation and crop/root uptake flags;
- macropore activation plus explicit admission identity;
- external crop ownership;
- root distribution, N/P uptake, combined crop ledger, dry-matter ledger and residue-generation flags.

The fixture fails closed on unsupported condition expressions.

## Unit and shape semantics

TIMEQ02 uses exact semantic unit IDs and exact shape-contract IDs from ARCH05. It does not define conversion factors and does not inspect numeric values to guess units or shape meaning. Shape IDs are semantic contracts, not production array implementations.

This is sufficient to test the ARCH07 rule that an adapter must reject a wrong unit/shape rather than resize, pad, truncate, reorder or infer conversion.

## Producer-native sign normalization

The synthetic hydrology producer may declare a native multiplier for a signed field. The adapter must create a new immutable normalized frame whose values obey the canonical ARCH05 sign semantics. It may not mutate an already registered frame under the same `frame_id`.

No floating tolerance is used.

## Chemistry separation

Hydrology frame metadata and fields may not carry undeclared chemistry. The fixture rejects producer-private chemistry keys rather than making ANIMO interpret hidden solute composition through a water-state adapter.

## External crop ownership

External crop state and demand fields remain frame observations. They are never copied into ANIMO-owned persistent state by the fixture.

Residue, exudate and external export are accepted only as explicit event bundles. The fixture contains no function that derives those physical transfers from crop-state differences; attempts to request such inference fail closed.

Realized N/P uptake is an ANIMO trial result. TIMEQ02 links a result to exactly one TIMEQ01 `PHYSICAL` transfer event for the same trial, quantity and amount. A rejected trial therefore cannot leave committed uptake behind.

## Coupled transaction harness

TIMEQ02 reuses the TIMEQ01 runtime transaction state machine for:

- begin binding;
- accepted-state immutability;
- reject atomicity;
- fresh retry identity;
- coupled generation barrier;
- accepted-boundary checkpoint restriction.

Synthetic external-owner accepted states remain outside the ANIMO checkpoint. The checkpoint carries only ANIMO-owned state plus compatibility references in the fixture.

## ARCH07 case policy

TIMEQ02 targets 38 of the 41 ARCH07 cases as executable synthetic adapter/coupled fixtures.

Three cases remain intentionally deferred:

- `H016`, positive scientifically admitted macropore adapter case;
- `T008`, split-run reference equivalence;
- `T009`, rollback-replay reference equivalence.

TIMEQ01 already demonstrated synthetic reject/replay determinism, but that does not satisfy ARCH07 `REFERENCE_BEHAVIOR` evidence for T009.

## Non-admissions

A complete TIMEQ02 pass would show that the candidate exchange and transaction contracts are executable and fail closed under synthetic producer mutation. It would not establish:

- correctness of SWAP or another hydrology producer mapping;
- correctness of WOFOST or another crop producer mapping;
- historical ANIMO behavioural equivalence;
- scientific correctness of any process;
- positive macropore exchange admission;
- numerical tolerance or precision equivalence;
- canonical STATE, TIME, MASS or EX;
- B3/B4 or production readiness.

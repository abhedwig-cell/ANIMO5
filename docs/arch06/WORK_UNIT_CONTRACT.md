# ANIMO-ARCH06 — Normalized Model Configuration & Identity Manifest

Status: `CANDIDATE_ARCHITECTURE_DESIGN_ONLY_NOT_CANONICAL_ADMISSION`.

## Purpose

Define a deterministic, fail-closed normalized model-configuration manifest that binds the candidate state, feature, exchange, parameter, geometry and numerical-policy identities produced or referenced by ARCH01–ARCH05.

ARCH06 must make these identities reproducible without implementing production configuration parsing or changing scientific behaviour:

- `feature_set_id`;
- `physical_layout_id`;
- `exchange_binding_id`;
- `configuration_identity`;
- `observer_configuration_id`.

## Starting point

ARCH06 starts exactly from ANIMO-ARCH05 head `99b6098a19db405ce34928af89bb78b856dce7cd` and its decision `QUALIFIED_CANDIDATE_EXTERNAL_EXCHANGE_CONTRACT_ARCHITECTURE`.

## In scope

- normalized static model configuration fields;
- conditional-field validity;
- separation of physical configuration, numerical policy, exchange binding and diagnostics;
- deterministic canonical serialization rules for identity calculation;
- domain-separated SHA-256 identity derivation;
- exact linkage to ARCH04 layout fields and ARCH05 exchange compatibility fields;
- fail-closed compatibility semantics;
- structural audit and deterministic identity test vectors.

## Out of scope

- canonical STATE/TIME/MASS/EX admission;
- production configuration parser or serializer;
- production SWAP/WOFOST adapters;
- scientific parameter values or defaults;
- numerical tolerance or precision selection;
- forcing values for a particular interval;
- timestep acceptance/retry/convergence policy;
- checkpoint migration;
- corrected legacy behaviour;
- any legacy source or testcase modification.

## Hard rules

1. Unknown manifest fields fail closed.
2. Required fields cannot be synthesized from unspecified defaults.
3. Conditional fields are present with a normalized null value when inactive and non-null when active.
4. Diagnostics do not change `physical_layout_id` or `configuration_identity`.
5. Interval-specific frame IDs, `t0`, `t1`, trial IDs and accepted-state generations are not static configuration.
6. Parameter values are represented here only by an immutable `parameter_set_id`; ARCH06 does not define parameter semantics or canonical numeric formatting for scientific values.
7. Forcing values are not embedded. `forcing_binding_id` and schema identity bind the configured forcing source/contract; the actual immutable interval frame is bound by ARCH05.
8. Physical configuration and numerical policy remain distinct namespaces even when numerical representation affects layout compatibility.
9. GHG and macropore activation remains invalid without matching admission identities.
10. Dormant surface stable DOM remains unsupported and cannot be enabled through normalization.

## Maximum decision

`QUALIFIED_CANDIDATE_NORMALIZED_MODEL_CONFIGURATION_AND_IDENTITY_ARCHITECTURE`

This is architecture qualification only. It does not admit production migration or any canonical gate.

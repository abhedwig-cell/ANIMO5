# ANIMO-ARCH06 normalized configuration model

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

## Why this exists

ARCH04 introduced feature and layout identities. ARCH05 introduced exchange-contract and coupled-trial compatibility identities. ARCH06 provides one normalized static manifest from which those compatibility identities can be derived reproducibly instead of depending on parser order, defaults, file spelling or adapter-specific configuration objects.

The manifest is not a legacy input-file replacement and is not a production API. It is an architecture contract for identity and compatibility.

## Namespaces

The manifest separates:

- `identity`: schema identity of the manifest itself;
- `physical`: state schema and conditional state schemas;
- `parameters`: immutable parameter-set reference and schema;
- `geometry`: layer/domain geometry identity and cardinalities;
- `features`: normalized activation and ownership choices;
- `qualification`: admission identities required by blocked optional features;
- `exchange`: static external-owner and exchange-schema bindings;
- `forcing`: configured forcing/management contract and source bindings, not interval values;
- `numerics`: references to numerical and precision policies, without defining them;
- `diagnostics`: observer-only configuration.

## Static versus interval-specific data

Static configuration includes the selected parameter set, geometry, feature topology, ownership mode, exchange schemas, forcing-source binding and numerical-policy references.

It excludes:

- `t0` and `t1`;
- `interval_id` and `trial_id`;
- producer frame IDs;
- accepted/trial snapshot IDs;
- interval forcing values;
- trial results.

Those belong to ARCH05 transaction binding.

## No hidden defaults

A normalized manifest is complete. Required fields are explicit. Conditional fields are explicit `null` when inactive. A source parser may support conveniences or defaults in the future, but it must resolve them before producing the normalized manifest. Two source documents that normalize to the same manifest have the same ARCH06 identities.

ARCH06 itself does not define any scientific default.

## Parameter and forcing boundaries

Scientific parameter values are not serialized into ARCH06 identity records. They are represented by `parameter_schema_id` plus immutable `parameter_set_id`. This prevents ARCH06 from accidentally defining floating-point formatting, units or parameter semantics before those contracts are qualified.

Likewise, interval forcing values are not static configuration. The manifest binds `forcing_contract_schema_id`, `forcing_binding_id`, `management_contract_schema_id` and `management_binding_id`; ARCH05 binds the exact immutable interval frames used by a trial.

## Diagnostics separation

`diagnostics_mode` and `observer_schema_id` derive `observer_configuration_id` only. They do not affect `configuration_identity`, `physical_layout_id`, `feature_set_id` or `exchange_binding_id`.

This preserves the invariant that turning detailed output on or off does not create a different physical model configuration.

## Qualification-sensitive optional features

GHG and macropore activation are not ordinary booleans. A true activation requires a matching admission identity and state schema. Macropores additionally require detailed hydrology. Until the relevant scientific/evidence blockers are cleared, no normalized production configuration can legitimately provide an admitted identity.

Surface stable DOM remains forbidden in the candidate because PREP06 found parser-visible but dynamically dormant state.

## Crop ownership

`crop_mode` is exactly one of `none`, `animo`, or `external`.

- `none`: no crop state or external crop contract;
- `animo`: ANIMO crop-state schema is required and external crop schema fields are null;
- `external`: external crop exchange/state contract is required and ANIMO crop-state schema is null.

No normalized manifest can represent duplicate persistent crop ownership.

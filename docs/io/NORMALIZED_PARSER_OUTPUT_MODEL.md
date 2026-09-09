# Normalized parser output model

Parser equivalence is evaluated before ANIMO physics runs.

Each normalized record has at least:

```text
field_id
normalized_name
value
value_type
units
schema_version
source_family
source_file
source_location
lexical_form
presence = EXPLICIT | DEFAULTED | INACTIVE_NULL
default_rule_id | null
feature_condition | null
target_object
target_path
legacy_parser_path
adapter_id
```

`source_location` is a line/section/record locator when recoverable. It is diagnostic provenance, not physical state.

## Target objects

- `LegacyInputBinding`: direct-file routing and adapter identity only.
- `ModelConfiguration`: scientific feature and model-option selection after version-aware normalization.
- `SimulationWindow`: start/end dates and temporal input identity.
- `DiagnosticsConfiguration`: output/balance selection, explicitly nonphysical.
- `ParameterSet`: material, plant, soil-chemical and chemistry parameters, with units and immutable parameter identity.
- `ProfileGeometry`: horizons/layers and geometry identity.
- `FeatureConfiguration`: explicit configuration for admitted optional feature schemas; inactive fields are null.
- `InitialState`: physical state initialization only.
- `ManagementForcing`: typed management events and material additions.
- `BoundaryForcingConfiguration` and `BoundaryForcingSeries`: boundary composition and time series.
- `HydrologyExchangeBinding` / `HydrologyFrame`: external water exchange contract, not text-parser internals.
- `CropExchangeBinding` / `ExternalCropForcing`: external crop contract.
- `SoilTemperatureForcing`: external temperature series.
- `CheckpointState`: restart/checkpoint serialization owner.

No reader is allowed to return one mutable mega-object containing all of these concerns.

## Equivalence comparison

The comparison pipeline is:

```text
legacy file bytes
 -> exact legacy parser observation/dump
 -> canonical normalized records

same legacy file bytes
 -> candidate adapter
 -> canonical normalized records

compare by field_id + target path + condition + explicit/defaulted/null status
```

For a literal parsed directly into the same representation, compare the semantic value exactly in that representation. IO01 defines no blanket floating tolerance. Any later tolerance must be field- and representation-specific and owned by a numerical/serialization contract.

Model output is a downstream regression check only. It cannot identify swapped fields, hidden defaults or inactive-value leakage when those happen to cancel or remain unexercised.

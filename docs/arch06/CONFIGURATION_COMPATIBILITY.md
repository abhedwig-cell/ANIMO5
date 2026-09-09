# ANIMO-ARCH06 configuration compatibility

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

## Compatibility layers

ARCH06 intentionally has multiple identities because different operations require different kinds of sameness.

- `feature_set_id`: same normalized feature activation/cardinality choices.
- `physical_layout_id`: same directly interpretable physical state topology and ownership-sensitive layout.
- `exchange_binding_id`: same static external-owner exchange contract binding.
- `configuration_identity`: same static physical/behavioural model configuration for trial binding.
- `observer_configuration_id`: same diagnostics configuration.

No broader identity may be substituted for a narrower compatibility requirement.

## Checkpoint restore

Direct checkpoint restore requires exact `physical_layout_id`, state schema, geometry and other ARCH02/ARCH04 checkpoint identities. Matching `configuration_identity` is not a substitute for a specific checkpoint contract, and mismatch cannot be repaired by silent resize, truncation, zero fill or ownership conversion.

## Coupled trial binding

ARCH05 `configuration_identity` is interpreted as the ARCH06 static normalized configuration identity. The exact interval and forcing/crop/hydrology frames remain separately pinned by ARCH05 `interval_id`, trial/frame IDs and snapshot IDs.

This resolves a key separation:

- static forcing source/schema selection contributes to `configuration_identity`;
- the actual forcing values consumed in a particular interval do not.

## Diagnostics changes

Changing `diagnostics_mode` or `observer_schema_id` may change `observer_configuration_id` but must not change `configuration_identity`, `feature_set_id`, `physical_layout_id` or `exchange_binding_id`.

A future runtime may therefore change diagnostic allocation at an accepted boundary subject to ARCH02 diagnostic-continuation rules without pretending the physical model configuration changed.

## Numerical policy

`numerical_policy_ref` is part of `configuration_identity`. `precision_policy_ref` is also part of `physical_layout_id` because representation can affect state/checkpoint compatibility.

ARCH06 does not choose either policy. It only ensures the selected policy is explicit and identity-bearing.

## Producer model versions

ARCH05 runtime frames carry producer implementation/version provenance. ARCH06 binds the static producer contract identity, not one runtime producer version string. A future adapter qualification contract may restrict which producer builds are admitted to satisfy a contract identity.

## Fail-closed schema evolution

An identity derived under one manifest schema/domain version is not assumed compatible with another. Schema evolution must either:

1. preserve the exact identity contract and version; or
2. provide an explicit qualified migration/equivalence rule.

There is no implicit compatibility by matching field names.

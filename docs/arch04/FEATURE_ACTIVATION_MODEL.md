# ANIMO-ARCH04 feature activation model

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

ARCH04 separates model capability, configured activation, ownership and qualification. A legacy parser switch or array is not by itself enough to make a feature supported in ANIMO5.

## Four separate questions

For every feature the runtime configuration must answer:

1. is the capability represented by the candidate architecture;
2. is it requested by this model configuration;
3. is the relevant scientific/behavioural qualification sufficient for activation;
4. if active, which component owns its persistent state and which dimensions shape that state.

A feature may therefore be architecturally represented but still fail closed when requested. GHG and macropores are the main current examples.

## Core and optional domains

`FT-CORE-SOIL-CHEMISTRY` supplies the candidate core ownership for organic matter, dissolved organic matter and mineral N/P. Optional domains are layered on top of this core rather than forcing every configuration to allocate every legacy array.

Hydrology is externally owned. Exactly one candidate hydrology mode is selected. Detailed mode exposes interception/ponding coordinates and can host snow or a future admitted macropore contract. Aggregated mode instead uses its aggregate surface representation. ANIMO does not duplicate those externally owned coordinates in its own persistent checkpoint state.

The surface reservoir, stable soil DOM, crop compartment, GHG and macropore domain are separately activated. Fast and slow P site counts are explicit state-shape dimensions rather than invisible parser-side cardinalities.

## Ownership modes

Crop activation has three candidate modes:

- `none`: no crop persistent owner or crop exchange contract;
- `animo`: ANIMO owns and checkpoints crop dry matter and actual N/P state;
- `external`: an external crop model owns persistent crop state and ANIMO receives only the admitted exchange data needed for soil-crop transfers.

This prevents hidden duplicate crop ownership.

Hydrology remains externally owned in all modes. Required hydrology coordinates are part of the exchange compatibility contract, not ANIMO-owned physical persistence.

## Blocked features

`ghg_enabled=true` is invalid unless a GHG admission identifier demonstrates that the theory/state/ledger contract required by the selected configuration has been qualified. TCD-008 remains open.

`macropore_enabled=true` is invalid unless the feature has an admitted active-case and complete state/transfer/ledger contract. The supplied historical testbank does not provide that, and TCD-025 remains open.

Parser-visible stable surface DOM/DON/DOP remains explicitly forbidden as a supported runtime feature until its dynamic evolution is qualified.

## Allocation is not scientific selection

ARCH04 determines what would be allocated for a valid feature configuration. It does not decide that a scientific process should be enabled for a user scenario and does not change process equations. Feature selection and numerical policy remain separate configuration concerns.

## Fail-closed validation

Configuration construction must reject at least:

- both detailed and aggregated hydrology selected, or neither selected;
- snow without a compatible detailed hydrology exchange contract;
- external crop mode without a crop exchange schema;
- ANIMO crop-owner mode without a crop state schema;
- GHG or macropores without an admitted feature identity;
- negative P site counts;
- feature/layout dimensions inconsistent with checkpoint or exchange identity;
- attempted activation of dormant surface stable DOM.

Validation occurs before model state is allocated or a checkpoint is restored.

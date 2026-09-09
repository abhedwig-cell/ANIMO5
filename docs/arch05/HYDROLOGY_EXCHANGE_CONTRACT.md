# ANIMO-ARCH05 hydrology exchange contract

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

## Evidence basis

PREP06 source-bound evidence identifies the hydrological storage and transfer families that ANIMO transport and conservation depend on. That evidence includes matrix water, interception, snow, ponding, vertical matrix water transfer, lateral drainage/infiltration, bottom exchange, runoff/runon, irrigation, precipitation, evaporation, transpiration and conditional macropore routes.

ARCH05 converts that evidence into semantic exchange fields. It does not preserve legacy argument-list structure or assume that a future hydrology provider uses revision-53 variable names.

## State coordinates

The external hydrology owner supplies interval-bound coordinates for the accepted start state and proposed end state.

Core transport requires matrix water coordinates by ANIMO layer/geometry. Detailed hydrology additionally exposes interception and ponding storage; snow is exposed when active. These values remain externally owned even though they are used in ANIMO storage projections and water-dependent transport calculations.

A proposed end coordinate may belong to an unaccepted external hydrology trial. Its producer trial snapshot identity must therefore travel with the frame.

## Interval-integrated transfers

Transport and conservation consume interval-integrated water transfer quantities rather than an implicit producer-specific instantaneous flux convention. The candidate field registry includes:

- vertical matrix transfer across each layer interface;
- lateral drainage outflow and drain-system infiltration;
- signed bottom exchange;
- runoff and runon;
- precipitation and irrigation water inputs for the complete water ledger;
- relevant evaporation/sublimation/transpiration outputs for water closure.

Positive directions are normalized by the exchange contract. ANIMO process code should not contain producer-specific sign knowledge.

## Why both state and transfers are required

Transport cannot reconstruct every required interval transfer from two water-state snapshots alone. Conversely a transfer-only interface is insufficient for storage-dependent concentrations and conservation checks. The contract therefore carries both endpoint coordinates and interval-integrated transfer information.

Beginning and end storage in any future MassLedger view are derived from the same externally owned coordinates that ANIMO process execution sees. A separate reporting interface must not substitute different hydrology state.

## Solute boundary composition is separate

Water quantity does not define chemical composition. Irrigation concentration, runon concentration, atmospheric deposition composition or bottom-boundary solute concentration must come from explicit forcing/material contracts.

This prevents a hydrology adapter from silently becoming the owner of chemistry parameters and preserves the architecture invariant separating forcing from exchange data.

## Detailed versus aggregated hydrology

ARCH04 requires exactly one hydrology mode.

Detailed mode exposes the storage coordinates and boundary-transfer topology needed for detailed conservation. Aggregated mode may expose a reduced surface representation, but it may not fabricate detailed interception or ponding state.

A consumer requiring a detailed field set must fail closed when bound to an aggregated frame.

## Macropore extension

Macropore water fields are present in the registry only as a blocked extension contract. They are accepted only when:

- `macropore_enabled=true`;
- the feature has a matching scientific admission identity;
- compatible detailed hydrology is active;
- the exchange schema contains the required macropore storage and transfer fields.

TCD-025 and the lack of an active supplied historical macropore testcase prevent treating this extension as admitted merely because legacy arrays/routines exist.

## Interception ledger seam

PREP06/TCD-018 shows that interception evaporation was exposed in the legacy public ledger without corresponding complete interception storage change. ARCH05 therefore requires the same hydrology state coordinates used by process execution to be available to the ledger observer. No independent summary-only interception bookkeeping is allowed.

## Geometry and units

Every layer or domain shaped field is interpreted only under the exact `geometry_id` and `physical_layout_id` bound to the frame.

Units are semantic contract units. A future adapter may convert native producer units at the adapter boundary, but the conversion must be explicit, deterministic and covered by schema/qualification. The ANIMO kernel does not guess units from field magnitude or producer identity.

## Immutable frame rule

A hydrology frame is immutable after its `producer_frame_id` is assigned. Any revised producer trial state, revised water transfer or revised interval requires a distinct frame identity and a new ANIMO trial binding.

## Not defined here

ARCH05 does not define:

- SWAP internal variable mappings;
- the orchestration iteration algorithm;
- timestep acceptance/rejection criteria;
- interpolation/substepping policy between different model timesteps;
- numerical precision/tolerance;
- macropore scientific admission;
- production ABI or memory layout.

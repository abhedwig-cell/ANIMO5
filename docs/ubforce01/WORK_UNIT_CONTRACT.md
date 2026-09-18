# ANIMO-UBFORCE01 Work Unit Contract

Workunit: `ANIMO-UBFORCE01 - TCD-042 Upper-Boundary Solute Load Forcing Contract & Source Mapping`.

Execution discipline: `RECONCILE -> SOURCE MAP -> IMPLEMENT CONTRACT -> QUALIFY -> REVIEW -> HANDOFF`.

## Purpose

UBFORCE01 qualifies the separate upper-boundary solute-load forcing seam identified by KT12.

It does not calculate the loads from raw BOUNDARY.INP values. It defines and tests a typed carrier for already-resolved revision-53 `Load1...Load6` values so downstream TCD-042 science cannot accidentally treat hydrology forcing as chemistry forcing.

## Authorities and prior boundaries

Current program authority:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Scientific consumer candidate:

`ANIMO-KT12@8f0e8e4bfd0b391b781f7c69b7d2063d5cf8705e`

Architecture boundary:

`ANIMO-ARCH05@99b6098a19db405ce34928af89bb78b856dce7cd`

ARCH05 explicitly states that irrigation concentration, runon concentration, atmospheric deposition composition and other chemical boundary composition do not belong to the hydrology owner.

Input-family audit:

`ANIMO-IO01@2bcf65360b08d278f28f1cc61ac96714db4793a3`

IO01 identifies `BOUNDARY.INP` as a separate forcing family with target normalized objects `BoundaryForcingConfiguration|BoundaryForcingSeries`, but explicitly does not qualify BOUNDARY migration.

## Frozen source identity

Source archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant members:

- `UBoundconc.for`: `b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7`
- `input1.for`: `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`

## Bounded source mapping

For the current detailed hydrology route `Iwa=2 AND Iopthyvs=1`, revision-53 `UBoundconc` constructs the wet/advective top loads from:

- rain and snow water flux with yearly precipitation concentration;
- irrigation flux with timestep irrigation concentration;
- runon flux with timestep runon concentration;
- run-in water with lateral-boundary concentration;
- `Rupr` as the precipitation/runoff partition term subtracted from the precipitation contribution.

The first four legacy load channels are always part of this branch. The fifth and sixth are active only when phosphorus is enabled with `Ipo=1`.

The exact constituent interpretation is preserved through legacy channel identity. UBFORCE01 does not rename `DIORMA`, `DIORNI` or `DIORPO` into a more specific chemistry class without a separate theory/source authority.

## Dry deposition boundary

Revision-53 applies dry N deposition before the top-load calculation as a separate state pulse. It is not part of `Load1...Load6`.

UBFORCE01 therefore excludes dry deposition from this carrier. Future composition must not fold dry deposition into these wet/advective load channels or count it twice.

## Units

IO01 records BOUNDARY concentration forcing in `kg m-3`; KT03 hydrology fluxes use `m d-1`.

The resolved load-rate dimension is therefore:

`kg constituent m-2 d-1`

with the constituent identity inherited from the selected legacy channel.

## Qualified carrier candidate

`tcd042_upper_loads_t` contains:

- schema identity;
- load unit-contract identity;
- detailed forcing-mode identity;
- forcing execution provenance identifier;
- exact origin and endpoint time;
- four always-present resolved load channels;
- explicit phosphorus enablement and presence;
- two phosphorus load channels when active.

The carrier stores already-resolved load rates only. It does not parse BOUNDARY.INP and does not derive load rates from water fluxes or concentrations.

## Current scope

`REV53_IWA2_IOPTHYVS1_DETAILED`

with exact forward whole-day interval binding.

Phosphorus inactive means the two inactive P carrier values are exact binary64 zero and semantically absent.

## Governance

This is a forcing/science composition interface and is conservatively classified as a GOV04 Tier D candidate.

Same-agent adversarial review may qualify the bounded contract package but cannot satisfy an independent Tier D admission gate.

## Hard boundaries

No BOUNDARY.INP parser migration.
No source load resolver.
No dry-deposition migration.
No hydrology ownership of chemistry.
No TCD-042 re-admission.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.

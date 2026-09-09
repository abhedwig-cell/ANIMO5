# Macropore release-lineage reconciliation

Decision: `PRE40_IMPLEMENTATION_LINEAGE_WITH_ANIMO40_NONOPERATIONAL_RELEASE_STATUS_AND_LATER_REV53_ACTIVE_SOURCE`

Production migration: `NOT_ADMITTED`

## Evidence layers

### 1. Frozen revision-53 source

`MAPOTRANSPORT.FOR` contains two unusually specific provenance statements:

- it identifies itself as a subprogram of `ANIMO 3.7.5, version that includes macropores`;
- its history records `9-9-1999 R.F.A. Hendriks creation`.

The routine transports solute in macropore water, calculates average/end macropore concentrations and couples macropore-to-matrix transfer into the ordinary transport source term.

`mapoinput.for` carries later history entries:

- 2007 Hendriks, labelled `Release of ANIMO4.0`;
- 2008 Hendriks, labelled `Release of ANIMO4.0 (32)`.

`MAPOHYDRO.FOR` contains an `October 2008` marker and represents the later two-domain water-storage and exchange architecture present in revision 53.

These source comments show at least three development layers rather than one clean introduction event.

### 2. Independent 1999 publication

Hendriks, Oostindie & Hamminga (1999), *Simulation of bromide tracer and nitrogen transport in a cracked clay soil with the FLOCR/ANIMO model combination*, independently confirms that a modified FLOCR/ANIMO combination already simulated preferential solute transport through cracked/macroporous clay.

The abstract specifically identifies permanent macropores and internal catchment domains as important modifications and reports evidence of rapid preferential transport.

WUR record:

`https://research.wur.nl/en/publications/simulation-of-bromide-tracer-and-nitrogen-transport-in-a-cracked-/`

This is independent evidence that the scientific/macropore implementation lineage predates ANIMO 4.0.

### 3. Later Alterra application description

A later Alterra report on nutrient loading states that ANIMO was adapted with preferential transport and rapid drainage through macropores, referencing Hendriks (1993) and Hendriks et al. (1999).

Public eDepot source:

`https://edepot.wur.nl/18573`

This supports continuity of the pre-4.0 macropore development lineage.

### 4. Official ANIMO 4.0 documentation

The supplied 2005 ANIMO 4.0 User's Guide exposes macropore concepts and input surfaces but explicitly says the option is not fully operational.

That statement remains authoritative for the supported ANIMO 4.0 release described by the guide.

It does not imply that macropore code or experimental model variants did not exist before 4.0.

## Reconciliation

The apparently conflicting evidence is resolved by separating four distinct concepts:

1. **first known experimental/source implementation**: at least 1999, with source self-identification as ANIMO 3.7.5;
2. **scientific model lineage**: independently demonstrated in the 1999 FLOCR/ANIMO publication;
3. **official ANIMO 4.0 supported status**: exposed but not fully operational in the supplied guide;
4. **revision-53 source presence**: active macropore water and nutrient routines exist and participate in state/transfer calculations.

Therefore the chronology is not:

`ANIMO4.0 -> new post-4.0 macropore feature`

but rather:

`pre-4.0 experimental implementation -> 4.0 documented but non-operational release surface -> later integration/rework -> active revision-53 source`

## What this does not establish

TH02 has not established:

- the exact official release in which macropore functionality became supported/operational;
- whether every revision-53 transfer equation descends unchanged from the 1999 model;
- the exact relationship between FLOCR/ANIMO domain equations and later SWAP Main Bypass/Internal Catchment hydrology;
- an active historical revision-53 macropore testcase;
- B2 historical numerical behaviour;
- a corrected public/main balance design for TCD-025.

## B3 implication

This lineage recovery improves theory/provenance confidence for the existence and long scientific history of macropore transport. It does not remove the B3 blockers identified by TH01 and PREP06.

Current B3 state remains:

`BLOCKED_ANIMO_SOLUTE_FORMULATION_ACTIVE_REFERENCE_CASE_AND_TCD025_RECONCILIATION`

The practical correction is interpretive: future ANIMO5 migration planning must preserve the distinction between historical implementation lineage and official release support. It must not classify macropores as a simple late 4.1.x invention.

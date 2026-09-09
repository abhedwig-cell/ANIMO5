# Revision-53 greenhouse-gas theory qualification

Decision: `THEORY_PARTIALLY_RECONSTRUCTED_VERSION_SPECIFIC_AUTHORITY_MISSING`

Production migration: `NOT_ADMITTED`

## Evidence classes

### Public independent process provenance

Classification: `PUBLIC_SECONDARY_MODEL_DESCRIPTION`

Hendriks, Wollewinkel & van den Akker (2007, with a related 2008 peat-congress citation in later WUR material) describe a process-based SWAP-ANIMO extension for peat soils that simulates CO2, CH4 and N2O and was calibrated/validated against two Dutch experimental fields.

WUR Research Portal:

`https://research.wur.nl/en/publications/predicting-soil-subsidence-and-greenhouse-gas-emission-in-peat-so/`

WUR eDepot record:

`https://edepot.wur.nl/159749`

This is strong provenance evidence that the GHG module is scientifically intentional. It is not an exact specification for ANIMO 4.1.5 revision 53.

### Frozen-source formulation

Classification: `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`

Primary source routines:

- `ghgasses.for`;
- `ghg_ch4.for`;
- `ghg_n2o.for`;
- `ghgtransport.for`;
- `ghgtranssub.for`;
- GHG-related coupling in `Init.for`, `Animo.for`, `input1.for` and aeration/mineralisation routines.

## CH4 scientific structure visible in source

The revision-53 source implements CH4 as a transported state with production, oxidation and multiple atmospheric transfer routes.

### Production

Eligible methanogenic substrate is assembled from:

- labile dissolved organic matter;
- exudates;
- humus pools;
- selected fresh-organic-matter fractions.

The source restricts substrate to the anaerobic fraction:

`OmSubCH4 = (1 - Rdfaox) * eligible_organic_substrate`

and calculates production using a pH factor, temperature factor and reference production coefficient:

`QPrCH4 = RdfapH * CrfaTe * R0CH4pr * OmSubCH4`

The exact source temperature relation is a Q10-type factor with base 5 for positive soil temperatures. The source pH response is zero outside its defined range and polynomial within it.

These equations are not promoted beyond `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`. The source comments refer to Walter & Heimann (2000) and Hendriks-related work, but TH01 has not located an independent document that demonstrates that these exact formulas and constants are the revision-53 intended specification.

### Oxidation

Source intent is methanotrophic oxidation controlled by both CH4 and O2.

The source computes:

- an oxygen-response term `CoO2 / (CoO2 + KmO2)`;
- a temperature response with Q10 1.75;
- a CH4 Michaelis-Menten term through `AvCoCH4 / (AvCoCH4 + KmCH4)`;
- a cap imposed by oxygen available after or alongside organic-matter transformation and nitrification demand.

The resulting oxidation amount is converted to an effective first-order coefficient used by the transport solver. The oxygen stoichiometry corresponds to oxidation of CH4 to CO2 and water.

### Transport and emission

CH4 is represented in dissolved and gaseous state. A Bunsen relation couples phase concentrations. The source includes:

- diffusion through gas/water transport machinery;
- advective transport with air and water;
- plant-mediated transfer through the root zone;
- plant-associated oxidation fraction;
- ebullition when dissolved concentration exceeds a temperature-adjusted threshold;
- atmospheric boundary concentration.

The source reports separate emission components for diffusion, flow, plant transport and ebullition.

## N2O scientific structure visible in source

### Production by nitrification

Nitrification produces N2O as a specified fraction of the nitrification transformation rate. This directly couples the GHG state to the inherited mineral-N process system.

### Production and reduction during denitrification

The source distinguishes NO3 reduction to N2O and subsequent N2O reduction to N2. The relative N2O-versus-NO3 reduction strength includes:

- a pH response attributed in source comments to Bril et al. (1994);
- a Q10 temperature factor of 2.6 attributed in source comments to Hendriks et al. (2009);
- an aeration term;
- `RelK_N2Ode`, a relative electron-acceptor-strength factor;
- stoichiometric limits based on organic-matter respiration potential.

The routines explicitly distinguish nitrate-limited and organic-matter-limited denitrification situations and iterate N2O production/reduction with transport.

Exact formulas remain implementation-derived until independently matched.

### Transport and emission

N2O uses the common GHG transport path with dissolved/gas partitioning, diffusion and advective atmospheric exchange.

## Governing states and units

Principal physical state families observed in the frozen source include:

- dissolved CH4 concentration `CoCH4/RsCoCH4`, expressed on a C mass basis;
- gas-phase CH4 concentration `CsCH4/RsCsCH4`;
- dissolved N2O concentration `CoN2O/RsCoN2O`, expressed on an N mass basis;
- gas-phase N2O concentration `CsN2O/RsCsN2O`;
- average state counterparts used in transformation/transport integration;
- atmospheric boundary concentrations;
- production, oxidation/reduction and emission rates in mass per area per day or volumetric rate equivalents depending on the local routine.

The state model is therefore dynamic and transport-coupled. GHG cannot be treated as output-only post-processing in ANIMO5.

## Activation and parser provenance

Revision-53 `input1.for` exposes `GreenHouseGasOption` in the ANIMO41 parser. The older ANIMO40 compatibility route accepts a sixth positional simulation option for GHG even though the supplied 4.0 guide documents only five options.

When GHG is active, revision 53 also expects a `>outGHG:` section containing selected CO2 fraction information and CH4/N2O CO2-equivalent conversion values.

The supplied `GHGMais` testcase follows a different textual contract. It has a named `[GreenHouseGasses]` output block and a `>defGHG:` material section, but not the required revision-53 `>outGHG:` contract. Additional organic-fraction fields also differ. This is `PROVENANCE_ONLY` evidence of a source/testcase lineage mismatch.

## Conservation constraints

The source couples GHG processes to C and N transformations:

- methanogenesis consumes eligible organic-C substrate and produces CH4-C;
- CH4 oxidation produces CO2-equivalent carbon flux;
- N2O production draws from nitrification/denitrification N transformation pathways;
- N2O reduction transfers N toward N2.

However, PREP06 shows that a future canonical mass ledger must explicitly reconcile these GHG states and transfers with the ordinary C/N stores and balances. Legacy GHG state ownership alone is not proof that all public balance outputs close an element-level GHG control volume.

## Known uncertainty and conflicts

1. No exact revision-53 GHG theory/change document has been located.
2. Source comments carry dates and release labels that are not sufficient to prove exact release provenance, especially given heterogeneous SVN metadata in the frozen archive.
3. The supplied GHG testcase is not parser-native to the frozen source.
4. Exact temporal coupling, parameter provenance and calibration domains have not been independently reconstructed.
5. CO2 already exists as an inherited consequence of organic-matter dissimilation in ANIMO 4.0, while the later GHG option expands explicit gas accounting. The boundary between inherited CO2 accounting and new GHG reporting must remain explicit.

## B3 judgement

Current GHG evidence supports all of the following:

- the GHG extension is scientifically intentional;
- CH4 and N2O are genuine dynamic process states in the frozen source;
- broad process mechanisms can be independently connected to published SWAP-ANIMO GHG work;
- exact revision-53 equations and parser/testcase lineage are not independently qualified.

Therefore:

`B3_READINESS = BLOCKED_VERSION_SPECIFIC_THEORY_AND_REFERENCE_LINEAGE`

A defect correction involving GHG physics cannot presently be qualified against theory alone. B2 evidence remains necessary unless ANIMO5 explicitly uses the EB01 fallback path with stronger independent theory, conservation evidence and review.

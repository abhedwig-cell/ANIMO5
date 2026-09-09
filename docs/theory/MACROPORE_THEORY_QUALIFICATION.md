# Revision-53 macropore theory qualification

Decision: `THEORY_PARTIALLY_RECONSTRUCTED_ANIMO_SOLUTE_AUTHORITY_MISSING`

Production migration: `NOT_ADMITTED`

## 1. What ANIMO 4.0 already establishes

The supplied ANIMO 4.0 User's Guide exposes a macropore option and a fairly detailed data interface, but repeatedly marks the option as not operational in ANIMO 4.0.

The guide names two domains:

- Main Bypass Flow domain;
- Internal Catchment domain.

It also exposes planned hydrological quantities such as macropore volume, water storage, precipitation/runoff inflow, matrix exchange, wall-contact fraction and rapid drainage, plus initial macropore solute concentrations for NH4, NO3, dissolved organic matter/N/P and PO4.

This is `AUTHORITATIVE_INHERITED_ANIMO40_THEORY` for the intended interface vocabulary and an important negative fact: operational revision-53 macropore behaviour must not be projected backwards onto ANIMO 4.0.

## 2. Independent hydrological provenance

Classification: `PUBLIC_SECONDARY_MODEL_DESCRIPTION`

SWAP 3.2 theory and related SWAP macropore literature describe the same two-domain architecture.

Main Bypass domain:

- continuous/interconnected macropores;
- rapid transport to greater depth while bypassing the matrix;
- possible rapid drainage to drains.

Internal Catchment domain:

- discontinuous/non-interconnected macropores ending at different depths;
- inflow becomes trapped at macropore endings;
- water is forced into the surrounding, mainly unsaturated matrix.

This makes the hydrological lineage of the revision-53 ANIMO macropore interface defensible. It does not independently specify the nutrient-transfer equations implemented by ANIMO.

Principal public WUR source used by TH01:

`https://swap.wur.nl/Documents/Alterra%20Report1649%2802%29%20-%20Swap32%20Theory%20description%20and%20user%20manual.pdf`

## 3. Revision-53 source-defined process system

Classification for the exact ANIMO equations:

`IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`

Primary routines:

- `MAPOHYDRO.FOR`;
- `MAPOTRANSPORT.FOR`;
- `mapoinput.for`;
- `Hydro_detailed.for`;
- ordinary transport/mineralisation routines that consume macropore-to-matrix source terms;
- `Init.for` for state promotion;
- balance routines for public accounting.

### Water states and fluxes

The revision-53 source represents physical macropore water storage in two domains through `SrWaMp` and `SrWaMpOld`.

Source-visible transfer classes include:

- direct precipitation input to macropores;
- routed surface/runoff input;
- vertical transfer inside macropores;
- macropore-to-matrix exchange by soil layer;
- rapid drainage from the Main Bypass domain;
- storage change between start and end of timestep.

`MAPOHYDRO` evaluates a dedicated water balance that includes storage change and direct drainage. These terms therefore belong to the physical control volume rather than being optional reporting diagnostics.

### Solute states

The source defines macropore concentrations for:

- dissolved organic matter;
- dissolved organic N;
- dissolved organic P;
- NH4-N;
- NO3-N;
- PO4-P.

Start/result concentration pairs are carried separately, consistent with the revision-53 transaction pattern identified by PREP06.

### Solute transfer

`MAPOTRANSPORT` constructs incoming solute mass from surface and matrix-related flows, computes average and end concentrations in each macropore domain, transfers mass from macropore water into the matrix and accounts for rapid drainage from the bypass domain.

Its dedicated balance has the form conceptually:

`inputs + old_storage = outputs + new_storage`

with old and new stores explicitly formed from macropore water storage multiplied by old/result concentration.

The exact solver and transfer equations are source-derived. No ANIMO-specific public formulation document located by TH01 establishes these equations as the revision-53 intended scientific specification.

## 4. Diffusion status

`mapoinput.for` contains a source comment that molecular diffusion functionality is disabled in this version. The supplied ANIMO 4.0 guide exposes diffusion coefficients in its planned macropore input surface.

That combination must be treated carefully:

- the 4.0 interface shows that diffusive matrix/macropore exchange was contemplated;
- the frozen revision-53 source comment says molecular diffusion is disabled in this build;
- no independent version-specific document located by TH01 resolves whether this was a deliberate scientific restriction, unfinished functionality or a build-specific limitation.

Classification:

`CODE_DEFINED_THEORY_UNCONFIRMED`

## 5. Main-ledger discrepancy

PREP06 TCD-025 is directly relevant to scientific conservation.

The specialized macropore routines include physical water and solute storage and rapid drainage in their own control volumes. The main `Outbal_calc` interface cannot represent the same system completely:

- it does not receive full macropore water storage state;
- it does not receive all result macropore solute states as storage inputs;
- direct-drainage integration is incomplete across species;
- `Dra4` is exposed as a reporting quantity but is not consistently part of the main residual equations.

The correct classification remains:

`SOURCE_CONFIRMED_MACROPORE_MAIN_LEDGER_STATE_AND_DRA4_INTEGRATION_GAP_TESTBANK_UNEXERCISED`

This finding does not establish the numerical magnitude under a physical case.

## 6. Testbank and behavioural evidence

All supplied `MacroPoreOption` occurrences found by PREP06 are zero. Therefore:

- revision-53 macropore source paths are not naturally exercised by the supplied testbank;
- no historical behavioural tolerance can be inferred;
- absence of a macropore failure in current regression runs is non-evidence;
- a synthetic future case may prove structural properties but cannot become B2 merely by being executable.

## 7. Governing scientific constraints that are already defensible

Even without a complete ANIMO-specific theory document, the combined independent hydrological provenance and source-bound process structure support these constraints:

1. macropore water is a physical store;
2. macropore solutes are physical stores coupled to that water;
3. matrix/macropore exchange is an internal transfer for a combined matrix-plus-macropore control volume;
4. rapid drainage is an external loss from that control volume;
5. Main Bypass and Internal Catchment have different hydrological roles and must not be collapsed without scientific qualification;
6. mass leaving a macropore domain into the matrix must enter the corresponding matrix species ledger with equal magnitude and compatible units;
7. storage change must be included when evaluating macropore conservation.

These constraints are enough to audit conservation architecture, but not enough to reproduce or redesign every revision-53 flux relation.

## 8. B3 judgement

Evidence strength:

- hydrological architecture: `MEDIUM_HIGH`;
- ANIMO-specific solute formulation: `MEDIUM_LOW`;
- conservation ownership: `HIGH_SOURCE_BOUND`;
- historical behaviour: `ABSENT_FOR_ACTIVE_ROUTE`.

Reconciliation state:

`THEORY_PARTIALLY_RECONSTRUCTED`

B3 readiness:

`BLOCKED_ANIMO_SOLUTE_THEORY_ACTIVE_REFERENCE_CASE_AND_TCD025_RECONCILIATION`

Required next evidence:

1. locate an ANIMO-specific macropore transport/process report or change document;
2. locate or construct provenance for a native historical case with macropores enabled;
3. capture unrounded matrix/macropore storage and exchange terms;
4. reconcile specialized and public balances before any corrected ledger is admitted;
5. preserve domain-specific semantics in ANIMO5 until equivalence of any simplification is demonstrated.

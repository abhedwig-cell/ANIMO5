# TCD-016 theory evidence sweep

Work unit: `ANIMO-SQ01`

Status: `ANIMO40_EVIDENCE_NARROWS_CANDIDATES_BUT_DOES_NOT_DEFINE_DRY_PHASE`

Production migration: `NOT_ADMITTED`

## Purpose

This follow-up note records the additional ANIMO-specific theory evidence reviewed after the initial SQ01 closeout. It tests whether the supplied ANIMO 4.0 documentation or public ANIMO references can convert the preferred dry-solute continuation hypothesis into a corrected-legacy state model.

It does not change frozen source or testcase bytes and it does not admit a production correction.

## 1. Supplied ANIMO 4.0 User's Guide

The supplied ANIMO 4.0 User's Guide, Alterra Report 224 (2005), gives several relevant constraints.

### 1.1 Dissolved storage is explicitly a liquid-phase state

Section 2.3 defines the generic transport equation with:

- `theta`: volume fraction of liquid, m3 m-3;
- `c`: mass concentration in the liquid phase, kg m-3;
- optional solid-phase contents `Xe`, `Xn`, `Xp` for equilibrium adsorption, non-equilibrium adsorption and precipitation in soil.

The documented storage coordinate for dissolved solute is therefore `theta * c`. The guide does not define a finite dissolved mass coordinate at `theta = 0`.

This strengthens the conclusion that a concentration-only continuation cannot represent finite mass once the hydrological surface-water volume disappears.

### 1.2 Ponding layer and additions reservoir are distinct

The same section states that solute transport by surface runoff is simulated by a solute balance of the ponding layer above the soil surface.

Separately, manure and fertilizer additions may be put into an extra artificial reservoir above the compartment division and leach from that reservoir proportional to cumulative precipitation since application.

Table 8 (`INITIAL.INP`, p. 46) makes the distinction explicit for NH4:

- `CONHTOP`: NH4-N concentration in the virtual top layer used for additions;
- `CONH(0:NL)`: NH4-N concentration in soil moisture of compartments 0-NL.

Therefore the virtual additions reservoir is not documentary authority for treating arbitrary residual ponding NH4 as the same state.

### 1.3 NH4 sorption is soil-horizon based

Table 6 (`SOIL.INP`, p. 43) defines the NH4-N sorption coefficient `SOCFNHHO` per soil horizon.

The guide's nitrogen-cycle diagram includes adsorbed NH4 as a soil-system pool, but there is no corresponding documented surface-solid owner for the ponding layer.

This strengthens rejection of an automatic `surface aqueous -> first-soil-layer adsorbed NH4` transition. Such a transfer would cross a compartment and invoke a soil adsorption process that the dry-down event itself does not establish.

### 1.4 The guide's mass balance keeps solution and solid/complex storage separate

Annex 2 reports NH4 storage separately as:

- solution storage at beginning/end of the balance period;
- soil-complex storage at beginning/end.

This is consistent with explicit phase ownership. It provides no documented third dry-surface NH4 store.

## 2. Public ANIMO 4.0 process-description record

The WUR Research Portal confirms the existence and bibliographic identity of:

Groenendijk, P., Renaud, L.V. & Roelsma, J. (2005), *Prediction of nitrogen and phosphorus leaching to groundwater and surface waters; process descriptions of the ANIMO 4.0 model*, Alterra Report 983, 114 p.

Public record:

`https://research.wur.nl/en/publications/prediction-of-nitrogen-and-phosphorus-leaching-to-groundwater-and/`

Public eDepot target:

`https://edepot.wur.nl/35121`

The current research environment can verify the record and abstract, but the eDepot full text is not retrievable through the available web path. Therefore SQ01 still cannot claim what Report 983 says or does not say about the dry-solute continuation problem.

This is a real evidence gap, not evidence of absence.

## 3. ANIMO 3.5 process lineage

The WUR Research Portal also confirms Groenendijk & Kroes (1999), *Modelling the nitrogen and phosphorus leaching to groundwater and surface water with ANIMO 3.5*, Report 144, 138 p., with public eDepot target `https://edepot.wur.nl/363774`.

This source is relevant because the revision-53 `Transsub` lineage predates 4.0. The currently accessible public metadata establish the document identity but not enough text to define a dry-surface continuation phase.

No claim is made that ANIMO 3.5 lacks such semantics until the report itself is reviewed.

## 4. Consequences for the candidate set

The new review does not qualify a corrected-legacy continuation state, but it narrows the interpretation further.

### Candidate A: explicit dry/immobile surface-solute mass

Still the preferred engineering/scientific hypothesis because it can conserve mass without ghost water, false boundary export or phase aliasing.

However, Report 224 does not define the physical identity or rewetting kinetics of that store. Candidate A therefore remains `PROPOSED_MODEL_EXTENSION`, not `CORRECTED_LEGACY_CANDIDATE`.

A useful refinement is to keep its provisional state name chemically noncommittal, for example:

`M_surface_NH4_non_aqueous_continuation [kg N m-2]`

until theory establishes whether the mass should be interpreted as dry residue, crystallized salt, adsorbed material, a residual film phase, or another physical state.

That naming discipline avoids silently choosing new chemistry merely to close mass.

### Candidate B: transfer to existing soil sorption

Further weakened. ANIMO 4.0 explicitly binds NH4 sorption coefficients to soil horizons. No documentary basis was found for automatic transfer of residual ponding NH4 into the first soil horizon at disappearance of ponding.

### Candidate C: residual aqueous water

Further weakened. The documented dissolved storage is `theta * c`, and the hydrological ponding volume may become zero. A positive chemical water floor would therefore be an added hydrological/chemical state unless independently documented.

### Candidate D: additions reservoir reuse

Further weakened. Report 224 explicitly distinguishes `CONHTOP` from `CONH(0:NL)` and assigns the former to additions. Reusing it as generic dry residue would change state meaning and release law.

## 5. Current theory disposition

The strongest defensible statement after this evidence sweep is:

`INSUFFICIENT_ANIMO_SPECIFIC_THEORY_TO_DEFINE_CORRECTED_LEGACY_DRY_PHASE`

with a separate design hypothesis:

`PREFERRED_MODEL_EXTENSION_HYPOTHESIS = EXPLICIT_NON_AQUEOUS_SURFACE_NH4_CONTINUATION_MASS`

This does not qualify dissolution kinetics, adsorption, precipitation, volatilization, residual-water thickness or any other dry-phase chemistry.

## 6. Evidence needed to move beyond the blocker

One of the following is required before corrected-legacy Class-C admission can be reconsidered:

1. full-text review of Alterra Report 983 showing an intended dry/phase continuation state or an unambiguous phase rule;
2. full-text historical ANIMO 3.x/4.x theory or design documentation defining the same;
3. source-history documentation tied to the affected transport formulation that independently defines the state transition;
4. otherwise, explicit reclassification of Candidate A as physics/model evolution with independent scientific review and separate admission.

Until then:

`CORRECTED_LEGACY_CANDIDATE = NOT_ESTABLISHED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`

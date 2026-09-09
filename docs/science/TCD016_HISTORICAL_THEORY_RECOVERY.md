# TCD-016 historical theory recovery

Work unit: `ANIMO-SQ01`

Status: `HISTORICAL_THEORY_STRENGTHENS_CONSERVATION_AND_REPRESENTATION_GAP_BUT_DOES_NOT_DEFINE_DRY_PHASE`

Production migration: `NOT_ADMITTED`

## 1. Purpose and evidence tiers

This follow-up tests whether earlier ANIMO process theory supplies the missing physical semantics for TCD-016.

Evidence is separated strictly:

1. **Canonical frozen source evidence**: `ANIMO_4.1.5.53(3).zip`, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.
2. **Supplied ANIMO 4.0 documentation**: Alterra Report 224 (2005), already pinned in the ANIMO5 evidence model.
3. **Official bibliographic evidence**: Wageningen University & Research publication records for ANIMO 3.5 Report 144 and ANIMO 4.0 Report 983.
4. **Recovered historical full text**: a public secondary mirror of ANIMO 3.5 Report 144. Its title, authors, report number and page count match the official WUR record. It is used as a theory-recovery cross-check, not promoted to immutable B0 bytes.
5. **Search-index snippets for Report 983**: useful only as supporting evidence. They are not a substitute for full-text review.

No external theory source is allowed to silently redefine revision-53 behaviour.

## 2. ANIMO 3.5 Report 144: conservation law and phase storage

The recovered Report 144 text states in section 2.2 that transport must obey conservation of matter. Accumulation is the storage change of a substance and may occur in liquid and solid phases.

The total substance concentration in a soil system is formulated as the sum of:

- liquid storage `theta * c`;
- equilibrium sorbed content;
- non-equilibrium sorbed content;
- precipitated content.

For the dissolved transport coordinate, `theta` is volumetric moisture content and `c` is liquid-phase concentration.

This is important for TCD-016. It establishes a theory-level conservation requirement, but the represented phase set remains liquid plus named soil-solid phases. The recovered theory does not introduce a generic dry surface-solute store.

Qualification consequence:

`MASS_MUST_BE_CONSERVED = THEORY_SUPPORTED`

but:

`DRY_SURFACE_PHASE_IDENTITY = NOT_DEFINED_BY_RECOVERED_THEORY`

## 3. Upper surface reservoir is addition-specific, not a generic residue phase

Report 144 section 2.1.3 describes an imaginary storage reservoir at the soil surface for animal manure and fertilizer additions. Added material is immediately dissolved in that reservoir. Release is described as piston flow driven by cumulative rainfall, and unreleased nutrients are retained by bookkeeping until the precipitation volume equals the reservoir volume.

The same section separately describes surface runoff and distinguishes runoff water interacting with the surface reservoir and first soil layer.

This historical theory strengthens the earlier ANIMO 4.0 User's Guide reading:

- the surface additions reservoir has an explicit management origin;
- it has a specific rainfall-controlled release law;
- it is not a general sink for solute left behind when ponding water disappears.

Therefore Candidate D remains rejected as semantic aliasing.

## 4. NH4 sorption is explicitly a soil-complex phase

Report 144 section 2.4.1 states that ammonium may adsorb to the soil complex, defined by negative surfaces of clay particles and humic compounds. A linear equilibrium sorption relation is used between liquid ammonium and sorbed ammonium.

This is consistent with the supplied ANIMO 4.0 input contract, where the NH4 sorption coefficient is specified per soil horizon.

There is still no theory-supported rule saying that residual NH4 in a disappearing ponding-water compartment is instantaneously deposited into the first soil horizon's sorption complex.

Therefore Candidate B remains rejected as a corrected-legacy candidate.

## 5. Numerical transport theory and the revision-53 low-storage guard

Report 144 section 2.2.3 describes the ANIMO numerical approach:

- model layers are perfectly mixed;
- water fluxes are supplied by the hydrological model;
- moisture content varies linearly during a timestep;
- the rate of aqueous storage is derived from `theta(t) * c(t)`;
- equilibrium sorption is incorporated through an apparent differential sorption coefficient;
- the resulting first-order concentration equation is solved semi-analytically.

Annex 2 gives coefficient functions for combinations of moisture-change and disappearance coefficients. The formulas contain powers and logarithms of terms built from moisture storage plus sorption storage.

The frozen revision-53 `Transsub.for` is directly recognizable as this formulation. It solves:

```text
dc/dt + HV1/(MTO + RHBD*SOCF + HV*t) * c
      = HV2/(MTO + RHBD*SOCF + HV*t)
```

and `Detcoef` implements the corresponding power/log coefficient functions.

However, revision 53 adds an early low-storage branch around this analytical solution. For layer 0 it uses `Factor=100`, and when the final aqueous storage crosses below the threshold it can set `Rsc=0`. The residual mass is forced into the outgoing-water concentration only if `Fu > 1e-6 m d-1`; otherwise the observed `Iflsol=2` route also sets `Avc=0` and returns.

This distinction is now clearer:

- the **underlying historical theory** defines a conservation equation in represented liquid and soil-solid phases;
- the **revision-53 low-storage branch** is a representation/numerical guard at the edge of that formulation;
- the guard itself does not document a new physical dry phase.

Therefore the branch cannot be used as scientific authority for deleting residual mass, nor can its thresholds be promoted to physical phase-transition parameters.

## 6. Wet-from-dry branch does not reconstruct vanished mass

The frozen routine also has the reverse low-storage branch. When final water storage becomes representable while initial storage was below the threshold, it initializes concentration from current forcing and then applies a layer-0 balance correction.

That branch has no independent dry mass coordinate from the preceding timestep. It therefore cannot recover mass that the wet-to-dry branch removed from represented state.

This confirms that the legacy transition pair is not a reversible physical wet/dry state machine.

## 7. Report 983 status

The official WUR Research Portal confirms:

- P. Groenendijk, L.V. Renaud and J. Roelsma;
- *Prediction of nitrogen and phosphorus leaching to groundwater and surface waters; process descriptions of the ANIMO4.0 model*;
- Alterra Report 983;
- 2005;
- 114 pages;
- public eDepot target `https://edepot.wur.nl/35121`.

The abstract states that the report describes process formulations implemented in ANIMO 4.0 and notes changes relative to 3.5, particularly soil-moisture effects on mineralization/denitrification and external crop uptake.

Public search indexing also exposes Report 983 text for a `Surface reservoir` section with wording consistent with the addition-specific reservoir in Report 144. Full report bytes were not retrieved in this workunit, so SQ01 does not make a comprehensive negative claim about every Report 983 paragraph.

Targeted searches did not expose an explicit dry-solute continuation state or dry-to-wet remobilization law. This is evidence of an unresolved gap, not proof that no such sentence exists in inaccessible text.

## 8. Revised interpretation of the four candidates

### Candidate A: explicit non-aqueous surface continuation mass

Historical theory now gives stronger support for why a continuation representation is needed: conservation is explicit, while liquid storage collapses with water volume and the documented solid phases belong to soil chemistry.

It still does **not** identify the physical nature or remobilization kinetics of a dry surface phase.

Status remains:

`PREFERRED_PROPOSED_MODEL_EXTENSION_NOT_CORRECTED_LEGACY`

### Candidate B: first-soil-layer sorption

Further rejected. Historical ANIMO theory identifies ammonium sorption with the soil complex, not with disappearance of ponding water.

### Candidate C: residual aqueous water

Further rejected under current ANIMO hydrology. Historical transport theory uses actual moisture content supplied by hydrology. A positive chemical water floor would add a state not supplied by the hydrological model.

### Candidate D: additions reservoir

Further rejected. Historical theory explicitly defines the surface reservoir around added manure/fertilizer and rainfall-driven release.

## 9. Revised atomization conclusion

The historical recovery strengthens the separation between the two child questions.

### TCD-016-C1

The need for a conserved continuation destination is now supported by historical conservation theory, not only by code diagnostics.

But the physical identity remains undefined.

Current gate result:

`THEORY_SUPPORTED_CONSERVATION_REQUIREMENT_AND_REPRESENTATION_GAP`

not:

`THEORY_QUALIFIED_DRY_PHASE`

### TCD-016-E1

The low-storage threshold and `Fu > 1e-6` route are more defensibly treated as numerical/representation policy layered around the semi-analytical transport equation. They must be qualified only after C1 establishes the physical state semantics.

No threshold value is admitted as physics.

## 10. Qualification disposition

The stronger historical evidence does not justify a corrected-legacy Class-C admission.

The defensible result is:

`BLOCKED_TCD016_INSUFFICIENT_THEORY_FOR_CORRECTED_LEGACY_ADMISSION`

with:

`PREFERRED_EXTENSION_HYPOTHESIS = EXPLICIT_NON_AQUEOUS_SURFACE_NH4_CONTINUATION_MASS`

and:

`PRODUCTION_MIGRATION = NOT_ADMITTED`

The key unresolved scientific question has become narrower: not whether conservation requires a destination, but what physical surface phase that destination represents and what law governs later remobilization.

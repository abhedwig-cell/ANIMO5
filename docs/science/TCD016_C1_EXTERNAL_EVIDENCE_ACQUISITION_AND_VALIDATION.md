# ANIMO-SQ10 — TCD-016-C1 external evidence acquisition and rewetting validation

## Scope

SQ10 follows the closed negative Class-F assessment in `ANIMO-SQ09@d7f63e56daef8285e6a137774c703131a1100fa2`.

It does not change the SQ09 candidate, production source, frozen B0, the TCD register, the global B3 queue, aggregate/routing authority, the central testbank registry, TCD-016-E1, B4, or production authorization.

The only question is whether new external scientific evidence can unlock the two SQ09 blockers for the research-isolated candidate `REWETTABLE_SURFACE_NH4_N_RESIDUE_EQUIVALENT`:

1. authoritative theory or an equivalent traceable material-to-process basis;
2. process-specific validation of rewetting behavior.

## Frozen starting point

The inherited continuation state remains:

- `M_surface_NH4_non_aqueous_continuation`;
- unit `kg N m-2`;
- owner `SURFACE_CHEMISTRY_PONDING_CONTROL_VOLUME`;
- chemically noncommittal with respect to material phase and molecular speciation;
- persistent under the fail-closed no-process rule while no separately qualified process is active.

SQ09 defined a bounded candidate in which explicit positive surface aqueous storage triggers an atomic complete transfer of the continuation pool to `SURFACE_AQUEOUS_NH4_STORAGE`. SQ09 qualified that contract algebraically but not physically.

GitHub issue #48 records the prior internal-evidence exhaustion finding: frozen ANIMO source and documentation do not identify the residual material or supply a rewetting law. SQ10 therefore does not repeat the internal source audit.

## Bounded external acquisition

The search was deliberately targeted at four evidence families:

1. dry/wet ammonium fixation and defixation;
2. surface ammonium/ammonia volatilization and aqueous equilibrium;
3. phase-specific ammonium-salt water uptake/deliquescence;
4. direct dry-residue to rewetting experiments that might discriminate complete, partial, delayed or alternative-receiver behavior.

The key admissibility rule is stronger than generic chemical plausibility. A source can unlock the candidate only if its material identity and process domain can be mapped traceably to the ANIMO continuation state and if it supports the candidate receiver, activation and transfer law.

## Evidence found

### Ammonium fixation and defixation

Nieder, Benbi and Scherer (2011), DOI `10.1007/s00374-010-0506-4`, review ammonium fixation and defixation in soils. They show that NH4 can be rapidly fixed in mineral interlayers and that fixation and subsequent availability depend strongly on soil mineralogy, moisture conditions and other environmental factors.

This is not evidence that the ANIMO continuation owner is clay-fixed NH4. It is important counterevidence to any universal claim that all retained NH4-N must immediately return to an aqueous surface pool on rewetting whenever contact with soil/mineral surfaces is physically possible.

Opuwariboi and Odu (1975), DOI `10.1111/j.1365-2389.1975.tb01960.x`, report substantial retained added ammonium after repeated alternate wetting and drying in soils. Again, the system is not the ANIMO surface state, but it establishes that wet-dry cycling does not by itself imply complete immediate aqueous recovery.

### Ammonia volatilization and aqueous-surface behavior

Montes, Rotz and Chaoui (2009), DOI `10.13031/2013.29133`, review and validate process relationships for ammonia volatilization from ammonium solutions and manure surfaces. Temperature, pH, ionic strength and air-flow mass transfer all matter.

Bouwman et al. (2002), DOI `10.1029/2000GB001389`, synthesize agricultural ammonia volatilization evidence and likewise show that ammoniacal nitrogen can follow different pathways depending on pH, cation-exchange capacity, water, temperature, fertilizer form and management.

These sources strengthen the requirement for an explicit state/process mapping. They do not validate the dry-residue identity or complete instantaneous redissolution assumed by candidate M1.

### Phase-specific water uptake

Brooks et al. (2002), DOI `10.1029/2002GL014733`, provide laboratory evidence for high water solubility and deliquescence of identified ammonium-sulfate material.

This makes a rewettable-residue mechanism chemically plausible for at least some known ammonium salt phases. It does not identify the TCD-016 continuation state as ammonium sulfate or another specific salt. SQ08 explicitly left phase, counter-ion and molecular speciation unresolved. Therefore this analogue cannot be promoted to a material mapping.

## Adversarial synthesis before formal review

The external literature does not point to one unique law. It instead makes several competing mechanisms credible:

- rapid aqueous remobilization for some identified soluble salts;
- partial or delayed remobilization when material is retained/fixed;
- alternative receivers where soil or minerals participate;
- atmospheric loss controlled by NH4/NH3 chemistry and environmental state.

Therefore the candidate remains scientifically underdetermined. Parameter-free construction and exact mass conservation do not resolve this underdetermination.

No located study reproduces the exact TCD-016 sequence with a traceable material identity: ponded surface NH4, dry-down to zero explicit surface aqueous storage, quantified retained mass, and time-resolved rewetting with receiver-resolved and gaseous mass closure.

The statement above is bounded to the SQ10 search. It is not a claim that no such study or dataset exists anywhere.

## Class-F disposition

After evidence acquisition:

- scientific rationale: `PASS_BOUNDED`;
- authoritative theory/material mapping: `FAIL`;
- relation to preserved B3 baseline: `PASS`;
- calibration/parameter implications: `PASS`;
- conservation implications: `PASS`;
- process-specific validation: `FAIL`;
- expected differences: `PASS_AT_CONTRACT_LEVEL_ONLY`;
- historical behavior: `UNKNOWN_WITHOUT_B2`.

The bounded result is:

`QUALIFIED_EVIDENCE_ACQUISITION_COMPLETE_NO_CLASS_F_UNLOCK`

This is not a rejection of the candidate as impossible. It is a determination that current evidence does not scientifically select it over plausible alternatives.

## Minimum next empirical evidence

A useful next experiment or equivalent traceable dataset must follow a controlled dry-down and rewetting sequence and close the nitrogen mass across the relevant compartments. At minimum it should measure initial surface aqueous NH4-N, retained total NH4-N after drying, time-resolved aqueous NH4-N after rewetting, any soil/mineral receiver where contact is possible, and gaseous NH3-N where relevant. Material or phase characterization must be sufficient to connect the retained pool to a process law.

Metadata must include temperature, pH, ionic composition/counter-ions, surface or soil material, water depth/storage, drying endpoint, and rewetting amount/timing.

The evidence must be able to distinguish at least:

- complete instantaneous surface-aqueous remobilization;
- partial remobilization;
- delayed or finite-rate remobilization;
- direct or competing soil/mineral receiver behavior;
- irreversible or gaseous loss.

Until such evidence or an equivalent traceable material-identity basis exists, do not retry positive Class-F scientific admission and do not qualify TCD-016-E1 on top of the unqualified rewetting process.

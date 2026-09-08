# ANIMO-PREP03 — ANIMO 4.0 documentation to 4.1.5 revision-53 source reconciliation

Status: `SOURCE_BOUND_PARTIAL_RECONCILIATION_NO_SCIENTIFIC_ADMISSION`.

## Work-unit contract

Purpose: identify which parts of the supplied ANIMO 4.1.5 revision-53 source can and cannot be interpreted from the supplied ANIMO 4.0 User's Guide, and turn those differences into explicit qualification surfaces before ANIMO5 migration.

Affected components: documentation evidence, parser contracts, state/process inventory and migration qualification planning only.

Physics change: no.

Numerical-policy change: no.

Expected differences to model output: none. No legacy source or testcase is modified.

Verification contract: every claim below is source-bound to the frozen source archive or to an explicit statement in the supplied ANIMO 4.0 User's Guide. Absence from the 4.0 guide is not treated as proof of absence from every historical ANIMO 4.0 code line; it is treated as a documentation-version gap.

## Baseline identities

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Supplied User's Guide SHA-256:

`ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

The User's Guide explicitly describes ANIMO 4.0. The source archive self-identifies as ANIMO 4.1.5 revision 53. Therefore this reconciliation is deliberately asymmetric: the guide is authoritative evidence for documented 4.0 behaviour, not automatic truth for 4.1.5.

## 1. Stable 4.0 core still recognizable in revision 53

The main scientific skeleton described in the guide remains visible in the later source:

- compartment-based water-driven transport;
- fresh organic matter, dissolved organic matter, exudate and humus/biomass transformations;
- NH4-N and NO3-N mineral nitrogen;
- PO4-P sorption/precipitation;
- crop uptake;
- original oxygen-diffusion aeration and SONICG moisture response;
- externally supplied detailed or aggregated hydrology;
- additions and tillage;
- balance compilation in `Outbal_calc` and writing in `Outbal_write`.

This is enough to use the 4.0 guide as a terminology and conceptual cross-check for those inherited surfaces. It is not enough to qualify the exact revision-53 equations or tolerances.

## 2. GHG is a post-guide scientific surface

The 4.0 guide's documented input contract has no greenhouse-gas option and its ordinary output selection ends at `OUTSE(37)`.

Revision-53 source contains a substantial greenhouse-gas subsystem:

- `GHGasses` orchestration;
- methane production, oxidation, transport and emission in `ghg_ch4.for`;
- nitrous-oxide production, reduction, transport and emission in `ghg_n2o.for`;
- `GHGtransport` and `GHGtranssub`;
- `GreenHouseGasOption` in ANIMO 4.1 input;
- CH4/N2O initial states and restart output;
- GHG terms in aeration, denitrification, mineralisation, balances and selected outputs;
- GHG output indices in the later output surface.

Source history comments place much of this work in 2007-2009 and describe a 2011 ANIMO 4.1 release. This agrees with the already-open TCD-008 documentation-version gap, but does not resolve it. Exact revision-53 equations still require a matching formulation source and reference case.

Migration consequence: GHG must be its own qualification-owned process family. It must not be inferred from the 4.0 C/N theory and must not be folded into an undifferentiated `nitrogen` migration.

## 3. Stable dissolved organic matter is an additional state model

The 4.0 guide describes one dissolved organic matter pool in the C/N/P cycles.

Revision-53 source contains an additional explicitly labelled `stable dom pool + revision of labile dom pool` surface, including:

- `CoStdiorma`, `CoStdiorni`, `CoStdiorpo` states;
- separate restart/current/average values;
- `Socfdom` and `Socfsdo` sorption coefficients;
- `recfSDO` and `recfHUSDO` transformation parameters;
- the `>sordom:` input area;
- stable-DOM participation in additions, initialization, transport, balance accounting and outputs;
- selected outputs for stable DOM, DON and DOP and their sorbed/total forms.

This is not a cosmetic output extension. It changes the represented chemical state and its storage/transport accounting.

Migration consequence: labile DOM and stable DOM require separate explicit state ownership in ANIMO5. A compatibility layer that collapses them into one generic DOM pool would destroy revision-53 semantics.

## 4. ANIMO 4.1 input grammar is not a rename-only change

The supplied testbank uses `Animo41` steering files. Revision-53 has a distinct named-key parser for that path, including options such as:

- `HydrologicInput`;
- `PhosphorusCycle`;
- `SulphateSimulation`;
- `AerationModel`;
- `CropUptakeModel`;
- `MacroPoreOption`;
- `GreenHouseGasOption`;
- `SoilTempFile`;
- `PClassOption` and related P-class controls.

The 4.0 guide documents positional records under labels. This difference must be treated as an input-contract version change, not merely formatting.

### ANIMO40 compatibility seam in revision 53

Revision-53 still recognizes `Animo40`, but its `>simopt:` parser reads six integers:

`Iwa, Ipo, Ioptae, Ioptcu, Ioptmp, IoptGHG`

where the supplied 4.0 guide documents five switches:

`IWA, IPO, ioptAE, ioptCU, ioptMP`.

Revision-53 also first attempts 40 `OUTSE` values on the ANIMO40 path and falls back to the documented 37-value form if that read fails.

The supplied testbank does not exercise `Animo40`; every discovered steering file starts with `Animo41`.

Interpretation: revision-53 contains compatibility code, but exact backward compatibility with the published 4.0 grammar is not qualified. Do not use the mere existence of the `Animo40` branch as proof that old 4.0 cases are plug-compatible.

## 5. Output surface expanded from 37 to a much larger state/process view

The supplied guide documents 37 `OUTSE` selections. Revision-53 `Animo41` parsing validates output indices 1 through 78.

The later surface adds, among others:

- time-averaged liquid N and P;
- DOM and stable-DOM state variants;
- soil temperature and vertical flux;
- potential denitrification and soil respiration;
- CO2, CH4 and N2O state/process outputs;
- P saturation degree;
- soil scheme and groundwater-relative summary products.

Migration consequence: legacy output indices are evidence about state/process observability, not an API design. ANIMO5 should expose typed diagnostics from owned state/process components and provide legacy formatting as an adapter where required.

## 6. `SulphateSimulation` is parser-visible but no process implementation is present

Revision-53 `input1.for` reads and range-checks `SulphateSimulation` into `IoptSul`. A source-wide search of the supplied archive finds `IoptSul` only in the active and alternate input parsers. No downstream process routine consumes it.

Likewise, `PrintBalSulphate` is read into `Outba(:,5)`, but `Outbal_write` branches only on balance selectors 1 through 4. No sulphate process/state symbols or sulphate balance implementation were found elsewhere in the supplied source units.

This is stronger than a documentation gap. For the supplied revision-53 bytes, the exposed sulphate switches are non-operational configuration surface.

Migration consequence: ANIMO5 must not advertise sulphate support merely because the legacy parser accepts these keys. The option should be classified unsupported unless a missing source component or authoritative implementation is recovered.

## 7. P-class logic is a later uptake/management policy surface

Revision-53 contains `PClassOption`, `PClassYearSwitch`, `PClass`, PAL/Pw class thresholds and `ChoosePClass`. The selected class controls class-indexed crop uptake and crop-loss arrays and is revisited during initialization/year transitions.

The supplied 4.0 guide documents crop uptake, including external crop input, but not this later P-class policy.

Migration consequence: P-class logic is not generic file parsing. It is a version-specific crop/management policy that can change forced uptake/loss trajectories and therefore needs explicit scientific ownership and qualification.

## 8. Macropores remain a separate unresolved version surface

The 4.0 guide explicitly warns that the macropore option is not fully operational. Revision-53 contains dedicated MAPO hydrology and transport units and many macropore state/flux arguments.

This is already TCD-007. PREP03 adds only an architectural consequence: macropore state and matrix state should be separate owned domains in ANIMO5. No macropore production migration is admitted without a matching theory source and qualified testcase.

## 9. Theory hierarchy for migration

The evidence now supports a practical hierarchy:

1. **Inherited 4.0 core**: the guide can define terminology and expected process families, but exact revision-53 behaviour still needs reference qualification.
2. **Post-4.0 scientific extensions**: GHG, stable DOM, P-class and later macropore behaviour require separate theory/source reconciliation.
3. **Parser-only or operational surface**: named-key input grammar, output selection and file conventions belong in adapters, not scientific state.
4. **Exposed but non-operational surface**: sulphate must fail closed rather than being copied into ANIMO5 as a nominal feature.

## Gate

`PARTIAL_4_0_TO_4_1_5_RECONCILIATION_ESTABLISHED_REFERENCE_AND_EXTENSION_THEORY_STILL_REQUIRED`

This work does not qualify revision-53 scientific behaviour, does not resolve PREP02's historical-reference blocker and does not admit production migration.
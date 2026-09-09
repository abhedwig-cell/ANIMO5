# Revision-53 stable-DOM theory qualification

Decision: `THEORY_PARTIALLY_RECONSTRUCTED_WITH_VERSION_LABEL_CONFLICT`

Production migration: `NOT_ADMITTED`

## 1. Scope and evidence boundary

The frozen ANIMO 4.1.5 revision-53 source contains a distinct stable dissolved organic matter state family for C, N and P. The supplied ANIMO 4.0 User's Guide does not. TH01 therefore does not infer the stable-DOM formulation from the source alone and does not treat the version label used by a later external research branch as proof of the lineage of the frozen revision-53 bytes.

The exact source archive remains identified by SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

## 2. Independent scientific provenance

### 2.1 2008 WUR precursor evidence

Classification: `PUBLIC_SECONDARY_MODEL_DESCRIPTION`

Hendriks, Walvoort & Jeuken (2008), Alterra Report 619, evaluated SWAP-ANIMO for peatland nutrient loading and explicitly recommended adding a second dissolved-organic-matter pool so labile/fresh organic matter could be distinguished from more stable peat-derived organic matter.

Public WUR record:

`https://research.wur.nl/en/publications/evaluation-of-the-applicabillity-of-the-swap-animo-model-for-simu/`

This establishes a dated scientific motivation for a second DOM pool. It does not specify the later implementation equations.

### 2.2 2011 UFZ/BMBF implementation-lineage evidence

Classification: `CONFLICTING_EVIDENCE`

A 2011 BMBF/UFZ final report, project FKZ 02WT0913, describes an ANIMO model-development effort that started from ANIMO 3.8 and added a stable dissolved organic matter pool. The report states that ANIMO developers at Alterra/Wageningen actively participated in the modifications and that the resulting new version was also used at Alterra.

Public report:

`https://edocs.tib.eu/files/e01fb12/72746826X.pdf`

The model-development section is unusually specific. Its process diagram contains:

- `Stable Dissolved organic matter (SDO)`;
- `Sorbed stable DOM`;
- `Ratio_rd_st`;
- `sdofr`;
- `recfSDO`;
- `recfHSDO`;
- `asfaSDO`;
- explicit routes between fresh organic matter, ordinary dissolved organic matter, SDO, humus/biomass and CO2.

This nomenclature and graph structure strongly overlap with the frozen revision-53 implementation, which uses `Ratio_rd_st`, `SDOfr`, `recfSDO`, `recfHUSDO`, `asfaSDO`, stable-DOM sorption and the corresponding pools.

That content makes the report substantially stronger than a generic later application description. It is independent scientific and provenance evidence for the carbon-side formulation family.

However, the report calls its improved branch `ANIMO Version 4.0`. That conflicts with the supplied 2005 ANIMO 4.0 User's Guide, which has only one DOM pool and predates the 2007-2010 project. The external report also says the work began from ANIMO 3.8 and progressed through model modifications. TH01 therefore does not equate its `4.0` label with the supplied 2005 canonical ANIMO 4.0 documentation lineage.

The defensible conclusion is narrower:

`STABLE_DOM_FORMULATION_LINEAGE_STRONGLY_LINKED_TO_ANIMO_AND_ALTERRA_BUT_EXACT_RELEASE_NUMBERING_UNRESOLVED`

## 3. Revision-53 implementation correspondence

Classification for correspondence with the 2011 carbon diagram: `PUBLIC_SECONDARY_MODEL_DESCRIPTION` plus `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY`.

Primary frozen-source surfaces include:

- `resp_miner.for`;
- `Rates.for`;
- `Addit.for`;
- `Transca.for`;
- `Init.for`;
- `Outbal_Init.for`;
- `Outbal_calc.for`;
- `input1.for`.

The source contains stable-DOM C, N and P concentrations such as `CoStdiorma`, `CoStdiorni` and `CoStdiorpo`, plus start/result/average and restart variants. It also contains stable-DOM sorption and transformation parameters including `SocfSDO`, `recfSDO`, `recfHUSDO`, `asfaSDO`, `SDOfr` and `Ratio_rd_st`.

At the carbon-process level, the correspondence with the public 2011 process diagram is strong enough to support the broad intended structure:

1. a separate stable dissolved-organic pool exists;
2. it can be sorbed;
3. fresh organic matter and ordinary DOM can feed stable DOM;
4. stable DOM can turn over;
5. stable DOM exchanges with humus/biomass;
6. part of the turnover is dissimilated toward CO2.

The exact revision-53 algebra, temporal integration and parameter calibration remain source-defined unless independently matched line by line.

## 4. C versus N/P evidence strength

The independent 2011 formulation evidence is explicitly a carbon-cycle development. The revision-53 source generalizes stable DOM to dissolved organic N and P as well.

TH01 therefore separates the evidence strength:

- stable-DOM carbon state and broad transformation topology: `MEDIUM_HIGH`;
- exact carbon equations and parameter semantics in revision 53: `MEDIUM`;
- extension of the same topology to DON and DOP: `MEDIUM_LOW_TO_MEDIUM`;
- exact N/P stoichiometric coupling and transformation algebra: `IMPLEMENTATION_DERIVED_NOT_INDEPENDENT_THEORY` unless separately documented.

It would be an overclaim to use the carbon-only external diagram as independent authority for every revision-53 N/P equation.

## 5. Governing states, transfers and conservation

The frozen source and PREP06 establish stable DOM as physical state, not reporting state. A future B3/B4 ledger therefore has to preserve at least:

- dissolved stable organic C, N and P mass;
- sorbed stable organic C, N and P where represented;
- transport with water;
- exchange with sorbed state;
- internal transfers from fresh organic matter and labile DOM;
- internal exchange with humus/biomass;
- dissimilation/mineralisation products;
- beginning/end storage symmetry and explicit restart ownership.

For each element, internal transformation partitions must conserve that element subject to explicitly modelled gaseous or mineral sinks/sources.

## 6. Theory/code conflict: TCD-023

In `resp_miner.for` Case(2), the frozen source computes the stable-DOM phosphorus decay amount in `Transfop(17)` but forms the two subsequent P partition terms from `Transfon(17)`. The corresponding C and N branches partition their own elemental term, and other stable-DOM P branches use the P-specific quantity.

This is a cross-species algebra inconsistency. PREP04 demonstrated that the branch is reachable and that the two-line source-only correction changes the P source term and collapses the associated local/annual P residual in the exercised case.

The theory classification is:

`THEORY_CODE_CONFLICT`

The correction is still not B3-admitted. Exact historical behaviour and unrounded P-state consequences remain part of the later discrepancy qualification contract.

## 7. Activation, parameters and temporal assumptions

The stable-DOM extension is always part of the source state/parameter system rather than a single top-level on/off module comparable to `GreenHouseGasOption`. Its effective activity is controlled by material parameters and available stores.

Revision-53 source exposes, among others:

- split toward stable versus labile routes through `Ratio_rd_st` and `SDOfr`;
- stable-DOM decay through `recfSDO`;
- stable-DOM-to-humus partition through `asfaSDO`;
- humus/stable-DOM exchange through `recfHUSDO`;
- separate stable-DOM sorption through `SocfSDO`.

The 2011 process diagram supports the broad meaning of most carbon-side parameters by name and topology. Exact units, averaging rules, environmental modifiers and N/P generalization still require revision-specific reconciliation.

## 8. B3 judgement

Current reconciliation state:

`THEORY_PARTIALLY_RECONSTRUCTED`

B3 readiness:

`BLOCKED_VERSION_LINEAGE_NP_EXTENSION_AND_TCD023_QUALIFICATION`

What can already be judged scientifically:

- collapsing stable DOM into the old single ANIMO-4.0 DOM pool would lose intended state structure;
- the broad carbon-side stable-DOM topology has independent support;
- TCD-023 contradicts elemental/species-consistent partitioning;
- stable-DOM storage must be represented explicitly in conservation accounting.

What cannot yet be admitted:

- exact historical revision-53 state trajectories;
- exact parameter provenance and calibration domain;
- every N/P transformation equation;
- a corrected TCD-023 production baseline.

A B2 comparison remains required for historical preservation where available. If B2 cannot be recovered, EB01's independent-scientific-admission fallback would need a stronger process-specific package than this theory note alone.
# ANIMO-GHG01 — GHG ledger reconciliation

Status: `GHG_C_N_LEDGER_NOT_CLOSED_SOURCE_BOUND_CONSERVATION_AND_REPORTING_GAPS_IDENTIFIED`

This document extends the PREP06 state/transfer inventory specifically for the greenhouse-gas subsystem. It is a source qualification, not a corrected implementation and not a claim about historical executable behaviour.

Frozen source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Pinned PREP06 evidence head:

`work/animo-prep06-conserved-state-ledger@9b1f1ea51c24fb82823290193651830dc61ea3c8`

## 1. PREP06 ownership baseline

PREP06 already identifies greenhouse-gas state families as physical source state rather than balance-array state:

- CH4: `CoCH4/CsCH4 -> RsCoCH4/RsCsCH4`;
- N2O: `CoN2O/CsN2O -> RsCoN2O/RsCsN2O`;
- owner/mutator family: `GHGasses`, `GHG_Methane`, `GHG_NitrousOxide` and shared GHG transport;
- accepted/trial state separation follows the wider revision-53 state transaction pattern.

That ownership model is supported by the deeper GHG audit. The gas states are genuine dynamic stores. They are not merely output variables.

The qualification question is therefore stricter than whether ANIMO prints CH4 or N2O. A full C/N ledger must reconcile source-pool depletion, gas production, gas storage change, interphase transport, oxidation/reduction and boundary emission without creating or deleting conserved C or N.

## 2. Expected transfer structure

For methane the complete carbon chain should be representable as:

```text
organic-C source pool
  -> CH4-C production
  -> CH4-C gas/liquid system storage
  -> oxidation to CO2-C and/or atmospheric CH4-C emission
```

For nitrous oxide the nitrogen chain should be representable as:

```text
NH4-N or NO3-N
  -> N2O-N production
  -> N2O-N gas/liquid system storage
  -> reduction to N2-N and/or atmospheric N2O-N emission
```

Internal phase transfer and vertical/lateral gas transport are not external losses until the model boundary is crossed. A GHG-inclusive MassLedger therefore needs the gas stores explicitly, even if the older nutrient balances choose a smaller control volume and book conversion to gas as a terminal loss.

## 3. CH4 source-pool reconciliation

### 3.1 Production is generated from four source families

`ghg_ch4.for::CH4produc` apportions total CH4-C production over:

- dissolved organic matter: `QPrCH4Do`;
- exudates: `QPrCH4Ex`;
- humus: `QPrCH4Hu`;
- fresh organic-matter fractions: `QPrCH4Os`.

These contributions are then added to the CH4 transport source term.

### 3.2 Only DOM has an active source depletion path outside `GHG_Miner`

`Rates.for::Rates2` contains an active GHG block that converts `QPrCH4Do` to a zero-order DOM sink and subtracts the associated organic N and P according to current dissolved-organic composition.

No equivalent active depletion transfer for `QPrCH4Ex`, `QPrCH4Hu` or `QPrCH4Os` was found outside `GHG_Miner`.

### 3.3 The intended comprehensive methanogenesis transfer routine is not active

`ghgasses.for` contains `GHG_Miner`, whose own source documentation states that it calculates organic C/N/P mineralisation due to methanogenesis and adds the resulting terms to ordinary mineralisation, CO2 and subsidence accounting. It explicitly handles DOM, exudates, humus and fresh organic matter.

The two calls to `GHG_Miner` in `resp_miner.for` are commented out in the frozen revision-53 source. The first would calculate methanogenesis mineralisation terms. The second would merge those terms into general mineralisation and calculate CO2/subsidence output terms.

No other active call to `GHG_Miner` was found.

Source-bound consequence:

`QPrCH4Ex`, `QPrCH4Hu` and `QPrCH4Os` can contribute positive CH4-C production while the intended routine that removes corresponding material from those source pools is inactive. This is a conservation-path gap in the supplied source. Its numerical magnitude is not qualified because no supplied revision-53-compatible GHG case reaches the branch.

Classification:

`SOURCE_CONFIRMED_INCOMPLETE_METHANOGENESIS_SOURCE_POOL_TRANSFER_PATH_REFERENCE_UNEXERCISED`

## 4. CH4 oxidation, CO2 and subsidence reporting

`GHG_Methane` actively removes CH4 through soil and plant oxidation terms `QOxCH4Soi` and `QOxCH4Plt` and couples soil oxidation to oxygen demand.

However, the intended conversion of those terms into CO2/subsidence accounting is located inside `GHG_Miner`. Because its calls are commented out, a complete active C-transfer chain from CH4 oxidation to the GHG CO2/subsidence reporting state was not found.

This is visible in source state as well:

- `AmCO2(0:NL)` is passed through `resp_miner`/main/output interfaces and is written by GHG output routines;
- active assignments to `AmCO2` were found only inside `GHG_Miner`;
- the apparent `AmCO2(0)=0` initialization in `resp_miner.for` is itself commented out;
- `Subsd` is likewise calculated inside `GHG_Miner` and otherwise only consumed by output code.

Therefore revision-53 GHG CO2 and subsidence output variables do not have a complete active producer path in the frozen source as audited.

This must not be converted into a historical claim such as “the old executable emitted random CO2”. Compiler storage/initialization behaviour and the native historical runner are not qualified. The source-level statement is narrower: these values are consumed without a source-confirmed active assignment on the audited path.

Classification:

`SOURCE_CONFIRMED_GHG_CO2_SUBSIDENCE_PRODUCER_PATH_INACTIVE_HISTORICAL_RUNTIME_EFFECT_UNRESOLVED`

## 5. Main balance observer has disconnected GHG working arrays

`Outbal_calc.for` uses three arrays in its GHG-specific observer terms:

- `AmCH4(0:Manl)`;
- `AmN2Odeni(0:Manl)`;
- `AmN2Onitr(0:Manl)`.

`AmN2Onitr` is actively calculated inside `Outbal_calc` from the nitrification fraction, `Rekinh`, average NH4 concentration, moisture, layer thickness and timestep.

The other two arrays are different:

- `AmCH4` is declared in the routine but is not in the `Outbal_calc` argument list and no assignment to `AmCH4` exists in `Outbal_calc` or elsewhere under that symbol;
- `AmN2Odeni` is likewise declared but not passed into the routine and no assignment to that symbol exists.

They are nevertheless consumed by the GHG observer:

```text
OmCH4 = AmCH4(Ln) / Cfracom
Btom(CH4e) <- AmCH4(0)
Bani(N2Od) <- AmN2Odeni(Ln)
Bani(N2Oe) <- AmN2Odeni(0) + AmN2Onitr(0)
```

The physical GHG process arrays available in the main program are instead `QPrCH4`, `QPrN2Oden`, `QPrN2Onit`, `QRdN2O`, gas states and emission fluxes. They are not supplied to `Outbal_calc` for these observer terms.

This is a source-interface/reporting defect independent of the GHGMais parser mismatch.

Classification:

`SOURCE_CONFIRMED_GHG_OUTBAL_DISCONNECTED_UNASSIGNED_WORKING_ARRAYS_HISTORICAL_RUNTIME_EFFECT_UNRESOLVED`

## 6. N2O physical-state chain versus nutrient ledger

The active N2O process code is more internally connected than the CH4 source-pool path:

- nitrification partitions NH4 transformation between NO3 and N2O using `FrNitrN2O`;
- denitrification calculates NO3-to-N2O production and N2O-to-N2 reduction;
- `Rekonide` is adjusted so the definitive nitrate transport/reaction calculation reflects the denitrification competition;
- `GHGtransport` evolves N2O liquid/gas state and boundary emission.

The standard nitrate balance, however, treats denitrification as a nitrate loss from its nutrient control volume. It does not add `CsN2O/RsCsN2O` as a stored N end state. The gas can therefore be physically present inside the model profile after nitrate-N has already left the conventional nitrate ledger.

That can be a legitimate smaller control-volume definition for a nutrient-leaching balance, but it is not a complete model-wide nitrogen conservation ledger once GHG state is included.

The GHG-specific `N2Od`/`N2Oe` observer additions do not solve this because:

1. they are not included as canonical gas end-state storage in the ordinary `Ddev` residual;
2. the denitrification observer term depends on the disconnected `AmN2Odeni` array described above.

Verdict:

`N2O_PROCESS_STATE_EXISTS_BUT_FULL_MODEL_N_LEDGER_DOES_NOT_CLOSE_OVER_GAS_STORAGE_AND_EMISSION`

## 7. CH4 physical-state chain versus organic-C ledger

The same control-volume problem is stronger for CH4.

`RsCsCH4` is a real end-of-step C store, and CH4 emission components are explicit model-boundary fluxes. Neither `CsCH4` nor `RsCsCH4` participates in the main organic-matter balance end-state calculation in `Outbal_calc`.

A full C ledger therefore cannot be reconstructed from the standard OM balance alone. It must include at least:

- organic source-pool depletion caused by methanogenesis;
- start/end CH4 system storage;
- CH4 oxidation transfer to CO2;
- CH4 diffusion, air-flow, ebullition and plant-mediated boundary fluxes;
- CO2 boundary emission where the selected GHG C accounting requires it.

Because the comprehensive source-pool transfer routine is inactive, the current source does not provide a complete closed chain for all of these transfers.

Verdict:

`CH4_FULL_MODEL_C_LEDGER_NOT_CLOSED`

## 8. Process-by-process ledger assessment

| GHG transfer | Physical source implementation | Main C/N ledger integration | Qualification |
| --- | --- | --- | --- |
| DOM-C -> CH4-C | Active CH4 production plus active DOM sink in `Rates2` | Gas storage not included in standard OM end state | `PARTIAL` |
| exudate-C -> CH4-C | Active CH4 production | Intended source depletion in inactive `GHG_Miner` | `NOT_CLOSED` |
| humus-C -> CH4-C | Active CH4 production | Intended source depletion in inactive `GHG_Miner` | `NOT_CLOSED` |
| fresh-OM-C -> CH4-C | Active CH4 production | Intended source depletion in inactive `GHG_Miner` | `NOT_CLOSED` |
| CH4 oxidation -> CO2 | Active CH4 sink and oxygen coupling | GHG CO2 producer/accounting path depends on inactive `GHG_Miner` | `NOT_CLOSED` |
| CH4 storage -> atmospheric CH4 | Active GHG transport/emission | Not represented as canonical C storage plus boundary transfer in standard OM ledger | `NOT_CLOSED` |
| NH4-N -> N2O-N | Active process partition | NH4/nitrification accounting partly split; N2O gas store absent from conventional N end state | `PARTIAL` |
| NO3-N -> N2O-N -> N2-N | Active coupled N2O/denitrification process | nitrate loss is represented, but gas storage and GHG observer are not a closed full-N ledger | `PARTIAL_NOT_MODEL_WIDE_CLOSED` |
| N2O storage -> atmospheric N2O | Active gas transport/emission | no canonical N gas-storage term in standard N residual; observer denitrification array disconnected | `NOT_CLOSED` |
| base aerobic/denitrifying CO2 from organic transformation | ordinary ANIMO process/ledger exists | GHG-selected CO2/subsidence extension has inactive producer path | `BASE_LEDGER_ONLY` |

## 9. PREP06 integration consequence

PREP06 should retain `G-CH4` and `G-N2O` as canonical physical state families. GHG01 strengthens the architectural consequence:

A future ANIMO5 MassLedger cannot infer complete C/N conservation from the legacy `Btom`, `Bani`, `Bano` or `Bfom/Bahu/Bdom` arrays. It must observe explicit typed transfers between organic/mineral source stores, GHG gas stores and external atmosphere boundaries.

Minimum future ledger contract, before implementation admission:

- `CH4_PRODUCTION`: source organic-C store -> CH4-C store;
- `CH4_OXIDATION`: CH4-C store -> CO2-C boundary/store according to chosen physical state model;
- `CH4_EMISSION_*`: CH4-C store -> atmosphere, separated by diffusion, air flow, ebullition and plant transport;
- `N2O_NITRIFICATION`: NH4-N -> N2O-N;
- `N2O_DENITRIFICATION`: NO3-N -> N2O-N;
- `N2O_REDUCTION`: N2O-N -> N2-N atmosphere/boundary;
- `N2O_EMISSION_*`: N2O-N store -> atmosphere;
- start/end `CH4-C` and `N2O-N` storage included in model-wide residuals.

The legacy balance arrays may remain useful diagnostic observers, but they cannot be treated as authoritative physical state or as proof of conservation.

## 10. Qualification and blocker

These findings are source-confirmed static discrepancies. They have not been numerically exercised by a revision-53-compatible GHG testcase, and no qualified historical executable/reference is available. Their historical numerical magnitude therefore remains `REFERENCE_BLOCKED`.

They nevertheless block GHG B3 admission because the scientific process route cannot be considered conservation-qualified while source-pool transfer and observer interfaces are incomplete.

Recommended central follow-up is to register the distinct source discrepancies in the canonical theory/code discrepancy register after regie reconciliation, without repairing them on this branch.

Final ledger status:

`GHG_CONSERVATION_OWNERSHIP_IDENTIFIED_BUT_LEGACY_C_N_TRANSFER_AND_OBSERVER_CHAIN_INCOMPLETE`

Production migration remains `NOT_ADMITTED`.

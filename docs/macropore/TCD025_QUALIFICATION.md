# TCD-025 qualification

Work unit: `ANIMO-MP01`

Target: `TCD-025`

Original PREP06 classification:

`SOURCE_CONFIRMED_MACROPORE_MAIN_LEDGER_STATE_AND_DRA4_INTEGRATION_GAP_TESTBANK_UNEXERCISED`

MP01 disposition:

`SOURCE_AND_B1_PATH_CONFIRMED_MACROPORE_MAIN_LEDGER_CONTROL_VOLUME_GAP_HISTORICAL_MAGNITUDE_OPEN`

Production correction: `NOT_ADMITTED`

## 1. Question

Does revision 53 treat macropore storage and direct drainage as real conserved state/flux in the specialized subsystem while failing to include the same physical control volume consistently in the public/main balance observer?

MP01 answer: yes.

The evidence is now stronger than the PREP06 static finding because the specialized water and solute paths have been causally exercised with nonzero storage, exchange and direct drainage.

## 2. Specialized water control volume

`MAPOHYDRO` owns:

- `SrWaMpOld` and `SrWaMp` as beginning/end water storage;
- surface inflow;
- matrix/macropore exchange;
- full macropore drainage;
- a dedicated profile residual.

In the MP01 direct-drain diagnostic:

- inflow: `0` m;
- outflow: `0.005` m;
- storage change: `-0.005` m;
- specialized residual: `0` m.

This demonstrates that direct drainage and storage change are both causally active terms of the physical macropore water control volume.

## 3. Specialized solute control volume

`MAPOTRANSPORT` owns old/new macropore solute mass as:

`SrWaMpOld * CoMpX`

and:

`SrWaMp * RsCoMpX`.

It also includes matrix exchange and Main Bypass direct drainage in its dedicated balance.

In the MP01 direct-drain solute diagnostic:

- old macropore mass: `0.020`;
- direct-drain export: `0.010`;
- new macropore mass: `0.010`;
- specialized residual: `0`.

In the Internal Catchment exchange diagnostic, nonzero matrix input/output and storage change close to `-3.47e-18`.

These are `SYNTHETIC_DIAGNOSTIC_ONLY` observations, not historical B2 magnitudes.

## 4. Public/main water ledger gap

`Outbal_calc.for` contains provisional macropore water direct-drain code, but it is commented out.

The ordinary water deviation is composed from:

- ordinary top/bottom terms;
- matrix storage change;
- evapotranspiration/runoff terms;
- the configured ordinary drainage systems.

It does not add beginning/end `SrWaMp` storage to the public water storage terms.

It also does not subtract `FlMpOuDrMp` as a separate external direct-drain term.

Therefore the public water observer describes a smaller control volume than the active physical subsystem.

## 5. Public/main dissolved organic matter gap

The `Bdom(Dra4)` block based on `FlMpOuDrMp * AvCoMpDiorMa` is present in source as commented code.

The active DOM deviation sums only the ordinary drainage-system indices. Macropore DOM storage is not supplied as beginning/end public storage state.

Therefore both state coverage and direct-drain coverage are incomplete for DOM.

## 6. Public/main nitrogen gap

Revision 53 does actively accumulate:

- `Banh(Dra4)` from macropore NH4 direct drainage;
- `Bani(Dra4)` from macropore NO3 direct drainage;
- `Bano(Dra4)` from macropore DON direct drainage.

However, the corresponding `Ddev` equations iterate over `Dra(Drn)` for the ordinary drainage systems and do not subtract `Dra4`.

In addition, beginning/end macropore NH4, NO3 and DON storage is not part of the main N storage interface.

Therefore the presence of nonzero `Dra4` reporting slots does not close the main N control volume.

This distinction matters: a term can be printed and still be absent from the residual identity.

## 7. Public/main phosphorus gap

The P drainage blocks account for ordinary matrix drainage of PO4-P and dissolved organic P.

Unlike N, the macropore direct-drain block is absent at the active `Macropores` placeholder in the P section. `Bapp(Dra4)` and `Bapo(Dra4)` therefore are not populated there.

The P deviations again sum ordinary `Dra(Drn)` drainage only, and beginning/end macropore PO4/DOP storage is not supplied as public storage state.

The public P control volume is therefore incomplete when the active macropore P route carries mass.

## 8. Output exposure does not repair the identity

`Outbal_write.for` contains a macropore output record that writes `Dra4` slots for water, DOM, organic N, NH4, NO3, organic P and PO4.

This does not establish conservation because:

- several of those slots are not populated by `Outbal_calc`;
- the active N `Dra4` slots are not included in the N deviation equations;
- macropore beginning/end storage remains absent from the public storage interface.

Therefore `Dra4` is partly a reporting surface without a complete observer identity.

## 9. Activated-path significance

PREP06 could not measure a physical-case magnitude because the testbank had no active macropore case.

MP01 changes what is known in one important way:

- direct drainage is no longer merely a source-declared possibility;
- controlled execution of the frozen specialized kernels produced nonzero direct drainage and exact local closure;
- controlled execution produced nonzero matrix/macropore exchange and exact local closure;
- controlled execution produced nonzero storage change and exact local closure.

Thus the omitted public-ledger terms are demonstrably reachable in the frozen process kernels.

What MP01 still does not establish:

- the public balance residual magnitude in a full naturally parameterized ANIMO macropore simulation;
- historical executable behaviour;
- historical output tolerances;
- whether any external historical workflow post-processed `Dra4` outside the main residual;
- a scientifically admitted corrected public ledger.

## 10. Restart interaction

`Init.for` contains the in-memory accepted-state promotion for macropore water and solutes.

Persistent restart is different. `Output_Init.for` has the macropore `>MPnitr:`, `>MPorgs:` and `>MPphos:` writer block commented out, and the macropore arguments in the `Output_Init` call surface are commented out in `Animo.for`.

Consequently the normal `INITIAL.out` serialization does not preserve active macropore solute concentrations.

Classification:

`SOURCE_CONFIRMED_PERSISTENT_RESTART_INCOMPLETE_FOR_MACROPORE_SOLUTES`

This is not reclassified as TCD-025 itself. It is a separate subsystem qualification blocker because a correct public conservation model must also survive a restart boundary.

## 11. Why MP01 does not implement a fix

A naive repair would add `SrWaMp` storage and `Dra4` terms to the public ledgers.

That direction is structurally plausible but is not yet admitted because several questions remain:

1. which exact public control volume was historically intended for each balance family;
2. how `FlMpOuDrSo` and ordinary drainage must be composed without double counting;
3. how all six solute species should be mapped into the public elemental/organic families;
4. how restart state should be made complete;
5. what historical active reference should constrain corrected behaviour;
6. whether an observer-only correction is sufficient or a broader state/output contract change is required.

MP01 therefore confirms the defect more strongly but does not correct it.

## 12. Evidence ladder

| Evidence statement | Result |
| --- | --- |
| specialized macropore storage exists | `SOURCE_SUPPORTED` |
| specialized direct drainage exists | `SOURCE_SUPPORTED` |
| specialized matrix exchange exists | `SOURCE_SUPPORTED` |
| water storage/exchange/direct-drain paths causally exercised | `B1_CAUSALLY_EXERCISED` |
| generic solute storage/exchange/direct-drain paths causally exercised | `B1_CAUSALLY_EXERCISED` |
| public water/DOM/P direct-drain integration complete | `false` |
| public N direct-drain reporting slots exist | `true` |
| public N residual includes `Dra4` | `false` |
| public main ledgers include macropore beginning/end storage | `false` |
| historical active macropore reference | `B2_HISTORICALLY_REFERENCED = false` |
| corrected ledger admitted | `false` |
| B3 ready | `false` |

## 13. Final TCD-025 judgement

`TCD-025` remains open and is strengthened from a source-only unexercised finding to an activated-path qualified finding:

`SOURCE_AND_B1_PATH_CONFIRMED_MACROPORE_MAIN_LEDGER_CONTROL_VOLUME_GAP_HISTORICAL_MAGNITUDE_OPEN`

The specialized revision-53 macropore kernels can conserve the selected diagnostic water/solute control volumes. The public/main observer does not consistently represent that same physical system.

No production correction is admitted by MP01.

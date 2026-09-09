# Macropore process model

Work unit: `ANIMO-MP01`

Decision scope: source, theory and diagnostic qualification only. Production migration is not admitted.

## 1. Evidence reconciliation

The evidence is coherent once implementation lineage, release support and behavioural coverage are kept separate.

### ANIMO 4.0 documentation

The official ANIMO 4.0 User's Guide already exposes a macropore option and a detailed planned interface. It names two domains, `Main Bypass Flow` and `Internal Catchment`, and lists macropore water storage, precipitation/runoff inflow, matrix exchange, wall-contact fraction, direct drainage and dissolved-solute concentrations. The same guide repeatedly states that the macropore option is not fully operational in ANIMO 4.0.

Classification: `THEORY_SUPPORTED_INHERITED_INTERFACE_WITH_NEGATIVE_RELEASE_STATUS`.

### TH01

TH01 reconstructed the revision-53 source subsystem and concluded:

`THEORY_PARTIALLY_RECONSTRUCTED_ANIMO_SOLUTE_AUTHORITY_MISSING`

The two-domain hydrology and conservation ownership are well supported. The exact revision-53 nutrient-transfer equations remain implementation-derived because no independent ANIMO-specific formulation document has been recovered that completely specifies them.

### TH02

TH02 resolved the chronology as:

`PRE40_IMPLEMENTATION_LINEAGE_WITH_ANIMO40_NONOPERATIONAL_RELEASE_STATUS_AND_LATER_REV53_ACTIVE_SOURCE`

`MAPOTRANSPORT.FOR` identifies itself as part of an ANIMO 3.7.5 version containing macropores and records a 1999 creation history. Public scientific evidence independently confirms FLOCR/ANIMO preferential solute transport in cracked clay in 1999. Later source history shows subsequent integration and rework.

This means macropores are not a simple post-4.0 feature.

### PREP06

PREP06 identified macropore water and solute concentrations as conserved physical state and opened `TCD-025` because the specialized macropore control volumes and the public/main ledger are not equivalent.

### TQ01

TQ01 found:

`natural_macropore_active_cases = 0`

for the supplied nine-case testbank. Therefore source presence and ordinary regression success do not provide positive behavioural qualification of the macropore route.

## 2. Scientific lineage

Independent public evidence supports the existence and scientific purpose of preferential transport through cracks/macropores before ANIMO 4.0:

- Hendriks, R.F.A., Oostindie, K. and Hamminga, P. (1999), *Simulation of bromide tracer and nitrogen transport in a cracked clay soil with the FLOCR/ANIMO model combination*, Journal of Hydrology 215, 94-115, DOI `10.1016/S0022-1694(98)00264-9`.
- Later Alterra documentation states that ANIMO was adapted for preferential transport and rapid drainage through macropores and coupled to SWAPcr/FLOCR, referring to Hendriks (1993) and Hendriks et al. (1999).
- SWAP macropore theory independently supports a two-domain hydrological concept in which connected macropores can bypass the matrix and discontinuous/internal-catchment macropores terminate and force water into the surrounding matrix.

These sources support the hydrological concept. They do not independently define every nutrient equation in revision 53.

## 3. Source-bound subsystem boundary

Primary revision-53 source members:

- `input1.for`
- `mapoinput.for`
- `Input_hydro.for`
- `Hydro_detailed.for`
- `MAPOHYDRO.FOR`
- `MAPOTRANSPORT.FOR`
- `TRANSPORT.FOR`
- `Transca.for`
- `Transgen.for`
- `Init.for`
- `Output_Init.for`
- `Outbal_calc.for`
- `Outbal_write.for`

The macropore subsystem is not merely a reporting route. It owns physical water and solute stores and exchanges mass with the ordinary soil-matrix transport equations.

## 4. Domain model

### Domain 1: Main Bypass Flow

Source and independent hydrological theory are consistent with this domain representing connected preferential flow paths.

Revision-53 source capabilities include:

- direct precipitation input;
- routed runoff input;
- vertical transport through the domain;
- bidirectional matrix exchange by layer;
- water storage;
- direct rapid drainage to the drain system;
- dissolved-solute transport and storage.

Only domain 1 receives the dedicated direct-drainage treatment in `MAPOHYDRO`.

### Domain 2: Internal Catchment

The second domain represents discontinuous or internally terminating preferential paths.

Revision-53 source capabilities include:

- direct precipitation input;
- routed runoff input;
- vertical transport before termination;
- bidirectional matrix exchange by layer;
- water storage;
- dissolved-solute transport and storage.

The hydrology input and `MAPOHYDRO` do not define a separate direct-drain array for domain 2. This is consistent with internal-catchment water being forced back into the matrix rather than discharged directly through a connected bypass path.

The two domains therefore cannot be collapsed into one generic macropore bucket without a new scientific equivalence argument.

## 5. Conserved water state

Canonical revision-53 macropore water state:

| State | Meaning | Unit | Owner |
| --- | --- | --- | --- |
| `SrWaMpOld(1:2)` | accepted/start macropore water storage | m3 m-2 | macropore hydrology |
| `SrWaMp(1:2)` | result/end macropore water storage | m3 m-2 | macropore hydrology |
| `SrWaMpCp(1:2,layer)` | layer-resolved macropore water storage used by coupled calculations | m3 m-2 | hydrology input/macropore subsystem |
| `SrWaMpCpOld(layer)` | accepted combined layer-resolved macropore water storage | m3 m-2 | `Init` continuation state |

`Init.for` promotes `SrWaMp` to `SrWaMpOld` after an accepted timestep. This is physical continuation state, not a diagnostic accumulator.

`Inicalc.for` also modifies matrix saturation bookkeeping to account for static macropore volume, using `VlMpSt` and constructing `MofrsaMp`. Macropore geometry therefore affects more than a separate bypass calculation.

## 6. Water transfers

`MAPOHYDRO` distinguishes the following classes:

| Transfer | Direction | Control-volume role |
| --- | --- | --- |
| `FlMpInPr` | external surface -> macropores | external input |
| `FlMpInRuRv` | routed runoff/reservoir -> macropores | external input to macropore CV |
| `FlMpInRuSo` | routed runoff through soil route -> macropores | external input routed through layer 1 |
| `FlMpInEf` | matrix -> macropores | internal for combined matrix + macropore CV |
| `FlMpOuIf` | macropores -> matrix | internal for combined matrix + macropore CV |
| `FlMpVt` | vertical within macropore domain | internal within macropore CV |
| `FlMpOuDrSo` | macropore drainage routed through soil | internal coupling before ordinary drainage accounting |
| `FlMpOuDrMp` | Main Bypass -> external drain directly | external output |

The specialized profile identity is evaluated by `MAPOHYDRO` from total inflow, total outflow and `SrWaMp - SrWaMpOld`.

## 7. Conserved solute state

Revision 53 carries accepted/result concentration pairs for six dissolved quantities in both macropore domains:

| Quantity | Accepted/start | Result/end | Conserved basis |
| --- | --- | --- | --- |
| labile dissolved organic matter | `CoMpDiorMa` | `RsCoMpDiorMa` | `SrWaMp * concentration` |
| dissolved organic N | `CoMpDiorNi` | `RsCoMpDiorNi` | `SrWaMp * concentration` |
| dissolved organic P | `CoMpDiorPo` | `RsCoMpDiorPo` | `SrWaMp * concentration` |
| NH4-N | `CoMpNh` | `RsCoMpNh` | `SrWaMp * concentration` |
| NO3-N | `CoMpNi` | `RsCoMpNi` | `SrWaMp * concentration` |
| PO4-P | `CoMpPo` | `RsCoMpPo` | `SrWaMp * concentration` |

`Init.for` promotes each result concentration into the corresponding accepted/start concentration. P-specific states are promoted only when the P cycle is active.

## 8. Solute transfer coupling

`MAPOTRANSPORT.FOR` contains a species-generic macropore transport kernel. The ordinary process routines supply species-specific concentration and source arrays.

Source-traced orchestration is:

- DOM via `Transca` -> `Transport` -> `MapoTransport`;
- DON via `Transca` -> `Transport` -> `MapoTransport`;
- DOP via `Transca` -> `Transport` -> `MapoTransport` when P is active;
- NH4-N via `Transport` -> `MapoTransport`;
- NO3-N via `Transport` -> `MapoTransport`;
- PO4-P via `Transgen` -> `MapoTransport`.

The macropore kernel computes:

- surface solute input associated with precipitation and routed runoff;
- matrix-to-macropore input using matrix concentration;
- macropore-to-matrix transfer using the macropore/matrix coupled concentration solution;
- Main Bypass direct-drain export;
- average and result macropore concentrations;
- a source/sink contribution for the ordinary soil-matrix transport equation;
- a dedicated macropore mass-balance check.

This establishes an explicit equal-and-opposite coupling requirement for matrix/macropore exchange.

## 9. Molecular diffusion

The 4.0 guide exposes macropore diffusion coefficients. In revision 53, `mapoinput.for` explicitly comments that molecular diffusion is disabled in this version and its corresponding input block is commented out.

Classification:

`SOURCE_SUPPORTED_DISABLED_FUNCTION_WITH_THEORY_INTENT_BUT_VERSION_SPECIFIC_SCIENTIFIC_STATUS_UNRESOLVED`

MP01 does not reactivate or redesign diffusion.

## 10. Causal B1 diagnostic evidence

Qualification-only probes compiled the frozen `MAPOHYDRO.FOR` and `MAPOTRANSPORT.FOR` kernels with GNU Fortran 14.2 using the established diagnostic precision/runtime policy. Frozen source and testbank bytes were not modified.

Machine-readable evidence: `integration/animo-macropore/ANIMO-MP01_DIAGNOSTIC.json`.

### Water kernel

Four controlled cases exercised storage, matrix exchange, Main Bypass direct drainage and precipitation-to-storage. Reconstructed residuals were:

- storage only: `0` m;
- matrix exchange: `0` m;
- direct drainage: `0` m;
- precipitation storage: `8.67e-19` m.

`MAPOHYDRO` emitted no balance warning in these cases.

### Solute kernel

Five controlled cases exercised storage, Internal Catchment matrix exchange, Main Bypass direct drainage, surface solute input and input followed by matrix transfer. Reconstructed residual magnitudes were at most `3.47e-18` in the diagnostic mass units.

`MAPOTRANSPORT` emitted no balance warning in these cases.

This is strong causal evidence for the specialized local identities. It is not a historical reference and does not establish parameter realism or whole-model numerical tolerances.

## 11. B0-derived whole-case diagnostic design

The positive whole-case descendants are designed from the frozen `CranGrass` case because it uses detailed SWAP hydrology and its SWATRE header has `HLPIMP=1` while its active `GENERAL.INP` has `MacroPoreOption=0`.

Common transform for an execution copy:

1. change `MacroPoreOption` from 0 to 1;
2. change the SWATRE macropore header flag from `HLPIMP=1` to `HLPIMP=2`;
3. insert the exact static, initial and dynamic macropore records required by `mapoinput`;
4. add `>MPfrac:` input to `SOIL.INP`;
5. add `>MPnitr:` and `>MPorgs:` to `INITIAL.INP`, plus `>MPphos:` for a P-active descendant;
6. preserve every unrelated B0 value and record all changed member hashes.

Case-specific deltas then isolate:

- storage only;
- matrix exchange, with domain 2 as the primary exchange target;
- domain-1 direct drainage;
- solute input/transfer;
- unchanged no-macropore negative control.

These full descendants are designed but were not executed as complete ANIMO runs by MP01. The executed causal evidence is the source-kernel evidence described above. This distinction is deliberate.

## 12. Evidence classification

| Question | Status |
| --- | --- |
| source contains active revision-53 macropore state and transfer machinery | `SOURCE_SUPPORTED` |
| two-domain hydrological concept and historical preferential-flow lineage | `THEORY_SUPPORTED` |
| exact revision-53 ANIMO solute equations independently documented | `PARTIAL_ONLY` |
| water storage/exchange/direct-drain local conservation path | `B1_CAUSALLY_EXERCISED` |
| generic solute storage/exchange/direct-drain local conservation path | `B1_CAUSALLY_EXERCISED` |
| each full species orchestration executed in a complete ANIMO macropore case | `OPEN` |
| supplied historical active macropore case | `ABSENT` |
| historical numerical reference | `B2_HISTORICALLY_REFERENCED = false` |
| B3 admission | `false` |

## 13. Process-model judgement

Revision 53 contains a real, stateful two-domain macropore subsystem. Its specialized water and solute kernels are internally conservation-aware and have now been causally exercised under controlled diagnostics. The public/main ledger and restart serialization are separate concerns and are not complete merely because the specialized kernels close.

The source/theory/process model is sufficiently reconstructed to constrain a future migration. It is not sufficient to claim historically referenced operational support or to implement a corrected ANIMO5 subsystem without the remaining qualification gates.

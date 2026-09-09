# ANIMO-MASSQ01 control-volume runtime mapping

Status: `B1_RUNTIME_MAPPING_QUALIFIED_FOR_OBSERVER_USE_WITH_EXPLICIT_OPEN_BOUNDARIES`.

This mapping instantiates the PREP06 conserved-state inventory and ARCH03 control-volume rules on the revision-53 B1 diagnostic execution surface. It is an observer mapping only. It does not make legacy balance arrays physical state owners and it does not admit canonical MASS.

## 1. Residual convention

MASSQ01 records the balance-form residual

`begin storage + external input + source term - external output - end storage`.

This is the sign-reversed form of the ARCH03 candidate residual `S_end - S_begin - I_external + O_external`. Both have the same zero condition. MASSQ01 keeps the balance-form sign because it makes direct comparison with the established PREP01/TCD residual archaeology easier. No numerical tolerance is attached to either convention.

## 2. Runtime boundary

Beginning storage is snapshotted after `Init` has promoted the previous result state and after any initialization action that changes the accepted beginning representation, but before hydrology and process execution for the interval. This boundary is mandatory.

An early observer prototype reconstructed beginning storage later in the interval from nominal start-side arrays. That is invalid because some of those arrays or their composition coordinates can change during the interval. The corrected observer therefore persists a separate `massq01_start.dat` snapshot and combines it with transfer and end-state observations from `massq01_step.dat`.

The postprocessor deliberately ignores the instrumentation-only recomputed-begin and recomputed-residual columns in the end-of-step sidecar. `tools/analyze_massledger_b1_sidecars.py` fails closed when a matching persisted start snapshot is absent.

## 3. Observer record contract

The intended normalized observer record is:

| field | meaning |
| --- | --- |
| `interval` | accepted B1 diagnostic interval identity, currently source `Tito` plus `St` |
| `control_volume` | selected owner set |
| `element_or_quantity` | water, N, P, organic-matter mass, or later explicitly admitted C/GHG quantity |
| `store` | source-bound owner state projected into storage |
| `transfer_identity` | physical transfer or source/sink identity |
| `source_owner` | owner or external boundary from which quantity originates |
| `destination_owner` | owner or external boundary receiving quantity |
| `sign` | derived for the selected control volume, not hard-coded as a permanent event property |
| `quantity` | unrounded observed amount |
| `units` | explicit quantity unit |
| `evidence_source` | source variable/routine and evidence class |

The current B1 execution-copy instrumentation still aggregates several transfer variables by interval rather than emitting the full future typed event journal. That is sufficient to qualify observer non-interference and reproduce selected known TCDs, but it is the main reason discrete management/crop event clusters remain open.

## 4. Control volumes

### `CV-HYDRO-PROFILE`

Included stores:

- matrix water `Mofro -> Mofrt` integrated with layer thickness `He`;
- detailed ponding `Pn -> Pnt`;
- snow `Snla -> Snt` where active;
- interception `Sic -> Sict` where active;
- aggregated surface-water representation `Wale -> Walet` only for the corresponding hydrology route;
- macropore water only in the separate synthetic combined view below.

External inputs include precipitation/rain/snow, irrigation, runon/inundation and upward lower-boundary/drainage inflow where the source variables indicate an inward flux. External outputs include evaporation terms, runoff, downward lower-boundary loss and drainage outflow.

Internal layer-to-layer water transfer cancels. TCD-018 is a `LEGACY_REPORTING_ONLY_DIFFERENCE` for this view because the public `Bawa` interface omits interception storage even though the physical hydrology state contains it.

### `CV-SOIL-N`

Included stores:

- aqueous NH4 `Conh -> Rsconh`;
- adsorbed NH4 `Cxnh -> Rscxnh`;
- nitrate `Coni -> Rsconi`;
- labile DON `Codiorni -> Rscodiorni`, including source-defined sorbed contribution;
- stable DON `CoStdiorni -> RsCoStdiorni`, where dynamically supported;
- N carried by fresh organic matter, original humus, exudate-derived humus and exudate material through their explicit N composition coordinates;
- source-defined surface/top dissolved reservoirs.

External inputs include atmospheric deposition, precipitation solute, irrigation/runon/inundation solute, material additions and crop-residue returns that cross from an external crop owner into soil. External outputs include runoff/leaching/drainage, volatilization, soil-to-crop uptake and denitrification when GHG state is not explicitly inside the selected control volume.

Nitrification and mineralization/immobilization are internal N transfers in this whole-soil view. With GHG active, N2O requires a separate explicit owner and the whole N view is not yet qualified.

TCD-015 and TCD-016 are constraint/state-model nonclosures, not balancing fluxes to be invented by the observer.

### `CV-SOIL-CROP-N`

Candidate nested view only. It adds actual crop N ownership, so soil-to-crop uptake becomes internal. Harvest/grazing export remains external unless a return transfer re-enters soil.

Revision-53 exposes `Amplni_act/Rsamplni_act`, but a sensitivity probe showed that simply replacing the soil uptake transfer by the end-minus-begin crop-state delta is not semantically equivalent for all intervals. Crop routines reset and partition crop state around growth/harvest logic. Therefore this nested view is mapped but not runtime-qualified by MASSQ01.

### `CV-SOIL-P`

Included stores:

- aqueous PO4 `Copo -> Rscopo`;
- fast sorption sites `Amcxfa -> Rsamcxfa`;
- slow sorption sites `Amcxsl -> Rsamcxsl`;
- precipitated P `Ampopr -> Rsampopr`;
- labile/stable DOP;
- P in fresh organic matter, humus, exudate-derived humus and exudate material through their explicit P composition coordinates;
- source-defined surface/top P reservoirs.

External inputs/outputs mirror the N boundary classes where P exists: wet deposition/precipitation, irrigation/runon/inundation, material addition, crop-residue return, runoff/leaching/drainage and crop uptake.

Fast/slow sorption and precipitation/dissolution are internal phase transfers. TCD-014 is a separate initialization projection seam. TCD-019 is numerical constitutive nonclosure. TCD-024 is a slow-site indexing defect. TCD-017 is reporting-only redistribution bookkeeping and is not a physical P source or sink.

### `CV-SOIL-CROP-P`

Candidate nested view only. It adds actual crop P state. As for crop N, direct state-delta substitution has not been qualified as a complete interval transfer contract, so MASSQ01 does not claim closure for this view.

### `CV-SOIL-OM`

Included storage is explicit organic-matter mass:

- fresh solid organic pools `Os -> Rsos`;
- original humus `Huos -> Rshuos`;
- exudate-derived humus `Huex -> Rshuex`;
- exudate material `Ex -> Rsex`;
- labile/stable dissolved organic-matter storage using the source-defined aqueous plus sorbed projection;
- top dissolved organic-matter reservoir where represented.

External inputs include organic material additions and crop-residue returns. External outputs include dissolved-organic transport across the selected profile boundary and source-explicit mineralization/dissipation products when they leave the OM quantity contract.

This view is **not elemental carbon**. PREP06 and ARCH03 explicitly keep `organic_matter_mass`, crop dry matter and elemental/gaseous carbon separate until a scientific conversion/reaction contract is admitted. MASSQ01 therefore labels runtime sidecar code `O` as `organic_matter_mass`, not `C`.

### `CV-SURFACE-RESERVOIRS`

Surface-relevant state is not collapsed into one undocumented bucket. Hydrological surface state includes ponding/surface water, snow and interception according to route. Chemical layer 0 and source-defined top dissolved reservoirs remain separate from soil layers because dry-down, runoff and initialization semantics differ there.

TCD-016 demonstrates why the layer-0 liquid state cannot simply disappear when water vanishes. TCD-018 demonstrates why interception must remain an explicit water store.

### `CV-MATRIX-MACROPORE-WATER`

Synthetic B1 only, inherited from MP02.

Included stores add `SrWaMpOld -> SrWaMp` to the matrix/hydrology stores. Matrix-to-macropore exchange is internal in this combined view. Direct macropore drainage is external.

MP02 demonstrated complete active ANIMO orchestration but remains B0-derived synthetic B1. The public `Bawa` output can remain unchanged even when macropore storage and a designed 0.02 mm exchange/direct-drain event are present. This is TCD-025 evidence, not a reason to repair the public ledger inside MASSQ01.

### `CV-MATRIX-MACROPORE-OM/N/P`

Synthetic B1 only. Macropore dissolved storage is source-explicit as `SrWaMpOld * CoMp` at interval start and `SrWaMp * RsCoMp` at interval end. Matrix/macropore exchange is internal; direct drainage is external.

The main revision-53 `Outbal_calc` interface lacks the complete `SrWaMp/RsCoMp` storage coordinates and integrates `Dra4` inconsistently. MASSQ01 therefore treats MP02 as synthetic positive path evidence and does not infer a natural-case macropore closure result.

### `CV-GHG-C` and `CV-GHG-N`

Source ownership exists for CH4 and N2O state, but runtime closure is incomplete:

- none of the eight compatible natural B1 cases activates GHG;
- supplied `GHGMais` is not revision-53 parser-compatible;
- GHG01 has source-confirmed hidden task/restart state and incomplete full-model C/N ledger coupling.

MASSQ01 records this as `COVERAGE_INCOMPLETE`, not as a closure failure and not as an admission.

## 5. Classification discipline

`OBSERVER_CLOSURE_PASS` is used only when the reconstructed residual is exactly zero under the recorded arithmetic. It is not expanded by an epsilon.

`EXPECTED_KNOWN_TCD` requires an already governed TCD association supported by independent source/runtime evidence.

`LEGACY_REPORTING_ONLY_DIFFERENCE` means the physical observer and legacy report intentionally expose different semantics because the legacy report omits/misaccumulates a known term while physical state ownership is intact.

`UNEXPLAINED_RESIDUAL` remains a local MASSQ01 finding. The current discrete management/crop event clusters are in this class until their transfer projection is reconciled. MASSQ01 has no authority to assign them new canonical TCD numbers.

## 6. Qualification boundary

The runtime mapping is sufficient for B1 observer qualification work, known-TCD reproduction and non-interference testing. It is not yet a complete canonical transfer journal. In particular, crop/external-owner event projection, elemental-carbon conversion, GHG whole-system coupling and natural macropore coverage remain open.

Canonical MASS, B3 and production migration remain `NOT_ADMITTED`.

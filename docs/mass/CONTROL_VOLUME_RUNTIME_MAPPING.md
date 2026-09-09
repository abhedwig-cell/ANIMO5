# ANIMO-MASSQ01 control-volume runtime mapping

Status: `B1_RUNTIME_MAPPING_QUALIFIED_FOR_OBSERVER_USE_WITH_EXPLICIT_OPEN_BOUNDARIES`.

This mapping instantiates the PREP06 conserved-state inventory and ARCH03 control-volume rules on the revision-53 B1 diagnostic execution surface. It is an observer mapping only. It does not make legacy balance arrays physical state owners and it does not admit canonical MASS.

## 1. Residual convention

MASSQ01 records the balance-form residual

`begin storage + external input + source term - external output - end storage`.

This is the sign-reversed form of the ARCH03 candidate residual `S_end - S_begin - I_external + O_external`. Both have the same zero condition. MASSQ01 keeps the balance-form sign because it makes direct comparison with the established PREP01/TCD residual archaeology easier. No numerical tolerance is attached to either convention.

## 2. Runtime boundary is quantity-specific

The B1 diagnostic does not expose one universal program point at which every accepted-state coordinate can safely be reread as beginning storage. MASSQ01 therefore uses two read-only start snapshots.

For `CV-HYDRO-PROFILE`, `massq01_start.dat` is captured after `Init` and before interval hydrology/process mutation. Matrix water uses layers `1:Nl`; ponding, snow and interception are explicit surface stores.

For chemical quantities N, P and organic-matter mass, `massq01_chem_start.dat` is captured after hydrology and crop preparation and immediately before `Addit`. This is the process-start state used by the chemical projection.

The split is required by source and runtime evidence. On later timesteps `Init.for` promotes `Mofro(Ln)=Mofrt(Ln)` only for `Ln=1,Nl`, while NH4, NO3 and dissolved-organic concentrations are promoted for `Ln=0,Nl`. A chemical storage reconstruction immediately after `Init` can therefore combine new layer-0 concentrations with stale `Mofro(0)`. At wet/dry surface transitions this creates a representational mass jump that is not a physical transfer.

A dedicated diagnostic localized the earlier large apparent residual clusters exactly to this mismatch. Examples:

- GrassPeat TITO 1704: apparent N jump `-8.276164955692366 kg/ha`, predicted from the layer-0 moisture-coordinate mismatch `-8.27616495572782 kg/ha`;
- STONE TITO 1530: apparent N jump `-4.90885883878218 kg/ha`, predicted `-4.908858838774846 kg/ha`;
- Zuiderzeeland TITO 473: apparent N jump `-2.3146104119950905 kg/ha`, predicted `-2.314610412007279 kg/ha`.

Equivalent P and organic-matter jumps reconcile to the same layer-0 coordinate mismatch. These rejected diagnostic residuals are not new physical discrepancies and receive no canonical TCD identifier.

The postprocessor deliberately ignores the instrumentation-only recomputed-begin and recomputed-residual columns in `massq01_step.dat`. It fails closed when a matching hydrological or chemical start snapshot is absent or feature/timestep flags disagree.

## 3. Observer record contract

The intended normalized observer record is:

| field | meaning |
| --- | --- |
| `interval` | accepted B1 diagnostic interval identity, currently source `Tito` plus `St` |
| `control_volume` | selected owner set |
| `element_or_quantity` | water, N, P, organic-matter mass, or explicitly bounded organic C |
| `store` | source-bound owner state projected into storage |
| `transfer_identity` | physical transfer or source/sink identity |
| `source_owner` | owner or external boundary from which quantity originates |
| `destination_owner` | owner or external boundary receiving quantity |
| `sign` | derived for the selected control volume, not hard-coded as a permanent event property |
| `quantity` | unrounded observed amount |
| `units` | explicit quantity unit |
| `evidence_source` | source variable/routine and evidence class |

The B1 execution-copy instrumentation aggregates several transfer variables by interval rather than emitting the future typed event journal. That is sufficient for observer qualification, non-interference testing, known-TCD reproduction and local residual detection. It is not a canonical production transfer bus.

## 4. Control volumes

### `CV-HYDRO-PROFILE`

Included stores:

- matrix water `Mofro -> Mofrt` integrated over layers `1:Nl` with `He`;
- detailed ponding `Pn -> Pnt`;
- snow `Snla -> Snt` where active;
- interception `Sic -> Sict` where active;
- aggregated surface-water representation `Wale -> Walet` for the corresponding hydrology route;
- macropore water only in the separate synthetic combined view below.

External inputs include precipitation/rain/snow, irrigation, runon/inundation and inward lower-boundary/drainage fluxes. External outputs include evaporation terms, runoff, downward lower-boundary loss and drainage outflow. Internal layer-to-layer water transfer cancels.

TCD-018 is a `LEGACY_REPORTING_ONLY_DIFFERENCE` because the public `Bawa` interface omits interception storage even though the physical hydrology state contains it.

### `CV-SOIL-N`

Included stores are aqueous and adsorbed NH4, nitrate, labile and stable DON, N in fresh organic matter/humus/exudate stores, and source-defined surface/top dissolved reservoirs.

External inputs include deposition, precipitation solute, irrigation/runon/inundation solute, material additions and crop-residue return from an external crop owner. External outputs include runoff/leaching/drainage, NH4 volatilization, soil-to-crop uptake and denitrification when GHG state is outside the selected control volume.

Nitrification and mineralization/immobilization are internal N transfers in this whole-soil view. TCD-015 and TCD-016 are constraint/state-model nonclosures, not balancing fluxes to be invented by the observer. With GHG active, N2O requires an explicit additional owner and whole-system N closure remains outside this workunit's qualified runtime coverage.

### `CV-SOIL-CROP-N`

Candidate nested view only. Adding actual crop N ownership changes soil-to-crop uptake from external to internal. Harvest/grazing removal remains external unless a return event re-enters soil.

Revision-53 exposes `Amplni_act/Rsamplni_act`, but a sensitivity probe showed that crop-state end-minus-begin is not a universal replacement for the interval uptake transfer because crop routines reset and partition crop state around growth and harvest logic. The boundary semantics are mapped; a full nested crop-state closure is not claimed.

### `CV-SOIL-P`

Included stores are aqueous PO4, fast and slow sorption sites, precipitated P, labile/stable DOP, organic-pool P and source-defined surface/top P reservoirs.

External boundary classes mirror N where P exists: precipitation/deposition, irrigation/runon/inundation, material addition, crop-residue return, runoff/leaching/drainage and crop uptake. Sorption/desorption and precipitation/dissolution are internal phase transfers.

TCD-014 is an initialization projection seam, TCD-019 a numerical constitutive nonclosure, TCD-024 a slow-site indexing defect, and TCD-017 a reporting-only redistribution omission. They remain separate.

### `CV-SOIL-CROP-P`

Candidate nested view only. It adds actual crop P state. As for N, direct crop-state delta substitution is not admitted as the complete interval transfer contract, so MASSQ01 does not claim nested crop P closure.

### `CV-SOIL-OM`

Included storage is explicit organic-matter mass: fresh solid organic pools, original and exudate-derived humus, exudate material, labile/stable dissolved organic matter including source-defined sorbed contributions, and the top dissolved reservoir where represented.

External inputs include organic material additions and crop-residue returns. External outputs include dissolved-organic boundary transport and source-explicit mineralization/dissipation leaving the OM quantity contract.

### `CV-SOIL-ORGANIC-C`

This is a bounded elemental-carbon projection from `CV-SOIL-OM`, not a whole-model carbon ledger.

Revision-53 reads `Cfracom` from `>orgcom:` as the organic C content and uses that coefficient in organic-matter/carbon stoichiometry and output conversion. MASSQ01 therefore derives every store and transfer in this view as:

`organic C = Cfracom × organic-matter quantity`.

All eight compatible natural B1 cases use `Cfracom = 0.58`; the analyzer reads the value from each active material input and fails closed if it cannot be resolved or lies outside `(0,1]`.

This projection does **not** silently equate crop dry matter with carbon and does not include CH4-C. Consequently it satisfies the B1 soil-organic-C observer scope only. Whole-system C closure remains unqualified.

### `CV-SURFACE-RESERVOIRS`

Surface-relevant state is not collapsed into one undocumented bucket. Hydrological surface state includes ponding/surface water, snow and interception according to route. Chemical layer 0 and source-defined top dissolved reservoirs remain separate from soil layers because dry-down, runoff and initialization semantics differ there.

TCD-016 demonstrates why layer-0 dissolved mass cannot simply disappear when liquid storage vanishes. The transaction-boundary diagnostic above also demonstrates why water and solute coordinates at layer 0 must be observed at a compatible process boundary.

### `CV-MATRIX-MACROPORE-WATER`

Synthetic B1 only, inherited from MP02. Included storage adds `SrWaMpOld -> SrWaMp` to the matrix/hydrology stores. Matrix-to-macropore exchange is internal; direct macropore drainage is external.

MP02 demonstrated complete active ANIMO orchestration but remains B0-derived synthetic B1. The public `Bawa` output can remain unchanged even when macropore storage and a designed `0.02 mm` exchange/direct-drain event are present. This is TCD-025 evidence, not a reason to repair the public ledger inside MASSQ01.

### `CV-MATRIX-MACROPORE-OM/N/P`

Synthetic B1 only. Macropore dissolved storage is source-explicit as `SrWaMpOld * CoMp` at interval start and `SrWaMp * RsCoMp` at interval end. Matrix/macropore exchange is internal; direct drainage is external.

The main revision-53 `Outbal_calc` interface lacks the complete `SrWaMp/RsCoMp` storage coordinates and integrates `Dra4` inconsistently. MASSQ01 therefore treats MP02 as synthetic positive path evidence and does not infer a natural-case macropore closure result.

### `CV-GHG-C` and `CV-GHG-N`

Source ownership exists for CH4 and N2O state, but runtime closure is incomplete:

- none of the eight compatible natural B1 cases activates GHG;
- supplied `GHGMais` is not revision-53 parser-compatible;
- GHG01 has source-confirmed hidden task/restart state and incomplete full-model C/N ledger coupling.

MASSQ01 records this as coverage incomplete, not as a closure failure and not as an admission.

## 5. Classification discipline

`OBSERVER_CLOSURE_PASS` is used only when the reconstructed residual is exactly zero under the recorded arithmetic. It is not expanded by an epsilon.

`EXPECTED_KNOWN_TCD` requires an already governed TCD association supported by independent source/runtime evidence.

`LEGACY_REPORTING_ONLY_DIFFERENCE` means the physical observer and legacy report expose different semantics because the report omits or misaccumulates a known term while physical state ownership is intact.

`UNEXPLAINED_RESIDUAL` remains a local MASSQ01 finding. A residual that is reproduced by an independently evaluated legacy whole-profile equation is not treated as an observer-mapping failure merely because its canonical defect cause has not yet been isolated. MASSQ01 does not assign a new canonical TCD number.

Rejected observer-boundary artefacts are documented as tooling archaeology, not entered into the physical residual register.

## 6. Qualification boundary

This mapping is sufficient for B1 observer qualification, known-TCD reproduction, local residual detection and non-interference testing. It is not a complete canonical production event journal. Full soil+crop nested closure, whole-system elemental carbon including crop and GHG state, GHG runtime closure and natural active-macropore coverage remain open.

Canonical MASS, B3 and production migration remain `NOT_ADMITTED`.

# ANIMO-PREP06 transfer-ledger model

Status: `SOURCE_BOUND_PREPARATORY_EVIDENCE`.

The machine-readable ledger contains 124 transfer records in `integration/animo-prep/PREP06_TRANSFER_LEDGER.csv`. It is a source-bound inventory, not a corrected implementation.

## Ledger convention

Each transfer has a source and a sink. `EXT:*` nodes denote a boundary outside the selected physical control volume. Internal transfers must appear once as a source loss and sink gain in a canonical ledger. A reporting accumulator may observe that event but must not become a second state owner.

The `external_internal` field deliberately depends on control-volume scope. Crop uptake is external for a soil-only balance but internal when soil and vegetation are combined. The same applies to macropore-to-matrix exchange: it is internal for a combined matrix+macropore profile but external to either sub-control-volume alone.

Sign convention is expressed in physical transfer direction rather than copied mechanically from every legacy array. This avoids making legacy reporting sign choices part of the future state contract.

## Transfer classes covered

The register covers vertical transport, lateral drainage/infiltration, top and bottom boundaries, runoff/runon, irrigation, wet/dry deposition, fertilization/manure, crop uptake, harvest, grazing, root death, mineralization, immobilization, nitrification, denitrification, sorption/desorption, precipitation/dissolution, DOM production/decay, ploughing/redistribution, phase transfer, macropore exchange/direct drainage and reporting-only balancing terms.

### Water

Water is supplied by the hydrological model rather than solved as ANIMO nutrient physics. Revision-53 nevertheless carries water stores and a water ledger. For detailed hydrology the physically complete profile identity includes changes in matrix, snow, ponding and interception storage. TCD-018 demonstrates that the imported hydrology can close while the public ANIMO water ledger omits interception storage.

### Solute transport

`TRANSPORT.FOR` and `Transsub.for` implement the generic transport seam for labile DOM/DON/DOP, NH4 and NO3. `Transgen.for`/`Transorp.for` handle mineral P with aqueous, sorbed and precipitated storage. Adjacent vertical interface fluxes are internal and cancel when both layers are inside a balance profile. Drainage, infiltration, runoff, runon, irrigation and bottom exchange are external when they cross the selected profile boundary.

### Management and surface reservoir

`Addit.for` owns material additions, dry deposition, crop/root residues, volatilization and redistribution. When `WYAD=0`, mineral and dissolved parts can reside in the virtual top reservoir, while organic solid parts are assigned to soil material pools. Ploughing is an internal redistribution if the balance control volume contains both the source top/soil storage and destination layers. TCD-017 is precisely a reporting asymmetry of this internal transfer for organic P.

### Crop

Realized N and P uptake is deducted from soil solute state by the transport/source terms and added to plant state by `Upintg_*`. Harvest and grazing reduce crop state; only the modeled loss/residue fractions return to soil organic pools. The remainder is an external removal for a combined soil+plant system. This distinction is necessary for an ANIMO5 whole-system conservation ledger.

### Organic transformations and mineralization

`Resp_miner.for` owns a network among fresh OM, exudates, labile/stable DOM and humus, with species-specific N/P release or immobilization into mineral pools. Detailed `Transfom`, `Transfon` and `Transfop` terms are transfer evidence, while `Bafom/Bafon/Bafop` are report accumulators. TCD-023 shows why transfer events must remain species typed: two P partition terms use `Transfon17` in one stable-DOM branch.

### Mineral N

Mineralization/immobilization connects organic N and NH4. Nitrification connects NH4 to NO3 and, when GHG is active, an N2O partition. Denitrification removes NO3 into gaseous N products, with N2O represented as explicit gas state under the GHG option. PREP06 records this topology but does not claim the complete revision-53 GHG theory contract has been independently reconciled.

### Mineral P phase transfer

Aqueous PO4, fast sorption, slow sorption and precipitated P form one mineral-P control volume. Sorption/desorption and precipitation/dissolution are internal phase transfers. TCD-014, TCD-019 and TCD-024 show three different failure modes that must not be conflated: inconsistent initialization projection, numerical finite-change nonclosure and wrong site-parameter indexing.

### Macropores

`MAPOHYDRO.FOR` and `MAPOTRANSPORT.FOR` define their own storage-aware closure. Matrix/macropore exchange is internal to a combined profile. Direct macropore drainage is external. TCD-025 exists because the main public balance interface cannot represent this complete control volume and the supplied testbank never activates the route.

## TCD integration matrix

| TCD | Ledger location | Type of failure |
| --- | --- | --- |
| TCD-014 | P initialization and phase partition | beginning-state consistency / ledger seam |
| TCD-015 | NO3 local transport | algebraic local nonclosure |
| TCD-016 | NH4 layer-0 dry-down | missing continuation state / silent mass removal |
| TCD-017 | organic-P redistribution | reporting omission of one side of internal transfer |
| TCD-018 | water storage | public balance interface omits interception state |
| TCD-019 | PO4 sorption | numerical conservation-policy defect |
| TCD-023 | stable-DOM P transformation | cross-species transfer expression |
| TCD-024 | slow P sorption | state-site versus parameter-index mismatch |
| TCD-025 | macropore water/solute | public ledger control-volume incompleteness |
| TCD-026 | fresh-OM beginning storage | initial storage omission |
| TCD-027 | detailed organic-P report | reporting accumulator cross-slot defect |

No additional TCD is opened by this extension. The new registers organize already source-supported evidence and expose qualification boundaries; they do not convert untested suspicions into defects.

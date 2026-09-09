# ANIMO-ARCH03 control-volume model

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

The same physical state and transfer journal must support different conservation views without duplicating process bookkeeping.

## Endpoint projection rule

For a typed event and selected control volume:

- source outside, sink inside: external input;
- source inside, sink outside: external output;
- source inside, sink inside: internal transfer;
- source outside, sink outside: ignored by that view.

This classification is derived from compartment ownership and feature topology. Process routines do not hard-code separate balance meanings for each view.

## Core views

### Hydrological profile

`CV-HYDRO-PROFILE` contains the hydrological storage coordinates required for the ANIMO transport control volume. Matrix water, snow, ponding and interception belong to the complete detailed profile. If macropores are admitted, macropore water also belongs to the combined water control volume and direct macropore drainage becomes an external output.

TCD-018 and TCD-025 prevent treating the legacy public water balance as an already complete canonical implementation.

### Soil nitrogen

`CV-SOIL-N` includes soil/surface organic N, dissolved organic N, NH4 and NO3. Crop uptake crosses the control-volume boundary and is therefore an output.

`CV-SOIL-CROP-N` adds actual crop N state. The same uptake event is then internal. Harvest/grazing removal remains external unless another explicit return event brings material back.

This is one reason internal/external cannot be stored as a permanent property of an event.

### Soil phosphorus

`CV-SOIL-P` includes organic/dissolved P and the full site-resolved mineral-P system. Fast sorption, slow sorption and precipitation/dissolution are internal phase transfers. Redistribution is internal when source and destination stores are both included.

`CV-SOIL-CROP-P` additionally includes actual crop P state.

TCD-014, TCD-017, TCD-019, TCD-023, TCD-024 and TCD-029 concern different seams in this domain and remain separate evidence items.

### Organic-matter mass

`CV-SOIL-OM` closes explicit organic-matter mass stores and their admitted external additions/removals. It does not infer elemental carbon from OM or crop dry matter.

TCD-026 and TCD-028 motivate deriving beginning/end storage and reporting from the same canonical owner/event model.

### Crop dry matter

`CV-CROP-DM` is kept separate from elemental carbon. Root/shoot dry matter may participate in residue/harvest/grazing events, but any conversion into soil OM or elemental C requires an explicit conversion contract rather than name-based equivalence.

### Matrix plus macropore

`CV-MATRIX-MACROPORE-N` and `CV-MATRIX-MACROPORE-P` exist as candidate views only. They show how matrix/macropore exchange would cancel internally while direct macropore drainage remains external.

They are feature-blocked because the supplied testbank does not exercise the active macropore route and TCD-025 remains unresolved at the public-ledger level.

### GHG views

`CV-GHG-C` and `CV-GHG-N` observe explicit CH4-C and N2O-N system storage. They do not claim complete whole-system C/N closure because reaction coupling to the organic/mineral domains remains theory-ledger blocked.

## Nested-view consistency

Where one control volume is a strict extension of another, a transfer that moves from the smaller volume into the newly included compartment must change classification from boundary flux to internal transfer without changing event amount.

Examples:

- crop uptake: external in soil-only, internal in soil+crop;
- matrix-to-macropore exchange: external to matrix-only, internal in matrix+macropore.

A future implementation test should verify this projection property from one immutable event journal.

## Unsupported/dormant state

Parser-visible but dynamically dormant stable surface DOM/DON/DOP is not silently included as supported storage. It can enter a future control volume only after its timestep evolution and restart semantics are admitted.

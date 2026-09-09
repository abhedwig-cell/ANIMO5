# ANIMO-ARCH04 state allocation model

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

The machine-readable source is `integration/animo-architecture/ARCH04_STATE_ALLOCATION.csv`. It gives every one of the 53 ARCH01 state/non-state families an explicit allocation policy.

## Allocation classes

ARCH04 distinguishes:

- `MODEL_PERSISTENT`: ANIMO-owned continuation-critical state for the candidate core;
- `CONDITIONAL_PERSISTENT`: ANIMO-owned continuation state only when an admitted option is active;
- `CONDITIONAL_OWNER_PERSISTENT`: state allocated only when ANIMO is the configured owner;
- `EXTERNAL_COORDINATE`: continuation-critical exchange coordinate owned by another component;
- `DERIVED_VIEW`: recomputed from restored/accepted state or exchange data;
- `STEP_LOCAL_SCRATCH`: trial-local workspace, never checkpoint state;
- `DIAGNOSTIC_OBSERVER`: observer/continuation data separate from physical state;
- `UNSUPPORTED_DORMANT`: no supported runtime allocation.

These categories intentionally mirror the ownership/restart separation established in ARCH01 and ARCH02.

## Core persistence

Core soil chemistry keeps the physical OM, labile DOM, mineral-N and base mineral-P state needed for continuation. Their shapes depend on the admitted geometry and, where applicable, organic-fraction dimensions.

Stable soil DOM is conditional because its scientific lineage remains incomplete. This is not a claim that the legacy source never carries the arrays. It is a candidate ANIMO5 feature boundary that keeps TCD-021/TCD-023 visible rather than silently baking the option into all configurations.

## Variable P-site shape

Fast and slow sorption state is stored site-resolved. The candidate layout therefore uses:

- `layer_count × fast_p_site_count` for fast sites;
- `layer_count × slow_p_site_count` for slow sites.

Derived totals are not checkpointed. Changing either site count changes physical layout identity and invalidates direct checkpoint compatibility. TCD-029 and TCD-024 remain qualification constraints on the underlying science/legacy behaviour.

## Crop ownership

When `crop_mode=animo`, shoot/root dry matter and actual plant N/P are ANIMO-owned persistent state.

When `crop_mode=external`, those states are not duplicated. ANIMO holds only the admitted exchange representation required to evaluate soil-crop transfers. Potential N/P demand remains a derived/exchange view rather than physical crop storage.

## GHG and macropore allocation

GHG system states and macropore water/solute states have explicit conditional allocation policies, but allocation is permitted only after feature admission. Merely setting a configuration switch cannot override TCD-008 or TCD-025.

Derived gas-water phase concentrations are reconstructed from the admitted system state rather than checkpointed separately.

## Surface state

The active surface reservoir allocates NH4, NO3, labile DOM/DON/DOP and PO4 state as one optional state group. Stable surface DOM/DON/DOP is deliberately excluded because PREP06 found it parser-representable but dynamically dormant in revision 53.

## Scratch and diagnostics

Process scratch is worker/trial-local and reinitialized for each trial. It is not part of accepted state and cannot leak across rollback.

Diagnostic allocation is controlled independently. Turning detailed diagnostics on may allocate more observer data, but it must not alter the physical layout identifier or process state ownership. Mid-report-period diagnostic continuation, if requested, uses the separate observer checkpoint semantics from ARCH02.

## No production layout claim

ARCH04 names logical dimensions and allocation classes. It does not prescribe Fortran derived types, C structs, arrays-of-structures versus structures-of-arrays, alignment, precision, packing, allocator strategy or GPU layout. Those are later implementation choices constrained by the candidate semantics here.

# ANIMO5 local discrepancy identifier reconciliation

Work unit: `ANIMO-RG02`

This document resolves identifier collisions only. It does not reinterpret, merge, strengthen or weaken scientific findings.

The qualified B3Q01 discrepancy register ends at `TCD-027`. Its blob is `224acc350fde69d3c4aebed8628c0f945e0b3367`. Any `TCD-028` or higher label created on preparatory branches after that snapshot is therefore a branch-local label unless the B3 governance line explicitly reserves or appends it.

The only later central reservation observed by RG02 is `TCD-028` for the stable-DOM plough accumulator event-reset finding on `work/animo-b3-tcd028-stable-dom-intake`. That reservation is still `RESERVED_PENDING_CANONICAL_REGISTER_APPEND_NOT_ADMITTED`.

## Reconciliation keys

RG02 introduces stable local reconciliation keys so evidence can be converged without inventing canonical TCD numbers:

| RG02 key | Branch-local labels observed | Finding identity retained from source evidence | Canonical state |
| --- | --- | --- | --- |
| `RG02-LCL-EXHUMUS-PLOUGH-LEDGER` | `TCD-028` on PREP07/PREP08/PREP09 transfer lineage | exudate-humus ploughing redistribution ledger duplicate/double-count | unallocated |
| `RG02-LCL-MULTISITE-FAST-P-MANAGEMENT` | `TCD-029` on PREP07/PREP08/PREP09 transfer lineage | multi-site fast P management integration / mass-conservation gap | unallocated |
| `RG02-LCL-EXHUMUS-ELEMENT-FRACTION-SEQUENCING` | `TCD-030` on PREP08 transfer and PREP09 element-transfer lineage | exudate-humus N/P fraction sequencing during ploughing | unallocated |
| `RG02-LCL-AERATION-OPTION2-ALIAS` | `TCD-030` on PREP09 option-contract lineage | aeration option 2 semantic alias to option 0 | unallocated |
| `RG02-LCL-SLOW-SORPTION-TILLAGE-POLICY` | `TCD-031` on PREP09 element-transfer lineage | slow non-equilibrium P sorption tillage policy gap | unallocated |
| `RG02-LCL-MACROPORE-SOLUTE-RESTART-WRITER` | `TCD-032` on the reused PREP10 restart lineage | persistent macropore solute restart writer omission | unallocated |
| `RG02-LCL-PLANT-ACTUAL-UPTAKE-RESTART-DIRECTION` | `TCD-033` on the reused PREP10 restart lineage | actual plant uptake restart initialization-direction defect | unallocated |
| `RG02-LCL-PLANT-POTENTIAL-UPTAKE-RESTART-STATE` | `TCD-034` on the reused PREP10 restart lineage | potential plant uptake restart-state omission | unallocated |

The two different branch-local uses of `TCD-030` are a direct identifier collision and must never be treated as the same discrepancy merely because their number matches.

The reused PREP10 restart branch also contains a local reservation file claiming a local canonical tail of `TCD-031`. RG02 does not accept that claim as project-canonical because B3Q01 owns the qualified central register and ends at `TCD-027`.

## Superseded PREP10C TCD-032

The old `work/animo-prep10c-stable-dom-reset-readiness` branch proposed `TCD-032` for the stable-DOM event-reset candidate. The authoritative PREP10C reconciliation already records that proposal as superseded and redirects the candidate to the central `TCD-028` reservation. The old `TCD-032` must not be reused for that candidate.

This means local `TCD-032` is also collision-prone: the restart branch used it for the macropore solute writer omission while the superseded PREP10C branch used it for stable-DOM reset readiness. Neither local use creates a canonical ID.

## Integration rule

During evidence transplant:

1. preserve the original branch, head and blob provenance;
2. replace branch-local post-027 TCD references in governance metadata with the RG02 reconciliation key;
3. do not rewrite the scientific evidence text merely to remove its historical local label;
4. do not append any new canonical TCD number from RG02;
5. request canonical allocation only through the B3 governance line.

Machine-readable authority is in `integration/animo-reg/ANIMO_LOCAL_TCD_RECONCILIATION.json`.

With this mapping persisted, RG02 gate G1 is complete for the observed post-027 preparatory lineages. G2, path-level transplant of supplemental evidence, remains unexecuted.

`scientific_baseline_changed=false`

`corrected_legacy_admitted=false`

`production_migration_admitted=false`

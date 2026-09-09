# ANIMO-ARCH07 external crop adapter qualification test specification

Status: `CANDIDATE_TEST_SPECIFICATION_ONLY`.

## Ownership target

This specification applies when ARCH06 normalizes `crop_mode=external`.

The crop model owns its persistent crop state. ANIMO receives immutable observations and demand/exchange requests and may return realized nutrient uptake as trial results. No adapter may create a second ANIMO-owned persistent crop state in this mode.

## Input conformance

A positive external-crop fixture must exercise, as applicable:

- crop active status;
- root-distribution information;
- N and P uptake demand;
- optional crop N/P begin/end observations for nested conservation views;
- optional shoot/root dry-matter observations;
- explicit residue/exudate bundles;
- explicit harvest/grazing/export bundles.

Each field is validated against the exact ARCH05 unit, shape, temporal role and activation condition.

## Root distribution

The adapter must not guess whether a supplied distribution is normalized, weighted, layer-integrated or otherwise transformed. Its distribution contract must be explicit and compatible with the bound crop exchange schema and geometry.

ARCH07 does not invent a floating-point sum tolerance. A later numerical/adapter contract must define how any floating representation check is judged.

## Realized uptake

`CROP-N-UPTAKE-REALIZED` and `CROP-P-UPTAKE-REALIZED` are ANIMO trial results, not direct writes into crop persistent state.

A qualification test must establish that each nonzero realized result is:

- bound to the current `trial_id`;
- represented by the corresponding typed N or P soil-to-crop transfer event;
- absent from committed physical ledgers before coupled accept;
- discarded on reject;
- delivered to the external crop owner as part of the same logical accepted interval on coupled commit.

ARCH07 does not define the scientific uptake algorithm or a demand-exceedance tolerance.

## Residue and exudate transfers

The crop adapter cannot infer soil material additions from a difference between crop begin and end state.

Residues, root death, exudates or other crop-to-soil returns must arrive as explicit typed event bundles containing the relevant conserved quantities and destination compartments. The qualification pair is deliberately asymmetric:

- positive case: explicit bundle produces the corresponding candidate transfer events;
- negative case: crop state changes without a bundle produce no inferred soil addition.

## Harvest and grazing exports

If a combined soil+crop conservation view is requested, harvest, grazing and other external crop removals must be explicit observer/event bundles. They are not reconstructed as an unexplained remainder from crop-state change or the ANIMO soil balance.

## State observations are not ownership

Crop N/P and dry-matter beginning/end observations can support nested ARCH03 control-volume views. Their presence does not make them ANIMO state. The future adapter harness must verify that disabling those diagnostics does not change ANIMO physical state or realized transfer results.

## Immutable frames

Changing any demand, state observation or event bundle under an already bound crop frame ID is invalid. Retry with changed content requires a new immutable frame identity and new trial binding.

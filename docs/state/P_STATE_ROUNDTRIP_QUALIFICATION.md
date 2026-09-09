# ANIMO-STATEQ01 site-resolved P-state roundtrip qualification

Status: `PASS_SYNTHETIC_INPO1_SITE_RESOLVED_ROUNDTRIP_NON_B2`

Canonical STATE admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Scope

RC-R4 checks the P-active explicit-state checkpoint contract for the restricted-core candidate.

The current persistent-state matrix identifies four phosphorus owner families:

- aqueous orthophosphate per soil layer;
- equilibrium fast sorbed phosphorus per `[soil_layer;fast_site]`;
- non-equilibrium slow sorbed phosphorus per `[soil_layer;slow_site]`;
- precipitated phosphorus per soil layer.

Summed mineral-P and summed sorbed-P quantities are derived views, not independent checkpoint owners.

This sentinel is deliberately restricted to an explicit `Inpo=1` qualification fixture. It does not qualify the `Inpo=2/3` initialization-to-restart projection and does not change TCD-014 or TCD-024 governance.

## Candidate checkpoint rule

The checkpoint retains the full site-resolved owner coordinates and an exact layout header containing:

- soil-layer count;
- fast-site count;
- slow-site count;
- explicit initialization-mode identity for the fixture.

Restore must preserve site order and cardinality exactly. Missing values may not be zero-filled and extra values may not be truncated.

The layout header is validated before the site-resolved state is accepted as a restored state. RC-R7 separately covers the broader physical-layout fail-before-consume contract.

## Derived P views

The harness recomputes a total-P view per layer from aqueous, all fast sites, all slow sites and precipitated P. That total is deliberately absent from the checkpoint payload.

This makes ownership explicit: changing or omitting a site-resolved owner changes the derived total, but the total itself is not a second mutable degree of freedom.

## Executed result

GitHub Actions run `34337364081`, job `102419793911`, executed the persisted sentinel at head `4a49f9fc157ed295bb397dc7f559194c69d6cbdd` under CPython 3.12.14.

Result:

- 13 tests run;
- 13 passed;
- 0 failed;
- exact site-resolved roundtrip passed;
- fast and slow site order was preserved;
- layout/cardinality mismatches were rejected;
- missing sites were not zero-filled;
- extra sites were not truncated;
- derived P totals were absent from the checkpoint and recomputable from owners;
- checkpoint and restore did not mutate their inputs.

## Evidence boundary

The executable sentinel uses exact rational values to avoid introducing an arbitrary floating comparison policy into this structural roundtrip test.

The pass proves synthetic candidate-state roundtrip and cardinality semantics only. It does not prove revision-53 uninterrupted-versus-split trajectory equivalence, numerical P-process equivalence or canonical STATE admission.

`Inpo=2/3` remains explicitly outside this qualification. A later admitted route must separately qualify any initialization-to-explicit-state canonicalization for those modes.

## Files

Harness:

`tools/stateq01/p_state_roundtrip_harness.py`

Tests:

`tests/stateq01/test_p_state_roundtrip_harness.py`

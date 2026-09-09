# Ordered TTUTIL rollout policy

The rollout is by contract family, not by file count.

| Order | Family / scope | Risk class | Action |
| --- | --- | --- | --- |
| 1 | direct-file routing | low scientific risk, medium parser-quirk risk | pilot strict legacy adapter and separate native schema if desired |
| 2 | MATERIAL non-GHG static core | medium/high | pilot only after normalized dump/default provenance exists |
| 3 | CHEMPAR static P parameters | medium | migrate after site/horizon cardinality and dummy-field mapping tests |
| 4 | BOUNDARY static/series split | medium | split static configuration from time series before TTUTIL use |
| 5 | SOIL | high | only after geometry, feature activation and source defaults are fully explicit |
| 6 | PLANT | high | only after crop-type variants and compatibility defaults are explicit |
| 7 | GENERAL | high parser-contract risk | retain strict legacy ordering in legacy adapter; any order-free TTUTIL file is a new versioned representation |
| 8 | MANAGEMENT | specialized | keep specialized event adapter; TTUTIL utilities may support a future new schema but not replace sequential event semantics blindly |
| 9 | external crop | specialized | keep ARCH05 crop exchange adapter; parser and scientific/time normalization must be separated first |
| 10 | external soil temperature | specialized | keep forcing adapter; fixed runtime series is not ordinary static config |
| 11 | INITIAL / restart | specialized state owner | keep explicit initialization/checkpoint adapter |
| 12 | WATBAL.INP + hydrology exchange | specialized external owner | align to ARCH05 hydrology binding; do not fold into general config parser |
| blocked | GHGMais / unresolved GHG schema | lineage-sensitive | reject under revision-53 until provenance-qualified versioned adapter exists |
| excluded | SWATRE.UNF, WATBAL.UNF, SWAP.BUN, result.bun | binary/runtime | never convert to TTUTIL under this work unit |

Every step must separately pass positive normalized equivalence, negative parser contract, default provenance and ordinary model regression. Model regression alone cannot promote a family.

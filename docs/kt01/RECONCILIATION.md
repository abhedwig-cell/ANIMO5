# ANIMO-KT01 Reconciliation

Phase: `RECONCILE`.

## Live authority check

Immediately before branch creation, no branch named `animo-kt01` and no repository code result for `ANIMO-KT01` or a materially equivalent SWAP5 runtime-substrate reuse workunit was found.

The requested authority pins were rechecked live. GOV06, TIMEQ01, TIME02 and the SWAP5 canonical heads matched the supplied values. No newer central ANIMO regie authority was found. GOV06 remains the legitimate branch base. GOV06 records B3Q06 as a negative whole-B3 closure gate and states that B4 remains closed. KT01 therefore cannot be a production admission path.

The six required SWAP5 source blobs were checked at both the pinned scientific production source `50346642bd565f79134ea17d5462e544b354998c` and live canonical `992a5c657bfe10a10100f92e0cb77c4825ae65b6`. All six blob identities are unchanged between those authorities, so there is no source delta requiring a stop before classification.

## Semantic crosswalk

| SWAP5 concept | ANIMO contract | Compatibility | Semantic mismatch | Required KT01 adaptation | Permitting/limiting authority |
| --- | --- | --- | --- | --- | --- |
| committed physical state | `AcceptedState` | high at execution-mechanics level | SWAP carrier embeds SWAP transaction type and floating committed time | ANIMO-native accepted carrier, immutable during trial, exact TIME02 candidate coordinate | ARCH01, TIMEQ01, TIME02 |
| candidate/trial state | `TrialState` | high | SWAP candidate fields use SWAP physical type and real interval endpoints | private ANIMO synthetic candidate bound to exact origin lineage, generation/revision and time | ARCH01, TIMEQ01, TIME02 |
| checkpoint | accepted-only restart snapshot | high | SWAP snapshot has schema/layout but not the full ANIMO configuration/feature identity surface | add explicit schema, state layout, configuration and feature-layout identities; no trial/scratch/journal | ARCH02, ARCH04, ARCH06 |
| lineage identity | accepted-generation/transaction lineage | compatible pattern | SWAP lineage is local kernel provenance; coupled owner generations are not represented | preserve local lineage and keep coupled-owner identity explicit/separate | ARCH01, ARCH05, TIMEQ01 |
| revision/generation identity | accepted generation | compatible pattern | naming and owner scope differ | ANIMO revision/generation increments exactly once only on accepted publication | ARCH01, TIMEQ01 |
| trial origin | interval/trial binding to accepted start | compatible pattern | SWAP origin time is REAL | bind exact TIME02 candidate coordinate plus origin revision/lineage | TIMEQ01, TIME02 |
| atomic commit | accepted publication | compatible pattern | SWAP commit is one kernel owner; ANIMO coupled use can require an atomic logical commit group | prototype proves local atomic publication only and leaves coupled barrier as an external contract | ARCH01, ARCH05 |
| rollback/reject | discard candidate and uncommitted events | high | SWAP result/accounting payload is water-runtime shaped | complete discard of synthetic candidate and trial-local typed events; accepted state unchanged | ARCH01, TIMEQ01 |
| retry | fresh attempt from accepted origin | partial | SWAP reference implementation contains retry scaling, full/half estimation and solver policy | retain only origin-reset mechanics; retry/subdivision decision is injectable/test-only and receives fresh attempt identity | TIMEQ01, NQ01, GOV06 |
| interval orchestration | accepted origin -> private work -> attempts -> accepted internal progress -> final publication | high control-structure compatibility | SWAP uses REAL endpoints, tolerance-based progress, water/solver aggregation | exact time comparisons, fail-closed progress, generic acceptance, no SWAP diagnostics or water fields | TIME02, ARCH01, ARCH03 |
| temporal progress | exact ANIMO time progress | incompatible implementation detail | SWAP uses floating comparisons/tolerance | no epsilon, no ULP, no REAL canonical equality; bounded exact rational backend | TIME02 |
| persistence | accepted continuation only | high mechanics compatibility | SWAP persistence lacks ANIMO configuration/feature identities and stores real time | serialization-neutral ANIMO-native snapshot with exact time and ANIMO identity fields | ARCH02, ARCH04, ARCH06, TIME02 |
| scratch ownership | worker/job-local scratch | high principle compatibility | SWAP worker payload is HeadCalc/hydraulic/sensitivity/calendar specific | new minimal ANIMO worker context; no hydraulic arrays or solver predesign | ARCH01, GOV06 |
| diagnostics ownership | nonphysical attempt/report data | compatible principle | SWAP diagnostic fields are solver/hydraulic specific | separate minimal diagnostic counters from physical state; never checkpoint as physical continuation | ARCH01, ARCH02, TIMEQ01 |
| forcing ownership | immutable external frames / request data outside physical state | partial | SWAP canonical forcing seam is not the ANIMO frame-identity contract | retain ANIMO ARCH05 immutable frame ownership concept; KT01 prototype does not implement real hydrology/crop frames | ARCH05, ARCH06 |
| numerical-policy ownership | explicit policy reference, separate from science/state | partial | SWAP supplies concrete tolerances, fallback/retry and step-doubling choices | no inherited numerical tolerances or fallback ladders; only explicit attempt/substep budgets and injectable test policy | NQ01, ARCH06, GOV06 |
| transfer/event journal | trial-local typed physical events | mismatch in available implementation payload | SWAP inspected modules primarily expose aggregate water/mass result fields rather than ANIMO typed multi-quantity journal semantics | implement ANIMO-native trial journal with typed quantity/control-volume/event identity | ARCH01, ARCH03, TIMEQ01, MASSQ04 |
| conservation acceptance | multi-quantity, control-volume-aware supplied assessment | incompatible SWAP scientific acceptance | SWAP reference path has single water/mass residual and tolerance | generic collection of supplied assessments with completeness/admissibility; runtime chooses no scientific tolerance and creates no balancing flux | ARCH03, MASSQ04 |
| coupled-owner identity | bound ANIMO/external owner generations and frames | design relation only | inspected SWAP runtime does not define ANIMO owner-generation/frame identity | keep local prototype owner/lineage identity compatible with later ARCH05 orchestration, but do not invent a distributed protocol | ARCH05, TIMEQ01 |
| restart compatibility | exact accepted-state compatibility identities | partial | SWAP layout/schema check is narrower than ANIMO requirements | exact schema + physical layout + configuration + feature layout + lineage/revision + exact time validation | ARCH02, ARCH04, ARCH06, TIME02 |
| configuration/layout identity | multiple narrow identities | partial | SWAP persistence uses one layout id and SWAP-specific state layout | carry separate prototype state-layout, configuration and feature-layout ids; do not substitute broader ids | ARCH04, ARCH06 |

## Time boundary

TIME02 remains candidate semantics and explicitly has `canonical_time_admitted=false`. KT01 may realize a bounded integer backend only as a prototype. The implementation must normalize rationals exactly, compare without unchecked integer cross-products, serialize/deserialize without loss, and fail closed on overflow or nonrepresentability. No fixed timestep quantum is introduced.

## Production and evidence boundary

TIMEQ01 is synthetic runtime evidence, not B2 historical evidence. SWAP5 Status-A and SWAP5 source qualification are evidence about source-of-reuse, not ANIMO authority. The prototype therefore cannot establish historical ANIMO restart/rollback equivalence, B3/B4 admission, canonical TIME, production readiness, Status A or Status AA.

## Reconcile disposition

`RECONCILE_PASS_TO_CLASSIFY`.

No current authority conflict was found that prevents an isolated nonproduction prototype. The next permitted action is classification of each considered SWAP5 implementation element before any implementation is written.

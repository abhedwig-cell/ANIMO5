# ANIMO-TB03B transaction, mass-conservation and control-volume bank adoption

Status target: `QUALIFIED_TB03B_BOUNDED_TRANSACTION_AND_CONSERVATION_FRAGMENT_PACKAGE`.

## Scope

TB03B adopts reusable conservation contracts into the ANIMO5 testbank architecture without changing production source, performing TCD admission, mutating the central testbank registry, or creating a whole-model golden baseline. It is based on qualified TB02 infrastructure and uses TB01 taxonomy and permanence criteria.

The primary scientific input is MASSQ02. Its typed-event projection requires a single directed physical edge with non-negative amount, explicit owner membership and exact internal cancellation. MASSQ02 also requires observer independence from legacy balance accumulators and rejects magnitude-based residual acceptance. PREP06 supplies conserved-state ownership context, but public legacy balance arrays remain reporting surfaces rather than physical state owners.

## Adopted contracts

Every conservation test in this fragment must declare the conserved element, the species or pool, beginning and ending physical storage, external inputs, external outputs, internal transfers, boundary signs and a residual equation. Missing declarations are a qualification failure.

The common residual orientation is:

`R = begin_storage + inputs - outputs + internal_net - end_storage`.

A directed internal event uses one non-negative amount `q` and one edge `source_owner -> destination_owner`. The source contributes `-q`; the destination contributes `+q`. When both owners are inside the selected control volume, the contribution cancels exactly. No tolerance belongs to that identity.

For a single layer, inter-layer interfaces are boundaries of the local control volume and therefore appear with explicit direction. For the whole profile, those same layer-to-layer edges become internal and cancel exactly once. An interface must never be independently booked on both sides as two physical events.

NH4-N and NO3-N remain separate species ledgers. They may be aggregated to elemental N only after species-resolved storage and transactions are formed. Nitrification is therefore an internal NH4-N to NO3-N transfer for an encompassing total-N control volume, not an external N source or sink.

## MASSQ01/02 and audit adoption

TB03B does not copy MASSQ residual values into a golden baseline. Instead it adopts the reusable semantics behind them: physical-owner storage, typed transactions, causal residual interpretation, explicit control volumes and no acceptance by magnitude. Known and newly causal MASSQ findings remain evidence about legacy behavior; they are not converted into balancing events.

TB01 already reserves reusable balance index/deviation audit adapters. TB03B makes those structural audits prerequisites for conservation interpretation. They can detect species/index drift or known reporting deviations, but an audit result is never itself a mass flux.

## Permanence decision

Permanent candidates are only cross-case contracts that remain useful after individual TCDs are corrected: single-edge transaction semantics, explicit sign rules, local-layer control-volume equations, whole-profile internal cancellation, species-preserving N aggregation and structural balance/index audit gating.

TCD-specific debugging probes, individual legacy residual magnitudes and execution-only causal probes are deliberately not promoted to permanent testbank entries by TB03B. They can remain provenance or historical evidence and may support later bounded tests when their scientific purpose is separately qualified.

## Scientific boundaries

No scientific tolerance is introduced. A later numerical runner may need floating-point comparison metadata, but such an execution tolerance cannot redefine the conservation identity or turn a non-zero physical residual into scientific closure.

Whole-system elemental C remains unqualified. GHG-complete C/N topology remains outside this fragment. Soil/crop membership must be declared per control volume, because crop uptake is an external sink for a soil-only volume but an internal transfer for a soil+crop volume.

## GOV05 adversarial self-review

The same agent challenged the fragment against the principal failure modes: double-booked interfaces, sign ambiguity, silent NH4/NO3 conflation, balance-array ownership, compensating events for known nonclosure, tolerance promotion, central-registry mutation and scope expansion into admission. The result is process self-review only and is not represented as independent review.

Qualification is valid only after exact-final-head GitHub Actions success for the TB03B workflow.

# ANIMO-TB04B — Boundary & Initialization Bank Adoption

## Scope

TB04B adopts a bounded TB-L6 fragment only. It does not modify the central testbank registry, production source, canonical TCD state, or numerical policy.

The fragment separates what is actually qualified from what remains open:

- the TCD-042 exact-zero-throughflow upper-reservoir atom is reusable only for `Flux=0` and `Hetop>0`;
- the naturally reachable finite-positive subthreshold seam remains a numerical-policy gap;
- `HETOP=0` remains semantically non-unique and no model policy is selected;
- the GHG closed lower external advective air boundary is exactly zero in the BUILDQ04 contract, while the production initialization defect remains unadmitted;
- whole-model cold-start/restart boundary and initialization completeness remains open.

## Why ATB-BND-001 is not reused as qualified authority

TB01 registered `ATB-BND-001` as an adapter candidate with broad wording across zero, subthreshold and active domains. Subsequent UBQ work showed that those domains cannot be treated as one already-qualified contract. TB04B therefore leaves the central entry untouched and creates narrower fragment IDs. A later serial registry-consolidation workunit must decide whether and how `ATB-BND-001` is superseded.

## Permanent contracts

`ATB-BND-002` preserves the qualified exact-zero upper-reservoir conservation limit and its exact isolated natural probe. `ATB-BND-005` preserves the qualified closed GHG lower-air boundary value and rejects compiler-provided uninitialized state as model semantics.

`ATB-BND-003`, `ATB-BND-004` and `ATB-BND-006` are explicit gaps. They are permanent gap trackers, not pseudo-tests with inferred expected values.

## GOV05 adversarial self-review

This is same-agent adversarial review and is not independent. The review explicitly tested for accidental widening of TCD-042, empirical-tolerance promotion, invented `HETOP=0` semantics, conversion of BUILDQ04 into a production fix, whole-model overclaiming and central-registry mutation. All are prohibited by the fragment and CI guard.

## Qualification boundary

Qualification of this package means the manifest accurately and mechanically preserves the bounded upstream authorities and gaps. It does not mean TCD-042 is fully qualified or admitted, does not choose a numerical threshold or tolerance, does not admit a GHG production repair, and does not establish whole-model boundary or initialization qualification.

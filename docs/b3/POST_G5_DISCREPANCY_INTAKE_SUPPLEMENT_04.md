# ANIMO-B3I01 live post-G5 intake supplement 04

Status: `BUILDQ04_GHG_BOTTOM_BOUNDARY_CANDIDATE_RESERVED_PENDING_REGISTER_APPEND_NO_ADMISSION`

This supplement consumes completed ANIMO-BUILDQ04 evidence for the `GHGasses` lower air-boundary first-use finding. It supersedes only the evidence-state disposition assigned to this same local key in supplement 03. It does not reinterpret BUILDQ03 storage-duration findings and does not admit corrected behaviour.

## Authority checked

B3I01 prior head before reservation:

`91bedfcfdc2af7b0183a3d4898d5f638b1bce4a4`

BUILDQ04 source head:

`work/animo-buildq04-ghg-bottom-boundary-initialization@0ae1e58f80ca01c1b6eced7ac0d6e5c031827676`

BUILDQ04 executable qualification succeeded at both the original qualification head and the status closeout head. Historical Intel behaviour remains unknown.

Canonical register before reservation:

- tail `TCD-040`;
- blob `fb44f54aabcf9cd9ee8a8a52bbec78e5cdf06c25`.

A best-effort collision audit immediately before reservation found no `TCD-041` in the authoritative register tail, default-branch code search, issue search, pull-request search or matching branch refs. The current connector does not expose the commit-search endpoint used in some earlier intake passes, so this is recorded explicitly rather than silently claimed. The reservation is not a transactional repository lock.

## BUILDQ04 evidence change

Supplement 03 retained:

`BUILDQ03-LCL-GHGASSES-FLAIR-NLPLUS1-UNINITIALIZED`

as:

`BUILD_RUNTIME_INITIALIZATION_HAZARD_NOT_TCD_PENDING_BOUNDARY_SEMANTICS`

That was appropriate at the time because the intended lower boundary value was not yet independently established.

BUILDQ04 now closes that missing semantic step.

Full source-control-flow reconstruction proves that after the `La=Max(0,La-1)` update:

`0 <= La <= Nl-1`

for every `Nl>=1`. Therefore Task 1 never assigns `Flair(Nl+1)` before the bottom transformation reads it. The first-read gap is source-unconditional over the normal layer domain, not merely a special `La<Nl` case.

Connected revision-53 source also defines `Flair(Nl+1)` as the lower external advective air interface and establishes a closed lower GHG gas boundary. `GHGtransport` has no lower-neighbour gas concentration or bottom diffusion term; `GHGtranssub` removes lower inflow and diffusion coupling; no bottom-air reservoir input exists. The qualified local boundary identity is therefore:

`Flair(Nl+1) = 0.0`

for the preserved revision-53 closed lower GHG air boundary.

The 2011 peer-reviewed ANIMO N2O formulation is consistent with vertical air advection and atmosphere-soil emission but does not by itself specify this exact revision-53 discrete bottom boundary. The zero identity remains primarily a connected-source result.

## Controlled materiality

BUILDQ04 separates compiler accident from boundary semantics.

An uninitialized first-read probe shows GNU optimization and initialization sensitivity, including NaN propagation and nonzero automatic-storage values.

A separate 60-row boundary sensitivity matrix makes the missing coordinate explicit and is byte-identical at O0 and O2. Positive artificial lower flux directly changes bottom gas advection and the disappearance coefficient. Thus the finding is controlled `FLUX_MATERIAL` and `STATE_MATERIAL`, with output materiality possible. Historical Intel magnitude remains unknown.

## Canonical classification

The phenomenon is not TCD-011. TCD-011 concerns cross-call storage duration. TCD-041 concerns a same-call first-use omission for one external interface coordinate whose intended value is now source-qualified.

It is also distinct from canonical GHG TCD-032 through TCD-037.

Provisional class:

`B`

Subtype:

`LOCAL_BOUNDARY_INDEX_INITIALIZATION_OMISSION`

No new physical state is introduced and no numerical policy is changed.

Fail-closed reservation:

`TCD-041`

Canonical phenomenon:

`GHG lower air boundary initialization`

Reservation is identity and routing only. It is not admission.

## Required admission work

Before any corrected behaviour can be admitted:

- retain the exact connected-source zero lower-boundary identity;
- exercise an activated qualified GHG case;
- prove the minimal local correction covers all active Task-1 paths;
- compare unrounded affected gas flux and state trajectories;
- prove non-interference outside the lower GHG air-advection boundary;
- preserve historical Intel behaviour as unknown unless matching reference evidence is recovered;
- obtain independent B3 review.

## Admission state

`new_corrections_admitted=false`

`b3_baseline_established=false`

`production_migration_admitted=false`

`evidence_strength_increased_by_routing=false`

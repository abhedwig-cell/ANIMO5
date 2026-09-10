# ANIMO-STATEQ04 — TCD-031 qualification-only macropore restart remediation

Status: `QUALIFIED_CANDIDATE_RESTORE_CONTRACT_READY_FOR_TIER_C_READINESS_NOT_ADMITTED`

Branch: `work/animo-stateq04-tcd031-macropore-restart-remediation`

Parent qualification: `ANIMO-STATEQ03@10c50e65d1369d5f3b26736c4b12d3a482379eb5`

Aggregate authority rechecked before branch creation: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`.

This workunit does not patch production source. It qualifies a candidate accepted-boundary checkpoint and restore transaction strongly enough to decide whether TCD-031 may proceed to a separate GOV04 Tier-C readiness/review cycle.

## Why STATEQ04 exists

STATEQ03 failed closed for two independent native revision-53 reasons. `Output_Init` persists none of the required active macropore solute concentration state, and the macropore block in `Init` promotes `RsCoMp*` into `CoMp*` even on the first timestep, while no corresponding native restart load for `RsCoMp*` exists on that path.

The failure established the missing contract but could not execute a meaningful native continuous-versus-split comparison. STATEQ04 therefore tests a qualification-only correction contract without claiming that revision 53 already implements it.

## Candidate persistent owner set

The accepted physical owner is the macropore dissolved concentration in each active domain. For P-off profiles the checkpoint requires eight scalar coordinates: DOM, DON, NH4-N and NO3-N in Main Bypass Flow and Internal Catchment. With P active it additionally requires DOP and PO4-P in both domains, for twelve scalar coordinates total.

The accepted mass identity for species `X` is:

`sum_domain(SrWaMpOld(domain) * CoMpX(domain))`

The result/end identity is:

`sum_domain(SrWaMp(domain) * RsCoMpX(domain))`

Macropore water and hydrological geometry remain external hydrology-owner state. The public/main balance arrays are observers, not state owners.

## Restore transaction qualified here

At an accepted restart boundary:

1. validate topology, accepted time and the external hydrology binding before mutation;
2. restore every enabled `CoMp*` domain coordinate exactly;
3. initialize `RsCoMp*` from restored `CoMp*` as a runtime result alias before any legacy result-to-start promotion can overwrite the accepted owner;
4. initialize `AvCoMp*`, `AvCoML*`, `MpReKo*` and other current-interval work arrays afresh;
5. run no chemistry or transport as part of restore;
6. resume with the next physical interval.

This does not make `RsCoMp*` an independent checkpoint degree of freedom. It qualifies deterministic alias reconstruction at an accepted boundary from the restored owner coordinate.

## Frozen-source kernel split discriminator

The executable discriminator compiles the frozen revision-53 `MAPOTRANSPORT.FOR` and `Transsub.for` bytes directly with GNU Fortran 14.2. The qualification driver is separate from production source.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

`MAPOTRANSPORT.FOR` SHA-256:

`735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da`

`Transsub.for` SHA-256:

`c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`

Qualification driver SHA-256:

`be3cc92e8e7a53347624ce902017f0e9dc588ecc1ddc2089fe3d35903cf4de7a`

Reproducible qualification executable SHA-256:

`d0ea3b40f1f41db478bbbb93ad0307ce33e33560787d2911fcdb8dd8a34f9f1f`

The build was repeated in two separate work directories. The executable hashes and complete machine-readable result files were identical.

## Active split design

No natural active-macropore case exists in the frozen nine-case testbank, so this remains synthetic B1-style diagnostic evidence. The discriminator uses both revision-53 macropore domains with nonzero stored water, direct surface inflow, matrix-to-macropore inflow, macropore-to-matrix transfer and Main Bypass direct drainage. Current-step forcing varies by timestep.

Each species is exercised separately with a distinct nonzero concentration scale:

- DOM;
- DON;
- NH4-N;
- NO3-N;
- DOP;
- PO4-P.

For each species, uninterrupted execution runs ten accepted steps. The split run executes steps 1 through 5, serializes accepted `CoMp(1:2)` plus the external hydrology boundary coordinate used by the isolated kernel, terminates the process, starts a fresh process, reconstructs `RsCoMp=CoMp`, resets all current-step workspace and executes steps 6 through 10.

The comparison includes accepted concentration, result concentration, accepted water storage, average domain concentration, macropore-to-matrix source and the local matrix-input bookkeeping written by the kernel driver.

Comparison policy: `EXACT_BYTEWISE_NO_TOLERANCE`.

## Result

For all six species:

- Stage-A trace equals the uninterrupted prefix exactly;
- the fresh-process Stage-B trace equals the uninterrupted five-step suffix byte-for-byte;
- first post-restore absolute difference is exactly zero in both domains;
- no `MPTRANSP` balance-warning bytes are emitted.

The result is not merely a deterministic rerun in one process. Stage B is a fresh executable process, so saved/static kernel work arrays do not survive the split.

## Causal negative controls

Two negative discriminator families were required.

First, the revision-53 native-direction failure is emulated by restoring `CoMp`, leaving `RsCoMp` unrestored at zero, then performing the legacy `CoMp=RsCoMp` promotion before continuation. Every species diverges at the first post-restore step. The first-step concentration differences are large compared with exact zero in the corrected candidate route and no tolerance is used to hide them.

Second, each accepted domain coordinate is independently removed from the candidate checkpoint. Dropping domain 1 or domain 2 causes the continuation suffix to diverge for every species. This is direct executable evidence that both domain concentrations are required persistent coordinates rather than reconstructible decoration.

The higher-level inactive controls remain the pinned MP02 `NO-MP` complete case and the STATEQ02 exact split profile with macropores excluded. Those are stronger negative feature-topology controls than inventing a second synthetic no-op kernel case here.

## What this proves and what it does not

STATEQ04 qualifies the candidate state ownership and restore transaction at the frozen source-kernel boundary. Together with MP02, which already proves complete-model reachability of all six active macropore species, the evidence is sufficient to stop treating TCD-031 as an undefined state-model problem.

It does not prove a whole-ANIMO active-macropore split run. It does not establish historical B2 behaviour, parameter realism or a production checkpoint format. A future production implementation must still be independently reviewed and must reproduce this accepted-boundary contract in complete-model tests.

## Downstream decision

`TCD-031 atomic GOV04 Tier-C readiness = MAY_OPEN`

This means a separate readiness/admission workunit may now be authored. It does not mean TCD-031 is B3-admitted. GOV04 second-line review remains mandatory before admission.

For TCD-025, the state-side prerequisite is now sufficiently constrained to open a separate Class-A ledger-readiness workunit. STATEQ04 supplies the exact beginning/end macropore solute storage coordinates and owner boundary needed by that observer correction. TCD-025 still has to prove direct-drain/Dra4 integration, unchanged physical state and flux trajectories, conservation closure, non-interference and the applicable historical-uncertainty review route.

`TCD-025 Class-A ledger readiness = MAY_OPEN`

No TCD-025 correction or composition is performed here.

Final status:

`QUALIFIED_CANDIDATE_RESTORE_CONTRACT_READY_FOR_TIER_C_READINESS_NOT_ADMITTED`

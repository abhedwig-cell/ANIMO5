# ANIMO-B3B10R2 — Targeted Independent Rereview of TCD-031 Source Provenance & Restart-State Evidence

## Disposition

`PASS_TARGETED_INDEPENDENT_REREVIEW_TCD031_SOURCE_PROVENANCE_GATES_CLOSED`

This is a targeted GOV04 Tier-C rereview. It closes only the source/provenance insufficiency recorded by ANIMO-B3B10R. It does not perform a B3 admission, production patch, canonical state admission, canonical TCD-register update, TCD-025 composition, B4 action, or RG05 update.

The original ANIMO-B3B10R remains the historical authority for the first fail-closed review. This document is a separate rereview authority.

## Exact review base and live authority check

The rereview branch was confirmed at the requested clean start:

`ANIMO-B3B10E1@8522752f9941e6fd5b421cf5ac4ef839384d7ce7`

A persist-early checkpoint was then committed as:

`a20325d819c92bc49aebafd720ad045c635fb5f1`

Current authorities rechecked live before the substantive rereview:

- aggregate: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`
- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- STATEQ03: `10c50e65d1369d5f3b26736c4b12d3a482379eb5`
- STATEQ04: `ef9a5998cafae433deeba701a8e9a8a08eacc92f`
- B3B10: `eccba6712f65455161d05fa9cdf6aa142f823dd4`
- B3B10R: `36aad892cac546105dfec0fe43aa34a18e23bcad`
- B3B10E1: `8522752f9941e6fd5b421cf5ac4ef839384d7ce7`
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`
- MP02: `6b0f2e7470f13baeb6612b0bddb662a497dea528`
- MASSQ02: `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`
- latest routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- frozen B0 retention: `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`

The aggregate advanced from RG05G to RG05H, but that change concerns later routing/admission integration and does not supersede or alter the pinned TCD-031 evidence authorities. No later TCD-031 targeted rereview, dedicated TCD-031 issue, or contradictory later TCD-031 evidence was found. The only TCD-031 PR mention found is PR 19, which is routing-only and has no issue comments or reviews.

## Independent source replay and provenance chain

The exact frozen archive supplied to the reviewer was independently hashed before using any B3B10E1 conclusion:

`ANIMO_4.1.5.53(3).zip`

SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The archive contains 63 `.for`/`.inc` source members. A fresh canonical source-member index reproduced:

`be4182c7438650f86399f912c57bbad42adf71fc362b694537f2db4d64c816fc`

All nine requested member hashes independently match the B3B10E1 pins:

- `mapoinput.for` `081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065`
- `Init.for` `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`
- `Output_Init.for` `6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f`
- `Animo.for` `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`
- `MAPOTRANSPORT.FOR` `735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da`
- `Transca.for` `7f31150050bd41aef203587818cde94cf689e6288094b2ad84aea34732b07ff9`
- `Transgen.for` `cd5efa76c1a4840b50901ee5015940b74c5fe4df79aca43d53a4a4cb77b9fecb`
- `input1.for` `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`
- `Hydro_detailed.for` `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`

The normalized line-slice hashes for all B3B10E1 source probes were independently regenerated and match the committed probe records. The chain therefore closes mechanically as:

`archive SHA-256 -> source-member SHA-256 -> exact normalized line slice SHA-256 -> structured probe claim`

The committed B3B10E1 generator verifies those links and rejects mismatched archives, member hashes, line slices, source-index identity, unexpected named `RsCoMp*` writes, or changed call ordering. The archive itself is not repository-visible and is not republished by this rereview. Public redistribution rights remain unestablished, but source access/licensing is no longer the evidence blocker because the rereview could perform the controlled local hash-bound replay without redistributing source text.

B3B10E1 workflow run `34541324786` is green. Its role is package integrity and replay-contract completeness only. It is not treated as the scientific review PASS.

## Targeted failed-gate results

### 1. Complete source-level ownership: PASS

The source supports distinct lifecycle roles rather than only manifest labels.

Persistent accepted ANIMO macropore solute state is `CoMpDiorMa`, `CoMpDiorNi`, `CoMpNh`, and `CoMpNi`, with `CoMpDiorPo` and `CoMpPo` added when phosphorus is active. Each is two-domain state.

`RsCoMp*` is the end-of-interval/result alias generated later by macropore transport and consumed by the next `Init` promotion. `AvCoMp*`, `AvCoML*`, and `MpReKo*` are current-interval workspaces produced and consumed inside the macropore transport path. `ItRec` is an iteration diagnostic, initialized separately and incremented by species-specific transport iterations. `SrWaMp`, `SrWaMpOld`, `SrWaMpCp`, and `SrWaMpCpOld` are hydrology-owned dependencies rather than TCD-031 solute checkpoint coordinates.

### 2. Native `mapoinput.for` loader: PASS

For `Nupa=4`, revision 53 actively reads:

- `>MPnitr:` into `CoMpNh(1:2)` and `CoMpNi(1:2)`;
- `>MPorgs:` into `CoMpDiorMa(1:2)` and `CoMpDiorNi(1:2)`;
- `>MPphos:` under `Ipo.EQ.1` into `CoMpPo(1:2)` and `CoMpDiorPo(1:2)`.

`input1.for` actively calls `Mapoinput` task 4 when `Ioptmp=1`. The proof therefore includes destination mapping and both domains, not merely label discovery.

A separate `Checkrea` wrong-species argument seam exists for the NO3 validation calls after the read. It does not change the active `Read` destination proven here and is outside this TCD-031 restart-state scope.

### 3. Native `Output_Init.for` serialization omission: PASS

The macropore writer code exists in revision 53, but the macropore arguments in the `Output_Init` signature and the entire `>mpnitr` / `>mporgs` / conditional `>mpphos` writer block are commented. Presence of source text is therefore not confused with executable active-path behavior.

The active `Output_Init` route does not serialize the persistent macropore solute end-state.

### 4. Native `Animo.for` Output_Init call surface: PASS

`Animo.for` actively calls `Output_Init`, but the macropore argument continuation is commented/inactive. The caller therefore agrees with the inactive callee writer path. The omission is not inferred from `Output_Init.for` in isolation.

### 5. Native `Init.for` restore direction and timing: PASS

The exact active direction is:

`CoMp* <- RsCoMp*`

for domains 1 and 2, with the phosphorus families conditional on `IPO.EQ.1`.

This macropore block occurs after and outside the first-timestep special-case block in `Init`. `Animo.for` calls `Init` before the macropore transport calls that produce `RsCoMp*`. Consequently the promotion also executes on the first active timestep of a resumed run and can overwrite `CoMp*` values loaded from `INITIAL.INP` before those values reach transport.

### 6. Native `RsCoMp*` pre-promotion initialization: PASS, answer NO

A fresh scan of all 63 frozen source members found no active family-specific direct assignment, `DATA` initialization, `SAVE` initialization, restart load, or active input reference that establishes any of:

`RsCoMpDiorMa`, `RsCoMpDiorNi`, `RsCoMpDiorPo`, `RsCoMpNh`, `RsCoMpNi`, `RsCoMpPo`

before the first relevant `Init` promotion.

Their production happens later through the generic `MPTRANSP` `RsCoMp` output path, including direct result assignments for zero-storage branches and the `Transsub` output argument for the general branch. The native answer is therefore `NO, with exact proof`, not `UNKNOWN`.

This result closes the evidence gate. It does not mean native restart behavior is correct. It proves the lifecycle defect that the future atomic correction must address.

## Persistent scalar count: PASS

There are exactly two macropore domains.

With phosphorus off, four persistent solute families times two domains gives 8 scalars.

With phosphorus on, two conditional phosphorus families add four scalars, giving 12 total. The phosphorus state is explicitly conditional on `IPO.EQ.1`.

## Atomic correction identity: CONFIRMED

`COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY`

The serializer and restore/lifecycle sides must remain one atomic correction. A serializer-only fix would still allow the first resumed `Init` to replace restored `CoMp*` from a non-restored `RsCoMp*` alias. A restore-direction/lifecycle-only fix would still lack a complete serialized accepted end-state. Correct restart transfer therefore requires both halves together.

## Reuse of previously passed B3B10R gates

GOV04 allows targeted Tier-C rereview only when failed gates are isolatable and reused PASS evidence remains immutable and pinned. Those conditions were checked live.

The exact pins for B3B10, B3B10R, B3Q01, GOV03, GOV04, MASSQ02, MP01, MP02, STATEQ03, and STATEQ04 remain unchanged. The frozen source archive hash and frozen testbank hash also reproduce exactly. No superseding or contradictory TCD-031 evidence was found.

The following prior gates are therefore reused rather than reopened: STATEQ04 candidate restore transaction, six-species kernel evidence, both-domain causal controls, native-bad emulation, exact bytewise/no-tolerance policy, fresh Stage-B process, MP02 active complete-model reachability at its existing B1 boundary, whole-model evidence boundary, atomicity contract evidence, and Tier-C classification.

No full rereview is required by GOV04 because the failure classes were evidence/provenance insufficiency, not scientific falsification, and the claim scope has not widened.

## Historical uncertainty and whole-model boundary

GOV03 remains `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`. No active macropore historical B2 reference was recovered. Therefore:

`historical revision-53 active macropore restart behaviour = UNKNOWN`

No historical intent is reconstructed from source.

The whole-model boundary also remains unchanged:

`whole-model active production split equivalence = NOT PROVEN`

This rereview PASS must not be interpreted as production restart equivalence, migration readiness, or whole-model checkpoint validation. Closing the source/provenance blocker does not supply those stronger claims.

## GOV04 risk tier

Tier C is retained. Restart/cold-start discrimination, initialization semantics, canonical state ownership, and checkpoint semantics are explicit GOV04 Tier-C triggers. A small future implementation diff does not by itself lower the scientific review risk tier.

## STATEQ04 and TCD-025 boundary

STATEQ04 is not reopened. The fresh source replay found no substantive contradiction with its pinned candidate evidence; the prior failure was evidence/provenance exposure, not scientific falsification.

No TCD-025 work is executed here. After this targeted independent PASS, TCD-031 may be consumed as a certified dependency for a separate TCD-025 Class-A ledger-readiness workunit. That statement authorizes neither TCD-025 composition nor admission.

## Admission boundary

Independent Tier-C review gate: `PASSED`.

B3 admission: `NOT YET PERFORMED`.

Production patch: `NOT PERFORMED`.

Whole-model production split: `NOT PROVEN`.

Historical B2: `ABSENT` under the current GOV03 closure authority.

An atomic TCD-031 B3 admission workunit may be opened only after this rereview's own fail-closed workflow is green on the exact final rereview head. The live B3D number must be checked at that point; this rereview does not create the admission branch.

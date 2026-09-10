# ANIMO-B3B10R — Independent Second-Line Review of TCD-031

Work unit: `ANIMO-B3B10R`

TCD: `TCD-031`

Branch: `review/animo-b3b10r-tcd031-independent-second-line`

Exact starting head: `ANIMO-B3B10@eccba6712f65455161d05fa9cdf6aa142f823dd4`

Review type: genuinely independent GOV04 Tier-C second-line review

Final disposition: `REMEDIATION_REQUIRED`

Failure classification: `EVIDENCE_INSUFFICIENCY` + `PROVENANCE_INSUFFICIENCY`

This is not a scientific falsification of the proposed restart-state contract. It is a fail-closed refusal to certify two native revision-53 source/lifecycle claims that cannot be independently replayed from primary source through the repository-visible evidence surface.

## 1. Live authority and routing check

The review branch was verified before any write to be exactly at `eccba6712f65455161d05fa9cdf6aa142f823dd4`. No later `ANIMO-B3B10R` independent-review work was found.

Live authorities rechecked:

- `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`
- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- `ANIMO-MP01@7b5979dd6301b9d55d23e8c22948a0dba24b229b`
- `ANIMO-MP02@6b0f2e7470f13baeb6612b0bddb662a497dea528`
- `ANIMO-STATEQ01@4adae99576eb56978da71f7c8a250e4445fd3bc4`
- `ANIMO-STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`
- `ANIMO-STATEQ03@10c50e65d1369d5f3b26736c4b12d3a482379eb5`
- `ANIMO-STATEQ04@ef9a5998cafae433deeba701a8e9a8a08eacc92f`
- `ANIMO-B3B10@eccba6712f65455161d05fa9cdf6aa142f823dd4`
- `ANIMO-MASSQ02@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`
- frozen B0 retention authority `a818b5a37b80ed92aded0b9c404990d356eb2300`

Canonical routing was checked through and beyond the handoff. `ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9` has been superseded as latest routing authority by `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`. B3I07 is a child of B3I06 and routes TCD-037; no TCD-031 scientific scope change was found.

Repository issue search found no GitHub issue whose text matches `TCD-031`. One historical PR, #19 / B3I01, mentions TCD-031 only as canonical discrepancy routing. It has zero issue comments and does not constitute an independent TCD-031 review.

## 2. Frozen source identity and independent-review limitation

The frozen source baseline is `ANIMO_4.1.5.53(3).zip`, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`, revision 53. The repository intentionally does not republish the raw archive because no redistribution licence has been established. It retains cryptographic identity and per-member hashes.

The review independently crosschecked the relevant manifest identities, including:

- `Animo.for` `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`
- `Init.for` `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`
- `input1.for` `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`
- `mapoinput.for` `081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065`
- `MAPOTRANSPORT.FOR` `735b3f86497a6968c24d2dbce2ad23ae350b4eed573da421baa1a7557a0615da`
- `Output_Init.for` `6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f`
- `Param.inc` `20d85ed8bca9e0060d3b51c2f800ff02fdf0bc3ebb8c834baf4afca870a33475`

Hash identity proves which source object prior extraction refers to. It does not let this independent reviewer inspect the primary bytes of `mapoinput.for`, `Output_Init.for`, `Animo.for`, or `Init.for` through the live GitHub evidence surface.

STATEQ03 contains hash-pinned line anchors for those files. Those anchors are useful source-bound evidence and are internally coherent, but this review was explicitly instructed not to accept STATEQ03 as authority and to inspect the source itself. That independent primary-source replay is unavailable here. The affected gates therefore remain fail closed.

## 3. Persistent-state identity

The proposed accepted macropore-solute state is structurally coherent:

P off:

- `CoMpDiorMa(1:2)`
- `CoMpDiorNi(1:2)`
- `CoMpNh(1:2)`
- `CoMpNi(1:2)`

This is four species times two domains = 8 scalars.

P on adds:

- `CoMpDiorPo(1:2)`
- `CoMpPo(1:2)`

This is six species times two domains = 12 scalars.

The STATEQ04 kernel harness independently exercises the same six species families as `DOM`, `DON`, `NH4`, `NO3`, `DOP`, and `PO4`, with two macropore domains. Its accepted coordinate is the two-element `comp` vector and its end/result alias is `rscomp`.

The kernel evidence strongly supports the physical interpretation that one accepted concentration coordinate per enabled species and domain is required across a restart boundary. It also supports treating the result coordinate as an alias/lifecycle result, not as a second independently checkpointed physical owner: the successful restore transaction loads the accepted coordinate and then initializes the result alias from it.

However, because the exact symbol mapping from frozen `MAPOTRANSPORT.FOR` to all named `CoMp*`/`RsCoMp*` variables is available here only through the prior STATEQ03 source extraction rather than primary source bytes, this review does not elevate the exact native symbol-level identity gate to independent PASS.

## 4. Ownership

At scientific-contract level the ownership split is coherent and no contradictory evidence was found:

- macropore solute accepted concentration is ANIMO-solute-owned physical continuation state;
- `SrWaMpOld`, `SrWaMp`, `SrWaMpCp`, and `SrWaMpCpOld` are hydrologic storage/geometry dependencies and must be restored/bound from the exactly compatible hydrologic state;
- `AvCoMp*`, `AvCoML*`, and `MpReKo*` are current-interval transport workspace and should be recomputed;
- `ItRec` is a derived iteration diagnostic and is not physical restart state;
- `RsCoMp*` is an end/result lifecycle alias of the same physical macropore-solute owner, not a second checkpoint coordinate.

MP02 independently establishes complete-model reachability of active macropore transport, including both domains and all six solute families. STATEQ04 independently demonstrates that the two-domain accepted solute coordinate controls future kernel trajectories.

The exact native producer/consumer ownership of all named symbols is nevertheless source-level Tier-C evidence. Because the primary revision-53 source bytes for the relevant lifecycle files cannot be independently inspected here, the source-level ownership gate remains incomplete rather than silently inherited from STATEQ03.

## 5. Native TCD-031 omission

STATEQ03 reports source anchors that `mapoinput.for` reads `>MPnitr:`, `>MPorgs:` and conditional `>MPphos:` into the accepted/start macropore concentrations, while `Output_Init.for` has the matching restart writer records commented and `Animo.for` comments the macropore arguments at the active `Output_Init` call surface.

MP01/MP02 independently persisted the same omission classification from their source investigations.

No contradictory evidence was found. The claim is highly plausible and provenance-pinned to exact source member hashes. But the user-required review gate is stronger: this independent context must verify the frozen source itself. Because those source bytes are not repository-visible, this review cannot independently certify that the writer block and call arguments are actually commented/inactive or that the loader reads exactly the claimed native fields.

Disposition of this gate: `FAIL_CLOSED_SOURCE_PRIMARY_REPLAY_UNAVAILABLE`.

## 6. Native restore-direction defect

This is the decisive second incomplete gate.

STATEQ03 reports that the revision-53 `Init.for` promotion from result state to accepted/start state lies outside the first-step conditional and can therefore execute on the first resumed active timestep.

STATEQ04 does not compile or execute frozen `Init.for`. Its driver explicitly labels `stageB-nativebad` as an emulation of the reported revision-53 first resumed `Init` promotion when `RsCoMp` has no restart representation. The bad control sets the result alias to zero and then copies result to accepted state.

That control is scientifically useful: it establishes that the alleged direction can destroy a valid accepted state and causes deterministic divergence. It does not independently prove that frozen `Init.for` contains that direction, that it executes at that exact lifecycle point, or that native `RsCoMp*` lacks any other valid initialization before the promotion.

Disposition of this gate: `FAIL_CLOSED_NATIVE_INIT_PRIMARY_REPLAY_UNAVAILABLE`.

## 7. Remediation transaction

The proposed transaction is independently supported at kernel-contract level:

Checkpoint:

`accepted CoMp* state`

Restore:

`checkpoint -> CoMp*`

`CoMp* -> RsCoMp*`

then resume the normal legacy lifecycle.

This is the minimal coherent direction because the accepted coordinate is the checkpoint owner while the result coordinate is initialized only as a runtime alias. It does not persist workspace, does not create dual physical-state ownership, covers both macropore domains, and naturally extends from four P-off to six P-on species. It remains scientifically conditional on restoring the exactly compatible hydrologic state.

A writer-only correction is insufficient if native first-resumed lifecycle promotion can still overwrite the loaded accepted state. A restore-direction-only correction is insufficient if the accepted macropore concentration is never serialized. Therefore serialization and restore bootstrap form one atomic correction identity:

`COMPLETE_ACCEPTED_MACROPORE_SOLUTE_STATE_TRANSFER_ACROSS_RESTART_BOUNDARY`

## 8. Executable evidence review

STATEQ04 was inspected at runner, driver, and persisted-result level rather than accepting its JSON conclusion alone.

Verified:

- runner verifies frozen source archive SHA-256 before extraction;
- `MAPOTRANSPORT.FOR`, `Transsub.for`, and `Param.inc` are hash-verified frozen members;
- only build/harness adaptations are a stable file copy, case-insensitive `param.inc` alias, and the purpose-built driver;
- six species are run: DOM, DON, NH4, NO3, DOP, PO4;
- split occurs after accepted step 5;
- stage B is launched through separate subprocess invocations, hence a fresh process;
- comparison is raw byte equality: `EXACT_BYTEWISE_NO_TOLERANCE`;
- no numerical tolerance is introduced;
- correct restore matches the continuous suffix byte-for-byte for every species;
- native-bad emulation diverges for every species;
- dropping domain 1 diverges for every species;
- dropping domain 2 diverges for every species;
- warning files are zero length in the recorded kernel runs.

The two domain-drop controls are strong causal evidence that both domain coordinates are continuation-relevant persistent solute state at the kernel level.

The existing STATEQ04 GitHub Actions run `34536146367` is green, but its workflow validates persisted evidence and syntax-checks the harness. Because the frozen archive is not distributed in the public repository, that CI run is not a fresh independent kernel re-execution and is not treated as such here.

## 9. Evidence boundary

STATEQ04 proves a frozen-source-kernel restart-remediation contract for `MAPOTRANSPORT`. It does not prove complete-model active production split equivalence.

MP02 separately proves B1 complete-model active-macropore reachability for the six solute families and two-domain activation. It did not execute a complete-model continuous-versus-restart split because persistent state was incomplete.

The combination therefore supports:

- complete-model reachability of the active macropore path;
- kernel-level causal necessity of both macropore solute domain coordinates;
- kernel-level exactness of the proposed accepted-state restore transaction.

It does not support:

- a whole-model production restart-equivalence claim;
- historical active-macropore behaviour;
- historical tolerance or historical output fidelity.

No kernel PASS is promoted to Tier-D/production evidence.

## 10. Historical uncertainty

The frozen nine-case testbank was rechecked. Every case has `macropore_option = 0`. No qualified active-macropore historical B2 reference was found.

Therefore:

`historical revision-53 active-macropore restart behaviour = UNKNOWN`

GOV03 explicitly permits later claim-scoped B3 consideration under historical uncertainty after reasonable B2 acquisition is exhausted, while prohibiting fabrication of historical behaviour. This route is compatible with a scientifically necessary state/restart correction if the TCD-specific Tier-C gates are otherwise satisfied.

## 11. GOV04 tier

Risk tier remains `GOV04_TIER_C`.

The strictest applicable triggers are directly present: persistent physical-state ownership, initialization semantics, restart serialization, restore direction, accepted-boundary checkpoint lifecycle, and cold-start/restart discrimination. The prospective source patch size is irrelevant to the risk classification. No downgrade is justified.

## 12. TCD-025 boundary

TCD-025 is not executed or composed here.

TCD-025 concerns the public/main macropore conservation ledger. A later TCD-025 Class-A ledger-readiness analysis needs a trusted identity for the macropore beginning/end storage it proposes to observe. TCD-031, if independently passed and later admitted, would provide the solute-state storage identity needed for that separate analysis.

Because B3B10R is not PASS, TCD-025 may not yet consume TCD-031 as a certified state dependency. Purely exploratory TCD-025 analysis that makes no TCD-031 PASS/admission assumption is logically separable, but formal ledger-readiness advancement remains blocked on the TCD-031 review gate.

## 13. Final fail-closed disposition

Overall disposition:

`REMEDIATION_REQUIRED`

The following gates are sufficiently supported for later targeted reuse if their exact pins remain immutable and unsuperseded:

- GOV04 Tier C classification;
- two-domain continuation relevance at frozen kernel level;
- six-species kernel coverage including conditional phosphorus families;
- exact/no-tolerance split comparison;
- correct restore transaction at kernel-contract level;
- causal native-bad emulation;
- causal domain-1 and domain-2 drop controls;
- evidence-boundary discipline;
- historical behaviour remains `UNKNOWN`;
- atomic correction identity joining serialization and restore bootstrap.

The following gates are not independently closed:

1. direct primary-source verification of native `mapoinput.for` / `Output_Init.for` / `Animo.for` serialization and call-surface behaviour;
2. direct primary-source verification of native `Init.for` restore/promotion direction, timing, and pre-promotion `RsCoMp*` initialization state;
3. exact native source-level producer/consumer confirmation for the complete named ownership list, including `AvCoMp*`, `AvCoML*`, `MpReKo*`, `ItRec`, and the hydrology-owned `SrWaMp*` family.

These are provenance/evidence deficiencies, not a contradiction of STATEQ03/04.

### Required remediation

Do not reopen the STATEQ04 kernel qualification merely to repeat the already adequate kernel test.

Open a narrowly scoped source-evidence remediation/extension for TCD-031 that makes the exact frozen revision-53 source facts independently reviewable without violating the source redistribution constraint. Acceptable evidence must be mechanically tied to the frozen archive/member hashes and expose enough license-safe source-probe output or controlled source slices to verify the loader, writer, `Output_Init` call surface, `Init.for` promotion direction/timing, pre-promotion result-alias initialization, and named ownership roles.

After that remediation, run a targeted independent B3B10R re-review of the failed source/provenance gates plus regression guards. GOV04 permits targeted re-review because the failure is evidence/provenance insufficiency and the other PASS gates can remain immutable and scope-identical.

Whole-model active production split evidence is not required to repair this specific independent-source blocker or to establish the narrow kernel-level atomic correction identity. It remains required before any later whole-model production restart-equivalence or migration claim.

No atomic B3 admission workunit may be opened from this review result.

# ANIMO-STATEQ03 TCD-031 active macropore restart-state qualification

Status: `FAIL_CLOSED_TCD031_NATIVE_ACTIVE_MACROPORE_RESTART_STATE_INCOMPLETE`

Branch: `work/animo-stateq03-tcd031-macropore-persistent-solute-state`

Base aggregate authority: `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`.

This workunit qualifies state ownership and native restart sufficiency only. It does not implement a production correction, admit canonical STATE, compose TCD-025, enter B4, or update central regie.

## 1. Live authority and routing recheck

The branch was created only after checking that no dedicated `STATEQ03` or `TCD-031` branch existed and no TCD-031 GitHub issue was present. The canonical discrepancy register already contains TCD-031 as open/not started.

Pinned authorities used here:

- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-MP01@7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- `ANIMO-MP02@6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- `ANIMO-STATEQ01@4adae99576eb56978da71f7c8a250e4445fd3bc4`;
- `ANIMO-STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`;
- `ANIMO-MASSQ02@56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`;
- canonical routing checked from `B3I03@814ea660d367494432beb63ea78298d1f6cd73d7` through `B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`;
- frozen B0 retention `@a818b5a37b80ed92aded0b9c404990d356eb2300`.

Frozen identities were independently rechecked locally: revision-53 source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`; testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

GOV04 classifies restart/cold-start discrimination, canonical state ownership and missing/redefined state as Tier C surfaces. B3Q01 Class C covers missing or incomplete physical/restart state models. TCD-031 is therefore retained as GOV04 Tier C and B3 Class C. Source-edit size is irrelevant to that classification.

## 2. Complete persistent macropore solute owner

Revision 53 represents two macropore domains: domain 1 Main Bypass Flow and domain 2 Internal Catchment. For each enabled solute, the independent accepted-boundary coordinate is the domain concentration `CoMpX(domain)` paired with externally owned domain water storage `SrWaMpOld(domain)`. The conserved beginning mass is `SrWaMpOld * CoMpX`. The current interval produces `RsCoMpX(domain)` and the conserved end mass is `SrWaMp * RsCoMpX`.

For C/N operation the complete ANIMO-owned accepted solute state is eight scalars:

`CoMpDiorMa(1:2)`, `CoMpDiorNi(1:2)`, `CoMpNh(1:2)`, `CoMpNi(1:2)`.

With P enabled, four more scalars are mandatory:

`CoMpDiorPo(1:2)`, `CoMpPo(1:2)`.

Thus the P-active complete state is twelve scalar concentration coordinates. There is no independent layer-resolved macropore solute concentration coordinate in the inspected source. Layer-resolved averages and transfer rates are current-step workspace.

The result aliases `RsCoMp*` are not a second physical stock. They are the end-of-current-interval representation of the same owner and become accepted only after the interval is accepted. A checkpoint taken at that accepted boundary must capture the accepted end values without treating a provisional result as accepted state.

The machine-readable map records meaning, units, owner, producer, consumers, update frequency, serialization, restore direction, reconstruction status and matrix/hydrology dependencies for these owner aliases and the relevant workspace/diagnostic variables.

## 3. Classification by lifecycle, not storage location

`PERSISTENT_STATE`: all six enabled `CoMp*` concentration families across two domains, with corresponding `RsCoMp*` result aliases for the same physical owner. The external water coordinates `SrWaMpOld/SrWaMp` and layer-resolved hydrology are persistent external-owner references, not ANIMO solute ownership.

`EPHEMERAL_WORKSPACE`: `AvCoMp*`, `AvCoML*` and the generic `MpReKo/MpReKoLn` transfer workspace. These values are produced inside the current transport interval and can be recomputed after restore from accepted owner state plus the rebound current hydrology/frame.

`DERIVED_DIAGNOSTIC`: `ItRec`, which records transport-iteration counts and is not a physical continuation coordinate.

`DETERMINISTIC_RECONSTRUCTION`: no required macropore solute owner qualifies globally for this class. The zero-old-storage branch in `MAPOTRANSPORT` is a conditional process branch, not a general restart reconstruction law.

The decisive source identity is the specialized balance itself: for nonzero stored macropore water, old mass contains `SrWaMpOld * CoMp`. The same matrix state and hydrology can therefore coexist with different macropore solute masses. Reconstructing `CoMp` from matrix state, hydrology or zero would erase an independent degree of freedom.

## 4. Native restart serialization is incomplete

The input side exists. `input1.for:3458-3465` calls `Mapoinput` with `Nupa=4`; `mapoinput.for:116-183` reads `>MPnitr:`, `>MPorgs:` and, when P is enabled, `>MPphos:` into both domain concentrations.

The output side does not exist as an active path. `Output_Init.for:137-153` contains the macropore records only as commented code. The corresponding macropore arguments in the final `Output_Init` call are also commented in `Animo.for:1099-1109`. MP02 independently observed that an active complete-case `Output/initial.out` contained none of those three record groups.

For P-off, revision 53 therefore serializes 0 of 8 required active-macropore solute scalar coordinates. For P-on it serializes 0 of 12.

## 5. Restore direction has a second independent defect

Serialization omission is not the only blocker.

`Init.for` states that ordinary result-to-start promotion is skipped for the first timestep, but the macropore block at `Init.for:501-532` sits outside that first-step conditional. Whenever `IoptMp=1`, it assigns all `CoMp* = RsCoMp*` and `SrWaMpOld = SrWaMp`, including on the first timestep.

The restart loader has already populated `CoMp*` from `INITIAL.INP`, but no native restart representation or initialization of the corresponding `RsCoMp*` result aliases was found before this promotion. Consequently, a loaded accepted macropore concentration is not protected as the accepted start coordinate on the first resumed step.

This finding is stronger than a formatting omission. A future correction contract must define both checkpoint projection and restore transaction direction. Simply uncommenting the legacy writer would not, by itself, prove a scientifically continuous restart.

## 6. Executable split-run decision

All nine frozen B0 testbank cases were scanned. Every active `GENERAL.INP` has `MacroPoreOption=0`; there is no naturally active macropore case.

MP02 remains the exact pinned complete-case active B1 evidence. Its synthetic P-active CranGrass descendants completed six whole-model runs of 2922 timesteps, and the five positive labels exercised all six solute transport routes without specialized macropore balance warnings. MP02 also confirmed the missing restart records and explicitly did not execute an active continuous-versus-split test.

The frozen GNU diagnostic build was independently reconstructed for STATEQ03. It again selects 58 legacy units and 14 syntax compatibility substitutions and yields executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`, exactly matching MP02.

A native active split discriminator is nevertheless blocked before its first scientific comparison. A split checkpoint cannot contain the required macropore solute state, and even externally supplying those input records would not establish the native restore direction because first-step `Init` overwrites the loaded accepted aliases.

Therefore:

- scientifically active split time: not reached as a native qualified boundary;
- exact checkpoint inventory: fail, 0/8 C/N or 0/12 C/N/P solute coordinates serialized;
- first post-restore comparison: not reached;
- bounded continuation comparison: not reached;
- species-separated comparisons: not reached;
- tolerance: none introduced.

This is not recorded as a numerical mismatch. It is a fail-before-comparison state-contract failure.

Supporting negative evidence remains useful but narrower: MP02's `NO-MP` complete case passes with macropores inactive, and STATEQ02 proves exact bitwise continuous-versus-split continuation for a restricted core profile that explicitly excludes macropores. Neither is promoted to an active TCD-031 split-run pass.

## 7. TCD-025 dependency decision

STATEQ03 does remove one TCD-025 design ambiguity at source/ownership level. The macropore solute storage owner is now explicit per species:

`begin storage = sum_domain(SrWaMpOld(domain) * CoMpX(domain))`

`end storage = sum_domain(SrWaMp(domain) * RsCoMpX(domain))`

Water storage is externally hydrology-owned; solute concentration and the resulting solute-mass identity belong to the ANIMO macropore-solute owner. Public balance arrays are observers and cannot substitute for those owners. This is consistent with MASSQ02.

If TCD-031 later passes executable restart qualification, the following TCD-025 prerequisites are already defined: complete solute state inventory, accepted-boundary start/end storage identity, units, species mapping and domain ownership needed to source public ledger storage terms.

TCD-025 is not opened for Class-A ledger readiness here. TCD-031 itself did not pass, and TCD-025 still has independent blockers: direct-drain/Dra4 integration, absent historical active B2 reference, future Class-A non-interference evidence, and the applicable independent review/admission gates. No TCD-025 correction or composition is performed.

## 8. Fail-closed result and next admissible handoff

The already qualified MP01/MP02 ownership and activation evidence is preserved. The exact missing contracts are now localized:

1. persist every enabled accepted macropore solute concentration in both domains at the accepted checkpoint boundary;
2. define a fail-before-mutate restore transaction that restores `CoMp*` as accepted state and does not overwrite it from an unrestored result alias on the first resumed timestep;
3. after those contracts exist, run a P-active synthetic complete-case split at a scientifically active macropore time, compare the first restored accepted state and a bounded future trajectory, and keep species controls separate;
4. because this is GOV04 Tier C, require genuinely independent second-line review before atomic B3 admission.

Current decisions:

`TCD-031 atomic Tier-C B3 readiness = NOT_READY`

`TCD-025 Class-A ledger readiness = NOT_OPENED`

`canonical STATE admission = NONE`

`production patch = NONE`

Final status:

`FAIL_CLOSED_TCD031_NATIVE_ACTIVE_MACROPORE_RESTART_STATE_INCOMPLETE`

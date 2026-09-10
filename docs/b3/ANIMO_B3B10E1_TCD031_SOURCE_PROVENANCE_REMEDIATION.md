# ANIMO-B3B10E1: TCD-031 license-safe frozen-source provenance remediation

## Scope

This workunit repairs only the source/provenance evidence blocker recorded by `ANIMO-B3B10R@36aad892cac546105dfec0fe43aa34a18e23bcad`. It does not patch production source, reopen STATEQ04, admit TCD-031, modify the canonical TCD register, compose TCD-025, update RG05, enter B4, introduce a tolerance, or infer historical intent.

Disposition after deterministic local replay and package validation:

`QUALIFIED_SOURCE_PROVENANCE_REMEDIATION_READY_FOR_TARGETED_INDEPENDENT_REREVIEW`

This status means only that the failed B3B10R source-level gates can now be targeted by an independent reviewer. B3B10R itself remains `COMPLETE_FAIL_CLOSED / REMEDIATION_REQUIRED` until that separate review is completed.

## Frozen identity and license boundary

The only source authority used is local frozen archive `ANIMO_4.1.5.53(3).zip`, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. The frozen testbank remains `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` and is not modified.

No frozen source file and no source archive is committed. The repository stores member hashes, source-member names, line-number ranges, normalized slice hashes, semantic probe results, an archive-wide source-member hash index, and a deterministic replay tool. This deliberately exposes what was checked without redistributing the underlying source text.

A reviewer who lawfully possesses the exact archive can run the generator and byte-compare the generated JSON files with the committed hashes. A reviewer without that archive can validate package integrity and the cryptographic bindings, but cannot honestly claim independent regeneration of the frozen source evidence.

## Recomputed relevant source-member hashes

The local replay recomputed and matched the expected identities for `mapoinput.for`, `Init.for`, `Output_Init.for`, `Animo.for`, `MAPOTRANSPORT.FOR`, `Transca.for`, `Transgen.for`, `input1.for`, and `Hydro_detailed.for`. Additional members needed for the ownership reconstruction, including `Animo.inc`, `Inicalc.for`, `MAPOHYDRO.FOR`, `TRANSPORT.FOR`, and `resp_miner.for`, are also bound in the manifest.

## Repaired source gates

`SRC-MAPO-001` through `004` bind the three macropore INITIAL.INP labels to their CoMp destinations, both domains, and the phosphorus condition. `SRC-OUTINIT-001` and `002` bind the inactive native macropore Output_Init signature/writer route. `SRC-ANIMO-001` binds the active Output_Init call surface and its inactive macropore continuation.

`SRC-INIT-001` and `002` bind the lifecycle position and direction `CoMp <- RsCoMp`. The macropore promotion block occurs after and outside the first-timestep special-case guard, so it also executes at the first active timestep when macropores are enabled.

`SRC-RSCOMP-001` and `002` address the previously missing producer/initialization evidence. Across the complete frozen Fortran/include scan there is no direct family-specific `RsCoMp*` assignment and no active RsCoMp reference in the native startup input path. End-state production occurs through the generic `RsCoMp` dummy in `MPTRANSP`, reached by transport calls after `Init`. The initial macropore concentration input instead loads CoMp. Therefore the frozen source provides no native pre-promotion RsCoMp restore on the first active timestep. This supports the previously stated overwrite hazard and does not contradict STATEQ04.

The ownership map covers CoMpDiorMa, CoMpDiorNi, CoMpNh, CoMpNi, CoMpDiorPo, CoMpPo, RsCoMp*, AvCoMp*, AvCoML*, MpReKo*, ItRec, SrWaMpOld, SrWaMp, SrWaMpCp, and SrWaMpCpOld. It records declaration source, producers, consumers, timestep role, checkpoint relevance, classification, and evidence references.

## Replay and validation

Generate the source evidence from a lawful local copy:

```text
python tools/b3b10e1/generate_tcd031_source_provenance.py /path/to/ANIMO_4.1.5.53(3).zip --output-dir /tmp/b3b10e1
```

Then compare the generated artifact SHA-256 values with `ANIMO-B3B10E1_MANIFEST.json`. The package validator can additionally perform that replay when `--archive` is supplied. CI intentionally runs without the licensed archive and therefore validates only the committed evidence package, bindings, failed-gate coverage, ownership completeness, counts, scope guards, and changed-path boundary. CI success must not be reported as a scientific review PASS.

## Live authority snapshot at workunit opening

The dedicated B3B10E1 branch name was free and no later equivalent TCD-031 evidence-remediation workunit was found. The review branch remained exactly `ANIMO-B3B10R@36aad892cac546105dfec0fe43aa34a18e23bcad`, so this is the exact starting head.

The current green aggregate authority had advanced to `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`, with exact-head workflow run `34537563430` concluded `success`. The authority pins relevant to this remediation remained unchanged: GOV04 `1bbe4c211197590f346803106e45dca5faae79fc`, GOV03 `cbd262bdabe92923113b7326f2f42822ce9a971c`, B3Q01 `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`, MP01 `7b5979dd6301b9d55d23e8c22948a0dba24b229b`, MP02 `6b0f2e7470f13baeb6612b0bddb662a497dea528`, STATEQ03 `10c50e65d1369d5f3b26736c4b12d3a482379eb5`, STATEQ04 `ef9a5998cafae433deeba701a8e9a8a08eacc92f`, B3B10 `eccba6712f65455161d05fa9cdf6aa142f823dd4`, MASSQ02 `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`, B3I07 `54679c7555a963133dfd686648af334f479c5808`, and frozen-B0 retention `a818b5a37b80ed92aded0b9c404990d356eb2300`.

No dedicated TCD-031 issue was present. The only search hit among pull requests was historical merged PR #19, whose TCD-031 role is canonical routing rather than independent source review. No B3B10R pull request or later review result was found at opening.

## Boundary after remediation

STATEQ04 reopening is not required. A new whole-model active split was not needed to repair this evidence blocker and was not run. Whole-model production restart equivalence remains required before any production or migration claim. Atomic B3 admission remains blocked until a genuinely independent GOV04 Tier-C rereview passes TCD-031. TCD-025 remains formally blocked and no ledger or composition change is made here.

# ANIMO testcase lineage and evidence inventory

Work unit: `ANIMO-TQ01`

Evidence class: preparatory B0/B1 qualification evidence. No B2 reference is admitted.

## Evidence boundary

The nine testcase directories are immutable members of the frozen `ANIMO_testbank.zip` B0 artifact. Their presence proves historical input provenance only. Eight cases are parser-compatible with the supplied revision-53 source under the already qualified GNU diagnostic reconstruction and complete reproducibly; this is B1 observation, not historical reference. `GHGMais` is structurally incompatible with the supplied revision-53 input contract.

`TESTCASE_MEMBER_HASHES.csv` records the SHA-256 identity of every active steering-referenced input member used to define the canonical case input set. Auxiliary variants, runner files and output-like members remain B0 archive members but are not silently promoted to the canonical executed input set. The `input_set_sha256` below is a deterministic fingerprint of that active steering-referenced input set only.

## Case inventory

| case | active input-set SHA-256 | steering | lineage vs rev53 | hydrology | crop | C/N/P | GHG | MP | P sorption | management reachability | B1 | output observation | discrepancy relevance |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|
| `CranGrass` | `9513869cdb4cc853428227cac18c6584eb26187a04cd5d7720a395bbd07039d3` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `Input/swatre.unf` | internal, crop id 6, grassland in supplied case comments | C=yes, N=yes, P=yes | 0 | 0 | fast Langmuir Optcxfa=2/Ncxfa=1; slow Freundlich Optcxsl=3/Ncxsl=3; Optpr=0 | additions/fertilizer/manure route; top/surface reservoir route; no plough event observed in B1 | successful reproducible diagnostic run | 32 generated files; bundle `ed8122c66111c1c4e9404c062f82315fc4a2373ad89de60b5513cc9260724920` | TCD-014 PO4 initialization/state-consistency seam is naturally exposed by this P-active case |
| `CranMais` | `0e0de2816fc62883bff1e8b3febc38e1971587ee81e5286d9e693478394e3bcf` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `Input/swatre.unf` | internal, crop id 2, maize in supplied case comments/name | C=yes, N=yes, P=no | 0 | 0 | P off | additions/fertilizer/manure route; top/surface reservoir route; 9 plough events observed in B1 | successful reproducible diagnostic run | 24 generated files; bundle `6b2f3cd80d11af3ba4bd2e7a87fa805d04f02470f8edce90e609ccbdbf83aef7` | natural plough reachability; PREP10 stable-DOM plough-accumulator observer is non-discriminating in this case |
| `GHGMais` | `27bfd0249cdc5a1975255a99fa68e42006fb6a8027c2f4f3254233832ecf7a62` | `Animo41` | `LINEAGE_UNCERTAIN_CONTRACT_MISMATCH` | Iwa=2, `Input/result.bun` | external, crop id 2, maize in supplied case comments/name | C=yes, N=yes, P=no | 1 | 0 | P off | additions/fertilizer/manure route; top/surface reservoir route; plough not evaluated because run is lineage-blocked | blocked at input contract | none from successful B1 | TCD-013 GHG source/testcase contract-lineage mismatch; no revision-53 GHG behavioural attribution allowed |
| `GrassPeat` | `4e2db1b3ded59c5258bddf6571c8eb7e6a9bd5d3560128fc4cdd23ad15a5e8ad` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `Input/swatre.unf` | external, crop id 5, external crop configuration | C=yes, N=yes, P=yes | 0 | 0 | fast Langmuir Optcxfa=2/Ncxfa=1; slow Freundlich Optcxsl=3/Ncxsl=3; Optpr=0 | additions/fertilizer/manure route; top/surface reservoir route; no plough event observed in B1 | successful reproducible diagnostic run | 61 generated files; bundle `171b6e343d4a80e9ae686f07df7ca6cd0e62450dd19aa146bba48f2793581e80` | PREP10 naturally observes nonzero plant restart state relevant to TCD-033/TCD-034; split-run equivalence is still missing |
| `LWKM_gras_1040.2021.2045` | `efa71c5725afd76beca88bd7c91957d29d1bffb47cb11255ebe021f8f3c79553` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `input/SWATRE.UNF` | external, crop id 5, external crop configuration | C=yes, N=yes, P=yes | 0 | 0 | fast Langmuir Optcxfa=2/Ncxfa=1; slow Freundlich Optcxsl=3/Ncxsl=3; Optpr=0 | additions/fertilizer/manure route; top/surface reservoir route; 4 plough events observed in B1 | successful reproducible diagnostic run | 55 generated files; bundle `80794ca2ff521d4e6009a2b46c1f533844a2d0029de7c0f64663b0b403f2be4c` | natural relevance to TCD-017/018/019/027/031 and restart findings; also parent B0 case for separate synthetic TCD-024/028/029/030 probes |
| `Puitmijn_Cranendonck_60` | `7d977937830f494a9e1ebb1130ccc7c5029e4c52641cf7e122247081d9153856` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `input/swap.bun` | internal, crop id 6, grassland in supplied case comments | C=yes, N=yes, P=yes | 0 | 0 | fast Langmuir Optcxfa=2/Ncxfa=1; slow Freundlich Optcxsl=3/Ncxsl=3; Optpr=0 | additions/fertilizer/manure route; top/surface reservoir route; no plough event observed in B1 | successful reproducible diagnostic run | 77 generated files; bundle `e57972659314b7c7ef41f9cf39982a12b0dc94dd6cf91906938432754190a989` | TCD-016 NH4 dry-down and TCD-023 stable-DOM P partition have natural case-specific evidence here |
| `RuurloGrass` | `3dfec0721b7f6817d8eeb48d87c963d9665bcd3e55b2c4f990d373d1c8396941` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `Input/swatre.unf` | internal, crop id 6, grassland in supplied case comments | C=yes, N=yes, P=no | 0 | 0 | P off | additions/fertilizer/manure route; top/surface reservoir route; no plough event observed in B1 | successful reproducible diagnostic run | 73 generated files; bundle `df0ec1c5995272e8f663762e4432c2ccf13480f03527cde956f506363d2eefd8` | output selection includes GHG-named fields while GHG is disabled, directly illustrating that output presence is not process coverage |
| `STONE_akk_0006.2001.2015` | `b9a1dfbb53c34aca69ec5eea76f91293b91849a7dc8baf9b3698c4eff8849747` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `input/SWATRE.UNF` | external, crop id 3, arable configuration; exact crop semantics not inferred beyond supplied files | C=yes, N=yes, P=yes | 0 | 0 | fast Langmuir Optcxfa=2/Ncxfa=1; slow Freundlich Optcxsl=3/Ncxsl=3; Optpr=0 | additions/fertilizer/manure route; top/surface reservoir route; 15 plough events observed in B1 | successful reproducible diagnostic run | 45 generated files; bundle `bed78a0ca44b5cad027b864025d37a1324521357f9f4ccce8e9111960de9fcc6` | natural plough reachability plus PREP10 nonzero plant restart state relevant to TCD-033/TCD-034 |
| `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA` | `3ea8824109ffd64102d6e43a0d1fd9171cdd4a679e9569f7422be171903aee6e` | `Animo41` | `REV53_PARSER_COMPATIBLE_LINEAGE_NOT_PROVEN` | Iwa=2, `Input/Swap.bun` | internal, management selects crop record 3 and supplied `Plant.INP` defines `>crop03:` with `CN=6`, therefore the ANIMO grassland branch is selected despite the folder name | C=yes, N=yes, P=yes | 0 | 0 | fast Langmuir Optcxfa=2/Ncxfa=1; slow Freundlich Optcxsl=3/Ncxsl=3; Optpr=0 | additions/fertilizer/manure route; top/surface reservoir route; 3 plough events observed in B1 | successful reproducible diagnostic run | 16 generated files; bundle `456c73e1d5a2c4d6f0c00b442f589bfe75fa8cc9ae1f109bc5851bb3658f707e` | natural plough reachability plus PREP10 actual plant restart state relevant to TCD-033; folder naming is not used as physics evidence |

## Reachability interpretation

Coverage is deliberately split into four questions:

1. **Configured**: the B0 input selects an option or contains the relevant state/parameter family.
2. **Reached**: source dispatch plus a successful B1 execution demonstrates that the route is entered.
3. **Mutated**: a dedicated observer or causal probe demonstrates non-zero state change. This is not inferred from successful termination.
4. **Observed in output**: a configured output selector or generated file exists. Output presence is not proof that the underlying process had a non-zero rate.

In `PROCESS_COVERAGE_MATRIX.csv`, `B1_DIAGNOSTIC_ACTIVE` means route reachability is supported for the natural case. It does **not** mean every internal rate or flux is proven non-zero. `NATURAL_B0_PRESENT_NOT_REACHED` is used where the input/hydrology interface contains the feature but no process-specific non-zero reachability/mutation evidence has been established.

The source main loop unconditionally invokes the major transformation and transport machinery (`Rates1`, `Rates2`, dissolved-organic transport, NH4/NO3 transport and `Denitr`) during successful timesteps; P transport is guarded by `Ipo=1`, GHG by `IoptGHG>=1`, and macropore hydrology/transport by `Ioptmp=1`. That gives route-level evidence, not automatic non-zero mutation evidence.

## Natural plough reachability

Existing non-intrusive B1 observers establish 31 actual plough events in four frozen cases: CranMais 9, LWKM 4, STONE 15, and Zuiderzeeland 3. The other four successful cases show zero plough events. GHGMais is excluded because it does not pass the revision-53 input contract.

This matters for two separate findings. First, stable-DOM plough accumulator state was zero at all 31 observed natural events under the current GNU diagnostic, so those natural cases are non-discriminating for that source defect. Second, LWKM contains non-zero heterogeneous slow-sorbed P at natural plough events, so slow-sorption tillage policy is naturally trajectory-relevant.

## P sorption coverage

Every supplied P-active canonical case selects fast equilibrium Langmuir sorption (`Optcxfa=2`) and slow non-equilibrium Freundlich sorption (`Optcxsl=3`, three sites). Therefore:

- fast Langmuir has natural B0/B1 route coverage;
- slow Freundlich has natural B0/B1 route coverage;
- slow Langmuir (`Optcxsl=2`) has **no natural B0 case**;
- slow linear (`Optcxsl=1`) also has no natural B0 case;
- helper branches for non-admitted fast equilibrium forms do not establish supported historical options.

## Restart evidence

The revision-53 input/output representation exposes restart surfaces, and two supplied directories also contain `initial.out`-like members. Neither fact is a natural split-run qualification. Existing restart work has source-bound and diagnostic causal evidence for plant-uptake state and macropore writer gaps, but no independent B2 continuous-versus-split reference. `restart_behaviour` therefore remains preparatory and unqualified.

## Ordered qualification gaps

The machine-readable ordered register is `docs/testing/QUALIFICATION_GAP_REGISTER.csv`. The highest-priority gaps remain:

1. `REFERENCE_OUTPUT_MISSING`: no independently trusted executable-linked B2 output is admitted.
2. `NATURAL_CASE_LINEAGE_UNCERTAIN`: GHGMais is the only GHG-active supplied case and is incompatible with the supplied revision-53 parser/material contract.
3. `NO_NATURAL_B0_COVERAGE`: active macropores, slow Langmuir and other intended/support-candidate routes have no supplied natural case.
4. `OPTION_PRESENT_BUT_UNEXERCISED`: several parser/source paths or nonzero state mutations are not established by the natural cases.
5. `REFERENCE_SPLIT_RUN_MISSING`: restart semantics are not qualified by an independent continuous-versus-split historical run.
6. `LINEAGE_COMPATIBLE_NOT_PROVEN`: successful revision-53 parsing of eight cases establishes compatibility, not that each case was originally authored for revision 53.

## Qualification consequence

The supplied testbank is useful as a heterogeneous B0/B1 evidence collection, not as one uniform scientific reference suite. It is suitable for path qualification preparation and for selecting future B2/B3 cases. It is not yet a historical behavioural oracle.

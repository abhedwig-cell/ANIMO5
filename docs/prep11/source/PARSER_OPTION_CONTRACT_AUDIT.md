# ANIMO-PREP09 — Parser-exposed option contract audit

Status: `QUALIFIED_SOURCE_AND_DIAGNOSTIC_OPTION_CONTRACT_AUDIT_REFERENCE_ADMISSION_BLOCKED`.

## Purpose

PREP08 showed that an option accepted by a parser is not necessarily implemented coherently across all participating process modules. PREP09 therefore audits selected revision-53 parser-visible option ranges against:

1. source dispatch;
2. supplied-testbank coverage;
3. the supplied ANIMO 4.0 user-guide contract where applicable;
4. controlled diagnostic behaviour for suspicious option values.

The audit does not change frozen source, testbank or production physics.

## Frozen identity

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Static audit tooling is persisted as `tools/audit_option_contracts.py`. It verifies both archive hashes before inspecting source/testbank content.

The focused static audit passes all six fail-closed checks.

A wider option inventory is persisted in `docs/prep09/OPTION_CONTRACT_MATRIX.csv`.

## 1. Existing option-contract findings remain visible

The broader matrix does not renumber previously established discrepancies:

- `SulphateSimulation/IoptSul=1` remains TCD-022 because the parser exposes the option but no sulphate process implementation was found;
- `MacroPoreOption/Ioptmp=1` remains linked to TCD-007 and TCD-025 because process code exists but supplied active coverage is absent and the public/main ledger control volume is incomplete;
- `Ncxfa=2..3` remains TCD-029, now dynamically confirmed as a management mass-creation defect;
- `Optcxsl=2` remains TCD-024 because the slow-Langmuir path has a confirmed site-index defect and no natural supplied coverage.

Coverage gaps by themselves are not promoted to defects. For example the separate soil-temperature-file route and precipitation-enabled P route have source branches but no supplied active testcase.

## 2. TCD-030 — AerationModel option 2 aliases option 0

### Published 4.0 contract

The supplied ANIMO 4.0 User's Guide documents only:

```text
Ioptae = 0: original aeration module / oxygen-diffusion concept
Ioptae = 1: SONICG moisture-response concept
```

with range `0..1`.

Revision 53 keeps that `0..1` check for the `AnimoVersion=40` parser route, but the `AnimoVersion=41` route reads `AerationModel` and explicitly accepts:

```fortran
Call Checkint(Uoer,Error,Label,'Ioptae',Ioptae,0,2)
```

Option 2 is therefore a later interface extension relative to the supplied 4.0 documentation.

### Supplied testbank advertises distinct option-2 semantics

All 12 supplied modern `AerationModel` records carry the same explanatory comment:

```text
0=diffusion model; 1=WFPS concept acording to SONICG/NITDEN; 2= option + adj. for denitrification
```

Observed configured values are:

```text
AerationModel=0: 8 records
AerationModel=1: 4 records
AerationModel=2: 0 records
```

Thus the delivered input contract advertises a third semantic mode but the supplied natural testbank never activates it.

### Source dispatch

The revision-53 main program does not contain a third aeration dispatch. It partitions the full accepted range into only two branches:

```fortran
If(Ioptae.ne.1) Then
    Call Aeration_original(...)
Else If(Ioptae.eq.1) Then
    Call Aeration_sonicg(...)
End If
```

A source-wide static search finds zero explicit `Ioptae == 2` / `Ioptae .Eq. 2` branches.

The original aeration routine does not receive `Ioptae`, so it cannot distinguish whether it was entered from parser value 0 or 2. Other source uses likewise distinguish only option 1 from non-1 for aeration-specific input/output handling.

Consequently revision-53 source semantics are:

```text
0 -> Aeration_original
1 -> Aeration_sonicg
2 -> Aeration_original
```

not the three-way semantics advertised by the supplied testcase comments.

## 3. Controlled option-0 versus option-2 execution

A diagnostic probe used supplied case `Puitmijn_Cranendonck_60`, which naturally has `AerationModel=0` and runs successfully under the pinned GNU diagnostic contract.

The comparison case changed exactly one scientific input value in the execution copy:

```text
AerationModel=0 -> AerationModel=2
```

No source, hydrology, material, soil, management or initial-state value was changed.

Execution-copy GENERAL hashes:

```text
option 0: cc68eec5936c9b25cf13044b5b5a1b308d243a85828ad296eeb84be8486c72c7
option 2: e700f74a6d67d8965aab05b2cf95efce460a0b93f6dbf602cebf2674e4c33a3f
```

Both executions complete with the normal legacy successful `STOP 100` route using diagnostic executable:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

Across 77 common non-input output files:

```text
raw files differing:        20
normalized files differing:  0
```

Every raw difference is explained by volatile run timestamp/file-creation metadata. After removal of only those declared volatile lines, option 0 and option 2 are identical across all 77 outputs.

This dynamic result is consistent with, and independently supports, the source dispatch proof.

It is not used to infer what option 2 *should* have done. The only supplied statement of intended difference is the testcase comment `option + adj. for denitrification`; revision-specific theory or implementation provenance for that intended adjustment is not available.

## 4. Classification

New discrepancy:

`TCD-030`

Classification:

`CONFIRMED_PARSER_AND_TESTCASE_ADVERTISED_AERATION_OPTION2_SEMANTIC_ALIAS_TO_OPTION0`

This is primarily an interface/feature-contract defect in the supplied revision-53 baseline. It does not demonstrate wrong physics for the exercised values 0 and 1.

The safe ANIMO5 rule is:

```text
AerationModel=2 is NOT_ADMITTED
```

until authoritative intended semantics or a trusted historical implementation is recovered.

Silently mapping legacy option 2 to option 0 in ANIMO5 would preserve the supplied source behaviour but would preserve a behaviour that contradicts the delivered option description. Silently inventing an extra denitrification adjustment would be worse because its equations and calibration are not established.

## 5. Wider option-screen result

The option matrix separates three categories:

1. **exercised and source-distinct**, for example phosphorus-cycle and crop-uptake switches;
2. **source-distinct but coverage-incomplete**, for example `SoilTempFile=1`, `Optpr=1` and `IoptGHG=2`;
3. **contract discrepancies already registered**, including sulphate, macropores, slow Langmuir, multi-site fast sorption and now aeration option 2.

No additional option is classified as a defect solely because a supplied testcase is missing.

`IoptGHG=2` is specifically *not* treated as an alias: revision 53 contains explicit option-2 branches. Its scientific qualification remains blocked by GHG theory/provenance and the GHGMais source-testcase lineage problem.

## 6. Architectural consequence for ANIMO5

Parser validation must not be the definition of feature support.

Every parser-exposed option value needs an explicit support state such as:

```text
UNSUPPORTED
PARSED_NOT_QUALIFIED
QUALIFIED_REFERENCE
QUALIFIED_CORRECTED
```

and an option may become production-supported only when all required process, state, management, restart, ledger and output participants are qualified for that value.

A future typed configuration layer should fail closed on unsupported legacy values instead of allowing semantically aliased or partially implemented modes to enter production silently.

## Gate

`QUALIFIED_PREP09_TCD030_OPTION_ALIAS_CAUSALITY_REFERENCE_ADMISSION_BLOCKED`

Production migration remains `NOT_ADMITTED`.

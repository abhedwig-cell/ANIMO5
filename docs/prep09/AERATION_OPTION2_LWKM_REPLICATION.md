# ANIMO-PREP09 — AerationModel=2 independent LWKM replication

Status: `DIAGNOSTIC_CAUSAL_REPLICATION_SUPPORTS_TCD030_NOT_REFERENCE`.

This evidence strengthens TCD-030 with an independent testcase and an explicit same-case sensitivity control. It does not change frozen source or testbank bytes and does not qualify the GNU build as historical reference behaviour.

## Frozen and execution identities

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

Deterministic GNU diagnostic executable SHA-256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

Case:

`LWKM_gras_1040.2021.2045`

The runtime case copies use only the already documented GNU diagnostic compatibility adaptations. The scientific comparison changes only `AerationModel` among values 0, 1 and 2.

## Three-way causal probe

All three variants complete successfully.

After normalization of only the already declared volatile run timestamps, file-creation timestamps and elapsed CPU seconds, the complete generated output trees compare as follows:

| comparison | common generated files | normalized different files | missing/extra |
|---|---:|---:|---:|
| option 0 vs option 2 | 55 | 0 | 0 |
| option 0 vs option 1 | 55 | 47 | 0 |
| option 1 vs option 2 | 55 | 47 | 0 |

Therefore option 0 and option 2 are behaviourally identical in this second diagnostic case, while option 1 changes most model outputs in exactly the same case.

The sensitivity control is important. It rules out the weak interpretation that the 0-versus-2 equality is merely caused by an aeration-insensitive testcase. The same forcing, soil, management and initial state respond strongly when the parser value is changed to the separately dispatched option 1.

One representative first-year output difference in `AnnualDOMNtotNO3_1mGWL.csv` is:

```text
option 0 / option 2:
1991, 9.3441E-01,4.0462E+01,5.4345E+00,1.9274E+00,3.8702E-02

option 1:
1991, 9.3441E-01,4.1451E+01,6.8866E+00,3.3776E+00,2.7972E-01
```

No tolerance was used to declare 0 and 2 equal. Their normalized output bytes are equal for all 55 generated files.

## Interpretation

Together with the revision-53 dispatch proof:

```text
Ioptae /= 1 -> Aeration_original
Ioptae == 1 -> Aeration_sonicg
```

and the absence of any explicit `Ioptae==2` source branch, this independent replication strengthens the existing TCD-030 classification:

`CONFIRMED_PARSER_AND_TESTCASE_ADVERTISED_AERATION_OPTION2_SEMANTIC_ALIAS_TO_OPTION0`.

No new discrepancy is created. This is replication evidence for TCD-030.

It still does not establish what the advertised `option + adj. for denitrification` semantics should have been. ANIMO5 must therefore continue to fail closed on `AerationModel=2` until authoritative theory or a trusted historical implementation is recovered.

Production migration remains `NOT_ADMITTED`.

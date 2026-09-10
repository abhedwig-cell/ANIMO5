# ANIMO-B3A05 — TCD-037-A1 CH4 Layer Formation Observer Tier-A Readiness

Status at authoring: `READINESS_ASSESSMENT_ONLY`

## Purpose

Qualify whether canonical child atom `TCD-037-A1` is ready for a later atomic B3 disposition/admission decision under GOV04 Tier A. This workunit does not admit corrected legacy behaviour and does not modify production source.

`TCD-037-A1` is the bounded claim that the layer CH4 formation observer in `Outbal_calc` must consume the source-owned accepted-timestep amount

`QPrCH4(Ln) * St`

and may affect only the six CH4/CO2 formation-partition observer fields qualified by RUNTIMEQ03 and SYNQ02.

## Starting authority

Branch base:

`ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`

Required authorities/evidence:

- `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- `ANIMO-SYNQ02@1975eda3586d79033be6af745994bb6181a825fc`
- SYNQ02 exact-final CI run `34538344680`, conclusion `success`
- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`

Frozen B0 source SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Required decisions

B3A05 must answer, fail closed:

1. Is A1 still canonical and atomic under B3I07?
2. Is its exact accounting owner unambiguous?
3. Is the expected-difference contract already frozen and observer-only?
4. Does SYNQ02 satisfy GOV04's qualified-synthetic-activation alternative without being promoted to B2?
5. Are physical state, process flux, restart state and solver/numerical policy outside the change surface?
6. Does GOV03 make the historical-uncertainty route eligible while keeping historical behaviour `UNKNOWN`?
7. Do all GOV04 Tier-A waiver predicates evaluate PASS at readiness scope?
8. Can the current B3Q01 schema represent the canonical child without changing the finalized schema?

## Child-to-B3Q01 schema binding

`B3_DISPOSITION_SCHEMA.json` accepts only top-level TCD identifiers in `tcd_ids` (`^TCD-[0-9]{3}$`). B3Q01 simultaneously states that one atomic record may cite the parent TCD while each admitted correction remains one atomic causal claim.

Therefore a later A1 disposition must retain `tcd_ids: ["TCD-037"]` and carry `TCD-037-A1` as the canonical atomic-child identity in its record identity, scope and class-specific evidence. B3A05 must not widen the B3Q01 schema merely to encode the child suffix.

## Hard boundaries

This workunit must not:

- change frozen B0 source or testcases;
- modify ANIMO production source;
- admit TCD-037, TCD-037-A1 or any sibling;
- grant a final admission-time Tier-A waiver;
- compose A1 with A2, A3, A4 or TCD-032 through TCD-036;
- alter the canonical TCD register;
- reserve a new top-level TCD;
- open B4;
- update RG05H or create a later aggregate;
- claim historical equivalence or B2 evidence.

## Allowed outcome

If every readiness predicate passes, the strongest result is:

`QUALIFIED_TCD037_A1_TIER_A_ADMISSION_READINESS_WAIVER_PREDICATE_PASS_NO_ADMISSION`

The next atomic route is then a separate admission/disposition decision, proposed as `ANIMO-B3D21`, which must recheck all live authorities and the Tier-A predicate before any waiver or admission is issued.
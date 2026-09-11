# TCD-037-A3 independent synthetic activation qualification

Work unit: `ANIMO-SYNQ04`

Target: `TCD-037-A3`

## Purpose

Independently qualify purpose-built synthetic activation for the exact A3 accounting observer claim. This is B1 causal/scope evidence only. It is not B2 historical reference evidence, does not grant a Tier-A waiver, and does not perform scientific admission.

## Exact authorities

- base: `ANIMO-B3D24@0f85d7102945c7c4d77bc49885f9ecca688209e3`
- aggregate snapshot: `ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`
- canonical routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`
- source/accounting semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`
- synthetic-oracle policy: `ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`
- current review governance: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`
- retained Tier-A predicates: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`
- historical-uncertainty closure: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`

## Atomic source/consumer contract

RUNTIMEQ03 and B3I07 qualify the source owner for the denitrification-formation observer as:

`QPrN2Oden(Ln) * St`

The frozen revision-53 source seam has `Z = 10000` and updates the `N2Od` observer with the layer amount multiplied by `Z`. Therefore the exact local accepted-timestep observer increment qualified here is:

`Delta Bani(N2Od,Ly) = 10000 * QPrN2Oden(Ln) * St`

at the existing active-GHG consumer seam.

This statement is deliberately local. It does not assert `Ly == Ln` as a global indexing theorem, does not alter the nitrification `N2On` observer, does not alter total atmosphere emission `N2Oe`, and does not map `QRdN2O` into any TCD-037 observer.

## Synthetic design

The source-shaped Fortran target and the Python oracle are separate implementations. The oracle uses exact `Fraction` arithmetic. Test values are dyadic and exactly representable in binary64, so no empirical tolerance is introduced.

Cases:
- `ACTIVE_NONZERO`: three distinct nonzero denitrification rates;
- `ZERO_DENI`: zero producer control;
- `PERMUTED`: layer rates are permuted to expose accidental profile-total or cross-layer ownership;
- `RATE_TIME_EQUIVALENT`: half-rate/double-time accepted-timestep equivalence;
- `INACTIVE`: nonzero source inputs with the GHG observer branch disabled.

Physical-state, process-flux, A1, A2, A4 and unrelated-observer sentinels must remain exactly unchanged. The only allowed difference surface is `Bani(N2Od)`.

## Evidence boundary

Natural revision-53 active-GHG execution remains `BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`. No testcase translation is performed. Historical revision-53 executable behaviour remains `UNKNOWN`.

The evidence is therefore exactly:

`B1_SYNTHETIC_NOT_B2`

A later `ANIMO-B3A07` must independently re-evaluate every then-current Tier-A predicate before any admission workunit may grant a final waiver.

## Hard boundaries

No production source modification, frozen-B0 modification, canonical-register change, parent or sibling admission, TCD-032..036 composition, B4, production migration, historical-fidelity claim, or B1-to-B2 promotion.

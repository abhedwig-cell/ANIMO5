# ANIMO-B3D15 — TCD-030 GOV04 Tier-B Formal Disposition and Atomic B3 Admission

## Decision scope

This workunit consumes the completed, genuinely separate `ANIMO-B3B06R` second-line review and performs the GOV04-permitted post-review formal disposition and atomic B3 admission for the unchanged TCD-030 claim. It does not repeat or relabel the independent review.

Atomic claim:

> In revision 53 macropore initial-input validation, keep the existing `>MPnitr:` read ownership unchanged and change only the two NO3-labelled `Checkrea` value selectors from `CoMpnh(1)` and `CoMpnh(2)` to the corresponding NO3 values `CoMpni(1)` and `CoMpni(2)`.

The admitted scientific scope is strictly the wrong-species selector defect in initial macropore NO3 validation. No production source is changed here.

## Live authority snapshot before disposition

- Current aggregate central regie: `ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`.
- RG05F already integrates `TCD-027` through `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4` and `TCD-041` through `ANIMO-B3D14@d672992bbc32d40d7e0fbdf03f3fa9bc4cd5a522`.
- Readiness: `ANIMO-B3B06@98235bad7d7fb25b5053e9101c52c0ee3226692a`.
- Independent second-line review: `ANIMO-B3B06R@e64f6ef936a08c8975a2c53000408b67dd03881d`.
- Review validation: GitHub Actions run `34482752015`, success, with validator and scope guard PASS after fail-closed tooling remediation.
- GOV04: `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`.
- GOV03: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`.
- B3Q01: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`.
- MP02: `6b0f2e7470f13baeb6612b0bddb662a497dea528`.
- Canonical TCD-030 register authority: B3I03 append `814ea660d367494432beb63ea78298d1f6cd73d7`.
- Frozen B0 retention authority: `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`.

Immediately before B3D15 authoring, no RG05G branch and no pre-existing B3D15 or later TCD-030 disposition/admission branch were found. A live TCD-030 issue search returned no issue. The B3D15 branch was therefore reserved and then aligned to the exact independent-review closeout head before substantive writes, matching the established post-review disposition pattern.

## Scientific disposition

The independent review returned:

`PASS_INDEPENDENT_SECOND_LINE_REVIEW_TIER_B`

and independently reconstructed the exact source-bound seam:

- routine `MaPoInput`;
- active branch `Nupa.EQ.4`;
- caller gate `Ioptmp.Eq.1`;
- `>MPnitr:` read sequence `CoMpnh(1)`, `CoMpnh(2)`, `CoMpni(1)`, `CoMpni(2)`;
- NO3-labelled validation calls at the retained revision-53 seam use `CoMpnh(1)` and `CoMpnh(2)` as the value arguments;
- the corrected selectors are `CoMpni(1)` and `CoMpni(2)` respectively.

The physical read ownership is already correct before validation: NH4 is read into `CoMpnh`, NO3 into `CoMpni`. The defect is therefore validation-only. It does not require state reconstruction or reassignment.

`Checkrea` uses `999.0` as the sentinel that disables a bound. For this path `Low=0.0` and `High=999.0`, so the effective accepted domain is `Value >= 0.0` with no active upper bound. Zero is accepted, values greater than 999 are accepted, and negative values trigger the lower-bound path with `Error=1992`. Generic `Error=1993` exists only when a non-sentinel upper bound is active and is unreachable on this TCD-030 path.

The earlier NH4 checks execute first. Consequently the atomic correction does not create a whole-routine newly accepted case for invalid NH4. Its observable divergence surface is specifically active input with valid NH4 and at least one negative NO3 value: revision-53 legacy validation can accept that invalid NO3 value because it rechecks NH4, while the corrected selector rejects it and reports the appropriate `CoMpni` diagnostic. On the common accepted-input domain, the physical macropore concentrations and subsequent model execution are unchanged by this selector correction.

No trajectory-equivalence claim is made for a case where one side rejects before model execution and the other proceeds.

## GOV04 risk disposition

The strictest applicable GOV04 trigger remains Tier B:

`GOV04_TIER_B__B_LOCAL_ALGEBRA_INDEX_SPECIES`

The correction is limited to two wrong-species validation value selectors. No persistent macropore state semantics, restart/checkpoint representation, initialization-state reconstruction, runtime architecture, solver/tolerance policy, numerical policy or exact-zero policy changes are required. The fact that the validation occurs while initial input is read does not by itself create a Tier-C state-semantics change because the physical NO3 state is already assigned correctly before `Checkrea` is called.

Any future candidate wider than these two selector substitutions invalidates this Tier-B disposition and requires fresh risk classification and review.

## Evidence and historical uncertainty

Frozen source identity remains pinned to:

- source ZIP SHA256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- `ANIMO_4.1.5.53/mapoinput.for` SHA256 `081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065`;
- `ANIMO_4.1.5.53/input1.for` SHA256 `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`.

The review qualified the source-bound replay and executable semantic matrix, including valid unequal NH4/NO3 controls, each negative NO3 domain, the exact zero boundary, just-below-zero, above-999 sentinel behavior, invalid-NH4 control and inactive macropore control.

No qualified B2 historical reference exists for this path. Under GOV03 the historical behavior therefore remains `UNKNOWN_WITHOUT_B2`. Source-bound and synthetic evidence are not promoted to historical execution evidence.

## Non-composition and expected-difference boundary

TCD-030 remains atomic and does not compose with:

- TCD-025 macropore main-ledger storage/direct-drainage integration;
- TCD-031 persistent macropore solute restart-state representation.

Expected differences are restricted to:

1. input acceptance versus rejection on the active divergence domain;
2. the directly associated validation diagnostic and error return.

No transport algebra, physical state assignment, persistent state, restart behavior, solver behavior, numerical policy, TCD-025 ledger behavior or TCD-031 state composition is admitted as part of TCD-030.

## Atomic B3 admission decision

Subject to the fail-closed machine validation in this workunit, TCD-030 is dispositioned as:

`QUALIFIED_ATOMIC_B3_ADMISSION_WITH_HISTORICAL_UNCERTAINTY_GOV04_TIER_B`

The one independent second-line review required by GOV04 Tier B is satisfied by `ANIMO-B3B06R@e64f6ef936a08c8975a2c53000408b67dd03881d`. B3D15 itself makes no independence claim.

This admission qualifies only the scientific correction identity and the bounded expected-difference surface. It does not authorize a production source patch.

## Hard boundary and aggregate cadence

B3D15 does not modify production or frozen source, edit the canonical TCD register, compose TCD-030 with other corrections, open B4, open production migration, or update aggregate central regie.

RG05F is the current aggregate and states a normal cadence of 3 to 5 new atomic admissions before the next aggregate unless an earlier GOV04 trigger applies. TCD-030 is the first atomic admission after RG05F in this workunit sequence, so aggregate integration remains pending rather than being opened here.

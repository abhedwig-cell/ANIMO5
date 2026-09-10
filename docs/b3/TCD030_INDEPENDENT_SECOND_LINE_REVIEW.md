# ANIMO-B3B06R — Independent Second-Line Review of TCD-030 Macropore Initial NO3 Validation

Date: 2026-09-10

Final review outcome: `PASS_INDEPENDENT_SECOND_LINE_REVIEW_TIER_B`

This is a separate-context second-line review. It does not admit TCD-030, patch production source, edit the canonical TCD register, open B4, start migration, update central regie, or compose TCD-030 with TCD-025 or TCD-031.

## Live authority and handoff recheck

Immediately before the first review write, the review branch still pointed exactly to:

`review/animo-b3b06r-tcd030-independent-second-line@baf54f57b3c94701d85d73336b7afd3e94a4b3d9`

The readiness branch still pointed to:

`ANIMO-B3B06@98235bad7d7fb25b5053e9101c52c0ee3226692a`

and readiness CI run `34474895406` was `success`.

A second live authority check during review found that RG05F had been created after the initial review snapshot. The current aggregate authority is therefore:

`ANIMO-RG05F@7c61a5031f41d602e996310df6f3958cbd1b511e`

RG05F integrates the two post-RG05E atomic admissions:

- `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4` for TCD-027;
- `ANIMO-B3D14@d672992bbc32d40d7e0fbdf03f3fa9bc4cd5a522` for TCD-041.

No RG05G or B3D15 branch was found at the recheck. The remaining review pins are:

- GOV04: `1bbe4c211197590f346803106e45dca5faae79fc`;
- GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- MP01: `7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- MP02: `6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- B3I01 routing: `7b2be9d9742aaad78128c0531591d8e38d7e8450`;
- B3I03 routing: `6a015587807130b4ce12c9f1518c1ddac4e5d624`;
- B3I03 canonical register append: `814ea660d367494432beb63ea78298d1f6cd73d7`;
- later routing observations B3I04 `400b7cd79f89043e091751707dfa96537587dcf6`, B3I05 `1f94a6e08db5d73e8935fb095de9ef9798f6544c` and `7fa0162415e02a6f0167e71b48ae38177a9e06e0`, and B3I06 `8f01f0cb366dfa8cc63a184d6f885100899a8cd9`;
- frozen B0 retention: `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`.

The later aggregate and sibling admissions do not supersede TCD-030. A renewed live lexical GitHub search found no TCD-030 issue. Earlier issue/PR searches likewise returned no TCD-030 item.

## Source-review boundary and frozen identity

The licensed raw frozen source ZIP is intentionally not republished in public GitHub. This review therefore does not claim a fresh byte-for-byte reopening of the ZIP. It uses the repository's established second-line boundary: independently review cryptographically pinned source-bound transcripts, recheck them against the frozen source manifest and antecedent source findings, and do not promote the authoring-context conclusion itself to evidence.

Frozen source identity:

- archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- `ANIMO_4.1.5.53/mapoinput.for`: `081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065`;
- `ANIMO_4.1.5.53/input1.for`: `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`.

The per-member hashes match the retained source manifest. MP01 independently predates B3B06 and already records the same source finding: `mapoinput` reads `CoMpNi` but the NO3-labelled range checks pass `CoMpNh` values. This makes the B3B06 source transcript source-bound replay evidence rather than a self-authenticating readiness assertion.

The global EG01 limitation remains: legally controlled immutable B0 byte retention is not yet fully proven. This review does not close that program-level retention gap and does not reinterpret it as historical B2 evidence.

## Independent source reconstruction

Target routine: `MaPoInput`.

Target local branch: `Nupa.EQ.4`.

Caller activation gate: `Ioptmp.Eq.1` at `input1.for:3460-3465`. When `Ioptmp=0`, the `>MPnitr:` path is not called.

Source-bound `>MPnitr:` read sequence:

1. `CoMpnh(1)`
2. `CoMpnh(2)`
3. `CoMpni(1)`
4. `CoMpni(2)`

The complete licensed Fortran READ line is not republished in Git, so this review deliberately does not invent unit, format, or ERR-clause syntax absent from the source-bound transcript. The exact species/value sequence relevant to TCD-030 is pinned and independently checked.

The two NO3-labelled checks are:

- `mapoinput.for:130`: diagnostic name `CoMpni(1)`, legacy value argument `CoMpnh(1)`, intended selector `CoMpni(1)`;
- `mapoinput.for:132`: diagnostic name `CoMpni(2)`, legacy value argument `CoMpnh(2)`, intended selector `CoMpni(2)`.

The read already stores nitrate in `CoMpni(1:2)`. TCD-030 is therefore not an initial-state assignment defect. It is a wrong-species validation selector defect.

## Checkrea semantics and diagnostics

The pinned source-bound checker transcript at `input1.for:4042-4086` gives:

`Abs(Low-999.).Gt.Nihil .And. Value.Lt.Low`

for the lower guard, setting `Error=1992`, and:

`Abs(High-999.).Gt.Nihil .And. Value.Gt.High`

for the upper guard, setting `Error=1993`.

For TCD-030, `Low=0.0` and `High=999.0`. Therefore:

- `0.0` is accepted because the lower test is strict `<`;
- `999.0` is a sentinel that disables the corresponding bound;
- values above `999.0` are accepted on this exact path;
- `Error=1993` exists in generic `Checkrea` semantics but is unreachable on the TCD-030 path while `High=999.0`;
- a negative active value reaches the lower failure, reports the associated variable, writes the interruption diagnostic, sets `Error=1992`, and returns;
- `input1.for` then returns when `Error.Ne.0`;
- `MaPoInput` read-error label 8500 is a separate malformed-input path outside TCD-030.

## Independent branch matrix

The review validator recomputes the checker and call-order semantics independently. It does not import the B3B06 matrix as its oracle.

| Case | Legacy | Species-correct candidate |
| --- | --- | --- |
| active, NH4=(1,2), NO3=(3,4) | accept | accept |
| active, NO3 domain 1 = -1 | accept | reject 1992 `CoMpni(1)` |
| active, NO3 domain 2 = -1 | accept | reject 1992 `CoMpni(2)` |
| active, NO3 domain 1 = 0.0 | accept | accept |
| active, NO3 domain 1 = -1e-6 | accept | reject 1992 `CoMpni(1)` |
| active, NO3=(1000,1e6) | accept | accept |
| active, NH4 domain 1 = -1, valid NO3 | reject 1992 `CoMpnh(1)` | same rejection |
| inactive `Ioptmp=0`, invalid NH4/NO3 values | path not called | path not called |

A separate generic checker probe confirms the `Error=1993` branch with a non-sentinel upper bound. That probe is not presented as a TCD-030 runtime case.

The unequal NH4/NO3 controls are decisive. They show that the defect is selector ownership, not a coincidental range condition.

## Effect boundary and composition

On the common accepted-input domain, the same READ has already populated the same NH4 and NO3 model values before validation. Replacing only the two NO3 validation value selectors changes no transport state, process flux, persistent state, restart state, solver branch, tolerance, or numerical policy.

On the divergence domain, no trajectory-equivalence claim is made. Legacy may continue after invalid negative NO3 while the corrected validation stops before model execution.

TCD-025 is a separate macropore main-ledger storage/direct-drainage integration gap. TCD-031 is a separate persistent macropore solute restart-state representation gap. Neither is required to correct the two TCD-030 validation selectors, and neither is composed into this review.

## GOV04 risk tier

The strictest applicable GOV04 trigger is Tier B: local algebra/index/species correction with one genuinely independent second-line review.

Tier C is not triggered merely because validation occurs while initial input is read. The nitrate state is already assigned to `CoMpni`; no state is reconstructed, added, re-owned, serialized, restored, or redefined. There is no numerical-policy, solver, tolerance, runtime-architecture, or exact-zero domain-policy change. The exact-zero boundary is already defined by the existing strict lower comparison.

Any future candidate wider than the two value-selector substitutions loses this Tier-B review and must be reclassified.

## Historical behavior

GOV03 closes the historical acquisition route with no qualified B2 reference. MP01 and MP02 likewise state that no active historical macropore B2 reference is available. Historical behavior therefore remains:

`UNKNOWN`

Synthetic or source-only evidence is not promoted to historical truth.

## Review-CI and tooling remediation

The first review CI run, `34482162963`, failed in the validator because it parsed the register snapshot inherited on the review branch, while TCD-030 resides in the separately pinned B3I03 canonical-register append. It failed at the register-presence assertion. This was classified fail-closed as `TOOLING_VALIDATOR_FAILURE`, not as scientific falsification.

The validator was remediated to parse the exact pinned canonical register using:

`git show 814ea660d367494432beb63ea78298d1f6cd73d7:docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv`

The complete remediated review package at `687e3af8aa3f950db787eb4c61eb4dafaab0658f` passed GitHub Actions run `34482752015`. Both the independent scientific validator and the review-only scope guard passed.

## Fail-closed conclusion

No scientific falsification, evidence insufficiency, TCD-030-specific provenance contradiction, scope ambiguity, or Tier-C trigger remains within the established source-bound review boundary. The one tooling-validator failure was identified, persisted, remediated, and successfully retested.

`PASS_INDEPENDENT_SECOND_LINE_REVIEW_TIER_B`

This PASS is review-only. A downstream formal disposition/admission workunit may be opened only if claim, route, pins, source identity, and atomic scope remain unchanged.

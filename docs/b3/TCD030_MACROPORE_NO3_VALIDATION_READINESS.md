# ANIMO-B3B06 - TCD-030 Macropore Initial NO3 Wrong-Species Validation Admission Readiness

## Decision

`PASS_ATOMIC_TIER_B_READINESS_REQUIRES_ONE_INDEPENDENT_SECOND_LINE_REVIEW`

This workunit qualifies only the atomic readiness claim for TCD-030. It does not patch production source, admit the correction, edit the canonical TCD register, open B4, open production migration, or update central regie.

Historical behaviour remains `UNKNOWN`. No qualified B2 active historical macropore reference has been established.

## Live authority recheck

The workunit was created from the current aggregate regie authority `ANIMO-RG05E@eed822037ed8d906a2ab424220597cffac9cca73`. The later atomic TCD-027 admission `ANIMO-B3D13@b20841eb71c338cad21abd8164fa025d8efc75c4` is authoritative as its own admitted object but is not the aggregate base.

Governance and scientific pins used here are:

- GOV04 `1bbe4c211197590f346803106e45dca5faae79fc`;
- GOV03 `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3Q01 `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- MP01 `7b5979dd6301b9d55d23e8c22948a0dba24b229b`;
- MP02 `6b0f2e7470f13baeb6612b0bddb662a497dea528`;
- B3I01 routing `7b2be9d9742aaad78128c0531591d8e38d7e8450`;
- later B3I03 routing observation `6a015587807130b4ce12c9f1518c1ddac4e5d624`;
- B3I03 canonical register append `814ea660d367494432beb63ea78298d1f6cd73d7`;
- frozen B0 retention `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`.

No ANIMO-B3B06 branch, TCD-030-named branch, TCD-030 issue, MP03 branch, MP04 branch, or MP05 branch existed at the live start check. MP02 is the only later dedicated macropore workunit found after MP01. The later canonical routing still identifies TCD-030 as the MP01 local initial-NO3 validation seam, Class B, not admitted. The canonical CSV append contains the TCD-030 row without changing its scientific identity.

## Exact frozen B0 identity

The retained archive `ANIMO_4.1.5.53(3).zip` has SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

That matches the EG01 frozen B0 archive identity. The exact source files used for this qualification also match the EG01 source manifest:

- `ANIMO_4.1.5.53/mapoinput.for`: `081c671d2f576ab0608350cbb0083eab157c586a6783522cda3534b141244065`;
- `ANIMO_4.1.5.53/input1.for`: `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`.

Exact source identity is therefore established. No source-evidence remediation is needed for this workunit.

## Exact defect

The defect is in `MaPoInput`, `mapoinput.for:116-133`, under `Nupa.EQ.4`. The routine reads the `>MPnitr:` values in this order:

`CoMpnh(1), CoMpnh(2), CoMpni(1), CoMpni(2)`

The two NH4 checks correctly validate `CoMpnh(1)` and `CoMpnh(2)`. The two labelled NO3 checks then call `Checkrea` with the wrong species values:

- line 130 labels `CoMpni(1)` but passes `CoMpnh(1)`;
- line 132 labels `CoMpni(2)` but passes `CoMpnh(2)`.

The intended bounded local correction is exactly:

- line 130 value argument `CoMpnh(1)` to `CoMpni(1)`;
- line 132 value argument `CoMpnh(2)` to `CoMpni(2)`.

No other expression is part of TCD-030 readiness.

The active call is gated by `Ioptmp.Eq.1` in `input1.for:3460-3465`. With `Ioptmp=0`, this initial macropore validation path is not called.

## Validation condition and diagnostic path

`MaPoInput` supplies `rarg1=0.0` and `rarg2=999.0` to `Checkrea`. In revision 53, `Checkrea` treats 999 as a no-limit sentinel. The effective TCD-030 condition is therefore only:

`value >= 0`

Zero is valid. There is no effective upper bound in this exact source path. A negative value causes the lower-bound branch to write the label and variable name, write `SIMULATION INTERRUPTED`, set `Error=1992`, and return. `input1.for` then returns when `Error.Ne.0`.

This matters because reading 999 as an upper limit would create a different validation contract that is not present in frozen B0. The older ANIMO 4.0 documentation is useful for species ownership and input ordering, but it cannot override this exact revision-53 checker implementation.

The `MaPoInput` read-error label 8500 is a separate malformed-input path. TCD-030 does not change it.

## NO3 and NH4 ownership

The source comments identify the first two values as macropore ammonium and the next two as macropore nitrate. The read statement already stores NO3 in `CoMpni(1:2)`. The defect does not mis-assign physical initialization state. It only passes the already-read NH4 values to two calls that are explicitly labelled as NO3 validation.

This distinction is also important for the observable routine outcome. The valid NH4 checks run first. Therefore a negative NH4 already fails as `CoMpnh` before the faulty NO3-labelled calls are reached. The local correction does not create a new acceptance path for any input. Its observable acceptance effect is narrower: negative NO3 can currently escape validation when NH4 is nonnegative, and the corrected selector would reject it.

## Predeclared comparison domain

For already-valid active inputs with all four NH4 and NO3 concentrations greater than or equal to zero, legacy and the planned corrected selector both accept the input. The same `Read` statement has already assigned the same physical values, and `Checkrea` is read-only with respect to those values. On this common acceptance domain, TCD-030 introduces no physical transport state, process flux, persistent state, restart, solver, tolerance, or numerical-policy difference.

For active inputs with nonnegative NH4 and at least one negative NO3 value, legacy can continue while the corrected validation is expected to stop with `Error=1992` on the corresponding `CoMpni` diagnostic. No physical trajectory equivalence is claimed for this divergence domain because one side does not enter model execution.

For `Ioptmp=0`, the `>MPnitr:` validation path is inactive and TCD-030 causes no acceptance or diagnostic difference.

## Executable branch matrix

The machine-readable matrix covers:

- valid active NO3 with deliberately unequal NH4 and NO3 values;
- invalid negative NO3 independently in domain 1 and domain 2;
- exact lower boundary `0.0`;
- a just-below-boundary negative value;
- values greater than 999 to prove that 999 is a sentinel, not an upper bound;
- negative NH4 with valid NO3 to prove unchanged NH4 ownership and earlier rejection;
- inactive `Ioptmp=0`.

The validator implements the exact Checkrea lower-bound and sentinel semantics, legacy call ordering, and the two planned corrected value selectors. Expected differences are limited to input acceptance/rejection and the directly associated validation diagnostic.

## GOV04 risk classification

The evidence supports risk Tier B, not Tier C.

This seam occurs while initial input is being read, but it does not change initialization-state reconstruction or state ownership. The same `Read` statement populates `CoMpni` before validation in both forms. The only proposed difference is the value argument selected by two local `Checkrea` calls. No persistent state representation is added or redefined, no restart path changes, no runtime architecture changes, and no numerical policy changes.

If a later implementation proposal widens beyond those two value-selector substitutions or requires state/restart semantics, this Tier B qualification no longer applies and the work must be reclassified or escalated under GOV04.

## Composition exclusions

TCD-025 is the separate macropore main-ledger storage/direct-drainage integration gap. TCD-030 does not alter that ledger and makes no ledger-composition claim.

TCD-031 is the separate persistent macropore solute restart-serialization/state problem. TCD-030 does not add, serialize, restore, or redefine persistent macropore state.

The workunit also makes no whole-model, B4, production, or migration claim.

## Readiness conclusion and independent handoff

TCD-030 is ready for one genuinely independent GOV04 Tier-B second-line review at this exact scope and these pins. This authoring context does not perform or approve that review.

The separate handoff branch is reserved as:

`review/animo-b3b06r-tcd030-independent-second-line`

An independent PASS is required before any admission. If that review passes without changing claim, route, pins, or scope, GOV04 permits one downstream workunit to combine formal disposition and admission closeout. Central-regie aggregation remains separate and is not part of this workunit.

# ANIMO-B3B01R: Independent second-line review of TCD-015 NO3 transport algebra

Date: 2026-09-10

Disposition: `PASS_TCD015_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION`

Semantic result: `PASS`

## Review boundary and independence

This review was executed in a separate ChatGPT context from the ANIMO-B3B01 readiness and ANIMO-B3D09 disposition authoring contexts. Their conclusions were treated as review objects and handoff context, not as self-authenticating scientific evidence. Source-bound records, frozen identities, equations, execution evidence, synthetic evidence, branch coverage, comparison tooling, feature boundaries and the live GOV03 route were reopened and checked independently.

No organizational, institutional or human independence is claimed. The independence claim is limited to separate-context review and independent re-evaluation.

This review does not admit TCD-015. It does not modify production source, the frozen source, frozen testcases, clipping policy, `Optneg`, `Vsmall`, numerical tolerances, solver policy, analytical-branch policy, the canonical TCD register or central RG05. It performs no B4 step and no composition with another correction.

## Live heads rechecked before review write

Immediately before the first review write, the clean review branch still pointed exactly to:

`review/animo-b3b01r-tcd015-independent-second-line@c05486e76993d26771f62f32842508479d14fdde`

That handoff commit has direct parent `2a5abc00a779baaa3fb3fa28b3c051231c286132`.

The following review objects and authorities were pinned:

- ANIMO-B3B01 readiness: `b982242949aecab32b9067cf7910ad75abfc2b19`;
- ANIMO-B3D09 scientific disposition: `2a5abc00a779baaa3fb3fa28b3c051231c286132`;
- ANIMO-B3D09 administrative closeout: `cf3e2746351c5c75d236e1b63fb0623daa8e7372`;
- ANIMO-GOV03: `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- ANIMO-B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- central regie at handoff, ANIMO-RG05D: `f3d6b9780631bd627f8bca0658a8e3878746e666`;
- SYNQ01 independent synthetic-oracle head: `842f72300fd03ede0b9024537a7ee6126722a121`.

The B3B01 readiness branch remained exactly at its supplied readiness head. The B3D09 work branch was live at the supplied administrative closeout head. The RG05D branch remained at the supplied handoff authority head.

GitHub issue #32 and all comments were reread immediately before writing. The only pre-review comment was B3D09 handoff metadata and explicitly stated that it was not independent review evidence.

## Evidence classification used in this review

Four evidence labels are used deliberately:

1. `SOURCE_BOUND_REPLAY_VERIFIED`: a persisted source audit, source transcript or execution record is cryptographically bound to the frozen source member and is independently checked for the claim made here.
2. `INDEPENDENTLY_RECOMPUTED`: the reviewer recomputed the equation, numerical identity or logical implication from persisted inputs rather than accepting a prior conclusion.
3. `EVIDENCE_REPLAYED`: a persisted execution/comparison result was inspected for its exact scope and acceptance rule. It is not presented as a fresh execution in this review context.
4. `ASSERTION_ONLY_NOT_ACCEPTED`: B3B01, B3D09 or same-account review prose is recorded for traceability but is not used to close a scientific gate without another check.

The frozen raw source ZIP is intentionally not republished in GitHub. Therefore this review does not claim a fresh byte-for-byte opening of the licensed `Transsub.for` member. The source seam is reviewed against the frozen archive hash, member hash, source manifest, pre-B3 source-bound PREP01 records, source-bound branch transcripts, generic-use evidence and independent algebraic/control-flow checks. This is the same narrow source-review boundary already used by repository second-line review convention. No stronger claim is made.

## Frozen B0 identity

Rechecked frozen identities:

- source evidence ID: `ANIMO-B0-SRC-41553-R53`;
- source archive: `ANIMO_4.1.5.53(3).zip`;
- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank evidence ID: `ANIMO-B0-TB-202609`;
- testbank archive: `ANIMO_testbank.zip`;
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- exact source member: `ANIMO_4.1.5.53/Transsub.for`;
- `Transsub.for` SHA-256: `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`;
- canonical TCD register blob at B3Q01: `224acc350fde69d3c4aebed8628c0f945e0b3367`.

Gate: `PASS` as `SOURCE_BOUND_REPLAY_VERIFIED`.

## Atomic source algebra

The source-bound seam records:

```fortran
Hv = (Mt-Mto)/st

Hv1 = Fu/ld + Rd*Fev/ld + Reki*Half*(Mt+Mto) + Hv
```

At the second negative-concentration reconstruction the legacy expression is:

```fortran
Reko = (Mt*rsc-Mto*Co)/St
     - (-Avc*Hv1
        + Flo*Con/ld
        + Flb*Cb/ld
        + Fid*Coid/ld)
```

The nitrate-scoped candidate atomic expression is:

```fortran
Reko = (Mt*rsc-Mto*Co)/St
     - (-Avc*(Hv1-Hv)
        + Flo*Con/ld
        + Flb*Cb/ld
        + Fid*Coid/ld)
```

Independent symbolic subtraction gives:

```text
candidate - legacy
= [storage + Avc*(Hv1-Hv) - inflow]
  - [storage + Avc*Hv1 - inflow]
= -Avc*Hv
```

No other term is required for that identity. The claim is limited to the second reconstruction seam.

Gate: `PASS` as `INDEPENDENTLY_RECOMPUTED` from source-bound expressions.

## Exact control-flow location and clipping boundary

Source-bound execution records place the target expression only after the analytical solution has produced a second negative concentration, the existing clipping path has replaced `Rsc` with `Vsmall`, and `Avc` has been recomputed from that clipped state. The proposed atomic change acts only in the subsequent `Reko` reconstruction. It does not alter the negative-concentration trigger, the `Rsc=Vsmall` action, the `Avc` recomputation or the analytical solution that led to the negative concentration.

This matters scientifically. The candidate is not a redesign of clipping physics. It removes one storage derivative from the zero-order source reconstruction after the already-existing clipped state has been selected.

Gate: `PASS` as `SOURCE_BOUND_REPLAY_VERIFIED` plus independent control-flow interpretation.

## Nitrate binding and generic `Transsub`

The natural target event is explicitly the main ANIMO transport call for substance `NITRATE`, TITO 2312, layer 1, `Iflsol=1`. Branch instrumentation across the eight natural cases records 508 target reconstruction hits and all 508 are `NITRATE`.

`Transsub` itself is not nitrate-exclusive. Independent pre-B3 PREP01 evidence records a natural `AMMONIUM` call through the same `Transsub` routine at Puitmijn TITO 1490, layer 0, `Iflsol=2`. Therefore the scientific scope must be carried by the caller/species binding, not by changing generic `Transsub` behavior for all substances.

The review authorizes no generic shared-substance correction. TCD-015 remains nitrate-scoped only.

Gate: `PASS` as `SOURCE_BOUND_REPLAY_VERIFIED`.

## Natural LWKM activation and local mass identity

The natural event is:

- case: `LWKM`;
- year: 1997;
- TITO: 2312;
- layer: 1;
- substance: `NITRATE`;
- analytical solution class: `Iflsol=1`.

Persisted event values include:

```text
Mto  = 0.350588
Mt   = 0.385095
St   = 10 d
Ld   = 0.05 m
BAPD = -0.00084267311478156 kg/m2
BATR = -0.00090054430498043 kg/m2
legacy Reko    = -0.0016853462295631
corrected Reko = -0.0018010886099609
```

Independent decimal recomputation gives:

```text
Hv = (0.385095 - 0.350588) / 10
   = 0.0034507 d-1

BAPD - BATR
= 0.00005787119019887 kg/m2
```

Using the local duplicated-storage identity,

```text
Avc * Hv * St * Ld = BAPD - BATR
```

the event values imply:

```text
Avc = 0.033541710492868113716057611499116121366679224505173
```

and therefore:

```text
-Avc*Hv
= -0.000115742380397740000000000000...
```

The persisted candidate-minus-legacy `Reko` is:

```text
-0.0018010886099609 - (-0.0016853462295631)
= -0.0001157423803978
```

The displayed difference between these two representations is `6e-17`, attributable to the persisted decimal display precision. It is reported, not thresholded. No tolerance is used to decide the identity.

The duplicated local mass is independently recomputed as:

```text
Avc*Hv*St*Ld
= 0.00005787119019887 kg/m2
= 0.5787119019887 kg/ha
```

This is the same local quantity as `BAPD-BATR` at the event from the displayed persisted values.

Gate: `PASS` as `INDEPENDENTLY_RECOMPUTED`.

## Execution-only corrected reconstruction and annual effect

The PREP01 execution-only diagnostic changed only the reconstruction term from `Avc*Hv1` to `Avc*(Hv1-Hv)` at the target seam. It was not a production correction and is not historical evidence.

Persisted causal effects are:

- local TITO-2312 residual closes to effectively zero at printed execution precision;
- LWKM annual NO3 residual changes from `+0.5760503022407 kg/ha N` to approximately `+2.28e-7 kg/ha N`;
- NO3 transport mass-balance warnings change from 3 to 0.

The annual residual is not asserted to equal the single local `0.5787119019887 kg/ha` duplicated term because the annual balance aggregates other contributions. The local identity is exact at the event; the annual effect is corroborating causal execution evidence.

These values are not a numerical tolerance and are not historical truth. They are causal evidence about the frozen-source diagnostic build.

Gate: `PASS` as `EVIDENCE_REPLAYED`, with the local identity independently recomputed.

## SYNQ-O001 independent conservation discriminator

SYNQ-O001 is implemented in `tools/reference/synthetic_oracles.py`. That module imports no ANIMO production or legacy implementation. Its TCD-015 oracle is the isolated conservation statement:

```text
duplicated_storage_term = Avc * Hv * St * Ld
conservative_residual   = 0
```

The discriminator uses:

```text
Avc = 0.2
Hv  = 0.1
St  = 2
Ld  = 0.1
```

Independent decimal recomputation gives exactly:

```text
0.2 * 0.1 * 2 * 0.1 = 0.004 kg/m2
```

The synthetic implementation asserts exact equality to `0.004` and exact zero for the conservative residual. It does not copy the Transsub control flow, source indexing, solver or convergence policy. The natural LWKM event corroborates the same identity at a different point, but does not define the synthetic expected value.

SYNQ-O001 is therefore independent causal evidence for the local conservation identity. It is not B2, does not establish historical prevalence or historical fidelity, and does not by itself justify admission.

Gate: `PASS` as independently inspected synthetic evidence plus `INDEPENDENTLY_RECOMPUTED` discriminator.

## Predeclared expected-difference and unchanged surfaces

The expected-difference contract was persisted before the broad eight-case B1 comparison. Commit ordering was rechecked: the predeclaration commit `00cd64daf052c06432505212ac95771860a56f63` precedes the broad readiness evidence commit `4f96b5aaf3c7e140d02587aba6d7a6c6ce915023`.

Declared changed surface is limited to the nitrate reconstruction and causally derived N-balance/report consequences, including an already-existing `CORRECTION(2)` transfer if the changed nitrate bookkeeping crosses that existing threshold.

Declared unchanged surface includes, among other things:

- clipping trigger and `Optneg`;
- `Vsmall` and clipping/tolerance constants;
- analytical branch choice and solver policy;
- `Rsc` and `Avc` computation;
- water states and water fluxes;
- nitrate transport input/boundary concentrations;
- all non-NITRATE substances under the species-scoped candidate;
- transport physics outside the duplicated storage bookkeeping term.

Gate: `PASS` as predeclaration chronology plus exact contract inspection.

## Eight-case natural B1 non-interference matrix

The persisted candidate comparison covers the eight natural B1 cases. Across 550 compared output files excluding stdout:

```text
430  EQUAL_RAW
 99  EQUAL_DECLARED_VOLATILE_NORMALIZATION_ONLY
 21  scientific differences
---
550  total
```

The arithmetic was independently checked. The 21 scientific differences are reported entirely within the predeclared nitrate/N-balance surface. Cases without activation remain scientifically unchanged. Changed cases are limited to nitrate balance/report outputs and, for LWKM, the expected removal of the relevant warning messages.

The comparator implementation was inspected independently. Its normalization rules are anchored only to five forms of volatile legacy metadata: file-creation timestamp, output run-start timestamp, message run-start timestamp, message run-end timestamp and elapsed CPU seconds. Scientific numbers are never tolerance-filtered. When numbers differ, the comparator reports the difference and diagnostic magnitude rather than accepting it by threshold.

An unguarded generic diagnostic probe and the nitrate-scoped probe happened to be scientifically identical on these eight natural cases because all observed target hits were nitrate. That observation is non-interference evidence only. It is explicitly not authorization to alter generic `Transsub` behavior.

Gate: `PASS` as `EVIDENCE_REPLAYED` plus independent comparator-policy inspection.

## IFLSOL branch coverage supplement

Natural branch instrumentation records 508 target second-reconstruction hits, all nitrate:

- `Iflsol=1`: 486 natural hits;
- `Iflsol=3`: 22 natural hits;
- non-nitrate target hits: 0.

`Iflsol=1` has nonzero `Hv` and is discriminating. `Iflsol=3` is an exact negative control for this atomic difference because the source-bound branch relation gives `Hv=0`; therefore `-Avc*Hv=0` and baseline/candidate `Reko` are exactly identical in the isolated formatted output.

An isolated exact frozen-Transsub harness exercises reachable `Iflsol=4` and observes identical `Rsc` and `Avc` with a nonzero `Reko` delta matching the same source-algebraic identity. This supplies branch coverage where the natural B1 suite does not activate mode 4.

For `Iflsol=2`, define the frozen-source storage factor:

```text
B = Mto + Rhbd*Socf
```

The pre-adjust source invariant ensures the numerator `B*Co + Hv2*St` is nonnegative, or replaces `Hv2` so the numerator becomes positive `Vsmall`. With `Hv1=Hv` the final concentration reduces to:

```text
Rsc = (B*Co + Hv2*St) / (B + Hv*St)
```

Under the valid positive final-storage denominator required by the model domain, a negative `Rsc` cannot be produced. Therefore the target second negative-concentration reconstruction is structurally unreachable for mode 2 in that domain.

For `Iflsol=5`, `Hv=Hv1=0` and:

```text
Rsc = (B*Co + Hv2*St) / B
```

With positive `B` and the same nonnegative pre-adjust numerator, the target negative reconstruction is structurally unreachable.

The source-bound branch inventory contains no additional analytical mode capable of reaching this target reconstruction. Thus the target seam is covered by natural/synthetic modes 1, 3 and 4, with source-level structural unreachability for 2 and 5 under valid positive storage denominators.

This conclusion is `SOURCE_BOUND_REPLAY_VERIFIED` for the frozen branch formulas and `INDEPENDENTLY_RECOMPUTED` for their sign/reachability implications. It is not a claim of a fresh raw-source parse.

Gate: `PASS`.

## GHG feature boundary

TCD-015 is qualified here only for core nitrate transport with `GreenHouseGasOption=0`.

The supplied GHG-enabled `GHGMais` testcase cannot be treated as a revision-53 qualification case. PREP01 shows that it does not match the frozen revision-53 parser contract, including missing or incompatible GHG/organic-matter sections. Consequently this review does not infer anything about GHG-enabled downstream consequences from the GreenHouseGasOption=0 matrix.

GHG-enabled downstream consequences remain explicitly unqualified.

Gate: `PASS` for the stated feature boundary, not for GHG-enabled execution.

## No policy redesign bundled into the claim

The atomic correction reviewed here does not require or authorize:

- clipping-policy redesign;
- `Optneg` change;
- `Vsmall` change;
- numerical-tolerance change;
- solver change;
- analytical-branch policy change;
- generic `Transsub` behavior change;
- any non-nitrate transport-physics change.

The candidate difference is the single nitrate-scoped `Hv` removal from the second post-clipping `Reko` reconstruction.

Gate: `PASS`.

## GOV03 route and historical uncertainty

The live GOV03 authority is `cbd262bdabe92923113b7326f2f42822ce9a971c`.

Its persisted acquisition evidence records a completed targeted historical-reference search across multiple named expert/archive routes and no provenance-qualified executable or historical testcase-output bundle suitable for B2. The evidence explicitly refuses to promote the problematic executable, rebuilt executable, source code or expert concurrence to historical B2 evidence.

The qualified route state is therefore:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

G6U state:

`ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`

This review does not turn G6U eligibility into historical evidence. Historical TCD-015 behavior remains `UNKNOWN`. Historical fidelity is not claimed.

Gate: `PASS` for route eligibility and uncertainty preservation.

## Existing PR #21 COMMENTED material

PR #21 contains one prior second-line handoff review submission marked `COMMENTED`, authored by the same GitHub account `abhedwig-cell`. Its text asks a future reviewer to verify the TCD-015 gates. It is not accepted as independent second-line evidence in this review.

Gate: `PASS` for independence handling.

## B3Q01 Class-B requirements

B3Q01 classifies this family as local algebra/index/species work and requires, under historical uncertainty, exact causal-path evidence, a local conservation identity, stronger branch coverage, non-interference and a genuinely separate second-line review. Synthetic evidence may support causality but may not substitute for B2 historical prevalence.

For the atomic nitrate-only TCD-015 claim, the independent review finds those scientific gates closed by the combination of:

- exact frozen identity and member binding;
- source-bound seam/control-flow evidence;
- independent symbolic delta derivation;
- independently recomputed LWKM local mass identity;
- natural execution closure effect;
- independent SYNQ-O001 conservation discriminator;
- predeclared changed/unchanged surface;
- eight-case no-tolerance non-interference matrix;
- natural and isolated IFLSOL coverage plus structural unreachability proof;
- explicit nitrate-only and GreenHouseGasOption=0 boundaries;
- live GOV03 historical-uncertainty route.

No required scientific gate for this atomic review remains unresolved.

## Fail-closed gate table

| Gate | Result | Review basis |
| --- | --- | --- |
| frozen B0 source/testbank/member identity | PASS | source-bound replay |
| exact `Hv` and `Hv1` definitions | PASS | source-bound replay |
| exact second reconstruction expression | PASS | source-bound replay |
| candidate-minus-legacy `-Avc*Hv` | PASS | independent algebra |
| post-`Rsc=Vsmall`/`Avc` control-flow location | PASS | source-bound replay plus interpretation |
| nitrate caller binding | PASS | natural instrumentation |
| `Transsub` generic, not nitrate-exclusive | PASS | independent NH4 PREP01 evidence |
| natural LWKM TITO 2312 activation | PASS | natural execution evidence |
| local `Avc*Hv*St*Ld` identity | PASS | independent decimal recomputation |
| relation to `BAPD-BATR` | PASS | independent decimal recomputation |
| execution-only corrected closure | PASS | evidence replay |
| annual NO3 balance effect | PASS | evidence replay |
| evidence treated as causal, not tolerance/history | PASS | explicit evidence/tool boundary |
| SYNQ-O001 independence and discriminator | PASS | independent oracle-code inspection and recomputation |
| expected-difference predeclaration | PASS | commit chronology and contract inspection |
| required-unchanged surface | PASS | contract plus matrix |
| eight-case natural B1 non-interference | PASS | evidence replay |
| 550-file accounting | PASS | independent arithmetic |
| volatile-metadata-only normalization | PASS | comparator source inspection |
| absence of numerical tolerance | PASS | comparator source inspection |
| IFLSOL 1 natural coverage | PASS | branch evidence |
| IFLSOL 3 exact zero-delta control | PASS | branch evidence plus independent algebra |
| IFLSOL 4 isolated reachability | PASS | isolated harness evidence |
| IFLSOL 2 and 5 target unreachability | PASS | source-bound formulas plus independent sign proof |
| no hidden reachable target mode | PASS | source-bound branch inventory |
| nitrate-only scope, no generic authorization | PASS | caller/generic-use crosscheck |
| GreenHouseGasOption=0 boundary | PASS | feature/provenance crosscheck |
| no clipping/tolerance/solver/policy redesign | PASS | candidate surface review |
| GOV03/G6U route | PASS | live governance evidence |
| historical behavior remains UNKNOWN | PASS | explicit boundary |
| PR #21 COMMENTED material excluded | PASS | live PR review check |
| review hard boundary, no admission | PASS | review diff/scope guard |

## Disposition

Semantic result: `PASS`.

Repository-native disposition:

`PASS_TCD015_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION`

Meaning: the independent separate-context second-line review supports the bounded TCD-015 nitrate-only Class-B atomic scientific claim at the reviewed heads and evidence objects. It does not admit TCD-015, does not create a production correction and does not establish historical fidelity.

Historical behavior remains `UNKNOWN`.

GHG-enabled downstream consequences remain unqualified.

A later separate admission-closeout workunit is required before any B3 admission reconciliation. This workunit stops here after validated independent-review closeout.
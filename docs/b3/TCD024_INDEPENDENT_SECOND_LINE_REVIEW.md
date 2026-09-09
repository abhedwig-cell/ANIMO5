# ANIMO-B3B03R — Independent second-line review of TCD-024 Slow Langmuir Site Indexing

Date: 2026-09-09

Disposition: `PASS_TCD024_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION`

## Independence boundary

This review was executed in a separate ChatGPT context from the ANIMO-B3B03 authoring context. The B3B03 readiness conclusion, the earlier technical review, and B3D03 were treated as review objects or route context, not as self-authenticating scientific evidence. Source-bound records, exact hashes, equations, synthetic controls, route state, and the numerical discriminator were rechecked independently.

No organizational or human independence is claimed. The independence claim is limited to the separate review context and independent re-evaluation performed here.

No B3 admission is performed. No production source is modified.

## Atomic claim reviewed

Only the following local slow-Langmuir indexing claim is reviewed:

```fortran
legacy:    Yy = One + Parcxsl(3,I) * Avc
candidate: Yy = One + Parcxsl(3,J) * Avc
```

The question is whether the site-specific slow-Langmuir affinity in `Conc_unl` belongs to slow-sorption site index `J`, rather than nonlinear trial counter `I`.

The review does not admit TCD-019, change nonlinear policy, select tolerances, redesign the solver, or establish historical behaviour.

## Live identities rechecked before review write

- clean review branch starting head: `07e440bb42d58facad6b4e5408dd57a0d8f82daf`;
- candidate B3B03 head: `446f57f3aeff6e7db56ce473f0724bdb58cad94f`;
- B3Q01 framework head: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- NQ02 head: `40a41089020f78ee1d5181b8afc7bdb511af3193`;
- GOV03 head: `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3D03 head: `a3e194573b3a7ce95d5ef15fc179ddb3a613d8a6`;
- prior technical-review head, not used as scientific authority: `02ce1f49582d2b8cb794c3bfb9d674481a2eea1e`;
- handoff-contract head: `1d0aeae8c9f40547f8ac9273fc4c9655593bdecd`.

SYNQ01 required one metadata correction during the live recheck. The actual live commit head is `842f72300fd03ede0b9024537a7ee6126722a121`. `124364c008cdca511f024b3b7d7677572c6ac0c7` is that commit's tree SHA, not the commit head. The relevant oracle-register blob remains exactly `4c215d19844614de8868380fb03f93268ea4c5d8`. This head/tree distinction does not change the TCD-024 scientific evidence, but it is pinned correctly here.

## Frozen B0 and canonical TCD identity

Rechecked frozen identities:

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- supplied testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- frozen source member: `ANIMO_4.1.5.53/Transorp.for`;
- frozen `Transorp.for` member SHA-256: `65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`;
- canonical TCD register blob at B3Q01: `224acc350fde69d3c4aebed8628c0f945e0b3367`.

The canonical TCD-024 record identifies the same nested-index seam: nonlinear trial `I=1..20`, slow site `J=1..Ncxsl`, and a site-parameter array bounded by `Macx=3`. It classifies the `Parcxsl(3,I)` use inside the site loop as a wrong-index defect and latent bounds risk.

Evidence boundary: the frozen source ZIP itself is intentionally not republished in the public repository. Therefore this second-line review cannot claim a fresh byte-for-byte opening of the raw `Transorp.for` member through GitHub. The seam is instead reverified against the frozen member hash, source manifest, source-bound PREP05 evidence, canonical TCD record, and independently checked index-domain and equation evidence. This is sufficient for the atomic claim reviewed here, but the narrower provenance boundary is retained explicitly.

## Exact source seam and meaning of I versus J

The source-bound `Conc_unl` evidence shows an outer nonlinear iteration `I=1..20` and an inner slow-site loop `J=1..Ncxsl`. Within that site loop, site equilibrium, `Recf(J)`, and the updated slow-site amount are site-local. The legacy exponent nevertheless reads `Parcxsl(3,I)`.

That selector is semantically inconsistent with the array's site domain. With `Ncxsl <= Macx = 3`, `J` is the site selector. `I` is not. The exact integer-domain cross-check is stronger than a numerical coincidence: `I` may range to 20 while the site domain ends at 3, with trial index 4 already outside that domain.

Gate result: `PASS`.

## Class-B atomicity

The candidate correction changes only one parameter selector, from `I` to `J`, in the local slow-Langmuir kinetic expression. A direct compare of B3Q01 to B3B03 shows only readiness documentation, evidence, validator, and workflow files were added. No production source file was modified by the readiness workunit.

The atomic correction requires no new state, no constitutive-form change, no timestep/subdivision change, no stopping-rule change, no tolerance change, no fallback change, and no TCD-019 numerical-policy change.

Gate result: `PASS` as `B_LOCAL_ALGEBRA_INDEX_SPECIES`.

## Unequal-site discriminator and unrounded evidence

The active discriminator uses deliberately unequal sites with `C=0.04`, `rho=1`, and `dt=1.5`:

| site | Qmax | K | qold | r_ads | r_des |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.30 | 2 | 0.010 | 0.20 | 0.02 |
| 2 | 0.90 | 40 | 0.020 | 0.07 | 0.01 |
| 3 | 0.12 | 600 | 0.005 | 0.015 | 0.003 |

The independently re-evaluated relation is:

```text
qeq_j  = (Qmax_j/rho) * (K_j*C)/(1 + K_j*C)
y_j    = exp(-r_j * (1 + K_j*C) * dt)
qnew_j = qold_j*y_j + qeq_j*(1-y_j)
```

Using 80-decimal arithmetic, the site-J states reproduce as:

```text
site 1: 0.013382497037579703764323601003327353135602564031862008456803506888922032817413340
site 2: 0.14753969645039970073105831290404905178546400628007091356315257450780555441805199
site 3: 0.052409932714652284323717408180830665689512840129054843302530861570332277037363397
```

The wrong `K1` selector gives:

```text
site 1: 0.013382497037579703764323601003327353135602564031862008456803506888922032817413340
site 2: 0.077231793016630632245642328684096944742583375424392326084530401228142520492628225
site 3: 0.0076455859493262592189248710070344630901401232826660990593613765090187853437838248
```

Site 1 is intentionally non-discriminating because `I=J=1` there. Sites 2 and 3 separate the selectors strongly, so the defect cannot hide behind equal site parameters.

The corresponding unrounded site-transfer rates `(qnew-qold)/dt` for the site-J calculation are:

```text
site 1: 0.0022549980250531358428824006688849020904017093545746723045356712592813552116088933
site 2: 0.085026464300266467154038875269366034523642670853380609042101716338537036278701327
site 3: 0.031606621809768189549144938787220443793008560086036562201687241046888184691575598
```

These values were re-derived from the equation rather than accepted from rounded report output. The shortened SYNQ-O006 display strings are therefore not used as acceptance tolerances.

Unequal-site discriminator gate: `PASS`.

Unrounded state and transfer gate: `PASS`.

## Exact multi-site conservation identity

For the isolated internal transfer control volume, the independently recomputed total slow-site storage gain is:

```text
sum_j(qnew_j-qold_j)
= 0.17833212620263168881909932208820707061057941044098776532248694296705986427282873
```

Defining the dissolved counter-transfer as its exact negative gives:

```text
Delta P_solution + sum_j(Delta P_slow,j) = 0
```

exactly, with no tolerance and no external source or sink in this isolated control volume.

This is a legitimate local conservation cross-check. It is not evidence that the full coupled phosphorus model closes, and it does not absorb TCD-019 into this claim.

Gate result: `PASS`.

## Active and inactive controls

Three required controls were checked:

1. Active `Optcxsl=2` unequal-site synthetic microcase: the `J` selector produces the independently calculated site-specific states and transfers above, while the wrong selector is discriminated at sites 2 and 3.
2. Zero-rate inactive site: with both kinetic rates zero, `qnew=qold=0.005` and transfer is exactly `0`, independent of the affinity selector.
3. Inactive constitutive route: the supplied `Optcxsl=3` Freundlich natural case is outside the target expression. The source-bound diagnostic comparison reports 55 normalized model outputs with zero differences for the TCD-024-only mutation.

The third control is deliberately scoped only to the supplied normalized comparison and is not generalized to every inactive configuration.

Gate result: `PASS`.

## TCD-019 separation

NQ02 is live at `40a41089020f78ee1d5181b8afc7bdb511af3193`. Its four-way synthetic interaction study explicitly distinguishes TCD-019, a Class-E nonlinear phosphorus numerical-policy issue, from TCD-024, a Class-B slow-site indexing issue. The historical LWKM TCD-019 case uses slow Freundlich sorption, so TCD-024 is not naturally active there. The combined synthetic probe is composition evidence only and performs no composition admission.

This review therefore does not use improvement in mass balance as proof that TCD-019 is solved, nor does it require a TCD-019 change for TCD-024 to be atomic.

Gate result: `PASS`.

## Expected difference and non-interference

The predeclared expected-difference surface is coherent with the one-expression correction. When `Optcxsl=2` is active and `K_J != K_I`, direct differences may occur in the site-J kinetic factor, slow-sorbed P state, site-local P transfer, and downstream P quantities receiving that transfer.

Expected unchanged within the qualified diagnostic scope are branch selection, trial/site loop ordering, `Recf(J)`, the TCD-019 numerical policy, nonlinear stopping/tolerance/fallback rules, `Optcxsl=1` and `Optcxsl=3`, a zero-rate inactive site, hydrology, and unrelated species outside existing P coupling.

The B3B03 readiness branch itself contains no production-source change. The evidence therefore supports the declared difference surface without silently broadening the correction.

Gate result: `PASS` within the explicitly qualified diagnostic scope.

## Natural activation and historical uncertainty

No supplied frozen natural test case positively activates `Optcxsl=2`; the supplied active-P cases use `Optcxsl=3`. Synthetic activation therefore establishes causality and branch coverage only.

The historical prevalence remains `UNKNOWN`. There is no qualified B2 for the target path, and no historical fidelity or historical equivalence is claimed.

Natural-activation limitation gate: `PASS` because the limitation is retained rather than hidden.

Historical-prevalence gate: `PASS` because `UNKNOWN` is retained.

## GOV03 and B3D03 route recheck

GOV03 is live at `cbd262bdabe92923113b7326f2f42822ce9a971c`, with its closeout workflow successful at run `34391300744`. It qualifies bounded historical-reference acquisition closure and makes G6U eligible as `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`. It explicitly does not recover B2, establish historical behaviour, or admit a correction.

B3D03 is live at `a3e194573b3a7ce95d5ef15fc179ddb3a613d8a6`, with its closeout workflow successful at run `34395336504`. Its formal disposition is route-open but not admitted because the independent second-line gate was still pending at that snapshot.

The older B3B03 candidate status still records the pre-GOV03 route as blocked. That is a stale route snapshot at the immutable candidate head, not evidence that the live route is now closed. Live GOV03 and B3D03 supersede it for route-state review.

Gate result: `PASS` for live route recheck. The route is available, but this review does not execute admission.

## Gate disposition

| gate | result |
| --- | --- |
| frozen B0 and canonical TCD-024 identity | PASS |
| exact source seam and I/J meaning | PASS |
| Class-B atomicity | PASS |
| unequal-site positive discriminator | PASS |
| unrounded site-state and site-transfer evidence | PASS |
| exact multi-site conservation identity | PASS |
| active/inactive controls | PASS |
| TCD-019 separation | PASS |
| expected-difference and non-interference boundaries | PASS |
| natural positive activation limitation retained | PASS |
| historical prevalence retained UNKNOWN | PASS |
| GOV03/B3D03 route live rechecked | PASS |

## Final second-line disposition

`PASS_TCD024_ATOMIC_CLASS_B_SECOND_LINE_REVIEW_NO_ADMISSION`

The independently re-evaluated evidence supports the narrow scientific claim that the slow-Langmuir affinity in the site-J update must be indexed by `J`, not by nonlinear trial counter `I`.

This PASS is intentionally narrower than an admission decision. There is still no qualified B2, historical behaviour remains unknown, no historical fidelity is claimed, and no natural positive `Optcxsl=2` activation exists in the supplied frozen testbank. A separate B3 admission-closeout step would be required to admit the correction under the qualified GOV03 historical-uncertainty route.

No B3 admission is performed. No production source is modified.

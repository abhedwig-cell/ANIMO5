# TCD-024 independent second-line review packet

Work unit: `ANIMO-B3B03R`

Target: `TCD-024`

Class: `B_LOCAL_ALGEBRA_INDEX_SPECIES`

Candidate to review: `work/animo-b3b03-tcd024-slow-langmuir-index-readiness` at `446f57f3aeff6e7db56ce473f0724bdb58cad94f`.

Review status: `REQUEST_PREPARED_NOT_COMPLETED`

This packet exists to make the B3Q01 independent-review gate executable without allowing the authoring activity to mark its own work as independently reviewed. It is not an admission record and contains no production patch.

## Review only this atomic claim

In frozen revision-53 `Transorp.for`, `Conc_unl`, the slow-Langmuir affinity used inside the site update must be indexed by slow-sorption site `J`, not nonlinear trial counter `I`.

Verify independently:

```fortran
legacy:    Yy = One + Parcxsl(3,I) * Avc
candidate: Yy = One + Parcxsl(3,J) * Avc
```

Do not broaden the review into TCD-019, solver redesign, convergence policy, tolerance selection or global phosphorus modernization.

## Frozen identity

Recheck rather than merely trust these authoring-side pins:

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- frozen `Transorp.for` member SHA-256: `65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`;
- canonical TCD register blob: `224acc350fde69d3c4aebed8628c0f945e0b3367`.

The reviewer must independently confirm that `I` is the trial counter and `J` is the slow-site counter, and that the site-array domain is not the trial domain.

## Class-B atomicity review

Confirm that the candidate changes only parameter binding in one local expression and does not require:

- new state;
- changed constitutive physics;
- changed timestep/subdivision policy;
- changed nonlinear stopping rule;
- changed tolerance;
- changed fallback logic;
- changed TCD-019 policy.

If any of those are needed to make the correction work, fail the Class-B atomicity gate and require atomization/reclassification.

## Unequal-site active fixture

Re-evaluate the active microcase independently. Do not use equal site parameters.

Common values:

```text
C   = 0.04
rho = 1
dt  = 1.5
```

Sites:

| site | Qmax | K | qold | r_ads | r_des |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.30 | 2 | 0.010 | 0.20 | 0.02 |
| 2 | 0.90 | 40 | 0.020 | 0.07 | 0.01 |
| 3 | 0.12 | 600 | 0.005 | 0.015 | 0.003 |

Independent equation to review:

```text
qeq_j  = (Qmax_j/rho) * (K_j*C)/(1 + K_j*C)
y_j    = exp(-r_j * (1 + K_j*C) * dt)
qnew_j = qold_j*y_j + qeq_j*(1-y_j)
```

The review must prove that a wrong selector cannot remain numerically invisible for sites 2 and 3. Use unrounded states and transfer terms. Rounded report output is not sufficient.

## SYNQ01 evidence

Review `SYNQ-O006` and `SYNQ-O007` from the pinned SYNQ01 register blob `4c215d19844614de8868380fb03f93268ea4c5d8`.

Do not ignore the B3B03 finding that three shortened SYNQ-O006 displayed numbers differ by one unit in their last displayed decimal from fresh 80-digit evaluation. That display-level representation issue must not be turned into a tolerance.

The reviewer should decide the claim from the equation, unequal-site discriminator and exact integer-domain result, not from those shortened strings.

## Multi-site conservation identity

For the isolated internal transfer control volume, independently check:

```text
Delta P_solution + sum_j(Delta P_slow,j) = 0
```

with no external source or sink.

The B3B03 implementation defines the dissolved counter-transfer as the exact negative of slow-site storage gain. Confirm whether this is a legitimate closed local conservation identity for the isolated transfer and whether it is independent enough from the wrong-index mutation to serve as a cross-check.

Do not infer full coupled phosphorus closure from this local identity.

## Active and inactive controls

Required review controls:

1. active unequal-site `Optcxsl=2` case;
2. zero-rate inactive site, expected `qnew=qold` and transfer `0` exactly;
3. inactive constitutive route using supplied `Optcxsl=3` Freundlich case.

PREP05 reports 55 normalized model outputs and zero differences for the TCD-024-only diagnostic on the supplied Freundlich route. Recheck the evidence and its declared normalization. Do not silently extend that result to all possible inactive configurations.

## Natural activation and prevalence

The supplied frozen active-P cases use `OPTCXSL=3`. No supplied natural case positively activates TCD-024.

The review must retain:

```text
natural_positive_activation = unavailable in supplied frozen testbank
historical_prevalence = UNKNOWN
```

Synthetic activation is causal/coverage evidence, not B2 evidence.

## TCD-019 separation

Use the exact NQ02 authority pinned by B3B03:

- branch `work/animo-nq02-tcd019-nonlinear-p-qualification`;
- head `40a41089020f78ee1d5181b8afc7bdb511af3193`;
- interaction blob `9ca37e90115faab9604a3f3051a8246b5e3a0813`.

Verify that this evidence keeps TCD-019 and TCD-024 separate and does not admit their composition.

Do not float to a similarly named NQ02 development branch without explicitly changing the evidence authority and explaining why.

## Expected-difference review

Directly expected to change only when the target branch is active and `K_J != K_I`:

- site-J kinetic factor;
- site-J slow-sorbed P state;
- site-local P transfer;
- downstream P quantities receiving that transfer.

Expected unchanged:

- branch selection;
- trial/site loop ordering;
- `Recf(J)`;
- TCD-019 fast-sorption numerical policy;
- nonlinear stopping/tolerance/fallback rules;
- `Optcxsl=1` and `Optcxsl=3` routes;
- zero-rate inactive site;
- hydrology;
- unrelated species outside existing P coupling;
- frozen and production source bytes in this readiness workunit.

Any broader intended correction fails this packet's atomic scope.

## Live route review

Before closing review, re-read live PREP02R and GOV02 rather than relying on the packet date.

At packet creation the pinned PREP02R evidence still says:

```text
BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED
reference_qualified = false
external_request_sent = false
```

Therefore neither the normal B2 route nor the GOV02 historical-uncertainty route is currently open. A technical PASS may still be recorded, but B3 admission must remain false.

## Required independent reviewer record

Record at least:

| field | required result |
| --- | --- |
| independent from ANIMO-B3B03 authoring | `true` |
| reviewed branch/head | exact SHA |
| frozen/canonical identity | PASS/FAIL |
| exact source seam | PASS/FAIL |
| Class-B atomicity | PASS/FAIL |
| unequal-site discriminator | PASS/FAIL |
| unrounded state/transfer evidence | PASS/FAIL |
| conservation identity | PASS/FAIL |
| active/inactive controls | PASS/FAIL |
| TCD-019 separation | PASS/FAIL |
| expected-difference/non-interference | PASS/FAIL |
| natural activation limitation retained | PASS/FAIL |
| historical prevalence retained UNKNOWN | PASS/FAIL |
| live admission-route state | PASS/FAIL |
| overall technical second-line result | PASS/FAIL |

A passing independent review still does not admit TCD-024. Admission requires a separately valid B3 disposition route and explicit admission record.

# ANIMO-B3B03 — TCD-024 Slow Langmuir Sorption Site Indexing Admission Readiness

Status: `QUALIFIED_TCD024_CLASS_B_ADMISSION_READINESS_HISTORICAL_ROUTE_BLOCKED_SECOND_LINE_REVIEW_PENDING`

This workunit qualifies only the atomic admission-readiness claim for `TCD-024`. It does not admit corrected legacy behaviour, does not alter production source, and does not modify or compose the `TCD-019` numerical policy.

## 1. Atomic claim

In frozen revision-53 `Transorp.for`, subroutine `Conc_unl`, the slow-Langmuir kinetic exponent is evaluated inside a slow-site loop indexed by `J`, but one site-specific affinity parameter is selected with the unrelated nonlinear trial counter `I`.

The frozen source structure is:

```fortran
Do 1030 I=1,20
...
Do 1050 J=1,Ncxsl
...
If(Optcxsl .Eq. 2)Then
   Yy = One + Parcxsl(3,I) * Avc
   Yy = exp( - Recf(J) * Yy * T )
End If
```

The exact wrong-index expression is:

```fortran
Yy = One + Parcxsl(3,I) * Avc
```

The atomic candidate correction is exactly:

```fortran
Yy = One + Parcxsl(3,J) * Avc
```

No other expression belongs to this claim. `I` is the trial counter. `J` is the active slow-sorption site. `Parcxsl` has only `Macx=3` site columns, while the trial loop can reach `I=20`, so the legacy expression is both semantically wrong and a latent bounds risk when an accepted trial index exceeds the site domain.

## 2. Frozen identity and evidence authority

The frozen B0 identities used by this workunit are:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- documentation SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`;
- `ANIMO_4.1.5.53/Transorp.for` SHA-256 `65ab0f70ed7cc4f1c0012ca95bcdddeb5c26dd21b09df0ec61b7b269e51cd0ad`.

The canonical TCD register blob is `224acc350fde69d3c4aebed8628c0f945e0b3367`; its `TCD-024` classification is `CONFIRMED_LEGACY_WRONG_INDEX_DEFECT_AND_LATENT_BOUNDS_RISK`.

Class semantics come from B3Q01. Under that contract this is a Class B local algebra/index correction because the intended operation is a site-local parameter binding. The claim does not introduce state, constitutive physics, a solver tolerance, a stopping rule, or any other numerical policy.

## 3. Separation from TCD-019

NQ02 independently characterized the four-way interaction between the TCD-019 numerical policy and the TCD-024 index correction. Its status is:

`FOUR_WAY_SYNTHETIC_INTERACTION_CHARACTERIZED_NO_COMPOSITION_ADMISSION`

The evidence separates the mechanisms:

- `TCD-024`: binding of the slow-Langmuir affinity to site `J`;
- `TCD-019`: fast-sorption finite-change consistency and nonlinear stopping policy.

ANIMO-B3B03 therefore evaluates only the TCD-024-only axis. It does not alter TCD-019, does not treat the combined result as the expected result, and does not admit both discrepancies together.

## 4. Predeclared expected-difference surface

Before B3B03 acceptance validation, `integration/animo-b3/TCD024_EXPECTED_DIFFERENCE.json` declared the affected and unaffected surfaces.

Expected direct differences when `Optcxsl=2` reaches the targeted slow-site update and `K_J != K_I` are:

1. site-J relaxation factor `Yy`;
2. updated slow-sorbed P state for the affected site;
3. the corresponding site-local slow-sorption P transfer;
4. downstream dissolved-P and P-only state, balance, restart and reporting surfaces to which that transfer propagates.

Expected unchanged surfaces include:

- option selection and branch triggers;
- trial and site loop ordering;
- `Recf(J)` selection;
- all input parameter values;
- TCD-019 finite-change and stopping policies;
- all tolerances, clipping thresholds and solver controls;
- `Optcxsl=1` linear and `Optcxsl=3` Freundlich slow-sorption routes;
- a site with exactly zero selected kinetic rate;
- hydrological states and water fluxes;
- C and N state/flux/balance families outside existing P coupling;
- all frozen and production source bytes.

Rounded report output is explicitly not an oracle for the active fixture.

## 5. Unequal-site active fixture and unrounded comparison

The active synthetic fixture uses deliberately unequal slow-Langmuir sites:

| site | Qmax | K | qold | r_ads | r_des |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.30 | 2 | 0.010 | 0.20 | 0.02 |
| 2 | 0.90 | 40 | 0.020 | 0.07 | 0.01 |
| 3 | 0.12 | 600 | 0.005 | 0.015 | 0.003 |

with `C=0.04`, `rho=1`, and `dt=1.5`.

The independent per-site equation is:

```text
qeq_j  = (Qmax_j/rho) * (K_j*C)/(1 + K_j*C)
y_j    = exp(-r_j * (1 + K_j*C) * dt)
qnew_j = qold_j*y_j + qeq_j*(1-y_j)
```

B3B03 evaluates this at 80-digit Decimal precision. The unrounded state comparison against a defect-seeding `K_1` selector is:

| site | correct qnew using K_J | wrong-selector qnew using K_1 | discriminator |
| ---: | --- | --- | --- |
| 1 | `0.013382497037579703764323601003327353135602564031862008456803506888922032817413340` | `0.013382497037579703764323601003327353135602564031862008456803506888922032817413340` | equal by construction |
| 2 | `0.14753969645039970073105831290404905178546400628007091356315257450780555441805199` | `0.077231793016630632245642328684096944742583375424392326084530401228142520492628225` | different |
| 3 | `0.052409932714652284323717408180830665689512840129054843302530861570332277037363397` | `0.0076455859493262592189248710070344630901401232826660990593613765090187853437838248` | different |

The corresponding unrounded correct site-transfer rates `(qnew-qold)/dt` are:

- site 1: `0.0022549980250531358428824006688849020904017093545746723045356712592813552116088933`;
- site 2: `0.085026464300266467154038875269366034523642670853380609042101716338537036278701327`;
- site 3: `0.031606621809768189549144938787220443793008560086036562201687241046888184691575598`.

Thus the fixture cannot make the wrong selector numerically invisible through equal site parameters.

## 6. SYNQ01 reconciliation

SYNQ01 provides two applicable oracles:

- `SYNQ-O006`, the per-site slow-Langmuir analytical equation and unequal-site discriminator;
- `SYNQ-O007`, the exact index-domain result that trial `I=1..20` is not a valid site selector for `Nsite<=3`, with the first invalid trial index at `I=4`.

During B3B03 validation, direct 80-digit re-evaluation found a representation inconsistency in three of the shorter numerical strings published in the SYNQ01 register: they differ from the recomputed value by one unit in the last displayed decimal place. This is persisted, not hidden. No tolerance was introduced.

Consequently B3B03 uses the SYNQ01 equation, discriminator and integer-domain oracle as scientific evidence, while its own 80-digit values are the exact numerical fixture values. The shorter SYNQ01 display strings are provenance evidence only and are not used as an acceptance threshold.

This finding does not weaken the wrong-index claim: sites 2 and 3 remain strongly separated from the wrong-selector mutant, and the index-domain proof is exact.

## 7. Multi-site conservation identity

For the isolated internal sorption transfer control volume consisting of dissolved P plus all slow sites, with no external P source or sink during the isolated transfer, the identity is:

```text
Delta P_solution + sum_j(Delta P_slow,j) = 0
```

or equivalently:

```text
solution_counter_transfer + sum_j(qnew_j - qold_j) = 0
```

The B3B03 validator evaluates this as an exact Decimal identity with no tolerance. The sum of the unrounded site-transfer rates also equals total slow-site storage gain divided by `dt` exactly under the same Decimal evaluation.

This is a control-volume qualification identity for the targeted internal transfer. It is not claimed as proof that every coupled P solver seam is already resolved. TCD-019 remains separate.

## 8. Active and inactive controls

### Active control

The unequal three-site `Optcxsl=2` fixture activates the target equation and discriminates site-local `K_J` from a wrong selector for sites 2 and 3.

PREP05 also previously executed a full synthetic three-site slow-Langmuir case with unequal affinities `500`, `1000`, and `2000`. Changing only `Parcxsl(3,I)` to `Parcxsl(3,J)` changed only 11 of 55 normalized model outputs, concentrated in P state/balance/reporting surfaces, while inspected ordinary N and organic-matter families remained unchanged. The TCD-024-only correction removed more than 99.5 percent of the synthetic cumulative P nonclosure, but that residual improvement is supporting causality evidence only, not an admission criterion.

### Inactive site control

A site with `r_ads=0` and `r_des=0` has `qnew=qold=0.005` and transfer `0` exactly under both correct and wrong selector evaluations. This establishes exact site inactivity independent of the affinity selector.

### Inactive constitutive-route control

The supplied LWKM case uses `Optcxsl=3` Freundlich slow sorption. PREP05 ran a TCD-024-only diagnostic copy and compared 55 model outputs against frozen-source GNU diagnostic execution. After only previously declared volatile metadata normalization, differences were exactly `0`, with no missing or extra model outputs.

## 9. Natural activation and historical prevalence

No supplied frozen active-P testcase naturally activates slow Langmuir. All six supplied cases with active P use:

```text
OPTCXSL = 3
```

Therefore there is no natural positive B1 activation of TCD-024 in the supplied frozen testbank. The natural negative control is available and passes, but historical activation frequency or magnitude cannot be inferred from it.

PREP02R currently has no qualified historical B2 artifact for this path. Its live status remains `BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`, and the prepared external request is still recorded as unsent. Under GOV02, the historical-uncertainty route is therefore not open.

The required historical statement is consequently:

```text
historical_prevalence = UNKNOWN
historical_fidelity_claim = false
```

## 10. Non-interference conclusion

Within the evidence available, the correction surface is narrow and consistent with the atomic Class-B claim:

- source change candidate is one index only;
- the active unequal-site probe changes slow-site P state and its P propagation;
- inactive slow site is exactly invariant;
- supplied Freundlich route is output-identical in the diagnostic comparison;
- inspected N and OM families remain unchanged in the active full-case probe;
- TCD-019 policy is not modified;
- no hydrology or production source is touched by B3B03.

The full expected-difference whitelist remains the governing non-interference contract. Any future candidate that changes solver policy, constitutive option selection, tolerances, hydrology, unrelated species, or production source fails this Class-B scope.

## 11. Readiness decision and residual blockers

The atomic technical evidence is sufficient to qualify the TCD-024 Class-B admission-readiness dossier:

`QUALIFIED_TCD024_CLASS_B_ADMISSION_READINESS_HISTORICAL_ROUTE_BLOCKED_SECOND_LINE_REVIEW_PENDING`

This is not B3 admission.

Remaining blockers before any admission decision are:

1. no qualified B2 historical reference for the target path;
2. GOV02 historical-uncertainty entry requirements are not currently satisfied;
3. historical prevalence remains unknown;
4. no independent second-line B3 disposition review has been completed;
5. there is no natural positive `Optcxsl=2` case in the supplied frozen testbank;
6. the SYNQ01 short displayed O006 numbers carry the persisted last-displayed-unit representation inconsistency noted above.

The last item is not converted into a numerical tolerance and does not change the analytical or index-domain claim.

Explicit boundaries at closeout:

```text
production_patch = false
TCD019_policy_changed = false
TCD019_TCD024_joint_admission = false
solver_redesign = false
tolerance_introduced = false
B3_admission = false
historical_prevalence = UNKNOWN
production_migration_admitted = false
```

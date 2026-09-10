# TCD-027 GOV03 Formal B3 Disposition

Work unit: `ANIMO-B3D10`

Target: `TCD-027`

Class: `A_ACCOUNTING_REPORTING_ONLY`

## Scope

This workunit reconciles the already-qualified TCD-027 Class-A readiness claim with the current GOV03 historical-uncertainty route. It does not perform the independent second-line review and does not admit TCD-027.

The atomic claim is limited to the detailed organic-P reporting accumulator slot 24 in `Outbal_calc.for`.

Legacy statement:

```fortran
Bafop(24,Ly)=Bafop(25,Ly)+Dum
```

Candidate statement:

```fortran
Bafop(24,Ly)=Bafop(24,Ly)+Dum
```

No organic-P process physics, physical state, process flux, numerical policy, production source, B4 state or other TCD is in scope.

## Live authorities

The live branch heads were rechecked before authoring:

- central regie: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`
- readiness: `ANIMO-B3A01@b2bac82512fef0fa232e759f0c68b472567c11d5`
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- historical-route authority: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`

Before branch creation, no `ANIMO-B3D10`, TCD-027 disposition branch, independent-review branch or dedicated TCD-027 review issue was found. The only TCD-027 branch found was the qualified B3A01 readiness branch.

Frozen B0 identities remain:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The authoring-context source recheck used the supplied hash-pinned B0 source bytes matching this public identity. That recheck is evidence for this disposition, not the independent second-line review.

## Source-bound slot semantics

The frozen source supports the narrow reporting interpretation directly.

`Outbal_write.for` labels the detailed organic-P `Bafop` channels in order. In that output contract:

- slot 24 is `redis_EXP`;
- slot 25 is `redis_OP`;
- slot 26 is `redis_DOP`;
- slot 27 is `redis_HUP`.

The writer sends this detailed `Bafop` vector to `transfop<profile>.Out` and resets the reporting accumulator after the balance period. This is a detailed reporting surface, not a physical organic-P state owner.

The frozen `Outbal_calc.for` statements give an orthogonal accumulator cross-check:

- organic matter slot 24 self-accumulates: `Bafom(24,Ly)=Bafom(24,Ly)+Adexpl(I,Ln)*Z`;
- organic nitrogen slot 24 self-accumulates: `Bafon(24,Ly)=Bafon(24,Ly)+Dum`;
- organic phosphorus slots 25, 26 and 27 self-accumulate their own prior values;
- only organic phosphorus slot 24 is seeded from slot 25 in the legacy statement.

The local identity is therefore:

`new_slot24 = old_slot24 + current_redis_EXP_increment`

The legacy statement violates this identity by cross-seeding `redis_EXP` from `redis_OP` history.

This source evidence does not justify any broader organic-P correction.

## Natural B1 discriminator and non-interference

The retained PREP06 evidence and B3A01 readiness package identify natural activation in `LWKM_gras_1040.2021.2045`, period 1997.

For the one-expression diagnostic probe:

- legacy `redis_EXP` is approximately `-7.0644 kg/ha P`;
- candidate `redis_EXP` is `0.0 kg/ha P`;
- affected profiles are `GP`, `RP` and `TP`;
- among 58 common top-level outputs, only `transfopGP.Out`, `transfopRP.Out` and `transfopTP.Out` change.

The same bounded evidence reports unchanged:

- physical state trajectory;
- process flux trajectory;
- total organic-P balance;
- total mass balance;
- `redis_OP`;
- `redis_DOP`;
- `redis_HUP`;
- ordinary non-reporting model outputs.

This is causal Class-A readiness evidence. It remains B1 diagnostic evidence and must not be promoted to historical B2.

## GOV03 route reconciliation

The old B3A01 route blocker predates GOV03. B3A01 correctly recorded at its own closeout that no qualified B2 existed and that the historical-uncertainty route had not yet been opened because acquisition was still active.

GOV03 is the later route authority. It qualifies:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

and:

`G6U = ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`

No qualified B2 has appeared. Exact historical revision-53 behaviour for this accumulator remains `UNKNOWN`, and no historical-fidelity claim is made.

For TCD-027, the former B2 route blocker is therefore reconciled as PASS only for use of the B3Q01 historical-uncertainty route. GOV03 does not itself qualify the scientific claim and does not waive independent second-line review.

## B3Q01 sufficiency before review

For the narrow Class-A claim, the presently available package contains:

- fixed B0 source and testcase identities;
- a source-bound exact accumulator identity and writer-slot mapping;
- a dedicated natural causal discriminator in LWKM 1997;
- cross-species and neighbouring-slot accumulator checks that do not depend only on the observed residual becoming smaller;
- a predeclared three-file expected-difference surface;
- state, flux, total-balance and non-reporting non-interference evidence within the B1 diagnostic scope;
- explicit GOV03 acquisition closure and historical uncertainty;
- explicit exclusion of broader organic-P physics and all composition.

This is sufficient to open the formal route for independent review. It is not sufficient for admission because the independent second-line gate is still absent.

## Formal disposition

The disposition remains:

`UNRESOLVED_NOT_ADMITTED`

The route-specific decision is:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_NOW_QUALIFIED_BY_GOV03`

TCD-027 is therefore not admitted. A clean independent review handoff is authorized, but the review must occur in a separate context and must fail closed on any unresolved source, scope, causality, non-interference, route or uncertainty question.

## Hard boundaries

This workunit does not:

- compose TCD-027 with TCD-017, TCD-026, TCD-028 or any other correction;
- change organic-P physics;
- change frozen source or testcases;
- apply a production patch;
- establish B4;
- update central regie;
- claim historical revision-53 behaviour is known;
- perform or self-certify the independent review;
- admit corrected legacy behaviour.

A later credible historical artifact immediately reopens B2 qualification for this scope. A passing independent review would be review evidence only and would still require a separate admission-closeout workunit.
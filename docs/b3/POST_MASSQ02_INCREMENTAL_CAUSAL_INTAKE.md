# ANIMO-B3I03 post-MASSQ02 incremental causal discrepancy intake

Status: `QUALIFIED_POST_MASSQ02_INCREMENTAL_CAUSAL_INTAKE_TCD042_RESERVED_NO_ADMISSIONS`

Canonical admission: `NONE`

Production migration: `NONE`

## 1. Scope and authority

B3I03 consumes completed MASSQ02 causal evidence without reopening the full B3 register and without admitting any correction.

Authority base:

- B3I02 branch `work/animo-b3i02-post-b3i01-incremental-intake`;
- B3I02 closeout head `c1a69c00a02aa0e32ca60580c3d0ebee96442c17`;
- canonical register tail `TCD-041`.

Evidence source:

- MASSQ02 branch `work/animo-massq02-residual-causality-typed-events`;
- MASSQ02 closeout head `56a11b524d03c33ee4ab9b1cd13b2cd523d543fc`;
- 15 records classified `NEW_CAUSAL_FINDING`;
- 0 residuals left `UNEXPLAINED` in MASSQ02.

Causal localization by itself is not enough for canonical allocation. A new TCD still requires one collision-checked phenomenon with a defensible atomic correction boundary. Magnitude is never an admission or allocation criterion.

## 2. Intake result

The 15 MASSQ02 causal records are routed as follows:

- 1 new fail-closed top-level reservation: `TCD-042` from R016;
- 3 P initialization records routed to the existing `TCD-014` parent context, with its existing atomization requirement preserved;
- 1 composite R015 record that contains a known `TCD-016` NH4 component plus a separate NO3 component that remains unassigned;
- 10 records retained without a new TCD because process localization has not yet closed the exact violated implementation or scientific identity.

No correction is admitted and the canonical CSV is not appended in B3I03.

## 3. New reservation TCD-042

RuurloGrass at `TITO=1915` provides the strongest new MASSQ02 evidence.

At `UBoundconc.for:110-132`:

- `Iopthyvs = 0`;
- `Flib(1) = 0`;
- `Rurv = 0`;
- `Flux = Max(0, Flib(1)+Rurv) = 0`;
- the branch sets `A1=1`, `A2=0`;
- the incoming NH4 and NO3 load therefore receives zero transfer weight into the represented top concentration state.

At the same accepted interval `Outbal_calc.for:766-784` books precipitation/deposition input:

- NH4-N `0.005069031338 kg/ha`;
- NO3-N `0.00168034188 kg/ha`;
- total `0.006749373218 kg/ha N`.

The independent MassLedger residual is `0.0067493732130969875 kg/ha N`.

This is sufficient to reserve the canonical discrepancy phenomenon:

`TCD-042 = upper-boundary precipitation/deposition solute transaction at zero top throughflow`

It is not sufficient to select a corrected behaviour.

### Why the parent requires atomization

Three correction semantics remain logically possible and must not be conflated:

1. Class A hypothesis: the external mass has not yet crossed the ANIMO physical boundary when top throughflow is zero, so the ledger/input booking is premature.
2. Class C hypothesis: the external mass crosses immediately and therefore needs a persistent surface/top solute owner while no aqueous throughflow exists.
3. Class B hypothesis: only if an already represented owner should receive the load and one local algebraic transfer expression is demonstrably wrong.

Because Class C is the strictest live possibility, the reservation remains fail-closed under Class C until the boundary semantics are atomized.

## 4. Collision scan

The authoritative register contains `TCD-001` through `TCD-041`. No existing top-level TCD matches R016.

The closest prior local observation is `SQ01-LCL-UBOUNDCONC-DRY-DEPOSITION-1MM`. SQ01 treated the 1 mm UBoundconc threshold as ancillary and did not establish causal relevance. B3I03 does not silently equate that threshold finding with TCD-042. The MASSQ02 event instead proves a natural accepted-interval zero-throughflow input/state-transfer mismatch.

TCD-016 is distinct. It concerns wet-to-dry NH4 continuation-state loss inside `Transsub`.

TCD-018 is distinct. It is a reporting-only interception-storage omission with intact physical hydrology state.

## 5. TCD-014 parent-context evidence

R019, R022 and R023 are first-step P residuals with supplied slow-site state inconsistent with `Copo` and reproduce in the `Transgen` initialization surface.

They are routed to the existing TCD-014 parent context because TCD-014 already governs PO4 initial-state mass accounting and B3Q01 already marks that parent `REQUIRES_ATOMIZATION` between numerical-policy and accounting interpretations.

B3I03 does not create a new top-level P discrepancy and does not invent a new child key. The new cases strengthen natural evidence for the parent while leaving atomization unresolved.

## 6. TCD-015 candidate-family N records

R012, R014, R017 and R018 are nitrate-dominated local `TRANSPORT` nonclosures. They are not promoted to TCD-015 instances because MASSQ02 did not independently prove the exact negative-concentration branch with the `Hv` double-count identity for those events.

R013 additionally activates the `Transsub` zero-order adjustment path, but the exact violated identity is not closed.

R011 is a mixed layer-0 DON/NH4/NO3 local nonclosure and likewise lacks a single atomic mechanism.

These records remain explicit follow-up evidence rather than being merged by routine or species similarity.

## 7. Composite R015

Puitmijn TITO 1490 contains:

- known TCD-016 NH4 component `0.13880242022597072 kg/ha N`;
- additional layer-0 NO3 component about `0.08524873053248594 kg/ha N`;
- negligible layer-1 NO3 compensation.

Only the NH4 component maps to TCD-016. The NO3 component is not widened into TCD-016 and receives no new identifier until its own mechanism is established.

## 8. P and organic-matter records without allocation

R020 is important negative evidence: the documented TCD-019 diagnostic correction did not change the target LWKM P event. Therefore a shared local `Transgen` surface does not justify folding it into TCD-019.

R021 remains a local P nonclosure with TCD-019 context but no closed mechanism.

R024 remains a bounded soil-organic-C projection of a dissolved-organic-matter transport residual. The local process is known, but the violated transport identity is not. No whole-system elemental-C claim is made.

R010 likewise reproduces exactly in the detailed hydrology balance equation, but this identifies the observer/process surface, not a local code or theory defect. It therefore receives no TCD from B3I03.

## 9. Canonical and admission consequences

B3I03 creates exactly one fail-closed reservation:

`TCD-042`

The reservation does not append `docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv`. A separate explicit register-append integration step is required before TCD-042 becomes a row in the central CSV snapshot.

No B3 correction is admitted. No B2 claim is created. No production source is changed.

## 10. Required follow-up

The next high-value scientific work is a focused upper-boundary transaction qualification for TCD-042. It must decide when precipitation/deposition mass crosses the ANIMO system boundary under zero throughflow and whether the correct atom is accounting-only, an existing-owner algebra correction, or a missing-state problem.

Separate follow-ups remain appropriate for:

- exact TCD-015 reachability of the nitrate residual family;
- TCD-014 child atomization using the new natural slow-site initialization evidence;
- unexplained local mechanisms behind R010, R011, R013, R020, R021 and R024;
- the extra NO3 component of R015.

Final B3I03 status:

`QUALIFIED_POST_MASSQ02_INCREMENTAL_CAUSAL_INTAKE_TCD042_RESERVED_NO_ADMISSIONS`

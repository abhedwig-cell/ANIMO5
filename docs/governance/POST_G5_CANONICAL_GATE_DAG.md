# Post-G5 Canonical Gate DAG

Work unit: `ANIMO-RG03`

This document is the RG03 canonical gate topology. It is a governance DAG, not an implementation schedule and not an admission record.

## Core rule

Evidence integration never strengthens evidence. B0 remains B0, B1 remains B1, B2 remains B2, synthetic oracle evidence remains synthetic/non-B2, and a readiness qualification remains readiness.

Historical fidelity and scientific qualification are separate tracks that can exchange constraints without being collapsed.

## DAG

```text
                         RG02 G0-G5
                             |
                  +----------+-----------+
                  |                      |
                GOV02              post-G5 evidence streams
                  |          SYNQ / NQ / SQ / MP / GHG / BUILD
                  |          STATEQ / TIME / TIMEQ / MASS / ARCHG
                  |                      |
                  +----------------------+
                             |
          +------------------+----------------------+
          |                                         |
   HISTORICAL TRACK                         SCIENTIFIC READINESS
          |                                         |
      PREP02R                                      G7 queue
          |                                  (atomic process scopes)
     +----+----+                                    |
     |         |                              class-specific blockers
    G6H       G6U                         theory / numerics / state / runtime
     |         |                                    |
 B2 fidelity  bounded closure               atomic B3 admission attempt
 comparison  eligibility only                        |
     |         |                                      |
     +---- claim-scoped legitimate route ------------+
                                                      |
               +----------------+----------------+----+----------------+
               |                |                |                     |
            GSTATE            GTIME            GMASS                  GEX
               |                |                |                     |
               +----------------+----------------+---------------------+
                                      |
                                    GARCH
                              candidate readiness
                                      |
                                 B4(profile)
                                      |
                                  PRODUCTION
```

The diagram does not mean GSTATE, GTIME, GMASS and GEX are globally serial in that printed order. Their dependencies are profile-scoped and may be qualified in parallel. Cyclic design dependencies are resolved through candidate contracts first, then admitted as a consistent profile. No gate may self-authorize another gate's unresolved scientific semantics.

## Historical track

### G6H

`G6H = B2 historical fidelity acquisition/comparison`

G6H answers historical questions: what did an independently trustworthy historical ANIMO environment do, and does a candidate preserve that behaviour where historical fidelity is claimed?

Current state: `ACTIVE_B2_ACQUISITION_NOT_PASSED`.

PREP02R has not obtained the reference artifact.

### G6U

`G6U = bounded PREP02R acquisition closure`

G6U is an eligibility gate for the stricter historical-uncertainty route. It is not an alternative B2 artifact and does not mark G6H passed.

Current state: `NOT_ELIGIBLE_ACQUISITION_NOT_EXHAUSTED`.

The actual external request has not been sent, so a failed/exhausted acquisition effort cannot be inferred.

## Scientific track

### G7

`G7 = atomic process-scoped B3 qualification`

G7 consumes the B3Q01 class contract, B3I01 canonical identity/routing, and evidence specific to one atomic discrepancy or process scope. Later incremental intake such as B3I02/B3I03 may reserve or route findings but cannot create admission by itself.

G7 has two distinct concepts:

1. readiness to prepare an admission record;
2. actual scientific admission.

Readiness can proceed before G6H/G6U if the scientific, numerical, state and runtime dependencies are independently qualified enough for that bounded work. Actual corrected-legacy admission must still satisfy the claim-scoped route required by GOV02/B3Q01.

No G7 admission exists at the current RG03 refresh.

## Canonical STATE

`GSTATE(profile)`

GSTATE defines the accepted-boundary continuation state for a declared active feature profile.

It requires:

- one owner for each continuation-critical active physical state;
- complete checkpoint representation or a qualified deterministic reconstruction;
- explicit external-owner split;
- exact layout/configuration/state identity;
- event cursor and accepted-boundary semantics tied to canonical time;
- admitted state-model changes for active Class C scopes;
- split-run/restart qualification appropriate to the claim.

STATEQ01 qualifies the structural readiness matrix and checkpoint completeness contracts. STATEQ02 adds direct B0-hash-pinned diagnostic executable evidence for a deliberately restricted `CORE_CNP_WITH_EXTERNAL_CROP` profile: accepted snapshots and post-restore trajectories are bitwise exact across five qualified split boundaries, including one full 833-record remainder. It also fail-closes an active surface/layer-0 sentinel before checkpoint creation.

This is materially stronger GSTATE readiness than STATEQ01 alone, but it is still profile-bounded and non-B2. STATEQ02 explicitly excludes GHG, macropores, active TCD-040 layer-0 restart state, internal-crop restart state, active stable DOM and active P-class state. Those exclusions remain real blockers for profiles that enable them. Canonical STATE admission still requires a separate admission authority and compatible canonical TIME/external-owner binding for the claimed profile.

Current state: `RESTRICTED_CORE_EXECUTABLE_CHECKPOINT_SEMANTICS_QUALIFIED_ADMISSION_BLOCKED`.

## Canonical TIME

`GTIME(profile)`

TIME02 selects the candidate `NORMALIZED_EXACT_RATIONAL_CIVIL_DAY_COORDINATE` under calendar contract `ANIMO_PG_86400_NOLEAPSECONDS_V1`.

Canonical event comparisons use exact identities. No hidden epsilon and no floating tolerance may define calendar semantics.

TIMEQ01 qualifies the candidate transaction/scheduler state machine synthetically. TIMEQ02 qualifies schema-driven synthetic external-owner transactions. Neither is B2 or production evidence.

GTIME still depends on the admitted state/external-owner profile and real producer adapter qualification. Historical event-boundary equivalence additionally requires the historical track where that equivalence is claimed.

Current state: `CONCRETE_CANDIDATE_QUALIFIED_ADMISSION_BLOCKED`.

## Canonical MASS

`GMASS(profile)`

MASSQ01 proves an observer-only B1 projection can be attached without physical-output interference across its qualified case set. MASSQ02 then reconciles the current residual evidence set without correcting residuals: 23 nonzero records are classified, 15 are new causal findings and zero remain unexplained. It also qualifies a candidate typed-event projection with explicit source/destination owners and no legacy balance accumulator as authoritative physical state or event owner.

The MASSQ02 candidate is not a canonical runtime event journal. B3I03 conservatively routes the 15 new causal findings and reserves only `TCD-042`; it performs no register append and no admission. Existing mass-relevant TCDs, nested soil/crop closure, active macropore/GHG feature closure and whole-system elemental-C completeness remain open.

GMASS therefore requires canonical active state owners and admitted transfer/process identities. It must include active feature control volumes. GHG and macropore ledger gaps cannot be hidden by choosing a smaller observer volume while still claiming those features.

Legacy balance accumulators remain report/comparison evidence, not authoritative storage owners.

Current state: `TYPED_EVENT_PROJECTION_AND_RESIDUAL_RECONCILIATION_QUALIFIED_ADMISSION_BLOCKED`.

## External exchange

`GEX(profile)`

ARCH05 and ARCH07 define candidate external exchange/adapter contracts. TIMEQ02 executes synthetic hydrology and external-crop producer fixtures.

Canonical GEX additionally requires producer-specific real adapter qualification, exact time/state identity binding, and feature-compatible semantics. No real SWAP/WATBAL or external-crop production adapter is qualified by TIMEQ02. STATEQ02's qualification-only replay/rebind is executable evidence for restart identity in its restricted profile, not a production producer adapter admission.

Current state: `SYNTHETIC_CONTRACT_FIXTURE_QUALIFIED_REAL_ADAPTER_BLOCKED`.

## Architecture readiness

`GARCH`

ARCHG01 consolidates ARCH01 through ARCH07. ARCHG02 revalidates that candidate architecture against final TS01/TIME01 temporal semantics and passes its structural audit.

GARCH therefore records candidate architecture readiness:

`QUALIFIED_CANDIDATE_ARCHITECTURE_REVALIDATED`

This is not a production implementation gate. It does not admit canonical state, time, mass, exchange, science, or B4.

## B4

`B4(profile)` may only be constructed from admitted upstream scopes.

Minimum composition rule:

```text
B4(profile) =
  admitted G7 atoms for every included process/feature
  + admitted GSTATE(profile)
  + admitted GTIME(profile)
  + admitted GMASS(profile)
  + admitted GEX(profile) where external ownership is used
  + qualified GARCH
  + explicit historical-fidelity/uncertainty metadata
```

No readiness-only result can be promoted during composition. No last-writer-wins merge can replace a stronger owner document or discrepancy register.

Current state: `NOT_ADMITTED`.

## Canonical discrepancy routing

The B3I01 canonical append surface still ends at `TCD-041` at this RG03 refresh. Appends were reconciled as append-only identity/routing updates. They create no scientific admission.

B3I03 is later incremental causal intake over MASSQ02. It reserves `TCD-042` fail-closed for the upper-boundary precipitation/deposition solute transaction at zero top throughflow and explicitly requires atomization before admission. B3I03 performs no canonical append, so the authoritative register tail remains `TCD-041`. RG03 tracks the TCD-042 reservation separately and does not insert it into the canonical queue prematurely.

RG03 therefore routes TCD-028 through TCD-041 from the canonical register, even where the initial B3I01 closeout only reserved TCD-028 through TCD-037. Later state and runtime supplements are treated as additional canonical identity evidence, not as retrospective strengthening of the original findings.

## Fail-closed invariants

RG03 requires all of the following:

- B2 remains mandatory for historical fidelity/equivalence claims.
- G6U cannot become eligible while the actual bounded acquisition action has not occurred.
- B1 and synthetic evidence cannot be relabelled B2.
- B3 readiness is not B3 admission.
- a fail-closed TCD reservation is not a canonical register append and not an admission.
- canonical STATE, TIME, MASS and EX remain separate gates.
- Class C state gaps cannot be repaired as reporting-only fixes.
- Class E numerical policy cannot be selected from smaller residual alone.
- composition cannot increase evidence strength.
- a canonical TCD append cannot mutate prior rows through last-writer-wins.
- B4 and production remain closed until their explicit profile dependencies are admitted.

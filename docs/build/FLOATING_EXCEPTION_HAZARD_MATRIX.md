# ANIMO-BUILDQ01 — Floating Exception Hazard Matrix

Status: `QUALIFIED_GNU_OBSERVATION_WITH_HISTORICAL_EFFECTS_EXPLICITLY_UNRESOLVED`

## Classification vocabulary

- `IEEE_FLAG_ONLY`: observed nontrapping execution sets an IEEE flag without demonstrated state/output change.
- `CONTROL_FLOW_MATERIAL`: exception handling or evaluation can alter continuation/termination or select a branch.
- `STATE_MATERIAL`: arithmetic result can directly change physical or numerical state.
- `OUTPUT_MATERIAL`: arithmetic result can directly change reported output without necessarily changing physical state.
- `HISTORICAL_EFFECT_UNKNOWN`: historical Intel runtime effect has not been established.

A row can carry more than one materiality label because GNU nontrapping behavior and a trapping environment can differ.

| ID | Location/expression | GNU evidence | Qualified classification | Historical Intel | Action boundary |
|---|---|---|---|---|---|
| FPE-001 | `MAPOTRANSPORT.FOR:670`, `Abs(BaDev)>1e-5 .AND. Abs(BaDev/BaMx)>0.005` | MP02 active cases set `IEEE_INVALID_FLAG`. BUILDQ01 exact-expression probe with 0/0: branch false, invalid flag true, ratio NaN. With `-ffpe-trap=invalid,zero,overflow`: SIGFPE at the guard. | `IEEE_FLAG_ONLY` for observed normal GNU execution; `CONTROL_FLOW_MATERIAL` under trapping FP environment; no normalized output difference observed by MP02 | `HISTORICAL_EFFECT_UNKNOWN` | Do not repair here. Future code must avoid relying on short-circuit/evaluation order, but corrected behavior requires separate admission. |
| FPE-002 | PREP01 baseline underflow/denormal events | PREP01 records underflow/denormal notes in diagnostic runs without promoting them to model defects | `IEEE_FLAG_ONLY` on available GNU evidence | `HISTORICAL_EFFECT_UNKNOWN` | Keep as runtime diagnostic evidence unless state/output materiality is demonstrated. |
| FPE-003 | `TRANSPORT.FOR:264`, relative balance deviation divided by `max(abs(Bapd),abs(Batr))` | source recheck shows an enclosing `IF` requires `Abs(Bapd)>1e-30 .OR. Abs(Batr)>=1e-30` before the division is reached | `ZERO_SCALE_DIVISION_GUARDED_FOR_FINITE_INPUTS`; not retained as a zero/zero FPE candidate | not needed for this closed zero-scale hypothesis | Reopen only for independent NaN/Inf-domain evidence. |
| FPE-004 | `Transgen.for:379`, same relative balance pattern | enclosing `IF` requires `Abs(Bapd)>1e-5 .OR. Abs(Batr)>=1e-5` before the division | `ZERO_SCALE_DIVISION_GUARDED_FOR_FINITE_INPUTS`; initial static suspicion closed | not needed for this closed zero-scale hypothesis | Reopen only if non-finite upstream state is independently established. |
| FPE-005 | `ghgtransport.for:263`, gas-transport balance relative deviation | enclosing `IF` requires `Abs(Bapd)>1e-30 .OR. Abs(Batr)>1e-30` before the division | `ZERO_SCALE_DIVISION_GUARDED_FOR_FINITE_INPUTS`; initial static suspicion closed | not needed for this closed zero-scale hypothesis | Keep separate from GHG domain risks involving non-finite or physically invalid state. |
| FPE-006 | `ghg_n2o.for:483,560`, terms containing `AvCoNO3/RatFacN2O` | no explicit positive-domain guard at expression; no qualified runtime event | `HISTORICAL_EFFECT_UNKNOWN`; potential `STATE_MATERIAL` because result feeds N2O reduction rates | `HISTORICAL_EFFECT_UNKNOWN` | Requires scientific domain/reachability qualification. Compiler flags are not a fix. |
| FPE-007 | `Transorp.for:1121` and analogous nonlinear convergence predicates with `Dif/rsc`, `Dif/avc`, `Dif/tau` in compound logical expressions | source-level evaluation-order sensitivity; NQ02 independently establishes nonlinear P numerical-policy sensitivity, not this FPE as a defect | `HISTORICAL_EFFECT_UNKNOWN`; potential `CONTROL_FLOW_MATERIAL` and then `STATE_MATERIAL` via solver path | `HISTORICAL_EFFECT_UNKNOWN` | Keep under NQ02/TCD-019 routing unless independent runtime-semantic evidence justifies separate intake. |
| FPE-008 | `Transsub.for:267`, compound logical with `(Hv1*Vsmall-Hv2)/(Hv1*Co-Hv2)` | source risk only | `HISTORICAL_EFFECT_UNKNOWN`; potential `CONTROL_FLOW_MATERIAL` | `HISTORICAL_EFFECT_UNKNOWN` | Reachability and denominator-domain probe required before classification increase. |

## Reconciliation of initially over-broad balance-check suspicion

The first BUILDQ01 pass grouped the relative balance checks in `TRANSPORT`, `Transgen` and `GHGtransport` with the MP02 `MAPOTRANSPORT` guard. That was too broad. Reinspection of the full enclosing control flow shows that all three execute the relative division only after an outer test establishes a strictly positive finite scale threshold for at least one of `Bapd` or `Batr`. Therefore `max(abs(Bapd),abs(Batr))` cannot be zero on that path for finite inputs.

These rows are retained in the matrix to record closure of the candidate, not as open hazards. The MP02 expression remains different because the potentially invalid division is itself inside a compound `.AND.` and is not structurally dominated by a separate denominator-domain guard.

## MP02 reconciliation

The macropore finding is now narrower than a generic “GNU invalid operation” statement. The source expression is a balance-warning guard, not the macropore transport state update itself. Under the observed nontrapping GNU runtime, the 0/0 produces NaN, raises invalid, and the comparison does not enter the warning branch. MP02 found no normalized-output nondeterminism from this seam. Therefore the available GNU evidence supports `IEEE_FLAG_ONLY` for ordinary execution.

That is not the whole portability story. When invalid exceptions trap, the same expression terminates execution, so it is also `CONTROL_FLOW_MATERIAL` with respect to floating-point environment. Historical Intel evaluation and exception-mask behavior for the actual executable remain unknown. BUILDQ01 therefore does not use this warning seam to infer intended science or to admit a source correction.

## Evaluation-order rule for ANIMO5

Future ANIMO5 code must not use `.AND.` or `.OR.` as a safety guard for an operation that is invalid outside the guarded domain. Safe-domain tests and arithmetic must be structurally sequenced. This is a language/runtime contract, not a change to scientific equations.

## Gate

No row in this matrix authorizes a production numerical correction. Materiality can only be increased by source reachability plus controlled runtime evidence and, for scientific-rate expressions, domain/science qualification.

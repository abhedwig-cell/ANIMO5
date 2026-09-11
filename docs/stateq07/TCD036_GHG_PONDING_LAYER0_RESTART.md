# ANIMO-STATEQ07 — TCD-036 GHG pre-existing ponding layer0 restart-state qualification

## Question

Can the revision-53 layer0 GHG restart gap be resolved from the already serialized total-system layer0 state, without adding a new physical GHG store?

## Frozen-source lifecycle

GHG01 established that revision 53 serializes and reloads gas-specific total-system state for indices `0:Nl`, including layer0, but `Inicalc` reconstructs aqueous `Co` only for soil layers `1..Nl`.

The active GHG transport code distinguishes two ponding situations through `Ln1 = 1-Flpn`:

- when `Ln1 == 0` and `Pn < 1.0d-4`, a new ponding event is present and `Co(0)` is explicitly initialized from inflow concentrations;
- when ponding already exists and that new-event condition is false, transport does not overwrite `Co(0)` before solving.

For an active ponding layer, the source explicitly defines total-system and aqueous concentrations to be identical because the air concentration belongs to the atmosphere:

`AvCs(0) = AvCo(0)` and `RsCs(0) = RsCo(0)`.

Therefore, for pre-existing active ponding at a restart boundary, the serialized total-system owner already contains the exact aqueous concentration needed by the next transport step.

## Qualified owner/reconstruction rule

For frozen revision 53, `IoptGHG >= 1`, active pre-existing ponding (`Ln1 == 0` and not the source-defined new-ponding initialization case):

- the gas-specific serialized layer0 total-system concentration is the accepted checkpoint owner;
- the gas-specific layer0 aqueous concentration is a derived identity view;
- restart reconstruction is `Co(0) = Cs(0)` and the accepted dissolved alias is likewise synchronized to the same accepted owner value before normal continuation;
- CH4 and N2O remain separate species;
- no new physical storage is introduced.

For a new ponding event (`Pn < 1.0d-4` under active ponding), the source-defined inflow initialization remains authoritative and this workunit does not replace it.

When ponding is absent, revision-53 transport sets layer0 total result state to zero; this workunit does not create dormant layer0 GHG storage in that state.

## Executable oracle

The bounded oracle checks:

- pre-existing ponding with nonzero CH4 or N2O: exact owner reconstruction preserves `Co0 == Cs0`;
- zero-gas control;
- absent-ponding control with zero layer0 state;
- new-ponding control remains owned by the source inflow initialization, not the restart identity;
- omission/zero-reset in a pre-existing nonzero ponding state differs from exact reconstruction;
- CH4 and N2O are never cross-mapped.

This is source-derived B1 evidence, not B2 and not a whole-model split-run baseline.

## Classification consequence

The B3Q04 queue marked TCD-036 `C provisional` while layer0 owner/reconstruction was unresolved. The bounded source identity above resolves that state question without adding, splitting or redefining physical storage. A later readiness workunit may therefore assess a Class-B local restart reconstruction of an existing owner, while retaining Tier-C review risk because restart semantics affect future trajectories.

## Excluded scope

- TCD-035 soil-layer phase reconstruction, already separately admitted;
- any dormant ponding state when ponding is absent;
- new-ponding event initialization beyond preserving its existing source rule;
- TCD-032, TCD-033 and TCD-034;
- canonical STATE admission;
- checkpoint file-format migration;
- full-model activated-GHG split-run equivalence;
- historical revision-53 magnitude;
- production source changes, B4 or production migration.

Historical behavior remains `UNKNOWN_WITHOUT_B2`.

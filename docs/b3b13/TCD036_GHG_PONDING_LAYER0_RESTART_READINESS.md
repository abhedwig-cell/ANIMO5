# ANIMO-B3B13 — TCD-036 GHG pre-existing ponding layer0 restart admission readiness

## Purpose

This workunit determines whether the bounded state-ownership result qualified by `ANIMO-STATEQ07@26f6e61da328a5578b9c4b332de04eb99a3ac04f` is sufficiently specified for a separate atomic B3 admission decision.

It performs no B3 admission and changes no production source.

## Candidate identity

The only candidate is:

`TCD036_PRE_EXISTING_ACTIVE_PONDING_LAYER0_GHG_RESTART_IDENTITY_FROM_SERIALIZED_TOTAL_SYSTEM_OWNER`

For each gas independently, CH4 and N2O:

- accepted checkpoint owner: serialized total-system layer0 concentration `Cs(0)` / accepted result `RsCs(0)`;
- derived aqueous layer0 view: `Co(0)` / `RsCo(0)`;
- for active pre-existing ponding, the source identity is `Cs(0)=Co(0)`, therefore restart reconstruction is `Co(0)=Cs(0)`;
- no second persistent aqueous checkpoint owner is introduced.

## Lifecycle scope

The candidate is intentionally narrower than all GHG restart behavior.

Included:

- revision-53 GHG active;
- layer 0 only;
- CH4 and N2O separately;
- active pre-existing ponding.

Excluded:

- soil layers 1..Nl, already handled by TCD-035;
- a new ponding event, where source inflow initialization remains authoritative;
- no-ponding state, where no dormant layer0 GHG state is created;
- TCD-032, TCD-033 and TCD-034;
- checkpoint-format redesign;
- canonical ModelState admission;
- whole-model split-run equivalence;
- production migration.

## Classification and review tier

B3Q04 classified TCD-036 as `C provisional` while layer0 ownership/reconstruction was unresolved. STATEQ07 resolves the scientific ownership question without adding physical state. The readiness candidate therefore uses:

`B_LOCAL_RESTART_RECONSTRUCTION_EXISTING_OWNER`

This does not lower the review risk. Restart/checkpoint semantics can alter future trajectories, so the strictest applicable GOV05 review tier remains:

`C_RESTART_CHECKPOINT_SEMANTICS_FUTURE_TRAJECTORY`

## Evidence strength

Evidence consumed here is:

- hash-pinned frozen revision-53 source semantics through GHG01;
- STATEQ07 source-shaped executable B1 oracle;
- STATEQ07 exact-final CI.

The B1 oracle is not B2. Historical revision-53 runtime behavior remains `UNKNOWN_WITHOUT_B2`.

## Admission-readiness predicates

A later atomic B3 admission may be opened only if all of these remain true:

1. the candidate is bounded to active pre-existing layer0 ponding;
2. CH4 and N2O retain independent gas identities;
3. `Cs(0)` remains the accepted serialized owner and `Co(0)` remains a deterministic identity view;
4. new-ponding source inflow initialization is not overridden;
5. no dormant layer0 store is introduced when ponding is absent;
6. TCD-035 and TCD-032..034 are not reopened;
7. B1 evidence is not promoted to historical B2;
8. no full-model split-run, canonical-state, B4 or production claim is made.

## Intended disposition

If exact-head CI and GOV05 adversarial review pass, the readiness disposition is:

`READY_TCD036_BOUNDED_PRE_EXISTING_PONDING_LAYER0_RESTART_FOR_SEPARATE_ADMISSION`

This disposition is not itself an admission.

# ANIMO-SQ06 — TCD-016-C1 dry-hold scientific process qualification

## Scope

This workunit asks one bounded model-evolution question: which physical law, if any, governs `M_surface_NH4_non_aqueous_continuation` during a dry period before any separately qualified rewetting transition? It does not change production source, frozen B0 evidence, the canonical discrepancy register, the central B3 queue or the central testbank registry. It performs no B3 admission and does not qualify rewetting.

The continuation owner remains the SQ02 state: kg N m-2, independent of represented aqueous volume and deliberately chemically noncommittal. SQ03 permits exact persistence when no process is active but explicitly does not interpret that persistence as physical inertness. MASSQ04 keeps the owner explicit in `S_NH4 = S_aq + S_complex + S_cont` and forbids the observer from reconstructing physical state from a residual.

## Evidence boundary

The frozen revision-53 source archive is identified by SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`. The ANIMO 4.0 User's Guide is identified by SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`. The guide is ANIMO 4.0 documentation, not exact revision-53 theory and not historical B2 behaviour.

Relevant guide evidence is bounded. Pages 17-18 separate the nitrogen-cycle pools and processes but do not define a dry non-aqueous surface residual-NH4 store. Page 21 defines aqueous transport and soil solid-phase contents and separately identifies the artificial additions reservoir. Pages 25-26 describe moisture response for soil biological transformations and nitrification, which demonstrates process dependence on environmental state but does not map those soil processes to the continuation owner. Page 43 defines soil-horizon NH4 sorption. Page 46 identifies `CONHTOP` as the virtual top layer used for additions. Pages 49-50 define `FRVO` as an NH4 volatilization fraction of an addition event. SQ04 already established that these revision-53 routes cannot be reused unchanged as the continuation process.

No external literature is invoked in SQ06. That is deliberate, not a claim that relevant literature does not exist. Before a literature law can be applied, the continuation owner would need a qualified physical phase/speciation, interface and activation domain. Assigning those here merely to enable a published formula would be new unqualified model semantics.

## Adversarial hypothesis test

H0, exact conservative dry hold, is not qualified as physics. Its numerical identity is already the fail-closed no-process update from SQ03. Neither absence of a qualified process nor exact conservation proves that the physical process rate is zero.

H1, volatilization, remains scientifically plausible in the abstract but is not currently mappable. `FRVO` belongs to an addition event and is not a kinetic law for pre-existing continuation mass. A continuation volatilization law would need qualified NH3/NH4 speciation, gas-exchange geometry, activation variables, a rate law, parameter provenance and an atmospheric boundary transfer.

H2, binding or sorption into another owner, cannot be selected because no surface receiver and no binding law are qualified. Reusing soil sorption unchanged is excluded by SQ04, and choosing a receiver would violate the receiver-neutral SQ03 envelope.

H3, nitrification or another N transformation, cannot be selected because the current state is not qualified as microbially accessible soil NH4. ANIMO 4.0 soil nitrification has moisture, temperature and pH response, but there is no qualified mapping from the continuation owner into that process domain or a daughter-owner transition.

H4 has no additional explicit bounded candidate in the frozen evidence or existing authorities. Inventing a phase, receiver, coefficient or calibration parameter is not acceptable.

Therefore H5 is selected: no dry-hold process law is currently scientifically qualifiable.

## Qualified negative result

`NO_DRY_HOLD_PROCESS_LAW_SCIENTIFICALLY_QUALIFIED`

The resulting workunit outcome is `QUALIFIED_NEGATIVE_NO_DRY_HOLD_PROCESS_LAW_CURRENTLY_DEFENSIBLE`.

The existing no-process persistence remains operationally valid and exactly conservative, but only as fail-closed state semantics. During such an interval no dry-process event, owner transition or external boundary term is emitted. `M_surface_NH4_non_aqueous_continuation` remains a required persistent restart state. This says nothing about the true physical rate in nature.

No process parameter is introduced. No receiver is selected. No historical ANIMO behaviour is inferred. Historical behaviour remains `UNKNOWN_WITHOUT_B2`.

## Evidence that can reopen the dry-process question

A later positive qualification needs evidence that resolves the missing model semantics, for example recovered comprehensive ANIMO theory that explicitly defines the dry continuation process, or new model-evolution evidence that identifies the phase/speciation and interface and supplies a bounded process law with independently traceable parameters. Process-specific observations must distinguish the candidate mechanism from competing loss or transformation routes. Total mass closure by itself is insufficient.

The normal next workunit is separate rewetting qualification: receiver, activation envelope and kinetics. SQ06 does not preselect any of them.

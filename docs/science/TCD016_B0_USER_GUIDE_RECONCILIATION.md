# ANIMO-SQ05 - TCD-016-C1 B0 user-guide reconciliation

Target: `TCD-016-C1`

Base: `ANIMO-SQ04@063627cddd478904c437c9c47f02513ef0d9326b`

This workunit uses the supplied ANIMO 4.0 User's Guide only as bounded documentary evidence. It does not modify production source, the frozen B0 artifacts, the canonical register or the B3 queue.

## Evidence identity

The locally available PDF re-hashed exactly to:

`ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

This matches `ANIMO-B0-DOC-UG40-2005` in the repository B0 evidence register. The document is *User's guide of the ANIMO 4.0 nutrient leaching model*, Alterra Report 224, 2005.

The evidence register explicitly limits this guide to ANIMO 4.0. It is therefore documentary authority for 4.0 concepts and input semantics, not an exact design specification for 4.1.5 revision 53.

## Reconciliation findings

The guide materially corroborates the state-separation conclusions from SQ02-SQ04:

- page 17 places additions/removals at or above the system boundary and soil states below it;
- page 18 shows mineral NH4-N and adsorbed NH4-N as distinct nitrogen-cycle states, but does not identify a dry residual surface-NH4 pool;
- page 21 defines dissolved transport and solid-phase contents as soil-system terms, while separately describing an artificial additions reservoir above the compartment division and a ponding-layer solute balance for surface runoff;
- page 46 defines `CONHTOP` as NH4-N concentration in a virtual top layer used for additions, distinct from `CONH` for compartments 0-NL;
- pages 49-50 tie `FRVO` to material-addition events and to the NH4-N fraction of those additions.

These statements support the earlier conclusion that `Conhtop/Rsconhtop`, soil sorption and `Frvo` are not semantically interchangeable with residual ponding NH4 mass.

## What the guide does not supply

A bounded full-document search found no explicit ANIMO 4.0 contract for:

- a persistent non-aqueous NH4 continuation owner for layer 0 after complete disappearance of ponding water;
- the physical or chemical identity of such a state;
- a dry-period transformation law for such a state;
- a rewetting/remobilization law for such a state;
- a generic rule that applies `FRVO` to pre-existing residual surface NH4;
- a rule that transfers the residual directly into a soil-sorption owner when ponding vanishes.

This negative documentary result is not proof that such physics cannot exist. It means the supplied guide does not authorize it.

## Scientific decision

SQ05 qualifies the following narrow conclusion:

`ANIMO_4_0_USER_GUIDE_CORROBORATES_EXISTING_STATE_AND_PROVENANCE_SEPARATION_BUT_DOES_NOT_DEFINE_TCD016_C1_DRY_CONTINUATION_OR_REWETTING_PROCESS`

Therefore the SQ03 fail-closed process envelope remains the strongest qualified model-evolution contract. SQ04's rejection of unchanged reuse remains intact. No new process law, receiver, kinetic coefficient, volatilization fraction, transition threshold or historical behavior is admitted.

Historical behavior remains `UNKNOWN_WITHOUT_B2`.

`TCD-016-C1` and parent `TCD-016` remain `UNRESOLVED_NOT_ADMITTED`; E1 remains blocked.

## Remaining evidence route

The guide itself points to more comprehensive model-theory sources. A future process-law workunit must therefore use one of the following before selecting new physics:

1. recovered comprehensive ANIMO theory that explicitly defines the missing state/process; or
2. an explicitly declared ANIMO5 model-evolution decision with independently justified process theory, parameters, application envelope, ordering, observables and falsification tests.

Absence of a rule in the user guide is not permission to invent one.

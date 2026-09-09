# TTUTIL adapter policy for ANIMO-IO01

## Decision

TTUTIL 4.27 is **not** a replacement parser for the revision-53 ANIMO text grammar.

ANIMO5 shall keep two explicitly versioned representation paths:

1. `LegacyRevision53TextAdapter`
2. `TTUTILNativeTextAdapter/v1`

Both may normalize to the same narrow configuration objects, but they do not share an accepted surface grammar.

## LegacyRevision53TextAdapter

This adapter owns historical revision-53 compatibility. For the DIRECT/`animo.ini` pilot it must preserve the observed source behaviour:

- first seven characters must be exactly `Animo40` or `Animo41`;
- selector records are interpreted as fixed `A4,A80` records;
- filename extraction follows legacy `Strip` behaviour, including the requirement for a closing double quote;
- unknown four-character selectors are ignored in legacy mode, with provenance/diagnostic recording in the normalized dump;
- duplicate known selectors use the last assignment;
- `MES=` with an empty normalized filename is an immediate parser error;
- absent `MES=` selects the legacy `message.Out` default;
- `CHE=` records the phosphorus-file binding and the legacy `Flipo` presence flag;
- `STE=` records the soil-temperature binding and activates the corresponding option;
- required binding validation remains feature-dependent and occurs before physics.

The legacy adapter does not call TTUTIL merely to make the implementation look uniform. Doing so would risk widening historical syntax and would not improve the DIRECT grammar.

## TTUTILNativeTextAdapter/v1

The native adapter is a **new representation**, not a compatibility mode. It uses TTUTIL 4.27 name-based typed input and maps fields into the same normalized `LegacyInputBinding` object.

The native representation must:

- carry an explicit schema/version identifier;
- use symbolic names rather than the legacy four-character fixed selector stream;
- reject unknown or duplicate semantic keys according to its own versioned schema policy;
- reject missing mandatory bindings before physics;
- never inherit legacy last-wins or ignore-unknown behaviour accidentally;
- remain separate from binary hydrology, restart/checkpoint state, external crop forcing and other adapter classes already classified as specialized.

## Equivalence claim

A representation-only claim means that, for the same intended configuration, both adapters produce field-exact normalized objects with the same units, presence flags, defaults and feature bindings. It does **not** mean that the two input grammars accept the same malformed or ambiguous text.

For legacy input, historical accept/reject behaviour remains authoritative. For native TTUTIL input, the v1 schema contract is authoritative.

## Admission sequence

1. qualify exact legacy DIRECT normalization and negative cases;
2. qualify a native TTUTIL DIRECT fixture using the pinned official TTUTIL 4.27 source;
3. compare normalized `LegacyInputBinding` dumps field by field;
4. only then classify Pilot A as a representation-only adapter candidate;
5. proceed to Pilot B MATERIAL only after Pilot A closes.

No science semantics, binary hydrology representation, GHG lineage or production migration is admitted by this policy.

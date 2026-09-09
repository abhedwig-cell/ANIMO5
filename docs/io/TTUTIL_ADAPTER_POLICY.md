# TTUTIL adapter policy for ANIMO-IO01

## Decision

TTUTIL 4.27 is **not** a replacement parser for the revision-53 ANIMO text grammar.

ANIMO5 keeps two explicitly versioned representation paths:

1. `LegacyRevision53TextAdapter`
2. `TTUTILNativeTextAdapter/v1`

Both may normalize to the same narrow configuration objects, but they do not share an accepted surface grammar.

## LegacyRevision53TextAdapter

This adapter owns historical revision-53 compatibility. For the DIRECT/`animo.ini` pilot it preserves the defined source behaviour:

- first seven characters must be exactly `Animo40` or `Animo41`;
- selector records are interpreted as fixed `A4,A80` records;
- filename extraction follows legacy `Strip` semantics where those semantics are defined;
- unknown four-character selectors are ignored in legacy mode, with provenance/diagnostic recording in the normalized dump;
- duplicate known selectors use the last assignment;
- a defined blank `MES=` result is an immediate parser error 1016;
- absent `MES=` selects the legacy `message.Out` default;
- `CHE=` records the phosphorus-file binding and the legacy `Flipo` presence flag;
- `STE=` records the soil-temperature binding and activates the corresponding option;
- required binding validation remains feature-dependent and occurs before physics.

The adapter does not invent deterministic semantics for a revision-53 runtime-undefined edge. If a payload is empty or whitespace-only but quoted, `Strip` can leave `Istart=0` while `Ilast>0`, after which the source forms `Fname(0:Ilast)` even though `Fname` is declared with indices starting at 1. This is classified `FAIL_CLOSED_NOT_NORMALIZED`; it must not be rewritten as a guaranteed legacy error code or accepted value.

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

A representation-only claim means that, for the same intended configuration, both adapters produce field-exact normalized objects with the same presence flags, defaults and feature bindings. It does **not** mean that the two input grammars accept the same malformed or ambiguous text.

For legacy input, defined historical behaviour remains authoritative. Runtime-undefined legacy behaviour is explicitly excluded and fails closed. For native TTUTIL input, the v1 schema contract is authoritative.

## Pilot A qualification

Pilot A has completed the bounded admission sequence:

1. legacy DIRECT normalization and negative cases are implemented and tested;
2. the exact official TTUTIL 4.27 source is hash-pinned and materialized from the supplied SWAP 4.3.1 distribution;
3. a native TTUTIL DIRECT probe is compiled against that source;
4. all 10 natural `animo.ini` cases in the frozen testbank produce field-exact equivalent `LegacyInputBinding/v1` semantic projections;
5. the undefined quoted-empty `Strip` edge is explicitly excluded rather than normalized.

Pilot A is therefore classified `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE` for the DIRECT routing object only.

Pilot B MATERIAL may proceed as a separate bounded qualification. No science semantics, binary hydrology representation, GHG lineage or production migration is admitted by this policy.

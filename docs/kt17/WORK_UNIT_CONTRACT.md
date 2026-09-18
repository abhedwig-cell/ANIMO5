# ANIMO-KT17 Work Unit Contract

Workunit: `ANIMO-KT17 - Accepted Checkpoint Manifest Integrity, Build Identity & Evidence Binding Qualification`.

Execution discipline: `RECONCILE -> ARCHITECTURE BINDING -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT17 closes the next bounded restart-integrity gap identified by KT16 without selecting a disk checkpoint format or admitting canonical restart.

KT16 proved that the bounded KT15A accepted application aggregate is sufficient for exact in-memory split-run continuation. KT17 adds:

- deterministic canonical in-memory preimages for the immutable application configuration and KT16 accepted checkpoint;
- an internally computed SHA-256 implementation;
- a cryptographic payload digest;
- a cryptographic manifest digest;
- explicit build-commit identity binding;
- explicit frozen source, testbank and documentation evidence identities;
- feature-set and diagnostic-policy identity.

## Program authority

Current program rebaseline:

`ANIMO-RG07@c60dd36a38a2030e4f4ac1925f95b2966a6d1c87`

Exact-final RG07 CI:

`35379875781 = success`.

Accepted checkpoint candidate:

`ANIMO-KT16@7cd863b71a7a7fcc985514a8af28dcb69cae999a`.

Restart architecture design basis:

`ANIMO-ARCH02@a079d93c965f6073586c55ee4b3544dd8873b723`.

ARCH02 remains candidate architecture, not canonical restart authority.

## Integrity scope

KT17 wraps one valid KT16 checkpoint in `kt17_checkpoint_envelope_t`.

The envelope records:

- envelope schema;
- hash algorithm;
- canonicalization contract;
- bounded feature-set identity;
- diagnostic-continuation policy;
- producer build commit identity;
- frozen source archive SHA-256;
- frozen testbank SHA-256;
- frozen documentation SHA-256;
- canonical application-configuration SHA-256;
- canonical KT16 checkpoint-payload SHA-256;
- manifest SHA-256;
- the KT16 accepted checkpoint itself.

## SHA-256 implementation

KT17 implements SHA-256 in Fortran and validates it against standard known-answer vectors for:

- empty input;
- `abc`;
- the standard multi-block `abcdbc...nopq` message.

No external hashing executable or library is required for runtime verification.

## Canonical integrity preimage

The integrity preimage is an in-memory canonical ASCII grammar, not a checkpoint file format.

Primitive values are represented with explicit type tags:

- strings are length-prefixed;
- integers use fixed 64-bit hexadecimal bit identity;
- REAL64 values use their exact IEEE binary64 bit pattern;
- logicals use explicit 0/1 identity;
- TIME02 coordinates encode calendar id, day index, numerator and denominator;
- arrays encode extent followed by every element in order.

This avoids locale-sensitive decimal formatting and tolerance-based identity.

## Immutable configuration inspection seam

KT15A stores application configuration in a public type with private fields. KT17 adds one read-only inspector to the KT15 module so the existing immutable configuration can be canonically hashed without making its internals mutable.

The inspector:

- validates the config first;
- only copies values out;
- changes no science, ownership, equality or execution behavior.

KT17 CI reruns KT15 and KT16 regression harnesses after this change.

## Evidence identity boundary

The following evidence identities are hard-bound into KT17:

- source archive: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- documentation: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

KT17 checks that the manifest contains exactly those identities.

It does NOT read those source artifacts and recompute their SHA-256 values. Therefore it qualifies evidence-identity binding, not source-byte custody verification.

## Build identity boundary

The producer build identity is a canonical 40-character lowercase Git commit identifier.

The encode path records the supplied build id, and verify/restore require an independently supplied expected build id to match exactly.

KT17 does not introspect the running executable to discover its own Git commit. Build identity is therefore externally asserted and internally bound, not runtime-attested.

## Verification order

Restore is allowed only after:

1. envelope/schema/policy validation;
2. expected build-id match;
3. frozen evidence-identity match;
4. exact expected application-config match;
5. recomputed application-config SHA-256 match;
6. recomputed KT16 checkpoint-payload SHA-256 match;
7. recomputed manifest SHA-256 match;
8. ordinary KT16 internal checkpoint validation.

Only then does KT17 delegate to the trusted KT16 restore path.

## Negative qualification

Tests reject at least:

- checkpoint science-payload mutation;
- declared payload-digest mutation;
- manifest-digest mutation;
- source-evidence identity mutation;
- feature-set mutation;
- wrong expected build commit;
- wrong expected immutable application config.

## Hard boundaries

No file I/O.
No disk/binary checkpoint format.
No claim that evidence source bytes were rehashed.
No claim that the running executable self-attested its build commit.
No canonical checkpoint admission.
No canonical state admission.
No historical B2 restart claim.
No trial or mid-step checkpoint.
No process-science change.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.

## Governance

This remains a cross-module accepted-application restart/integrity candidate and is conservatively GOV04 Tier D.

Same-agent review may qualify the implementation candidate only as:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Genuine independent Tier D review remains required before any admission.

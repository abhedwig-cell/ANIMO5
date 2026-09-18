# ANIMO-KT17 Qualification Rationale

KT16 established state sufficiency and exact split-run continuation but deliberately left checkpoint integrity and identity out of scope. KT17 adds those mechanics without pretending that an in-memory integrity preimage is already a portable checkpoint file format.

The core distinction is between three kinds of evidence:

1. checkpoint content integrity, which KT17 can recompute itself;
2. immutable application-configuration integrity, which KT17 can recompute itself;
3. external artifact/build identity, which KT17 can bind and compare but cannot independently rediscover from source bytes or the running executable.

The first two are cryptographically verified inside the bounded runtime candidate. The third remains identity binding.

This distinction prevents a hash-shaped string from being mistaken for source custody proof.

The SHA-256 primitive is implemented directly and checked against standard known-answer vectors. The checkpoint and config preimages use exact bit identities rather than formatted floating-point values.

KT17 modifies the KT15 module only to add a validating read-only configuration inspector. The existing KT15 and KT16 harnesses are rerun in KT17 CI to prove this introspection seam does not change their qualified behavior.

A positive KT17 qualification means:

`THE_BOUNDED_KT16_ACCEPTED_CHECKPOINT_CAN_BE_WRAPPED_IN_AN_IN_MEMORY_MANIFEST_WITH_RECOMPUTABLE_SHA256_CONTENT_INTEGRITY_AND_EXACT_BUILD_EVIDENCE_CONFIGURATION_IDENTITY_BINDING`.

It does not mean:

- the checkpoint has a canonical disk format;
- source/testbank/documentation bytes were rehashed by the runtime;
- the executable self-attested its Git commit;
- canonical restart is admitted;
- independent Tier D review has occurred;
- production is open.

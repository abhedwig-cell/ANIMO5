# ANIMO-KT16 Qualification Rationale

KT15A provides a coherent accepted application aggregate whose science state, cross-module continuation and immutable execution configuration all have one accepted meaning. KT16 tests whether that aggregate is sufficient to stop after an accepted interval and continue later without changing the bounded result.

The checkpoint intentionally serializes concepts, not bytes. Its in-memory typed record is enough to test state sufficiency and exact restore behavior without prematurely choosing a file format.

The restore path does not directly fabricate private application internals. It reconstructs the accepted science store through the trusted KT02 reconstruction API and then re-enters KT15A through its public initialization/validation boundary.

The expected configuration is supplied separately at restore and must exactly match the configuration stored in the checkpoint. This is the fail-closed configuration-identity check required before continuation.

The split-run qualification is exact. The uninterrupted and restored paths must end with bit-identical bounded science and continuation state after the second interval.

A positive qualification means:

`THE_BOUNDED_KT15A_ACCEPTED_APPLICATION_AGGREGATE_IS_SUFFICIENT_FOR_EXACT_IN_MEMORY_CHECKPOINT_RESTORE_AND_SPLIT_RUN_CONTINUATION`.

It does not mean canonical ANIMO5 checkpoint/restart has been admitted. In particular, ARCH02's future manifest integrity and whole-model ownership requirements remain open.

# ANIMO-KT21 Qualification Rationale

KT21 converts an architectural warning into quantified real-source evidence.

The first LWKM packet has zero runoff. Revision-53 detailed hydrology does not assign `Runinu` in that branch. The same is true for the following near-zero-runoff packets. Because `Runinu` is an in/out continuation value and enters the upper-boundary hydrology/load calculation, source-faithful characterization must remain unresolved until a later branch explicitly assigns it.

The pinned sequence does not encounter such a branch until zero-based packet 347, endpoint day 3531, where positive runoff assigns `Runinu=0`.

After that reset, the remaining sequence can be characterized without any assumption about the historical first-call value. The result is strongly diagnostic: the modern provider/runtime architecture can carry real hydrology, but the current TCD-042 scientific envelope covers only a small subset of the deterministic real sequence.

That means the next scientific question is not how to make the adapter accept more packets. It is whether the missing scientific envelopes are already represented by other admitted TCDs, require additional source/theory qualification, or represent model-evolution decisions.

A positive KT21 qualification means only:

`THE_PINNED_LWKM_SEQUENCE_HAS_A_REPRODUCIBLE_BOUNDED_HYDROLOGY_ENVELOPE_CHARACTERIZATION_WITH_THE_FIRST_CALL_RUNINU_UNCERTAINTY_PRESERVED`.

It does not make the real sequence runnable end-to-end.

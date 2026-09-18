# ANIMO-KT13A Composition Coherence Remediation

KT13A is a narrow pre-independent-review remediation of the KT13 bounded TCD-042 composition candidate.

Two cross-module coherence issues were identified before Tier D review.

First, HYDROEXEC01 uses `start_context%he_top` in the revision-53 upper hydrology algebra while KT12 uses the separately supplied `hetop` in TCD-042. KT13 did not require those two geometry coordinates to be identical. A caller could therefore execute one composed interval with two different top-layer thicknesses.

KT13A adds an exact binary64 identity guard:

`hetop == start_context%he_top`

before hydrology binding or science execution. No tolerance is introduced.

Second, KT13 previously changed `success` back to false if post-commit diagnostics were unexpectedly unavailable after `run_interval` had already committed the KT02 transaction. That could make the API report failure after accepted state had changed. KT13A records commit truth first and never rewrites a successful commit into a false transactional failure. Diagnostic validity is exposed separately in the trace.

The finite-positive end-to-end test is strengthened with exact binary64 end-state and average-concentration oracles. A new negative test verifies that mismatched top geometry fails before KT06 binding and preserves the accepted store exactly.

No frozen upstream implementation is modified. No scientific equation, TCD-042 admission predicate, threshold, tolerance, state ownership, B3 object, TB7, B4 or production authority is changed.

KT13A is same-agent technical remediation only. It does not satisfy the required independent Tier D review.

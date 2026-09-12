# ANIMO-B3D42 — TCD-019 Restricted Numerical Policy Atomic B3 Admission

This workunit performs only the separate B3 admission decision for the bounded numerical policy qualified by `ANIMO-NQ05@62080a8e731681407e2e7e759decc49c1a47fa7b`.

Target: canonical top-level `TCD-019`.

Candidate admitted identity:

`TCD019_FAST_LANGMUIR_EXACT_STORAGE_REPRESENTATION_STABLE_TWO_VARIABLE_ROOT_NO_LEGACY_FALLBACK_BINARY64_POLICY`

The scope is exactly the NQ05 envelope: fast Langmuir `Optcxfa=2`; slow sorption `Optcxsl in {1,3}`; constitutively consistent fast start state; finite nonnegative binary64 state; cancellation-safe exact Langmuir secant with no delta switch; reconstructed `C_unl` two-variable equations; state-local slow-rate selection; NQ04/B3D36 `Iflsol=4` coefficient policy; representation-stable discrete root acceptance with immediate-neighbour residual guard; fail closed otherwise; no legacy fallback.

Representation stability is a binary64 acceptance predicate, not a proof of global convergence. NQ05 does not establish whole-model physical adequacy or coverage of every timestep.

Historical revision-53 corrected behavior remains `UNKNOWN_WITHOUT_B2`. NQ02 diagnostic and synthetic evidence are not B2.

Authorities: RG05N `8758bd30e302b75dd7854ac00fd2e29473669a13`; B3Q05 `997d867a2b107ec8e28efce530c82a204719de46`; B3I01 `383c7a83e84a578969f92113280dc715b7bdddb4`; GOV05 `f65a47724e4a4fca7f2d8b8d6de9eeee51867904`; GOV04 `1bbe4c211197590f346803106e45dca5faae79fc`; GOV03 `cbd262bdabe92923113b7326f2f42822ce9a971c`; B3Q01 `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

B3D40 and B3D41 are the first two exact-final post-RG05N admissions. If B3D42 becomes exact-final green, it is the third and reaches the normal aggregate cadence. A separate RG05O integration workunit is then required before any fourth post-RG05N scientific admission.

Hard boundaries: no production source; no frozen-B0 change; no canonical-register change; no central-queue or aggregate-regie change here; no fast Freundlich; no slow Langmuir/TCD-024; no TCD-014 initialization admission; no fallback tolerance or global tolerance; no legacy fallback; no B4; no production migration; no historical-fidelity claim.
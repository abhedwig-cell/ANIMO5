# ANIMO-KT05 Reconciliation

KT05 starts from the clean KT03 closeout head:

`c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`

This base already contains:

- the qualified nonproduction KT02 model-neutral runtime prototype;
- the frozen KT03 file-independent hydrology-step contract;
- the separated legacy provenance design;
- the explicit Hlpimp=11 interception-state evidence.

## Relevant live delta

KT03F01 has since been corrected to a GOV04 Tier-C review checkpoint because the Hlpimp=1 missing-state disposition still requires genuinely independent second-line review. KT04 therefore fails closed on Hlpimp=1.

KT05 avoids that dependency entirely. It advances only the explicit-state path, where interception storage is actually present in the producer contract.

## Why a separate Fortran adapter

KT03 proved the boundary using a Python diagnostic carrier/parser. The next architecture question is whether the same file-independent contract can be expressed at the language boundary where ANIMO science actually lives.

KT05 therefore moves one step closer to real ANIMO integration without migrating or rewriting the legacy science:

`normalized typed packet -> compiled Fortran ANIMO call-boundary projection`.

This is intentionally narrower than executing `Hydro_detailed`. The projection must first be correct, bounded and file-independent before any scientific-routine wrapper is attempted.

## Reuse relation

KT05 reuses the **contract**, not SWAP-specific science. It does not change KT02 runtime mechanics and does not import SWAP solver, forcing-file or timestep policy.

Current phase: `IMPLEMENT`.


## Implemented boundary

The first implementation is a compiled Fortran contract adapter only. It mirrors the full normalized KT03 packet sufficiently to validate the frozen schema and then projects the bounded producer-derived subset required at the `Hydro_detailed` call boundary.

No file framing, `Hlpimp`, record hash, SWAP solver policy, ANIMO accepted state or scientific transformation is carried into the adapter. Interception storage is mandatory in KT05, so the unresolved Hlpimp=1 route cannot enter this workunit.

The implementation was compiled locally before persistence with GNU Fortran 14.2 using `-std=f2008 -Wall -Wextra -Werror -fcheck=all`; the test executable passed. Repository qualification still depends on exact-head CI and review.

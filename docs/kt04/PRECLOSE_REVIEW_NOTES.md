# ANIMO-KT04 Pre-close Review Notes

The implementation has been challenged in successive fail-closed passes rather than treating CI success as sufficient.

## Initial hardening

The first implementation at `7111ebc969fff927240a3c5532a2e322402814c9` passed CI run `35284103015`.

Its first review found that a free policy string could over-authorize typed producers, the projection carrier contained a mutable dictionary, and the supplementary build evidence incorrectly encoded an absent project property as false. Those points were remediated at `94ad6473711dc1136f41ff8ce6c7ebd147fd3aa8`, which passed CI run `35284238167`.

## Second hardening

### KT04-R1, medium: direct projection construction did not require an exact field set or coherent profile shape

A manually constructed projection could omit a required external field or provide incoherent profile vectors and still pass the interception-only validation.

Disposition: remediated by exact absent/explicit field-set validation plus `Mofrt/Flev/Flab/Fldr` shape checks.

### KT04-R2, medium: ANIMO-owned transformation context accepted non-finite values

A NaN in accepted-state/context data could propagate through the diagnostic transformation.

Disposition: remediated by explicit finite context validation.

The second remediation at `708738dca426bfa4eba6a8c374995619ed234fbf` passed CI run `35284458112`.

## Third hardening: source-order fidelity

### KT04-R3, high: the first top-boundary probe allowed caller-supplied values for terms that the source computes or imports

The original helper accepted both `flab1_before_correction` and `flab2` as context and also accepted the layer-1 drainage total as context. That proves file/typed symmetry only under an arbitrary shared context; it does not faithfully encode the source sequence.

Revision-53 `Hydro_detailed` first computes preliminary `Flab(1)` from imported `Flab(2)`, imported `Evso`, imported `Flev(1)`, summed imported `Fldr(:,1)` and ANIMO-owned state terms. It then computes `Dif`, clamps `Evso`, and recomputes `Flab(1)`.

Disposition: remediated by deriving `Flab(2)` and the layer-1 drainage total from the projection, deriving preliminary `Flab(1)` in source order, then applying `Dif -> Evso -> final Flab(1)`. The helper also checks runoff split closure against imported `Ru`.

## Accepted boundary

The pinned `ProjectionAuthority` object is a semantic contract reference, not a cryptographic proof that a producer is entitled to use that contract. Python callers can deliberately construct or reuse an allowed authority token. KT04 therefore does not claim producer authentication. Composition code remains responsible for supplying only a qualification authority valid for that producer.

The top-boundary helper is still a bounded source-equation probe. It does not execute `Hydro_detailed`, `Modflux`, macropore logic, the whole profile, or solute transport.

## Review continuation

After the third hardening commit and exact-head CI, the final adversarial review must re-check authority ownership, file/typed symmetry, absent-state non-fabrication, explicit-state lifecycle, source-order fidelity, frozen KT03 payload, and the bounded nonproduction scope.

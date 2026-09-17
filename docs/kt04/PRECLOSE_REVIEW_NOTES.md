# ANIMO-KT04 Pre-close Review Notes

The first implementation at `7111ebc969fff927240a3c5532a2e322402814c9` passed CI run `35284103015`. The first remediation at `94ad6473711dc1136f41ff8ce6c7ebd147fd3aa8` passed CI run `35284238167`.

Pre-close adversarial inspection then challenged the remediated contract rather than treating CI success as sufficient.

## Findings requiring a second hardening pass

### KT04-R1, medium: direct projection construction did not require an exact field set

`HydroDetailedProjection.validate()` checked interception semantics but did not require the complete expected external field set. A manually constructed projection could therefore omit an unrelated required field and pass validation until a later operation failed with an incidental lookup error.

Disposition: remediated by exact absent/explicit field-set validation.

### KT04-R2, medium: ANIMO-owned transformation context accepted non-finite values

The bounded top-boundary evaluator validated the projection but not its ANIMO-owned context. A NaN in accepted-state/context data could therefore propagate through the diagnostic transformation instead of failing closed.

Disposition: remediated by explicit finite context validation.

## Accepted boundary

The pinned `ProjectionAuthority` object is a semantic contract reference, not a cryptographic proof that a producer is entitled to use that contract. Python callers can deliberately construct or reuse an allowed authority token. KT04 therefore does not claim producer authentication. Composition code remains responsible for supplying only a qualification authority valid for that producer.

This is acceptable for the nonproduction contract proof, provided closeout does not say that possession of an authority string independently qualifies a future SWAP5 provider.

## Review continuation

After the second hardening commit and exact-head CI, the final adversarial review must re-check these findings plus the original file/typed symmetry, absent-state non-fabrication, explicit-state lifecycle, frozen KT03 payload, and bounded `Dif -> Evso -> Flab(1)` scope.

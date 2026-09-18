# ANIMO-KT09 Reconciliation

KT09 branches from closed KT08:

`281dc65cbaceaa61d31f9cb731b3c5a733ca5d57`.

No equivalent KT09 branch existed before the safe-parallel work was opened.

The main runtime lane remains at KT06. Its frozen implementation target remains
`fc818917a46408d55cd7f03e2fa8257534683907` and it still requires a genuinely
independent GOV04 Tier C review. KT09 therefore does not import or modify KT06.

The eight selected packet identities are the exact anchor identities already
frozen by KT08. Local rematerialization from the pinned user-supplied LWKM
`SWATRE.UNF` reproduced all eight KT08 typed-step and dynamic-group hashes
before the fixture was persisted.

The decompressed complete-anchor bundle is independently pinned by SHA-256:

`fcb306cb4661139be0bc425db8fd4ff3d1d8d696a1a485c22dd6c67f5bb662b2`.

Evidence remains B1 because normalization still uses the frozen KT03
diagnostic `Dble_trunc` reproduction and does not establish historical Intel
compiler equivalence.

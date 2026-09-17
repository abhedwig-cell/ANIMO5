# ANIMO-KT05 Reconciliation

KT05 is deliberately branched from the closed KT03 authority `c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`, not from KT03F01 or KT04.

This avoids importing the unresolved Hlpimp=1 scientific claim.

Current relevant authorities:

- KT02 closed nonproduction model-neutral runtime: `1f88db4dc87fc4d93075884ac35a59711f0725bf`;
- KT02 frozen executable: `1909709e7a244b5d0ee53342a26bab74815c118c`;
- KT03 closed file-independent hydrology exchange contract: `c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT03 frozen contract implementation: `e844c7658a95819fc0463c55737f9bd41b29a6da`;
- KT03F01 current state: independent Tier C review required; not consumed here.

KT03 explicitly states that producer endpoint/duration metadata are not authoritative runtime time. KT05 implements the first bounded adapter-level mapping proof for the explicit-state path.

The mapping is intentionally whole-day and exact. Any need for fractional producer coordinates or subday runtime intervals is deferred to a separate qualification surface rather than hidden behind a tolerance.

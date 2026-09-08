# ANIMO5 architecture invariants

Version: PREP01-v1, 2026-09-08.

These are programme design invariants, not claims about the legacy implementation.

1. One ANIMO computational kernel serves standalone and coupled use.
2. The kernel is fully independent of file I/O.
3. Parameters, state, forcing, numerical configuration, exchange data, scratch, diagnostics, and results are explicit and separated.
4. Persistent state is compact and contains only continuation-critical model state.
5. Scratch is owned per worker/job rather than global mutable context.
6. State/layout decisions must scale to many logical columns.
7. State transitions support checkpoint, trial, commit, and rollback.
8. Rejected trials do not alter committed state.
9. Time advances generically over `[t0,t1]`.
10. No implicit daily or calendar semantics are introduced unless a physical process explicitly requires them.
11. Mass conservation is a hard invariant.
12. SWAP-ANIMO coupling uses explicit exchange contracts.
13. ANIMO does not depend on internal SWAP state.
14. SWAP does not depend on internal ANIMO state.
15. WOFOST coupling uses explicit ownership and exchange contracts.
16. Dependency reduction is achieved through coherent data ownership, not global mutable context.
17. Physical configuration and numerical policy are separate.
18. Precision is explicit numerical policy.
19. Diagnostics are part of runtime evidence and qualification.
20. Optional functionality consumes persistent state and computational work only when active, within practical implementation limits that must be measured.
21. Documentation, theory, code, and evidence remain traceable and reconcilable.
22. Status A is designed as an intermediate quality gate and Status AA as the long-term target.

## Invariant change control

Any later change must state why the invariant is insufficient or incorrect, which evidence triggered the change, which workstreams and tests are affected, and whether the change alters scientific semantics, numerical policy, or coupling contracts.

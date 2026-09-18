# ANIMO-KT08 Reconciliation

KT08 branches from closed KT07 at
`24dc3164c7832963d0b8931a8edf5155879a3f8d`.

No KT08 or equivalent full-LWKM-sequence evidence branch existed at workunit
start.

The KT06 runtime-binding branch remains unchanged at
`a31c057842d80f8f3724bedbb19817f869073053` with frozen review target
`fc818917a46408d55cd7f03e2fa8257534683907`. Its checkpoint still says
`NOT_YET_QUALIFIED_UNDER_GOV04_TIER_C`, and no independent KT06 review branch
was present during reconciliation.

KT08 therefore follows the explicit KT06 safe-parallel route: evidence/tooling
that does not consume KT06 as qualified authority.

Local materialization from the pinned user-supplied LWKM source produced the
following complete-sequence identities:

- packet count: 1800;
- ordered typed-step digest sequence:
  `c17319d5a014d498335ed6d6736d0f10adffc4dc30fd3722b220e77dc2eaa5e4`;
- ordered dynamic-group digest sequence:
  `40664a5fa73a980ad00b044bbce543b571b0e9302356f4b889dae2802deb2e34`;
- ordered temporal-and-digest record sequence:
  `eb14311a997129df4ae590ea1c72baecadcc2991ec0c3e8e313ed4ba3720ddc1`.

The normalized sequence starts at producer origin 0 d and closes at endpoint
18263 d with zero chain discontinuities. The duration histogram is 8 d: 37,
9 d: 13, 10 d: 1400 and 11 d: 350.

All claims remain B1 because the frozen KT03 `Dble_trunc` reproduction is
diagnostic and the historical compiler/executable path is not independently
replayed here.

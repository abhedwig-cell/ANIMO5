# ANIMO-KT07 Work Unit Contract

Workunit: `ANIMO-KT07 — LWKM Full Explicit Hydrology Packet Derived Fixture`.

Execution discipline: `RECONCILE -> ACQUIRE/MATERIALIZE -> QUALIFY -> REVIEW -> CLOSE`.

## Purpose

KT07 strengthens the evidence between the frozen KT03 legacy-file adapter and
the qualified KT05 compiled explicit-state hydrology boundary.

The bounded question is:

> Can the complete first explicit-state LWKM `HydrologyStep`, derived from the
> pinned Hlpimp=11 `SWATRE.UNF` bytes through the frozen KT03 diagnostic
> normalization, be represented as an immutable B1 fixture and consumed without
> loss by the frozen KT05 compiled validator, projection and legacy-slice mapper?

This is evidence/tooling qualification only. It changes no scientific process
semantics and does not consume KT06 as qualified authority.

## Authorities

- KT03 authority:
  `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT05 closeout:
  `3319e57adbf6036a86684f8e26d9559454c07b82`;
- KT05 frozen implementation:
  `69dd607ba1efa28de3f83cc963526021352b3311`;
- pinned LWKM `SWATRE.UNF` SHA-256:
  `b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`.

The first dynamic logical-record group is independently pinned in the derived
fixture by SHA-256:
`2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7`.

## Evidence boundary

The committed fixture is B1 derived evidence. The raw B0 producer file is not
added to the repository.

Normalization uses the already documented KT03
`legacy_dble_trunc_diagnostic`. That function is diagnostic and is not B2
Intel/compiler authority. KT07 therefore cannot and does not claim historical
executable equivalence.

The fixture contains the complete normalized first packet, including all
surface scalars, 30-layer `Sc`, `Mofrt`, `Flev`, 31-boundary `Flab`,
5x30 `Fldr`, explicit `Sict`, and 30-layer soil temperature.

## Qualification proof

The fixture must be machine checked for schema, dimensions, provenance pins and
the frozen KT03 typed-step digest.

A generator converts the JSON fixture into a temporary Fortran module during
tests. The generated `hydrology_step_t` must:

1. pass the frozen KT05 explicit-state validator;
2. pass the frozen KT05 `Hydro_detailed` external projection;
3. preserve every projected scalar and array exactly;
4. pass the frozen KT05 legacy-slice mapper;
5. preserve all ANIMO-owned index-zero legacy slices.

## Governance

KT07 changes evidence and verification tooling only. It does not change state,
runtime, restart, numerical policy, scientific algebra, production source or
composition. GOV04 scientific Tier B/C/D independent-review gates are therefore
not invoked by this workunit.

Same-agent adversarial review remains required and must be labelled
`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Exclusions

No B2 claim, no Hlpimp=1 semantics, no `Hydro_detailed` execution, no
scientific admissibility, no KT02/KT06 runtime integration, no SWAP5 in-memory
provider, no retry/timestep policy, no production migration, no B3/B4
admission, and no Status A/AA claim.

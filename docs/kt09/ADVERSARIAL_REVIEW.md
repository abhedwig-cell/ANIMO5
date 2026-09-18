# ANIMO-KT09 Same-Agent Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`

Frozen evidence/tooling head reviewed:

`e54fc115fabb58da5e79fad33e1359717a5ed19c`

Exact-head CI:

`35293001679 -> SUCCESS`

## Review verdict

`PASS_B1_REPRESENTATIVE_REAL_LWKM_PACKET_COMPILED_KT05_CONSUMPTION`

No material finding remains open.

KT09 is an evidence/tooling workunit. It changes no production source, ANIMO
scientific process, accepted-state ownership, runtime time authority, retry
semantics, restart semantics, numerical policy or coupling composition.

## Fixture provenance and identity

PASS within the declared B1 scope.

The eight complete packet fixtures are derived from the pinned LWKM
`SWATRE.UNF` source:

`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`

The canonical decompressed KT09 bundle is independently pinned by:

`fcb306cb4661139be0bc425db8fd4ff3d1d8d696a1a485c22dd6c67f5bb662b2`

and its persisted compressed-text representation by:

`bb28e4f8ce0a23dfad497c4c52c4916fd6c30b322ad66b326db09d7d88f2ea13`.

The integrity test reconstructs every packet as a frozen KT03
`HydrologyStep`, reruns validation, recomputes each typed-step digest and
cross-checks every anchor against the corresponding KT08 dynamic-group and
typed-step identities.

Anchor 0 is additionally checked for exact normalized-payload parity with the
qualified KT07 first-real-packet fixture.

## Representative envelope

PASS.

The frozen anchor indices are:

`0, 2, 5, 41, 449, 899, 1349, 1799`.

Together they cover:

- first and final producer packets;
- all four observed producer duration classes: 8, 9, 10 and 11 d;
- quarter, midpoint and three-quarter positions;
- both zero and nonzero explicit interception-storage endpoints.

This is representative coverage, not a claim that all 1800 packets were
compiled through KT05.

## Frozen KT05 compiled consumption

PASS for all eight representative packets.

Each complete real-derived packet:

1. passes `validate_hydrology_step_explicit`;
2. passes `project_hydro_detailed_explicit`;
3. preserves every KT05-projected scalar exactly;
4. preserves `Mofrt`, `Flev`, `Flab` and `Fldr` exactly;
5. passes `apply_projection_to_legacy_slices`;
6. preserves ANIMO-owned index-zero legacy slices.

The generated Fortran fixture is produced with round-trip decimal REAL64
literals from the pinned normalized JSON values. This verifies lossless
consumption of the B1 normalized evidence by the frozen KT05 carrier. It does
not establish historical Intel/compiler B2 equivalence.

## Historical CI failures

Two pre-qualification CI failures occurred and are classified as
`TOOLING_VALIDATOR_FAILURE`.

Run `35292838414` failed because generated Fortran parameter-array lines
exceeded the free-form source line limit under `-Werror=line-truncation`.
The generator was changed to emit wrapped array constructors. No fixture value
or evidence identity changed.

Run `35292901652` then reached the KT09 test and failed because
`-Werror=compare-reals` rejected an exact REAL inequality expression used
only to record whether a nonzero interception-storage anchor was present. The
test expression was rewritten using an absolute-value check. No fixture value,
adapter, projection or scientific claim changed.

The resulting head
`e54fc115fabb58da5e79fad33e1359717a5ed19c`
passed the complete workflow in run `35293001679`.

## Scope and authority review

PASS.

KT09 does not consume KT06 as qualified authority. It does not define:

- runtime packet selection;
- retry-aware forcing identity;
- timestep subdivision;
- forcing lifetime or caching;
- calendar conversion;
- accepted-state publication;
- scientific admissibility.

KT09 therefore cannot satisfy or bypass KT06's genuinely independent GOV04
Tier C runtime review.

## Evidence strength

The evidence class remains:

`B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2`

The KT03 `legacy_dble_trunc_diagnostic` remains diagnostic-only. The raw B0
producer bytes are externally supplied rather than committed, so CI validates
the persisted B1 fixture and its independent identities rather than replaying
the historical producer executable.

## Final disposition

`SELF_REVIEW_PASS_B1_REPRESENTATIVE_COMPILED_CONSUMPTION_TOOLING_ONLY`

Open material findings: none.

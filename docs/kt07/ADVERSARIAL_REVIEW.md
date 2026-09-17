# ANIMO-KT07 Same-Agent Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Frozen implementation/remediation head reviewed:

`2d469e0a00071b73207112222199eef82c96a961`

Exact-head CI:

`35288769233 -> SUCCESS`

The workflow re-ran the frozen KT03 adapter tests, frozen KT05 compiled-adapter
tests, KT07 fixture-integrity checks, generated-Fortran compilation and full
packet projection/slice-mapping tests, and JSON validation.

## Review verdict

`PASS_B1_DERIVED_FULL_LWKM_PACKET_FIXTURE_AND_COMPILED_KT05_CONSUMPTION`

No material finding remains open.

This is an evidence/tooling qualification. It is not an independent scientific
review and does not alter scientific, runtime, restart, numerical or production
semantics.

## Provenance and identity

PASS within B1 scope.

The fixture pins three independent identities:

- raw supplied LWKM `SWATRE.UNF` SHA-256
  `b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`;
- first dynamic logical-record group SHA-256
  `2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7`;
- normalized typed-step digest
  `eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c`.

After KT07-R1 remediation, the typed-step digest is pinned outside the mutable
fixture both in the integrity test and in the raw-source materializer.
Coordinated fixture-plus-digest drift therefore fails closed.

## Complete packet coverage

PASS.

The fixture contains the complete first normalized explicit-state Hlpimp=11
LWKM packet required by the frozen KT03 contract:

- all surface scalars;
- 30 `Sc` values;
- 30 `Mofrt` values;
- 30 `Flev` values;
- 31 `Flab` values;
- 5 by 30 `Fldr` values;
- explicit `Sict`;
- 30 soil temperatures.

The integrity validator reconstructs a KT03 `HydrologyStep`, validates it and
recomputes the independently pinned typed-step digest.

## KT05 compiled consumption

PASS.

The temporary generated Fortran carrier is consumed by the frozen KT05
implementation without changing KT05 itself.

The exact derived packet:

1. passes `validate_hydrology_step_explicit`;
2. passes `project_hydro_detailed_explicit`;
3. preserves every projected scalar and array represented in the fixture;
4. passes `apply_projection_to_legacy_slices`;
5. leaves ANIMO-owned index-zero legacy slices unchanged.

This strengthens the contact between the KT03 derived producer packet and the
KT05 compiled call-boundary adapter beyond the earlier synthetic KT05 fixture.

## Initial CI failure

The first KT07 CI run `35288616990` failed because
`-Werror=compare-reals` rejected exact REAL equality syntax in the test
program.

Classification:

`TOOLING_VALIDATOR_FAILURE`

The test expression was corrected without changing the fixture, source
identities, normalized packet, KT03 contract or KT05 implementation. The next
head `90f1c9ba240da681033b6392d0843ddb131b6ef3` passed CI
`35288669987`.

## KT07-R1 disposition

KT07-R1 found that the first green fixture integrity check compared the
recomputed normalized digest only with a digest stored in the same fixture.

Disposition: CLOSED.

The exact expected normalized digest is now independently pinned. The
remediated exact head passed CI `35288769233`.

## Evidence limitations

The raw B0 legacy file is not committed to the repository. CI therefore verifies
the persisted B1 derived fixture and its independent identity pins but cannot
re-run raw-byte materialization without the externally supplied file.

The JSON-to-Fortran generator represents the persisted normalized decimal
values as REAL64 literals. This is appropriate for the bounded B1 compiled
consumption proof. It does not establish Intel/legacy compiler bitwise
equivalence.

KT07 inherits the KT03 classification of
`legacy_dble_trunc_diagnostic` as diagnostic-only. No B2 promotion occurs.

## Scope guard

PASS.

KT07 does not:

- change production source;
- modify KT03 or KT05 implementations;
- consume KT06 as qualified authority;
- execute `Hydro_detailed`;
- assess ANIMO scientific admissibility;
- resolve Hlpimp=1;
- define runtime time mapping, retry or timestep policy;
- admit B3/B4 or Status A/AA.

## Governance disposition

No separate GOV04 Tier B/C/D independent review is required for this
evidence/tooling-only workunit because no scientific or runtime semantics are
changed.

Current review result:

`SELF_REVIEW_PASS_B1_EVIDENCE_TOOLING_ONLY`

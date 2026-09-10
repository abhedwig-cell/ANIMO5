# ANIMO-B3B04E1 - TCD-040 provenance-pinned independent replay evidence remediation

Status: `FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN`

Target: `TCD-040`

Scope: `EVIDENCE_REPLAYABILITY_ONLY`

Branch: `work/animo-b3b04e1-tcd040-replay-evidence`

Clean base: `ANIMO-B3B04R@bb001129578457ca8435e39deb2b8586e7ebc6a2`

## Purpose and boundary

B3B04E1 exists only to remediate the independent-replay blockers recorded by B3B04R. It does not re-decide the TCD-040 science, admit TCD-040, patch production source, start B4, claim canonical STATE admission, compose TCD-016, expand crop/restart architecture, modify central regie, change GOV03 historical UNKNOWN, or perform an independent second-line reconsideration.

Pinned authorities:

- readiness: `ANIMO-B3B04@19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865`;
- route and restore-discriminator disposition: `ANIMO-B3D11@4cc782986faf3d3af829f2e16142dd7f8622c6ac`;
- independent review: `ANIMO-B3B04R@bb001129578457ca8435e39deb2b8586e7ebc6a2`;
- central regie: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`.

## Frozen B0 identity

The exact transient artifacts available in the authoring environment were re-hashed before derived inspection:

| Artifact | SHA-256 | Local result |
|---|---|---|
| ANIMO 4.1.5 revision-53 source ZIP | `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` | match |
| ANIMO testbank ZIP | `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` | match |
| ANIMO 4.0 user guide PDF | `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301` | match |

This remains a local identity check only. The current B0 register still does not prove controlled immutable acquisition or retention.

## Natural GrassPeat witness

`tools/b3b04e1/extract_grasspeat_activation.py` reads the exact frozen testbank ZIP directly. It verifies both the archive hash and the pinned GrassPeat `INITIAL.INP` member hash before interpreting the fixed layout.

Original layer-0 values:

| Coordinate | Original value |
|---|---:|
| `Conh(0)` | `6.885736E-03` |
| `Coni(0)` | `5.743774E-04` |
| `Codiorma(0)` | `9.904185E-02` |
| `Codiorni(0)` | `5.673512E-03` |
| `Codiorpo(0)` | `5.456775E-04` |
| negative control `Copo(0)` | `3.703004E-03` |

This makes the natural initial witness independently inspectable once the exact testbank bytes are acquired through the approved route.

## Reconstruction of the executable replay

The original B3B04 authoring harness was not found in the immutable branch history or workflow artifacts. That fact is preserved. It is not silently rewritten as if the original harness had been recovered.

B3B04E1 now persists `tools/b3b04e1/replay_tcd040.py`, a transparent deterministic reconstruction of the already bounded split-282 and split-67 evidence. This is within B3B04E1's explicit requirement to persist a standalone regeneration/replay harness. The reconstruction is not a new scientific claim and does not alter production source. It creates execution-only instrumented descendants of exact frozen B0.

The harness uses the same deterministic GNU build contract already established for the B0 diagnostic execution route:

```text
GNU Fortran (Debian 14.2.0-19) 14.2.0
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
-Wl,--build-id=none
```

The bundle uses the governance-allowed deterministic-generator-plus-cryptographic-hashes route. Large binary trace payloads are regenerated on demand rather than committed to public Git.

## Local reconstructed replay result

A complete local run was executed against the hash-matched source and testbank bytes and persisted as `integration/animo-b3/b3b04e1/RECONSTRUCTED_REPLAY_LOCAL_RESULT.json`.

The reconstruction uses an explicit little-endian binary trace with two records per step for 900 steps. A full trajectory has 1800 records. For `Nl=30`, a record is 3036 bytes and contains accepted time/surface coordinates plus the current and restart representations of the five target aqueous owners and the `Copo` negative control across layers `0:Nl`.

No tolerance is used. Comparisons are exact bytes.

### Split 282

Stage A stops after 282 steps and emits 564 records. Its trace is an exact byte prefix of the uninterrupted trace.

The reconstructed checkpoint is 48 bytes, one GNU sequential-unformatted little-endian record containing the five target binary64 values. It reproduces the historical B3B04 checkpoint hash exactly:

```text
833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e
```

The five raw little-endian binary64 payloads are:

| Coordinate | Raw hex |
|---|---|
| `Conh(0)` | `d154eca7b66a4d3f` |
| `Coni(0)` | `9cea8abdf062e23e` |
| `Codiorma(0)` | `f8c17a4b6af2713f` |
| `Codiorni(0)` | `b4e1ea3e5e14203f` |
| `Codiorpo(0)` | `bb02ab6430bae93e` |

Under the explicit B3B04E1 trace serialization the local hashes are:

```text
continuous:        6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3
corrected restore: 6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3
defective restart: d93ec85c00c9f026d1d215d5aea250192d250775ee1433a7b3754cb090590388
```

The corrected restore is byte-identical to the uninterrupted 1800-record trajectory.

The defective replay first diverges at zero-based record 564, step 283, phase 0, layer 0. At that record exactly the five target coordinates differ and each defective value is exact positive zero. All other traced coordinates remain exact there. `Copo(0)` remains exact and is therefore an explicit negative control.

### Split 67

Stage A emits 134 records. All five target checkpoint values are already exact positive zero. Applying the bounded legacy zeroing action therefore changes nothing.

The full 1800-record legacy-zeroing trajectory is byte-identical to the uninterrupted reconstruction trajectory. Both have SHA-256:

```text
6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3
```

## Historical trace hashes versus reconstructed trace hashes

The original B3B04 summary reported different trace SHA-256 values. That is not treated as a scientific discrepancy because the original trace serialization contract and payloads were not retained.

B3B04E1 does not invent an undocumented serializer to force the old trace hashes. Instead it pins a new explicit trace contract and verifies the scientific identities directly: split arithmetic, exact checkpoint bytes, first-divergence coordinates and location, corrected full-trace equality, and split-67 zero-path equality.

The historical B3B04 trace hashes remain provenance targets only. The split-282 checkpoint hash is stronger here because its record format is independently recoverable and has been reproduced exactly.

## Documentation provenance

The exact hash-pinned ANIMO 4.0 user guide was inspected directly. The relevant restart-style contract is at **physical PDF page 59**, **section 3.3**, in the `INITIAL.OUT` row of the input/output-file table. It describes `INITIAL.OUT` as a formatted state-variable representation compatible with initializing another simulation run.

The required representation boundary is therefore:

```text
INITIAL.OUT = FORMATTED_RESTART_STYLE_REPRESENTATION
B3B04 atomic checkpoint fixture = RAW_BYTE_IDENTITY_EVIDENCE
```

B3B04E1 does not claim that `INITIAL.OUT` is a raw-byte exact checkpoint.

## Validator and CI semantics

`tools/b3b04e1/validate_b3b04e1.py` now distinguishes two modes.

The ordinary gate requires all static evidence checks, exact B0 artifact hashes, source-member identity, GrassPeat witness extraction, scope guards, the documentation distinction, controlled immutable B0 status, and a successful actual executable replay using `replay_tcd040.py`. It fails closed on any mismatch.

`--audit-blocked-state` is the CI-safe mode while B0 acquisition is unavailable to GitHub Actions. It may be green only when the reconstruction bundle is internally complete and the controlled-B0 blocker remains truthfully present. Green blocked-state CI is not evidence qualification.

## Remaining blocker

The missing-harness blocker is now resolved by a transparent reconstruction and deterministic generator. The replay payload persistence blocker is resolved through the explicitly allowed generator-plus-hashes route.

One substantive gate remains: a genuinely independent runner still cannot obtain the exact source ZIP, testbank ZIP, and guide PDF through a governance-approved controlled immutable acquisition route. The repository B0 register remains unqualified on that point.

Therefore B3B04E1 remains fail closed:

```text
FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN
```

and TCD-040 remains:

```text
UNRESOLVED_NOT_ADMITTED
```

## Resume condition

Resume qualification only after the B0 Evidence Custodian supplies and governance accepts controlled immutable acquisition proof for all three exact B0 artifacts. Then run the persisted ordinary B3B04E1 gate from those acquired bytes.

Only if that ordinary gate passes may B3B04E1 be closed as evidence-replay qualified and a new clean genuinely independent second-line reconsideration branch be created. B3B04R itself remains unchanged.

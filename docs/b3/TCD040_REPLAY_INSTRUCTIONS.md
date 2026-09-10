# TCD-040 reconstructed replay instructions

Workunit: `ANIMO-B3B04E1`

Scope: `EVIDENCE_REPLAYABILITY_ONLY`

Current status: `FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN`

These instructions are intentionally sufficient to run the persisted B3B04E1 reconstruction without information from the authoring chat. They do not authorize TCD-040 admission, a production patch, B4, canonical STATE admission, TCD-016 composition, crop/restart architecture expansion, central-regie changes, GOV03 historical-status changes, or an independent second-line decision.

## 1. What is reconstructed

The original B3B04 authoring harness and its original trace serialization were not retained. B3B04E1 therefore does not claim to have recovered them.

`tools/b3b04e1/replay_tcd040.py` is a transparent reconstruction harness for the already bounded TCD-040 evidence. This is permitted here because B3B04E1 explicitly requires a standalone regeneration/replay route. The reconstruction does not create a new scientific claim object. It instruments an execution-only copy of exact frozen B0 and tests the same five layer-0 aqueous owners, the same split-282 divergence, the same corrected restore identity, and the same split-67 zero-path control.

The deterministic-generator-plus-cryptographic-hashes route is the bundle representation. Large binary traces do not need to be committed to Git.

## 2. Required frozen inputs

The runner must independently obtain the following exact B0 artifacts through a governance-approved controlled immutable acquisition route:

| Artifact | Required SHA-256 |
|---|---|
| ANIMO 4.1.5 revision-53 source ZIP | `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` |
| ANIMO testbank ZIP | `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` |
| ANIMO 4.0 user guide PDF | `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301` |

Do not substitute a re-zipped archive, extracted tree, renamed-content reconstruction, different guide scan, or merely similar testcase. Hash mismatch means stop.

The current repository does not yet provide the controlled acquisition route. That is the remaining qualification blocker.

## 3. Toolchain

Pinned compiler identity:

```text
GNU Fortran (Debian 14.2.0-19) 14.2.0
```

Compile flags:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

Link flag:

```text
-Wl,--build-id=none
```

The reconstruction reuses the repository's existing `tools/build_gnu_diagnostic.py` and `tools/prepare_gnu_case.py`. Those tools create execution-only descendants. Frozen B0 bytes remain unchanged.

## 4. Run the natural GrassPeat input witness

To inspect the exact original layer-0 values from the frozen GrassPeat testcase:

```bash
python tools/b3b04e1/extract_grasspeat_activation.py /controlled/path/ANIMO_testbank.zip
```

Expected original layer-0 values:

| Coordinate | Expected value |
|---|---:|
| `Conh(0)` | `6.885736E-03` |
| `Coni(0)` | `5.743774E-04` |
| `Codiorma(0)` | `9.904185E-02` |
| `Codiorni(0)` | `5.673512E-03` |
| `Codiorpo(0)` | `5.456775E-04` |
| negative control `Copo(0)` | `3.703004E-03` |

The inspector verifies the testbank archive hash and the exact GrassPeat `INITIAL.INP` member hash before interpreting its pinned layout.

## 5. Run the reconstructed executable replay

From the repository root:

```bash
python tools/b3b04e1/replay_tcd040.py \
  /controlled/path/ANIMO_4.1.5.53.zip \
  /controlled/path/ANIMO_testbank.zip \
  build/b3b04e1/replay
```

The output directory is disposable. The durable expected values are in:

- `integration/animo-b3/b3b04e1/TCD040_REPLAY_EXPECTATIONS.json` for prior B3B04 targets;
- `integration/animo-b3/b3b04e1/RECONSTRUCTED_REPLAY_LOCAL_RESULT.json` for the transparent B3B04E1 serialization;
- `integration/animo-b3/b3b04e1/REPLAY_MANIFEST.json` for bundle semantics.

The harness must terminate nonzero on any required mismatch.

## 6. Transparent trace contract

B3B04E1 uses an explicit little-endian binary stream. It contains two records per simulation step for 900 steps, so a complete trajectory has 1800 records.

For `Nl=30`, each record is 3036 bytes and contains:

1. `int32 Sttot`;
2. `int32 phase`, where `0` is post-Init before ordinary timestep process calculations and `1` is after ordinary timestep calculations and `Outsel`;
3. `int32 Nl`;
4. binary64 scalars `Pn`, `Pnt`, `Snla`, `Snt`, `Wale`, `Walet`;
5. binary64 arrays `0:Nl` for `Conh`, `Coni`, `Codiorma`, `Codiorni`, `Codiorpo`, `Copo`, `Rsconh`, `Rsconi`, `Rscodiorma`, `Rscodiorni`, `Rscodiorpo`, and `Rscopo`.

Comparison policy is exact bytes, no tolerance.

This trace serialization is deliberately explicit and newly documented. Its hashes must not be confused with the lost original B3B04 trace serialization hashes.

## 7. Split-282 expected replay

The reconstructed Stage A must stop after step 282 with 564 trace records. Its trace must be an exact byte prefix of the uninterrupted reconstruction trace.

The checkpoint is one GNU sequential-unformatted little-endian record containing exactly five binary64 values. The required checkpoint SHA-256 is:

```text
833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e
```

Required raw little-endian binary64 payloads:

| Coordinate | Raw hex |
|---|---|
| `Conh(0)` | `d154eca7b66a4d3f` |
| `Coni(0)` | `9cea8abdf062e23e` |
| `Codiorma(0)` | `f8c17a4b6af2713f` |
| `Codiorni(0)` | `b4e1ea3e5e14203f` |
| `Codiorpo(0)` | `bb02ab6430bae93e` |

This checkpoint hash reproduces the prior B3B04 checkpoint hash exactly.

For the B3B04E1 transparent trace contract, the local reconstruction produced:

```text
continuous:        6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3
corrected restore: 6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3
defective restart: d93ec85c00c9f026d1d215d5aea250192d250775ee1433a7b3754cb090590388
```

The corrected restore must match the uninterrupted 1800-record trace byte for byte.

The defective replay must first diverge at zero-based trace record 564, simulation step 283, phase 0, layer 0. At that first divergence exactly these five coordinates differ: `Conh(0)`, `Coni(0)`, `Codiorma(0)`, `Codiorni(0)`, and `Codiorpo(0)`. Their defective raw values must be exact positive zero. `Copo(0)` is a required negative control and must remain exact there.

The prior B3B04 trace hashes `29055b...` and `920cc...` remain historical provenance targets only. The original B3B04 trace serialization was not persisted, so B3B04E1 does not invent a byte layout merely to force those old trace hashes.

## 8. Split-67 zero-path negative control

Stage A must stop after step 67 with 134 records. All five target checkpoint values must already be exact positive zero.

The reconstructed legacy-zeroing continuation must remain byte-identical to the uninterrupted 1800-record trace. Under the B3B04E1 trace contract the required full-trace SHA-256 is:

```text
6089d7191c01cf09da3a84cec5d73bbe6a13b4d5ac13c73e92321dd9a1db69e3
```

## 9. Documentation provenance

The exact guide is the hash-pinned ANIMO 4.0 user guide listed above. The restart-style file contract is independently inspectable at **physical PDF page 59**, **section 3.3**, in the `INITIAL.OUT` entry of the input/output-file table.

That passage supports only this representation boundary:

```text
INITIAL.OUT = FORMATTED_RESTART_STYLE_REPRESENTATION
B3B04 atomic checkpoint fixture = RAW_BYTE_IDENTITY_EVIDENCE
```

Do not claim that `INITIAL.OUT` is a raw-byte exact checkpoint. It is a formatted restart-style representation that can be used to initialize another run.

## 10. Run the fail-closed qualification validator

After acquiring all three exact artifacts through the approved controlled route:

```bash
python tools/b3b04e1/validate_b3b04e1.py \
  --source-zip /controlled/path/ANIMO_4.1.5.53.zip \
  --testbank-zip /controlled/path/ANIMO_testbank.zip \
  --guide-pdf /controlled/path/animo_user_guide_4_0.pdf \
  --require-git-scope
```

The default gate verifies the static bundle, B0 hashes, source-member hashes, natural witness, scope guard, documentation distinction, and actual reconstructed executable replay. It may pass only when the repository B0 register also records `PROVEN_CONTROLLED_IMMUTABLE` for all three required artifacts.

For repository CI while controlled B0 acquisition is still unavailable:

```bash
python tools/b3b04e1/validate_b3b04e1.py --audit-blocked-state
```

A green blocked-state audit means only that the deterministic reconstruction bundle is complete and the controlled-B0 blocker is truthfully still present. It is not evidence qualification.

## 11. Handoff gate

Do not create a reconsideration review branch while the ordinary default gate is red.

Only after the ordinary gate passes may a new clean branch be created for a genuinely independent second-line reconsideration. B3B04R itself is not reopened or silently altered.

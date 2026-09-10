# ANIMO-B3B04E3 — TCD-040 reconstructed replay harness and session-local authoring evidence

Status: `RECONSTRUCTED_REPLAY_IMPLEMENTED_SESSION_LOCAL_SEMANTIC_MATCH_CONTROLLED_B0_CUSTODY_PENDING`

Target: `TCD-040`

Scope: `DISTINCT_E2_AUTHORIZED_RECONSTRUCTED_REPLAY_HARNESS`

Upstream authorization: `ANIMO-B3B04E2@01e6df610d236bac19d17f16d109a4e0e676ccfa`

## 1. Purpose and evidence class

ANIMO-B3B04E2 authorized construction of a new, distinct provenance-pinned replay harness after the original B3B04 Stage-A/Stage-B implementation and full-trace serializer were found not to have been persisted. E3 implements that reconstruction and persists the exact generator, the post-generation comparator, the generated-result summary, and the replay contract.

E3 does **not** claim that the original B3B04 harness or original full-trace files were recovered. The E3 generator does not load the frozen B3B04 expected-result manifest. Historical B3B04 values are consulted only by the separate post-generation comparator.

The authoring execution reported here used session-local B0 bytes whose SHA-256 values match the frozen identities. Those bytes are not controlled immutable custody evidence under ANIMO-EG01. Therefore this workunit remains `NOT_QUALIFIED_FOR_INDEPENDENT_REPLAY` even though the reconstructed replay semantically reproduces the bounded B3B04 findings.

## 2. Frozen input identity

The authoring execution verified before use:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- deterministic fixture `LWKM_gras_1040.2021.2045`.

Selected frozen source members were independently hashed before instrumentation:

- `Inicalc.for`: `306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1`;
- `input1.for`: `041328a24569f7649958e6d7a0385911656f49e11a812be6adfb8d81b16f8b95`;
- `Init.for`: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`;
- `Output_Init.for`: `6452c175dcd7c6e80983c1176467735d07f75595cf8341526b115b70121b6a2f`;
- `Animo.for`: `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7`.

Only an extracted execution copy is instrumented. Frozen B0 and production source are not modified.

## 3. Build and compatibility contract

The authoring execution used:

`GNU Fortran (Debian 14.2.0-19) 14.2.0`

with the diagnostic compatibility flags:

```text
-ffree-form
-ffree-line-length-none
-fallow-argument-mismatch
-std=legacy
-fdefault-real-8
-fdefault-double-8
-fno-automatic
```

and link option:

```text
-Wl,--build-id=none
```

The reconstruction uses the already established diagnostic compatibility transforms for case-insensitive include resolution, the bounded `Outsel.for` GNU syntax adaptation, the `dfport` timing shim, Intel intrinsic shims, testcase path normalization, `PrintBalLabel` lexical adaptation, and PowerStation-compatible hydrology record conversion. These are execution-compatibility transforms, not scientific-input changes.

## 4. Reconstructed trajectory schema

E3 intentionally introduces a new explicit trace schema, `B3B04E3_RECONSTRUCTED_TRACE_V1`, because the original B3B04 full-trace serializer schema was not persisted.

Each GNU Fortran sequential-unformatted record contains:

1. `int32 step`, `int32 phase`, `int32 Nl`;
2. binary64 arrays `NH4`, `NO3`, `DOM`, `DON`, `DOP`, `PO4`, `MOFRT`, each over `0:Nl`;
3. binary64 scalars `Wale`, `Snla`, `Pn`.

Two records are emitted per timestep:

- phase 0: current owners after `Init` and after the bounded optional restore/defect action;
- phase 1: accepted `Rs*` owners at the end of the timestep.

The reconstructed continuous trace contains exactly 1,800 records and has SHA-256:

`c73df6a35ccff5af39a4497aba4f1bc8f38b160a25d0cfe29e962285026d0163`

This hash belongs only to the E3 reconstructed schema. It is not compared for equality with the unavailable original B3B04 trace bytes.

## 5. Split 282 result

Stage A stops at accepted boundary 282 after exactly 564 trajectory records. The Stage-A trajectory is byte-exact to the corresponding continuous prefix under the E3 schema.

The reconstructed checkpoint is one GNU Fortran sequential-unformatted logical record containing only five little-endian binary64 values in this order:

`NH4, NO3, DOM, DON, DOP`

The logical payload is 40 bytes and the complete file is 48 bytes. Its independently generated SHA-256 is:

`833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e`

The generated values and raw binary64 encodings are:

| coordinate | value | little-endian binary64 hex |
|---|---:|---|
| `Conh(0)` | `8.977310061221382e-4` | `d154eca7b66a4d3f` |
| `Coni(0)` | `8.767359689234193e-6` | `9cea8abdf062e23e` |
| `Codiorma(0)` | `4.381575788713558e-3` | `f8c17a4b6af2713f` |
| `Codiorni(0)` | `1.2267733059957502e-4` | `b4e1ea3e5e14203f` |
| `Codiorpo(0)` | `1.2267733059957505e-5` | `bb02ab6430bae93e` |

Only after generation did the separate comparator consult the frozen B3B04 target manifest. The checkpoint values, raw bytes and checkpoint SHA are all exact matches to the previously reported B3B04 targets.

The corrected restore branch is byte-exact to the uninterrupted continuous trajectory over all 1,800 E3 records. Its E3 trace SHA is therefore also:

`c73df6a35ccff5af39a4497aba4f1bc8f38b160a25d0cfe29e962285026d0163`

The defective five-coordinate erasure branch has E3 trace SHA:

`fd4048b934736ca5fa9abdb1f915318c6c549c5d48d15207434519083ed2c568`

Its first divergence occurs at record index 564, step 283, phase 0, and exactly at the five target layer-0 coordinates. There is no earlier divergence. Exactly 1,236 records differ thereafter.

The independently generated consequence envelope also reproduces the earlier B3B04 comparison targets:

| field | changed layers | maximum absolute difference |
|---|---|---:|
| NH4 | `0:30` | `8.977310061221382e-4` |
| NO3 | `0:30` | `8.767359689234193e-6` |
| DOM | `0:30` | `4.381575788713558e-3` |
| DON | `0:30` | `1.2267733059957502e-4` |
| DOP | `0:30` | `1.2267733059957505e-5` |
| PO4 | `1:29` | `1.4751153212333792e-10` |

`MOFRT`, `Wale`, `Snla` and `Pn` remain unchanged on the captured surface. `Copo(0)` is not modified at the defect boundary.

## 6. Exact-zero control at split 67

Stage A at split 67 contains 134 trajectory records. All five checkpoint values are exact positive binary64 zero. The checkpoint SHA is:

`32bdf5749fde9e0553f2efa3c55d0b329e1ab5beafdcf6eb1d86db6e19aabd94`

Applying the same five zero assignments is an exact identity operation. The resulting 1,800-record trajectory is byte-exact to continuous under the E3 schema and has SHA:

`c73df6a35ccff5af39a4497aba4f1bc8f38b160a25d0cfe29e962285026d0163`

This rejects the explanation that the split/replay mechanism itself creates the split-282 divergence.

## 7. Deterministic replay commands

With exact B0 archives available locally under governance-approved custody, generation is:

```bash
python tools/b3b04e3/run_reconstructed_replay.py \
  /path/to/ANIMO_4.1.5.53.zip \
  /path/to/ANIMO_testbank.zip \
  /tmp/b3b04e3-replay
```

The generator verifies both archive hashes before build or execution. It does not read the expected-result manifest.

Only after generation, compare against the frozen E1 target manifest:

```bash
python tools/b3b04e3/compare_reconstructed_replay.py \
  /tmp/b3b04e3-replay/TCD040_RECONSTRUCTED_REPLAY_RESULT.json \
  integration/animo-b3/b3b04e1/TCD040_REPLAY_EXPECTATIONS.json \
  --output /tmp/b3b04e3-replay/TCD040_RECONSTRUCTED_REPLAY_COMPARISON.json
```

The expected successful semantic comparison result is:

`PASS_B3B04E3_RECONSTRUCTED_REPLAY_SEMANTICS`

## 8. CI boundary

The public repository intentionally does not contain the copyrighted/raw B0 source and testcase archives. Therefore E3 CI cannot honestly claim a fresh controlled-custody B0 replay. CI validates:

- Python syntax and reconstruction package structure;
- expected-result quarantine between generator and comparator;
- frozen hash pins and result-manifest consistency;
- the persisted session-local generated-result summary;
- the post-generation semantic comparison;
- the E3 scope guard.

A future custody-enabled replay must rerun the generator from independently restored B0 bytes. Until that occurs, `independent_replay_qualified = false`.

## 9. Explicit non-admissions

E3 does not authorize or claim:

- TCD-040 B3 admission;
- a production source patch;
- B4 implementation;
- canonical STATE admission;
- whole-model checkpoint qualification;
- TCD-016 composition;
- internal crop-state composition;
- restart architecture redesign;
- historical fidelity or prevalence;
- central-regie update.

The only remaining qualification blocker addressed by neither E2 nor E3 is controlled immutable B0 custody under ANIMO-EG01. A new independent second-line reconsideration must not start from E3 alone.

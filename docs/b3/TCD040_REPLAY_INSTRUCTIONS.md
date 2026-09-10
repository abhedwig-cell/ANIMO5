# TCD-040 independent replay instructions and acquisition gate

These instructions belong to `ANIMO-B3B04E1`. They are intentionally incomplete at the executable replay step because the required original B3B04 Stage-A/Stage-B harness and immutable B0 acquisition route are not currently available in the repository. Do not fill that gap from chat-only knowledge.

## Required immutable inputs

An independent execution must acquire these exact bytes through a governance-approved B0 route:

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 user-guide PDF SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

Do not use a similarly named archive. Do not use an unpacked copy whose parent archive identity is unknown. Do not publish these raw bytes in the public repository unless redistribution has been explicitly authorized.

## Toolchain contract

The existing diagnostic build path used by B3B04 is pinned to GNU Fortran 14.2.0 with:

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

The repository build helper also requires exactly 58 selected legacy compilation units, excludes `input1_1.for` and `Outselorg.for`, creates case-compatible include aliases, uses the recorded `dfport/secnds` and Intel-intrinsic shims, and applies exactly 14 GNU syntax compatibility substitutions in `Outsel.for`.

The diagnostic build remains `DIAGNOSTIC_NOT_REFERENCE`. Its role here is only evidence replay under the already used B3B04 execution contract.

## Independent preflight

After retrieving the controlled immutable B0 bytes, run:

```bash
python tools/b3b04e1/validate_b3b04e1.py \
  --source-zip /controlled/path/ANIMO_4.1.5.53.zip \
  --testbank-zip /controlled/path/ANIMO_testbank.zip \
  --guide-pdf /controlled/path/animo_user_guide_4_0.pdf
```

The gate must remain failed until the full replay bundle exists.

Inspect the natural GrassPeat witness independently with:

```bash
python tools/b3b04e1/extract_grasspeat_activation.py \
  /controlled/path/ANIMO_testbank.zip
```

Expected layer-0 values are pinned in `integration/animo-b3/b3b04e1/TCD040_REPLAY_EXPECTATIONS.json`.

## Build and case preparation

Once the controlled source and testbank bytes are available, the existing repository helpers are the starting point:

```bash
python tools/build_gnu_diagnostic.py \
  /controlled/path/ANIMO_4.1.5.53.zip \
  build/b3b04e1/base \
  --compiler gfortran

python tools/prepare_gnu_case.py \
  /controlled/path/ANIMO_testbank.zip \
  LWKM_gras_1040.2021.2045 \
  build/b3b04e1/lwkm
```

Both tools fail on the frozen archive hash before making execution-only working copies.

## Required replay outputs

A qualifying replay must persist or deterministically regenerate and cryptographically hash all of these surfaces:

- split-282 raw checkpoint payload;
- 1800-record uninterrupted continuous trace;
- 1800-record defective restart trace;
- 1800-record corrected restore trace;
- 1800-record split-67 zero-path control trace.

The replay must independently derive, not merely copy from the target manifest:

- split = 282;
- five checkpoint values and their exact binary64 bytes;
- first defective divergence at step 283, phase 0, layer 0 for the five target coordinates;
- corrected restore full-trace byte equality to continuous execution;
- split-67 exact-zero negative-control equality.

Comparison is exact raw-byte comparison with no tolerance.

## Current hard stop

There is no `tools/b3b04e1/replay_tcd040.py` in the qualified bundle because the original B3B04 executable replay implementation was not persisted. There are also no raw checkpoint or trace payloads under `integration/animo-b3/b3b04e1/payloads/`.

Do not infer an implementation from the B3B04 summary and then label the result a replay of the original evidence. Either recover the original provenance-pinned harness/payloads, or obtain an explicit governance decision authorizing a distinct reconstruction step.

## Documentation boundary

The ANIMO 4.0 user-guide restart passage is documentation evidence for a formatted restart-style file. It is not evidence that `INITIAL.OUT` preserves every state coordinate bitwise.

Keep the classifications exact:

```text
INITIAL.OUT = FORMATTED_RESTART_STYLE_REPRESENTATION
B3B04 atomic checkpoint fixture = RAW_BYTE_IDENTITY_EVIDENCE
```

A replay or validator that treats `INITIAL.OUT` as the raw checkpoint must fail.

# ANIMO-B3B04E1 - TCD-040 provenance-pinned independent replay evidence remediation

Status: `FAIL_CLOSED_INDEPENDENT_REPLAY_BUNDLE_NOT_QUALIFIED`

Target: `TCD-040`

Scope: `EVIDENCE_REPLAYABILITY_ONLY`

Branch: `work/animo-b3b04e1-tcd040-replay-evidence`

Clean base: `ANIMO-B3B04R@bb001129578457ca8435e39deb2b8586e7ebc6a2`

## 1. Purpose and non-purpose

B3B04E1 exists only to remediate the independent-replay blockers recorded by B3B04R. It does not re-decide the TCD-040 science, does not admit TCD-040, does not patch production source, and does not perform an independent second-line reconsideration.

The input authorities are pinned as follows:

- readiness: `ANIMO-B3B04@19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865`;
- route and restore-discriminator disposition: `ANIMO-B3D11@4cc782986faf3d3af829f2e16142dd7f8622c6ac`;
- independent review: `ANIMO-B3B04R@bb001129578457ca8435e39deb2b8586e7ebc6a2`;
- central regie: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`.

The live repository was checked before creating this branch. No pre-existing `ANIMO-B3B04E1` issue was found. The new branch was created directly from the immutable B3B04R closeout head.

## 2. Frozen B0 identity rechecked in the authoring environment

The exact transient artifacts supplied to this work environment were re-hashed before any derived inspection:

| Artifact | SHA-256 | Result |
|---|---|---|
| ANIMO 4.1.5 revision-53 source ZIP | `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566` | match |
| ANIMO testbank ZIP | `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84` | match |
| ANIMO 4.0 user guide PDF | `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301` | match |

This is a local identity check only. It is not an immutable acquisition route and it is not controlled-retention proof.

Source-member hashes independently rechecked from the source ZIP are recorded in `integration/animo-b3/b3b04e1/TCD040_REPLAY_EXPECTATIONS.json`. The exact GrassPeat `INITIAL.INP` member hash is also recorded there.

## 3. Natural GrassPeat activation recovered from the frozen testcase bytes

A new hash-pinned inspector, `tools/b3b04e1/extract_grasspeat_activation.py`, reads the exact frozen testbank ZIP directly. It first verifies the archive hash and the exact GrassPeat `INITIAL.INP` member hash, then interprets only that pinned fixed layout.

The original layer-0 input values are:

| Owner | Original value |
|---|---:|
| `Conh(0)` | `6.885736E-03` |
| `Coni(0)` | `5.743774E-04` |
| `Codiorma(0)` | `9.904185E-02` |
| `Codiorni(0)` | `5.673512E-03` |
| `Codiorpo(0)` | `5.456775E-04` |
| negative control `Copo(0)` | `3.703004E-03` |

This closes the inspectability gap for the natural initial witness once an independent reviewer possesses the exact frozen testbank bytes. It does not solve independent acquisition of those bytes.

## 4. Split-282 replay targets pinned, not promoted to new proof

The previously reported B3B04 split-282 targets are copied into a separate replay-target manifest and explicitly classified `REPLAY_TARGETS_NOT_INDEPENDENT_PROOF`. This avoids treating summary JSON as a replay.

The five reported checkpoint values deterministically encode as little-endian IEEE-754 binary64:

| Coordinate | Value | Raw bytes, hex |
|---|---:|---|
| `Conh(0)` | `0.0008977310061221382` | `d154eca7b66a4d3f` |
| `Coni(0)` | `8.767359689234193e-06` | `9cea8abdf062e23e` |
| `Codiorma(0)` | `0.004381575788713558` | `f8c17a4b6af2713f` |
| `Codiorni(0)` | `0.00012267733059957502` | `b4e1ea3e5e14203f` |
| `Codiorpo(0)` | `1.2267733059957505e-05` | `bb02ab6430bae93e` |

The validator recomputes these bytes with `struct.pack("<d", value)` and rejects any mismatch. It also checks the reported split arithmetic `282 * 2 = 564`, total length `900 * 2 = 1800`, first-divergence identity at step 283, phase 0, layer 0, corrected-trace hash equality, and the split-67 negative-control hash equality.

These checks only pin the target that a fresh executable replay must reproduce. They are not a substitute for regenerating the trace payloads.

## 5. Documentation provenance and representation boundary

The hash-pinned ANIMO 4.0 user guide states in section 3.3 that `INITIAL.out` contains state-variable data in the same type and sequence as `INITIAL.INP` and can be used to initialize another simulation run. That is a formatted restart-style representation contract.

B3B04 used a separate qualification checkpoint fixture for raw-byte identity evidence. These two representations must remain distinct:

`INITIAL.OUT = FORMATTED_RESTART_STYLE_REPRESENTATION`

`B3B04 atomic checkpoint fixture = RAW_BYTE_IDENTITY_EVIDENCE`

B3B04E1 does not claim, and its validator rejects metadata claiming, that `INITIAL.OUT` is a raw-byte exact checkpoint.

## 6. Why the requested independent executable replay cannot yet be qualified

The blocker is now narrower and explicit.

First, the current B0 evidence register still records `CONTRACT_DEFINED_EXTERNAL_CONTROLLED_STORAGE_NOT_YET_PROVEN`. For the source, testbank and user guide, the controlled-storage record IDs and immutability-proof references are null, post-ingest and secondary-copy verification are false, and the restore test has not passed. The same register explicitly says that transient supplied project bytes are not proof of controlled retention.

Second, repository governance prohibits placing the raw source archive, raw testcase archive, the copyrighted user-guide PDF, or functionally equivalent unpacked copies in this public repository unless redistribution is explicitly authorized. B3B04E1 therefore cannot make the missing B0 acquisition route self-contained by copying the supplied bytes into GitHub.

Third, the immutable B3B04 tree contains `tools/b3b04/validate_b3b04.py`, the workflow, documentation and summary evidence, but not the actual Stage-A/Stage-B replay implementation or the raw checkpoint and trace payloads whose hashes were reported. A new independent reviewer cannot regenerate the reported trajectory hashes from that tree alone.

Because B3B04E1 was instructed to make the existing evidence independently replayable, not silently create a replacement scientific claim object, the workunit stops here fail closed rather than inventing a new replay implementation and treating it as the original evidence.

## 7. Validator and CI semantics

`tools/b3b04e1/validate_b3b04e1.py` is deliberately fail closed.

Its ordinary gate mode can pass only when all of the following are simultaneously true:

- controlled immutable B0 acquisition is proven for source, testbank and user guide;
- the exact artifacts supplied to the validator match the frozen SHA-256 pins;
- required source members match their member hashes;
- the GrassPeat witness regenerates from the exact testbank;
- all required replay harness and payload paths exist;
- split arithmetic, raw binary64 values, divergence identity, corrected exactness target and split-67 target are internally consistent;
- the documentation representation boundary is correct;
- no out-of-scope path was modified.

The CI workflow runs `--audit-blocked-state`. That mode succeeds only if the repository still truthfully exposes the expected blockers. A green blocked-state audit is not an evidence qualification result. The ordinary evidence gate remains red until the missing acquisition and replay material exists.

## 8. Fail-closed disposition

B3B04E1 disposition:

`FAIL_CLOSED_INDEPENDENT_REPLAY_BUNDLE_NOT_QUALIFIED`

TCD-040 remains:

`UNRESOLVED_NOT_ADMITTED`

No reconsideration review branch is created. No B3B04R decision is changed. No B4, canonical STATE admission, TCD-016 composition, production patch, crop/restart architecture expansion, central-regie change or GOV03 historical-status change is authorized by this workunit.

## 9. Exact resume condition

Resume this workunit only after both prerequisites are available:

1. a B0 Evidence Custodian has supplied governance-approved, non-secret immutable acquisition references for the exact source ZIP, testbank ZIP and user guide PDF, with the retention controls required by the B0 evidence register proven;
2. the original B3B04 Stage-A/Stage-B replay implementation and the required checkpoint/trace payloads are made available, or an explicit governance decision authorizes a provenance-pinned reconstruction as a distinct evidence-generation step.

Only after the ordinary B3B04E1 evidence gate passes may a new clean branch be created for a genuinely independent second-line reconsideration.

# ANIMO-B3B04R independent second-line review of TCD-040

Work unit: `ANIMO-B3B04R`

Target: `TCD-040`

Review branch: `review/animo-b3b04r-tcd040-independent-second-line`

Starting head verified before writing: `4cc782986faf3d3af829f2e16142dd7f8622c6ac`

Review disposition: `FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE`

Canonical TCD-040 state after this review: `UNRESOLVED_NOT_ADMITTED`

This is an independent second-line review. It does not admit TCD-040, patch production source, start B4, update central regie, qualify whole-model restart, qualify canonical STATE, compose TCD-016, or make a historical-fidelity claim.

## 1. Live review object and authorities

GitHub issue #35 was read before review writing. At review start it was open and had no comments. The clean review branch pointed exactly to the expected B3D11 handoff head.

Live heads rechecked before writing:

- `ANIMO-B3B04` readiness: `19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865`;
- `ANIMO-B3D11` disposition: `4cc782986faf3d3af829f2e16142dd7f8622c6ac`;
- `ANIMO-RG05D` handoff regie: `f3d6b9780631bd627f8bca0658a8e3878746e666`;
- `ANIMO-STATEQ01`: `4adae99576eb56978da71f7c8a250e4445fd3bc4`;
- `ANIMO-STATEQ02`: `cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`;
- `ANIMO-B3I04`: `400b7cd79f89043e091751707dfa96537587dcf6`;
- `ANIMO-B3Q01`: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-GOV03`: `cbd262bdabe92923113b7326f2f42822ce9a971c`.

Frozen B0 identities were independently read from the persisted hash files:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The review scope is exactly the five layer-0 aqueous restart identity pairs:

- `Conh(0) / Rsconh(0)`;
- `Coni(0) / Rsconi(0)`;
- `Codiorma(0) / Rscodiorma(0)`;
- `Codiorni(0) / Rscodiorni(0)`;
- `Codiorpo(0) / Rscodiorpo(0)`.

`Copo(0)` is an excluded PO4 negative control. TCD-016 is outside scope.

## 2. Independent source and ownership cross-check

The source mechanism is independently corroborated by STATEQ01 evidence that predates B3B04 and B3D11. That audit records the revision-53 sequence `Input1 -> Inicalc -> ... -> Init`, the layer-0 input reader surface, and the unconditional destructive block at `Inicalc.for:125-129`:

```fortran
Conh(0)=0.0
Coni(0)=0.0
Codiorma(0)=0.0
Codiorni(0)=0.0
Codiorpo(0)=0.0
```

The same independent STATEQ01 line records that first ordinary `Init` does not rescue those values from the input surface. Separate restart/state work establishes accepted-state/result ownership and that restore must load accepted physical state without projection or chemistry changes.

This supports the local causal seam independently of the B3B04 conclusion. However, the raw frozen source archive is intentionally not republished in the public repository. The repository contains its cryptographic identity and per-member manifest, not the B0 source bytes themselves. Therefore this review can cross-check the earlier independent source audit, but cannot honestly label the frozen source bytes as newly re-inspected in this GitHub-only second-line execution.

Source ownership/call-order check: `PASS_PRE_B3_INDEPENDENT_SOURCE_AUDIT_CROSSCHECK`, with `RAW_B0_BYTE_REINSPECTION_NOT_AVAILABLE` explicitly recorded.

## 3. Natural GrassPeat activation

STATEQ01 independently records natural nonzero GrassPeat layer-0 values for NH4, NO3, DOM and DON, and independently records `Copo(0)` as nonzero while excluded from the destructive block. B3B04 additionally records nonzero DOP `Codiorpo(0)`.

The testbank ZIP itself is not stored in GitHub. The repository explicitly says this is a recorded retention blocker, not a completed byte freeze in GitHub. Consequently this review cannot independently reopen the unmodified GrassPeat `INITIAL.INP` and re-read all five target values, in particular the fifth DOP target, from the frozen testcase bytes.

Natural activation check: `PARTIAL_BLOCKED`. Four target coordinates and the PO4 control have an independent pre-B3 cross-check; the required five-coordinate raw testcase reinspection is unavailable in this execution context.

## 4. Split-282 causal evidence

B3B04 records the split-282 accepted values:

| Coordinate | Accepted value | little-endian IEEE-754 binary64 hex |
| --- | ---: | --- |
| NH4 | `8.977310061221382e-4` | `d154eca7b66a4d3f` |
| NO3 | `8.767359689234193e-6` | `9cea8abdf062e23e` |
| DOM | `4.381575788713558e-3` | `f8c17a4b6af2713f` |
| DON | `1.2267733059957502e-4` | `b4e1ea3e5e14203f` |
| DOP | `1.2267733059957505e-5` | `bb02ab6430bae93e` |

This review independently regenerated those five binary64 byte encodings from the recorded decimal values. All five match exactly. It also independently checks the trace arithmetic: two records per step through split 282 gives 564 accepted-prefix records, and `1800 - 564 = 1236` post-split records.

That computational cross-check is stronger than merely copying the B3B04 fields, but it is not a replay of the underlying executable campaign. The B3B04 workflow runs only its JSON/document validator. GitHub Actions run `34386299961` has zero persisted artifacts. The B3B04 branch does not persist the checkpoint payload, uninterrupted trace, defective trace, corrected trace, or a harness that regenerates them. The raw B0 source and testcase archives are likewise not available through the GitHub repository.

Therefore the following B3B04 claims cannot be independently replayed or byte-compared in this second-line review:

- the checkpoint file contains the recorded bytes;
- the complete trace contains exactly 1800 records;
- the first defective divergence is exactly step 283, phase 0, layer 0, simultaneously on the five targets;
- no earlier record diverges;
- corrected restore is full-trace exact;
- split 67 is a full 1800-record zero-state exact control.

STATEQ02 is a useful independent control-plane cross-check, but it does not fill this gap. It independently proves exact split-run continuation for its restricted zero-layer0 profile, including an 833-record remainder from split 67, and it explicitly rejects split 282 before checkpoint creation because the TCD-040 path is active. STATEQ02 therefore supports the distinction between the zero-state control and the TCD-040 path, but is not TCD-040 nonzero-path evidence.

Split-282 causal check: `PARTIAL_BLOCKED`. Raw IEEE encoding and arithmetic independently pass. The mandatory full numerical replay and trace localization do not.

## 5. INITIAL.OUT and checkpoint identity

The supplied ANIMO 4.0 user guide is cryptographically inventoried, but the PDF is not republished in the public repository because of its copyright boundary. This review therefore cannot newly inspect the guide pages that B3B04 cites for the `INITIAL.OUT` restart-style contract.

Independent STATEQ01 architecture evidence nevertheless makes the representation boundary unambiguous: legacy `Output_Init` is not a canonical checkpoint serializer, and legacy final/restart output is evidence about fields rather than the canonical acceptance mechanism. A formatted restart representation must not be treated as raw-byte atomic checkpoint identity.

Documentation-contract check: `PARTIAL_BLOCKED` for direct user-guide reinspection, while the formatted-versus-raw distinction is independently `PASS`.

## 6. GOV03 eligibility and historical uncertainty

GOV03 independently establishes `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT` and makes bounded claims eligible for the historical-uncertainty route subject to claim-scoped B3 requirements. B3Q01 requires, among other things, multiple independent causal evidence forms, stronger branch coverage, and a genuine second-line review.

Historical revision-53 behavior remains `UNKNOWN`. This review makes no historical-fidelity, prevalence, or intent claim.

GOV03 route eligibility check: `PASS`, but route eligibility is not admission.

## 7. Independent discriminator assessment

The bounded correction needs one decision before the destructive five-assignment transaction: is this invocation a cold initialization, or is it restoring already accepted layer-0 aqueous state?

For this bounded claim the semantic decision space is exactly two-way:

- `COLD_START`;
- `RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE`.

This semantic partition is sufficient. It is also minimal for the bounded seam. It is not claimed that these exact enum spellings are the only possible API encoding. What is unique is the required intent distinction, not the syntax used to encode it.

The selector must be invocation/control-plane intent. The physical values cannot establish intent because a legitimate cold-start input may itself contain nonzero layer-0 values, as GrassPeat demonstrates. Filename, date, ponding, hydrology, crop state, PO4, other scientific inputs, or any model-state heuristic have the same problem: they do not uniquely state whether the caller requests a cold start or an accepted-state restore.

A restore-capable entrypoint must therefore require an explicit recognized selector and fail before mutation when it is absent or invalid. The selector need not and should not become physical model state or a canonical checkpoint coordinate.

Discriminator sufficiency check: `PASS_SEMANTIC_TWO_STATE_CONTROL_PLANE_INTENT`.

## 8. Atomic implementation seam

The independently corroborated causal seam is limited to the five unconditional assignments at `Inicalc.for:125-129`.

The admissible semantics for a later implementation candidate are bounded as follows:

- `COLD_START`: execute the existing five zero assignments exactly as today;
- `RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE`: preserve the five already restored current-owner values across this transaction;
- do not conditionalize or change any other `Inicalc` initialization;
- do not modify `Copo(0)`;
- do not infer restore intent from state;
- do not simply delete the five assignments unconditionally.

This is a local initialization-control seam. It does not require a new physical state variable and does not itself qualify a checkpoint file format, a broad restart architecture, crop continuation, TCD-016, PO4 behavior, hydrology, macropores, GHG, or numerical policy.

Atomic seam and dependency check: `PASS_BOUNDED_SEAM_NO_SCIENTIFIC_DEPENDENCY_EXPANSION`.

A later real restore-capable integration obviously needs a caller that has already obtained the five accepted owner values. That is an invocation precondition, not evidence that TCD-040 must absorb whole-model checkpoint completeness.

## 9. Second-line decision

A positive second-line review requires every mandatory claim-scoped evidence gate to be independently satisfied. That condition is not met here.

The blocker is precise: the evidence package required to independently replay the nonzero TCD-040 executable campaign is not retained on GitHub. The raw testbank/source archives are not repository-accessible, B3B04 persists no executable replay harness or trace/checkpoint payloads, its workflow validates summary metadata only, and the cited user-guide PDF is not repository-accessible. Independent byte regeneration of five recorded decimal checkpoint values and independent STATEQ controls are useful cross-checks, but they do not substitute for the required nonzero-path replay.

Second-line disposition:

`FAIL_CLOSED_INDEPENDENT_EVIDENCE_REPLAY_INCOMPLETE`

Required canonical consequence:

`TCD-040 = UNRESOLVED_NOT_ADMITTED`

No formal-admission integration should be opened from this review result. A later second-line review could reconsider the same bounded claim if a provenance-pinned, independently runnable TCD-040 evidence bundle becomes available, including the frozen input/source material or a legally usable controlled copy, the split-282 checkpoint/trace artifacts or deterministic regeneration harness, and direct documentation evidence for the formatted restart contract.

This review stops at that disposition.
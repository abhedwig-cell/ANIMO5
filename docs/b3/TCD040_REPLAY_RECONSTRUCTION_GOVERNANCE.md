# ANIMO-B3B04E2 — TCD-040 provenance-pinned replay reconstruction governance

Status: `QUALIFIED_RECONSTRUCTION_AUTHORIZATION_ONLY`

Target: `TCD-040`

Scope: `GOVERNANCE_ONLY_REPLAY_RECONSTRUCTION_AUTHORIZATION`

Branch: `work/animo-b3b04e2-tcd040-replay-reconstruction-governance`

Base: `ANIMO-B3B04E1@9f3e1e9b583d540e5d7048de31e62701747ab69d`

## 1. Purpose

ANIMO-B3B04E1 stopped fail closed because the original B3B04 Stage-A/Stage-B replay implementation and trajectory payloads were not persisted. B3B04E1 explicitly permits a later continuation if either the original replay material is recovered or a separate governance decision authorizes a provenance-pinned reconstruction.

This workunit provides only that governance decision. It does not reconstruct the replay itself, does not qualify the B3B04E1 evidence bundle, and does not change the scientific disposition of TCD-040.

TCD-040 remains `UNRESOLVED_NOT_ADMITTED`.

## 2. Authorities

The following frozen authorities are inputs to this decision:

- readiness: `ANIMO-B3B04@19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865`;
- route and restore-discriminator disposition: `ANIMO-B3D11@4cc782986faf3d3af829f2e16142dd7f8622c6ac`;
- independent second-line review: `ANIMO-B3B04R@bb001129578457ca8435e39deb2b8586e7ebc6a2`;
- evidence-remediation checkpoint: `ANIMO-B3B04E1@9f3e1e9b583d540e5d7048de31e62701747ab69d`;
- B0 retention contract: `ANIMO-EG01@a818b5a37b80ed92aded0b9c404990d356eb2300`;
- current central regie: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`.

Frozen B0 identities remain:

- source ZIP SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 user guide SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

## 3. Governance decision

A new replay harness may be reconstructed as a **distinct remediation artifact** when all rules in this workunit are followed.

Decision:

`AUTHORIZED_DISTINCT_PROVENANCE_PINNED_REPLAY_RECONSTRUCTION`

This authorization does not retroactively convert a reconstructed harness into the original B3B04 harness. Any reconstructed implementation, generator, checkpoint, trace, manifest or hash is new evidence-generation infrastructure and must be labeled as such.

## 4. Allowed reconstruction inputs

The reconstruction may use only:

1. exact frozen B0 source bytes after SHA-256 verification;
2. exact frozen B0 testbank bytes after SHA-256 verification;
3. the frozen documentation identity where documentation is used;
4. source-bound ownership and call-order facts independently inspectable from the frozen source;
5. the bounded TCD-040 semantic seam qualified by B3D11;
6. the B1 compiler/compatibility contract already qualified for diagnostic execution;
7. the replay topology required by B3B04R: uninterrupted execution, independent split process, corrected restore-identity branch, defective five-coordinate erasure branch and exact-zero negative control.

The reconstruction must not depend on hidden chat state, transient prose, unversioned scripts, manually edited outputs or unpublished binary fixtures.

## 5. Expected-result quarantine

Previously reported B3B04 values and hashes are **comparison targets, not generator inputs**.

A reconstructed harness must generate its checkpoint and traces from the frozen inputs and execution path before consulting the frozen B3B04 replay-target manifest for pass/fail comparison.

The implementation must not hard-code the following as generated evidence:

- split-282 checkpoint values;
- checkpoint hash;
- continuous-trace hash;
- defective-trace hash;
- first-divergence identity;
- split-67 equality result.

Those values may be loaded only by a separate comparison/validation stage after generation.

This rule exists to prevent circular evidence where the expected answer is embedded in the generator.

## 6. Required reconstructed topology

The distinct reconstructed replay must implement, at minimum:

### Continuous reference path

Run the exact frozen deterministic fixture through the complete horizon and capture the bounded instrumented trajectory.

### Stage A

Run independently to the accepted split boundary and write only the atomic five-coordinate checkpoint payload required by TCD-040.

### Stage B corrected restore path

Start in a separate process, independently replay deterministic inputs to the same boundary, verify pre-restore boundary identity, read the five-coordinate checkpoint, preserve/restore the accepted values and continue without applying the TCD-040 destructive zero operation.

### Stage B defective-erasure path

Start from the same independently reconstructed boundary, verify identical pre-erasure state, then apply exact positive zero only to:

- `Conh(0)`;
- `Coni(0)`;
- `Codiorma(0)`;
- `Codiorni(0)`;
- `Codiorpo(0)`.

`Copo(0)` remains an excluded negative-control coordinate.

### Exact-zero control

Repeat the split topology at the previously identified exact-zero accepted boundary and demonstrate that applying the five zero assignments is an identity operation.

## 7. Independence and reproducibility requirements

The reconstructed bundle must persist:

- complete harness source;
- exact build and execution instructions;
- compiler version and flags;
- all compatibility transforms and their hashes;
- exact source/testbank/document hashes used;
- checkpoint serialization specification;
- trajectory record schema;
- deterministic generation commands;
- generated checkpoint and trace hashes;
- first-divergence derivation procedure;
- negative-control procedure;
- a machine-readable manifest linking every generated artifact to the reconstruction commit.

A later second-line reviewer must be able to reproduce results without reading the authoring conversation.

## 8. B0 custody boundary

This workunit does **not** waive ANIMO-EG01.

Local or session-scoped access to bytes matching the frozen hashes remains useful for reconstruction authoring but is not controlled immutable retention proof.

Qualification of the eventual B3B04E1 evidence bundle still requires governance-approved external B0 custody evidence satisfying the EG01 proof contract, including primary retention, independent secondary retention and restore verification.

No raw source archive, raw testcase archive, copyrighted user-guide PDF or functionally equivalent unpacked copy is authorized for republication to the public ANIMO5 repository by this decision.

## 9. Scientific and architecture boundaries

This authorization must not be interpreted as:

- a production source patch;
- B3 admission of TCD-040;
- canonical STATE admission;
- whole-model checkpoint qualification;
- TCD-016 composition;
- crop-state composition;
- restart architecture redesign;
- numerical-policy change;
- historical fidelity or prevalence evidence;
- a central-regie update.

The reconstructed harness may encode only the already bounded two-state semantic distinction:

- `COLD_START`;
- `RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE`.

No heuristic restart discriminator is authorized.

## 10. Closeout consequence

This workunit satisfies only the second alternative in the B3B04E1 resume condition:

`original replay recovered OR explicit governance authorization for provenance-pinned reconstruction`.

The first B3B04E1 prerequisite, controlled immutable B0 acquisition, remains open under ANIMO-EG01 / issue #5.

A separate reconstruction implementation workunit may proceed in parallel and may use locally hash-verified B0 bytes for authoring and testing, but it must remain `NOT_QUALIFIED_FOR_INDEPENDENT_REPLAY` until the B0 custody gate is independently satisfied.

No second-line reconsideration branch may be created from this authorization alone.

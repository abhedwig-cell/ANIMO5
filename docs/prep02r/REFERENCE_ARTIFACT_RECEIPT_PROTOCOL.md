# ANIMO-PREP02R — Reference Artifact Receipt Protocol

Status: `READY_FOR_EXTERNAL_ARTIFACT_RECEIPT_NOT_REFERENCE_ADMISSION`.

## Purpose

Define what happens when a historical ANIMO executable, build project, archived output bundle or compiler/environment artifact is received. Receipt must preserve evidence before any execution or interpretation.

This protocol does not admit a reference and does not authorize execution merely because bytes have been received.

## Receipt sequence

1. Keep the received bytes in controlled storage. Do not copy historical binaries into the public repository unless redistribution permission is explicit.
2. Record the sender/source, transfer route, original filename or directory name, any claimed version/revision, dates and accompanying provenance statements.
3. Hash the received bytes before execution. For a single file record SHA-256 directly. For a directory or bundle record every member path, byte size and SHA-256 plus a deterministic content-set hash.
4. Preserve the original bytes unchanged. Extraction, renaming, line-ending conversion, archive recompression or testcase editing creates a derived artifact and must be recorded separately.
5. Classify lineage before native execution:
   - exact revision-53 candidate;
   - nearby provenance-qualified 4.1.x candidate;
   - distinct older/newer lineage;
   - unknown or weakly attributed artifact.
6. Review whether provenance is sufficient to permit a controlled native qualification attempt. Receipt alone is not sufficient.
7. Only after that review, run the smallest compatible frozen native testcase, preferably `RuurloGrass`, without silent testcase translation.

## Receipt tool

`tools/capture_reference_artifact_manifest.py` records a fail-closed manifest without executing or copying the artifact.

Example:

```text
python tools/capture_reference_artifact_manifest.py \
  /controlled/inbox/animo41.exe \
  --label "received historical animo41.exe" \
  --artifact-class historical_executable \
  --claimed-version 4.1.5 \
  --claimed-revision 53 \
  --json receipt.json
```

If the sender supplies an expected SHA-256, pass it with `--expected-sha256`. A mismatch fails closed. Expected SHA-256 is intentionally restricted to single-file artifacts; directory identity uses the per-file manifest and content-set hash.

The generated manifest always states:

- `evidence_class = RECEIPT_MANIFEST_NOT_REFERENCE_ADMISSION`;
- `trust_classification = UNASSESSED_RECEIVED_ARTIFACT`;
- `reference_admitted = false`;
- `native_execution_admitted = false`.

The tool deliberately omits the absolute controlled-storage path from the manifest. Public provenance records should not leak local archive locations merely to prove byte identity.

## Native execution boundary

Historical Windows executables and obsolete compiler environments should be treated as untrusted legacy software until separately reviewed. If native execution is admitted, use an isolated qualification environment and capture the complete runtime contract, inputs, stdout/stderr, outputs, exit status, warnings and hashes.

A successful run is still only a candidate reference observation. PREP02R must separately decide whether provenance plus behavioural evidence justify `QUALIFIED_HISTORICAL_REFERENCE_ENVIRONMENT` or an explicitly scoped equivalent-reference contract.

## Verification

The receipt tool has unit coverage for:

- single-file SHA-256 capture without admission;
- deterministic directory content-set identity independent of absolute root path;
- fail-closed expected-hash mismatch;
- rejection of a single-file expected hash for a directory bundle.

No numerical tolerance or behavioural equivalence policy is introduced by this protocol.

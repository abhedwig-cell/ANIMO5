# ANIMO-KT03 Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Reviewed head: `8f940d9f7f9fafeb167c2847fe0c0d15749816b8`.

Exact-head GitHub Actions run: `35281950236`, conclusion `SUCCESS`.

This review treats the current implementation as a candidate future SWAP5-to-ANIMO exchange boundary, not merely as a parser that happens to pass its synthetic tests.

## Findings

### KT03-R1, HIGH: normalized carrier still leaks legacy file identity

The current `HydrologyStep` contains `hlpimp` and `source_record_sha256` as required payload fields.

Those values are useful file-adapter provenance, but they are not hydrological forcing. Requiring them in the normalized carrier would force a future in-memory SWAP5 producer to imitate a legacy file layout and invent a file-record hash. That violates the intended file-backed/in-memory symmetry.

Disposition: `MUST_REMEDIATE_BEFORE_KT03_CLOSE`.

Required remediation: move legacy layout identity and source-record digest into an adapter provenance object. The hydrology payload consumed downstream must be independent of whether the producer was a file or an in-memory model.

### KT03-R2, MEDIUM: producer time metadata is insufficiently distinguished from runtime time authority

The current fields `tiwa` and `step_days` are useful to reconstruct the legacy producer interval, and `St` is required by `Hydro_detailed`. However KT02 already establishes a model-neutral interval/runtime authority.

Without an explicit distinction, a later adapter could accidentally create two time owners: the runtime interval and the hydrology packet.

Disposition: `MUST_RECONCILE_BEFORE_KT03_CLOSE`.

Required remediation: name these values as producer-coordinate metadata and state that a later runtime adapter must validate them against the authoritative runtime interval. The payload must not select or advance runtime time by itself.

### KT03-R3, MEDIUM: cross-model unit contract is implicit

The current carrier has field names but no explicit unit-contract identity. The legacy ANIMO guide documents mixed units, including days, metres, metres per day, centimetres, volumetric fractions and degrees Celsius. A future in-memory producer therefore needs an explicit conversion target.

Disposition: `MUST_RECONCILE_BEFORE_KT03_CLOSE`.

Required remediation: add a versioned unit-contract identity and document the field units. No numerical conversion should be introduced silently.

### KT03-R4, LOW: source-record provenance validation is too weak

The current payload accepts any 64-character string as `source_record_sha256`. Even within a diagnostic prototype this overstates provenance validation.

Disposition: this finding is superseded if R1 is remediated by moving the digest to adapter provenance and constructing it internally from source bytes. If any caller-supplied digest remains, validate it as hexadecimal.

### KT03-R5, BOUNDARY: `Dble_trunc` reconstruction is not B2 numerical authority

The diagnostic Python normalization reproduces the visible revision-53 algorithmic intent, but historical Intel intrinsic/build behaviour has not been independently recovered here.

Disposition: `ACCEPTED_EXPLICIT_BOUNDARY`.

The evidence must remain `B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`.

### KT03-R6, BOUNDARY: Hlpimp=1 remains incomplete for interception storage

CranMais `Hlpimp=1` does not supply `sSict`. KT03 correctly fails closed rather than inventing the missing state. The Hlpimp=11 LWKM case separately demonstrates a complete file-derived projection when `sSict` is actually present.

Disposition: `ACCEPTED_EXPLICIT_LAYOUT_BOUNDARY`.

KT03-F01 remains open for Hlpimp=1 and must not be hidden by the positive Hlpimp=11 proof.

## Review verdict before remediation

`NOT_YET_QUALIFIABLE_AS_CLEAN_FILE_INDEPENDENT_TYPED_EXCHANGE_CONTRACT`.

The real-file evidence supports the architecture direction, and the Hlpimp=11 proof is materially useful. R1 through R3 must be resolved before KT03 is closed as the first reusable ANIMO hydrology exchange contract.

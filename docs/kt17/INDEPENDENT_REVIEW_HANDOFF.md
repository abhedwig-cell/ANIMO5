# ANIMO-KT17 Independent Tier D Review Handoff

## Frozen substantive target

Substantive authoring head:

`1411e245f62d87494947b648a89ea8207dfe9079`

Tree:

`55500a1bd253603c423b21c43057c4d55506461a`

Validated freeze-package head:

`90799c0b4d22f244b6d6d36db2f952da7afcec38`

Exact-head CI:

`35380747443 = success`.

## Candidate claim

`BOUNDED_KT16_ACCEPTED_CHECKPOINT_HAS_RECOMPUTABLE_SHA256_CONFIG_PAYLOAD_AND_MANIFEST_INTEGRITY_WITH_EXACT_EXPECTED_BUILD_AND_FIXED_EVIDENCE_IDENTITY_BINDING`.

## Required independent review axes

The independent reviewer should verify at minimum:

1. SHA-256 implementation correctness and known-answer-vector coverage.
2. Canonical preimage grammar is deterministic, unambiguous and independent of locale-sensitive floating formatting.
3. REAL64 identity uses exact IEEE bit patterns rather than tolerance or decimal round-trip.
4. KT15 configuration inspection is read-only and does not alter execution, equality or science.
5. KT15 and KT16 regression harnesses remain green after the inspector addition.
6. The checkpoint payload digest actually covers every bounded KT16 continuation coordinate used by restore.
7. Application configuration is independently hashed and also included in checkpoint-payload integrity.
8. Manifest digest covers build identity, evidence identities, feature set, diagnostic policy, config hash and payload hash.
9. Any manifest-digest mismatch is fail-closed. Review the repaired guard specifically.
10. Expected build commit is compared exactly but is not misrepresented as executable self-attestation.
11. Frozen source/testbank/documentation hashes are exact identity pins but are not misrepresented as runtime source-byte rehashing.
12. The in-memory canonical hash preimage is not mislabeled as a persistent checkpoint byte/file format.
13. Restore cannot reach KT16 until KT17 integrity and expected-identity checks pass.
14. No canonical state/checkpoint, B2, B3, B4, TB7 or production admission is implied.
15. Same-agent authoring review remains labeled `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

## Material authoring repair already performed

An early CI run exposed a fail-open status-propagation defect in the manifest digest mismatch guard. A previous successful hash verification left `ok=.true.`; the manifest mismatch path set a reason and returned without resetting `ok`.

The guard was repaired before freeze to set `ok=.false.` explicitly. The repaired head passed:

- KT17 integrity tests;
- SHA-256 known-answer vectors;
- KT15 regression;
- KT16 regression.

Independent review should treat this repaired frozen head as the only valid target and should not review or admit the failed pre-repair heads.

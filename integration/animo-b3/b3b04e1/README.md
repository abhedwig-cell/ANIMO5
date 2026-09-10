# ANIMO-B3B04E1 replay bundle index

This directory contains the machine-readable evidence bundle for the TCD-040 replay-remediation workunit.

The distinct reconstruction route is authorized by `ANIMO-B3B04E2@01e6df610d236bac19d17f16d109a4e0e676ccfa` with decision `AUTHORIZED_DISTINCT_PROVENANCE_PINNED_REPLAY_RECONSTRUCTION`. That authorization is governance-only and does not qualify this bundle, waive controlled B0 custody, perform second-line reconsideration, or admit TCD-040.

Bundle components:

- `TCD040_REPLAY_EXPECTATIONS.json`: frozen B3B04 comparison targets and representation boundary;
- `REPLAY_MANIFEST.json`: deterministic-generator bundle manifest, reconstruction governance pin, generated checkpoint/trace hashes and qualification state;
- `RECONSTRUCTED_REPLAY_LOCAL_RESULT.json`: local hash-pinned reconstruction result, explicitly not independently provenanced.

Executable components live in `tools/b3b04e1/`:

- `replay_tcd040.py`: deterministic reconstructed split-282/split-67 replay generator;
- `extract_grasspeat_activation.py`: hash-pinned natural activation inspector;
- `validate_b3b04e1.py`: fail-closed bundle/replay qualification gate and blocked-state audit.

Current scientific consequence remains `TCD-040 = UNRESOLVED_NOT_ADMITTED`.

The only remaining qualification dependency is governance-approved controlled immutable acquisition of the exact source ZIP, testbank ZIP, and user-guide PDF under ANIMO-EG01 / issue #5. Until that proof exists, the ordinary B3B04E1 gate must remain closed and no reconsideration review branch may be created.

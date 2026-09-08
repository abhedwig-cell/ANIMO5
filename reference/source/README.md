# Frozen legacy source baseline

Status: `BLOCKED_MATERIAL_NOT_AVAILABLE`.

ANIMO-PREP01 did not receive an importable ANIMO production Fortran source tree. No substitute source was downloaded or inferred from unrelated repositories because that would destroy provenance control.

When the authoritative legacy source is supplied, PREP02 or a dedicated source-ingest gate must:

1. import it without content edits;
2. hash every file;
3. record original archive/directory identity and version evidence;
4. preserve original encoding and line endings in the frozen copy;
5. establish a dedicated immutable B0 source commit before any fixes or modernization.

No production code is present under `src/` as a result of PREP01.

# ANIMO5 PREP01 provenance

## Scope

This record freezes the provenance of the evidence available to ANIMO-PREP01 on 2026-09-08. It does not claim that unavailable legacy material does not exist elsewhere.

## Repository bootstrap

- Repository: `abhedwig-cell/ANIMO5`
- Initial repository commit: `0fb4758bdaa55eab28a3bf521fa2a5cffb1aa9b2`
- PREP01 branch: `work/animo-prep01-bootstrap`
- Import date: 2026-09-08
- Legal status: no LICENSE added because no legal basis was supplied or established in PREP01.

## Legacy source origin

Status: `BLOCKED_MATERIAL_NOT_AVAILABLE`

No ANIMO production Fortran source tree was present in the locally mounted PREP01 artifacts, and repeated project-file searches did not return an ANIMO production source tree. PREP01 therefore does not create a fictitious source baseline. `reference/source/` records the blocked state.

Source version: `NOT_ASSESSED`.

Frozen source commit: `NOT_AVAILABLE`.

## Legacy documentation origin

Status: `BLOCKED_TECHNICAL_DOCUMENTATION_NOT_AVAILABLE`

No ANIMO theory manual or user manual was available as an importable technical legacy artifact during PREP01. Project planning documents mentioning ANIMO modernization were found, but these are programme context, not a frozen theory/user-manual baseline.

Documentation version: `NOT_ASSESSED`.

Frozen documentation commit: `NOT_AVAILABLE`.

## Testcase origin

Available artifact: `ANIMO_testbank.zip` supplied to this ChatGPT project for PREP01.

- Original byte size: 7,659,314 bytes
- SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- ZIP file members: 119 files plus directory entries
- Top-level testcase directories: 9
- Per-file identity: `reference/testcases/testbank_manifest.csv`
- Parsed testcase metadata: `reference/testcases/testbank_inventory.json`

### Known transformations

The source ZIP used for analysis was not line-ending-normalized, re-encoded, renamed, or repacked.

Text files were decoded only for analysis, using UTF-8 where possible and falling back to Windows-1252/Latin-1. That decoding is not applied to the frozen source artifact.

Binary `.UNF` and `.bun` hydrology files are preserved unchanged in the supplied archive. Their internal record format was not decoded in PREP01.

### Persistence limitation

The GitHub connector available to this chat accepts UTF-8 text and Git blob content but does not expose a local-file upload parameter. The 7.66 MB binary ZIP therefore cannot be transferred byte-for-byte through the connector without embedding its entire base64 payload in the chat. PREP01 persists its exact SHA-256 and per-member hashes and treats the repository-side binary freeze as `BLOCKED_BINARY_UPLOAD_CAPABILITY`, not as completed.

## Original file identities

Exact member paths, byte sizes, CRC32 values, ZIP timestamps, SHA-256 values, and observed text encoding are listed in `reference/testcases/testbank_manifest.csv`.

## Evidence separation

PREP01 treats three evidence classes separately:

1. source behaviour: currently blocked because the production source tree is unavailable;
2. documentation/theory intent: currently blocked because technical legacy documentation is unavailable;
3. testcase behaviour: input packages are inventoried and hashed, but numerical behaviour is not qualified because the ANIMO executable/source and trusted expected outputs are unavailable.

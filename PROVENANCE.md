# ANIMO5 PREP01 provenance

## Scope

This record identifies the evidence supplied to ANIMO-PREP01 on 2026-09-08. Source, documentation and testcase evidence remain separate and none is automatically treated as scientific truth.

## Repository bootstrap

- repository: `abhedwig-cell/ANIMO5`
- initial repository commit: `0fb4758bdaa55eab28a3bf521fa2a5cffb1aa9b2`
- PREP01 branch: `work/animo-prep01-bootstrap`
- import date: 2026-09-08
- legal status: no LICENSE added because no legal basis was supplied or established.

## Legacy source

Supplied project artifact: `ANIMO_4.1.5.53(3).zip`.

- size: 350,696 bytes
- SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- 65 file members under `ANIMO_4.1.5.53/`
- exact member identities and hashes: `reference/source/source_manifest.csv`
- archive transformations: none for analysis; archive was inspected without rewriting or repacking

`Version.inc` self-identifies the source as tag `animo4.1.5`, revision `53`, and names Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64] as the build toolchain. This is embedded source evidence, not independent authentication of the archive origin.

The raw archive is not republished to the public GitHub repository because no redistribution licence or equivalent legal basis has been established. Its byte identity is cryptographically pinned. A controlled retained B0 byte snapshot remains required before the source-freeze deliverable can be called fully complete.

## Legacy documentation

Supplied project artifact: ANIMO 4.0 user's guide, Alterra Report 224, Renaud, Roelsma and Groenendijk, 2005.

- SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`
- evidence role: ANIMO 4.0 user, I/O, example, mass-balance and technical-program documentation, with summarized model theory
- version limitation: it documents 4.0, not the supplied 4.1.5 revision 53 source
- completeness limitation: it refers to additional publications for comprehensive theory

The report carries an explicit copyright restriction. Its full bytes are therefore not republished to the public repository without an established legal basis. The exact document identity and evidence role are retained by hash and inventory.

## Testcase evidence

Supplied artifact: `ANIMO_testbank.zip`.

- size: 7,659,314 bytes
- SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- 119 files
- 9 top-level testcases
- exact member identities: `reference/testcases/testbank_manifest.csv`
- parsed metadata: `reference/testcases/testbank_inventory.json`

The testbank was not line-ending-normalized, re-encoded, renamed or repacked for analysis. Binary hydrology files remain undecoded as reference bytes.

## Evidence separation and current qualification boundary

1. **Source:** a concrete 4.1.5 revision-53 candidate is now available and hash-inventoried. Its exact build and behavioural status are not yet qualified.
2. **Documentation:** a 4.0 technical user's guide is available and hash-inventoried. It is useful evidence but not an exact 4.1.5 theory specification.
3. **Testcases:** nine input packages are inventory-frozen, but no numerical oracle has yet been qualified.

No source, documentation or testcase difference is silently corrected in PREP01.

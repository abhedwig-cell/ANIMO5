# PREP01 evidence inventory

## Evidence available

### Testcase package

`ANIMO_testbank.zip` is the only complete ANIMO legacy artifact made available locally to PREP01. Its binary bytes are not yet persisted in GitHub; the exact archive hash and member manifest are persisted.

Observed facts:

- 9 top-level testcase directories;
- 119 files in the archive;
- `animo.ini` in every testcase identifies `Animo41`;
- several legacy input files contain comments identifying ANIMO version 4.0 or 4.1;
- five Windows runner scripts are present;
- runner scripts refer to `animo41.exe` or `ANIMO` from PATH;
- no executable is present;
- no testcase `Output/` directory contains numerical output;
- hydrologic input is supplied through `.UNF` or `.bun` binary files;
- exact numerical testcase behaviour has not been reproduced.

### Programme/context documents

Project-file search returned planning/context documents that describe ANIMO modernization needs such as code revision, a test bench, documentation, input-data improvement, and version control. These are useful governance context but are not treated as legacy model theory or behavioural evidence.

### LWKM workflow context

Project material also contains an LWKM process register with an ANIMO handoff step after hydrological QA/QC. This is architecture/context evidence only. It does not define ANIMO internal source behaviour.

## Evidence unavailable

### Production source

`BLOCKED_MATERIAL_NOT_AVAILABLE`.

No ANIMO production source tree was available for import. Therefore PREP01 cannot source-bound assess:

- Fortran standard/legacy constructs;
- module/common/global state;
- call graph;
- argument semantics;
- compiler errors/warnings;
- I/O routines;
- process ordering;
- mass-accounting implementation;
- precision declarations;
- hidden side effects.

### Theory/user documentation

`BLOCKED_TECHNICAL_DOCUMENTATION_NOT_AVAILABLE`.

No technical ANIMO theory/user manual was available for import. Theory-code reconciliation is therefore not started beyond registering gaps.

### Trusted numerical oracle

`BLOCKED_EXPECTED_OUTPUT_NOT_AVAILABLE`.

The testbank does not contain trusted output sets in its Output directories. `initial.out` files found in two input areas are not classified as expected results without provenance.

## Evidence status vocabulary

- `FACT`: directly observed in the available artifact;
- `INFERENCE`: derived from one or more observed facts;
- `HYPOTHESIS`: plausible but unverified interpretation;
- `NOT_ASSESSED`: no adequate evidence yet.

# I/O dependency inventory

## Scope boundary

Source-level I/O dependency mapping is `BLOCKED_SOURCE_UNAVAILABLE`.

PREP01 can, however, map the external file contract visible in the testcase steering files. This is testcase-observed interface evidence, not proof of internal routine ownership.

## Observed `animo.ini` roles

| Key | Observed role from filenames/configuration | Provisional future ownership |
| --- | --- | --- |
| GEN | general simulation/options input | configuration / numerical and physical options to separate later |
| MAT | material definitions | parameters |
| PLA | plant/crop definitions | parameters / crop contract |
| SOI | soil/profile definitions | parameters / initial structure |
| BOU | boundary chemistry conditions | forcing / boundary contract |
| INI | initial model values | initial state |
| MAN | management schedule | forcing / management |
| SWU | hydrologic binary input (`SWATRE.UNF`, `swap.bun`, `result.bun`) | hydrology exchange / forcing |
| WAI | water-balance text input when used | hydrology input, exact semantics NOT_ASSESSED |
| WAU | water-balance binary input when used | hydrology input, exact semantics NOT_ASSESSED |
| CHE | chemistry parameters | parameters |
| CRU | external crop input | crop exchange / forcing |
| INO | `initial.out` target | restart/state serialization candidate |
| MES | `message.out` target | diagnostics/reporting |

This ownership column is an architectural mapping hypothesis for later separation. It is not a claim about current legacy implementation.

## Runner-observed output behaviour

Legacy runner scripts copy top-level `*.bal`, `*.out`, and in one case `*.csv` files into an `Output` directory, then delete the top-level copies. Exact producer routines and numerical semantics are `NOT_ASSESSED`.

## Current gaps

- all frozen Output directories are empty;
- exact generated output filenames are unavailable;
- six testcases have one or more unresolved `animo.ini` path references;
- the internal binary hydrology format is not decoded;
- no source exists to map OPEN/READ/WRITE/CLOSE calls to compute routines.

## Architectural target retained

The future ANIMO5 computational kernel must not know file units, paths, parsing, serialization formats, or report formats. Legacy file behaviour may survive behind adapters.

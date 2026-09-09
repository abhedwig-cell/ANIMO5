# I/O dependency inventory

Evidence level: `SOURCE_BOUND_BASELINE`.

## Architectural observation

Legacy ANIMO 4.1.5 is not separated into a file-free computational kernel. File parsing, file opening, reporting, restart output and runtime diagnostics are spread over dedicated I/O routines and are connected directly to the main time-step program through very large argument lists and file-unit arguments.

This is an architectural finding, not a scientific defect.

## Source-bound I/O ownership

| Routine / area | Observed responsibility | Future ANIMO5 boundary hypothesis |
| --- | --- | --- |
| `Input1` | reads steering/general/material/plant/soil/boundary/initial configuration and performs input checking | parser/adapters -> parameters, initial state, config |
| `Input_addit` | reads time-dependent management/addition events | management forcing adapter |
| `Input_cropext` | reads external crop input | crop exchange adapter |
| `Input_hydro` | reads dynamic hydrology records | hydrology exchange adapter |
| `Input_SoilTemper` | reads externally supplied soil temperature | forcing/exchange adapter |
| `Input_Echo` | opens/writes input echo and intermediate report stream | diagnostics/report adapter |
| `Outbal_write` | opens/writes balance files | mass-diagnostic serialization adapter |
| `Outsel` | opens/writes selected state/flux outputs | results serialization adapter |
| `Output_Init` | writes final/restart-style state output | explicit state serialization adapter |
| `grass_init` / output routines | opens/writes crop reporting | results adapter |
| `Animo.for` | central STOP/error termination control and top-level call orchestration | runtime controller, no file I/O in future kernel |

A static statement scan confirms extensive legacy I/O: dozens of `OPEN`/`CLOSE` operations and hundreds of `READ`/`WRITE` statements are present. Exact semantics remain routine-specific and must be audited before extraction.

## External file contract

The 4.0 user's guide documents the principal external contract as general/default files, field-specific nutrient files and hydrological files. The supplied testbank and 4.1.5 parser confirm the continued use of `animo.ini` indirection and roles such as `GEN`, `MAT`, `PLA`, `SOI`, `BOU`, `INI`, `MAN`, hydrology, chemical parameters and external crop input.

Provisional ANIMO5 ownership mapping:

- material/soil/chemical/plant definitions -> parameters;
- initial profile quantities -> state initialization;
- management/boundary/weather/hydrology/crop time series -> forcing or exchange;
- numerical/output switches -> numerical/runtime configuration, to be separated from physical configuration;
- `INITIAL.out` semantics -> state checkpoint/restart serialization candidate;
- balance and message output -> diagnostics/results, not kernel file operations.

## Binary hydrology boundary

The supplied testbank contains binary hydrology files including `SWATRE.UNF`, `swap.bun` and `result.bun`. The legacy source uses unformatted Fortran reads. A GNU/Linux probe does not read at least the supplied `SWATRE.UNF` using default GNU sequential-unformatted runtime semantics.

The binary record format, compiler-runtime convention and compatibility relationship therefore remain an explicit blocker. No binary file is converted or reinterpreted in PREP01.

## Target retained

The ANIMO5 computational kernel must not know file units, paths, parsing, serialization or report formats. Legacy file behaviour may be retained behind adapters after behaviour is qualified.

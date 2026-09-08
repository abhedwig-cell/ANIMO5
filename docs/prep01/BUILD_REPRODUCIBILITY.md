# Legacy build and reproducibility assessment

Status: `BLOCKED_SOURCE_AND_EXECUTABLE_MISSING`.

## Observed environment

PREP01 runtime tools:

- GNU Fortran 14.2.0 available;
- CMake 3.31.6 available;
- GNU Make 4.4.1 available;
- Intel `ifort`/`ifx` not observed;
- `flang-new` not observed;
- Wine not observed.

These tool versions are environment facts only. They do not establish the historical ANIMO compiler.

## Source-bound build assessment

Not possible because the ANIMO production source tree is unavailable.

The following remain `NOT_ASSESSED`:

- Fortran language level;
- fixed/free source form;
- compiler extensions;
- required compiler/vendor;
- compiler flags;
- external libraries;
- generated files;
- compile/link order;
- platform-specific APIs;
- record-format assumptions for binary hydrology input;
- reproducibility under GNU Fortran.

## Testcase execution assessment

Five runner scripts were observed. Four call `..\animo41.exe`; one calls `ANIMO` from PATH. The archive does not contain the executable. The remaining four cases contain no runner script.

Therefore no legacy testcase is executable from the frozen package alone.

The absence of some files referenced by `animo.ini` is recorded separately. Their mandatory/optional semantics cannot be decided without the parser/source or a working executable.

## Build gate

PREP01 build gate result:

`BLOCKED_AUTHORITATIVE_SOURCE_REQUIRED`

No attempt is made to patch input, invent a build system, or substitute a different ANIMO version.

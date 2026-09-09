# Legacy input contracts and normalization boundaries

## 1. Grammar strata

Revision 53 does not have one text grammar.

### Direct file

The direct file begins with exactly `Animo40` or `Animo41` in the first seven characters. Following records are read as a four-character selector plus an 80-character string until `END`. `Strip` removes leading spaces, tabs and double quotes and only retains a filename if it finds a closing double quote. A duplicate selector overwrites the previous filename binding. An unrecognized selector is not rejected in the selector loop. Missing required bindings are detected when the associated file is opened or when a feature requires it.

These are observed quirks. A new adapter may diagnose them more clearly, but a `REPRESENTATION_ONLY_ADAPTER_CHANGE` cannot silently reinterpret historical files.

### Label-addressed files

`Findadr` rewinds the file and compares the first eight characters of records to the exact label. This gives three consequences:

- independent section order is mostly irrelevant when every section is located through `Findadr`;
- duplicate labels resolve to the first occurrence;
- case/spelling and the first eight characters matter.

The traditional ANIMO40 grammar then uses list-directed positional records after the label. Comments are safe as records outside the data records; they are not a general inline-key grammar.

### ANIMO41 sequential named records

Some GENERAL sections use `ReadOp`, `Readvals`, `Readints` and `ReadTs`. These routines read the next record and compare its left-hand name with the expected name. They do not search by key. `ReadOp`, `Readvals` and `Readints` derive the value substring from `=` to `!`.

Therefore the historical ANIMO41 contract is sequence-sensitive even though its records resemble TTUTIL. Direct TTUTIL parsing, which is name-based and order-independent, would expand the accepted-input language unless a strict compatibility validator is placed in front of it.

### Sequential event streams

`Input_addit` uses `Findadrfix`, which scans forward without rewind, for `>addNNN:` event labels. It also uses `BACKSPACE` and condition-dependent record consumption. Management event order and record counts are therefore semantic input-structure constraints, not presentation details.

### Fixed table/series formats

`Input_cropext` and `Input_SoilTemper` are separate fixed time-series contracts. `Input_cropext` performs date/timestep validation and conversions after reading. `Input_SoilTemper` skips eight header records and reads fixed columns. These routines should first be split into lexical parser, normalized forcing record and scientific/time validation before considering reuse of TTUTIL utilities.

## 2. Parsing, normalization and science must remain separate

Example, external crop input:

- parsing: decode date and eight numeric columns;
- normalization: bind each column to a typed field, preserve input units/provenance and construct timestep records;
- scientific/time semantics: validate compatibility with ANIMO timestep, apply the source-authorized conversion to internal areic quantities and apply any correction logic.

Moving all three into a TTUTIL call would make the library an accidental scientific authority. IO01 forbids that.

## 3. Conditional fields

A normalized object never uses absence to mean several different things. Every field is one of:

- required and present;
- conditionally required and present because its feature condition is active;
- explicitly null because the feature is inactive;
- populated by an identified legacy default, with `default_applied=true` and an explicit default rule id.

Supplying active-only fields while the feature is inactive is a contract question that must be tested per family. It must not be silently retained in an untyped bag.

## 4. Unknowns, duplicates and ordering

No global policy is invented. Legacy behaviour differs by grammar:

- direct file unknown selector: historically ignored by the selector loop;
- direct file duplicate known selector: later assignment wins;
- duplicate eight-character section label found through `Findadr`: first occurrence wins;
- ANIMO41 sequential named record: unexpected name in the next required position is rejected, except documented source compatibility fallbacks;
- management event block: sequence is required.

A future native TTUTIL schema should be stricter and versioned, but that would be a new representation contract. It cannot be mislabeled legacy-equivalent.

## 5. GHGMais

GHGMais is retained as lineage-sensitive B0 evidence. The supplied schema contains GHG values under `>defGHG:` and has a `>deffra:` layout that does not match the revision-53 parser. Revision 53 requires `>outGHG:` and later `>orgcom:` on the active GHG route. IO01 therefore defines only two valid outcomes for GHGMais input support:

- `VERSIONED_LEGACY_ADAPTER` once the consuming lineage is provenance-qualified; or
- `LINEAGE_UNRESOLVED_REJECT` under the revision-53 adapter.

Combining both schema families into one permissive reader is prohibited.

## 6. Binary hydrology and restart

`SWATRE.UNF`, `WATBAL.UNF`, `SWAP.BUN` and `result.bun` remain specialized external exchange formats. Their normalized semantic payload should ultimately satisfy ARCH05 hydrology frame contracts, but TTUTIL is not the reader.

`INITIAL.OUT` is state serialization. Its textual appearance does not make it ordinary configuration. A restart adapter must be qualified against state ownership and split-run/restart sufficiency separately.

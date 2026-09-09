# TTUTIL public context and ANIMO boundary consequence

Evidence in this file is public TTUTIL/SWAP context, not ANIMO-specific behavioural authority.

The public TTUTIL version-4 manual describes a name-based reader family (`RDINIT`, `RDSINT`, `RDSREA`, array readers and range-checking variants). TTUTIL analyses a data file and lets callers request values by symbolic name. The manual explicitly demonstrates that call order need not match file order. Current SWAP documentation likewise describes TTUTIL-format input as free-format `VariableName = value`, with array tables, comments and blank lines.

That makes TTUTIL technically useful for typed lexical decoding, arrays, range-aware readers and clearer input code. It also creates a direct compatibility issue with revision-53 ANIMO:

- most legacy ANIMO files are eight-character label plus positional records, not native TTUTIL files;
- `Animo41` GENERAL records look name-based but `ReadOp`, `Readvals`, `Readints` and `ReadTs` consume the next record sequentially, so key order is part of the observed parser contract;
- the revision-53 helpers slice named values between `=` and `!`, so the comment delimiter participates in actual parsing;
- `Findadr` rewinds and finds the first exact eight-character label, while `Findadrfix` searches forward for management event sections.

Therefore a direct substitution of TTUTIL for the revision-53 parser would broaden or otherwise change accepted syntax. Such a change is not `REPRESENTATION_ONLY_ADAPTER_CHANGE` unless a strict legacy compatibility layer preserves the relevant old accept/reject contract.

IO01 consequently distinguishes two future adapters:

1. `LegacyRevision53TextAdapter`, which accepts the legacy grammar and normalizes it exactly;
2. a possible `TTUTILNativeTextAdapter`, which may offer a cleaner versioned text representation but must map to the same normalized objects and must never silently replace the legacy grammar.

The second adapter is a new representation. It is not evidence that TTUTIL can natively parse all historical ANIMO files.

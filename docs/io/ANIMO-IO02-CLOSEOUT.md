# ANIMO-IO02 closeout

Status: `CLOSEOUT_READY_BOUNDED_GENERAL_REPRESENTATION_QUALIFICATION_COMPLETE`

Decision:

`QUALIFIED_BOUNDED_REV53_GENERAL_NORMALIZED_REPRESENTATION_WITH_EXPLICIT_LEGACY_HAZARD_EXCLUSIONS`

## Work unit

`ANIMO-IO02 — GENERAL.INP Strict Legacy Grammar, Ordering & Normalized Representation Qualification`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-io02-general-input-normalization`

Upstream IO01 head:

`2bcf65360b08d278f28f1cc61ac96714db4793a3`

Qualification baseline head:

`06c0371b72df9415bc76562188b10266fc8826db`

Qualification baseline CI:

- workflow: `IO02 GENERAL contract audit`;
- run: `34386275458`;
- conclusion: `success`;
- 11/11 unit tests passed;
- persisted qualification audit passed.

Closeout commits after that qualification baseline contain only bounded evidence, documentation and closeout/audit wiring. They do not widen the qualified parser claim.

## Frozen identities

IO02 used the same frozen ANIMO evidence lineage as IO01:

- revision-53 source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- ANIMO testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- supplied `animo41.vfproj` SHA-256: `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`;
- supplied documentation SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

No frozen source or testbank bytes were changed.

## What is qualified

IO02 qualifies a bounded normalized representation of revision-53 `GENERAL.INP` for the admitted non-GHG grammar. The representation preserves the parser contract before any physics execution.

The typed target boundary is restricted to:

- `ModelConfiguration`;
- `SimulationWindow`;
- `DiagnosticsConfiguration`.

The complete machine-auditable grammar is persisted at:

`integration/animo-io/GENERAL-REV53-GRAMMAR.json`

The detailed natural and mutation evidence is persisted at:

`integration/animo-io/ANIMO-IO02-QUALIFICATION.json`

The human-readable contract is:

`docs/io/GENERAL_INPUT_CONTRACT.md`

## Ordering result

The strongest correction to the initial IO01 shorthand is that revision-53 GENERAL ordering has two levels.

At top level, complete section blocks are not required to occur in parser call order because every `Findadr` call rewinds the file and performs a fresh exact A8 label search. A complete `>simtim:` block can therefore be physically moved relative to `>outscr:` without changing the qualified semantic projection.

Within a located section, ordering is strict. `ReadOp`, `ReadTs`, `Readvals` and `Readints` consume the next record and do not search forward. Reordering individual options changes or breaks the legacy parse contract.

The qualified representation is therefore deliberately not a free-order key/value object.

## Source-observed compatibility behaviour

Only source-observed defaults are admitted.

`PClassOption=` has an explicit compatibility path. On an ordered-record mismatch, `ReadOp` consumes the record and reports an error; the caller clears that error and assigns `IoptPCl=0`. This is represented as a `DEFAULTED` value with an explicit rule id, not as a generic parser default.

`HydroYearSwitch=` has a comparable mismatch default to zero. More importantly, revision-53 subsequently checks `IoptPCl` rather than `HydrYrSw`. The natural LWKM GENERAL contains `HydroYearSwitch=-30`, and the executable source therefore does not reject that value at this point. IO02 preserves `-30`; inserting a new range check would change the legacy grammar/validation contract.

## Repeated balance structures

`NumberOfPrintBal=` owns a repeated ordered balance structure. `PrintBalUpdDate=` has cardinality derived from `PrintBalNoUpd` when the latter is neither -1 nor 0.

Revision-53 sorts balance update dates after parsing. IO02 therefore distinguishes:

- lexical input order, retained as source provenance;
- post-parser semantic order, retained as the normalized value.

The supplied executable project uses `RealKIND="realKIND8"`, so these GENERAL real values are treated as binary64 in this bounded executable representation. No blanket tolerance is introduced.

A negative `PrintBalNoUpd` below -1 is not assigned normalized repeat semantics. The source `Checkint` call uses its `999` no-lower-bound sentinel, so such values can pass that check, but that does not establish a safe or intentional repeat contract.

## Output selector grammar

`>outsel:` is strongly sequential. It includes seven output groups, with one consumed separator record before each group. The complete exact key sequence and `Outse` indexes are frozen in the grammar manifest.

`ReadTs` is a source-specific lexical parser. After the expected key prefix it scans the remainder of the record for the first character `0`, `1`, `2` or `3`. That digit can occur in comment text. The values encode file-output and selected-compartment-output flags.

A conventional integer parser would therefore not be source-equivalent.

Two late selectors, `AnnDOMNtotNO3_1mGWL=` and `DOMNtotNO3_1mGWL=`, have a special mismatch path: revision-53 sets file output to zero and clears the parser error, but leaves the selected-compartment storage unassigned. IO02 records that state explicitly as `LEGACY_UNDEFINED_IF_OMITTED`; it does not synthesize zero.

Several WholeProfile calls also send the second `ReadTs` selector to `idum` while a later global check inspects `OutseLn`. These storage states are not input-defined values and remain outside the normalized value claim.

## Natural testbank result

The frozen testbank contains nine GENERAL files.

Seven non-GHG cases satisfy the bounded revision-53 representation contract:

- CranGrass;
- CranMais;
- LWKM grass;
- Puitmijn Cranendonck;
- RuurloGrass;
- STONE akkerbouw;
- Zuiderzeeland MeeuwenTocht.

`GrassPeat` is retained as negative evidence. At line 118 it contains `WFPS=` where the revision-53 sequential reader expects `O2_content=`. The bounded observer consequently reaches the revision-53 `9871` sequence mismatch. IO02 does not reinterpret this as a valid extension of GENERAL.

`GHGMais` is explicitly excluded because `GreenHouseGasOption=1` routes into the unresolved GHG schema. No `>outGHG:` payload is admitted by IO02.

## Mutation qualification

Thirteen targeted probes are persisted and pass the intended contract assertions. They cover:

- physical reordering of complete top-level sections;
- illegal reordering within `>simopt:`;
- missing exact-A8 label;
- shifted ordered key;
- PClass compatibility default;
- natural negative HydroYearSwitch;
- `ReadTs` comment-digit scanning;
- positional date-record semantics;
- post-parser balance-date sorting;
- late optional output omission with explicit undefined-storage hazard;
- `PrintBalLabel` mismatch return-without-error path;
- EOF at a required `ReadOp`;
- GHG route-only boundary.

## TTUTIL boundary

IO01 qualified exact TTUTIL 4.27 provenance and bounded representation pilots. IO02 does not reopen or widen that result.

TTUTIL may be parser infrastructure in a later GENERAL adapter, but it is not the authority for:

- GENERAL field ordering;
- source compatibility defaults;
- feature activation;
- `ReadTs` lexical selector semantics;
- ANIMO numeric/scientific policy.

Any future adapter must constrain TTUTIL or any other parser infrastructure to the strict revision-53 contract rather than allowing the infrastructure to define a more permissive grammar.

## Explicit non-admissions

IO02 does not admit:

- production input migration;
- GENERAL grammar redesign;
- free ordering of sequential GENERAL records;
- silent default insertion beyond source-observed rules;
- GHGMais schema admission;
- generic GHG schema admission;
- binary hydrology;
- INITIAL migration;
- restart/checkpoint migration;
- broad reopening of IO01;
- TTUTIL as scientific authority;
- TTUTIL as numeric authority;
- conversion of undefined storage into fabricated configuration values;
- production activation;
- canonical merge on the authority of IO02 alone.

## Handoff

A future GENERAL adapter may consume `General41NormalizedRepresentation/v1` and the machine-auditable grammar only if it preserves the bounded ordering, compatibility defaults, lexical semantics and hazard exclusions qualified here.

GHG schema work requires a separate scoped qualification. INITIAL/restart remains a specialized state contract. Production migration requires a separate admission decision and cannot be inferred from representation qualification.

## Final boundary

ANIMO-IO02 is complete as a parser-boundary qualification work unit.

The result is not that GENERAL has been migrated. The result is that revision-53 GENERAL grammar is now explicit enough to prevent a future parser replacement from silently making the input language more permissive, inserting new defaults, changing numeric representation, or hiding storage hazards.

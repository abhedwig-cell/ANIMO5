# ANIMO-PREP02 — Legacy Reference Build and Behavioural Qualification

Status: `PLANNED_FAIL_CLOSED_REFERENCE_ENVIRONMENT_REQUIRED`.

## Purpose

PREP02 resolves the central blocker left by PREP01: the repository has a deterministic modern diagnostic execution route, but no build or executable is yet admitted as behavioural truth for the supplied legacy ANIMO source.

PREP02 is qualification-only. It does not start ANIMO5 production migration and it does not silently correct any PREP01 defect.

## Exact starting evidence

PREP02 starts from the PREP01 evidence head that includes:

- source archive `ANIMO_4.1.5.53(3).zip`, SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- nine-case testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- ANIMO 4.0 User's Guide SHA-256 `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`;
- deterministic GNU diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`;
- source-derived build-contract hypotheses in `docs/prep01/HISTORICAL_INTEL_BUILD_CONTRACT.md`;
- deterministic diagnostic execution for eight supplied cases;
- causal mass-ledger evidence TCD-014 through TCD-018.

The exact source bytes remain frozen. Diagnostic adapters and probes do not redefine that source.

## Evidence classes

PREP02 uses four non-interchangeable evidence classes.

### B0_SOURCE

Exact supplied source, documentation and testcase identities. No behavioural claim.

### HISTORICAL_NATIVE_REFERENCE_CANDIDATE

An executable or build produced with the historical Intel compiler lineage and a source/project configuration whose provenance is sufficiently explicit to test as the original behaviour contract.

This class is not automatically trusted merely because it uses Intel Fortran.

### EQUIVALENT_REFERENCE_CANDIDATE

A modern or reconstructed build admitted only after it matches an independently trusted native reference over the required behavioural surfaces.

The current GNU build remains `DIAGNOSTIC_NOT_REFERENCE` until this gate passes.

### CORRECTED_LEGACY_CANDIDATE

A later build containing one or more explicitly admitted corrections to frozen legacy defects. It must never overwrite or masquerade as the frozen reference.

## Serial qualification gates

### P2-G0 — Controlled B0 availability

Required:

- exact source ZIP hash matches PREP01;
- exact testcase ZIP hash matches PREP01;
- documentation identity is pinned;
- raw artifacts are available in a legally controlled location to the qualification runner;
- extraction preserves exact member bytes.

Failure is fatal for reference qualification.

### P2-G1 — Historical build-contract reconstruction

First candidate should minimize invented options.

Historical/source evidence currently supports testing:

- Intel Visual Fortran Composer XE 12.1.0.233, Intel 64;
- PowerStation-compatible unformatted I/O semantics, plausibly `/fpscomp:ioformat`;
- eight-byte default `REAL`, plausibly `/4R8` or `/Qautodouble`;
- Intel default local-storage behaviour before introducing `/Qsave`;
- exact source-unit selection must be explicit, including choice of `input1.for` versus `input1_1.for` and `Outsel.for` versus `Outselorg.for`;
- optimisation, floating-point model, alignment, preprocessing and link flags must be recorded rather than guessed away.

PREP02 must run controlled build variants when an option is uncertain. A variant that merely produces successful completion is not sufficient.

### P2-G2 — Minimal native behavioural case

Primary first case: `RuurloGrass`.

Reason:

- it is one of the supplied legacy-style cases;
- the ANIMO 4.0 guide explicitly describes the Ruurlo carbon/nitrogen example family;
- it avoids the known GHGMais lineage mismatch;
- it avoids using the already identified PO4 initialization seam as the first build-equivalence discriminator;
- it already completes deterministically in the GNU diagnostic route.

Admission requires:

- successful completion under the native candidate;
- complete output-file inventory and hashes;
- exact runtime/build metadata;
- no silent input translation;
- all warnings and STOP semantics captured;
- hydrology bytes used by the native run identified exactly.

### P2-G3 — Native versus GNU behavioural equivalence

Compare the current GNU diagnostic candidate with the admitted native run at several levels.

Level 1, compatibility surface:

- output file set;
- record counts;
- formatted output values;
- message/warning classes;
- balance-period boundaries;
- simulation start/end and hydrology alignment.

Level 2, numerical surface:

- values parsed numerically before formatting where the output precision permits;
- mass-balance terms and residuals;
- cumulative uptake/loss quantities;
- key state trajectories available in ordinary legacy output.

No global tolerance is invented up front. Differences are classified by variable, unit, scale, formatting precision and known compiler semantics.

A single successful case is sufficient only for a first `REFERENCE_BUILD_CONTRACT_CANDIDATE`, not for full scientific admission of all ANIMO processes.

### P2-G4 — Observer-only unrounded reference capture

Formatted legacy files are not enough for later scientific qualification.

After a native behavioural build is established, create an observer-only build from the same source/compiler contract that emits high-precision internal values at selected qualification seams.

Observer rules:

- no state or process calculation may be changed;
- ordinary legacy output must remain identical to the non-observer native build;
- observers write only additional evidence streams;
- observer points and types/kinds are source-bound and reviewed;
- the observer build must reproduce the same legacy outputs before its extra streams are trusted.

Initial observer targets:

- complete mass-ledger terms before formatted output;
- storage before/after each accepted timestep;
- boundary transport terms;
- `Transsub` inputs/outputs for selected substances;
- initialization stores used in PO4 reconciliation;
- water stores including interception, snow, ponding and soil water where active.

This is the preferred route to a trusted unrounded reference oracle.

### P2-G5 — Expand reference coverage

After Ruurlo, use cases selected for specific process coverage rather than simply running everything and declaring parity.

Suggested sequence:

1. `CranGrass`, including P and the TCD-014 initialization seam;
2. `LWKM_gras_1040.2021.2045`, including TCD-015 NO3, TCD-017 organic-P and TCD-018 water-ledger evidence;
3. `Puitmijn_Cranendonck_60`, including TCD-016 surface NH4 dry-down;
4. remaining compatible supplied cases;
5. `GHGMais` only after source/testcase lineage is resolved.

Known deterministic defects are expected to appear in the frozen reference if they are genuinely historical. Reproducing a defect is evidence of parity, not approval of that defect for ANIMO5.

## Corrected-legacy admission sequence

Corrections start only after the relevant frozen behaviour is reference-qualified.

For every correction:

1. freeze the original source/event/output evidence;
2. state the scientific or algebraic invariant being violated;
3. make the smallest correction in a separate corrected-legacy lineage;
4. run causal local tests;
5. run the full reference case;
6. prove unrelated outputs remain unchanged within the explicitly admitted equivalence policy;
7. update theory-code-evidence reconciliation;
8. admit or reject the correction independently.

Current candidate defect work:

- TCD-014: PO4 initialization consistency policy, correction not yet defined;
- TCD-015: NO3 negative-concentration `Reko` algebra;
- TCD-016: NH4 wet-to-dry state representation, requires theory/state decision rather than the pathological tiny-outflow workaround;
- TCD-017: organic-P redistribution balance bookkeeping;
- TCD-018: interception-storage coverage in the water ledger interface.

## Fail-closed decisions

PREP02 must not:

- declare the GNU build a reference because eight cases are deterministic;
- infer Intel flags solely from options that make GNU output look plausible;
- modify GHGMais input to fit revision-53 source;
- define mass-balance tolerances from known legacy residual defects;
- merge corrected behaviour into the frozen reference;
- start production process migration before the required reference gate is passed.

## Exit states

Possible PREP02 exits include:

`QUALIFIED_MINIMAL_NATIVE_REFERENCE_BUILD_CONTRACT`

This means at least one native case and build contract are sufficiently proven to anchor later equivalence work. It is not whole-model scientific qualification.

`QUALIFIED_EQUIVALENT_REFERENCE_BUILD_CONTRACT`

This additionally admits a reconstructed build, such as GNU, against independent native evidence for a defined scope.

`BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`

Use when no independently trustworthy native executable/build environment can be obtained and equivalence therefore cannot be established.

`BLOCKED_B0_CONTROLLED_RETENTION_REQUIRED`

Use when raw reference artifacts cannot be made available under an acceptable retention/redistribution arrangement.

`BLOCKED_REFERENCE_CONTRACT_AMBIGUOUS`

Use when multiple plausible historical build contracts produce materially different behaviour and no provenance can select among them.

## Current PREP02 state

Planning and admission criteria can be implemented now. Actual reference qualification remains blocked until an appropriate historical native executable or build environment and controlled B0 artifact access are available.

Production migration remains `NOT_ADMITTED`.

# ANIMO-KT16 Work Unit Contract

Workunit: `ANIMO-KT16 - Accepted Application Checkpoint Materialization & Split-Run Restart Qualification`.

Execution discipline: `RECONCILE -> ARCHITECTURE BINDING -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT16 materializes a typed, nonproduction checkpoint for the bounded accepted application aggregate qualified by KT15A and proves exact split-run restart equivalence for that bounded modern runtime path.

The checkpoint is created only from an already accepted application state. It contains no trial state, retry state, transfer journal, scratch or diagnostics.

## Authorities

Program:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Accepted application identity:

`ANIMO-KT15A@2279a961459211e03550dfda4af09ab4f7f6b9a3`

Restart architecture design basis:

`ANIMO-ARCH02@a079d93c965f6073586c55ee4b3544dd8873b723`

ARCH02 remains candidate architecture only. KT16 uses its accepted-boundary-only rule without promoting ARCH02 to canonical checkpoint authority.

## Typed checkpoint record

`kt16_application_checkpoint_t` carries:

- checkpoint schema id;
- record kind `ACCEPTED_BOUNDARY_ONLY`;
- bounded science payload schema id;
- producer-contract id;
- lineage id;
- accepted generation;
- exact accepted TIME02 coordinate;
- layer-count identity;
- bounded TCD-042 accepted concentration;
- the complete KT15A immutable application configuration object;
- the complete STATEQ11 composite accepted continuation object.

The configuration is stored as its qualified public type with private internals rather than re-declaring its fields.

## Encode rule

Encoding requires a valid KT15A accepted application aggregate.

The encoder obtains information only through accepted-state APIs:

- `validate_kt15_application_state`;
- `kt15_application_generation`;
- `kt15_application_time`;
- `snapshot_kt15_application_config`;
- `snapshot_kt15_continuation`;
- `snapshot_kt15_science_payload`.

Only the bounded `tcd042_top_state_t` payload is supported.

## Restore rule

Restore first validates internal checkpoint coherence.

It then requires an externally expected KT15A configuration and demands exact `same_kt15_application_config` identity with the checkpoint configuration. This prevents restoring a valid checkpoint under a different runtime configuration.

The accepted store is reconstructed through the trusted KT02 reconstruction API using the checkpoint lineage, generation, accepted time and TCD-042 payload.

The application aggregate is then reconstructed through `initialize_kt15_application_state`, which re-validates science/continuation/config coherence.

## Split-run qualification

The qualification harness compares:

A. two uninterrupted accepted intervals;

B. one accepted interval, checkpoint encode, restore, second accepted interval.

The final states must match exactly for:

- science generation;
- accepted time;
- TCD-042 accepted concentration;
- continuation lineage and generation;
- hydrology-origin `Pn`, `Sic`, `Snla`, `Mofro`;
- `Runinu` continuation;
- boundary cursor state;
- immutable application configuration.

No tolerance is used for floating continuation comparisons.

## Negative qualification

The harness rejects:

- wrong checkpoint schema;
- a trial-like record kind;
- generation mismatch;
- lineage mismatch;
- accepted-time mismatch;
- layer-count mismatch;
- nonfinite science payload;
- restore under a different valid application configuration.

## Architecture boundary

KT16 is deliberately narrower than canonical ARCH02 restart admission.

It does NOT yet provide:

- a disk or binary checkpoint format;
- a cryptographic checkpoint integrity hash;
- exact executable/build commit identity inside the record;
- external SWAP/WOFOST coordinated checkpoint tokens;
- whole-model ANIMO physical state coverage;
- diagnostic-continuation persistence;
- historical revision-53 restart equivalence.

Those omissions prevent canonical checkpoint admission.

## Hard boundaries

No file I/O.
No checkpoint byte format.
No integrity-hash implementation.
No source-byte hash verification.
No canonical checkpoint admission.
No canonical state admission.
No B2 historical restart claim.
No trial/mid-step checkpoint.
No process-science change.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.

## Governance

This is a cross-module restart/state/runtime composition and is conservatively GOV04 Tier D.

Same-agent adversarial review can qualify the bounded candidate only. Genuine independent Tier D review remains required before admission.

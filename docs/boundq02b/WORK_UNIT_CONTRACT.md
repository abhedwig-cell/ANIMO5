# ANIMO-BOUNDQ02B Immutable Content-Bound Boundary Frame Qualification

## Purpose

BOUNDQ02B hardens the BOUNDQ02 interval chemistry frame before it is used as a scientific composition input.

BOUNDQ02 qualified source-faithful year-cursor selection and exact interval binding, but its public derived-type components allowed callers to mutate chemistry, year/slot metadata, forcing identity or dry-deposition values after construction.

That is weaker than the ANIMO5 architecture invariant for immutable external frames.

BOUNDQ02B adds an opaque wrapper with private components and content-bound forcing identity.

## Authorities

Program authority:

`ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`

Source-faithful year binding:

`ANIMO-BOUNDQ02@fb0c0c842aed9a90378aca613279e09a856ad09b`

BOUNDQ02 exact-final CI:

`35373354465 = success`

TIME02 exact calendar candidate remains inherited through BOUNDQ02.

## Architecture issue being repaired

A valid BOUNDQ02 frame could be constructed and then altered externally because `static_boundary_interval_frame_t` fields were public.

A downstream consumer could therefore observe changed chemistry under an already-established frame identity.

BOUNDQ02B makes the scientific frame opaque.

The new type:

`immutable_static_boundary_interval_frame_t`

has private components. External code receives frame content only through a validating inspector that returns copies.

Mutation of a returned chemistry copy cannot modify the stored frame.

## Content identity

BOUNDQ02B additionally requires a canonical 64-character lowercase SHA-256 content identity.

The identity is an upstream assertion about the BOUNDARY content consumed to create the normalized BOUNDQ01 representation.

The runtime forcing identity becomes:

`SHA256=<64 lowercase hex>:SLOT=<n>`

This makes the selected chemistry forcing identity explicitly dependent on both source content identity and year slot.

BOUNDQ02B validates this deterministic relation on every inspection.

BOUNDQ02B does not itself hash file bytes. Verification that the supplied SHA-256 corresponds to the source bytes remains the responsibility of the file/input adapter or host layer.

That limitation is explicit and prevents a false cryptographic verification claim.

## Construction

Construction receives:

- an already parsed BOUNDQ01 static boundary representation;
- its asserted canonical SHA-256 content identity;
- simulation start year;
- accepted BOUNDQ02 year cursor;
- exact origin and endpoint.

BOUNDQ02B calls BOUNDQ02 internally, using `SHA256=<content-id>` as the BOUNDQ02 source identity.

The mutable intermediate frame never leaves the constructor.

The opaque frame then stores copies of:

- source content SHA-256;
- exact origin and endpoint;
- simulation start year and source year count;
- selected year and slot;
- validated UBFORCE02 chemistry;
- separate dry NH and NI deposition values.

## Validation and access

The public inspector first validates the complete opaque frame and only then returns copies.

Validation checks:

- frame schema;
- canonical lowercase SHA-256 syntax;
- year/slot coherence and bounds;
- finite separate dry-deposition coordinates;
- deterministic content-and-slot forcing identity;
- chemistry reconstruction through the UBFORCE02 constructor;
- exact origin identity;
- exact endpoint identity.

The caller cannot directly modify stored components.

## Test evidence

The synthetic BOUNDQ01 no-P fixture used by BOUNDQ02B has SHA-256:

`629a94972504c2865f8f0cbae9960e1354f6acd09e39ef663cc8f74375a7a169`

Tests establish:

- exact content-bound forcing identity;
- exact chemistry and dry-deposition extraction;
- mutation of an inspected chemistry copy does not alter the frame;
- a different declared content SHA produces a different forcing identity;
- malformed and noncanonical SHA values fail closed;
- stale endpoint identity fails closed.

The different-SHA test demonstrates identity mechanics only. It is not evidence that an arbitrary supplied SHA actually hashes a source file.

## Governance

This is a runtime/exchange-frame integrity hardening workunit and is conservatively GOV04 Tier C.

Same-agent adversarial review can qualify the candidate but cannot satisfy independent Tier C review.

## Hard boundaries

No BOUNDARY parser change.
No source chemistry change.
No year-selection semantic change.
No dry-deposition process.
No file hashing implementation.
No claim that caller-provided SHA was independently verified.
No canonical forcing-state admission.
No checkpoint schema change.
No B3 mutation.
No TB7.
No B4.
No production.

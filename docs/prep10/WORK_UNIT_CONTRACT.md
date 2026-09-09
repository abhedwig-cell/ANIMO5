# ANIMO-PREP10 work-unit contract

## Work unit

**ANIMO-PREP10 — Stable-DOM plough accumulator audit**

Branch: `work/animo-prep10-stable-dom-plough-accumulators`

Source parent: `e3c3b0dfa8daabe345c51be8c4f29f2731d65c47` (`ANIMO-PREP09: close element-transfer and slow-sorption audit`).

This contract applies only to this stable-DOM accumulator branch. Other historical branches that also carry a PREP10 label are separate work histories and are not silently composed here.

## Purpose

Determine whether revision-53 `Addit.for` reads the event-local stable dissolved-organic matter, nitrogen and phosphorus plough accumulators before explicit definition, and determine whether the frozen testcase package contains a management path that requests the corresponding plough operation.

## Frozen evidence

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testcase archive SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The raw source and testcase archives remain external B0 evidence. This work unit may inspect exact supplied bytes and persist public-safe hashes, line locations, scanner code, synthetic unit tests and diagnostic metadata. It must not republish the raw archives.

## Allowed changes

- static source-audit tooling;
- frozen-testbank activation-audit tooling;
- synthetic unit tests for the scanners;
- machine-readable audit results;
- explanatory PREP10 documentation.

## Prohibited changes

- no modification of frozen revision-53 source;
- no modification of frozen testcase bytes;
- no silent initialization fix in `Addit.for`;
- no promotion of diagnostic output to reference output;
- no corrected-legacy or ANIMO5 production admission;
- no claim that compiler-dependent numerical manifestation has been quantified unless separately demonstrated.

## Qualification boundary

A static audit may qualify a **source-level use-before-definition** finding when the exact frozen source archive is hash-matched and the relevant assignments are demonstrated to self-read before any explicit definition.

A frozen-input audit may qualify that a testcase requests the relevant ploughing path. This is not equivalent to historical native execution or reference-output admission.

Runtime magnitude, compiler/storage manifestation, downstream scientific effect and corrected behavior remain separate gates.

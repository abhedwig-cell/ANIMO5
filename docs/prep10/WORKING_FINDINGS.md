# ANIMO-PREP10 — Stable-DOM plough accumulator audit

Status: `QUALIFIED_SOURCE_LEVEL_USE_BEFORE_DEFINITION_FROZEN_PLOUGH_INPUT_PRESENT_RUNTIME_MAGNITUDE_OPEN`.

## Purpose

PREP10 follows the revision-53 stable dissolved-organic matter ploughing path in `Addit.for`, with particular attention to whether event-local redistribution accumulators are defined before each management event.

Frozen source and supplied testcase bytes remain immutable. No production correction is admitted.

## Frozen identity

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## Qualified source-level finding

The exact frozen source archive was scanned with `tools/audit_stable_dom_plough_accumulators.py`. The audit hash-pins the archive before inspecting `ANIMO_4.1.5.53/Addit.for`.

`Addit.for` declares scalar local accumulators:

```fortran
Real :: SuStdiorma, SuStdiorni, SuStdiorpo
```

The plough branch begins at source line 449. Within that branch the first assignments to the three accumulators are self-reading assignments:

- `SuStdiorma`: line 475;
- `SuStdiorni`: line 477;
- `SuStdiorpo`: line 479.

No explicit definition or zero assignment occurs before those first self-reads, and no explicit zero assignment for these three scalars was found elsewhere in the file. The exact `Addit.for` member is 35,615 bytes with SHA-256 `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`.

The source-level classification is therefore:

`CONFIRMED_SOURCE_LEVEL_USE_BEFORE_DEFINITION`

This is stronger than the earlier "potentially material" wording. The finding no longer depends on guessing whether an explicit reset exists elsewhere in the routine. It is a reproducible source fact for the frozen revision-53 bytes.

## Frozen testcase activation evidence

`tools/audit_stable_dom_plough_activation.py` independently hash-pins the frozen testbank and inspects the CranMais inputs.

`ANIMO_testbank/CranMais/Input/MANAGEMENT.INP` contains nine explicit plough requests for the first two compartments, at lines 66, 93, 107, 121, 135, 149, 159, 169 and 179. The management member SHA-256 is `61458d7e849fd5e181133d62d0abc8f9b0eb2dbe0b0d45bdb3adf03e488446da`.

`ANIMO_testbank/CranMais/Input/Initial.inp` has the `>sdomin:` block at line 106. Its 69 listed stable soluble organic matter, nitrogen and phosphorus initial values on lines 107-109 are all zero. The member SHA-256 is `8df3d78e830f344bc315d4dff2ae4c1ee4d6e959a07ba7d112e4105e6fbbb201`.

This establishes a concrete frozen-input path requesting repeated ploughing. It does not establish that a provenance-qualified historical executable actually ran the case. Initial stable-DOM values being zero do not remove the source-level undefined read: the accumulator itself is still read before definition. The observed numerical value of such a read remains dependent on compiler/runtime/storage semantics.

## Verification

Seven synthetic scanner unit tests passed in the authoring environment:

```text
python -m unittest discover -s tests/prep10 -v
```

The exact source archive audit and exact frozen-testbank activation audit also passed against the supplied B0 bytes. Raw source and testcase archives were not added to Git.

Machine-readable evidence is persisted in:

`integration/animo-prep/PREP10_STABLE_DOM_PLOUGH_ACCUMULATOR_AUDIT.json`

## What is not yet qualified

This source/input qualification does not yet quantify numerical consequences. In particular it does not prove:

- the value observed for an undefined local under the historical Intel build;
- whether a GNU diagnostic build happens to zero, preserve or otherwise expose the local storage;
- the magnitude of any stable DOM/DON/DOP redistribution difference;
- downstream balance effects;
- agreement or disagreement with a provenance-qualified historical reference executable.

The next meaningful gate is an observer-only diagnostic on a working copy under an explicit compiler/build contract, followed by build-semantics sensitivity. Any actual initialization correction must remain a separate corrected-legacy candidate and cannot be applied to B0.

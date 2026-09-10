# ANIMO-B3B04E1 qualification resume checklist

This checklist is intentionally administrative and evidence-replay-only. It does not admit TCD-040 and does not authorize scientific scope expansion.

Current workunit status:

`FAIL_CLOSED_LOCAL_RECONSTRUCTION_PASS_CONTROLLED_B0_ACQUISITION_UNPROVEN`

TCD-040 status:

`UNRESOLVED_NOT_ADMITTED`

## Prerequisite

Do not resume the ordinary qualification gate until the canonical B0 evidence register records `PROVEN_CONTROLLED_IMMUTABLE` for all three required B0 artifacts:

1. `ANIMO-B0-SRC-41553-R53`
2. `ANIMO-B0-TB-202609`
3. `ANIMO-B0-DOC-UG40-2005`

For each artifact the record must contain a non-empty primary storage record ID, independent secondary storage record ID, immutability proof reference and custodian approval reference, with post-ingest SHA-256 verification, secondary-copy SHA-256 verification and restore testing all true.

Required content SHA-256 values are:

```text
source   183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566
testbank 44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84
guide    ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301
```

A local copy with the right digest is not sufficient proof of controlled immutable acquisition.

## Qualification execution

After the prerequisite is satisfied, acquire the three exact artifacts through the approved route and run from a clean checkout of the B3B04E1 candidate head:

```bash
python tools/b3b04e1/validate_b3b04e1.py \
  --source-zip /controlled/path/ANIMO_4.1.5.53.zip \
  --testbank-zip /controlled/path/ANIMO_testbank.zip \
  --guide-pdf /controlled/path/animo_user_guide_4_0.pdf \
  --require-git-scope
```

The ordinary gate must independently:

- verify all three whole-artifact hashes;
- verify the pinned relevant source-member hashes;
- regenerate the natural GrassPeat layer-0 witness;
- execute `tools/b3b04e1/replay_tcd040.py` from the acquired frozen source and testbank;
- reproduce the split-282 checkpoint SHA-256 `833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e`;
- reproduce the five raw little-endian binary64 checkpoint values;
- reproduce a 564-record exact Stage-A prefix at split 282;
- reproduce a complete 1800-record uninterrupted trajectory;
- reproduce full-trace exact equality for the corrected restore trajectory;
- reproduce first defective divergence at zero-based record 564, step 283, phase 0, layer 0, on exactly the five TCD-040 target coordinates while `Copo(0)` remains exact;
- reproduce the split-67 exact-zero checkpoint and full 1800-record negative-control equality;
- preserve the `INITIAL.OUT` formatted-restart versus raw qualification-checkpoint distinction;
- pass the scope guard relative to B3B04R.

No tolerance is permitted.

## Successful evidence-only closeout

Only after the ordinary validator returns success may the B3B04E1 status be changed to:

```text
QUALIFIED_EVIDENCE_REPLAYABILITY_ONLY
```

with decision:

```text
EVIDENCE_REPLAYABILITY_QUALIFIED
```

TCD-040 must still remain:

```text
UNRESOLVED_NOT_ADMITTED
```

Persist the exact immutable B3B04E1 head and the successful qualification workflow/run identity. Do not represent the earlier green blocked-state audit as the qualification run.

## Reconsideration handoff

Only after successful evidence-only closeout create a new clean branch for a genuinely independent second-line reconsideration. The reconsideration branch must start from the immutable evidence-qualified B3B04E1 head and must not reuse the B3B04R review branch as its working branch.

The reconsideration workunit must independently assess the evidence. B3B04E1 itself must not perform that review or pre-commit its outcome.

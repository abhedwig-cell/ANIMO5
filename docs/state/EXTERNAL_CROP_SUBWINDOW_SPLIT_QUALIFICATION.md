# ANIMO-STATEQ01 external-crop subwindow split qualification

Status: `EXECUTABLE_SPLIT_ROUTE_CONFIRMED_BEHAVIOURAL_EQUIVALENCE_FAILED`

Canonical STATE admission: `NOT_ADMITTED`

Canonical TIME admission: `NOT_ADMITTED`

Production migration: `NOT_ADMITTED`

## Purpose

The supplied testbank has no uncontaminated full-run `CORE_CNP_SUBSURFACE_ONLY` witness. The only full-run exact-zero-surface case, `RuurloGrass`, uses the internal ANIMO crop route and therefore cannot be treated as crop-free state evidence.

This qualification instead asks a narrower question for the separate profile `CORE_CNP_WITH_EXTERNAL_CROP`: does a supplied external-crop case contain a profile-clean exact-zero-surface subwindow from which a real revision-53 uninterrupted-versus-restart execution can be attempted without changing physics or external forcing payloads?

This work does not promote external crop to canonical ownership, does not repair legacy restart behaviour and does not make `INITIAL.OUT` a canonical checkpoint.

## Frozen evidence identities

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The scan uses the PREP01 deterministic GNU diagnostic build contract and adds read-only surface and management observers in an execution copy. Evidence remains `DIAGNOSTIC_NOT_REFERENCE` / non-B2.

## Reproducible external-crop window scan

`tools/stateq01/external_crop_window_scan.py` rebuilds the hash-pinned diagnostic executable, prepares the supplied cases without changing scientific input values, executes the three successful external-crop cases and searches for exact-zero-surface checkpoint candidates.

No epsilon is used. A candidate must satisfy the strict restricted-state surface condition exactly and must also satisfy the source `Stlen` external-crop start contract used by revision 53.

Observed coverage:

| Case | Surface records | Exact-zero records | Management events | External-crop-start-compatible candidates |
| --- | ---: | ---: | ---: | ---: |
| `GrassPeat` | 540 | 438 | 366 | 37 |
| `LWKM_gras_1040.2021.2045` | 900 | 898 | 600 | 89 |
| `STONE_akk_0006.2001.2015` | 540 | 492 | 271 | 88 |

The earlier provisional `Tito=4424` candidate is not retained. Once the actual external-crop reader start contract is included, that boundary is not a valid exact restart start.

The deterministic selected candidate is:

- case: `LWKM_gras_1040.2021.2045`;
- accepted checkpoint coordinate: legacy `Tito=4403`;
- accepted interval end date: `2033-01-20`;
- restart start date: `2033-01-21`;
- previous accepted coordinate: `4393`;
- next uninterrupted coordinate: `4414`;
- next step length: `11 d`;
- surface storage at previous, current and next observed boundaries: exactly zero;
- no management event on the previous, current or next boundary;
- external-crop start contract: compatible.

Machine-readable scan evidence is in `integration/animo-state/EXTERNAL_CROP_WINDOW_SCAN.json`.

## Qualification-only restart-tail adapter

`tools/stateq01/prepare_external_crop_restart_tail.py` constructs the legacy input tail needed to resume from the accepted boundary. It is an adapter over a prepared diagnostic case copy, not a model implementation.

For the selected split it:

- binds the Stage-A checkpoint as the restart input;
- changes the runtime start date to `2033-01-21`;
- retains and rebases the remaining management schedule, beginning with original `>add289`;
- retains 13 management periods and 312 addition blocks;
- slices annual boundary-condition vectors from the original 2021-2045 horizon to the remaining 2033-2045 horizon;
- leaves the hydrology payload unchanged;
- leaves the external-crop payload unchanged.

The reproduced tail has:

- checkpoint/restart SHA-256: `f27ae73d68db6323359dd4c6e7ecfae545c4972eff480cd4d216ef1f18506d50`;
- management SHA-256: `1c7f62432ad849c0788c18765705a31abb1d65b5d9015b99df8528212ec89934`;
- boundary SHA-256: `f8c298faa386109e82f354060807e0a5bbd220fb361e046c2843cce9d38b61e3`.

The generated management and boundary files are byte-identical to those used in the completed Stage-B execution. The manifest is stored in `integration/animo-state/EXTERNAL_CROP_RESTART_TAIL_MANIFEST.json`.

## Real revision-53 split execution

### Stage A

A qualification-only execution-copy stop was inserted after physical interval processing at exact `Tito=4403`. Revision 53 reached successful completion and wrote its normal legacy final restart output.

Checkpoint:

`f27ae73d68db6323359dd4c6e7ecfae545c4972eff480cd4d216ef1f18506d50`

Stage-A executable:

`3606db8c7d425dddba588a75c4022a40c4188147e0016e147111e6c3267a47ef`

This use of legacy output is diagnostic only. It is not a declaration that `INITIAL.OUT` is a canonical checkpoint or observationally pure serializer.

### Stage B

The prepared restart tail resumes on `2033-01-21`. Revision 53 runs through the remaining horizon to 2045 and reports successful completion.

Stage-B final restart-output SHA-256:

`69960ca466d40df8e1ff7bda1cadae175f31982796856547c13e67d36a731b86`

Stage-B observed post-restart records:

- surface/hydrology boundaries: 466;
- management events: 312.

## Comparison with uninterrupted execution

### Management continuation

The uninterrupted and restarted trajectories each contain 312 post-split management events. After the expected local time-origin shift, all 312 observed management records match exactly, including the observed event timing/continuation fields. Mismatch count: zero.

This is strong behavioural evidence for the exercised management-tail/cursor reconstruction, but it does not by itself admit the generic management contract or canonical TIME.

### First post-restart hydrology/surface boundary

The surface comparison contains exactly one mismatch across 466 compared post-split records. It occurs at the first restarted boundary.

Uninterrupted at legacy `Tito=4414`:

```text
Pn   = 0.0 m
Snla = 0.0 m
Pnt  = 0.0 m
Snt  = 0.0 m
St   = 11 d
Flpn = 0
```

Restarted at corresponding local `Tito=11`:

```text
Pn   = 5.0e-5 m
Snla = 0.0 m
Pnt  = 0.0 m
Snt  = 0.0 m
St   = 11 d
Flpn = 0
```

The remaining 465 surface records match exactly after the time-origin shift.

The positive `5.0e-5 m` ponding value cannot be accepted under `CORE_CNP_WITH_EXTERNAL_CROP`, because that profile inherits the strict exact-zero-surface guard from `CORE_CNP_SUBSURFACE_ONLY`. No tolerance is introduced to hide it.

The current evidence therefore identifies a concrete first-post-restart hydrology/frame-positioning seam. It does not yet prove the precise root cause inside the hydrology reader or t0/t1 binding.

### Final persistent-state comparison

The uninterrupted and restarted final legacy restart outputs are not byte-identical.

Uninterrupted final SHA-256:

`c56ec44bcfcefcc36962d6b543009b684d7b722e99afe73add43f53185026018`

Restarted final SHA-256:

`69960ca466d40df8e1ff7bda1cadae175f31982796856547c13e67d36a731b86`

Six parsed state labels contain numeric differences: `ammoni`, `humorg`, `inipho`, `nitrat`, `orgfsh` and `orgsol`. The largest observed absolute difference is approximately `1.0e-5` in `orgfsh`.

It is not justified to attribute all final-state differences to the first surface-frame mismatch. Legacy `Output_Init` formatting and restart/initialization precision remain independent candidate contributors, including observed P initialization consistency warnings. Those effects must be isolated separately.

## Qualification result

The external-crop route is no longer merely hypothetical. A real revision-53 split can be constructed, both stages execute successfully, management continuation is exact in the exercised run and almost the entire post-restart surface sequence reproduces exactly.

The behavioural equivalence gate still fails because:

1. the first post-restart surface frame has `Pn=5.0e-5 m` instead of exact zero;
2. the final persistent state diverges in six parsed blocks;
3. the causal contribution of frame rebinding versus serializer/restore precision is not yet separated.

Therefore:

`CORE_CNP_WITH_EXTERNAL_CROP = EXECUTABLE_SPLIT_ROUTE_CONFIRMED_BEHAVIOURAL_EQUIVALENCE_FAILED`

`canonical STATE = NOT_ADMITTED`

`canonical TIME = NOT_ADMITTED`

`production migration = NOT_ADMITTED`

This result does not change RC-R1 for `CORE_CNP_SUBSURFACE_ONLY`. The supplied testbank still lacks a clean crop-free full-run witness.

## Next qualification steps

1. Isolate the first post-restart hydrology t0/t1/frame positioning and explain the exact `5.0e-5 m` `Pn` discontinuity.
2. Independently isolate `Output_Init` formatting and restart/initialization precision effects on the final-state divergence.
3. Repeat the same split only after both seams have explicit qualification contracts. Do not promote this diagnostic run to STATE admission.

Machine-readable split result:

`integration/animo-state/EXTERNAL_CROP_SPLIT_RUN_RESULT.json`

# ANIMO-PREP04 — Stable-DOM phosphorus partition cross-species defect

Status: `CONFIRMED_SOURCE_AND_DIAGNOSTIC_BEHAVIOUR_DEFECT_NOT_REFERENCE_ADMITTED`.

## Work-unit contract

Purpose: investigate a source-level species mismatch found in `resp_miner.for`, determine whether the affected branch is reachable in the supplied testbank, and measure the effect of the smallest causal correction.

Affected components: stable dissolved organic matter transformation, net phosphorus mineralisation, phosphorus balance diagnostics and potentially subsequent mineral-P state through `Rekopo`.

Physics change in frozen source: no. The supplied source archive remains unchanged.

Numerical-policy change: no.

Diagnostic candidate change: two temporary execution-copy expressions only.

Reference qualification: unchanged. All results below remain `DIAGNOSTIC_NOT_REFERENCE` until PREP02 obtains an independent native reference.

## Frozen identity

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The diagnostic builds use the existing PREP02 GNU runtime contract: eight-byte default `REAL`, eight-byte `DOUBLE PRECISION`, static local storage, source-bound compatibility adaptations and the explicit testcase adapter.

## Source finding

`Resp_miner` solves several stable-DOM/humus rate combinations through `icase=1..8`.

For `Case(2)`, described in the source as:

`no decay of humus pool; transfer from SDO to HU pool`

the carbon and nitrogen transformation bookkeeping partitions their own stable-DOM decay terms:

```fortran
Transfom(17,Ln) = ... AvcoStdiorma(Ln) ...
Transfom(19,Ln) = (1.0-AsfaSDO) * Transfom(17,Ln)
Transfom(20,Ln) = AsfaSDO       * Transfom(17,Ln)

Transfon(17,Ln) = ... AvcoStdiorni(Ln) ...
Transfon(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfon(20,Ln) = AsfaSDO       * Transfon(17,Ln)
```

The phosphorus block first calculates the P-specific decay term correctly:

```fortran
Transfop(17,Ln) = ... AvcoStdiorpo(Ln) ...
```

but then partitions the **nitrogen** term:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO       * Transfon(17,Ln)
```

The analogous phosphorus expressions in the other active stable-DOM cases use `Transfop(17,Ln)` rather than `Transfon(17,Ln)`.

This is therefore not merely a naming anomaly. It injects a nitrogen transformation quantity into the phosphorus transformation ledger.

## Why it is process-relevant rather than reporting-only

`Transfop(19,Ln)` and `Transfop(20,Ln)` are used inside `Resp_miner` to calculate:

- released P;
- immobilised P;
- `Tomnpo`, the net P mineralisation amount.

After the layer loop the routine sets:

```fortran
Rekopo(Ln) = Tomnpo(Ln) / St / He(Ln)
```

so the mismatch can alter the zero-order phosphorus source/sink passed into later P transport/sorption calculations. `Outbal_calc` also consumes `Transfop(19/20)` directly.

For that reason this defect must **not** be classified as a Class-A ledger-only correction even though the observed supplied-case effect is very small.

## Reachability

The branch is selected when:

```text
Recfhu    < 1e-12
RecfHUSDO < 1e-12
recfSDO  >= 1e-12
```

A temporary observer-only execution-copy probe was run over the eight PREP02-compatible supplied cases.

`icase=2` is reached in several cases at very low effective transformation rates, but the erroneous phosphorus expressions execute only when `Ipo=1`.

The supplied `Puitmijn_Cranendonck_60` case has phosphorus active and reaches the affected path.

For the actual, non-potential `Resp_miner` pass:

```text
P-active Case(2) events: 9658
layers observed:          17..23
Recfhu range:             8.33707622733057e-15 .. 9.996862028415146e-13 d-1
recfSDO range:            1.0004491472796685e-12 .. 1.1996234434098174e-10 d-1
recfSDO / Recfhu:         120
```

The path is therefore source-reachable and behaviourally exercised, not dead code.

## Causal correction probe

Only the two execution-copy expressions were changed:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)
Transfop(20,Ln) = AsfaSDO       * Transfop(17,Ln)
```

No frozen source, testcase, hydrology input, parameter or other equation was changed.

Diagnostic corrected executable SHA-256:

`5eb45508c53883057e5572c89e63ab8565cae1255fdfcbc8852b9a91ac4a2234`

Observer baseline executable SHA-256:

`8d72ed3606aae9247944bd6e6ee6bd13c02b056b9e4c27143b50e41c6c09aae1`

Observer corrected executable SHA-256:

`a134f66a30a8a5ad5be9e78de0195e2e4f0716f5fa301d8f86cb2057a87f5c72`

## Local conservation identity

For an SDO-to-humus partition, the two P branches must partition the P-specific stable-DOM decay amount:

```text
Transfop(19) + Transfop(20) = Transfop(17)
```

In the frozen source's affected branch, the left-hand side instead sums to `Transfon(17)`.

Across the 9658 actual P-active Case(2) events in `Puitmijn_Cranendonck_60`, the accumulated mismatch is:

```text
1.0806894643265774e-11 kg m-2 P
= 1.0806894643265774e-7 kg ha-1 P
```

The largest single-event mismatch is:

`1.0228664519933875e-14 kg m-2 P`

The small magnitude is explained by the branch being entered only when effective rates are near the hard `1e-12` selection threshold. Small magnitude does not make the cross-species algebra correct.

## Whole-case balance effect

For `Puitmijn_Cranendonck_60`:

### `bapoLO.Out`

Frozen diagnostic run:

```text
maximum absolute annual BAPODV: 1.40e-8 kg/ha P
final cumulative BAPODVCU:     -1.08e-7 kg/ha P
```

Corrected execution-copy probe:

```text
maximum absolute annual BAPODV: 5.59e-12 kg/ha P
final cumulative BAPODVCU:      2.31e-11 kg/ha P
```

The baseline cumulative organic-P residual therefore matches the independently accumulated local cross-species mismatch to the displayed precision and collapses after the two-line correction.

### `bapoTP.Out`

Frozen diagnostic run:

```text
maximum absolute annual BAPODV: 1.36e-8 kg/ha P
final cumulative BAPODVCU:     -1.05e-7 kg/ha P
```

Corrected execution-copy probe:

```text
maximum absolute annual BAPODV: 1.36e-9 kg/ha P
final cumulative BAPODVCU:      2.74e-9 kg/ha P
```

The remaining TP residual is not attributed to this defect.

## State/process sensitivity

An observer-only comparison confirms that the correction changes `Tomnpo` and therefore the derived `Rekopo` in the affected low-rate events.

Maximum observed absolute differences:

```text
Tomnpo:  1.0228664519933892e-14 kg m-2 per step
Rekopo:  9.327856586446364e-15 kg m-3 d-1
```

The ordinary legacy non-balance outputs of `Puitmijn_Cranendonck_60` remain unchanged at their formatted output precision after normalizing only volatile timestamps/elapsed time. The normalized scientific differences are confined to:

- `bapoLO.Out`;
- `bapoTP.Out`;
- `ani_pLO.Bal`;
- `ani_pTP.Bal`;
- `message.out`, where tiny P-immobilisation diagnostic values change.

Across the other seven PREP02-compatible supplied cases, the two-line correction produces no normalized output differences.

This does **not** prove bitwise state equivalence. The observer demonstrates a real, though tiny in this testbank, P source-term change.

## Classification

Proposed discrepancy classification:

`CONFIRMED_LEGACY_CROSS_SPECIES_ALGEBRA_DEFECT_LOW_RATE_STATE_COUPLING`

Corrected-legacy class:

**Class B**, local algebraic conservation/species correction.

It is not Class A because `Tomnpo` and `Rekopo` can change. It does not require a new state representation like TCD-016.

## Admission rule

Do not patch the frozen source or admit this correction to ANIMO5 yet.

A later corrected-legacy admission must:

1. reproduce the affected branch under a qualified frozen reference;
2. preserve the exact source event and original output as defect evidence;
3. prove the P partition identity locally;
4. compare unrounded P state/source trajectories around affected events;
5. test configurations in which Case(2) is active at larger P mass or different N:P ratios, rather than relying only on the very-low-rate supplied case;
6. run the full corrected-reference qualification suite after composition with other P corrections.

## Gate

`CONFIRMED_TCD023_DIAGNOSTIC_CAUSALITY_CORRECTION_NOT_REFERENCE_ADMITTED`

Production migration remains `NOT_ADMITTED`.
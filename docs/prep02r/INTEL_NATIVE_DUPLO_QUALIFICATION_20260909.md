# ANIMO-PREP02R — Intel-native duplo execution qualification, 2026-09-09

Status: `CURRENT_INTEL_NATIVE_REPEAT_DETERMINISTIC_SEVEN_CASE_EXECUTION_CAPTURED_REFERENCE_NOT_QUALIFIED`

## Purpose

Qualify the first behavioural evidence from the supplied `animo41.exe` against two independently extracted copies of the frozen ANIMO testbank.

This is native execution evidence. It is **not** historical B2 admission and it does not establish that the supplied 2026 executable was built from the exact frozen revision-53 source bytes.

## Frozen identities

- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- executable SHA-256: `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`
- received run-1 ZIP SHA-256: `be67f35845c016e8d16db087f3ae8704d9bf6551d7539fef0ab03abba04aebf2`
- received run-2 ZIP SHA-256: `29ca595dd5551aa89e99c6deac2ee2e97f0a8aab40e08ad62915a92df355814e`

Both runs were created independently from the frozen ZIP and invoked each testcase directly as:

`..\animo41.exe animo.ini`

## Native repeat determinism

The two ZIPs contain the same 492 non-directory relative paths after removing only the outer `run1`/`run2` directory name.

Across the complete paired file set:

- 413 files are raw byte-identical;
- 79 differ in raw bytes because the run identity/timestamps are recorded.

Within the complete `ANIMO_testbank` tree, including the received executable and all original/generated testcase files:

- 464 paired files are present;
- 395 are raw byte-identical;
- 69 contain raw differences;
- after normalizing only five explicitly declared ANIMO runtime metadata surfaces, all 464 are equal.

The five metadata surfaces are:

1. `ANIMO40-run started on:` timestamp;
2. `File created on ...` timestamp;
3. `ANIMO run start:` timestamp;
4. `ANIMO run End:` timestamp;
5. `Elapsed:` runtime line.

No scientific value was normalized. No numerical tolerance was used. The normalized model-tree content-set SHA-256 is identical for both runs:

`1afed5769d5ee794cf7a4b585cac6a7f66135dcece97a9547e868286d6b83945`

All captured testcase stdout and stderr files are themselves raw byte-identical between run 1 and run 2. Administrative `RUN_INFO` and summary files differ in their declared run number and timestamps as intended.

Therefore the supplied Intel-native executable is repeat-deterministic for the entire attempted frozen suite, including its two deterministic failure modes.

## Case outcomes

| Case | Run 1 | Run 2 | Classification |
| --- | ---: | ---: | --- |
| CranGrass | 100 | 100 | successful completion |
| CranMais | 100 | 100 | successful completion |
| GHGMais | 1995 | 1995 | known GHG input-contract failure |
| GrassPeat | 100 | 100 | successful completion |
| LWKM_gras_1040.2021.2045 | 100 | 100 | successful completion |
| Puitmijn_Cranendonck_60 | 100 | 100 | successful completion |
| RuurloGrass | 1410 | 1410 | deterministic detailed-hydrology upper-boundary failure |
| STONE_akk_0006.2001.2015 | 100 | 100 | successful completion |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | 100 | 100 | successful completion |

`STOP 100` is the frozen-source success termination: it occurs immediately after `Successful completion of simulation`. Therefore exit code 100 must not be interpreted as a failed process in this legacy program.

### GHGMais

Both native runs stop identically with error 1995 because `>outGHG:` is absent from `Input\general.inp`. This is consistent with the already known revision-53/testcase input-contract mismatch. It remains separately classified and is not promoted into the ordinary compatible-case set.

### RuurloGrass

Both native runs stop on the first day with error 1410:

`subr. HYDRO: error in calculation of FLAB(0)`

and the same top-boundary deviation:

`0.002400241 m/d`

This is a material new comparison result because the deterministic GNU B1 build from the frozen source completes the same Ruurlo case successfully.

The frozen `Hydro_detailed.for` contains a directly relevant runtime-state hazard. Its runoff dispatch assigns `Runinu` for negative runoff and for the positive-runoff branch, but the near-zero runoff branch assigns only `Rupr`, `Rurv` and `Ruso` and leaves `Runinu` untouched. `Runinu` is then consumed by the detailed-hydrology top-boundary equations including the `Topdif` calculation.

This is a strong source-bound causal hypothesis for a compiler/storage-state-sensitive discrepancy. It is **not yet proven** to be the Intel failure root cause because the internal Intel value of `Runinu` was not observed. The finding should enter B3I02 as a runtime/state discrepancy rather than being assigned a scientific TCD from PREP02R.

## Intel versus GNU B1 — ordinary output

For the seven cases that complete under the supplied Intel executable, the ordinary generated output surface is compatible with the existing GNU B1 comparison route. The comparison is not globally exact: some formatted numerical outputs differ at the last printed digits, so this current Intel build cannot simply replace the frozen GNU diagnostic execution as an exact reference.

This is unsurprising but important. The supplied executable is a 2026 Intel Debug build with unresolved exact source-byte provenance; compiler/runtime and potentially source-revision differences remain live explanations.

No global tolerance is introduced to hide these differences. They require claim-scoped classification if used for B2.

## TCD-015 / LWKM result

The native LWKM case is particularly useful for B3B01.

At the ordinary formatted-output level, the Intel executable reproduces the GNU B1 legacy nitrate symptom on the relevant path. After only timestamp and cross-platform line-ending normalization where applicable:

- `nitrate.out` matches;
- `ammonium.out` matches;
- `miner-N.out` matches;
- `baniGP.Out`, `baniRP.Out` and `baniTP.Out` match;
- `initial.out` matches;
- the relevant transport warning content in `message.out` matches. The only observed message-format distinction around ordinary missing-label notices is Windows `\` versus GNU `/` path separation.

The three legacy nitrate transport mass-balance warnings occur at the same formatted events and values:

- TITO 2312, layer 1: `BAPD=-0.000843`, `BATR=-0.000901`;
- TITO 3042, layer 3: `BAPD=-0.000150`, `BATR=-0.000132`;
- TITO 4513, layer 2: `BAPD=-0.000598`, `BATR=-0.000558`.

The 1997 `baniGP.Out` annual line also matches the GNU B1 formatted residual exactly:

`5.76E-01 kg/ha`

with formatted cumulative residual `6.71E-01`.

This is strong native behavioural support that the received Intel executable exhibits the same ordinary TCD-015 legacy symptom.

It is still **not sufficient for B2** under the B3Q01 Class-B route. Ordinary output is rounded. The required unrounded affected nitrate state/flux comparison has not been captured, and the exact second negative-concentration clipping-branch activation has not been observed from inside this native binary. SYNQ01 remains synthetic evidence and cannot fill that B2 role.

## Admission consequence

PREP02R improves from “no native artifact/run” to a materially stronger state:

`CURRENT_INTEL_NATIVE_REPEAT_DETERMINISTIC_SEVEN_CASE_EXECUTION_CAPTURED_REFERENCE_NOT_QUALIFIED`

But reference admission remains fail-closed because all of the following remain true:

- the executable is a 2026 build rather than an untouched historical binary;
- exact source-byte-to-binary provenance is not independently established;
- Ruurlo exposes a material Intel-versus-GNU runtime discrepancy;
- TCD-015 lacks the unrounded native affected-state/flux observation required for normal B2;
- no global numerical tolerance is admitted;
- independent second-line review remains separately required for B3B01.

The new native evidence should therefore strengthen, not bypass, PREP02R and B3Q01 governance.
# ANIMO-PREP08 — Management transfer causal probes

Status: `QUALIFIED_DIAGNOSTIC_CAUSALITY_REFERENCE_ADMISSION_BLOCKED`.

## Purpose

PREP07 identified two management-transfer seams that required dynamic qualification evidence rather than additional static inference:

- TCD-028, exudate-humus ploughing ledger double count;
- TCD-029, multi-site fast phosphorus sorption during additions/ploughing.

PREP08 uses controlled diagnostic execution copies only. The frozen source archive and frozen supplied testbank remain unchanged. These synthetic probes are not golden cases and are not native-reference evidence.

## Frozen and diagnostic identity

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The baseline GNU diagnostic executable was rebuilt before the probes and reproduced the PREP01 hash exactly:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

The existing PREP02 runtime compatibility contract was used unchanged.

## 1. TCD-028 dynamic isolation

### Synthetic activation

The supplied LWKM case has zero initial `Huex`, so it does not naturally exercise the exudate-humus redistribution defect.

A temporary execution copy was created in which only the initial `>humexu:` row was changed. The first four soil compartments were assigned:

```text
0.01 0.02 0.03 0.04 kg m-2
```

and all remaining compartments were left at zero. Hydrology, management timing, material definitions and all other initial states were unchanged.

Modified execution-copy `initial.inp` SHA-256:

`d62c6455e3b3eb3c0bc700bb55dfa4c6f1d51922c2b6ae2093fdc6131337db54`

### Diagnostic source variants

Three executables were compared.

1. Frozen diagnostic source behaviour:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

2. Duplicate-only diagnostic correction. Exactly the second new-state addition was removed from `Addit.for`:

```fortran
Adhuexpl(I,Ln) = Adhuexpl(I,Ln) + Huex(Ln)
...
! second duplicate Adhuexpl += Huex removed
```

Executable SHA-256:

`2690e2d60f1000cece8ec636c9e3c24c92a730010784230724f275bafe2e9f14`

3. The same duplicate correction plus use of `Adhuexnipl` and `Adhuexpopl` instead of reconstructing N and P from `Adhuexpl` in `Outbal_calc`.

Executable SHA-256:

`239a6ba0f28d4a61b32829d691b21570be45bc6770718832c8565d7e0f02c0fc`

### Humus/organic-matter balance result

With the frozen source, all RP/GP/TP balance profiles show a maximum absolute annual humus residual of:

`942 kg ha-1 organic matter`

and final cumulative humus residual:

`3580 kg ha-1 organic matter`.

Removing only the duplicate `Adhuexpl` addition reduces the maximum absolute humus residuals to:

- RP: `1.16e-10 kg ha-1`;
- GP: `1.46e-10 kg ha-1`;
- TP: `6.98e-10 kg ha-1`.

The final cumulative humus residuals are then of order `1e-10 kg ha-1`.

This is direct dynamic causal evidence that the duplicate generic exudate-humus redistribution amount is a ledger defect.

### Organic-N result

Frozen synthetic execution:

- maximum absolute annual `BANODV`: `45.2 kg ha-1 N` in RP, GP and TP;
- final cumulative `BANODVCU`: `172 kg ha-1 N`.

Duplicate-only correction:

- RP maximum: `2.31e-9 kg ha-1 N`;
- GP maximum: `3.83e-7 kg ha-1 N`;
- TP maximum: `5.99e-6 kg ha-1 N`;
- final cumulative values remain near numerical noise.

Thus the duplicated generic carrier is also sufficient to explain the large activated organic-N ledger error in this configuration.

### Organic-P result and interaction with TCD-017

Frozen synthetic execution:

- maximum absolute annual `BAPODV`: `5.7 kg ha-1 P`;
- final cumulative `BAPODVCU`: `21.6 kg ha-1 P`.

Duplicate-only correction reduces this to:

- maximum absolute annual `BAPODV`: `0.0494 kg ha-1 P`;
- final cumulative `BAPODVCU`: `0.154 kg ha-1 P`.

The remaining characteristic `0.0494/0.154` P residual belongs to the independently established TCD-017 ploughing-ledger family and is not attributed to TCD-028.

### Species-reconstruction refinement

After the duplicate was removed, replacing the N and P consumers with the explicit `Adhuexnipl` and `Adhuexpopl` arrays produced **zero normalized differences across all 55 compared output files** in this activated configuration.

This matters for classification. PREP07 correctly identified a structural coupling in which N/P are reconstructed from a generic carrier even though explicit element-valued transfer arrays exist, but PREP08 does **not** establish an additional independent N/P defect beyond the duplicate for this configuration. The independent P-specific redistribution defects remain governed by TCD-017.

Therefore TCD-028 should be interpreted narrowly as a dynamically confirmed duplicate ledger update, while generic-versus-explicit element transfer consumption remains an architectural constraint and separate qualification concern rather than a newly demonstrated independent error here.

### Output-surface comparison

After normalization of only declared volatile timestamps and elapsed time, frozen versus duplicate-fixed execution changes 27 files. Every changed file belongs to the OM/N/P balance or detailed transformation-reporting families.

Ordinary non-balance output surfaces are unchanged at formatted precision.

Duplicate-only versus duplicate-plus-explicit-N/P execution has `55/55` normalized output equality.

## 2. TCD-029 multi-site fast-sorption management probe

### Synthetic two-site activation

The supplied LWKM case was used as base because it has active P, real additions/ploughing and an already executable diagnostic path.

Only an execution copy was modified:

- `NCXFA: 1 -> 2`;
- second fast Langmuir parameter row added as:
  `0.0, 2.500e-6, 500.0, 0.0, 0.0`;
- a second initial fast-sorption site row was added under `>inipho:`;
- that second row was adjusted to the revision-53 `Fast` relation at the supplied initial `Copo` values sufficiently closely that the final probe reports zero `Given Amcxfa(2) does not comply with Copo` consistency warnings.

Modified execution-copy hashes:

- `chempar.inp`: `72cba1019cfddf164b3393187ffca94a11e57f7c739e1c3d2102dcb98af41cec`;
- `initial.inp`: `0fd579a28c9d062d2645cf37b17dc7d6700e80dd102ede1c559ed7ed86642675`.

The synthetic case remains `DIAGNOSTIC_NOT_REFERENCE`.

### Observer contract

An observer-only executable was built from the frozen diagnostic source. It does not alter state. For each P-active ploughing event it records:

```text
P_before = total solution + all fast-site + precipitated P collected by Addit
P_after  = total solution + all fast-site + precipitated P in the redistributed soil layers
```

This directly tests whether the management operation conserves the inorganic-P control volume.

Observer executable SHA-256:

`01e020735359774293a51d083d55cbe5d14ea0907594c16c04587acef69c4a49`

The observer produces `55/55` normalized output equality against the corresponding non-observer NCXFA=2 execution, confirming that it is observational only at the persisted output precision.

### Single-site control

The unmodified supplied `NCXFA=1` LWKM configuration contains four ploughing events using addition index 6 and a four-compartment ploughing zone.

The observed event-wise P-control-volume differences are only floating-point noise:

- 1997: `-2.53e-15 kg m-2`;
- 1998: `+2.12e-15 kg m-2`;
- 2007: `-8.12e-16 kg m-2`;
- 2008: `-4.16e-15 kg m-2`.

Total over the four events:

`-5.38e-11 kg ha-1 P`.

Thus the legacy single-site management path is internally conservative for this observer identity.

### Two-site result

With the synthetic `NCXFA=2` case, the same four management events create P mass inside `Addit`:

| year | before kg m-2 | after kg m-2 | created kg m-2 | created kg ha-1 |
| --- | ---: | ---: | ---: | ---: |
| 1997 | 2.2429516957 | 2.3152923707 | 0.0723406750 | 723.40675 |
| 1998 | 2.7131772925 | 2.8018581077 | 0.0886808152 | 886.80815 |
| 2007 | 5.7988707557 | 5.8875515709 | 0.0886808152 | 886.80815 |
| 2008 | 6.3608426989 | 6.4495235141 | 0.0886808152 | 886.80815 |

Total artificial creation over the four observed ploughing events:

`0.3383831206 kg m-2 = 3383.831206 kg ha-1 P`.

This is direct behavioural confirmation of the PREP07 source finding. The multi-site management route is not merely underdocumented: the observed implementation violates P conservation when `NCXFA>1` is activated.

The same full synthetic execution also emits 3021 `TRANSGEN` P mass-balance warnings above 5%. Those warnings demonstrate broader pathological behaviour of this synthetic multi-site route but PREP08 does not attribute all of them exclusively to the ploughing defect. The event-local before/after observer is the causal evidence for TCD-029.

### Why no correction is proposed yet

A correct repair cannot safely be expressed as a one-line ledger patch. `Addit` currently lacks the site-specific `Parcxfa` constitutive parameter contract used by `Transorp`, while its multi-site loops still write `Amcxfa(1,Ln)` and use single-site helpers `Ampoma/Socfpo`.

A production-quality correction therefore requires an explicit management-side site contract and must be qualified independently against a trusted 4.1.x reference or authoritative theory.

## 3. Classification decisions

### TCD-028

Refined classification:

`CONFIRMED_LEGACY_EXUDATE_HUMUS_PLOUGHING_LEDGER_DOUBLE_COUNT`

Corrected-legacy class:

`A_LEDGER_REPORTING_ONLY`

within the tested diagnostic scope. Reference admission remains blocked.

The source-visible generic-to-element reconstruction concern is not promoted to an additional independent defect by PREP08 because duplicate-only and explicit-N/P variants are normalized-identical in the activated case.

### TCD-029

Upgraded classification:

`CONFIRMED_LEGACY_MULTISITE_FAST_SORPTION_MANAGEMENT_MASS_CREATION_AND_INTERFACE_GAP`

Corrected-legacy class:

`PROCESS_STATE_AND_CONSTITUTIVE_SITE_CORRECTION`

This is not Class A because a repair changes sorbed P state and can alter subsequent P transport.

## 4. Architectural consequences for ANIMO5

PREP08 strengthens four migration rules:

1. management operations must satisfy local before/after conservation identities before their outputs enter a global ledger;
2. every constitutive site must retain explicit identity through initialization, transport and management, not only inside the transport solver;
3. internal transfer records should be element-specific and immutable enough that duplicate insertion is mechanically detectable;
4. option ranges exposed by the parser are not production-supported until cross-module path coverage proves that every participating process understands the option.

## Gate

`QUALIFIED_PREP08_DIAGNOSTIC_CAUSALITY_REFERENCE_ADMISSION_BLOCKED`

No frozen source is modified. No corrected-legacy production change is admitted. ANIMO5 production migration remains `NOT_ADMITTED`.

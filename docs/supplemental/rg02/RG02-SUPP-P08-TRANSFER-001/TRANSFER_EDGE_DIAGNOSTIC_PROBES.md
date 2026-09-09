# ANIMO-PREP08 — Transfer-edge diagnostic probes

Status: `QUALIFIED_DIAGNOSTIC_TRANSFER_CAUSALITY_REFERENCE_ADMISSION_BLOCKED`.

## Purpose

PREP07 identified two source-bound transfer seams:

- TCD-028, duplicate exudate-humus ploughing bookkeeping plus an element-specific reconstruction concern;
- TCD-029, a multi-site fast-P-sorption management path that is inconsistent with the revision-53 parser/transport contract.

PREP08 performs controlled `DIAGNOSTIC_NOT_REFERENCE` probes to separate those effects. It also tightens the exudate-humus element-transfer analysis and identifies one additional source sequencing gap.

No frozen source or supplied testcase is modified. All activation cases are temporary execution copies and must not become golden cases.

Frozen identities:

- source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- reproduced GNU diagnostic baseline executable SHA-256: `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

## 1. TCD-028: dynamic separation of the duplicate `Adhuexpl` term

### Activation

A diagnostic LWKM execution copy was used. Only the initial `>humexu:` row was changed, setting the first four `Huex` compartments to depth-varying non-zero values `0.01, 0.02, 0.03, 0.04 kg m-2`; the remainder stayed zero.

Activation input SHA-256:

`d62c6455e3b3eb3c0bc700bb55dfa4c6f1d51922c2b6ae2093fdc6131337db54`

Three executables were compared:

1. frozen diagnostic source behaviour;
2. `dupfix`: remove only the second `Adhuexpl = Adhuexpl + Huex` update in `Addit.for`;
3. `explicit_np`: the same duplicate removal plus replacement of the N/P consumer reconstructions in `Outbal_calc` by `Adhuexnipl` and `Adhuexpopl`.

Executable SHA-256 values:

- duplicate-only probe: `2690e2d60f1000cece8ec636c9e3c24c92a730010784230724f275bafe2e9f14`;
- duplicate plus explicit-N/P consumer probe: `239a6ba0f28d4a61b32829d691b21570be45bc6770718832c8565d7e0f02c0fc`.

### Result

The duplicate-only correction collapses the activated exudate-humus redistribution residual in organic matter and organic N by many orders of magnitude.

| ledger/profile | frozen maximum absolute period residual | duplicate-only maximum absolute period residual |
| --- | ---: | ---: |
| humus OM RP | `942 kg/ha` | `1.16e-10 kg/ha` |
| humus OM GP | `942 kg/ha` | `1.46e-10 kg/ha` |
| humus OM TP | `942 kg/ha` | `6.98e-10 kg/ha` |
| organic N RP | `45.2 kg/ha N` | `2.31e-9 kg/ha N` |
| organic N GP | `45.2 kg/ha N` | `3.83e-7 kg/ha N` |
| organic N TP | `45.2 kg/ha N` | `5.99e-6 kg/ha N` |
| organic P RP/GP/TP | `5.7 kg/ha P` | `0.0494 kg/ha P` |

The remaining `0.0494 kg/ha P` maximum and approximately `0.154 kg/ha P` final cumulative residual are the already separated TCD-017 organic-P ploughing ledger family; PREP08 does not reassign that residual to TCD-028.

The `dupfix` and `explicit_np` executions are identical after normalization of timestamp/elapsed-time fields. Therefore this activation does **not** independently demonstrate a behavioural defect in the N/P consumer reconstruction after the duplicate has been removed.

This refines TCD-028. The duplicate generic `Adhuexpl` addition is causally confirmed. The element-specific reconstruction concern remains an architectural/source seam but is not independently proven by this activation.

## 2. TCD-029: direct NCXFA=2 ploughing mass jump

### Activation

A second temporary LWKM copy was changed from `NCXFA=1` to `NCXFA=2`. A second unequal Langmuir fast-sorption site and a second initial fast-sorption row were inserted. The activation is intentionally diagnostic and is not claimed to represent a calibrated soil.

Modified input hashes:

- `chempar.inp`: `72cba1019cfddf164b3393187ffca94a11e57f7c739e1c3d2102dcb98af41cec`;
- `initial.inp`: `0fd579a28c9d062d2645cf37b17dc7d6700e80dd102ede1c559ed7ed86642675`.

An observer-only executable brackets each ploughing redistribution inside `Addit.for`. Before redistribution it sums the same inorganic-P control volume that the management code has already collected: aqueous P, all fast-sorption sites and precipitated P. After redistribution it sums the corresponding layer states. The observer does not alter model state.

Observer executable SHA-256:

`01e020735359774293a51d083d55cbe5d14ea0907594c16c04587acef69c4a49`.

### Control: supplied NCXFA=1 path

Four observed ploughing events close to floating-point noise:

| year | before kg m-2 P | after kg m-2 P | delta kg/ha P |
| --- | ---: | ---: | ---: |
| 1997 | `3.130045623101660e-2` | `3.130045623101407e-2` | `-2.53e-11` |
| 1998 | `3.047275287091624e-2` | `3.047275287091836e-2` | `+2.12e-11` |
| 2007 | `2.223884898508565e-2` | `2.223884898508484e-2` | `-8.12e-12` |
| 2008 | `2.156912009012787e-2` | `2.156912009012371e-2` | `-4.16e-11` |

### NCXFA=2 activation

The same observer detects immediate positive P creation across the management redistribution itself:

| year | before kg m-2 P | after kg m-2 P | delta kg/ha P |
| --- | ---: | ---: | ---: |
| 1997 | `2.242951695726745` | `2.315292370702143` | `+723.406750` |
| 1998 | `2.713177292462200` | `2.801858107679592` | `+886.808152` |
| 2007 | `5.798870755720791` | `5.887551570938182` | `+886.808152` |
| 2008 | `6.360842698865333` | `6.449523514082725` | `+886.808152` |

The sum over the four diagnostic events is `+3383.831206 kg/ha P`. This number is **not** a general model-error magnitude and must not become a tolerance. It is only evidence that the admitted `NCXFA>1` management path can create mass.

The source explains the event-local failure. `Addit.for` sums `Supocxfa(J)` over every site, but the redistribution branch writes only `Amcxfa(1,Ln)`. In the precipitation branch the loop over `J=1,Ncxfa` repeatedly assigns site 1 and repeatedly subtracts site 1 from `Ampopr`; site 2 is not reconstructed from its own constitutive parameters. `Addit` does not receive `Parcxfa`, so it cannot preserve the site-specific contract used by `Transorp`.

The full synthetic NCXFA=2 trajectory later emits many `TRANSGEN` mass-balance warnings. PREP08 therefore uses only the observer-bracketed instantaneous management event as causal evidence. No later synthetic trajectory is admitted as scientific reference evidence.

TCD-029 is upgraded from an unexercised source gap to:

`DIAGNOSTICALLY_CAUSAL_MULTISITE_FAST_SORPTION_MANAGEMENT_MASS_NONCONSERVATION`

Production support for `NCXFA>1` remains blocked until a trusted 4.1.x reference and a scientifically qualified two/three-site management case exist.

## 3. TCD-030: exudate-humus N/P fraction sequencing gap

PREP08 also tightens the source algebra around `Huex` during ploughing.

The physical organic-N and organic-P storage equations represent exudate-derived humus as:

```text
Huex * Nifrhu
Huex * Pofrhu
```

Before redistribution `Addit.for` subtracts the old element amounts using the old layer fractions:

```fortran
Adhuexnipl -= Huex * Nifrhu
Adhuexpopl -= Huex * Pofrhu
```

It then redistributes `Huex`, but adds the new N/P amounts **before** `Nifrhu` and `Pofrhu` are recomputed from redistributed `Huosni/Huos` and `Huospo/Huos`:

```fortran
Adhuexnipl += new_Huex * old_layer_Nifrhu
Adhuexpopl += new_Huex * old_layer_Pofrhu
...
Nifrhu = redistributed_Huosni / redistributed_Huos
Pofrhu = redistributed_Huospo / redistributed_Huos
```

The element-specific arrays therefore encode:

```text
new_Huex * old_fraction - old_Huex * old_fraction
```

while the actual post-event storage is evaluated using the newly redistributed fraction. The true state-storage difference is:

```text
new_Huex * new_fraction - old_Huex * old_fraction
```

The generic `Adhuexpl * new_fraction` reconstruction is not generally equivalent either, because it applies the new fraction to the old-loss term.

If the pre-event humus fractions happen to be uniform across the plough layer, both representations collapse to the same answer. That explains why the PREP08 activation above does not separate the two N/P consumer choices after duplicate removal. The source contract, however, does not require old `Nifrhu/Pofrhu` to be spatially uniform.

This is registered as a new source-confirmed, testbank-unexercised sequencing gap:

`TCD-030 SOURCE_CONFIRMED_EXUDATE_HUMUS_ELEMENT_FRACTION_REDISPATCH_SEQUENCING_GAP_TESTBANK_UNEXERCISED`

No correction is admitted. A future controlled probe must force non-uniform pre-plough humus N/P fractions and compare the exact pre/post `Huex*Nifrhu` and `Huex*Pofrhu` storage difference against the ledger terms.

## 4. Qualification consequences

PREP08 supports three decisions:

1. TCD-028 can be narrowed to a causally confirmed duplicate generic exudate-humus redistribution amount; the N/P consumer reconstruction is not independently causal in the current activation.
2. TCD-029 is behaviourally demonstrated at the management-event boundary under a synthetic `NCXFA=2` activation, while remaining `DIAGNOSTIC_NOT_REFERENCE`.
3. TCD-030 must be kept separate from TCD-028 because it concerns the ordering and ownership of element fractions during redistribution, not the duplicate generic amount.

For ANIMO5, a management transfer should therefore carry explicit pre-state and post-state element amounts, rather than a generic carrier mass plus a fraction that can be evaluated at the wrong side of the transaction.

## Gate

`QUALIFIED_DIAGNOSTIC_TRANSFER_CAUSALITY_TCD028_REFINED_TCD029_CONFIRMED_TCD030_SOURCE_BOUND_REFERENCE_ADMISSION_BLOCKED`

Corrected-legacy production changes and process migration remain `NOT_ADMITTED`.
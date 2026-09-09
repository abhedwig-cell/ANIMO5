# ANIMO-PREP10 — Restart-state continuity baseline

Status: `SOURCE_BOUND_AND_DIAGNOSTIC_CAUSAL_BASELINE_PERSISTED_REFERENCE_SPLIT_RUN_BLOCKED`.

This document inventories restart/state-continuity findings for frozen ANIMO 4.1.5 revision 53. It does not change frozen source or testcase bytes and does not qualify historical runtime behaviour.

## 1. Lifecycle contract

PREP10 evaluates persistent state against:

```text
INITIAL.INP read
-> accepted/start state
-> result/end state
-> Init accepted-step copy
-> Output_Init INITIAL.OUT write
-> subsequent INITIAL.INP read
```

A state is restart-complete only if scientifically required information survives this chain. Derived state may be omitted only when reconstruction from persisted state is explicit and lossless for the admitted option.

## 2. Core state families with direct structural symmetry

Revision 53 exposes matching read/write surfaces for the major matrix-state families:

- soil moisture through `>moistf:`;
- NH4 solution through `>ammoni:`;
- NO3 solution through `>nitrat:`;
- exudate organic matter through `>orgexu:`;
- humus from exudates through `>humexu:`;
- fresh-organic-matter fractions through `>orgfsh:`;
- humus organic matter through `>humorg:`;
- labile dissolved organic C/N through `>orgsol:`;
- stable dissolved organic C/N/P through `>sdomin:`;
- root/shoot and actual plant uptake through `>orgpla:`;
- P solution, sorption, precipitation and DOP through `>inipho:`;
- CH4 and N2O concentrations through `>methan:` and `>nitoxi:` when GHG is active.

This proves only source-level representation symmetry. It is not split-run reference qualification.

Some accepted/result quantities that are not serialized are explicit derived state. Examples include NH4 sorbed amount `Cxnh/Rscxnh`, reconstructed from NH4 concentration plus sorption parameters, and total P sorption sums reconstructed from serialized site states. PREP10 does not classify such deliberate derivations as restart omissions.

## 3. P restart canonicalization remains open

`Output_Init.for` always writes P restart state using `Inpo=1` and explicit final solution P, every configured fast/slow sorption site, precipitated P and DOP.

Input accepts `Inpo=1..3`. A trajectory started from another initialization mode is therefore canonicalized to explicit-state mode at restart output.

All supplied P-active cases already use `Inpo=1`, so the testbank does not exercise a 2/3-to-1 round trip. PREP10 does not classify canonicalization itself as a defect. A dedicated split-run test is still required before modes 2 or 3 can be admitted as restart-equivalent.

## 4. TCD-032 — macropore solute writer omission

When `IoptMp=1`, `mapoinput.for` actively reads persistent macropore solute concentrations from:

```text
>MPnitr:  CoMpNh(1:2), CoMpNi(1:2)
>MPorgs:  CoMpDiorMa(1:2), CoMpDiorNi(1:2)
>MPphos:  CoMpPo(1:2), CoMpDiorPo(1:2)   [when P active]
```

`Init.for` carries all six result-state families back to accepted state on later timesteps.

The corresponding writer block in `Output_Init.for` is entirely commented out. Thus the standard `INITIAL.OUT` cannot serialize state that the active reader expects.

Classification:

`SOURCE_CONFIRMED_PERSISTENT_MACROPORE_SOLUTE_RESTART_WRITER_OMISSION_TESTBANK_UNEXERCISED`.

All supplied macropore options are zero, so no behavioural split-run magnitude is claimed. This is distinct from TCD-025, which concerns the public/main macropore balance control volume.

## 5. TCD-033 — actual plant uptake restart direction defect

`input1.for` reads cumulative actual plant uptake as `Rsamplni_act` and optional `Rsamplpo_act` from `>orgpla:`.

`Inicalc.for` then contains, for the relevant plant modes:

```fortran
If(Rsamplni_act.Lt.1.0d-4) Amplni_act = 0.0
Rsamplni_act = Amplni_act
```

with analogous P code. For a nontrivial restart value there is no preceding `Amplni_act = Rsamplni_act`; the dataflow is in the opposite direction.

This is naturally exercised by the supplied testbank. Four unmodified initial files contain nonzero actual N/P uptake and the observer sees the accepted values become zero immediately after `Inicalc`:

- LWKM: N `0.0666813`, P `0.0088759` kg/m2;
- GrassPeat: N `0.0632935`, P `0.00675465` kg/m2;
- STONE: N `0.0195003`, P `0.00295112` kg/m2;
- Zuiderzeeland: N `0.0235216`, P `0.00322743` kg/m2.

A temporary minimal causal probe assigns actual accepted state from the restart value before the existing small-value filter. For LWKM the post-`Inicalc` values then equal the supplied restart values exactly.

The correction is not accounting-only: in the full LWKM diagnostic comparison 26 of 55 common generated outputs differ after declared volatile-metadata normalization. These differences are diagnostic evidence only, not an acceptance envelope.

Classification:

`CONFIRMED_LEGACY_PLANT_ACTUAL_UPTAKE_RESTART_INITIALIZATION_DIRECTION_DEFECT`.

## 6. TCD-034 — potential plant uptake missing from restart representation

The plant system carries persistent potential uptake state between ordinary timesteps for applicable plant modes:

```text
Amplni_pot <-> Rsamplni_pot
Amplpo_pot <-> Rsamplpo_pot
```

`Uptpar_Plant` uses potential-minus-actual uptake in later nutrient-demand logic, so this is scientifically active state rather than a reporting accumulator.

Nevertheless `>orgpla:` reads and writes only root/shoot state plus cumulative **actual** N/P uptake. No potential-uptake restart fields exist, and `Inicalc` resets accepted potential uptake to zero.

Natural supplied-case observer evidence shows nonzero state immediately before the restart writer:

- LWKM: N potential `0.06634733`, P potential `0.007806854` kg/m2;
- GrassPeat: N potential `0.06759374`, P potential `0.009396654` kg/m2;
- STONE: N potential `0.021070089005`, P potential `0.0028565385393` kg/m2.

For LWKM, `initial.out` contains the actual N/P values in `>orgpla:` but no representation of these nonzero potential states.

Classification:

`CONFIRMED_LEGACY_PLANT_POTENTIAL_UPTAKE_RESTART_STATE_OMISSION`.

A full continuous-versus-split behavioural magnitude is still unmeasured and must not be guessed.

## 7. Nearby but not promoted findings

### Macropore nitrate validation

In `mapoinput.for`, checks labelled `CoMpNi(1)` and `CoMpNi(2)` pass the ammonium variables `CoMpNh(1)` and `CoMpNh(2)` to `Checkrea`. Nitrate is read but ammonium is validated twice. This remains a separate unexercised parser-validation candidate and is not folded into TCD-032.

### GHG CO2-associated humus auxiliary

`Huos_CO2/Rshuos_CO2` is not directly serialized, but source reconstruction through `Frhu_CO2*Huos` exists. Because the only supplied GHG case has a source/testcase lineage mismatch, PREP10 does not promote this to a restart defect.

## 8. Current boundary

At this checkpoint:

- core matrix-state read/write mapping: `STRUCTURALLY_MAPPED_NOT_SPLIT_RUN_QUALIFIED`;
- P `Inpo -> 1` restart conversion: `CANONICALIZATION_REQUIRES_SPLIT_RUN_CHECK`;
- TCD-032: source-confirmed persistent macropore restart writer omission, testbank unexercised;
- TCD-033: confirmed actual plant uptake initialization-direction defect with natural multi-case reachability;
- TCD-034: confirmed potential plant uptake restart-state omission with natural nonzero writer-boundary evidence;
- GHG auxiliary reconstruction: unresolved because of lineage/reference blockers.

PREP02 historical reference qualification remains unavailable. None of the diagnostic probes qualifies corrected production behaviour.

Production migration remains `NOT_ADMITTED`.

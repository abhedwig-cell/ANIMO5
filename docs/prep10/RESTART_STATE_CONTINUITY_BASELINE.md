# ANIMO-PREP10 — Restart-state continuity baseline

Status: `SOURCE_BOUND_BASELINE_PERSISTED_CAUSAL_PROBES_PENDING`.

This document inventories the first restart/state-continuity findings for frozen ANIMO 4.1.5 revision 53. It does not change source or testcase bytes and does not qualify historical runtime behaviour.

## 1. Lifecycle contract

PREP10 evaluates persistent state against the chain:

```text
INITIAL.INP read
-> accepted/start state
-> result/end state
-> Init accepted-step copy
-> Output_Init INITIAL.OUT write
-> subsequent INITIAL.INP read
```

A state is restart-complete only if its scientifically required information survives this chain. Derived state may be intentionally omitted only when reconstruction from persisted state is explicit and lossless for the admitted model option.

## 2. Core state families with direct read/write symmetry

The revision-53 source exposes direct restart read/write surfaces for the following major families:

- soil moisture state through `>moistf:`;
- NH4 solution state through `>ammoni:`;
- NO3 solution state through `>nitrat:`;
- exudate organic matter through `>orgexu:`;
- humus from exudates through `>humexu:`;
- fresh-organic-matter fractions through `>orgfsh:`;
- humus organic matter through `>humorg:`;
- labile dissolved organic C/N through `>orgsol:`;
- stable dissolved organic C/N/P through `>sdomin:`;
- actual plant/root/shoot state through `>orgpla:`;
- phosphorus solution/fast-sorbed/slow-sorbed/precipitated/DOP state through `>inipho:`;
- CH4 and N2O system concentrations through `>methan:` and `>nitoxi:` when GHG is active.

This is structural symmetry only. It does not prove bit-identical split-run restart equivalence.

## 3. Phosphorus restart canonicalization

`Output_Init.for` always writes P restart state using:

```fortran
Inpo = 1
```

and then writes explicit final solution P, every configured fast-sorption site, every configured slow-sorption site, precipitated P and dissolved organic P.

Revision-53 input supports `Inpo=1..3`. Therefore a run started from another initialization mode is canonicalized to explicit-state mode in the emitted restart file.

PREP10 does not classify this as a defect by itself. It is acceptable only if the emitted explicit state contains all information needed to continue the same trajectory. Split-run equivalence remains to be tested.

## 4. Source-confirmed macropore restart writer omission

When `IoptMp=1`, `Mapoinput.for` with `Nupa=4` actively reads macropore initial concentrations from `INITIAL.INP`:

- `>MPnitr:`: `CoMpnh(1:2)`, `CoMpni(1:2)`;
- `>MPorgs:`: `CoMpDiorma(1:2)`, `CoMpDiorni(1:2)`;
- `>MPphos:` when P is active: `CoMpPo(1:2)`, `CoMpDiorpo(1:2)`.

`Init.for` confirms these are persistent accepted/result state pairs. On later timesteps it copies:

```text
RsCoMpDiorMa -> CoMpDiorMa
RsCoMpDiorNi -> CoMpDiorNi
RsCoMpNh     -> CoMpNh
RsCoMpNi     -> CoMpNi
RsCoMpDiorPo -> CoMpDiorPo
RsCoMpPo     -> CoMpPo
```

However, the corresponding macropore blocks in `Output_Init.for` are entirely commented out. The standard emitted `INITIAL.OUT` therefore has no active writer for these persistent macropore solute states.

This is a strong source-confirmed restart-continuity omission. It is not yet a behavioural magnitude claim because all supplied testcases have macropores disabled.

A nearby validation error is also visible in `Mapoinput.for`: the checks labelled `CoMpni(1)` and `CoMpni(2)` pass `CoMpnh(1)` and `CoMpnh(2)` to `Checkrea`, so nitrate values are read but ammonium is checked twice. PREP10 records this separately as an unexercised parser-validation candidate and does not yet assign it a discrepancy number.

## 5. Plant cumulative potential-uptake candidate

The plant system has persistent accepted/result quantities:

```text
Amplni_pot  <-> Rsamplni_pot
Amplpo_pot  <-> Rsamplpo_pot
```

`Init.for` carries these values between ordinary timesteps for plant modes that use them. `Uptpar_Plant.for` uses `Amplni_pot - Amplni_act` in later nutrient-demand logic, so potential uptake is not merely a report accumulator.

Yet `>orgpla:` reads/writes only:

```text
Rsamplro
Rsamplsh
Rsamplni_act
Rsamplpo_act   [when P is active]
```

No `Rsamplni_pot` or `Rsamplpo_pot` restart field exists on this interface, and `Inicalc.for` initializes `Amplni_pot` and `Amplpo_pot` to zero.

This is a **candidate restart information-loss seam**, not yet a confirmed defect. Its effect depends on crop mode, restart timing and whether the cumulative potential quantity can be reconstructed from other persisted state. PREP10 requires a nonzero causal restart probe before promotion.

## 6. Actual plant uptake initialization requires special scrutiny

`input1.for` reads `Rsamplni_act` and optional `Rsamplpo_act`. In `Inicalc.for` the initialization block contains:

```fortran
If(Rsamplni_act.Lt.1.0d-4) Amplni_act = 0.0
Rsamplni_act = Amplni_act
Amplni_pot = 0.0
```

with the analogous P code.

For a nonzero restart value above the threshold, this block does not visibly execute `Amplni_act = Rsamplni_act` before copying the opposite direction. Because legacy storage semantics matter, PREP10 will not infer the resulting runtime value from static inspection alone. A controlled nonzero restart probe is required.

## 7. GHG auxiliary continuity candidate

The GHG path contains `Huos_CO2`, `Rshuos_CO2` and `Frhu_CO2`. `Init.for` carries `Rshuos_CO2 -> Huos_CO2` between timesteps, while `ghgasses.for` derives/updates the CO2-associated humus fraction. No explicit restart field for this auxiliary state is emitted by `Output_Init`.

The source also contains reconstruction logic (`Huos_CO2 = Frhu_CO2 * Huos`), so omission from the restart file is not by itself proof of information loss. GHG restart continuity remains a source-bound candidate and is additionally blocked by the existing GHG source/testcase lineage problem.

## 8. Current classification boundary

At this checkpoint:

- core read/write symmetry: `STRUCTURALLY_MAPPED_NOT_SPLIT_RUN_QUALIFIED`;
- P `Inpo -> 1` restart conversion: `CANONICALIZATION_REQUIRES_SPLIT_RUN_CHECK`;
- macropore solute restart writer: `SOURCE_CONFIRMED_PERSISTENT_STATE_WRITER_OMISSION_TESTBANK_UNEXERCISED`;
- plant cumulative potential uptake: `CAUSAL_PROBE_REQUIRED`;
- nonzero actual plant uptake initialization: `CAUSAL_PROBE_REQUIRED`;
- GHG auxiliary CO2 humus state: `RECONSTRUCTION_SEMANTICS_UNRESOLVED`.

Production migration remains `NOT_ADMITTED`.

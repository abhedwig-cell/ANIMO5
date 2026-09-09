# ANIMO-PREP09 — Element-transfer sequencing and slow-sorption tillage audit

Status: `QUALIFIED_DIAGNOSTIC_TCD030_CAUSALITY_SLOW_SORPTION_POLICY_SEAM_REFERENCE_ADMISSION_BLOCKED`.

## Purpose

PREP09 resolves two open transfer-ledger questions from PREP08 without changing the frozen ANIMO 4.1.5 revision-53 source or supplied testcase bytes:

1. is the TCD-030 exudate-humus N/P transfer-array sequencing gap dynamically causal when element fractions change during ploughing;
2. what is the source, documented and behavioural status of the disabled slow non-equilibrium phosphorus-sorption redistribution code in `Addit.for`.

All modified executions in this workunit are `DIAGNOSTIC_NOT_REFERENCE`. No production correction is admitted.

## Frozen identity and reproduced diagnostic baseline

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- reproduced GNU diagnostic executable SHA-256: `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

The source-bound PREP09 audit passes `20/20` checks against these exact archive identities.

## 1. TCD-030 is dynamically causal

### Source identity

`Addit.for` first records the old exudate-humus element quantities:

```fortran
Adhuexnipl(I,Ln) = Adhuexnipl(I,Ln) - Huex(Ln)*Nifrhu(Ln)
Adhuexpopl(I,Ln) = Adhuexpopl(I,Ln) - Huex(Ln)*Pofrhu(Ln)
```

It then redistributes `Huex`, `Huos`, `Huosni` and `Huospo`. Before the humus element fractions are recomputed, however, the new exudate-humus transfer is added with the old layer fractions:

```fortran
Adhuexnipl(I,Ln) = Adhuexnipl(I,Ln) + Huex(Ln)*Nifrhu(Ln)
Adhuexpopl(I,Ln) = Adhuexpopl(I,Ln) + Huex(Ln)*Pofrhu(Ln)
...
Nifrhu(Ln) = Huosni(Ln) / Huos(Ln)
Pofrhu(Ln) = Huospo(Ln) / Huos(Ln)
```

For a conserved element transfer the exact internal-redistribution quantity must instead equal the physical post-state minus pre-state element amount:

```text
Delta N = new_Huex * new_N_fraction - old_Huex * old_N_fraction
Delta P = new_Huex * new_P_fraction - old_Huex * old_P_fraction
```

### Controlled activation probe

A diagnostic observer activated non-uniform `Huex`, `Nifrhu` and `Pofrhu` immediately before the first natural LWKM plough event. It changed no frozen input bytes and is not a supplied testcase. Probe executable SHA-256:

`1f8f0241ce7f292157245cb710e04b9eb79f504aca0d7b9d78b18f9a9fd2da4d`

At `Tito=2414`, `Pl=4`:

| quantity | N | P |
| --- | ---: | ---: |
| pre-plough exudate-humus store, kg m-2 | `4.0000000000000008e-2` | `4.0000000000000001e-3` |
| post-plough store, kg m-2 | `3.4309421243672103e-2` | `3.4309421243672112e-3` |
| exact physical change, kg m-2 | `-5.6905787563279048e-3` | `-5.690578756327889e-4` |
| legacy explicit transfer mismatch, kg m-2 | `+6.9057875632789947e-4` | `+6.9057875632788797e-5` |
| mismatch, kg ha-1 | `+6.9057875633` | `+0.6905787563` |

The following three plough events are at floating-point-zero mismatch after the first redistribution has homogenized the relevant fractions over the ploughed zone. That is a useful causal control: the discrepancy appears when the pre- and post-redistribution fractions differ and disappears when they no longer differ.

### Refined classification

TCD-030 is therefore refined to:

`DIAGNOSTICALLY_CAUSAL_EXUDATE_HUMUS_ELEMENT_TRANSFER_LEDGER_SEQUENCING_DEFECT`

The measured numbers are synthetic activation magnitudes, not natural-case error estimates or acceptance tolerances. The defect is in the explicit element-transfer ledger arrays. A minimal sequencing correction is expected to be accounting-only, but Class-A admission still requires qualified-reference equivalence and must be composed explicitly with TCD-017 and TCD-028.

## 2. Slow non-equilibrium P sorption is a revision-specific tillage policy seam

### What the supplied 4.0 guide supports

The supplied ANIMO 4.0 User's Guide describes `PL` as the number of model compartments to be ploughed, explicitly annotated as redistributed. The same guide defines `AMCXSL(NCXSL,NL)` as the adsorbed non-equilibrium phosphorus mass concentration, specified by non-equilibrium site and model compartment.

Those statements support treating `Amcxsl` as a spatial physical P state inside compartments. They do not, however, prove the exact intended revision-53 policy for whether that state must move during tillage.

### Revision-53 source state

`Addit.for` contains a complete-looking site-specific slow-sorption ploughing route, but each of its four stages is disabled with the dated source marker `!-19-10-2010`:

1. accumulation of `Amcxsl(J,Ln)*He(Ln)` into `Supocxsl(J)`;
2. subtraction from `Adpocxslpl`;
3. redistribution of `Amcxsl` over the ploughed depth;
4. addition to `Adpocxslpl`.

The commented redistribution loop itself reads `Do J = I,Ncxsl`, coupling the sorption-site loop start to management index `I`; a mechanically re-enabled implementation would therefore contain an additional site-index risk. PREP09 does not treat that commented statement as executable legacy behaviour.

The surrounding interface was not removed:

- `Init.for` still resets `Adpocxslpl` every timestep;
- `Outbal_calc.for` still actively consumes `Adpocxslpl(I,Ln,J)` in `Bapp(Redi,Ly)`.

This leaves an explicit producer-consumer seam whose producer is disabled while its reset and consumer surfaces remain live.

## 3. Natural LWKM activation exists

The supplied `LWKM_gras_1040.2021.2045` case has:

```text
OPTCXSL = 3  (Freundlich)
NCXSL   = 3
```

and four actual `Pl=4` events in the diagnostic execution. An observer-only executable, SHA-256

`9a1dbb018b66ad61676bccb68ab883a39eda68ae23f46fe01a14989c69b3933f`,

shows that all three slow-sorption sites contain non-zero and spatially heterogeneous `Amcxsl` values at every observed plough event. At the first event the areic totals over the four ploughed layers are:

| site | total kg m-2 P | min concentration kg m-3 | max concentration kg m-3 |
| ---: | ---: | ---: | ---: |
| 1 | `5.2826545565671668e-3` | `2.2191925953796602e-2` | `3.8709042802477715e-2` |
| 2 | `3.5673159976589597e-2` | `1.6316986989212745e-1` | `2.0939701434076491e-1` |
| 3 | `4.7716524066739791e-2` | `2.1218154643866530e-1` | `3.0056561869476833e-1` |

The disabled path is therefore not merely attached to an impossible or zero state in the supplied testbank.

## 4. Conservative redistribution sensitivity

A diagnostic sensitivity variant re-enabled the four slow-sorption redistribution stages and changed the commented `Do J = I,Ncxsl` to the site-complete `Do J = 1,Ncxsl`. No other model source change was made. Executable SHA-256:

`8508313332cc95bd89cf5a0d188718e9d0cdb2a232cea92c196d88a16cca4afa`.

A separate observer variant, SHA-256

`f0b11f4b3bda03f15c95b5c6ad1f18730693c0cf4c1ea82140c73cf82b4c577b`,

measured the site-specific slow-sorbed P mass immediately before and after each of the four plough events. For every one of the 12 event/site combinations, the observed before-minus-after difference is exactly `0.0` in the diagnostic arithmetic. The sensitivity route is therefore locally conservative for this state.

That does **not** qualify it as the scientifically intended revision-53 route.

## 5. The policy choice is scientifically material

After normalizing only volatile run timestamps and elapsed-time fields, the frozen diagnostic baseline and the conservative slow-sorption sensitivity variant differ in 11 output files:

- `PClassYearSwitch.out`;
- `ani_pGP.Bal`, `ani_pRP.Bal`, `ani_pTP.Bal`;
- `bappGP.Out`, `bappRP.Out`, `bappTP.Out`;
- `discharge.out`;
- `initial.out`;
- `pal-P.out`;
- `pw-P.out`.

The first formatted `pal-P.out` and `pw-P.out` difference occurs exactly at the first plough event (`1997`, `Tito=2414`, `Tiyr=222`). Across the 900 written profile records:

| output | changed records | changed cells | maximum formatted absolute change |
| --- | ---: | ---: | ---: |
| `pal-P.out` | `663` | `3318` | `1.35` |
| `pw-P.out` | `663` | `3293` | `0.99` |

The largest formatted differences occur in compartment 1 in 2004. `discharge.out` changes only in the six PO4 runoff/drainage columns; the largest absolute formatted change is `2.7092e-5` in `RuPO4`.

The total-profile PO4 balance does not become artificially perfect under this sensitivity. Its final cumulative `BAPPDVCU` changes only from about `-0.273` to `-0.277 kg ha-1 P` for TP, with similarly small changes for RP and GP. That is consistent with the experiment being a conservative **spatial-state policy change**, not a missing-total-mass patch. Other already registered P numerical and ledger seams remain present.

## 6. TCD-031 classification

PREP09 registers a new discrepancy as:

`TCD-031 REVISION_SPECIFIC_SLOW_SORPTION_TILLAGE_POLICY_GAP_WITH_NATURAL_TRAJECTORY_MATERIALITY`

This is deliberately **not** classified as a confirmed legacy code defect. The evidence establishes all of the following:

- the 4.0 public semantics describe ploughed compartments as redistributed;
- slow-sorbed P is a site- and compartment-resolved physical state;
- revision 53 contains but disables the matching redistribution producer while retaining its ledger reset/consumer surface;
- the supplied LWKM case naturally activates non-zero heterogeneous slow-sorbed P during ploughing;
- a conservative site-preserving redistribution sensitivity materially changes P state, P indicators and PO4 discharge trajectory.

What the supplied evidence does **not** establish is why the route was disabled in 2010 or whether revision 53 intentionally adopted a policy in which slow-sorbed P remains spatially immobile during tillage. Matching 4.1.x formulation/change provenance or an independently trusted historical reference is required before choosing either behaviour for corrected legacy or ANIMO5.

## 7. ANIMO5 architectural consequences

PREP09 strengthens four migration constraints:

1. internal element transfers must be computed from explicit pre-state and post-state element amounts when carrier fractions can change during the event;
2. management operations must declare which physical state families they redistribute and which they intentionally leave immobile;
3. sorption-site identity must be preserved through management operations independently of management-event indices;
4. an inactive producer must not leave a misleading active ledger contract without an explicit feature/policy state.

## Gate

`QUALIFIED_DIAGNOSTIC_TCD030_CAUSALITY_AND_TCD031_POLICY_MATERIALITY_REFERENCE_ADMISSION_BLOCKED`

PREP02 historical or independently trusted reference qualification remains required before either corrected-legacy admission or production migration.
# TCD-016 dry-solute state reconstruction

Work unit: `ANIMO-SQ01`

Status: `SOURCE_BOUND_RECONSTRUCTION_COMPLETE_THEORY_GAP_REMAINS`

Production migration: `NOT_ADMITTED`

## 1. Evidence boundary

This reconstruction is bound to the frozen ANIMO 4.1.5 revision-53 source archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

and to the supplied historical testbank:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Neither frozen artifact was modified.

The supplied ANIMO 4.0 User's Guide is used as inherited ANIMO-specific theory/interface evidence. TH01 and TH02 are used as qualified provenance context, not as substitutes for missing dry-state theory. B3Q01 supplies the controlling qualification class. PREP06 supplies the source-bound state ownership model.

Relevant live evidence heads at work-unit start:

- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`
- TH01: `a3360415364ef4a66a81d7b6715bcd400829df1b`
- TH02 revision-41 lineage: `f7f3722b14f65340dc6d67a8f80d74f5d0ebb158`
- PREP06 observed head: `9b1f1ea51c24fb82823290193651830dc61ea3c8`

The SQ01 branch is intentionally based on the B3Q01 classification head. Parallel theory and preparatory branches are cited as pinned evidence rather than merged ad hoc.

## 2. TCD-016 classification

B3Q01 classifies TCD-016 as:

- primary Class C: `MISSING_PHYSICAL_STATE_OR_INCOMPLETE_STATE_MODEL`
- secondary Class E: numerical or threshold policy may also be involved
- atomicity: `REQUIRES_ATOMIZATION_BEFORE_ADMISSION`
- current disposition: `UNRESOLVED_NOT_ADMITTED`.

That classification is supported by the observed behaviour. The local balance can be closed algebraically by forcing a counterfactual outflow, but doing so produces a physically unacceptable concentration. Therefore the problem is not reducible to a missing balance term.

## 3. Physical and numerical states in the affected route

### 3.1 Layer 0 is the ponding/surface-water compartment

ANIMO 4.0 documents compartment 0 as the layer reserved for ponding. It separately documents a virtual top reservoir for additions. The two are not the same state.

For detailed hydrology, revision 53 reconstructs layer-0 water state in `Hydro_detailed.for`:

```fortran
Mofro(0) = max(0,(Pn+Snla)  / He(0))
Mofrt(0) = max(0,(Pnt+Snt) / He(0))
Mofr(0)  = 0.5 * (Mofro(0) + Mofrt(0))
```

Thus the layer-0 aqueous storage is driven by actual ponding plus snow water storage. `Pn -> Pnt` is a persistent water-state pair across timesteps.

### 3.2 NH4 state coordinates

The NH4 transport state is:

- `Conh(Ln)`: concentration at the start of the timestep, kg N m-3 water
- `Rsconh(Ln)`: concentration at the end of the timestep, kg N m-3 water
- `Cxnh(Ln)` / `Rscxnh(Ln)`: adsorbed NH4 layer amount for soil layers.

PREP06 correctly identifies `Conh/Rsconh` as aqueous NH4 for layer 0 plus soil layers, while the separately adsorbed NH4 state is a soil-layer state.

`Inicalc.for` maps soil-horizon sorption and bulk-density parameters only for `Ln=1..Nl`:

```fortran
Socfnh(Ln) = Socfnhho(Lnhn(Ln))
Rhbd(Ln)   = Rhbdho(Lnhn(Ln))
```

and initializes adsorbed NH4 only for `Ln=1..Nl`. There is no source-defined layer-0 dry solid or sorbed NH4 owner corresponding to the ponding compartment.

### 3.3 Artificial top reservoir is a different state

The source contains `Conhtop/Rsconhtop`, stored over `Hetop`. ANIMO 4.0 explicitly defines this as the virtual reservoir used for fertilizer additions. `UBoundconc.for` gives it precipitation or infiltration controlled residence-time behaviour when there is no ponding, and flushes it into the ponding route when ponding is active.

This existing state cannot be silently relabelled as generic dry residue from layer 0. Its origin, ownership and release law are different.

## 4. Transport equation and affected routines

The inherited ANIMO 4.0 conservation and transport equation represents dissolved storage as liquid fraction times concentration, with optional solid-phase terms. The affected revision-53 call chain is:

`Hydro_detailed -> UBoundconc -> TRANSPORT -> Transsub -> Init -> Output_Init`.

Important responsibilities are:

- `Hydro_detailed.for`: constructs old and new ponding water storage
- `UBoundconc.for`: routes upper-boundary loads and dry deposition to layer 0 or layer 1 depending on ponding
- `TRANSPORT.FOR`: invokes `Transsub` for NH4 and compiles local `BAPD` and `BATR`
- `Transsub.for`: computes average and end concentration, including low-storage branches
- `Init.for`: promotes `Rsconh -> Conh` for the next timestep
- `Output_Init.for`: writes restartable concentration states, including layer 0, but no dry-solute mass state.

## 5. Exact wet-to-dry failure mechanism

The canonical diagnostic event is from `Puitmijn_Cranendonck_60`, balance file `banhL1.Out`, year 2006, at `TITO=1490` for layer 0.

Observed call state:

| variable | value |
| --- | ---: |
| `Iflsol` | 2 |
| `Co` | 0.12767937602481674 kg N m-3 |
| `Mto` | 5.435585e-4 m3 m-3 |
| `Mt` | 1.628217e-5 m3 m-3 |
| `Ld` | 0.2 m |
| `St` | 1 d |
| `Fu` | 4.1184400265397315e-10 m d-1 |
| `Fev` | 1.05455e-4 m d-1 |
| `Reko` | 0 |
| `Reki` | 0 |
| layer-0 sorption contribution | 0 |

Initial dissolved NH4 mass is:

`M_before = Mto * Ld * Co = 1.3880242022597072e-5 kg N m-2`

which is:

`0.13880242022597072 kg N ha-1`.

`Transsub.for` applies `Factor=100` at `Ln=0`. When the final aqueous storage falls below the low-storage threshold while initial storage is above it, the relevant branch sets:

```fortran
rsc = 0.0
if (ln.eq.0 .and. Fu.gt.1.0d-6) then
   ...
else
   if (Iflsol.eq.2) avc = 0.0d0
endif
return
```

For the observed event `Fu` is far below `1e-6`. Therefore both `Rsc` and `Avc` become zero. `TRANSPORT.FOR` then has no end aqueous storage, no adsorbed layer-0 storage and no solute outflow carrying the old mass.

The local terms are:

- `BAPD = 0`
- `BATR = -1.3880242022597072e-5 kg N m-2`.

The annual deviation is the same mass in kg N ha-1 to the precision of the diagnostic evidence.

## 6. Independent frozen-source reproduction

SQ01 compiled the unmodified frozen `Transsub.for` in an external diagnostic driver. Compilation required the legacy compiler compatibility flag `-fallow-argument-mismatch`; no source bytes were changed.

Using the observed event parameters and zero external solute inputs, the frozen routine returned:

```text
RSC          = 0
AVC          = 0
M_BEFORE     = 1.3880242477171123E-05 kg N m-2
M_AFTER_AQ   = 0
M_OUT        = 0
RESIDUAL     = 1.3880242477171123E-05 kg N m-2
```

The small difference from the previously captured double-precision diagnostic value is explained by the routine's default `REAL` interface and the rounded parameters supplied to the standalone probe. The qualitative and control-volume result is exact: the branch deletes the represented dissolved mass.

## 7. Dry continuation and rewetting in the legacy source

### 7.1 No dry continuation state

A one-step counterfactual that retains the old mass by raising concentration can close the first transition, but once hydrology reaches exactly zero water storage the aqueous coordinate cannot hold finite mass. `Init.for` promotes only the resulting concentration. There is no independent layer-0 dry mass state to carry the material through the dry interval.

### 7.2 No defined dry-to-wet remobilization

The opposite low-storage branch in `Transsub.for` initializes a new wet concentration from current timestep forcing. It has no access to any mass that disappeared during a previous dry state. Consequently the legacy source does not define a reversible wet -> dry -> wet state transition for residual layer-0 NH4.

### 7.3 Restart is incomplete for the missing phase

`Output_Init.for` writes `Rsconhtop` and `Rsconh(0:Nl)`. It does not write a generic dry surface NH4 mass state because no such state exists. A hypothetical correction that keeps mass outside those existing states would therefore be restart-incomplete unless restart semantics were extended explicitly.

## 8. What ANIMO 4.0 theory does and does not establish

The supplied ANIMO 4.0 User's Guide establishes:

- dissolved NH4 is transported with water
- the dissolved state is a liquid-phase concentration
- compartment 0 is a ponding layer
- the additions reservoir is a separate virtual reservoir
- NH4 sorption is defined through soil-horizon parameters
- restart output reproduces the model state families used for initialization.

It does not define a dry surface residue store, a residual chemically active water film, a forced transfer from ponding residue into soil sorption, or a dry-to-wet remobilization law.

The guide cites Alterra Report 983 as the more complete ANIMO 4.0 process description. TH01 confirmed the public WUR record for that report but did not ingest it into B0. SQ01 located the official WUR publication record, but did not obtain a text of Report 983 that could be used to establish dry-continuation semantics. Therefore absence of such semantics in Report 983 is not claimed.

TH02 adds release-lineage provenance for `Transsub.for` but no dry-state model authority. The source history marker says that the routine participated in ANIMO 4.0 and 4.1 releases. A release stamp is not scientific proof that the low-storage branch expresses intended phase theory.

## 9. Reconstruction conclusion

TCD-016 is a genuine state-model seam:

1. layer-0 NH4 mass is physically represented only while a liquid ponding storage exists;
2. the low-storage branch can set both remaining and average concentration to zero before all mass has left the control volume;
3. no layer-0 sorbed, precipitated or dry-residue state receives the mass;
4. the additions reservoir is semantically distinct and cannot be reused without changing its meaning;
5. no dry-to-wet recovery path exists for vanished residual mass;
6. restart cannot preserve a nonexistent dry phase.

The legacy implementation is therefore conservation-incomplete across disappearance of the mobile surface-water phase. The scientific form of a corrected continuation state is not yet established by the available ANIMO-specific theory.

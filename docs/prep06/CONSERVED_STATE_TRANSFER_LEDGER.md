# ANIMO-PREP06 — Conserved state and transfer-ledger audit

Status: `SOURCE_BOUND_STATE_LEDGER_MAP_ESTABLISHED_MACROPORE_BEHAVIOURAL_QUALIFICATION_BLOCKED`.

## Work-unit contract

Purpose: reconstruct the conserved-state ownership and transfer-ledger structure of the supplied ANIMO 4.1.5 revision-53 source before any production state architecture or mass-ledger abstraction is designed.

Affected components: water storage, organic-matter C/N/P stores, mineral N, mineral P sorption/precipitation, GHG states, macropore water/solute states, timestep state promotion and public balance accounting.

Physics change: no.

Numerical-policy change: no.

Frozen-source change: no.

Verification contract: every asserted transaction/state or macropore ledger seam below must be source-bound to the exact source archive SHA-256 and checked by `tools/audit_conserved_state_ledger.py`. The supplied testbank is used only to establish path coverage, not to infer unobserved behaviour.

Checkpoint boundary: this workunit may qualify a source-bound state/ledger map and identify static integration gaps. It may not admit a corrected legacy implementation or ANIMO5 production migration without the PREP02 reference gate.

## Frozen identity

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

## 1. State promotion is an explicit legacy transaction seam

The source already contains a strong distinction between state at the beginning of a timestep and calculated state at the end of that timestep.

`Animo.for` calls `Init` at the start of the next step under the source comment `UPDATE STATE VARIABLES (RESULT FROM PREVIOUS STEP)`. `Init.for` then promotes result variables into current/start variables. Representative pairs are:

```text
Mofrt          -> Mofro
Sict           -> Sic
Pnt            -> Pn
Walet          -> Wale
Rsconh         -> Conh
Rscxnh         -> Cxnh
Rsconi         -> Coni
Rscodiorma     -> Codiorma
Rscodiorni     -> Codiorni
Rscodiorpo     -> Codiorpo
RsCoStdiorma   -> CoStdiorma
RsCoStdiorni   -> CoStdiorni
RsCoStdiorpo   -> CoStdiorpo
Rsex           -> Ex
Rshuex         -> Huex
Rshuos         -> Huos
Rsos           -> Os
Rscopo         -> Copo
Rsampopr       -> Ampopr
Rsamcxfa       -> Amcxfa
Rsamcxsl       -> Amcxsl
SrWaMp         -> SrWaMpOld
RsCoMp*        -> CoMp*
```

This is not yet an ANIMO5 transaction API, but it is important migration evidence. A later canonical state design should preserve the distinction between accepted/start state and trial/result state instead of flattening the paired legacy variables before their semantics are qualified.

## 2. Initial ledger storage is source-explicit

`Outbal_Init.for` reconstructs initial balance storage directly from state variables. Principal mappings are:

- matrix soil water from `He * Mofro`;
- snow and pond/surface-water stores according to the hydrology route;
- labile dissolved organic C/N/P from aqueous concentration plus the `Rhbd * SocfDOM` sorbed contribution;
- stable dissolved organic C/N/P from aqueous concentration plus the `Rhbd * SocfSDO` sorbed contribution;
- fresh organic matter, original humus, exudate-derived humus and exudate material from their solid stores and C/N/P fractions;
- aqueous NH4 plus the separate adsorbed NH4 store `Cxnh`;
- aqueous NO3;
- aqueous PO4, fast sorption, slow sorption and precipitated-P stores.

The machine-readable inventory in `docs/prep06/CONSERVED_STATE_INVENTORY.csv` records these state families, their result-state partners, principal mutators and public ledger families.

## 3. Process ownership is distributed, not ledger-owned

The balance arrays are observers/accounting surfaces. They are not the canonical physical state.

Source-bound process ownership is distributed approximately as follows:

- water: `Input_hydro`, `Hydro_detailed`, `Hydro_aggregated`, plus `MAPOHYDRO` for the macropore domain;
- labile dissolved organic C/N/P: `Transca -> Transport -> Transsub`;
- stable dissolved organic C/N/P and solid organic transformations: `Resp_miner`;
- NH4 and NO3: `Transport -> Transsub`, with process source/sink terms supplied by transformation routines;
- mineral P: `Transgen -> Transorp/Transsub`;
- GHG states: `GHGasses` and associated GHG transport routines;
- macropore solutes: `MAPOTRANSPORT`.

A future `MassLedger` must therefore observe explicit state and transfer ownership. It must not become a second hidden state machine whose accounting arrays are treated as authoritative physical stores.

## 4. TCD-025: macropore control volume is larger than the main balance interface

### Specialized macropore water closure

`MAPOHYDRO.FOR` explicitly treats macropore storage and direct drainage as part of its water control volume. Its balance calculations include:

```fortran
Badev = Badev - FlMpOuDrTo * St
Badev = Badev + FlMpInPr(Dn) * St - (SrWaMp(Dn)-SrWaMpOld(Dn))
```

and the dedicated macropore balance subtracts the change in `SrWaMp` from total inflow minus outflow. `SrWaMp` is therefore a physical water store in the macropore control volume.

### Specialized macropore solute closure

`MAPOTRANSPORT.FOR` constructs old and new solute storage from:

```text
SrWaMpOld * CoMp
SrWaMp    * RsCoMp
```

and evaluates:

```text
BaDev = ToInMp + SrAmMpOld - (ToOuMp + SrAmMp)
```

The macropore solute solver therefore also has an explicit conserved storage control volume.

### Main `Outbal_calc` mismatch

The main public balance route cannot represent the same control volume completely:

- `Outbal_calc.for` does not receive `SrWaMp`;
- it does not receive result macropore concentrations `RsCoMp*` as storage-state inputs;
- the macropore water direct-drainage addition is present only as commented provisional code;
- the DOM macropore direct-drainage addition is also commented;
- active `Dra4` additions exist for NH4, NO3 and organic N;
- no active `Dra4` addition was found for inorganic or organic P;
- no active `Ddev` expression in `Outbal_calc.for` references `Dra4` at all.

`Outbal_write.for` nevertheless exposes `Dra4` values in the diagnostic/output surface. `Dra4` is thus an intended ledger quantity but not an integrated term in the main residual equations in the supplied source.

The classification is:

`SOURCE_CONFIRMED_MACROPORE_MAIN_LEDGER_STATE_AND_DRA4_INTEGRATION_GAP_TESTBANK_UNEXERCISED`

This is stronger than a documentation gap because the source itself defines a conserved macropore storage/flux control volume that the main ledger interface cannot fully represent. It is weaker than behavioural/reference qualification because the supplied testbank never activates this route.

## 5. Supplied-testbank coverage is zero for the macropore route

The PREP06 audit found 12 `MacroPoreOption` settings across the supplied GENERAL input variants. Every observed value is `0`.

Therefore no supplied ordinary case can measure the size of TCD-025. Absence of a macropore residual in the current regression envelope is not evidence of correctness, and no tolerance may be derived for this route. A dedicated macropore qualification case is required before any corrected-ledger design is admitted.

This strengthens the broader test-architecture rule already exposed by TCD-024: every supported constitutive/process option needs explicit path coverage rather than relying on the historical testbank to happen to exercise it.

## 6. Dormant layer-0 stable-DOM limitation

`Outbal_calc.for` contains explicit comments that stable DOM/DON/DOP components are not yet included in the layer-0 runoff terms. This would be a ledger omission if stable dissolved-organic state were allowed at layer 0.

However, the supplied revision-53 source forces stable layer-0 concentrations and their average/result counterparts to zero in `Addit.for`. PREP06 therefore does not promote this to an active defect. It is retained as a source-declared dormant limitation that must be revisited if ANIMO5 permits stable dissolved-organic storage at the surface.

The same discipline applies to apparent N/P stable-runoff species-name inconsistencies in output routines. Because the relevant layer-0 stable states are forced to zero in the current source, they are not promoted to behavioural defects without an activating state contract.

## 7. Architectural consequences for ANIMO5

The source evidence supports several design constraints.

First, preserve explicit accepted/start versus trial/result state. The legacy pairing is scientifically meaningful and should not be erased before transactional semantics are qualified.

Second, give each conserved store one state owner and explicit unit. Ledger code should read those stores, not recreate them through unrelated reporting arrays.

Third, represent internal and external transfers separately. A transfer record should identify source store, destination store or boundary, conserved quantity, amount and control-volume scope. This makes omissions such as TCD-017, TCD-018 and TCD-025 detectable by construction.

Fourth, control-volume scope must be explicit data. The same transfer can be internal for one balance profile and external for another.

Finally, if macropores remain supported, `SrWaMp` and macropore solute storage must participate in the same canonical state/ledger contract as matrix water and solute stores. A special `Dra4` reporting slot is insufficient.

## 8. Qualification gate

PREP06 qualifies only the source-bound mapping and static identification of the macropore integration gap.

It does not qualify the magnitude of TCD-025 under a physical macropore case, a corrected legacy balance formula, the 4.1.5 macropore theory contract, a canonical ANIMO5 `MassLedger` implementation, or production process migration.

Required next evidence for TCD-025:

1. obtain the historical or independently admitted reference environment required by PREP02;
2. define a dedicated macropore case with nonzero storage change and direct drainage;
3. capture unrounded `SrWaMp`, `CoMp/RsCoMp`, matrix/macropore exchange and direct-drainage terms;
4. reconcile the specialized `MAPOHYDRO`/`MAPOTRANSPORT` balances with the public water/C/N/P ledgers;
5. only then design and independently admit a corrected ledger interface.

Production migration remains `NOT_ADMITTED`.

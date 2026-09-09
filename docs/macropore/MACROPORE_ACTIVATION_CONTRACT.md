# Macropore activation contract

Work unit: `ANIMO-MP01`

This document describes the revision-53 activation contract. It is not a proposal to broaden supported configurations.

## 1. Configuration gate

Revision-53 `GENERAL.INP` reads:

`MacroPoreOption=` -> `Ioptmp`

with an accepted integer range `0..1`.

Interpretation:

- `Ioptmp=0`: macropore subsystem disabled;
- `Ioptmp=1`: macropore subsystem requested.

Source presence alone is not activation. Positive path execution requires the hydrological and state contracts below.

## 2. Hydrology gate

The qualified macropore route is tied to detailed hydrology.

Required configuration:

`HydrologicInput=2`

The detailed SWATRE input contains `Hlpimp`. Revision 53 applies an explicit consistency check:

- `Hlpimp=2` and `Ioptmp!=1` -> error 152;
- `Hlpimp!=2` and `Ioptmp=1` -> error 153.

Therefore the positive revision-53 detailed-hydrology path requires:

`Ioptmp=1 AND Hlpimp=2`

The supplied natural cases do not satisfy this. Their active `GENERAL.INP` members use `MacroPoreOption=0`; the detailed SWAP cases inspected by MP01 use non-macropore hydrology flags such as `HLPIMP=1` or `11`.

### Aggregated hydrology

`Hydro_aggregated.for` locally sets `Ioptmp=0` and comments that macropore arguments are only relevant for `Hydro_detailed`.

MP01 therefore classifies `HydrologicInput=1` with `MacroPoreOption=1` as:

`NOT_A_QUALIFIED_REV53_MACROPORE_CONFIGURATION`

The legacy source does not provide a clean equivalent activation contract for aggregated hydrology. ANIMO5 must not infer support for this combination from the parser accepting `MacroPoreOption=1`.

## 3. Static hydrological records

When `Ioptmp=1`, `mapoinput.for` reads additional unformatted SWATRE records.

Static geometry, `Nupa=1`:

- `VlMpSt(1,1:Nl)`: static macropore volume, Main Bypass domain;
- `VlMpSt(2,1:Nl)`: static macropore volume, Internal Catchment domain;
- `AgDiam(1:Nl)`: matrix polygon/aggregate diameter input, retained in the file interface although molecular diffusion is disabled in this revision.

These records must be present in the exact binary sequence expected by revision 53. Merely changing the option flag without adding the records is not a valid diagnostic transformation.

## 4. Initial hydrological state

`mapoinput`, `Nupa=2`, reads:

- one dummy water-level value;
- `VlMp(1)`;
- `SrWaMp(1)`;
- `VlMp(2)`;
- `SrWaMp(2)`;
- `SrWaMpCp(1,1:Nl)`;
- `SrWaMpCp(2,1:Nl)`.

`SrWaMp` is conserved macropore water storage. It is not optional observer data.

## 5. Soil-side routing parameters

When active, `SOIL.INP` must contain:

`>MPfrac:`

followed by:

- `FrMpRuRv`, fraction of runoff input routed through the reservoir path;
- `FrMpDrSo`, fraction of macropore drainage routed through soil rather than directly through the macropore drain path.

Both are checked against `0..1`.

### Molecular diffusion

The historical 4.0 input surface exposes `>MPdscf:` coefficients. In revision 53 the corresponding read/check block is commented out and the source states that molecular diffusion is disabled in this version.

Contract status:

`DISABLED_IN_REV53`

No MP01 diagnostic re-enables it.

## 6. Initial solute state

When `Ioptmp=1`, `INITIAL.INP` must contain:

### `>MPnitr:`

Four values:

1. `CoMpNh(1)`
2. `CoMpNh(2)`
3. `CoMpNi(1)`
4. `CoMpNi(2)`

### `>MPorgs:`

Four values:

1. `CoMpDiorMa(1)`
2. `CoMpDiorMa(2)`
3. `CoMpDiorNi(1)`
4. `CoMpDiorNi(2)`

### `>MPphos:`

Required only when `Ipo=1`:

1. `CoMpPo(1)`
2. `CoMpPo(2)`
3. `CoMpDiorPo(1)`
4. `CoMpDiorPo(2)`

These are initial physical concentrations whose conserved mass contribution depends on macropore water storage.

### Ancillary source finding: nitrate input validation

`mapoinput.for` reads `CoMpNi(1:2)` correctly but the subsequent range-check calls labelled `CoMpni(1)` and `CoMpni(2)` pass `CoMpnh(1)` and `CoMpnh(2)` instead of the nitrate variables.

Classification:

`SOURCE_CONFIRMED_MACROPORE_INITIAL_NO3_VALIDATION_SEAM_NOT_PART_OF_TCD025`

MP01 does not repair it and does not promote it to a numbered canonical discrepancy on this divergent evidence branch. It must be reconciled through governance before any future production input layer is claimed equivalent.

## 7. Dynamic hydrological records

For every detailed hydrological timestep, `mapoinput`, `Nupa=5`, reads additional macropore data.

### Domain 1, Main Bypass

- `VlMp(1)`
- `SrWaMp(1)`
- `FlMpInPr(1)`
- `FlMpInRu(1)`
- `SrWaMpCp(1,1:Nl)`
- `FlMpOuIf(1,1:Nl)`
- `FlMpOuDr(1:Nl)`
- `FrHeWeMpWl(1,1:Nl)`

### Domain 2, Internal Catchment

- `VlMp(2)`
- `SrWaMp(2)`
- `FlMpInPr(2)`
- `FlMpInRu(2)`
- `SrWaMpCp(2,1:Nl)`
- `FlMpOuIf(2,1:Nl)`
- `FrHeWeMpWl(2,1:Nl)`

There is no separate domain-2 direct-drain array in this input contract.

## 8. Timestep reachability gate

`Ioptmp=1` means configured, not necessarily dynamically active during every timestep.

`MAPOHYDRO` determines the wet extent of each domain from `FrHeWeMpWl`. It then derives `Nd`:

- `Nd=0`: no wet macropore domain, further macropore calculations for the timestep are unnecessary;
- `Nd=1`: Main Bypass active;
- `Nd=2`: both domains relevant.

The solute path is guarded by conditions equivalent to:

`Ioptmp=1 AND Nd>0`

Positive B1 evidence therefore requires nonzero/reachable dynamic macropore water geometry, not only a configuration switch.

## 9. Process activation by species

With `Ioptmp=1` and `Nd>0`:

- labile DOM is routed through the generic transport/macropore kernel;
- DON is routed through the same kernel;
- NH4-N is routed through the same kernel;
- NO3-N is routed through the same kernel;
- DOP is routed through the same kernel if `Ipo=1`;
- PO4-P is routed through `Transgen` and the same macropore transport kernel if `Ipo=1`.

P-disabled cases must not be interpreted as positive evidence for DOP or PO4-P macropore transport.

## 10. Accepted-state promotion

At accepted timestep continuation, `Init.for` performs:

- `SrWaMp -> SrWaMpOld`;
- `RsCoMpDiorMa -> CoMpDiorMa`;
- `RsCoMpDiorNi -> CoMpDiorNi`;
- `RsCoMpNh -> CoMpNh`;
- `RsCoMpNi -> CoMpNi`;
- P-active `RsCoMpDiorPo -> CoMpDiorPo`;
- P-active `RsCoMpPo -> CoMpPo`;
- layer-resolved `SrWaMpCp` is combined into `SrWaMpCpOld`.

This is the in-memory continuation contract.

It must not be confused with persistent restart serialization. The latter is incomplete, as documented in `TCD025_QUALIFICATION.md` and the status file.

## 11. Controlled diagnostic case design

Positive whole-case diagnostics must be B0-derived rather than free-standing replacements.

Selected parent: supplied `CranGrass`.

Pinned parent members:

- `animo.ini`: `5d1f62faf62747b7d91d3e9199e33954e3038ddd005259f32a8bca95f0c82bb8`
- `Input/GENERAL.INP`: `fee38c975061ea187747f05e7c599d8313717739c1ed084a9225ad8942b3567b`
- `Input/SOIL.INP`: `2dae9930f49a7ca6ee8ea3d272818010dd86b8efb97d1c22597bfa2db6a8179f`
- `Input/Swatre.unf`: `350d3a3715e313d6fd19167fc34f6186f7ab8752fbf7570db05bfc0e7b8add80`

Its detailed hydrology has `HLPIMP=1`, so the activation delta to `2` is explicit.

Every future descendant must record the exact changed record set and preserve all unrelated parent content.

### MP01-STORAGE

- activate the common contract;
- nonzero initial and final `SrWaMp` with zero net change;
- nonzero macropore solute concentration;
- zero top input, matrix exchange and direct drainage;
- expected identity: old storage = new storage.

### MP01-EXCHANGE

- activate both domains;
- use domain 2 as the principal exchange path;
- prescribe matrix -> macropore and/or macropore -> matrix fluxes with no external direct drain;
- expected combined matrix + macropore identity: exchange cancels exactly.

### MP01-DIRECT-DRAIN

- activate Main Bypass domain;
- prescribe nonzero `FlMpOuDr`;
- use `FrMpDrSo` to isolate the direct component;
- expected identity: storage loss and/or input equals direct-drain export plus any matrix exchange.

### MP01-SOLUTE

- provide a nonzero top solute concentration with macropore water input;
- optionally pair with macropore -> matrix transfer;
- execute at least NH4-N/NO3-N and one P-active descendant before species-specific whole-route support is claimed.

### MP01-NO-MP

- exact frozen `CranGrass` active members unchanged;
- `MacroPoreOption=0`, `HLPIMP=1`;
- role: negative control and non-interference only.

The four positive whole-case descendants are currently `DESIGNED_NOT_FULL_CASE_EXECUTED`. The separate frozen-kernel B1 probes are already executed and are recorded in `ANIMO-MP01_DIAGNOSTIC.json`.

## 12. Admission rules

A future implementation may claim the macropore route only when all of the following are independently resolved:

- source and theory contract preserved;
- full active whole-case path executed;
- persistent restart state is complete;
- main ledger control volume includes macropore state and external direct drainage;
- historical B2 evidence is available or a formally approved alternative admission basis exists;
- a separate B3 decision has been made.

MP01 itself does not make that admission.

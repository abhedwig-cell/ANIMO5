# Legacy mass-balance crosswalk and qualification seam

Status: `SOURCE_BOUND_BALANCE_CONTRACT_MAPPED_4_1_5_THEORY_RECONCILIATION_OPEN`.

## Purpose

Mass conservation is a scientific invariant for ANIMO5. PREP01 therefore maps the legacy balance implementation before process migration or interface shortening.

This document distinguishes:

- source behaviour in the supplied ANIMO 4.1.5 revision-53 archive;
- documented ANIMO 4.0 balance output semantics in the supplied User's Guide, Annex 2, Tables 16-22;
- later 4.1.x extensions visible only in the supplied source;
- qualification decisions that remain open.

No numerical tolerance is invented in PREP01.

## 1. Balance families

`Outbal_calc.for` states that balances are created for water, organic matter, nitrate-N, ammonium-N, organic-N, ortho-PO4-P and organic-P over a configurable profile interval `BALNMI(LY):BALNMA(LY)` and balance period.

The source maintains the following principal arrays, each sharing the legacy term-index namespace from `outbal1.inc` and `outbal2.inc`:

| Array | Source/output interpretation | Units in legacy output |
| --- | --- | --- |
| `Bawa` | water | mm |
| `Bfom` | fresh/solid organic matter bookkeeping | kg ha-1 organic matter |
| `Bahu` | humus organic matter bookkeeping | kg ha-1 organic matter |
| `Bdom` | dissolved organic matter | kg ha-1 organic matter |
| `Banh` | NH4-N | kg ha-1 N |
| `Bani` | NO3-N | kg ha-1 N |
| `Bano` | organic N | kg ha-1 N |
| `Bapp` | PO4-P including solution/complex/precipitated storage | kg ha-1 P |
| `Bapo` | organic P | kg ha-1 P |
| `Btom` | additional GHG emission bookkeeping introduced after the documented 4.0 balance contract | kg ha-1 organic-matter-equivalent bookkeeping in source context; exact 4.1.5 theory interpretation remains open |

The supplied ANIMO 4.0 User's Guide Annex 2 documents seven public balance-output families: `BAWA`, `BAOM`, `BANH`, `BANI`, `BANO`, `BAPP` and `BAPO`. The source-level split of `BAOM` into `Bfom`, `Bahu` and `Bdom` is visible in `Outbal_calc.for` and `Outbal_write.for`.

## 2. Shared 74-slot balance-term namespace

`outbal1.inc` and `outbal2.inc` define one shared integer index contract used across the balance arrays. `tools/audit_balance_indices.py` extracts this directly from the hash-pinned source archive; the exact map is persisted in `docs/prep01/BALANCE_INDEX_MAP.csv`.

Important groups are:

- `1..4`: top/bottom vertical boundary fluxes;
- `5..17`: precipitation/snow/irrigation/runon/inundation, evaporation/runoff terms;
- `18..26`: infiltration from drainage systems 1..9;
- `27..35`: drainage to systems 1..9;
- `36..41`: beginning/end water storage slots for snow, ponding and soil moisture;
- `42`: `Ddev`, the balance-period residual;
- `43..48`: final/initial storage slots for solid/solution/precipitated chemical stores;
- `49..66`: additions, crop residues, exudates, transformations, deposition, mineralization, immobilization, nitrification, volatilization, uptake, denitrification, dissimilation, diffusion uptake and redistribution;
- `67..73`: GHG formation/emission and N2O bookkeeping;
- `74`: `Dra4`, a macropore drainage bookkeeping slot.

The GHG and macropore indices are later source extensions and are not described by the supplied 4.0 Annex 2 tables.

## 3. Balance-residual definition

The source does not derive a single generic residual. It constructs a separate `Ddev` expression for each balance family. The common conceptual form is:

```text
residual = external inputs
         - external outputs
         - storage change
         + internal source terms relevant to that pool
         - internal sink terms relevant to that pool
```

but the exact terms differ by pool and by whether the selected balance profile includes the addition reservoir (`Ln1=0`), soil layer 1, and lower soil layers.

### Water

For a balance beginning at the surface reservoir, `Bawa(Ddev,Ly)` contains precipitation/rain, snow, irrigation, runon, inundation and upward lower-boundary flux as inputs; pond evaporation, interception, snow sublimation, runoff and downward lower-boundary flux as outputs; snow/pond/soil storage changes; plant/soil evaporation where the soil profile is included; and drainage/infiltration terms for every active drainage system.

For a subsurface balance profile the top-boundary terms switch to `Topd`/`Topu`. This is an important qualification property: the meaning of a balance term depends on the selected balance-profile boundary, not only on its index.

### Organic matter

The source computes three residuals:

```text
Bfom(Ddev) = Addi + Redi + Crpr + Exud
           - Diss
           - Finp_x + Inip_x

Bahu(Ddev) = Addi + Redi + Form
           - Diss
           - Finp_x + Inip_x

Bdom(Ddev) = Addi + Redi + Crpr
           + lower/top/drainage transport terms
           - Finp_l + Inip_l
           + Form - Diss
```

with surface runoff and irrigation/runon/inundation terms added according to the selected profile boundary.

The source also stores `Dssi`, `CH4f`, `CO2f`, `CH4e` and `CO2e` as additional transformation/emission bookkeeping. These later decomposition terms are reported by `Outbal_write.for` but are not separately inserted as new top-level residual terms. PREP01 does not infer from this alone whether they are subordinate decompositions of already-accounted transformation terms or a theory/code discrepancy. That requires 4.1.x formulation evidence.

### Nitrogen

Three separate N residuals are maintained.

For ammonium:

```text
Banh(Ddev) = Addi + Redi + boundary inputs
           - boundary outputs
           - storage changes in solution/complex pools
           - Vola
           - Crup
           + Minn - Immo
           - Nitr
           + Crpr
           - N2On    [when GHG path is active in source]
```

plus wet/dry deposition and drainage/infiltration terms according to profile location.

For nitrate:

```text
Bani(Ddev) = Addi + Redi + boundary inputs
           - boundary outputs
           - solution storage change
           - Crup - Updf
           + Crpr
           + Nitr - Deni
```

plus wet/dry deposition and drainage/infiltration terms.

For organic N:

```text
Bano(Ddev) = Addi + Redi + boundary inputs
           - boundary outputs
           - dissolved-organic-N storage change
           + Crpr + Exud + Form - Ming
           - solid-organic-N storage change
```

plus drainage/infiltration and surface-runoff terms.

The supplied 4.0 User's Guide documents the corresponding output concepts such as mineralization, immobilisation, nitrification, denitrification, crop uptake, dry/wet deposition and transport. The source adds explicit N2O bookkeeping (`N2Od`, `N2Oe`, `N2On`) not covered by that 4.0 table contract.

### Phosphorus

For inorganic/PO4-P:

```text
Bapp(Ddev) = Addi + Redi + boundary inputs
           - boundary outputs
           - solution storage change
           - Crup + Crpr
           + Minn - Immo
           - solid/complex storage change
           - precipitated storage change
```

plus wet deposition and drainage/infiltration terms.

For organic P:

```text
Bapo(Ddev) = Addi + Redi + boundary inputs
           - boundary outputs
           - dissolved-organic-P storage change
           + Crpr + Exud + Form - Ming
           - solid-organic-P storage change
```

plus drainage/infiltration and surface-runoff terms.

The supplied 4.0 Annex 2 names the corresponding public output quantities `BAPPDV/BAPPDVCU` and `BAPODV/BAPODVCU` and documents their storage, input and output records.

## 4. Period and cumulative residuals

Each balance family stores both:

- a current balance-period residual in the shared `Ddev` slot;
- a cumulative residual variable such as `Bawadvcu`, `Baomdvcu`, `Bahudvcu`, `Badodvcu`, `Banhdvcu`, `Banidvcu`, `Banodvcu`, `Bappdvcu` or `Bapodvcu`.

At a configured balance-output/reset instant `Outbal_write` writes the current state and residuals and then resets period accumulators while carrying the end storage into the next period's initial storage slots.

This means qualification must test **both** period closure and continuity of storage across reset boundaries. Comparing only final cumulative output is insufficient.

## 5. Documentation/code alignment

Strong alignment with the supplied ANIMO 4.0 User's Guide:

- same seven public balance-output families;
- same distinction between record 1 storage/deviation, record 2 inputs and record 3 outputs;
- same top/bottom boundary interpretation depending on selected balance profile;
- same core transport, deposition, crop, mineralization/immobilisation and transformation terms;
- same units: water in mm, C/N/P balance quantities in kg ha-1.

Version-specific extensions or gaps requiring reconciliation:

1. source has up to nine drainage-system index slots and a separate macropore `Dra4` slot;
2. source has explicit GHG bookkeeping for CH4, CO2 and N2O absent from the 4.0 Annex 2 contract;
3. source records detailed organic transformation arrays `Bafom/Bafon/Bafop` beyond the high-level Annex 2 balance tables;
4. exact 4.1.5 interpretation of GHG-linked carbon and N balance decomposition is not supplied;
5. exact acceptable numerical closure tolerances are not documented in the supplied guide.

None of these differences is classified as a defect merely because the 4.0 documentation is older.

## 6. Qualification use

A future `MassLedger` abstraction should not be invented independently of this evidence. At minimum it must represent:

- conserved quantity or pool identity;
- balance-profile scope;
- beginning and end storage;
- signed external boundary transfers;
- internal transfers between explicitly represented pools;
- source/sink processes that cross the chosen ledger boundary;
- current residual;
- cumulative residual;
- units and sign convention;
- reset/continuation semantics.

For corrected-legacy and ANIMO5 qualification, conservation checks should be applied to unrounded internal quantities where possible. Formatted `.Out` files are evidence and compatibility surfaces, but must not become the only mass-conservation oracle.

## 7. Open qualification questions

PREP01 deliberately leaves these unresolved:

- numerical acceptance tolerance per conserved quantity and profile scale;
- whether the existing nonzero residuals are expected legacy numerical closure, formatting artefacts, omitted later process terms or defects;
- exact 4.1.x GHG contribution to the C/N ledger;
- macropore mass-transfer semantics and missing active testcase coverage;
- whether all nine generic drainage slots remain required in ANIMO5 or should become a dynamic boundary collection;
- whether the 74-slot shared index representation can be replaced without changing output semantics.

The next evidence step is to measure the existing deterministic diagnostic residual envelope without treating it as an acceptance threshold.

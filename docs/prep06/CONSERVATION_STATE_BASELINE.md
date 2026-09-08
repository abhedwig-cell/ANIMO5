# ANIMO-PREP06 — Conserved-state baseline

Status: `SOURCE_BOUND_STATE_LEDGER_BASELINE_EXUDATE_START_ASYMMETRY_UNQUALIFIED`.

This workunit is source/documentation audit only. Frozen source and testcases are unchanged. No production migration is admitted.

## 1. Control-volume state families visible in the revision-53 balance code

### Water

`Outbal_Init` and `Outbal_calc` explicitly book beginning/end storage for:

- ponding / surface water (`Stpn_b/e`);
- snow (`Stsn_b/e`);
- soil water (`Stsm_b/e`, from layer water contents times thickness).

The separately confirmed TCD-018 shows that detailed hydrology also carries interception storage while the legacy `Outbal_calc` interface does not.

### Organic matter / carbon-bearing state

The organic-matter balance distinguishes:

- fresh organic fractions: `Os/Rsos(Ln,Fn)`;
- humus from original material: `Huos/Rshuos`;
- humus from exudates: `Huex/Rshuex`;
- explicit exudate store: `Ex/Rsex`;
- labile dissolved organic matter: `Codiorma/Rscodiorma` including solution plus `SocfDOM` sorbed storage;
- stable dissolved organic matter: `CoStdiorma/RscoStdiorma` including solution plus `SocfSDO` sorbed storage;
- optional top-reservoir dissolved organic matter: `Codiormatop/Rscodiormatop`.

### Nitrogen

The standard N ledgers expose:

- dissolved NH4: `Conh/Rsconh` plus top-reservoir `Conhtop/Rsconhtop`;
- sorbed/exchange NH4: `Cxnh/Rscxnh`;
- dissolved NO3: `Coni/Rsconi` plus top-reservoir `Conitop/Rsconitop`;
- dissolved organic N: `Codiorni/Rscodiorni` and stable `CoStdiorni/RscoStdiorni` with DOM/SDO sorption factors;
- top-reservoir dissolved organic N: `Codiornitop/Rscodiornitop`;
- solid organic N carried by fresh OM, humus and exudate stores through `Nifr`, `Nifrhu` and `Nifrex`.

### Phosphorus

The P ledgers expose:

- dissolved PO4: `Copo/Rscopo` plus top-reservoir `Copotop/Rscopotop`;
- instantaneous/fast sorbed P: `Toamcxfa/Rstoamcxfa`;
- slow sorbed P: `Toamcxsl/Rstoamcxsl`;
- precipitated P: `Ampopr/Rsampopr`;
- dissolved organic P: `Codiorpo/Rscodiorpo` and stable `CoStdiorpo/RscoStdiorpo` with DOM/SDO sorption factors;
- top-reservoir dissolved organic P: `Codiorpotop/Rscodiorpotop`;
- solid organic P carried by fresh OM, humus and exudate stores through `Pofr`, `Pofrhu` and `Pofrex`.

## 2. Initial/final storage symmetry check

`Outbal_Init` and `Outbal_calc` are the authoritative source pair for beginning/end ledger storage in the standard balances.

A first cross-family symmetry audit shows one unqualified asymmetry:

- final fresh-organic-matter storage includes `Rsex(Ln)` in `Bfom(Finp_x,Ly)`;
- initial fresh-organic-matter storage includes `Os`, `Huos`, `Huex`, but does **not** include `Ex(Ln)` in `Bfom(Inip_x,Ly)`;
- organic-N initial storage does include `Ex(Ln)*Nifrex`;
- organic-P initial storage does include `Ex(Ln)*Pofrex`.

This is not yet classified as a defect. All supplied `INITIAL.INP` files set the `>orgexu:` state to zero, so the supplied testbank does not activate the asymmetry.

## 3. Why `Ex` is a persistent state

Source evidence shows `Ex` is not a transient diagnostic:

- `input1.for` reads `Ex(Ln)` from `INITIAL.INP`;
- `Resp_miner` evolves it to `Rsex(Ln)`;
- `Init.for` commits `Ex(Ln)=Rsex(Ln)` for the next step;
- `Output_Init.for` writes `Rsex` to restart output;
- ordinary output includes `Ex/Rsex` in total organic matter and corresponding N/P contents.

Therefore a nonzero beginning exudate store is a valid source-representable state and must be covered by a conserved ledger if the balance claims the same control volume.

## 4. Next causal gate

PREP06 will run a temporary nonzero-exudate initial-state probe against an otherwise unchanged compatible testcase, followed by a ledger-only control that adds exactly `Ex(Ln)` to `Bfom(Inip_x,Ly)`.

Only if the baseline balance offset equals the omitted initial exudate mass and the one-term control removes it without altering state/process trajectories will this finding be promoted to a discrepancy.

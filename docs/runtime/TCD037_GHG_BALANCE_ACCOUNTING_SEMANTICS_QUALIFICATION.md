# TCD-037 GHG balance observer accounting-semantics qualification

Work unit: `ANIMO-RUNTIMEQ03`

Status: `QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED`

## Decision

RUNTIMEQ02 established that revision-53 `Outbal_calc` has no source producer for local `AmCH4` or `AmN2Odeni`, while `AmN2Onitr` is rebuilt locally on each active call. RUNTIMEQ03 now resolves the next question: what source-owned quantities the disconnected observer terms are actually trying to represent.

The result is not one missing array producer. The legacy observer overloads index 0 with a different semantic role from layer indices and, for N2O, the current locally constructed index-0 value is inconsistent with the consumer label.

A single undifferentiated `AmCH4(0:Nl)` or `AmN2Odeni(0:Nl)` producer contract is therefore rejected.

The source-qualified observer inputs are instead:

1. CH4 layer formation amount from `QPrCH4(Ln) * St` for `Ln=1..Nl`;
2. CH4 atmosphere-boundary emission amount from `(QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`;
3. N2O denitrification layer formation amount from `QPrN2Oden(Ln) * St` for `Ln=1..Nl`;
4. N2O nitrification layer formation amount as already reconstructed locally from the current nitrification source, equivalent before its existing reporting threshold to `QPrN2Onit(Ln) * St`;
5. total N2O atmosphere-boundary emission amount from `(QEmN2ODif + QEmN2OFlw) * St`.

Production, reduction, storage and atmosphere emission remain distinct physical quantities. `QRdN2O` is not an observer producer for `N2Od` or `N2Oe`; it is a separate physical N2O-to-N2 reduction sink and is already reported separately by `Outsel`.

The parent TCD therefore requires canonical child-atom routing before any admission-readiness work. The proposed child atoms are provisional only in this workunit. RUNTIMEQ03 does not allocate canonical child identifiers.

## 1. Frozen source identity

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Relevant frozen file identities:

| file | SHA-256 |
| --- | --- |
| `Outbal_calc.for` | `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981` |
| `Outbal_write.for` | `cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea` |
| `Outsel.for` | `b058b88aef464183aa35bdb0377315e3755192e5ee70bb88db6522cf1311ec9d` |
| `ghg_ch4.for` | `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98` |
| `ghg_n2o.for` | `493bf88d4b321df64817a7c0eaa2725ad614a45df0a0f16cefa96ac348254175` |
| `outbal2.inc` | `dcf8458f3609af685f1058a378df4c4fab5a23406c573913cbd882a0a06921aa` |
| `Animo.for` | `352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7` |
| `Animo.inc` | `0f8b58e522ac2cdae95e8ae727dbf3ecea942e39c4d117b6bcae955d80fb69a2` |

Authorities checked live at start:

- `ANIMO-RUNTIMEQ02@45e8073fa95035b3565bd8b373ac327915cf1af5`;
- `ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6`;
- `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88`;
- `ANIMO-BUILDQ04@0ae1e58f80ca01c1b6eced7ac0d6e5c031827676`;
- canonical routing `ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`.

No `ANIMO-RUNTIMEQ03` or other later TCD-037 branch was present at start. No later RG05 aggregate than RG05G was present.

## 2. Observer labels establish the required accounting meanings

`outbal2.inc:19` explicitly documents the GHG slot suffixes:

`f = formation; e = emission`.

`Outbal_write.for` then emits:

- `Bfom/Bahu/Bdom(CH4f)` under `Dissimilated - CH4`;
- `Btom(CH4e)` under `Emission to air ... CH4`;
- `Banh(N2On)` and `Bani(N2Od)` under `N2O-evolution: ... from nitrification / as denitrification`;
- `Bani(N2Oe)` under `N2O-emission (total) to air`.

The organic-matter balance header is `Org.matter (kg/ha)`. That is why the CH4-C amount is divided by `Cfracom` before entering the organic-matter balance. This unit conversion does not make production and atmosphere emission the same physical quantity.

These labels are stronger semantic evidence than the local `Am...` variable names. RUNTIMEQ03 therefore follows consumer meaning, not naming convention.

## 3. Independent source-owned GHG quantities already exist

### CH4

`ghg_ch4.for::CH4produc` documents `QPrCH4` as CH4 production rate in `kg C m-2 d-1` and calculates it per soil layer.

`GHG_Methane` separately calculates atmosphere-boundary CH4 emission rates:

- `QEmCH4Dif` diffusion;
- `QEmCH4Ebl` ebullition;
- `QEmCH4Flw` air-flow advection;
- `QEmCH4Plt` plant-mediated emission.

`Outsel.for` independently confirms the output contract:

- layer CH4 production is written as `St * QPrCH4(Ln)`;
- total CH4 atmosphere emission is written as `(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt) * St`.

Therefore the layer producer and atmosphere-boundary producer are source-defined and distinct.

### N2O

`ghg_n2o.for` documents and calculates:

- `QPrN2Onit` as nitrification N2O production;
- `QPrN2Oden` as denitrification N2O production;
- `QRdN2O` as N2O reduction;
- `QEmN2ODif` and `QEmN2OFlw` as atmosphere emission by diffusion and air-flow advection.

`Outsel.for` again separates these quantities explicitly. For total-profile output it writes:

- total N2O emission `(QEmN2ODif+QEmN2OFlw)*St`;
- total N2O production split into denitrification and nitrification from sums of `QPrN2Oden*St` and `QPrN2Onit*St`;
- total N2O reduction from `QRdN2O*St`.

The same source therefore rejects any interpretation that production, reduction and emission are interchangeable observer inputs.

## 4. Layer semantics are qualified

### CH4 layer formation

`Outbal_calc.for:636` reads `AmCH4(Ln)` while calculating CH4 formation contributions to `Bfom(CH4f)`, `Bahu(CH4f)` and `Bdom(CH4f)`. The surrounding code partitions ordinary organic-matter dissimilation between CH4 and CO2 reporting.

The required layer quantity is therefore CH4 formation during the accepted timestep:

`CH4_FORMATION_AMOUNT(Ln) = QPrCH4(Ln) * St`.

It is a timestep amount, not persistent state and not atmosphere emission.

### N2O denitrification layer formation

`Outbal_calc.for:1133` writes `Bani(N2Od)` from `AmN2Odeni(Ln)`. The writer label defines this as N2O evolution from denitrification.

The exact source owner is:

`N2O_DENITRIFICATION_FORMATION_AMOUNT(Ln) = QPrN2Oden(Ln) * St`.

### N2O nitrification layer formation

`Outbal_calc.for:186-191` already reconstructs `AmN2Onitr(Ln)` from `FrNitrN2O`, `Rekinh`, `Avconh`, `Mofr`, `He` and `St`. `ghg_n2o.for:93-95` defines `QPrN2Onit` from the same source expression without `St`.

Before the existing observer threshold, the identity is:

`AmN2Onitr(Ln) = QPrN2Onit(Ln) * St`.

RUNTIMEQ03 does not change or approve the existing `<1e-8` reporting truncation. That is outside the missing-producer correction scope.

## 5. CH4 index 0 is semantically overloaded

The same `AmCH4(0)` is used by two different accounting statements at `Outbal_calc.for:653-655`:

1. `Btom(CH4e)` is explicitly labeled atmosphere CH4 emission;
2. `Btom(CO2e)` is calculated as total dissimilated organic matter minus the same CH4-equivalent amount.

Those two uses do not have one generally valid physical owner.

For the CH4 emission line, the source-qualified owner is:

`CH4_ATMOSPHERE_EMISSION_AMOUNT = (QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt) * St`.

For partitioning total organic-matter dissimilation into CH4 versus non-CH4 formation, the source-qualified CH4 term is instead the total CH4 formation amount:

`CH4_FORMATION_TOTAL = sum(QPrCH4(1:Nl) * St)`.

These quantities need not be equal because the physical GHG subsystem contains dynamic CH4 storage and CH4 oxidation before atmosphere transfer. GHG01 explicitly qualifies CH4 gas state as a real dynamic store and identifies the wider full-C-ledger/control-volume gap separately.

Therefore:

`AmCH4(0) = one scalar with both meanings`

is not a valid explicit ownership contract.

RUNTIMEQ03 does not repair the wider CO2 ledger or inactive `GHG_Miner` path. It only establishes that later TCD-037 correction must separate CH4 formation accounting from atmosphere emission accounting rather than hide both behind one index-0 value.

## 6. N2O index 0 has a direct consumer mismatch

`Outbal_calc.for:191` sets:

`AmN2Onitr(0) = sum(AmN2Onitr(1:Nl))`.

That is total nitrification N2O **production** for the timestep, subject to the local reporting threshold.

Later `Outbal_calc.for:1134-1135` uses:

`AmN2Odeni(0) + AmN2Onitr(0)`

for `Bani(N2Oe)`, whose writer label is total N2O **emission to air**.

The same source has an independent actual atmosphere-emission owner:

`N2O_ATMOSPHERE_EMISSION_AMOUNT = (QEmN2ODif + QEmN2OFlw) * St`.

Because N2O is a dynamic gas store and has explicit reduction `QRdN2O`, total production is not generally equal to total atmosphere emission in one timestep.

`Outsel.for` provides an additional source-side discriminator. It reports total N2O emission directly from the `QEm...` boundary fluxes and reports production and reduction separately. For annual attribution it may distribute emitted N2O between denitrification and nitrification according to production shares, but the total emitted amount remains the `QEm...` boundary total.

Therefore the `Bani(N2Oe)` consumer must be owned by the atmosphere-boundary emission total, not by a sum of production totals.

This is not a storage-duration issue. It is an observer semantic collision exposed after storage ownership was removed.

## 7. `QRdN2O` is deliberately excluded from the TCD-037 producer map

`QRdN2O` removes N2O from the modeled gas system by reduction to N2. It is neither N2O production nor atmosphere emission.

RUNTIMEQ03 includes `QRdN2O` in the ownership graph only as a discriminator proving that production and emission need not close instantaneously. No TCD-037 correction should map `QRdN2O` into the `N2Od`, `N2On` or `N2Oe` observer fields.

This preserves the separate GHG physical-process semantics and avoids accidental composition with other GHG discrepancies.

## 8. B1 semantic discriminator

`tools/runtimeq03/runtimeq03_accounting_semantics_probe.f90` is a bounded source-shaped diagnostic. It does not emulate the complete GHG model and is not historical reference evidence.

The probe supplies independently different but finite:

- CH4 layer production rates;
- CH4 atmosphere-emission components;
- N2O denitrification and nitrification production rates;
- N2O reduction rate;
- N2O atmosphere-emission components.

It verifies that:

- CH4 layer formation amount is `QPrCH4*St`;
- total CH4 formation and total CH4 atmosphere emission can differ;
- N2O denitrification layer formation is `QPrN2Oden*St`;
- total N2O production and total atmosphere emission can differ;
- the existing local nitrification layer amount has the `QPrN2Onit*St` meaning before its current threshold;
- the observer mapping leaves independent physical sentinel state unchanged.

GNU Fortran 14.2.0 O0 and O2 outputs are byte-identical.

Probe source SHA-256:

`e0da47422092896c7f3b2ab6b81070fb25e9907424ca51808b6a906ae76c0a47`

Expected output SHA-256:

`e734b3f90a7a86e7708a34ee309a71f2cd6d677f360e6cb87b0d394e44e2114b`

Evidence class:

`B1_SYNTHETIC_ACCOUNTING_SEMANTIC_DISCRIMINATOR_NOT_B2`.

## 9. Active-GHG evidence boundary

The supplied `GHGMais` testcase remains incompatible with the frozen revision-53 parser/input contract. RUNTIMEQ03 does not translate it.

Natural active-GHG execution remains:

`BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`.

The lack of a compatible natural case does not reopen the now source-complete producer semantics, but it matters for any later GOV04 Tier-A waiver. A later readiness workunit must evaluate the strengthened activation requirement explicitly and may not treat this same-context synthetic probe as an independent natural-runtime substitute.

Historical Intel behaviour remains `UNKNOWN`.

## 10. Expected-difference surfaces for later atomic corrections

RUNTIMEQ03 freezes structural, not historical-numeric, expected-difference whitelists. Historical values of the disconnected locals are not qualified.

### Candidate A: CH4 layer formation observer input

Allowed observer fields:

- `Bfom(CH4f)`;
- `Bahu(CH4f)`;
- `Bdom(CH4f)`;
- the associated `Bfom(CO2f)`, `Bahu(CO2f)`, `Bdom(CO2f)` partition fields that use the same per-layer CH4 formation amount.

Forbidden differences:

all physical CH4 state, CH4 process fluxes, hydrology, solver state, restart state and non-GHG process outputs.

### Candidate B: CH4 index-0 semantic split

Allowed observer fields:

- `Btom(CH4e)` from source-owned CH4 atmosphere emission;
- `Btom(CO2e)` only insofar as the existing legacy dissimilation complement is separated from the CH4 emission scalar and supplied with its formation-side CH4 amount.

This candidate does not assert that the legacy `Btom(CO2e)` field constitutes a model-wide physically complete CO2 ledger. GHG01's wider gas-store/source-pool ledger gaps remain separate.

### Candidate C: N2O denitrification formation observer input

Allowed observer field:

- `Bani(N2Od)`.

### Candidate D: N2O total atmosphere-emission observer input

Allowed observer field:

- `Bani(N2Oe)`.

`Banh(N2On)` per-layer production accounting is not changed by this candidate. The existing local reporting threshold is preserved unless a separately governed numerical/reporting workunit addresses it.

Across all candidates:

`EXPECTED_PHYSICAL_STATE_DIFFERENCE = NONE`

`EXPECTED_PROCESS_FLUX_DIFFERENCE = NONE`

`EXPECTED_RESTART_STATE_DIFFERENCE = NONE`

`EXPECTED_SOLVER_OR_NUMERICAL_POLICY_DIFFERENCE = NONE`

## 11. Atomicity and proposed child map

TCD-037 as currently registered describes one observer-interface phenomenon, but RUNTIMEQ03 proves at least four distinct atomic correction claims with different producer/consumer contracts.

Proposed child candidates for canonical routing, names provisional until B3 intake:

| proposed child | atomic claim | default qualification class | provisional GOV04 risk |
| --- | --- | --- | --- |
| `TCD-037-A1` | CH4 layer formation amount producer for `CH4f/CO2f` partition | `A_ACCOUNTING_REPORTING_ONLY` | Tier A candidate |
| `TCD-037-A2` | separate CH4 formation-total and atmosphere-emission semantics at index 0 | `A_ACCOUNTING_REPORTING_ONLY` | Tier A candidate |
| `TCD-037-A3` | N2O denitrification layer formation amount producer for `N2Od` | `A_ACCOUNTING_REPORTING_ONLY` | Tier A candidate |
| `TCD-037-A4` | total N2O atmosphere-emission owner for `N2Oe`, rejecting production-total substitution | `A_ACCOUNTING_REPORTING_ONLY` | Tier A candidate |

These identifiers are **not canonical** in RUNTIMEQ03. They are an atomization proposal only.

No new top-level TCD is proposed. All four claims remain children of canonical TCD-037 because they arise from the same disconnected/overloaded GHG balance-observer interface.

## 12. GOV04 classification after semantic qualification

RUNTIMEQ02 conservatively classified TCD-037 as Tier C because source/accounting ownership was scientifically ambiguous. RUNTIMEQ03 removes that particular ambiguity.

For each proposed atomic correction above, the qualified direction is observer-only:

- no physical-state write;
- no process-flux write;
- no restart/checkpoint state;
- no solver/tolerance/numerical-policy change;
- no runtime physical branch change;
- exact source-owned accounting quantity identified;
- bounded expected-difference surface identified.

Therefore each proposed child is a **GOV04 Tier-A candidate**.

The parent TCD itself is not Tier-A-admission-ready because the Tier-A waiver requires an atomic claim and RUNTIMEQ03 has proven the parent correction surface is compound. Parent-level Tier-A waiver is:

`NOT_AVAILABLE_AT_PARENT_SCOPE_ATOMIZATION_REQUIRED`.

A later canonical routing workunit may qualify the child map. Each child readiness workunit must then independently re-evaluate every GOV04 Tier-A waiver predicate. In particular, natural active-GHG evidence is unavailable and the current synthetic discriminator was authored in this qualification context, so no later workunit may assume that the strengthened synthetic-activation independence predicate is already satisfied.

## 13. Result and next routing

RUNTIMEQ03 qualifies:

- exact source owners for CH4 formation, CH4 atmosphere emission, N2O denitrification formation, N2O nitrification formation, N2O reduction and N2O atmosphere emission;
- CH4 layer formation mapping `QPrCH4*St`;
- N2O denitrification layer mapping `QPrN2Oden*St`;
- local nitrification amount identity `QPrN2Onit*St` before the existing reporting threshold;
- CH4 index-0 formation-versus-emission semantic overload;
- N2O index-0 production-versus-emission consumer mismatch;
- observer-only expected-difference surfaces;
- no legitimate persistent or restart ownership;
- no need to compose TCD-032..036 to define the TCD-037 observer inputs;
- provisional Tier-A classification for the resulting atomic observer corrections.

RUNTIMEQ03 does not qualify:

- a production patch;
- historical Intel output values;
- a complete GHG C or N mass ledger;
- GHG source-pool corrections;
- the existing nitrification reporting threshold;
- canonical child identifiers;
- any scientific admission.

Exact next workunit:

`ANIMO-B3I07 — TCD-037 GHG Balance Observer Child-Atom Routing & Tier-A Readiness Partition`

B3I07 should consume RUNTIMEQ02 and RUNTIMEQ03, decide the canonical child map under B3Q01/B3Q02 governance, keep the top-level TCD register unchanged, and state the exact readiness workunit for each admitted routing child. It must not itself admit a child unless the then-live governance contract explicitly authorizes such a combined routing/admission action, which is not assumed here.

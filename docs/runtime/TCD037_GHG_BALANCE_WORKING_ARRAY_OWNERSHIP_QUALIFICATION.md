# TCD-037 GHG balance working-array ownership qualification

Work unit: `ANIMO-RUNTIMEQ02`

Status: `QUALIFIED_SOURCE_RUNTIME_OWNERSHIP_TIER_C_ACCOUNTING_SEMANTICS_PENDING`

## Decision

Revision-53 source defines no valid producer for `Outbal_calc` local arrays `AmCH4` and `AmN2Odeni` before their first active reads. They are not formal arguments, are not assigned anywhere under those symbols in active frozen source, and are read only when `IoptGHG >= 1`.

Their source-defined status is therefore not “persistent working arrays”. It is:

`PROCEDURE_LOCAL_UNDEFINED_ON_ENTRY_WITH_NO_SOURCE_PRODUCER`

Any value obtained from stack reuse, static compiler storage, `/Qsave`, neighboring activation records or other storage-duration behavior would be incidental runtime state. Because the source contains no fresh writer under either symbol, persistence cannot repair ownership. At best it can preserve an old or indeterminate value.

`AmN2Onitr` is different. It is procedure-local scratch, explicitly reconstructed in every active `Outbal_calc` invocation from current timestep quantities before its observer reads. It is the positive control showing that revision 53 knows how to build an observer-local timestep amount when the producer is present.

This resolves the runtime/lifetime question but does not resolve the intended CH4 and denitrification-N2O accounting mapping. TCD-037 is therefore not admission-ready in this work unit.

## 1. Source identity and canonical scope

Frozen source archive:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Frozen `Outbal_calc.for`:

`4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`

Canonical routing authority at qualification start:

`ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9`

Canonical TCD-037 remains the GHG balance observer working-array interface defect. This work unit does not touch TCD-032..036 and does not change the canonical register.

## 2. Complete working-array inventory

A source-wide whole-token inventory over revision-53 Fortran and include files gives the following active ownership surface.

| symbol | declaration | active writers | active readers | formal argument | qualified result |
| --- | --- | --- | --- | --- | --- |
| `AmCH4` | `Outbal_calc.for:140` | none | `636`, `653` | no | undefined at first active read |
| `AmN2Odeni` | `Outbal_calc.for:140` | none | `1133`, `1135` | no | undefined at first active read |
| `AmN2Onitr` | `Outbal_calc.for:141` | `186`, conditional rewrite `188`, aggregate write `191` | local accumulation at `188-189`, observer reads `1132`, `1135` | no | refreshed active-call scratch |

A commented historical declaration fragment at `Outbal_calc.for:163` is not active code and is not counted as a producer.

The apparent “Formal Variables” comment above the declarations is not authority. The actual subroutine argument list at `Outbal_calc.for:10-52` passes only `IoptGHG`, `Btom`, `Cfracom` and `FrNitrN2O` on the relevant GHG observer interface. None of the three `Am...` arrays appears in that argument list.

The only main-program call, `Animo.for:987-1032`, likewise supplies no `AmCH4`, `AmN2Odeni` or physical CH4/N2O production arrays to `Outbal_calc`.

### First write before first read

`AmCH4`: **FAIL in source**. No write exists before `Outbal_calc.for:636`.

`AmN2Odeni`: **FAIL in source**. No write exists before `Outbal_calc.for:1133`.

`AmN2Onitr`: **PASS in source**. Each active call writes all `1..Nl` elements at `186`, applies its threshold at `188`, accumulates them, and writes element `0` at `191` before the balance reads at `1132` and `1135`.

## 3. Producer -> lifetime -> consumer ownership graph

### `AmCH4`

`NO SOURCE PRODUCER`

→ procedure-local storage allocated for an `Outbal_calc` invocation

→ no initialization and no caller transfer

→ active first read `AmCH4(Ln)` at `636`

→ local `OmCH4`

→ reporting/balance accumulators `Bfom(CH4f)`, `Bahu(CH4f)`, `Bdom(CH4f)`

and, for `Ln=1`:

→ active read `AmCH4(0)` at `653`

→ `Btom(CH4e)` and `Btom(CO2e)` observer terms.

Qualified lifetime: `NO_VALID_VALUE_LIFETIME_EXISTS_IN_SOURCE`.

### `AmN2Odeni`

`NO SOURCE PRODUCER`

→ procedure-local storage allocated for an `Outbal_calc` invocation

→ no initialization and no caller transfer

→ active read `AmN2Odeni(Ln)` at `1133`

→ `Bani(N2Od)` observer term

and, for `Ln=1`:

→ active read `AmN2Odeni(0)` at `1135`

→ combined `Bani(N2Oe)` observer term.

Qualified lifetime: `NO_VALID_VALUE_LIFETIME_EXISTS_IN_SOURCE`.

### `AmN2Onitr`

current accepted timestep state and rates (`FrNitrN2O`, `Rekinh`, `Avconh`, `Mofr`, `He`, `St`)

→ `Outbal_calc` per-layer write at `186`

→ thresholding at `188`

→ call-local accumulation

→ index-0 aggregate write at `191`

→ `Banh(N2On)` and the combined `Bani(N2Oe)` observer terms.

Qualified lifetime: `ACTIVE_OUTBAL_CALL_LOCAL_TIMESTEP_AMOUNT_SCRATCH`.

It is not iteration state and not persistent model state.

## 4. Reachability and GHG activation

`Outbal_calc` is called from the main timestep route. The suspect reads are guarded by `IoptGHG >= 1`. With GHG inactive, the CH4 and N2O working-array reads are not reached. With GHG active, the source reaches them without an intervening producer for `AmCH4` or `AmN2Odeni`.

The frozen testbank does not currently provide a revision-53-compatible natural active-GHG case. GHG01 established that the supplied `GHGMais` contract belongs to a different input-schema lineage: revision 53 requests `>outGHG:` and other fields that are absent or structurally different. RUNTIMEQ02 does not fabricate a translated case.

Natural active-GHG runtime evidence is therefore:

`BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`

This does not prevent source ownership qualification because the missing producer is source-complete and the active control branch is explicit. Runtime causality is additionally checked with a bounded source-shaped B1 discriminator.

## 5. Multi-call lifetime and stale-state discriminator

`tools/runtimeq02/runtimeq02_observer_lifetime_probe.f90` deliberately separates two questions.

The source-like diagnostic has local `AmCH4` and `AmN2Odeni` with no `SAVE`. Under GNU automatic local storage with signaling-NaN initialization:

- inactive GHG does not touch the suspect arrays;
- the first active read exposes both missing values as NaN;
- an instrumented one-call seed can make one call finite;
- a later active call has no source-like producer and again exposes invalid values;
- the locally computed nitrification comparison term is refreshed from the changed timestep length.

A counterfactual diagnostic then adds explicit `SAVE` only to the two missing arrays. A seeded value survives into a later call even though that later call has no fresh producer. The persisted CH4/denitrification values remain stale while the independently reconstructed nitrification amount changes with the timestep.

The counterfactual is not a proposed repair. It proves why silent persistence is not ownership.

The deterministic O0/O2 probe contract is:

- `INACTIVE_OK T`
- `FIRST_READ_EXPOSED T`
- `AUTOMATIC_REPEAT_NOT_PERSISTENT T`
- `PERSISTENCE_STALE_REUSE T`
- `NITR_STEP_REFRESH T`
- `PHYSICAL_UNCHANGED T`

## 6. Physical producer candidates exist, but mapping is not yet qualified

The GHG process subsystem has explicit physical arrays with different names and ownership. Examples include:

- `QPrCH4` from methane production;
- `QPrN2Oden` from denitrification-related N2O production;
- `QPrN2Onit` from nitrification-related N2O production;
- `QRdN2O` for N2O reduction;
- `QEmCH4Dif`, `QEmCH4Ebl`, `QEmCH4Flw`, `QEmCH4Plt` and N2O emission fluxes.

`Outsel.for` already converts physical production rates to timestep amounts using `QPr... * St` for GHG output. This is strong evidence that the missing observer arrays should not be invented from compiler-local persistence.

It is not enough to declare the eventual TCD-037 correction as `AmCH4 = QPrCH4*St` and `AmN2Odeni = QPrN2Oden*St` without further qualification. The observer also assigns special meaning to element `0`, including terms labeled as CH4 and N2O emission. Production, reduction, storage and atmosphere-boundary transfer are distinct physical concepts. The exact layer-0 aggregation and emission attribution must be reconciled against the process flux owners and balance identity before an expected-difference whitelist can be frozen.

Therefore exact accounting ownership remains:

`UNRESOLVED_INDEX0_AND_EMISSION_MAPPING`

## 7. Observer non-interference

Within the TCD-037 seam, the suspect local-array reads feed local arithmetic and balance/report accumulators. No path from `AmCH4`, `AmN2Odeni` or `AmN2Onitr` writes back into CH4/N2O process state, hydrological state, process rates or solver state.

The B1 discriminator holds independent physical sentinel state byte-for-byte unchanged across inactive, active, repeated-call and counterfactual-persistence calls.

Qualified scoped result:

`OBSERVER_SEAM_DOES_NOT_MUTATE_PHYSICAL_OWNER_STATE`

This is a scoped non-interference result. It does not claim that every operation performed by the whole `Outbal_calc` routine is a pure mathematical function, because it intentionally updates balance accumulator state.

## 8. Restart and checkpoint semantics

Neither missing working array has a legitimate persistent owner in revision 53. Neither is passed as restart state, and neither should be promoted to checkpointed ANIMO5 `ModelState` merely to reproduce compiler-local memory behavior.

Qualified result:

- `AmCH4`: `NOT_CHECKPOINT_STATE`;
- `AmN2Odeni`: `NOT_CHECKPOINT_STATE`;
- `AmN2Onitr`: `NOT_CHECKPOINT_STATE`, recomputable observer-local timestep scratch.

This is consistent with BUILDQ03's broader result that hidden GHG task context must not be wholesale converted into persistent physical ModelState. TCD-037 remains a distinct observer-interface problem.

## 9. Expected-difference contract

For **this qualification branch**:

`EXPECTED_PRODUCTION_DIFFERENCE = NONE`

No production source is changed, so model runtime output must not change.

For a **future TCD-037 correction**:

`EXPECTED_DIFFERENCE_WHITELIST = BLOCKED_PENDING_ACCOUNTING_SEMANTICS`

A future whitelist must be frozen before correction qualification and must state exactly which CH4/N2O balance fields may change, by which source-owned quantity, with no physical-state or process-flux change. RUNTIMEQ02 cannot honestly freeze that contract while layer-0 and emission mapping remain unresolved.

## 10. GOV04 risk classification

Risk classification is made only after the ownership result above.

The seam is physically non-interfering and appears to be accounting/reporting-only in its current consumer direction. However the strengthened GOV04 Tier-A waiver requires exact accounting ownership, no unresolved source-meaning ambiguity and a reproducible expected-difference contract.

Those conditions are not met. Exact `AmCH4`/`AmN2Odeni` producer mapping, especially index `0`, remains scientifically ambiguous. GOV04 explicitly routes source/state ownership ambiguity with scientific consequences to Tier C.

Current classification:

`GOV04_TIER_C_RUNTIME_SOURCE_OWNERSHIP_AMBIGUITY`

This classification is conservative and fail closed. It does not assert a physical-state mutation. It records that the scientifically correct observer ownership cannot yet be selected without resolving process-versus-emission accounting semantics.

Tier-A waiver: `NOT_AVAILABLE`.

## 11. Qualification result and routing

RUNTIMEQ02 qualifies all of the following:

- complete literal writer and reader ownership for the three working arrays;
- failure of first-write-before-first-read for `AmCH4` and `AmN2Odeni`;
- call-local reconstruction of `AmN2Onitr`;
- active/inactive control-flow discrimination;
- no valid persistent lifetime for the missing arrays;
- causal stale-value risk if persistence is silently assumed;
- scoped observer non-interference;
- no restart/checkpoint ownership for the working arrays.

It does **not** qualify the exact accounting replacement mapping, an expected-difference whitelist for a correction, a Tier-A waiver, scientific admission or production change.

Exact next atomic work unit:

`ANIMO-RUNTIMEQ03 — TCD-037 GHG Balance Observer Accounting-Semantics & Index-0 Producer Mapping Qualification`

RUNTIMEQ03 should reconcile `QPrCH4`, `QPrN2Oden`, `QPrN2Onit`, `QRdN2O`, GHG storage and atmosphere-emission owners against every affected `Btom/Banh/Bani` slot, then freeze an exact expected-difference contract. It must remain source/evidence qualification unless the then-live GOV04 route explicitly permits more.

Because Tier-A conditions are **not** currently satisfied, a readiness/admission work unit cannot safely be combined with RUNTIMEQ02. Under the present Tier-C classification, a genuinely independent second-line review remains required before any later scientific admission unless a later qualified ownership result legitimately changes the risk classification under GOV04.
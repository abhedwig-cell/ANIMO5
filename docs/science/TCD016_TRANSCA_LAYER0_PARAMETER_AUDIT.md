# TCD-016 adjacent audit: Transca layer-0 parameter initialization

Work unit: `ANIMO-SQ01`

Status: `SOURCE_STATIC_INITIALIZATION_GAP_CONFIRMED_RUNTIME_EFFECT_NOT_QUALIFIED`

Relation to TCD-016: `SCOPE_GUARD_SUPPORT_ONLY`

Production migration: `NOT_ADMITTED`

## 1. Why this audit was needed

The shared-solute reachability audit found that soluble organic matter, soluble organic N and soluble organic P can enter the same layer-0 `Transport -> Transsub` route as NH4 when ponding is active.

It also found that their `Transca.for` calls use arrays whose ordinary physical meaning belongs to soil layers. Before claiming that DOM, DON or DOP reproduce TCD-016, SQ01 therefore checked whether the revision-53 source explicitly defines those parameters at index 0.

Frozen source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

The archive was re-hashed before this audit and was not modified.

## 2. `Transca` consumes index 0

`Transca.for` declares and loops the following arrays over `0:Nl`:

- `Recfca(0:manl)`;
- `Recfpddiorma(0:manl)`;
- `Recfpddiorni(0:manl)`;
- `Recfpddiorpo(0:manl)`;
- `Rhbd(0:manl)`;
- `Socfdom(0:manl)`.

For soluble organic matter it executes, for every `Ln=0..Nl`:

```fortran
Reko(Ln) = Recfpddiorma(Ln)
Reki(Ln) = -Recfca(Ln)
Co(Ln)   = Codiorma(Ln)
```

and then passes `Rhbd` and `Socfdom` to `Transport`.

The corresponding organic-N and organic-P routes similarly pass layer-indexed process arrays through the same layer-0 transport interface.

Thus index 0 is not merely present in a declaration. It is source-reachable when `Flpn=1`.

## 3. Source assignments are soil-layer only

A whole-source assignment scan of the frozen archive found the following explicit writes.

### 3.1 First-order DOM decomposition coefficient

`Rates.for` defines `Recfca(Ln)` inside:

```fortran
Do Ln = 1,Nl
   ...
   Recfca(Ln) = Recfcaav * Help * RdFaRecfca
End Do
```

and later applies the oxygen reduction factor again only for:

```fortran
Do Ln = 1,Nl
   Recfca(Ln) = Recfca(Ln) * Rdfaox(Ln)
End Do
```

No explicit assignment to `Recfca(0)` was found in the frozen source.

### 3.2 Zero-order DOM/N/P production terms

Both `Rates1` and `Rates2` set and accumulate:

- `Recfpddiorma(Ln)`;
- `Recfpddiorni(Ln)`;
- `Recfpddiorpo(Ln)`;

inside `Do Ln = 1,Nl` loops.

No explicit writes to index 0 of these arrays were found.

### 3.3 Bulk density and DOM sorption coefficient

`Inicalc.for` maps horizon properties to layers only inside:

```fortran
Do Ln = 1,Nl
   Rhbd(Ln)   = Rhbdho(Lnhn(Ln))
   Socfdom(Ln)= Socfdomho(Lnhn(Ln))
   ...
End Do
```

No explicit source assignment to `Rhbd(0)` or `Socfdom(0)` was found.

## 4. What is and is not established

The source-bound statement is:

`TRANSA_LAYER0_PROCESS_PARAMETER_VALUES_ARE_NOT_EXPLICITLY_DEFINED_BY_THE_REVISION53_ASSIGNMENT_PATHS_AUDITED_HERE`.

This is stronger than merely saying the values are conceptually soil-derived.

It is **not** yet equivalent to either of the following claims:

- `the historical executable necessarily used random values at index 0`;
- `DOM/DON/DOP necessarily suffer a TCD-016 mass deletion`.

Why not:

1. Fortran does not give these uninitialized variables a portable scientific value merely because they reside in the main program, but compiler/linker/runtime behaviour can make storage appear zero in a particular executable.
2. SQ01 has not yet captured the index-0 runtime values from the authoritative historical executable/toolchain.
3. Species-specific `Reki`, `Reko`, sorption and storage coefficients alter the `Transsub` analytical-solution class and mass terms.
4. The supplied historical testbank has not been qualified here for a natural DOM/DON/DOP dry-down event analogous to the NH4 case.

Therefore the correct evidence label is:

`SOURCE_STATIC_INITIALIZATION_GAP_CONFIRMED_RUNTIME_EFFECT_NOT_QUALIFIED`.

## 5. Compiler diagnostic boundary

SQ01 attempted a read-only GNU build of the frozen source in an external temporary directory to explore whether a run-time initialization diagnostic could be made without editing source bytes.

The complete revision-53 tree did not compile directly under the available GNU invocation because the legacy Windows/Intel-oriented source has portability/interface issues beyond this audit, including case-sensitive include naming and compile errors in the supplied transport source under that invocation.

That failed build is **not** evidence about the index-0 runtime values and is not used to classify a defect.

No source file was modified to force compilation.

## 6. Consequence for shared-solute scope

The earlier conservative-equation proof remains clean for mineral phosphorus layer 0 because `Transgen` explicitly passes zero reaction, zero sorption and zero bulk-density contributions to `Transsub` at `Ln=0`.

The same proof must **not** be transferred to DOM/DON/DOP until index-0 process semantics are established.

Therefore the shared-solute matrix remains:

- NH4: observed and reproduced TCD-016 defect;
- mineral P: source-confirmed structural reachability of the conservative low-storage deletion branch, historical activation not established;
- NO3: shared seam reachable, exact deletion conditional on reaction coefficients;
- DOM/DON/DOP: shared route reachable, but layer-0 parameter semantics are source-incomplete and runtime behaviour is unqualified.

No new TCD is opened by this audit.

## 7. Governance consequence

This adjacent finding should be handed to the broader source-defect/evidence-governance process only as a candidate investigation item.

Before it could become a discrepancy record it would require, at minimum:

- authoritative runtime/toolchain reconstruction or an independently reproducible diagnostic showing the actual index-0 values;
- a natural or synthetic causal case separating initialization from the TCD-016 representation seam;
- a conservation/state consequence;
- atomization from TCD-016 if the issue proves independent.

SQ01 deliberately does not fold a possible initialization defect into the TCD-016 Class-C correction.

## 8. Current disposition

`TRANSCA_LAYER0_STATIC_PARAMETER_INITIALIZATION = SOURCE_INCOMPLETE`

`RUNTIME_EFFECT = NOT_QUALIFIED`

`NEW_TCD = NO`

`TCD-016_SCOPE = UNCHANGED`

`PRODUCTION_MIGRATION = NOT_ADMITTED`
